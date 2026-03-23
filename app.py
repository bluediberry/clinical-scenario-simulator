"""Standalone interactive simulation walkthrough of clinical scenarios.

This is a self-contained Streamlit app that can be deployed independently.
Scenarios are loaded from the bundled `scenarios/` folder or uploaded as JSON.
"""

import json
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Clinical Scenario Simulator",
    page_icon="\U0001f3ae",
    layout="wide",
)

from html import escape as _esc  # noqa: E402

from scenario_viewer import (  # noqa: E402
    REVIEW_CSS,
    build_action_index,
    compute_action_duration,
    compute_simulation_score,
    format_minutes_as_hours,
    match_common_errors,
    render_action_card_interactive,
    render_debriefing_point,
    render_patient_profile,
    render_time_tracker,
    render_vital_signs,
)
from theme import apply_theme, page_header, section_label  # noqa: E402

apply_theme()
st.markdown(REVIEW_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Scenario loading (simplified — no Firestore, no settings)
# ---------------------------------------------------------------------------
SCENARIOS_DIR = Path(__file__).parent / "scenarios"


def _load_bundled_scenarios() -> list[dict]:
    """Load all JSON scenario files from the bundled scenarios/ folder."""
    entries: list[dict] = []
    if not SCENARIOS_DIR.exists():
        return entries
    for path in sorted(SCENARIOS_DIR.glob("*.json")):
        try:
            with open(path, encoding="utf-8") as f:
                scenario = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(scenario, dict):
            entries.append({
                "data": scenario,
                "source": "Bundled",
                "title": scenario.get("title", path.stem),
                "scenario_id": path.stem,
            })
    return entries


def _format_label(entry: dict) -> str:
    """Format a scenario entry label for the selector."""
    title = entry.get("title", "Untitled")
    source = entry.get("source", "Unknown")
    scenario_id = entry.get("scenario_id", "?")
    return f"[{source}] {title} ({scenario_id})"


# ---------------------------------------------------------------------------
# Session state defaults
# ---------------------------------------------------------------------------
_DEFAULTS: dict[str, object] = {
    "sim_scenario_data": None,
    "sim_phase": "select",       # select | briefing | play | branch | debrief
    "sim_stage_idx": 0,
    "sim_dp_idx": 0,
    "sim_selected_actions": {},   # dp_id -> set of action_ids
    "sim_elapsed_minutes": 0.0,
    "sim_dp_locked": False,
    "sim_completed_dps": [],
    "sim_active_branch_id": None,
    "sim_branch_dp_idx": 0,
    "sim_branch_selected": {},
    "sim_completed_branches": set(),
    "uploaded_scenarios": [],
}

for key, default in _DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default


def _reset_simulation():
    """Reset all simulation state."""
    uploaded = st.session_state.get("uploaded_scenarios", [])
    for key, default in _DEFAULTS.items():
        st.session_state[key] = default
    st.session_state.uploaded_scenarios = uploaded


# ---------------------------------------------------------------------------
# Phase indicator
# ---------------------------------------------------------------------------
_PHASES = ["select", "briefing", "play", "debrief"]
_PHASE_LABELS = {"select": "Select", "briefing": "Briefing", "play": "Simulation", "branch": "Branch", "debrief": "Debrief"}


def render_phase_indicator(current: str):
    parts = []
    for i, phase in enumerate(_PHASES):
        if i > 0:
            parts.append('<span class="sep">\u203a</span>')
        idx_current = _PHASES.index(current) if current in _PHASES else 2
        if _PHASES.index(phase) < idx_current:
            parts.append(f'<span class="phase done">{_PHASE_LABELS[phase]}</span>')
        elif phase == current or (current == "branch" and phase == "play"):
            parts.append(f'<span class="phase active">{_PHASE_LABELS.get(current, current)}</span>')
        else:
            parts.append(f'<span class="phase">{_PHASE_LABELS[phase]}</span>')
    st.markdown(f'<div class="sim-phase-indicator">{"".join(parts)}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helper: get current DP list from stage or branch
# ---------------------------------------------------------------------------

def _get_current_dps(scenario):
    """Return the list of decision points for the current context."""
    if st.session_state.sim_active_branch_id:
        for branch in scenario.get("branches", []):
            if branch.get("id") == st.session_state.sim_active_branch_id:
                return branch.get("decision_points", [])
        return []
    stages = scenario.get("stages", [])
    if st.session_state.sim_stage_idx < len(stages):
        return stages[st.session_state.sim_stage_idx].get("decision_points", [])
    return []


def _get_current_stage(scenario):
    stages = scenario.get("stages", [])
    if st.session_state.sim_stage_idx < len(stages):
        return stages[st.session_state.sim_stage_idx]
    return None


# ---------------------------------------------------------------------------
# PHASE: SELECT
# ---------------------------------------------------------------------------

def phase_select():
    page_header("Clinical Scenario Simulator", "Step-by-step interactive walkthrough of clinical scenarios")
    render_phase_indicator("select")

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload scenario JSON files",
        type=["json"],
        accept_multiple_files=True,
        help="Upload one or more scenario JSON files to simulate them.",
    )

    if uploaded_files:
        new_uploaded = []
        for uf in uploaded_files:
            try:
                scenario = json.load(uf)
                if isinstance(scenario, dict):
                    new_uploaded.append({
                        "data": scenario,
                        "source": "Uploaded",
                        "title": scenario.get("title", uf.name),
                        "scenario_id": uf.name.replace(".json", ""),
                    })
            except (json.JSONDecodeError, Exception):
                st.error(f"Could not parse {uf.name}")
        st.session_state.uploaded_scenarios = new_uploaded

    # Combine bundled + uploaded
    entries = _load_bundled_scenarios() + st.session_state.get("uploaded_scenarios", [])

    if not entries:
        st.warning("No scenarios available. Upload a scenario JSON file or add files to the scenarios/ folder.")
        return

    st.markdown("---")

    labels = [_format_label(e) for e in entries]
    selected_idx = st.selectbox("Choose a scenario", range(len(labels)), format_func=lambda i: labels[i])

    if selected_idx is not None:
        scenario = entries[selected_idx]["data"]

        # Quick preview
        with st.expander("Preview", expanded=False):
            st.markdown(f"**{scenario.get('title', 'Untitled')}**")
            st.markdown(f"{scenario.get('domain', '')} \u203a {scenario.get('subdomain', '')}")
            st.markdown(f"Difficulty: {(scenario.get('difficulty') or 'N/A').title()} | Duration: ~{scenario.get('estimated_duration_minutes', '?')} min")
            stages = scenario.get("stages", [])
            total_dps = sum(len(s.get("decision_points", [])) for s in stages)
            total_actions = sum(
                len(dp.get("available_actions", []))
                for s in stages for dp in s.get("decision_points", [])
            )
            st.markdown(f"{len(stages)} stage(s), {total_dps} decision points, {total_actions} actions")

        if st.button("Start Simulation", type="primary", use_container_width=True):
            st.session_state.sim_scenario_data = scenario
            st.session_state.sim_phase = "briefing"
            st.rerun()


# ---------------------------------------------------------------------------
# PHASE: BRIEFING
# ---------------------------------------------------------------------------

def phase_briefing():
    scenario = st.session_state.sim_scenario_data
    page_header("Clinical Scenario Simulator", scenario.get("title", ""))
    render_phase_indicator("briefing")

    # Patient profile
    patient = scenario.get("patient")
    if patient:
        section_label("Patient Profile")
        render_patient_profile(patient)
        st.markdown("")

    # Initial presentation
    presentation = scenario.get("initial_presentation")
    if presentation:
        section_label("Initial Presentation")
        st.info(presentation)

    # Interaction prompt
    prompt = scenario.get("interaction_prompt")
    if prompt:
        section_label("Your Role")
        st.markdown(prompt)

    # Time window
    tw = scenario.get("clinical_time_window")
    if tw:
        st.markdown("")
        section_label("Clinical Time Window")
        onset = format_minutes_as_hours(tw.get("symptom_onset_minutes_ago"))
        window = format_minutes_as_hours(tw.get("max_treatment_window_minutes"))
        remaining = format_minutes_as_hours(tw.get("remaining_window_minutes"))
        st.markdown(
            f'<div class="time-window-alert">'
            f"<strong>Symptom onset:</strong> {onset} ago &bull; "
            f"<strong>Treatment window:</strong> {window} &bull; "
            f"<strong>Remaining:</strong> {remaining}"
            f"</div>",
            unsafe_allow_html=True,
        )
        rationale = tw.get("time_pressure_rationale")
        if rationale:
            st.caption(rationale)

    # Learning objectives
    los = scenario.get("learning_objectives", [])
    if los:
        st.markdown("")
        section_label("Learning Objectives")
        for lo in los:
            if isinstance(lo, dict):
                st.markdown(f"- **{lo.get('id', '?')}:** {lo.get('description', '')}")

    st.markdown("---")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button("Begin Simulation", type="primary", use_container_width=True):
            st.session_state.sim_phase = "play"
            st.session_state.sim_stage_idx = 0
            st.session_state.sim_dp_idx = 0
            st.session_state.sim_dp_locked = False
            st.rerun()
    with col2:
        if st.button("Back", use_container_width=True):
            _reset_simulation()
            st.rerun()


# ---------------------------------------------------------------------------
# PHASE: PLAY (core simulation loop)
# ---------------------------------------------------------------------------

def phase_play():
    scenario = st.session_state.sim_scenario_data
    stage = _get_current_stage(scenario)
    dps = _get_current_dps(scenario)

    if not stage or not dps:
        st.session_state.sim_phase = "debrief"
        st.rerun()
        return

    dp_idx = st.session_state.sim_dp_idx
    if dp_idx >= len(dps):
        stages = scenario.get("stages", [])
        next_stage = st.session_state.sim_stage_idx + 1
        if next_stage < len(stages):
            st.session_state.sim_stage_idx = next_stage
            st.session_state.sim_dp_idx = 0
            st.session_state.sim_dp_locked = False
            st.rerun()
        else:
            st.session_state.sim_phase = "debrief"
            st.rerun()
        return

    dp = dps[dp_idx]
    dp_id = dp.get("id", "")
    actions = dp.get("available_actions", [])
    critical_ids = set(dp.get("critical_action_ids", []))
    locked = st.session_state.sim_dp_locked

    # --- Header ---
    page_header("Clinical Scenario Simulator", scenario.get("title", ""))
    render_phase_indicator("play")

    # --- Sidebar: vital signs + time tracker + always-available info ---
    with st.sidebar:
        st.markdown("### Simulation")
        st.caption(f"Stage: {stage.get('name', '?')}")
        st.caption(f"Decision Point {dp_idx + 1} of {len(dps)}")
        st.markdown("---")

        vs = stage.get("vital_signs")
        if vs:
            st.markdown("#### Vital Signs")
            render_vital_signs(vs)
            st.markdown("---")

        render_time_tracker(st.session_state.sim_elapsed_minutes, scenario.get("clinical_time_window"))

        always = scenario.get("always_available_information")
        if always:
            with st.expander("Always Available Info"):
                for k, v in always.items():
                    st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

    # --- DP Context ---
    st.markdown(
        f'<div class="sim-dp-header">'
        f'<div class="dp-label">Decision Point {dp_idx + 1} of {len(dps)} &bull; {_esc(str(dp_id))}</div>'
        f'<div class="dp-context">{_esc(dp.get("context", ""))}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # --- Actions ---
    section_label(f"{len(actions)} Available Actions")

    if dp_id not in st.session_state.sim_selected_actions:
        st.session_state.sim_selected_actions[dp_id] = set()

    current_selections = set()
    for action in actions:
        action_id = action.get("id", "")
        is_critical = (action.get("requirement") or "").lower() == "critical" or action_id in critical_ids
        selected = render_action_card_interactive(
            action=action,
            dp_id=dp_id,
            revealed=locked,
            disabled=locked,
            is_critical=is_critical,
        )
        if selected:
            current_selections.add(action_id)

    if not locked:
        st.session_state.sim_selected_actions[dp_id] = current_selections

    st.markdown("---")

    # --- Submit / Next buttons ---
    if not locked:
        if st.button("Submit Decisions", type="primary", use_container_width=True):
            st.session_state.sim_dp_locked = True
            for action in actions:
                if action.get("id", "") in st.session_state.sim_selected_actions.get(dp_id, set()):
                    st.session_state.sim_elapsed_minutes += compute_action_duration(action)
            st.session_state.sim_completed_dps.append(dp_id)
            st.rerun()
    else:
        feedback = dp.get("feedback_on_completion")
        if feedback:
            st.success(f"**Feedback:** {feedback}")

        selected_set = st.session_state.sim_selected_actions.get(dp_id, set())
        critical_hit = sum(1 for a in actions if (a.get("id") in critical_ids or (a.get("requirement") or "").lower() == "critical") and a.get("id") in selected_set)
        critical_total = sum(1 for a in actions if a.get("id") in critical_ids or (a.get("requirement") or "").lower() == "critical")

        if critical_total > 0:
            pct = critical_hit / critical_total * 100
            color_class = "success" if pct >= 80 else ("warning" if pct >= 50 else "danger")
            st.markdown(
                f'<div class="sim-score-card {color_class}" style="margin:0.5rem 0;">'
                f'<div class="score-value">{critical_hit}/{critical_total}</div>'
                f'<div class="score-label">Critical Actions Performed</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        _check_branch_triggers(scenario, dp, selected_set)

        if st.button("Next Decision Point", type="primary", use_container_width=True):
            st.session_state.sim_dp_idx += 1
            st.session_state.sim_dp_locked = False
            st.rerun()


def _check_branch_triggers(scenario, dp, selected_actions):
    """Check if any selected action triggers a branch, and offer to explore it."""
    branches = scenario.get("branches", [])
    if not branches:
        return

    for action in dp.get("available_actions", []):
        aid = action.get("id", "")
        if aid not in selected_actions:
            continue
        if not action.get("is_branch_trigger"):
            continue
        trigger = action.get("branch_trigger", {})
        branch_id = trigger.get("branch_id", "")
        if not branch_id or branch_id in st.session_state.sim_completed_branches:
            continue

        for branch in branches:
            if branch.get("id") == branch_id:
                st.warning(
                    f"Your action **{action.get('description', '')}** "
                    f"has triggered a branch: *{branch.get('trigger_context', '')}*"
                )
                if st.button(f"Explore Branch {branch_id}", key=f"branch_{branch_id}"):
                    st.session_state.sim_active_branch_id = branch_id
                    st.session_state.sim_branch_dp_idx = 0
                    st.session_state.sim_phase = "branch"
                    st.rerun()
                break


# ---------------------------------------------------------------------------
# PHASE: BRANCH
# ---------------------------------------------------------------------------

def phase_branch():
    scenario = st.session_state.sim_scenario_data
    branch_id = st.session_state.sim_active_branch_id

    branch = None
    for b in scenario.get("branches", []):
        if b.get("id") == branch_id:
            branch = b
            break

    if not branch:
        st.session_state.sim_phase = "play"
        st.session_state.sim_active_branch_id = None
        st.rerun()
        return

    dps = branch.get("decision_points", [])
    dp_idx = st.session_state.sim_branch_dp_idx

    if dp_idx >= len(dps):
        st.session_state.sim_completed_branches.add(branch_id)
        st.session_state.sim_active_branch_id = None
        st.session_state.sim_phase = "play"
        st.rerun()
        return

    dp = dps[dp_idx]
    dp_id = dp.get("id", "")
    actions = dp.get("available_actions", [])
    critical_ids = set(dp.get("critical_action_ids", []))
    locked = st.session_state.sim_dp_locked

    page_header("Clinical Scenario Simulator", f"Branch: {branch_id}")
    render_phase_indicator("branch")

    st.info(f"**Branch context:** {branch.get('trigger_context', '')}")

    st.markdown(
        f'<div class="sim-dp-header">'
        f'<div class="dp-label">Branch DP {dp_idx + 1} of {len(dps)} &bull; {_esc(str(dp_id))}</div>'
        f'<div class="dp-context">{_esc(dp.get("context", ""))}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    section_label(f"{len(actions)} Available Actions")

    if dp_id not in st.session_state.sim_branch_selected:
        st.session_state.sim_branch_selected[dp_id] = set()

    current_selections = set()
    for action in actions:
        action_id = action.get("id", "")
        is_critical = (action.get("requirement") or "").lower() == "critical" or action_id in critical_ids
        selected = render_action_card_interactive(
            action=action,
            dp_id=f"br_{dp_id}",
            revealed=locked,
            disabled=locked,
            is_critical=is_critical,
        )
        if selected:
            current_selections.add(action_id)

    if not locked:
        st.session_state.sim_branch_selected[dp_id] = current_selections

    st.markdown("---")

    if not locked:
        if st.button("Submit Decisions", type="primary", use_container_width=True):
            st.session_state.sim_dp_locked = True
            for action in actions:
                if action.get("id", "") in st.session_state.sim_branch_selected.get(dp_id, set()):
                    st.session_state.sim_elapsed_minutes += compute_action_duration(action)
            st.session_state.sim_completed_dps.append(dp_id)
            st.rerun()
    else:
        feedback = dp.get("feedback_on_completion")
        if feedback:
            st.success(f"**Feedback:** {feedback}")

        if st.button("Next", type="primary", use_container_width=True):
            st.session_state.sim_branch_dp_idx += 1
            st.session_state.sim_dp_locked = False
            st.rerun()


# ---------------------------------------------------------------------------
# PHASE: DEBRIEF
# ---------------------------------------------------------------------------

def phase_debrief():
    scenario = st.session_state.sim_scenario_data
    page_header("Clinical Scenario Simulator", "Performance Debrief")
    render_phase_indicator("debrief")

    # Merge main + branch selections
    all_selected = dict(st.session_state.sim_selected_actions)
    all_selected.update(st.session_state.sim_branch_selected)

    score = compute_simulation_score(scenario, all_selected, st.session_state.sim_elapsed_minutes)

    # --- Score cards ---
    section_label("Performance Summary")

    cols = st.columns(4)

    crit_pct = score["critical_pct"]
    crit_class = "success" if crit_pct >= 80 else ("warning" if crit_pct >= 50 else "danger")
    with cols[0]:
        st.markdown(
            f'<div class="sim-score-card {crit_class}">'
            f'<div class="score-value">{crit_pct:.0f}%</div>'
            f'<div class="score-label">Critical Actions</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    with cols[1]:
        st.markdown(
            f'<div class="sim-score-card">'
            f'<div class="score-value">{score["critical_performed"]}/{score["critical_total"]}</div>'
            f'<div class="score-label">Critical Hit / Total</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    with cols[2]:
        st.markdown(
            f'<div class="sim-score-card">'
            f'<div class="score-value">{score["supportive_performed"]}/{score["supportive_total"]}</div>'
            f'<div class="score-label">Supportive Actions</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    elapsed = score["elapsed_minutes"]
    within = score["within_time_window"]
    time_class = "success" if within else ("danger" if within is False else "")
    with cols[3]:
        st.markdown(
            f'<div class="sim-score-card {time_class}">'
            f'<div class="score-value">{elapsed:.0f} min</div>'
            f'<div class="score-label">Elapsed Time</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    tw = scenario.get("clinical_time_window")
    if tw and within is not None:
        remaining = tw.get("remaining_window_minutes", 0)
        if within:
            st.success(f"Completed within the {remaining}-minute treatment window.")
        else:
            st.error(f"Exceeded the {remaining}-minute treatment window by {elapsed - remaining:.0f} minutes.")

    st.markdown("---")

    # --- Per-DP breakdown ---
    section_label("Decision Point Breakdown")
    for dp_score in score["per_dp"]:
        dp_id = dp_score["dp_id"]
        hit = dp_score["critical_hit"]
        total = dp_score["critical_total"]
        icon = "\u2705" if hit == total else ("\u26a0\ufe0f" if hit > 0 else "\u274c")
        st.markdown(f"{icon} **{dp_id}**: {hit}/{total} critical actions")

    st.markdown("---")

    # --- Common errors matched ---
    matched_errors = match_common_errors(scenario, all_selected)
    if matched_errors:
        section_label("Errors Identified")
        for error in matched_errors:
            error_type = error.get("_match_reason", "unknown")
            badge_cls = "badge-commission" if error_type == "commission" else "badge-omission"
            st.markdown(
                f'<span class="{badge_cls}">{_esc(error_type.upper())}</span> '
                f"**{_esc(error.get('description', ''))}**",
                unsafe_allow_html=True,
            )
            st.markdown(f"*Consequence:* {error.get('consequence', 'N/A')}")
            if error.get("_key_learning"):
                st.caption(f"Key Learning: {error['_key_learning']}")
            st.markdown("")
    else:
        st.success("No common errors matched your performance \u2014 well done!")

    st.markdown("---")

    # --- Debriefing points ---
    debriefing = scenario.get("debriefing", [])
    if debriefing:
        section_label("Clinical Debriefing")
        action_index = build_action_index(scenario)
        for debrief in debriefing:
            render_debriefing_point(debrief, action_index)

    # --- Key takeaways ---
    takeaways = scenario.get("key_takeaways", [])
    if takeaways:
        section_label("Key Takeaways")
        for t in takeaways:
            st.markdown(f"- {t}")

    st.markdown("---")

    if st.button("Try Again", type="primary", use_container_width=True):
        scenario_data = st.session_state.sim_scenario_data
        _reset_simulation()
        st.session_state.sim_scenario_data = scenario_data
        st.session_state.sim_phase = "briefing"
        st.rerun()

    if st.button("Choose Another Scenario", use_container_width=True):
        _reset_simulation()
        st.rerun()


# ---------------------------------------------------------------------------
# Main phase router
# ---------------------------------------------------------------------------

phase = st.session_state.sim_phase

if phase == "select":
    phase_select()
elif phase == "briefing":
    phase_briefing()
elif phase == "play":
    phase_play()
elif phase == "branch":
    phase_branch()
elif phase == "debrief":
    phase_debrief()
else:
    _reset_simulation()
    st.rerun()

"""Scenario viewer components for the standalone simulator."""

from html import escape as _esc

import streamlit as st


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def format_minutes_as_hours(minutes: int | float | None) -> str:
    """Format a duration in minutes as a human-readable hours string."""
    if minutes is None or minutes == "?":
        return "?"
    minutes = int(minutes)
    if minutes < 60:
        return f"{minutes} min"
    hours = minutes // 60
    remainder = minutes % 60
    if remainder == 0:
        return f"{hours}h"
    return f"{hours}h {remainder}min"


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

REVIEW_CSS = """
<style>
    .badge-critical { background: #C2410C; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.02em; }
    .badge-supportive { background: #2563EB; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.02em; }
    .badge-optional { background: #6B7280; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.02em; }
    .badge-positive { background: #C2410C; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.75rem; }
    .badge-negative { background: #0F766E; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.75rem; }
    .badge-noncontrib { background: #9CA3AF; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.75rem; }
    .badge-commission { background: #D97706; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; }
    .badge-omission { background: #7C3AED; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; }
    .badge-duration { background: #1B2A4A; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.72rem; }
    .badge-branch-trigger { background: #DB2777; color: white; padding: 3px 10px; border-radius: 99px; font-size: 0.72rem; font-weight: 700; }
    .time-window-alert { background: #FFFBEB; padding: 1rem 1.2rem; border-radius: 10px; border-left: 4px solid #D97706; margin: 0.5rem 0; }
    .key-learning-card { background: #F0FDF4; padding: 1rem 1.2rem; border-radius: 10px; border-left: 4px solid #059669; margin: 0.5rem 0; }
    .vital-signs-card { background: #EFF6FF; padding: 0.8rem; border-radius: 10px; border: 1px solid #BFDBFE; margin: 0.5rem 0; }
    .action-hint-critical { border-left: 3px solid #C2410C; padding-left: 0.6rem; margin-bottom: 0.15rem; }
    .action-hint-supportive { border-left: 3px solid #2563EB; padding-left: 0.6rem; margin-bottom: 0.15rem; }
    .action-hint-optional { border-left: 3px solid #D1D5DB; padding-left: 0.6rem; margin-bottom: 0.15rem; }
    .citation-inline { font-size: 0.78rem; color: #6B7280; font-style: italic; margin-top: 2px; }
</style>
"""

_REQUIREMENT_MAP = {
    "critical": "badge-critical",
    "supportive": "badge-supportive",
    "optional": "badge-optional",
}

_RELEVANCE_MAP = {
    "positive": "badge-positive",
    "negative": "badge-negative",
    "non contributory": "badge-noncontrib",
    "non_contributory": "badge-noncontrib",
}


# ---------------------------------------------------------------------------
# Badge helpers
# ---------------------------------------------------------------------------

def get_requirement_badge(requirement: str) -> str:
    """Return an HTML badge for action requirement level."""
    req = (requirement or "optional").lower()
    cls = _REQUIREMENT_MAP.get(req, "badge-optional")
    label = req.title()
    return f'<span class="{cls}">{label}</span>'


def get_relevance_badge(relevance: str) -> str:
    """Return an HTML badge for finding relevance."""
    rel = (relevance or "non contributory").lower().replace("_", " ")
    cls = _RELEVANCE_MAP.get(rel, "badge-noncontrib")
    label = rel.title()
    return f'<span class="{cls}">{label}</span>'


def get_duration_badge(action: dict) -> str:
    """Return an HTML badge showing action duration with optional range."""
    dur = action.get("duration_minutes")
    if not dur:
        return ""
    if isinstance(dur, list) and len(dur) == 2:
        label = f"{dur[0]}-{dur[1]} min"
    else:
        label = f"{dur} min"
    return f' <span class="badge-duration">{label}</span>'


# ---------------------------------------------------------------------------
# Rendering functions
# ---------------------------------------------------------------------------

def render_vital_signs(vital_signs: dict) -> None:
    """Render vital signs in a clean grid, showing only fields present in the data."""
    if not vital_signs:
        st.caption("No vital signs recorded")
        return

    _VITAL_FIELDS = [
        ("blood_pressure", "Blood Pressure"),
        ("heart_rate", "Heart Rate"),
        ("respiratory_rate", "Respiratory Rate"),
        ("temperature", "Temperature"),
        ("oxygen_saturation", "SpO2"),
        ("blood_glucose", "Blood Glucose"),
        ("gcs", "GCS"),
        ("nihss", "NIHSS"),
    ]

    present = [(label, vital_signs[key]) for key, label in _VITAL_FIELDS if vital_signs.get(key) is not None]

    if not present:
        st.caption("No vital signs recorded")
        return

    cols_per_row = 4
    for row_start in range(0, len(present), cols_per_row):
        row_items = present[row_start:row_start + cols_per_row]
        cols = st.columns(cols_per_row)
        for col, (label, value) in zip(cols, row_items, strict=False):
            with col:
                st.metric(label, value)

    rhythm = vital_signs.get("cardiac_rhythm")
    if rhythm:
        st.markdown(f"**Cardiac Rhythm:** {rhythm}")


def build_action_index(scenario: dict) -> dict:
    """Build a lookup from action ID / decision point ID to description."""
    index = {}
    for stage in scenario.get("stages", []):
        for dp in stage.get("decision_points", []):
            dp_id = dp.get("id", "")
            context = dp.get("context", "")
            index[dp_id] = context[:80] + "..." if len(context) > 80 else context
            for action in dp.get("available_actions", []):
                index[action.get("id", "")] = action.get("description", "")
    for branch in scenario.get("branches", []):
        for dp in branch.get("decision_points", []):
            dp_id = dp.get("id", "")
            context = dp.get("context", "")
            index[dp_id] = context[:80] + "..." if len(context) > 80 else context
            for action in dp.get("available_actions", []):
                index[action.get("id", "")] = action.get("description", "")
    return index


def render_debriefing_point(debrief: dict, action_index: dict | None = None) -> None:
    """Render a single debriefing point with common errors."""
    if action_index is None:
        action_index = {}

    st.markdown(
        f'<div class="key-learning-card"><strong>{_esc(debrief.get("key_learning", ""))}</strong></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**Clinical Reasoning:** {debrief.get('clinical_reasoning', '')}")

    if debrief.get("related_objectives"):
        st.markdown(f"**Related Objectives:** {', '.join(debrief['related_objectives'])}")

    if debrief.get("related_actions"):
        parts = []
        for ra in debrief["related_actions"]:
            parts.append(f"{ra['decision_point']}: {', '.join(ra['actions'])}")
        st.markdown(f"**Related Actions:** {' | '.join(parts)}")

    errors = debrief.get("common_errors", [])
    if errors:
        st.markdown("**Common Errors:**")
        for error in errors:
            error_type = (error.get("error_type") or "unknown").lower()
            badge_cls = "badge-commission" if error_type == "commission" else "badge-omission"
            badge = f'<span class="{badge_cls}">{error_type.upper()}</span>'

            st.markdown(f"{badge} **{_esc(error.get('description', ''))}**", unsafe_allow_html=True)
            st.markdown(f"*Consequence:* {error.get('consequence', 'N/A')}")

            ra = error.get("related_action")
            if ra:
                dp_id = ra.get("decision_point", "?")
                action_id = ra.get("action", "?")
                action_desc = action_index.get(action_id, "")
                ref_parts = [f"**{dp_id}**"]
                if action_id:
                    ref_parts.append(f"**{action_id}**")
                if action_desc:
                    ref_parts.append(f"*{action_desc}*")
                st.caption(f"Related to: {' / '.join(ref_parts)}")
            st.markdown("---")


def render_patient_profile(patient: dict) -> None:
    """Render patient demographics and history."""
    st.markdown(f"**Age:** {patient.get('age', '?')} years")
    st.markdown(f"**Gender:** {patient.get('gender', '?')}")
    st.markdown(f"**Presenting Complaint:** {patient.get('presenting_complaint', 'N/A')}")
    social = patient.get("social_context") or patient.get("social_history")
    if social:
        st.markdown(f"**Social Context:** {social}")

    history = patient.get("medical_history", [])
    st.markdown("**Medical History:**")
    if history:
        for item in history:
            st.markdown(f"- {item}")
    else:
        st.markdown("- None reported")

    meds = patient.get("medications", [])
    st.markdown("**Medications:**")
    if meds:
        for item in meds:
            st.markdown(f"- {item}")
    else:
        st.markdown("- None reported")

    allergies = patient.get("allergies", [])
    st.markdown("**Allergies:**")
    if allergies:
        for item in allergies:
            st.markdown(f"- {item}")
    else:
        st.markdown("- No known allergies")


# ---------------------------------------------------------------------------
# Interactive Simulation helpers
# ---------------------------------------------------------------------------

def compute_action_duration(action: dict) -> float:
    """Return the midpoint duration in minutes for an action."""
    dur = action.get("duration_minutes")
    if isinstance(dur, list) and len(dur) == 2:
        return (dur[0] + dur[1]) / 2
    elif isinstance(dur, (int, float)):
        return float(dur)
    return 0.0


def _render_citation_inline(citation) -> str:
    """Return HTML string for an inline citation display."""
    if not citation:
        return ""
    if isinstance(citation, str):
        return f'<div class="citation-inline">Citation: {_esc(citation)}</div>'
    if isinstance(citation, list):
        labels = []
        for entry in citation:
            if isinstance(entry, dict):
                src = entry.get("source", "")
                sec = entry.get("section", "")
                label = src
                if sec:
                    label += f", Section {sec}"
                labels.append(label)
            else:
                labels.append(str(entry))
        return f'<div class="citation-inline">Citation: {_esc("; ".join(labels))}</div>'
    return ""


def render_action_card_interactive(
    action: dict,
    dp_id: str,
    revealed: bool = False,
    disabled: bool = False,
    is_critical: bool = False,
) -> bool:
    """Render an action card with a checkbox; findings hidden until revealed."""
    action_id = action.get("id", "?")
    key = f"sim_cb_{dp_id}_{action_id}"

    # Determine requirement-based hint class (subtle left border before reveal)
    req = (action.get("requirement") or "optional").lower()
    hint_class = f"action-hint-{req}" if req in ("critical", "supportive", "optional") else "action-hint-optional"

    # Duration badge shown even before submission
    dur_badge = get_duration_badge(action)
    dur_html = f'<span style="float:right;">{dur_badge}</span>' if dur_badge else ""

    # Wrap in a hint div for the subtle border
    if dur_html and not revealed:
        st.markdown(f'<div class="{hint_class}">{dur_html}</div>', unsafe_allow_html=True)
    elif not revealed:
        st.markdown(f'<div class="{hint_class}" style="min-height:2px;"></div>', unsafe_allow_html=True)

    selected = st.checkbox(
        action.get("description", "Unknown action"),
        key=key,
        disabled=disabled,
    )

    if revealed:
        req_badge = get_requirement_badge(action.get("requirement", "optional"))
        rel_badge = get_relevance_badge(action.get("finding_relevance", "non contributory"))
        dur_badge_full = get_duration_badge(action)

        if is_critical:
            css_class = "sim-action-hit-critical" if selected else "sim-action-missed-critical"
        else:
            css_class = ""

        finding = _esc(action.get("finding", "N/A"))
        rationale = _esc(action.get("rationale", ""))
        parts = [f"{req_badge} {rel_badge}{dur_badge_full}", f"<b>Finding:</b> {finding}"]
        if rationale:
            parts.append(f'<span style="font-size:0.85rem;color:#6B7280;">Rationale: {rationale}</span>')
        # Citation
        citation_html = _render_citation_inline(action.get("citation"))
        if citation_html:
            parts.append(citation_html)
        inner_html = "<br>".join(parts)

        if css_class:
            st.markdown(f'<div class="{css_class}">{inner_html}</div>', unsafe_allow_html=True)
        else:
            st.markdown(inner_html, unsafe_allow_html=True)

    return selected


def render_time_tracker(elapsed_minutes: float, time_window: dict | None) -> None:
    """Render elapsed time with clinical time window context."""
    st.metric("Elapsed Time", f"{elapsed_minutes:.0f} min")

    if time_window:
        remaining = time_window.get("remaining_window_minutes", 0)
        if remaining > 0:
            used_fraction = min(elapsed_minutes / remaining, 1.0)
            st.progress(used_fraction)
            left = remaining - elapsed_minutes
            if left > 15:
                st.caption(f"{left:.0f} min remaining")
            elif left > 0:
                st.warning(f"Only {left:.0f} min left!")
            else:
                st.error("Time window exceeded!")


def compute_simulation_score(
    scenario: dict,
    selected_actions_by_dp: dict[str, set[str]],
    elapsed_minutes: float,
) -> dict:
    """Compute simulation performance metrics."""
    critical_performed = 0
    critical_total = 0
    supportive_performed = 0
    supportive_total = 0
    per_dp: list[dict] = []

    for stage in scenario.get("stages", []):
        for dp in stage.get("decision_points", []):
            dp_id = dp.get("id", "")
            dp_selected = selected_actions_by_dp.get(dp_id, set())
            critical_ids = set(dp.get("critical_action_ids", []))
            dp_crit_hit = 0
            dp_crit_total = 0

            for action in dp.get("available_actions", []):
                aid = action.get("id", "")
                req = (action.get("requirement") or "optional").lower()
                if req == "critical" or aid in critical_ids:
                    critical_total += 1
                    dp_crit_total += 1
                    if aid in dp_selected:
                        critical_performed += 1
                        dp_crit_hit += 1
                elif req == "supportive":
                    supportive_total += 1
                    if aid in dp_selected:
                        supportive_performed += 1

            per_dp.append({
                "dp_id": dp_id,
                "critical_hit": dp_crit_hit,
                "critical_total": dp_crit_total,
            })

    tw = scenario.get("clinical_time_window")
    within_window = None
    if tw:
        remaining = tw.get("remaining_window_minutes", 0)
        within_window = elapsed_minutes <= remaining if remaining > 0 else None

    return {
        "critical_performed": critical_performed,
        "critical_total": critical_total,
        "critical_pct": (critical_performed / critical_total * 100) if critical_total else 100.0,
        "supportive_performed": supportive_performed,
        "supportive_total": supportive_total,
        "elapsed_minutes": elapsed_minutes,
        "within_time_window": within_window,
        "per_dp": per_dp,
    }


def match_common_errors(
    scenario: dict,
    selected_actions_by_dp: dict[str, set[str]],
) -> list[dict]:
    """Identify debriefing common errors that match the user's action pattern."""
    matched: list[dict] = []

    critical_actions: dict[str, str] = {}
    for stage in scenario.get("stages", []):
        for dp in stage.get("decision_points", []):
            dp_id = dp.get("id", "")
            critical_ids = set(dp.get("critical_action_ids", []))
            for action in dp.get("available_actions", []):
                aid = action.get("id", "")
                req = (action.get("requirement") or "optional").lower()
                if req == "critical" or aid in critical_ids:
                    critical_actions[aid] = dp_id

    for debrief in scenario.get("debriefing", []):
        for error in debrief.get("common_errors", []):
            error_type = (error.get("error_type") or "").lower()
            related = error.get("related_action") or {}
            ref_dp = related.get("decision_point", "")
            ref_action = related.get("action", "")
            dp_selected = selected_actions_by_dp.get(ref_dp, set())

            if error_type == "omission" and ref_action and ref_action not in dp_selected:
                if ref_action in critical_actions:
                    matched.append({**error, "_match_reason": "omission", "_key_learning": debrief.get("key_learning", "")})
            elif error_type == "commission" and ref_action and ref_action in dp_selected:
                matched.append({**error, "_match_reason": "commission", "_key_learning": debrief.get("key_learning", "")})

    return matched

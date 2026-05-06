"""Standalone interactive simulation walkthrough of clinical scenarios."""

import json
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Clinical Scenario Simulator",
    page_icon="\U0001f3ae",
    layout="wide",
)

try:
    from standalone_simulator.simulation import (
        REVIEW_CSS,
        _t,
        apply_theme,
        init_session_state,
        page_header,
        render_language_toggle,
        render_phase_indicator,
        reset_simulation,
        run_phase_router,
    )
except ImportError:
    from simulation import (
        REVIEW_CSS,
        _t,
        apply_theme,
        init_session_state,
        page_header,
        render_language_toggle,
        render_phase_indicator,
        reset_simulation,
        run_phase_router,
    )

apply_theme()
st.markdown(REVIEW_CSS, unsafe_allow_html=True)
init_session_state()


SCENARIOS_DIR = Path(__file__).parent / "scenarios"

_ARCHITECTURE_LABELS = {
    "context_engineering": "Context Engineering",
    "multi_agent": "Multi-Agent",
}


def _load_bundled_scenarios() -> list[dict]:
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
            meta = scenario.get("metadata", {})
            arch = meta.get("architecture", "")
            label = _ARCHITECTURE_LABELS.get(arch, "Bundled")
            entries.append({
                "data": scenario,
                "source": label,
                "title": scenario.get("title", path.stem),
                "scenario_id": path.stem,
            })
    return entries


def _format_label(entry: dict) -> str:
    title = entry.get("title", "Untitled")
    source = entry.get("source", "Unknown")
    return f"[{source}] {title}"


def phase_select():
    render_language_toggle()
    page_header(_t("page_title"), _t("page_subtitle"))
    render_phase_indicator("select")

    uploaded_files = st.file_uploader(
        _t("upload_label"),
        type=["json"],
        accept_multiple_files=True,
        help=_t("upload_help"),
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

    entries = _load_bundled_scenarios() + st.session_state.get("uploaded_scenarios", [])

    if not entries:
        st.warning(_t("no_scenarios"))
        return

    st.markdown("---")

    labels = [_format_label(e) for e in entries]
    selected_idx = st.selectbox(_t("choose_scenario"), range(len(labels)), format_func=lambda i: labels[i])

    if selected_idx is not None:
        scenario = entries[selected_idx]["data"]

        with st.expander(_t("preview"), expanded=False):
            st.markdown(f"**{scenario.get('title', 'Untitled')}**")
            st.markdown(f"{scenario.get('domain', '')} \u203a {scenario.get('subdomain', '')}")
            st.markdown(
                f"Difficulty: {(scenario.get('difficulty') or 'N/A').title()} | "
                f"Duration: ~{scenario.get('estimated_duration_minutes', '?')} min"
            )
            stages = scenario.get("stages", [])
            total_dps = sum(len(s.get("decision_points", [])) for s in stages)
            total_actions = sum(
                len(dp.get("available_actions", []))
                for s in stages for dp in s.get("decision_points", [])
            )
            st.markdown(f"{len(stages)} stage(s), {total_dps} decision points, {total_actions} actions")

        if st.button(_t("start_simulation"), type="primary", use_container_width=True):
            reset_simulation()
            st.session_state.sim_scenario_data = scenario
            st.session_state.sim_phase = "briefing"
            st.rerun()

run_phase_router(phase_select)

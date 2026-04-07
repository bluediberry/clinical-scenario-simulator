"""Shared simulation engine used by both the standalone simulator and the main app."""

from html import escape as _esc

import streamlit as st

# Imports — work both as a package import and when running standalone
try:
    from standalone_simulator.scenario_viewer import (
        REVIEW_CSS,
        build_action_index,
        compute_action_duration,
        compute_simulation_score,
        compute_vital_signs_diff,
        format_minutes_as_hours,
        match_common_errors,
        render_action_card_interactive,
        render_action_card_static,
        render_debriefing_point,
        render_patient_profile,
        render_time_tracker,
        render_vital_signs,
    )
    from standalone_simulator.theme import apply_theme, config_banner, page_header, section_label
except ImportError:
    from scenario_viewer import (  # type: ignore[no-redef]  # noqa: F401, I001
        REVIEW_CSS,
        build_action_index,
        compute_action_duration,
        compute_simulation_score,
        compute_vital_signs_diff,
        format_minutes_as_hours,
        match_common_errors,
        render_action_card_interactive,
        render_action_card_static,
        render_debriefing_point,
        render_patient_profile,
        render_time_tracker,
        render_vital_signs,
    )
    from theme import apply_theme, config_banner, page_header, section_label  # type: ignore[no-redef]  # noqa: F401


_STRINGS = {
    "en": {
        "page_title": "Clinical Scenario Simulator",
        "page_subtitle": "Step-by-step interactive walkthrough of clinical scenarios",
        "upload_label": "Upload scenario JSON files",
        "upload_help": "Upload one or more scenario JSON files to simulate them.",
        "choose_scenario": "Choose a scenario",
        "start_simulation": "Start Simulation",
        "begin_simulation": "Begin Simulation",
        "submit_decisions": "Submit Decisions",
        "next_dp": "Next Decision Point",
        "next": "Next",
        "try_again": "Try Again",
        "choose_another": "Choose Another Scenario",
        "patient_profile": "Patient Profile",
        "initial_presentation": "Initial Presentation",
        "your_role": "Your Role",
        "clinical_time_window": "Clinical Time Window",
        "learning_objectives": "Learning Objectives",
        "available_actions": "Available Actions",
        "performance_summary": "Performance Summary",
        "dp_breakdown": "Decision Point Breakdown",
        "errors_identified": "Errors Identified",
        "clinical_debriefing": "Clinical Debriefing",
        "key_takeaways": "Key Takeaways",
        "critical_actions": "Critical Actions",
        "supportive_actions": "Supportive Actions",
        "elapsed_time": "Elapsed Time",
        "preview": "Preview",
        "back": "Back",
        "no_scenarios": "No scenarios available. Upload a scenario JSON file or add files to the scenarios/ folder.",
        "no_errors": "No common errors matched your performance \u2014 well done!",
        "feedback": "Feedback",
        "critical_performed": "Critical Actions Performed",
        "critical_hit_total": "Critical Hit / Total",
        "symptom_onset": "Symptom onset",
        "treatment_window": "Treatment window",
        "remaining": "Remaining",
        "language_label": "Language",
        "simulation": "Simulation",
        "stage": "Stage",
        "decision_point": "Decision Point",
        "vital_signs": "Vital Signs",
        "always_available_info": "Always Available Info",
        "additional_info": "Additional Information",
        "stage_progress": "Stage {current} of {total}",
        "dp_progress": "Decision Point {current} of {total}",
        "branch_context": "Branch context",
        "branch_dp": "Branch DP {current} of {total}",
        "explore_branch": "Explore Branch",
        "branch_trigger_msg": "Your action **{action}** has triggered a branch: *{context}*",
        "branch_terminal": "This branch leads to a terminal outcome. The scenario will now end.",
        "branch_terminal_consequence": "Consequence",
        "go_to_debrief": "Go to Debrief",
        "performance_debrief": "Performance Debrief",
        "within_window": "Completed within the {remaining}-minute treatment window.",
        "exceeded_window": "Exceeded the {remaining}-minute treatment window by {exceeded:.0f} minutes.",
        "critical_actions_count": "{hit}/{total} critical actions",
        "lo_assessed": "Learning Objectives Assessed",
        "lo_assessed_at": "Assessed at",
        "debrief_citation": "Reference",
        "phase_select": "Select",
        "phase_briefing": "Briefing",
        "phase_simulation": "Simulation",
        "phase_branch": "Branch",
        "phase_debrief": "Debrief",
        "phase_view": "Full View",
        "view_full_scenario": "View Full Scenario",
        "print_scenario": "Print / Save as PDF",
        "prerequisites": "Prerequisites",
        "stages": "Stages",
        "branches": "Branches",
        "setting": "Setting",
        "progression_criteria": "Progression Criteria",
        "trigger": "Trigger",
        "consequence": "Consequence",
        "merge_point": "Merge Point",
        "terminal_branch": "Terminal Branch",
        "branch_type": "Branch Type",
        "vital_signs_changed": "Vital Signs (changes from previous stage)",
        "no_vital_changes": "Vital signs unchanged from previous stage.",
    },
    "pt": {
        "page_title": "Simulador de Cen\u00e1rios Cl\u00ednicos",
        "page_subtitle": "Simula\u00e7\u00e3o interativa passo a passo de cen\u00e1rios cl\u00ednicos",
        "upload_label": "Carregar ficheiros JSON de cen\u00e1rios",
        "upload_help": "Carregue um ou mais ficheiros JSON de cen\u00e1rios para simul\u00e1-los.",
        "choose_scenario": "Escolher um cen\u00e1rio",
        "start_simulation": "Iniciar Simula\u00e7\u00e3o",
        "begin_simulation": "Iniciar Simula\u00e7\u00e3o",
        "submit_decisions": "Submeter Decis\u00f5es",
        "next_dp": "Pr\u00f3ximo Ponto de Decis\u00e3o",
        "next": "Pr\u00f3ximo",
        "try_again": "Tentar Novamente",
        "choose_another": "Escolher Outro Cen\u00e1rio",
        "patient_profile": "Perfil do Paciente",
        "initial_presentation": "Apresenta\u00e7\u00e3o Inicial",
        "your_role": "O Seu Papel",
        "clinical_time_window": "Janela Temporal Cl\u00ednica",
        "learning_objectives": "Objetivos de Aprendizagem",
        "available_actions": "A\u00e7\u00f5es Dispon\u00edveis",
        "performance_summary": "Resumo de Desempenho",
        "dp_breakdown": "An\u00e1lise por Ponto de Decis\u00e3o",
        "errors_identified": "Erros Identificados",
        "clinical_debriefing": "Debriefing Cl\u00ednico",
        "key_takeaways": "Pontos-Chave",
        "critical_actions": "A\u00e7\u00f5es Cr\u00edticas",
        "supportive_actions": "A\u00e7\u00f5es de Suporte",
        "elapsed_time": "Tempo Decorrido",
        "preview": "Pr\u00e9-visualiza\u00e7\u00e3o",
        "back": "Voltar",
        "no_scenarios": "Nenhum cen\u00e1rio dispon\u00edvel. Carregue um ficheiro JSON ou adicione ficheiros \u00e0 pasta scenarios/.",
        "no_errors": "Nenhum erro comum identificado \u2014 bom trabalho!",
        "feedback": "Feedback",
        "critical_performed": "A\u00e7\u00f5es Cr\u00edticas Realizadas",
        "critical_hit_total": "Cr\u00edticas Acertadas / Total",
        "symptom_onset": "In\u00edcio dos sintomas",
        "treatment_window": "Janela de tratamento",
        "remaining": "Restante",
        "language_label": "Idioma",
        "simulation": "Simula\u00e7\u00e3o",
        "stage": "Fase",
        "decision_point": "Ponto de Decis\u00e3o",
        "vital_signs": "Sinais Vitais",
        "always_available_info": "Informa\u00e7\u00e3o Sempre Dispon\u00edvel",
        "additional_info": "Informa\u00e7\u00e3o Adicional",
        "stage_progress": "Fase {current} de {total}",
        "dp_progress": "Ponto de Decis\u00e3o {current} de {total}",
        "branch_context": "Contexto do ramo",
        "branch_dp": "PD do Ramo {current} de {total}",
        "explore_branch": "Explorar Ramo",
        "branch_trigger_msg": "A sua a\u00e7\u00e3o **{action}** desencadeou um ramo: *{context}*",
        "branch_terminal": "Este ramo conduz a um desfecho terminal. O cen\u00e1rio ir\u00e1 terminar agora.",
        "branch_terminal_consequence": "Consequ\u00eancia",
        "go_to_debrief": "Ir para Debriefing",
        "performance_debrief": "Debriefing de Desempenho",
        "within_window": "Conclu\u00eddo dentro da janela de tratamento de {remaining} minutos.",
        "exceeded_window": "Excedeu a janela de tratamento de {remaining} minutos em {exceeded:.0f} minutos.",
        "critical_actions_count": "{hit}/{total} a\u00e7\u00f5es cr\u00edticas",
        "lo_assessed": "Objetivos de Aprendizagem Avaliados",
        "lo_assessed_at": "Avaliado em",
        "debrief_citation": "Refer\u00eancia",
        "phase_select": "Selecionar",
        "phase_briefing": "Briefing",
        "phase_simulation": "Simula\u00e7\u00e3o",
        "phase_branch": "Ramo",
        "phase_debrief": "Debriefing",
        "phase_view": "Visualiza\u00e7\u00e3o",
        "view_full_scenario": "Ver Cen\u00e1rio Completo",
        "print_scenario": "Imprimir / Guardar como PDF",
        "prerequisites": "Pr\u00e9-requisitos",
        "stages": "Fases",
        "branches": "Ramos",
        "setting": "Contexto",
        "progression_criteria": "Crit\u00e9rios de Progress\u00e3o",
        "trigger": "Gatilho",
        "consequence": "Consequ\u00eancia",
        "merge_point": "Ponto de Converg\u00eancia",
        "terminal_branch": "Ramo Terminal",
        "branch_type": "Tipo de Ramo",
        "vital_signs_changed": "Sinais Vitais (altera\u00e7\u00f5es em rela\u00e7\u00e3o \u00e0 fase anterior)",
        "no_vital_changes": "Sinais vitais sem altera\u00e7\u00f5es em rela\u00e7\u00e3o \u00e0 fase anterior.",
    },
}


def _t(key: str, **kwargs) -> str:
    """Get translated string for the current language."""
    lang = st.session_state.get("lang", "pt")
    text = _STRINGS.get(lang, _STRINGS["en"]).get(key, _STRINGS["en"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def render_language_toggle():
    """Render language toggle in the sidebar."""
    with st.sidebar:
        lang_options = {"English": "en", "Portugu\u00eas": "pt"}
        current = st.session_state.get("lang", "pt")
        current_label = "Portugu\u00eas" if current == "pt" else "English"  # noqa: F841
        selected = st.radio(
            _t("language_label"),
            list(lang_options.keys()),
            index=list(lang_options.values()).index(current),
            horizontal=True,
            key="lang_radio",
        )
        new_lang = lang_options[selected]
        if new_lang != current:
            st.session_state.lang = new_lang
            st.rerun()


# Session state defaults
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
    "lang": "pt",
}


def init_session_state():
    """Initialise session state defaults (call once per page)."""
    for key, default in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def reset_simulation():
    """Reset all simulation state, preserving uploads and language."""
    uploaded = st.session_state.get("uploaded_scenarios", [])
    lang = st.session_state.get("lang", "pt")
    for key, default in _DEFAULTS.items():
        st.session_state[key] = default
    st.session_state.uploaded_scenarios = uploaded
    st.session_state.lang = lang


# Phase indicator
_PHASES = ["select", "briefing", "play", "debrief"]


def _get_phase_labels() -> dict:
    return {
        "select": _t("phase_select"),
        "briefing": _t("phase_briefing"),
        "play": _t("phase_simulation"),
        "branch": _t("phase_branch"),
        "debrief": _t("phase_debrief"),
    }


def render_phase_indicator(current: str):
    labels = _get_phase_labels()
    parts = []
    for i, phase in enumerate(_PHASES):
        if i > 0:
            parts.append('<span class="sep">\u203a</span>')
        idx_current = _PHASES.index(current) if current in _PHASES else 2
        if _PHASES.index(phase) < idx_current:
            parts.append(f'<span class="phase done">{labels[phase]}</span>')
        elif phase == current or (current == "branch" and phase == "play"):
            parts.append(f'<span class="phase active">{labels.get(current, current)}</span>')
        else:
            parts.append(f'<span class="phase">{labels[phase]}</span>')
    st.markdown(f'<div class="sim-phase-indicator">{"".join(parts)}</div>', unsafe_allow_html=True)


# Metadata banner helper
def render_scenario_banner(scenario: dict):
    """Render a metadata banner for the scenario."""
    items = []
    domain = scenario.get("domain", "")
    subdomain = scenario.get("subdomain", "")
    if domain:
        label = f"{domain} \u203a {subdomain}" if subdomain else domain
        items.append(("Domain", label))
    difficulty = scenario.get("difficulty")
    if difficulty:
        items.append(("Difficulty", difficulty.title()))
    target = scenario.get("target_learner")
    if target:
        items.append(("Target", target))
    duration = scenario.get("estimated_duration_minutes")
    if duration:
        items.append(("Duration", f"~{duration} min"))
    if items:
        config_banner(items)


# Helper: get current DP list from stage or branch
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


# PHASE: BRIEFING
def phase_briefing():
    render_language_toggle()
    scenario = st.session_state.sim_scenario_data
    page_header(_t("page_title"), scenario.get("title", ""))
    render_phase_indicator("briefing")

    # Metadata banner
    render_scenario_banner(scenario)

    # Patient profile
    patient = scenario.get("patient")
    if patient:
        section_label(_t("patient_profile"))
        render_patient_profile(patient)
        st.markdown("")

    # Initial presentation
    presentation = scenario.get("initial_presentation")
    if presentation:
        section_label(_t("initial_presentation"))
        st.info(presentation)

    # Interaction prompt
    prompt = scenario.get("interaction_prompt")
    if prompt:
        section_label(_t("your_role"))
        st.markdown(prompt)

    # Time window
    tw = scenario.get("clinical_time_window")
    if tw:
        st.markdown("")
        section_label(_t("clinical_time_window"))
        onset = format_minutes_as_hours(tw.get("symptom_onset_minutes_ago"))
        window = format_minutes_as_hours(tw.get("max_treatment_window_minutes"))
        remaining = format_minutes_as_hours(tw.get("remaining_window_minutes"))
        st.markdown(
            f'<div class="time-window-alert">'
            f"<strong>{_t('symptom_onset')}:</strong> {onset} ago &bull; "
            f"<strong>{_t('treatment_window')}:</strong> {window} &bull; "
            f"<strong>{_t('remaining')}:</strong> {remaining}"
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
        section_label(_t("learning_objectives"))
        for lo in los:
            if isinstance(lo, dict):
                st.markdown(f"- **{lo.get('id', '?')}:** {lo.get('description', '')}")

    st.markdown("---")

    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(_t("begin_simulation"), type="primary", use_container_width=True):
            st.session_state.sim_phase = "play"
            st.session_state.sim_stage_idx = 0
            st.session_state.sim_dp_idx = 0
            st.session_state.sim_dp_locked = False
            st.rerun()
    with col2:
        if st.button(_t("back"), use_container_width=True):
            reset_simulation()
            st.rerun()


# PHASE: PLAY (core simulation loop)
def phase_play():
    render_language_toggle()
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
    page_header(_t("page_title"), scenario.get("title", ""))
    render_phase_indicator("play")
    render_scenario_banner(scenario)

    # --- Sidebar: vital signs + time tracker + stage info + always-available info ---
    total_stages = len(scenario.get("stages", []))
    with st.sidebar:
        st.markdown(f"### {_t('simulation')}")
        st.caption(_t("stage_progress", current=st.session_state.sim_stage_idx + 1, total=total_stages))
        st.caption(f"**{stage.get('name', '?')}**")
        st.caption(_t("dp_progress", current=dp_idx + 1, total=len(dps)))
        st.markdown("---")

        vs = stage.get("vital_signs")
        if vs:
            st.markdown(f"#### {_t('vital_signs')}")
            render_vital_signs(vs)
            st.markdown("---")

        render_time_tracker(st.session_state.sim_elapsed_minutes, scenario.get("clinical_time_window"))

        # Always-available information (global)
        always = scenario.get("always_available_information")
        if always:
            with st.expander(_t("always_available_info")):
                for k, v in always.items():
                    st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

        # Stage-level optional info (all_optional)
        all_optional = stage.get("all_optional", [])
        if all_optional:
            with st.expander(_t("additional_info")):
                for item in all_optional:
                    if isinstance(item, dict):
                        label = item.get("description") or item.get("category") or item.get("id", "?")
                        content = item.get("finding") or item.get("content", "")
                        st.markdown(f"**{label}:** {content}")
                    else:
                        st.markdown(f"- {item}")

        # Progression criteria
        prog = stage.get("progression_criteria")
        if prog:
            st.caption(f"*{prog}*")

    # --- DP Context ---
    st.markdown(
        f'<div class="sim-dp-header">'
        f'<div class="dp-label">{_t("decision_point")} {dp_idx + 1}/{len(dps)} &bull; {_esc(str(dp_id))}</div>'
        f'<div class="dp-context">{_esc(dp.get("context", ""))}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    # --- Actions ---
    section_label(f"{len(actions)} {_t('available_actions')}")

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
        if st.button(_t("submit_decisions"), type="primary", use_container_width=True):
            st.session_state.sim_dp_locked = True
            for action in actions:
                if action.get("id", "") in st.session_state.sim_selected_actions.get(dp_id, set()):
                    st.session_state.sim_elapsed_minutes += compute_action_duration(action)
            st.session_state.sim_completed_dps.append(dp_id)
            st.rerun()
    else:
        feedback = dp.get("feedback_on_completion")
        if feedback:
            st.success(f"**{_t('feedback')}:** {feedback}")

        selected_set = st.session_state.sim_selected_actions.get(dp_id, set()) | current_selections
        critical_hit = sum(
            1 for a in actions
            if (a.get("id") in critical_ids or (a.get("requirement") or "").lower() == "critical")
            and a.get("id") in selected_set
        )
        critical_total = sum(
            1 for a in actions
            if a.get("id") in critical_ids or (a.get("requirement") or "").lower() == "critical"
        )

        if critical_total > 0:
            pct = critical_hit / critical_total * 100
            color_class = "success" if pct >= 80 else ("warning" if pct >= 50 else "danger")
            st.markdown(
                f'<div class="sim-score-card {color_class}" style="margin:0.5rem 0;">'
                f'<div class="score-value">{critical_hit}/{critical_total}</div>'
                f'<div class="score-label">{_t("critical_performed")}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        _check_branch_triggers(scenario, dp, selected_set)

        if st.button(_t("next_dp"), type="primary", use_container_width=True):
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
                    _t("branch_trigger_msg",
                       action=action.get("description", ""),
                       context=branch.get("trigger_context", ""))
                )
                if st.button(f"{_t('explore_branch')} {branch_id}", key=f"branch_{branch_id}"):
                    st.session_state.sim_active_branch_id = branch_id
                    st.session_state.sim_branch_dp_idx = 0
                    st.session_state.sim_dp_locked = False
                    st.session_state.sim_phase = "branch"
                    st.rerun()
                break


# PHASE: BRANCH
def phase_branch():
    render_language_toggle()
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
        # Terminal branch (no merge_point) → end scenario; otherwise return to main path
        if branch.get("merge_point") is None:
            st.session_state.sim_phase = "debrief"
        else:
            st.session_state.sim_phase = "play"
        st.rerun()
        return

    dp = dps[dp_idx]
    dp_id = dp.get("id", "")
    actions = dp.get("available_actions", [])
    critical_ids = set(dp.get("critical_action_ids", []))
    locked = st.session_state.sim_dp_locked

    page_header(_t("page_title"), f"{_t('phase_branch')}: {branch_id}")
    render_phase_indicator("branch")

    st.info(f"**{_t('branch_context')}:** {branch.get('trigger_context', '')}")

    st.markdown(
        f'<div class="sim-dp-header">'
        f'<div class="dp-label">{_t("branch_dp", current=dp_idx + 1, total=len(dps))} &bull; {_esc(str(dp_id))}</div>'
        f'<div class="dp-context">{_esc(dp.get("context", ""))}</div>'
        f"</div>",
        unsafe_allow_html=True,
    )

    section_label(f"{len(actions)} {_t('available_actions')}")

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
        if st.button(_t("submit_decisions"), type="primary", use_container_width=True):
            st.session_state.sim_dp_locked = True
            for action in actions:
                if action.get("id", "") in st.session_state.sim_branch_selected.get(dp_id, set()):
                    st.session_state.sim_elapsed_minutes += compute_action_duration(action)
            st.session_state.sim_completed_dps.append(dp_id)
            st.rerun()
    else:
        feedback = dp.get("feedback_on_completion")
        if feedback:
            st.success(f"**{_t('feedback')}:** {feedback}")

        is_terminal = branch.get("merge_point") is None
        is_last_branch_dp = dp_idx + 1 >= len(dps)

        if is_terminal and is_last_branch_dp:
            consequence = branch.get("consequence_context", "")
            if consequence:
                st.error(f"**{_t('branch_terminal_consequence')}:** {consequence}")
            st.warning(_t("branch_terminal"))
            btn_label = _t("go_to_debrief")
        else:
            btn_label = _t("next")

        if st.button(btn_label, type="primary", use_container_width=True):
            st.session_state.sim_branch_dp_idx += 1
            st.session_state.sim_dp_locked = False
            st.rerun()


# PHASE: DEBRIEF
def phase_debrief():
    render_language_toggle()
    scenario = st.session_state.sim_scenario_data
    page_header(_t("page_title"), _t("performance_debrief"))
    render_phase_indicator("debrief")

    # Merge main + branch selections
    all_selected = dict(st.session_state.sim_selected_actions)
    all_selected.update(st.session_state.sim_branch_selected)

    score = compute_simulation_score(scenario, all_selected, st.session_state.sim_elapsed_minutes)

    # --- Score cards ---
    section_label(_t("performance_summary"))

    cols = st.columns(4)

    crit_pct = score["critical_pct"]
    crit_class = "success" if crit_pct >= 80 else ("warning" if crit_pct >= 50 else "danger")
    with cols[0]:
        st.markdown(
            f'<div class="sim-score-card {crit_class}">'
            f'<div class="score-value">{crit_pct:.0f}%</div>'
            f'<div class="score-label">{_t("critical_actions")}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    with cols[1]:
        st.markdown(
            f'<div class="sim-score-card">'
            f'<div class="score-value">{score["critical_performed"]}/{score["critical_total"]}</div>'
            f'<div class="score-label">{_t("critical_hit_total")}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    with cols[2]:
        st.markdown(
            f'<div class="sim-score-card">'
            f'<div class="score-value">{score["supportive_performed"]}/{score["supportive_total"]}</div>'
            f'<div class="score-label">{_t("supportive_actions")}</div>'
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
            f'<div class="score-label">{_t("elapsed_time")}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )

    tw = scenario.get("clinical_time_window")
    if tw and within is not None:
        remaining = tw.get("remaining_window_minutes", 0)
        if within:
            st.success(_t("within_window", remaining=remaining))
        else:
            st.error(_t("exceeded_window", remaining=remaining, exceeded=elapsed - remaining))

    st.markdown("---")

    # --- Per-DP breakdown (enhanced with expandable details) ---
    section_label(_t("dp_breakdown"))
    for stage in scenario.get("stages", []):
        for dp in stage.get("decision_points", []):
            dp_id = dp.get("id", "")
            dp_selected = all_selected.get(dp_id, set())
            critical_ids = set(dp.get("critical_action_ids", []))
            actions = dp.get("available_actions", [])

            crit_hit = sum(
                1 for a in actions
                if ((a.get("requirement") or "").lower() == "critical" or a.get("id") in critical_ids)
                and a.get("id") in dp_selected
            )
            crit_total = sum(
                1 for a in actions
                if (a.get("requirement") or "").lower() == "critical" or a.get("id") in critical_ids
            )

            icon = "\u2705" if crit_hit == crit_total else ("\u26a0\ufe0f" if crit_hit > 0 else "\u274c")
            with st.expander(
                f"{icon} **{dp_id}**: {_t('critical_actions_count', hit=crit_hit, total=crit_total)}",
                expanded=False,
            ):
                for action in actions:
                    aid = action.get("id", "")
                    req = (action.get("requirement") or "optional").lower()
                    is_crit = req == "critical" or aid in critical_ids
                    was_selected = aid in dp_selected

                    if is_crit:
                        mark = "\u2705" if was_selected else "\u274c"
                    else:
                        mark = "\u2611\ufe0f" if was_selected else "\u2610"

                    req_label = req.title()
                    st.markdown(f"{mark} `{aid}` [{req_label}] {action.get('description', '')}")

    st.markdown("---")

    # --- Learning objectives assessed ---
    los = scenario.get("learning_objectives", [])
    if los:
        section_label(_t("lo_assessed"))
        completed_dps = set(st.session_state.sim_completed_dps)
        for lo in los:
            if isinstance(lo, dict):
                assessed_at = lo.get("assessed_at", [])
                assessed_count = sum(1 for dp_id in assessed_at if dp_id in completed_dps)
                total = len(assessed_at)
                icon = "\u2705" if assessed_count == total and total > 0 else "\u26a0\ufe0f"
                st.markdown(
                    f"{icon} **{lo.get('id', '?')}:** {lo.get('description', '')} "
                    f"({_t('lo_assessed_at')}: {', '.join(assessed_at)})"
                )
        st.markdown("---")

    # --- Common errors matched ---
    matched_errors = match_common_errors(scenario, all_selected)
    if matched_errors:
        section_label(_t("errors_identified"))
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
        st.success(_t("no_errors"))

    st.markdown("---")

    # --- Debriefing points (with citations) ---
    debriefing = scenario.get("debriefing", [])
    if debriefing:
        section_label(_t("clinical_debriefing"))
        action_index = build_action_index(scenario)
        for debrief in debriefing:
            render_debriefing_point(debrief, action_index)
            # Show citation if present on debriefing point
            citation = debrief.get("citation")
            if citation:
                st.caption(f"{_t('debrief_citation')}: {citation}")

    # --- Key takeaways ---
    takeaways = scenario.get("key_takeaways", [])
    if takeaways:
        section_label(_t("key_takeaways"))
        for t in takeaways:
            st.markdown(f"- {t}")

    st.markdown("---")

    if st.button(_t("try_again"), type="primary", use_container_width=True):
        scenario_data = st.session_state.sim_scenario_data
        reset_simulation()
        st.session_state.sim_scenario_data = scenario_data
        st.session_state.sim_phase = "briefing"
        st.rerun()

    if st.button(_t("choose_another"), use_container_width=True):
        reset_simulation()
        st.rerun()


# PHASE: VIEW (full scenario, print-friendly)
def phase_view():
    render_language_toggle()
    scenario = st.session_state.sim_scenario_data

    if not scenario:
        st.session_state.sim_phase = "select"
        st.rerun()
        return

    # --- Title & metadata ---
    page_header(scenario.get("title", "Untitled"), scenario.get("domain", ""))
    render_scenario_banner(scenario)

    # --- Quick stats ---
    stages = scenario.get("stages", [])
    branches = scenario.get("branches", [])
    total_dps = sum(len(s.get("decision_points", [])) for s in stages)
    total_dps += sum(len(b.get("decision_points", [])) for b in branches)
    total_actions = sum(
        len(dp.get("available_actions", []))
        for s in stages for dp in s.get("decision_points", [])
    )
    total_actions += sum(
        len(dp.get("available_actions", []))
        for b in branches for dp in b.get("decision_points", [])
    )
    total_critical = sum(
        1 for s in stages for dp in s.get("decision_points", [])
        for a in dp.get("available_actions", [])
        if (a.get("requirement") or "").lower() == "critical" or a.get("id") in set(dp.get("critical_action_ids", []))
    )

    stats_html = (
        f'<div class="view-stats-bar">'
        f'<div class="view-stat"><div class="view-stat-value">{len(stages)}</div><div class="view-stat-label">{_t("stages")}</div></div>'
        f'<div class="view-stat"><div class="view-stat-value">{total_dps}</div><div class="view-stat-label">{_t("decision_point")}s</div></div>'
        f'<div class="view-stat"><div class="view-stat-value">{total_actions}</div><div class="view-stat-label">{_t("available_actions")}</div></div>'
        f'<div class="view-stat"><div class="view-stat-value">{total_critical}</div><div class="view-stat-label">{_t("critical_actions")}</div></div>'
        f'<div class="view-stat"><div class="view-stat-value">{len(branches)}</div><div class="view-stat-label">{_t("branches")}</div></div>'
        f'</div>'
    )
    st.markdown(stats_html, unsafe_allow_html=True)

    # --- Patient profile ---
    patient = scenario.get("patient")
    if patient:
        st.markdown('<div class="view-section-title">' + _t("patient_profile") + '</div>', unsafe_allow_html=True)
        render_patient_profile(patient)

    # --- Initial presentation ---
    presentation = scenario.get("initial_presentation")
    if presentation:
        st.markdown('<div class="view-section-title">' + _t("initial_presentation") + '</div>', unsafe_allow_html=True)
        st.info(presentation)

    # --- Interaction prompt ---
    prompt = scenario.get("interaction_prompt")
    if prompt:
        st.markdown('<div class="view-section-title">' + _t("your_role") + '</div>', unsafe_allow_html=True)
        st.markdown(prompt)

    # --- Clinical time window ---
    tw = scenario.get("clinical_time_window")
    if tw:
        st.markdown('<div class="view-section-title">' + _t("clinical_time_window") + '</div>', unsafe_allow_html=True)
        onset = format_minutes_as_hours(tw.get("symptom_onset_minutes_ago"))
        window = format_minutes_as_hours(tw.get("max_treatment_window_minutes"))
        remaining = format_minutes_as_hours(tw.get("remaining_window_minutes"))
        st.markdown(
            f'<div class="time-window-alert">'
            f"<strong>{_t('symptom_onset')}:</strong> {onset} ago &bull; "
            f"<strong>{_t('treatment_window')}:</strong> {window} &bull; "
            f"<strong>{_t('remaining')}:</strong> {remaining}"
            f"</div>",
            unsafe_allow_html=True,
        )
        rationale = tw.get("time_pressure_rationale")
        if rationale:
            st.caption(rationale)

    # --- Learning objectives ---
    los = scenario.get("learning_objectives", [])
    if los:
        st.markdown('<div class="view-section-title">' + _t("learning_objectives") + '</div>', unsafe_allow_html=True)
        for lo in los:
            if isinstance(lo, dict):
                cognitive = lo.get("cognitive_demand", "")
                assessed = ", ".join(lo.get("assessed_at", []))
                st.markdown(
                    f"- **{lo.get('id', '?')}:** {lo.get('description', '')}"
                    + (f" *({cognitive})*" if cognitive else "")
                    + (f" — assessed at: {assessed}" if assessed else "")
                )

    # --- Prerequisites ---
    prereqs = scenario.get("prerequisites", [])
    if prereqs:
        st.markdown('<div class="view-section-title">' + _t("prerequisites") + '</div>', unsafe_allow_html=True)
        for p in prereqs:
            st.markdown(f"- {p}")

    # --- Always-available information ---
    always = scenario.get("always_available_information")
    if always:
        st.markdown('<div class="view-section-title">' + _t("always_available_info") + '</div>', unsafe_allow_html=True)
        for k, v in always.items():
            st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")

    # --- Stages ---
    if stages:
        st.markdown('<div class="view-section-title">' + _t("stages") + f" ({len(stages)})" + '</div>', unsafe_allow_html=True)

        prev_vital_signs = None
        for s_idx, stage in enumerate(stages):
            stage_name = _esc(stage.get("name", f"Stage {s_idx + 1}"))
            setting = _esc(stage.get("setting", ""))
            setting_html = f'<div class="stage-setting">{_t("setting")}: {setting}</div>' if setting else ""

            st.markdown(
                f'<div class="view-stage-section">'
                f'<div class="view-stage-header">'
                f'<div class="stage-name">{_t("stage")} {s_idx + 1}: {stage_name}</div>'
                f'{setting_html}'
                f'</div></div>',
                unsafe_allow_html=True,
            )

            # Initial state
            initial_state = stage.get("initial_state")
            if initial_state:
                st.markdown(f"*{initial_state}*")

            # Vital signs — full for first stage, diff only for subsequent
            vs = stage.get("vital_signs")
            if vs:
                if s_idx == 0 or prev_vital_signs is None:
                    section_label(_t("vital_signs"))
                    render_vital_signs(vs, layout="grid")
                else:
                    diff = compute_vital_signs_diff(vs, prev_vital_signs)
                    if diff:
                        section_label(_t("vital_signs_changed"))
                        render_vital_signs(diff, layout="grid")
                    else:
                        st.caption(_t("no_vital_changes"))
                prev_vital_signs = vs

            # Optional info
            all_optional = stage.get("all_optional", [])
            if all_optional:
                section_label(_t("additional_info"))
                for item in all_optional:
                    if isinstance(item, dict):
                        label = item.get("description") or item.get("category") or item.get("id", "?")
                        content = item.get("finding") or item.get("content", "")
                        st.markdown(f"**{label}:** {content}")

            # Progression criteria
            prog = stage.get("progression_criteria")
            if prog:
                st.caption(f"{_t('progression_criteria')}: {prog}")

            # Decision points
            dps = stage.get("decision_points", [])
            for dp_idx, dp in enumerate(dps):
                dp_id = dp.get("id", "")
                critical_ids = set(dp.get("critical_action_ids", []))

                st.markdown(
                    f'<div class="sim-dp-header">'
                    f'<div class="dp-label">{_t("decision_point")} {dp_idx + 1}/{len(dps)} &bull; {_esc(str(dp_id))}</div>'
                    f'<div class="dp-context">{_esc(dp.get("context", ""))}</div>'
                    f"</div>",
                    unsafe_allow_html=True,
                )

                actions = dp.get("available_actions", [])
                n_critical = sum(
                    1 for a in actions
                    if (a.get("requirement") or "").lower() == "critical" or a.get("id") in critical_ids
                )
                n_supportive = sum(
                    1 for a in actions
                    if (a.get("requirement") or "").lower() == "supportive"
                )
                st.markdown(
                    f'<div class="view-dp-summary">'
                    f'{len(actions)} actions &bull; {n_critical} critical &bull; {n_supportive} supportive'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # Feedback on completion
                feedback = dp.get("feedback_on_completion")
                if feedback:
                    st.success(f"**{_t('feedback')}:** {feedback}")

                for action in actions:
                    action_id = action.get("id", "")
                    is_critical = (action.get("requirement") or "").lower() == "critical" or action_id in critical_ids
                    render_action_card_static(action, is_critical=is_critical)

            st.markdown("---")

    # --- Branches ---
    if branches:
        st.markdown('<div class="view-section-title">' + _t("branches") + f" ({len(branches)})" + '</div>', unsafe_allow_html=True)

        for branch in branches:
            branch_id = _esc(branch.get("id", "?"))
            branch_type = _esc(branch.get("branch_type", ""))
            trigger_context = _esc(branch.get("trigger_context", ""))
            consequence = _esc(branch.get("consequence_context", ""))
            merge = branch.get("merge_point")

            # Use a Streamlit container so the border-left wraps all content
            with st.container():
                st.markdown(
                    f'<div class="view-branch-header">'
                    f'<div class="branch-type">{_t("branch_type")}: {branch_type}</div>'
                    f'<div class="branch-name">{_t("phase_branch")} {branch_id}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                meta_parts = []
                if trigger_context:
                    meta_parts.append(f"**{_t('trigger')}:** {trigger_context}")
                if consequence:
                    meta_parts.append(f"**{_t('consequence')}:** {consequence}")
                if merge:
                    meta_parts.append(f"**{_t('merge_point')}:** {merge}")
                else:
                    meta_parts.append(f"**{_t('terminal_branch')}**")
                st.markdown(" | ".join(meta_parts))

                # Branch decision points
                branch_dps = branch.get("decision_points", [])
                for dp_idx, dp in enumerate(branch_dps):
                    dp_id = dp.get("id", "")
                    critical_ids = set(dp.get("critical_action_ids", []))

                    st.markdown(
                        f'<div class="sim-dp-header">'
                        f'<div class="dp-label">{_t("branch_dp", current=dp_idx + 1, total=len(branch_dps))} &bull; {_esc(str(dp_id))}</div>'
                        f'<div class="dp-context">{_esc(dp.get("context", ""))}</div>'
                        f"</div>",
                        unsafe_allow_html=True,
                    )

                    actions = dp.get("available_actions", [])
                    n_critical = sum(
                        1 for a in actions
                        if (a.get("requirement") or "").lower() == "critical" or a.get("id") in critical_ids
                    )
                    st.markdown(
                        f'<div class="view-dp-summary">{len(actions)} actions &bull; {n_critical} critical</div>',
                        unsafe_allow_html=True,
                    )

                    feedback = dp.get("feedback_on_completion")
                    if feedback:
                        st.success(f"**{_t('feedback')}:** {feedback}")

                    for action in actions:
                        action_id = action.get("id", "")
                        is_critical = (action.get("requirement") or "").lower() == "critical" or action_id in critical_ids
                        render_action_card_static(action, is_critical=is_critical)

            st.markdown("---")

    # --- Debriefing ---
    debriefing = scenario.get("debriefing", [])
    if debriefing:
        st.markdown('<div class="view-section-title">' + _t("clinical_debriefing") + '</div>', unsafe_allow_html=True)
        action_index = build_action_index(scenario)
        for debrief in debriefing:
            render_debriefing_point(debrief, action_index)
            citation = debrief.get("citation")
            if citation:
                st.caption(f"{_t('debrief_citation')}: {citation}")

    # --- Key takeaways ---
    takeaways = scenario.get("key_takeaways", [])
    if takeaways:
        st.markdown('<div class="view-section-title">' + _t("key_takeaways") + '</div>', unsafe_allow_html=True)
        for t in takeaways:
            st.markdown(f"- {t}")

    st.markdown("---")

    # --- Navigation ---
    col1, col2 = st.columns([3, 1])
    with col1:
        if st.button(_t("back"), use_container_width=True):
            reset_simulation()
            st.rerun()
    with col2:
        st.markdown(
            f'<button onclick="window.print()" style="'
            f'width:100%; padding:0.45rem 1.2rem; border-radius:6px; border:1.5px solid #d9d9d9; '
            f'background:#3c6e71; color:white; font-weight:600; font-family:DM Sans,sans-serif; '
            f'cursor:pointer; font-size:0.875rem;">{_t("print_scenario")}</button>',
            unsafe_allow_html=True,
        )


# Phase router helper
def run_phase_router(phase_select_fn):
    """Run the simulation phase router.

    Parameters
    ----------
    phase_select_fn : callable
        The function to call for the 'select' phase.  This is provided by
        the calling app since scenario loading differs between standalone
        and the main multi-page app.
    """
    phase = st.session_state.sim_phase

    if phase == "select":
        phase_select_fn()
    elif phase == "briefing":
        phase_briefing()
    elif phase == "play":
        phase_play()
    elif phase == "branch":
        phase_branch()
    elif phase == "debrief":
        phase_debrief()
    elif phase == "view":
        phase_view()
    else:
        reset_simulation()
        st.rerun()

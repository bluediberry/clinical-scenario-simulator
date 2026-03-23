"""Unified theme for the SBL Clinical Scenario Generator.

Import `apply_theme()` at the top of every page to inject the global CSS.
Use the helper functions for consistent, styled components.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Global CSS — injected once per page via apply_theme()
# Color tokens are defined as CSS custom properties in :root below.
# ---------------------------------------------------------------------------
_GLOBAL_CSS = """
<style>
/* ── Google Fonts ───────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=DM+Sans:wght@400;500;600;700&display=swap');

/* ── Root variables ─────────────────────────────────────────────────── */
:root {
    --c-primary: #1B2A4A;
    --c-primary-light: #2563EB;
    --c-accent-warm: #C2410C;
    --c-accent-teal: #0F766E;
    --c-bg: #F8F6F3;
    --c-surface: #FFFFFF;
    --c-surface-alt: #EFECE8;
    --c-border: #E5E1DC;
    --c-border-strong: #D1CBC3;
    --c-text: #1A1A2E;
    --c-text-muted: #6B7280;
    --c-text-light: #9CA3AF;
    --c-success: #059669;
    --c-warning: #D97706;
    --c-error: #DC2626;
    --font-display: 'Fraunces', Georgia, serif;
    --font-body: 'DM Sans', system-ui, sans-serif;
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --shadow-sm: 0 1px 3px rgba(27,42,74,0.06);
    --shadow-md: 0 4px 12px rgba(27,42,74,0.08);
    --shadow-lg: 0 8px 24px rgba(27,42,74,0.10);
}

/* ── Global typography ──────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
}

h1, h2, h3, .main-header {
    font-family: var(--font-display) !important;
    color: var(--c-primary) !important;
    letter-spacing: -0.02em;
}

/* ── Page background & main container ───────────────────────────────── */
.stApp {
    background: var(--c-bg);
}

[data-testid="stAppViewBlockContainer"] {
    max-width: 1200px;
    padding: 2rem 2.5rem 4rem !important;
}

/* ── Sidebar ────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--c-primary) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: #E0E7F1 !important;
}

[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label {
    color: #B0BFD4 !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    color: #CBD5E1 !important;
    font-weight: 500;
    padding: 0.6rem 1rem;
    border-radius: var(--radius-sm);
    transition: background 0.15s, color 0.15s;
    text-transform: capitalize;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(255,255,255,0.12) !important;
    color: #FFFFFF !important;
}

/* Home icon for main page (first nav link) */
[data-testid="stSidebarNav"] li:first-child a {
    visibility: hidden;
    position: relative;
}
[data-testid="stSidebarNav"] li:first-child a::after {
    content: 'Home';
    visibility: visible;
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    text-transform: none;
}

/* ── Top header bar ─────────────────────────────────────────────────── */
[data-testid="stHeader"] {
    background: transparent !important;
    backdrop-filter: blur(12px);
}

/* ── Buttons ────────────────────────────────────────────────────────── */
.stButton > button {
    font-family: var(--font-body) !important;
    font-weight: 600;
    border-radius: var(--radius-sm) !important;
    border: 1.5px solid var(--c-border-strong) !important;
    background: var(--c-surface) !important;
    color: var(--c-primary) !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.15s ease;
    box-shadow: var(--shadow-sm);
}

.stButton > button:hover {
    background: var(--c-primary) !important;
    color: #FFFFFF !important;
    border-color: var(--c-primary) !important;
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.stButton > button[kind="primary"],
.stButton > button[data-testid="stFormSubmitButton"] {
    background: var(--c-primary) !important;
    color: #FFFFFF !important;
    border-color: var(--c-primary) !important;
}

.stButton > button[kind="primary"]:hover {
    background: var(--c-primary-light) !important;
    border-color: var(--c-primary-light) !important;
}

/* Form submit button */
[data-testid="stFormSubmitButton"] > button {
    background: var(--c-primary) !important;
    color: #FFFFFF !important;
    border-color: var(--c-primary) !important;
    font-weight: 700;
    letter-spacing: 0.02em;
}

[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--c-primary-light) !important;
    border-color: var(--c-primary-light) !important;
}

/* ── Metrics ────────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--c-surface);
    padding: 1rem 1.25rem;
    border-radius: var(--radius-md);
    border: 1px solid var(--c-border);
    box-shadow: var(--shadow-sm);
}

[data-testid="stMetric"] label {
    color: var(--c-text-muted) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--c-primary) !important;
    font-family: var(--font-display) !important;
    font-weight: 700 !important;
}

/* ── Tabs ───────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0 !important;
    border-bottom: 2px solid var(--c-border);
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    font-family: var(--font-body) !important;
    font-weight: 600;
    color: var(--c-text-muted);
    padding: 0.7rem 1.4rem;
    border-bottom: 3px solid transparent;
    transition: all 0.15s;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--c-primary);
    background: rgba(27,42,74,0.03);
}

.stTabs [aria-selected="true"] {
    color: var(--c-primary) !important;
    border-bottom-color: var(--c-primary-light) !important;
}

/* ── Expanders ──────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--c-surface);
    border: 1px solid var(--c-border) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    font-weight: 600;
    color: var(--c-primary);
}

/* ── Forms ───────────────────────────────────────────────────────────── */
[data-testid="stForm"] {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
}

/* ── Inputs ──────────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: var(--radius-sm) !important;
    border-color: var(--c-border-strong) !important;
    font-family: var(--font-body) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--c-primary-light) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}

/* ── Select boxes ────────────────────────────────────────────────────── */
[data-baseweb="select"] {
    border-radius: var(--radius-sm) !important;
}

/* ── Data frames & tables ────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--c-border);
}

.stTable table {
    border-collapse: separate;
    border-spacing: 0;
    border-radius: var(--radius-md);
    overflow: hidden;
    border: 1px solid var(--c-border);
}

.stTable th {
    background: var(--c-primary) !important;
    color: #FFFFFF !important;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
    padding: 0.7rem 1rem !important;
}

.stTable td {
    padding: 0.6rem 1rem !important;
    border-bottom: 1px solid var(--c-border);
}

.stTable tr:nth-child(even) {
    background: var(--c-surface-alt);
}

/* ── Progress bars ───────────────────────────────────────────────────── */
.stProgress > div > div {
    background: var(--c-border) !important;
    border-radius: 99px;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--c-primary), var(--c-primary-light)) !important;
    border-radius: 99px;
}

/* ── Alerts ──────────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    border-left-width: 4px !important;
    font-family: var(--font-body) !important;
}

/* ── Dividers ────────────────────────────────────────────────────────── */
hr {
    border-color: var(--c-border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Download buttons ────────────────────────────────────────────────── */
.stDownloadButton > button {
    font-family: var(--font-body) !important;
    font-weight: 600;
    border-radius: var(--radius-sm) !important;
}

/* ── Radio buttons (horizontal) ──────────────────────────────────────── */
.stRadio > div {
    gap: 0.5rem;
}

/* ── JSON viewer ─────────────────────────────────────────────────────── */
[data-testid="stJson"] {
    border-radius: var(--radius-md);
    border: 1px solid var(--c-border);
}

/* ── Containers with border ──────────────────────────────────────────── */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--c-border) !important;
    border-radius: var(--radius-md) !important;
}

/* ── File uploader ───────────────────────────────────────────────────── */
[data-testid="stFileUploader"] {
    border-radius: var(--radius-md);
}

/* ── Custom component classes ────────────────────────────────────────── */
.page-header {
    font-family: var(--font-display);
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--c-primary);
    margin-bottom: 0.3rem;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

.page-subtitle {
    font-family: var(--font-body);
    font-size: 1.05rem;
    color: var(--c-text-muted);
    margin-bottom: 1.8rem;
    line-height: 1.5;
}

.section-label {
    font-family: var(--font-body);
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--c-text-light);
    margin-bottom: 0.5rem;
}

.nav-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-lg);
    padding: 1.6rem;
    height: 100%;
    transition: all 0.2s ease;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
}

.nav-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--c-primary), var(--c-primary-light));
    opacity: 0;
    transition: opacity 0.2s;
}

.nav-card:hover {
    border-color: var(--c-primary-light);
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

.nav-card:hover::before {
    opacity: 1;
}

.nav-card-icon {
    font-size: 1.8rem;
    margin-bottom: 0.8rem;
    display: block;
}

.nav-card-title {
    font-family: var(--font-display);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--c-primary);
    margin-bottom: 0.4rem;
}

.nav-card-desc {
    font-size: 0.88rem;
    color: var(--c-text-muted);
    line-height: 1.5;
}

.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--c-surface-alt);
    border: 1px solid var(--c-border);
    border-radius: 99px;
    padding: 0.35rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--c-primary);
}

.stat-pill-value {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 0.95rem;
}

.config-banner {
    background: linear-gradient(135deg, var(--c-primary), #2D4470);
    color: #FFFFFF;
    padding: 1.2rem 1.6rem;
    border-radius: var(--radius-lg);
    display: flex;
    align-items: center;
    gap: 1.5rem;
    box-shadow: var(--shadow-md);
    margin-bottom: 1.5rem;
}

.config-banner-item {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.config-banner-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.7;
}

.config-banner-value {
    font-family: var(--font-display);
    font-size: 1.05rem;
    font-weight: 700;
}

.config-banner-sep {
    width: 1px;
    height: 2rem;
    background: rgba(255,255,255,0.2);
}

.form-section-heading {
    font-family: var(--font-display);
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--c-primary);
    padding-bottom: 0.4rem;
    border-bottom: 2px solid var(--c-border);
    margin: 1.2rem 0 0.8rem 0;
}

/* ── Simulation page ──────────────────────────────────────────────── */
.sim-phase-indicator {
    display: flex;
    gap: 0.35rem;
    align-items: center;
    margin-bottom: 1.2rem;
    font-family: var(--font-body);
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--c-text-light);
}
.sim-phase-indicator .phase {
    padding: 0.3rem 0.7rem;
    border-radius: 99px;
    background: var(--c-surface-alt);
    border: 1px solid var(--c-border);
    transition: all 0.15s;
}
.sim-phase-indicator .phase.active {
    background: var(--c-primary);
    color: #FFFFFF;
    border-color: var(--c-primary);
}
.sim-phase-indicator .phase.done {
    background: var(--c-success);
    color: #FFFFFF;
    border-color: var(--c-success);
}
.sim-phase-indicator .sep {
    color: var(--c-border-strong);
}
.sim-action-hit-critical {
    background: #F0FDF4;
    border-left: 4px solid var(--c-success);
    padding: 0.5rem 0.8rem;
    border-radius: var(--radius-sm);
    margin-bottom: 0.4rem;
}
.sim-action-missed-critical {
    background: #FEF2F2;
    border-left: 4px solid var(--c-error);
    padding: 0.5rem 0.8rem;
    border-radius: var(--radius-sm);
    margin-bottom: 0.4rem;
}
.sim-score-card {
    background: var(--c-surface);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-lg);
    padding: 1.4rem;
    box-shadow: var(--shadow-sm);
    text-align: center;
}
.sim-score-card .score-value {
    font-family: var(--font-display);
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--c-primary);
    line-height: 1.1;
}
.sim-score-card .score-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--c-text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 0.3rem;
}
.sim-score-card.success { border-top: 4px solid var(--c-success); }
.sim-score-card.warning { border-top: 4px solid var(--c-warning); }
.sim-score-card.danger  { border-top: 4px solid var(--c-error); }
.sim-dp-header {
    background: linear-gradient(135deg, var(--c-primary), #2D4470);
    color: #FFFFFF;
    padding: 1rem 1.4rem;
    border-radius: var(--radius-md);
    margin-bottom: 1rem;
}
.sim-dp-header .dp-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.7;
    margin-bottom: 0.25rem;
}
.sim-dp-header .dp-context {
    font-size: 1rem;
    line-height: 1.5;
}
</style>
"""


def apply_theme() -> None:
    """Inject the global CSS theme into the current page. Call once per page."""
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Reusable component helpers
# ---------------------------------------------------------------------------


def page_header(title: str, subtitle: str = "") -> None:
    """Render a styled page header with optional subtitle."""
    st.markdown(f'<p class="page-header">{title}</p>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="page-subtitle">{subtitle}</p>', unsafe_allow_html=True)


def section_label(text: str) -> None:
    """Render a small uppercase section label."""
    st.markdown(f'<p class="section-label">{text}</p>', unsafe_allow_html=True)


def config_banner(items: list[tuple[str, str]]) -> None:
    """Render a dark banner showing current pipeline configuration.

    Parameters
    ----------
    items : list of (label, value) tuples
    """
    inner = ""
    for i, (label, value) in enumerate(items):
        if i > 0:
            inner += '<div class="config-banner-sep"></div>'
        inner += (
            f'<div class="config-banner-item">'
            f'<span class="config-banner-label">{label}</span>'
            f'<span class="config-banner-value">{value}</span>'
            f'</div>'
        )
    st.markdown(f'<div class="config-banner">{inner}</div>', unsafe_allow_html=True)


def nav_card(icon: str, title: str, description: str) -> None:
    """Render the HTML part of a navigation card. Place a st.button after this."""
    st.markdown(
        f'<div class="nav-card">'
        f'<span class="nav-card-icon">{icon}</span>'
        f'<div class="nav-card-title">{title}</div>'
        f'<div class="nav-card-desc">{description}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def form_section(title: str) -> None:
    """Render a styled section heading inside a form."""
    st.markdown(
        f'<div class="form-section-heading">{title}</div>',
        unsafe_allow_html=True,
    )

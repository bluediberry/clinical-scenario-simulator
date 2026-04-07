"""Unified theme for the SBL Clinical Scenario Generator.

Import `apply_theme()` at the top of every page to inject the global CSS.
Use the helper functions for consistent, styled components.
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Global CSS — injected once per page via apply_theme()
# Color palette:
#   Graphite #353535 | Stormy Teal #3c6e71 | White #ffffff
#   Dust Grey #d9d9d9 | Yale Blue #284b63
# ---------------------------------------------------------------------------
_GLOBAL_CSS = """
<style>
/* ── Google Fonts ───────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=DM+Sans:wght@400;500;600;700&display=swap');

/* ── Root variables ─────────────────────────────────────────────────── */
:root {
    --c-graphite: #353535;
    --c-teal: #3c6e71;
    --c-teal-light: #4a8a8d;
    --c-teal-dark: #2d5557;
    --c-yale: #284b63;
    --c-yale-light: #3a6580;
    --c-white: #ffffff;
    --c-dust: #d9d9d9;
    --c-dust-light: #f0f0f0;
    --c-bg: #ffffff;
    --c-surface: #ffffff;
    --c-surface-alt: #f5f5f5;
    --c-border: #e0e0e0;
    --c-border-strong: #d9d9d9;
    --c-text: #353535;
    --c-text-muted: #6b7280;
    --c-text-light: #9ca3af;
    --c-success: #059669;
    --c-warning: #d97706;
    --c-error: #dc2626;
    --font-display: 'Fraunces', Georgia, serif;
    --font-body: 'DM Sans', system-ui, sans-serif;
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --shadow-sm: 0 1px 3px rgba(40,75,99,0.06);
    --shadow-md: 0 4px 12px rgba(40,75,99,0.08);
    --shadow-lg: 0 8px 24px rgba(40,75,99,0.10);
}

/* ── Global typography ──────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
}

h1, h2, h3, .main-header {
    font-family: var(--font-display) !important;
    color: var(--c-yale) !important;
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
    background: var(--c-yale) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: #e0e7f1 !important;
}

[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stSelectbox label {
    color: #b0bfd4 !important;
}

/* Vital signs rows in sidebar */
[data-testid="stSidebar"] .vital-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 0.4rem 0.6rem;
    margin-bottom: 0.25rem;
    background: rgba(255,255,255,0.1);
    border-radius: var(--radius-sm);
}
[data-testid="stSidebar"] .vital-label {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #b0bfd4 !important;
}
[data-testid="stSidebar"] .vital-value {
    font-family: var(--font-display) !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

/* Metrics inside sidebar (elapsed time): dark text on white card */
[data-testid="stSidebar"] [data-testid="stMetric"] *,
[data-testid="stSidebar"] [data-testid="stMetric"] [data-testid="stMetricValue"],
[data-testid="stSidebar"] [data-testid="stMetric"] [data-testid="stMetricValue"] div {
    color: #284b63 !important;
    font-size: 2rem !important;
}
[data-testid="stSidebar"] [data-testid="stMetric"] label,
[data-testid="stSidebar"] [data-testid="stMetric"] label *,
[data-testid="stSidebar"] [data-testid="stMetric"] [data-testid="stMetricLabel"],
[data-testid="stSidebar"] [data-testid="stMetric"] [data-testid="stMetricLabel"] div {
    color: #6b7280 !important;
    font-size: 0.8rem !important;
}

/* Expanders inside sidebar: dark text on white background */
[data-testid="stSidebar"] [data-testid="stExpander"] *,
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: var(--c-text) !important;
}

/* Captions inside sidebar: brighter on dark background */
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] *,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #ffffff !important;
    opacity: 0.85;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    color: #cbd5e1 !important;
    font-weight: 500;
    padding: 0.6rem 1rem;
    border-radius: var(--radius-sm);
    transition: background 0.15s, color 0.15s;
    text-transform: capitalize;
}

[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover,
[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(255,255,255,0.12) !important;
    color: #ffffff !important;
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
    color: var(--c-graphite) !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.15s ease;
    box-shadow: var(--shadow-sm);
}

.stButton > button:hover {
    background: var(--c-teal) !important;
    color: #ffffff !important;
    border-color: var(--c-teal) !important;
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}

.stButton > button[kind="primary"],
.stButton > button[data-testid="stFormSubmitButton"] {
    background: var(--c-teal) !important;
    color: #ffffff !important;
    border-color: var(--c-teal) !important;
}

.stButton > button[kind="primary"]:hover {
    background: var(--c-teal-dark) !important;
    border-color: var(--c-teal-dark) !important;
}

/* Form submit button */
[data-testid="stFormSubmitButton"] > button {
    background: var(--c-teal) !important;
    color: #ffffff !important;
    border-color: var(--c-teal) !important;
    font-weight: 700;
    letter-spacing: 0.02em;
}

[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--c-teal-dark) !important;
    border-color: var(--c-teal-dark) !important;
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
    color: var(--c-yale) !important;
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
    color: var(--c-yale);
    background: rgba(40,75,99,0.03);
}

.stTabs [aria-selected="true"] {
    color: var(--c-yale) !important;
    border-bottom-color: var(--c-teal) !important;
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
    color: var(--c-yale);
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
    border-color: var(--c-teal) !important;
    box-shadow: 0 0 0 3px rgba(60,110,113,0.12) !important;
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
    background: var(--c-yale) !important;
    color: #ffffff !important;
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
    background: linear-gradient(90deg, var(--c-teal), var(--c-teal-light)) !important;
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
    color: var(--c-yale);
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
    border: 1.5px solid var(--c-border);
    border-radius: var(--radius-lg);
    padding: 1.6rem 1.6rem 1rem;
    height: 100%;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    box-shadow: var(--shadow-sm);
    cursor: pointer;
    display: flex;
    flex-direction: column;
}

.nav-card:hover {
    border-color: var(--c-teal);
    box-shadow: var(--shadow-md);
}

.nav-card-number {
    font-family: var(--font-display);
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--c-teal);
    margin-bottom: 0.6rem;
    opacity: 0.5;
}

.nav-card-title {
    font-family: var(--font-display);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--c-yale);
    margin-bottom: 0.4rem;
}

.nav-card-desc {
    font-size: 0.88rem;
    color: var(--c-text-muted);
    line-height: 1.5;
    flex: 1;
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
    color: var(--c-yale);
}

.stat-pill-value {
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 0.95rem;
}

.config-banner {
    background: linear-gradient(135deg, var(--c-yale), var(--c-teal-dark));
    color: #ffffff;
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
    color: var(--c-yale);
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
    background: var(--c-teal);
    color: #ffffff;
    border-color: var(--c-teal);
}
.sim-phase-indicator .phase.done {
    background: var(--c-success);
    color: #ffffff;
    border-color: var(--c-success);
}
.sim-phase-indicator .sep {
    color: var(--c-border-strong);
}
.sim-action-hit-critical {
    background: #f0fdf4;
    border-left: 4px solid var(--c-success);
    padding: 0.5rem 0.8rem;
    border-radius: var(--radius-sm);
    margin-bottom: 0.4rem;
}
.sim-action-missed-critical {
    background: #fef2f2;
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
    color: var(--c-yale);
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
    background: linear-gradient(135deg, var(--c-yale), var(--c-teal-dark));
    color: #ffffff;
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

/* ── Print styles ────────────────────────────────────────────────── */
@media print {
    /* Hide Streamlit chrome */
    [data-testid="stSidebar"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    .stButton,
    .stDownloadButton,
    .sim-phase-indicator,
    .no-print,
    [data-testid="stFileUploader"] {
        display: none !important;
    }

    /* Full width */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        padding: 0 1rem !important;
    }

    .stApp {
        background: white !important;
    }

    /* Preserve colors in print */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    /* Avoid breaking inside cards */
    .sim-dp-header,
    .action-hint-critical,
    .action-hint-supportive,
    .action-hint-optional,
    .key-learning-card,
    .vital-signs-card {
        page-break-inside: avoid;
    }

    /* Reduce spacing for print */
    .page-header {
        font-size: 1.8rem;
    }

    hr {
        margin: 0.8rem 0 !important;
    }
}

/* ── Full scenario view styles ───────────────────────────────────── */
.view-stage-section {
    margin-top: 1.5rem;
}

.view-stage-header {
    background: var(--c-yale);
    color: #ffffff;
    padding: 0.8rem 1.2rem;
    border-radius: var(--radius-md);
    margin-bottom: 1rem;
}

.view-stage-header .stage-name {
    font-family: var(--font-display);
    font-size: 1.2rem;
    font-weight: 700;
}

.view-stage-header .stage-setting {
    font-size: 0.85rem;
    opacity: 0.8;
    margin-top: 0.2rem;
}

.view-branch-header {
    background: linear-gradient(135deg, #DB2777, #9333EA);
    color: #ffffff;
    padding: 0.8rem 1.2rem;
    border-radius: var(--radius-md);
    margin-bottom: 1rem;
}

.view-branch-header .branch-name {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 700;
}

.view-branch-header .branch-type {
    font-size: 0.78rem;
    opacity: 0.8;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.view-section-title {
    font-family: var(--font-display);
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--c-yale);
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.3rem;
    border-bottom: 2px solid var(--c-border);
}

/* Vital signs grid (main content area) */
.vital-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0.5rem;
    margin: 0.5rem 0 1rem 0;
}
.vital-card {
    background: var(--c-surface-alt);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-md);
    padding: 0.6rem 0.8rem;
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}
.vital-card .vital-label {
    font-size: 0.68rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--c-text-muted);
}
.vital-card .vital-value {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--c-yale);
}

/* Keep the row style for sidebar (overridden there) */
.vital-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    padding: 0.4rem 0.6rem;
    margin-bottom: 0.25rem;
    background: var(--c-surface-alt);
    border-radius: var(--radius-sm);
    border: 1px solid var(--c-border);
}
.vital-row .vital-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--c-text-muted);
}
.vital-row .vital-value {
    font-family: var(--font-display);
    font-size: 1rem;
    font-weight: 700;
    color: var(--c-yale);
}

/* Quick stats bar for full scenario view */
.view-stats-bar {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.view-stat {
    background: var(--c-surface-alt);
    border: 1px solid var(--c-border);
    border-radius: var(--radius-md);
    padding: 0.6rem 1rem;
    text-align: center;
    flex: 1;
    min-width: 120px;
}
.view-stat-value {
    font-family: var(--font-display);
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--c-yale);
}
.view-stat-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--c-text-muted);
}

/* DP summary line in full view */
.view-dp-summary {
    font-size: 0.8rem;
    color: var(--c-text-muted);
    margin: 0.3rem 0 0.6rem 0;
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
        f'<span class="nav-card-number">{icon}</span>'
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

APP_CSS = """
<style>

/* ═══════════════════════════════════════════════
   SIDEBAR — Clean White Light Theme
═══════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1.5px solid #e2e8f0 !important;
    box-shadow: 2px 0 12px rgba(37, 99, 235, 0.06) !important;
}
[data-testid="stSidebar"] * {
    color: #1e293b !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #1e293b !important;
}
/* Sidebar section title */
[data-testid="stSidebar"] .stMarkdown h2 {
    font-size: 14px !important;
    font-weight: 800 !important;
    color: #1e293b !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 4px !important;
}
/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: #e2e8f0 !important;
    margin: 12px 0 !important;
}
/* Sidebar file uploader */
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: #f8fafc !important;
    border: 1.5px dashed #cbd5e1 !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {
    border-color: #2563eb !important;
    background: #eff6ff !important;
}
/* Sidebar inputs */
[data-testid="stSidebar"] [data-baseweb="input"] {
    background: #f8fafc !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-baseweb="input"]:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.10) !important;
}
[data-testid="stSidebar"] [data-baseweb="input"] input {
    color: #1e293b !important;
    background: transparent !important;
}
/* Sidebar button */
[data-testid="stSidebar"] .stButton > button {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 10px 0 !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.25) !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35) !important;
}
/* Sidebar label text */
[data-testid="stSidebar"] [data-testid="stTextInput"] label,
[data-testid="stSidebar"] [data-testid="stFileUploader"] label {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #64748b !important;
    letter-spacing: 0.2px !important;
}

/* ═══════════════════════════════════════════════
   GLOBAL APP BACKGROUND
═══════════════════════════════════════════════ */
[data-testid="stAppViewContainer"] {
    background: #f1f5f9 !important;
}
[data-testid="stMain"] {
    background: #f1f5f9 !important;
}

/* ═══════════════════════════════════════════════
   INPUTS — Force Light Mode
═══════════════════════════════════════════════ */
[data-baseweb="input"],
[data-baseweb="base-input"] {
    background-color: #ffffff !important;
    border: 1.5px solid #dde3ed !important;
    border-radius: 8px !important;
    transition: border-color 0.15s ease !important;
}
[data-baseweb="input"]:focus-within,
[data-baseweb="base-input"]:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
}
[data-baseweb="input"] input,
[data-baseweb="base-input"] input {
    background-color: #ffffff !important;
    color: #1e293b !important;
    font-size: 14px !important;
}
input::placeholder {
    color: #b0b8c8 !important;
    font-style: italic;
}

/* SELECT / DROPDOWN */
[data-baseweb="select"] > div:first-child {
    background-color: #ffffff !important;
    border: 1.5px solid #dde3ed !important;
    border-radius: 8px !important;
    color: #1e293b !important;
}
[data-baseweb="select"] > div:first-child:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
}
[data-baseweb="select"] [data-baseweb="icon"] { color: #64748b !important; }
[data-baseweb="popover"],
[data-baseweb="menu"] {
    background-color: #ffffff !important;
    border-radius: 10px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
}
[data-baseweb="option"] {
    background-color: #ffffff !important;
    color: #1e293b !important;
    font-size: 13px !important;
}
[data-baseweb="option"]:hover { background-color: #eff6ff !important; }

/* Number input spinners */
[data-testid="stNumberInput"] button {
    background: #f1f5f9 !important;
    color: #1e293b !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 6px !important;
}

/* Form container */
[data-testid="stForm"]  { background: transparent !important; border: none !important; padding: 0 !important; }
.stForm                 { background: transparent !important; border: none !important; }

/* Input labels */
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label {
    color: #374151 !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    margin-bottom: 2px !important;
}

/* ═══════════════════════════════════════════════
   FORM CARD — Modal Style
═══════════════════════════════════════════════ */
.emp-form-card {
    background: #ffffff;
    border: 1.5px solid #e2e8f0;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(37,99,235,0.10), 0 1px 4px rgba(0,0,0,0.06);
    margin: 12px 0 18px 0;
}
.emp-form-header {
    background: linear-gradient(120deg, #1d4ed8 0%, #2563eb 60%, #3b82f6 100%);
    padding: 16px 22px 14px 22px;
    display: flex;
    flex-direction: column;
    gap: 2px;
}
.emp-form-title {
    font-size: 16px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.2px;
}
.emp-form-subtitle {
    font-size: 12px;
    color: rgba(255,255,255,0.70);
    font-weight: 400;
}
.emp-form-body { padding: 20px 22px 16px 22px; }

/* Form primary button */
.emp-form-card [data-testid="column"]:first-child [data-testid="stFormSubmitButton"] button {
    background: #2563eb !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 0 !important;
    box-shadow: 0 2px 8px rgba(37,99,235,0.30) !important;
    transition: all 0.15s ease !important;
}
.emp-form-card [data-testid="column"]:first-child [data-testid="stFormSubmitButton"] button:hover {
    background: #1d4ed8 !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.40) !important;
}
/* Form cancel button */
.emp-form-card [data-testid="column"]:last-child [data-testid="stFormSubmitButton"] button {
    background: #f1f5f9 !important;
    color: #64748b !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px 0 !important;
}
.emp-form-card [data-testid="column"]:last-child [data-testid="stFormSubmitButton"] button:hover {
    background: #e2e8f0 !important;
    color: #374151 !important;
}

/* ═══════════════════════════════════════════════
   CARDS
═══════════════════════════════════════════════ */
.clean-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px 28px 20px 28px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}
.card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 16px;
    letter-spacing: -0.2px;
}

/* ═══════════════════════════════════════════════
   EMPLOYEE TABLE
═══════════════════════════════════════════════ */
.th-cell {
    font-size: 11px;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 0.9px;
    text-transform: uppercase;
    padding: 6px 4px 10px 4px;
}
.table-divider {
    height: 2px;
    background: linear-gradient(90deg, #e2e8f0, #f8fafc);
    border-radius: 2px;
    margin-bottom: 4px;
}
.table-row-divider {
    height: 1px;
    background: #f1f5f9;
    margin: 2px 0 4px 0;
}

/* ═══════════════════════════════════════════════
   AVATAR
═══════════════════════════════════════════════ */
.avatar-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-weight: 800;
    font-size: 15px;
    margin-top: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    flex-shrink: 0;
}

/* ═══════════════════════════════════════════════
   EMPLOYEE INFO
═══════════════════════════════════════════════ */
.emp-name-main {
    font-weight: 700; font-size: 14px; color: #1e293b;
    margin-top: 5px; line-height: 1.3;
}
.emp-id-sub {
    font-size: 11px; color: #94a3b8; margin-top: 2px; font-weight: 500;
}
.emp-full-name {
    font-size: 13px; color: #475569; margin-top: 8px; line-height: 1.4;
}

/* ═══════════════════════════════════════════════
   BADGES
═══════════════════════════════════════════════ */
.sched-badge {
    display: inline-flex; align-items: center;
    border: 1.5px solid #cbd5e1; border-radius: 20px;
    padding: 3px 11px; font-size: 12px; color: #334155;
    font-weight: 500; margin-top: 8px; white-space: nowrap;
    background: #f8fafc;
}
.status-active-badge {
    display: inline-flex; align-items: center;
    background: #dcfce7; color: #15803d;
    border: 1.5px solid #bbf7d0; border-radius: 20px;
    padding: 3px 11px; font-size: 12px; font-weight: 700; margin-top: 8px;
}

/* ═══════════════════════════════════════════════
   ALERT BOXES
═══════════════════════════════════════════════ */
.warn-box {
    background: #fef9c3; border-left: 4px solid #eab308;
    border-radius: 8px; padding: 12px 16px; margin-bottom: 12px;
    color: #713f12; font-size: 0.9rem;
}
.info-box {
    background: #eff6ff; border-left: 4px solid #3b82f6;
    border-radius: 8px; padding: 10px 16px; margin-bottom: 10px;
    color: #1e40af; font-size: 0.875rem;
}
.success-box {
    background: #f0fdf4; border-left: 4px solid #22c55e;
    border-radius: 8px; padding: 10px 16px; margin-bottom: 10px;
    color: #14532d; font-size: 0.875rem;
}

/* ═══════════════════════════════════════════════
   METRIC CARDS
═══════════════════════════════════════════════ */
.metric-box {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 16px 20px; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.metric-label {
    font-size: 11px; font-weight: 700; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 6px;
}
.metric-value {
    font-size: 1.9rem; font-weight: 800; color: #1e293b; line-height: 1;
}

/* ═══════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════ */
div[data-testid="stTabs"] [data-baseweb="tab"] {
    font-weight: 600; font-size: 0.875rem;
    padding: 10px 20px; color: #475569 !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    color: #2563eb !important;
}

/* ═══════════════════════════════════════════════
   GENERAL BUTTONS
═══════════════════════════════════════════════ */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.15s ease !important;
    background: #f1f5f9 !important;
    color: #1e293b !important;
    border: 1px solid #e2e8f0 !important;
}
.stButton > button:hover {
    background: #e2e8f0 !important;
    border-color: #cbd5e1 !important;
}
.stDownloadButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    background: #f1f5f9 !important;
    color: #1e293b !important;
    border: 1px solid #e2e8f0 !important;
}

/* ═══════════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════════ */
.footer {
    text-align: center;
    font-size: 11px;
    font-weight: 700;
    color: #94a3b8;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    padding: 24px 0 12px 0;
}

</style>
"""
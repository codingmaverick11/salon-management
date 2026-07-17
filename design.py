import streamlit as st

COLORS = {
    "bg": "#F8F5F2",          # warm ivory page background
    "surface": "#FFFFFF",     # card surface
    "ink": "#2B2323",         # primary text (warm charcoal, not pure black)
    "ink_soft": "#6B615F",    # secondary / muted text
    "rose": "#A6445C",        # primary accent — buttons, active states
    "rose_soft": "#F1DCE0",   # pale rose — card borders, badges
    "gold": "#B08A4E",        # secondary accent — owner-tier highlights
    "sage": "#6E8B74",        # success / confirmation only
    "border": "#E9E1DC",      # hairline borders
}

FONT_DISPLAY = "Fraunces"   # headings only — warm editorial serif
FONT_BODY = "Manrope"       # everything else


def apply_theme():
    """Inject fonts + global CSS. Call once, right after st.set_page_config()."""

    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">

        <style>
        :root {{
            --bg: {COLORS['bg']};
            --surface: {COLORS['surface']};
            --ink: {COLORS['ink']};
            --ink-soft: {COLORS['ink_soft']};
            --rose: {COLORS['rose']};
            --rose-soft: {COLORS['rose_soft']};
            --gold: {COLORS['gold']};
            --sage: {COLORS['sage']};
            --border: {COLORS['border']};
        }}

        /* ---------- base ---------- */
        .stApp {{
            background: var(--bg);
            font-family: '{FONT_BODY}', sans-serif;
            color: var(--ink);
        }}

        h1, h2, h3 {{
            font-family: '{FONT_DISPLAY}', serif !important;
            color: var(--ink) !important;
            font-weight: 600 !important;
            letter-spacing: -0.01em;
        }}

        p, span, label, div {{
            font-family: '{FONT_BODY}', sans-serif;
        }}

        .block-container {{
             padding-top: 1.5rem;
            padding-left: 1rem;
            padding-right: 1rem;
            max-width: 100%;
        }}

        /* ---------- eyebrow / page header ---------- */
        .app-eyebrow {{
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--rose);
            margin-bottom: 0.15rem;
        }}

        /* ---------- sidebar ---------- */
        [data-testid="stSidebar"] {{
            background: var(--surface);
            border-right: 1px solid var(--border);
        }}
        [data-testid="stSidebar"] .stButton > button {{
            background: transparent;
            color: var(--rose);
            border: 1px solid var(--rose-soft);
        }}
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: var(--rose-soft);
            border-color: var(--rose);
        }}

        .role-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: var(--rose-soft);
            color: var(--rose);
            font-weight: 700;
            font-size: 0.8rem;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            margin-bottom: 1.25rem;
        }}

        /* ---------- buttons ---------- */
        .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{
            background: var(--rose);
            color: #fff;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            padding: 0.55rem 1rem;
            transition: transform 0.08s ease, background 0.15s ease;
        }}
        .stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {{
            background: #8f3a4f;
            transform: translateY(-1px);
        }}

        /* ---------- inputs ---------- */
        .stTextInput input, .stNumberInput input, .stDateInput input, .stTimeInput input,
        [data-baseweb="select"] > div {{
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: 8px !important;
            color: var(--ink) !important;
        }}
        .stTextInput input:focus, .stNumberInput input:focus {{
            border-color: var(--rose) !important;
            box-shadow: 0 0 0 1px var(--rose) !important;
        }}

        /* ---------- forms as tickets ---------- */
        [data-testid="stForm"] {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-left: 3px solid var(--rose);
            border-radius: 10px;
            padding: 1.5rem 1.5rem 1rem 1.5rem;
        }}

        /* ---------- tabs ---------- */
        [data-testid="stTabs"] button[role="tab"] {{
            font-weight: 700;
            color: var(--ink-soft);
        }}
        [data-testid="stTabs"] button[aria-selected="true"] {{
            color: var(--rose);
        }}
        [data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
            background-color: var(--rose) !important;
        }}

        /* ---------- dataframes ---------- */
        [data-testid="stDataFrame"] {{
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
        }}

        /* ---------- alerts ---------- */
        [data-testid="stAlert"] {{
            border-radius: 8px;
        }}

        /* ---------- divider ---------- */
        hr {{
            border-color: var(--border) !important;
            margin: 1.75rem 0 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
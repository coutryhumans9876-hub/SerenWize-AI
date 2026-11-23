"""
SerenWize-AI - Giao diện lavender / tím pastel
Đặt file này vào modules/theme.py
"""
import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

:root {
    --ink: #2B2142;
    --ink-soft: #6B5F82;
    --ink-mute: #857A9B;
    --lav-50: #FAF8FF;
    --lav-100: #F3EEFF;
    --lav-200: #E8DFFC;
    --lav-300: #D6C8F7;
    --lav-400: #BDA9F0;
    --lav-500: #9F84E6;
    --lav-600: #7F60D8;
    --lav-700: #6747BD;
    --rose: #F6DFF4;
    --sky: #DDE6FF;
    --line: rgba(127, 96, 216, 0.14);
    --glass: rgba(255, 255, 255, 0.72);
    --shadow: 0 1px 2px rgba(80, 50, 140, 0.05), 0 14px 34px -14px rgba(80, 50, 140, 0.22);
}

/* ---------- Nền & khung chung ---------- */
html, body, [class*="css"] { font-family: 'Be Vietnam Pro', sans-serif; }

.stApp {
    background:
        radial-gradient(900px 520px at 6% -6%, #EADFFF 0%, transparent 62%),
        radial-gradient(800px 520px at 100% 0%, #DDE6FF 0%, transparent 56%),
        radial-gradient(760px 520px at 62% 112%, #F6DFF4 0%, transparent 62%),
        var(--lav-50);
    background-attachment: fixed;
    color: var(--ink);
}

[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.block-container {
    max-width: 1160px;
    padding-top: 2.4rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    color: var(--ink) !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}
h1 { font-size: 2.1rem !important; }
p, li, label, .stMarkdown { color: var(--ink-soft); line-height: 1.75; }
a { color: var(--lav-700) !important; }
::selection { background: var(--lav-300); color: var(--ink); }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(243,238,255,0.92) 0%, rgba(250,248,255,0.92) 100%);
    backdrop-filter: blur(18px);
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] > div:first-child { padding: 1.4rem 0.9rem 1rem; }

[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: var(--ink-mute);
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 8px;
}

[data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child { display: none; }

[data-testid="stSidebar"] [role="radiogroup"] label {
    width: 100%;
    padding: 11px 14px;
    border-radius: 14px;
    border: 1px solid transparent;
    transition: background 0.18s ease, border-color 0.18s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label p {
    color: #4B3D6B;
    font-size: 14.5px;
    font-weight: 500;
    margin: 0;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: var(--lav-200); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #fff;
    border-color: var(--lav-300);
    box-shadow: 0 6px 16px -8px rgba(103, 71, 189, 0.35);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {
    color: var(--lav-700);
    font-weight: 700;
}

.sw-brand { display: flex; align-items: center; gap: 12px; padding: 4px 6px 18px; }
.sw-brand-mark {
    width: 44px; height: 44px; border-radius: 15px;
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, var(--lav-400), var(--lav-700));
    color: #fff; font-size: 22px;
    box-shadow: 0 8px 18px -6px rgba(103, 71, 189, 0.55);
}
.sw-brand-name { color: var(--ink); font-size: 19px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.2; }
.sw-brand-tag { color: var(--ink-mute); font-size: 12px; margin-top: 2px; }

/* ---------- Nút bấm ---------- */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg, var(--lav-600), var(--lav-700));
    color: #fff;
    border: none;
    border-radius: 999px;
    padding: 0.6rem 1.6rem;
    font-weight: 600;
    box-shadow: 0 10px 22px -10px rgba(103, 71, 189, 0.7);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {
    color: #fff;
    border: none;
    transform: translateY(-2px);
    box-shadow: 0 14px 26px -10px rgba(103, 71, 189, 0.8);
}
.stButton > button:active { transform: translateY(0); }
.stButton > button:disabled { opacity: 0.45; box-shadow: none; transform: none; }
.stButton > button p, .stDownloadButton > button p { color: #fff; margin: 0; }

/* ---------- Ô nhập liệu ---------- */
[data-baseweb="textarea"], [data-baseweb="input"], [data-baseweb="select"] > div {
    background: rgba(255, 255, 255, 0.85) !important;
    border: 1px solid var(--line) !important;
    border-radius: 16px !important;
}
[data-baseweb="textarea"]:focus-within, [data-baseweb="input"]:focus-within, [data-baseweb="select"] > div:focus-within {
    border-color: var(--lav-500) !important;
    box-shadow: 0 0 0 4px rgba(159, 132, 230, 0.22) !important;
}
textarea, input { color: var(--ink) !important; }

[data-testid="stFileUploaderDropzone"] {
    background: rgba(255, 255, 255, 0.7);
    border: 1.5px dashed var(--lav-400);
    border-radius: 22px;
    padding: 1.6rem;
    transition: background 0.18s ease, border-color 0.18s ease;
}
[data-testid="stFileUploaderDropzone"]:hover { background: #fff; border-color: var(--lav-600); }

/* ---------- Thành phần Streamlit ---------- */
[data-testid="stMetric"] {
    background: var(--glass);
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 18px 20px;
    box-shadow: var(--shadow);
}
[data-testid="stMetricLabel"] p { color: var(--ink-mute); font-size: 13px; }
[data-testid="stMetricValue"] { color: var(--ink); font-weight: 800; }

[data-baseweb="tab-list"] {
    gap: 4px;
    width: fit-content;
    padding: 5px;
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid var(--line);
    border-radius: 999px;
}
[data-baseweb="tab"] { border-radius: 999px; padding: 8px 18px; height: auto; }
[data-baseweb="tab"] p { font-weight: 600; margin: 0; }
[data-baseweb="tab"][aria-selected="true"] {
    background: #fff;
    box-shadow: 0 4px 12px -6px rgba(103, 71, 189, 0.4);
}
[data-baseweb="tab"][aria-selected="true"] p { color: var(--lav-700); }
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] { display: none; }

[data-testid="stExpander"] {
    background: var(--glass);
    border: 1px solid var(--line);
    border-radius: 20px;
    overflow: hidden;
}
[data-testid="stAlert"] { border-radius: 18px; border: 1px solid var(--line); }
[data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 18px; overflow: hidden; }
.stProgress > div > div > div > div { background: linear-gradient(90deg, var(--lav-400), var(--lav-700)); }
hr { border-color: var(--line) !important; }

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: var(--lav-300); border-radius: 999px; }

:focus-visible { outline: 3px solid var(--lav-500); outline-offset: 2px; }

/* ---------- Thẻ & thành phần dùng chung ---------- */
.stApp .sw-section { margin: 34px 0 18px; }
.stApp .sw-section-title { color: var(--ink); font-size: 22px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 4px; }
.stApp .sw-section-desc { color: var(--ink-mute); font-size: 14px; }

.stApp .sw-feature-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 18px; }
.stApp .sw-tech-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; }

.stApp .sw-card, .stApp .sw-tech-card, .stApp .info-card, .stApp .feature-card {
    background: var(--glass);
    backdrop-filter: blur(10px);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 24px;
    min-height: 0;
    box-shadow: var(--shadow);
}
.stApp .sw-card { transition: transform 0.2s ease, box-shadow 0.2s ease; }
.stApp .sw-card:hover { transform: translateY(-3px); }
.stApp .sw-tech-card { text-align: center; padding: 22px 14px; }

.stApp .sw-icon {
    display: flex; align-items: center; justify-content: center;
    width: 48px; height: 48px;
    margin-bottom: 16px;
    background: linear-gradient(135deg, var(--lav-200), var(--rose));
    border-radius: 15px;
    font-size: 23px;
}
.stApp .sw-card-title { color: var(--ink); font-size: 17px; font-weight: 700; margin-bottom: 8px; }
.stApp .sw-card-desc { color: var(--ink-soft); font-size: 13.5px; line-height: 1.8; }
.stApp .sw-card-label { color: var(--lav-700); font-size: 12px; font-weight: 600; letter-spacing: 0; margin-top: 14px; }
.stApp .sw-tech-icon { font-size: 26px; margin-bottom: 8px; }
.stApp .sw-tech-title { color: var(--ink); font-size: 14.5px; font-weight: 700; }
.stApp .sw-tech-desc { color: var(--ink-mute); font-size: 12px; margin-top: 4px; }

.stApp .sw-notice {
    background: rgba(255, 255, 255, 0.65);
    border: 1px solid var(--line);
    border-left: 4px solid var(--lav-400);
    border-radius: 18px;
    padding: 16px 20px;
    color: var(--ink-soft);
}

.stApp .footer { text-align: center; color: var(--ink-mute); font-size: 12.5px; padding: 32px 0 8px; }

@media (max-width: 760px) {
    .stApp .sw-feature-grid { grid-template-columns: 1fr; }
    .stApp .sw-tech-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (prefers-reduced-motion: reduce) {
    .stApp .sw-card, .stButton > button { transition: none; }
}
</style>
"""


def apply_theme():
    """Gọi 1 lần ngay sau st.set_page_config()."""
    st.markdown(CSS, unsafe_allow_html=True)


def sidebar_brand(name="SerenWize-AI", tagline="Lắng nghe cảm xúc của bạn"):
    """Logo ở đầu thanh bên. Gọi bên trong `with st.sidebar:` trước st.radio."""
    st.html(
        f'<div class="sw-brand">'
        f'<div class="sw-brand-mark">♡</div>'
        f'<div><div class="sw-brand-name">{name}</div>'
        f'<div class="sw-brand-tag">{tagline}</div></div></div>'
    )


def section(title, desc=""):
    d = f'<div class="sw-section-desc">{desc}</div>' if desc else ""
    st.html(f'<div class="sw-section"><div class="sw-section-title">{title}</div>{d}</div>')


def feature_card(icon, title, desc, label=""):
    lab = f'<div class="sw-card-label">{label}</div>' if label else ""
    return (
        f'<div class="sw-card"><div class="sw-icon">{icon}</div>'
        f'<div class="sw-card-title">{title}</div>'
        f'<div class="sw-card-desc">{desc}</div>{lab}</div>'
    )


def feature_grid(cards):
    """cards: list các tuple (icon, title, desc, label)."""
    inner = "".join(feature_card(*c) for c in cards)
    st.html(f'<div class="sw-feature-grid">{inner}</div>')


def notice(text):
    st.html(f'<div class="sw-notice">{text}</div>')


def footer():
    st.html(
        '<div class="footer">♡ SerenWize-AI · Understand Emotions. Empower Minds.'
        '<br>Lắng nghe cảm xúc – Thấu hiểu tâm lý – Đồng hành cùng bạn</div>'
    )
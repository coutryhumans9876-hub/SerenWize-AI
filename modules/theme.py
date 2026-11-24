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

/* ===== v2: Sidebar có icon (kiểu ảnh 2) ===== */
[data-testid="stSidebar"] [role="radiogroup"] { gap: 6px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    display: flex; align-items: center; gap: 12px;
    padding: 8px 12px 8px 8px; border-radius: 18px; cursor: pointer;
}
[data-testid="stSidebar"] [role="radiogroup"] label::before {
    content: ""; flex: 0 0 38px; width: 38px; height: 38px; border-radius: 13px;
    background-color: var(--lav-100); background-repeat: no-repeat;
    background-position: center; background-size: 20px 20px;
    transition: background-color 0.18s ease, transform 0.18s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: rgba(255,255,255,0.75); }
[data-testid="stSidebar"] [role="radiogroup"] label:hover::before { background-color: var(--lav-200); transform: scale(1.06); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #9378EC 0%, #6747BD 100%);
    border-color: transparent;
    box-shadow: 0 12px 24px -12px rgba(103, 71, 189, 0.75);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked)::before { background-color: rgba(255,255,255,0.22); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p { color: #fff; font-weight: 700; }
[data-testid="stSidebar"] [role="radiogroup"] label p { font-size: 14.5px; line-height: 1.35; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] { display: none; }
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(1)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(1) label::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(1)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%237F60D8'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='m3%209%209-7%209%207v11a2%202%200%200%201-2%202H5a2%202%200%200%201-2-2z'/%3E%3Cpolyline%20points='9%2022%209%2012%2015%2012%2015%2022'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(1):has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(1) label:has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(1):has(input:checked)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23FFFFFF'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='m3%209%209-7%209%207v11a2%202%200%200%201-2%202H5a2%202%200%200%201-2-2z'/%3E%3Cpolyline%20points='9%2022%209%2012%2015%2012%2015%2022'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(2)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(2) label::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(2)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%237F60D8'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M14.5%202H6a2%202%200%200%200-2%202v16a2%202%200%200%200%202%202h12a2%202%200%200%200%202-2V7.5z'/%3E%3Cpath%20d='M14%202v6h6'/%3E%3Cpath%20d='M16%2013H8'/%3E%3Cpath%20d='M16%2017H8'/%3E%3Cpath%20d='M10%209H8'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(2):has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(2) label:has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(2):has(input:checked)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23FFFFFF'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M14.5%202H6a2%202%200%200%200-2%202v16a2%202%200%200%200%202%202h12a2%202%200%200%200%202-2V7.5z'/%3E%3Cpath%20d='M14%202v6h6'/%3E%3Cpath%20d='M16%2013H8'/%3E%3Cpath%20d='M16%2017H8'/%3E%3Cpath%20d='M10%209H8'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(3)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(3) label::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(3)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%237F60D8'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M12%202a3%203%200%200%200-3%203v7a3%203%200%200%200%206%200V5a3%203%200%200%200-3-3z'/%3E%3Cpath%20d='M19%2010v2a7%207%200%200%201-14%200v-2'/%3E%3Cline%20x1='12'%20x2='12'%20y1='19'%20y2='22'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(3):has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(3) label:has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(3):has(input:checked)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23FFFFFF'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M12%202a3%203%200%200%200-3%203v7a3%203%200%200%200%206%200V5a3%203%200%200%200-3-3z'/%3E%3Cpath%20d='M19%2010v2a7%207%200%200%201-14%200v-2'/%3E%3Cline%20x1='12'%20x2='12'%20y1='19'%20y2='22'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(4)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(4) label::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(4)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%237F60D8'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M19%2021v-2a4%204%200%200%200-4-4H9a4%204%200%200%200-4%204v2'/%3E%3Ccircle%20cx='12'%20cy='7'%20r='4'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(4):has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(4) label:has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(4):has(input:checked)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23FFFFFF'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M19%2021v-2a4%204%200%200%200-4-4H9a4%204%200%200%200-4%204v2'/%3E%3Ccircle%20cx='12'%20cy='7'%20r='4'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(5)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(5) label::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(5)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%237F60D8'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cline%20x1='12'%20x2='12'%20y1='20'%20y2='10'/%3E%3Cline%20x1='18'%20x2='18'%20y1='20'%20y2='4'/%3E%3Cline%20x1='6'%20x2='6'%20y1='20'%20y2='16'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(5):has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(5) label:has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(5):has(input:checked)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23FFFFFF'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cline%20x1='12'%20x2='12'%20y1='20'%20y2='10'/%3E%3Cline%20x1='18'%20x2='18'%20y1='20'%20y2='4'/%3E%3Cline%20x1='6'%20x2='6'%20y1='20'%20y2='16'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(6)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(6) label::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(6)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%237F60D8'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M19%2014c1.49-1.46%203-3.21%203-5.5A5.5%205.5%200%200%200%2016.5%203c-1.76%200-3%20.5-4.5%202-1.5-1.5-2.74-2-4.5-2A5.5%205.5%200%200%200%202%208.5c0%202.3%201.5%204.05%203%205.5l7%207Z'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(6):has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(6) label:has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(6):has(input:checked)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23FFFFFF'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M19%2014c1.49-1.46%203-3.21%203-5.5A5.5%205.5%200%200%200%2016.5%203c-1.76%200-3%20.5-4.5%202-1.5-1.5-2.74-2-4.5-2A5.5%205.5%200%200%200%202%208.5c0%202.3%201.5%204.05%203%205.5l7%207Z'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(7)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(7) label::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(7)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%237F60D8'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M17.7%207.7a2.5%202.5%200%201%201%201.8%204.3H2'/%3E%3Cpath%20d='M9.6%204.6A2%202%200%201%201%2011%208H2'/%3E%3Cpath%20d='M12.6%2019.4A2%202%200%201%200%2014%2016H2'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(7):has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(7) label:has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(7):has(input:checked)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23FFFFFF'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Cpath%20d='M17.7%207.7a2.5%202.5%200%201%201%201.8%204.3H2'/%3E%3Cpath%20d='M9.6%204.6A2%202%200%201%201%2011%208H2'/%3E%3Cpath%20d='M12.6%2019.4A2%202%200%201%200%2014%2016H2'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(8)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(8) label::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(8)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%237F60D8'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Ccircle%20cx='12'%20cy='12'%20r='10'/%3E%3Cpath%20d='M12%2016v-4'/%3E%3Cpath%20d='M12%208h.01'/%3E%3C/svg%3E");}
[data-testid="stSidebar"] [role="radiogroup"] label:nth-of-type(8):has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > *:nth-child(8) label:has(input:checked)::before, [data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(8):has(input:checked)::before{background-image:url("data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2024%2024'%20fill='none'%20stroke='%23FFFFFF'%20stroke-width='2'%20stroke-linecap='round'%20stroke-linejoin='round'%3E%3Ccircle%20cx='12'%20cy='12'%20r='10'/%3E%3Cpath%20d='M12%2016v-4'/%3E%3Cpath%20d='M12%208h.01'/%3E%3C/svg%3E");}
.sw-tip {
    display: flex; gap: 12px; align-items: flex-start; margin-top: 10px; padding: 14px;
    background: #fff; border: 1px solid var(--line); border-radius: 20px; box-shadow: var(--shadow);
}
.sw-tip-ico { flex: 0 0 38px; height: 38px; border-radius: 13px; display: flex; align-items: center; justify-content: center;
    background: var(--lav-100); font-size: 19px; }
.sw-tip-title { color: var(--ink); font-size: 13.5px; font-weight: 700; line-height: 1.35; }
.sw-tip-text { color: var(--ink-mute); font-size: 12.5px; line-height: 1.55; margin-top: 3px; }
.sw-ver { color: var(--ink-mute); font-size: 11.5px; text-align: center; margin-top: 12px; }

/* ===== v2: Tiêu đề trang dạng thẻ ===== */
.pg-head {
    display: flex; align-items: center; gap: 18px; padding: 22px 26px; margin: 0 0 26px;
    background: linear-gradient(125deg, rgba(234,223,255,0.9) 0%, rgba(243,232,251,0.9) 55%, rgba(221,230,255,0.9) 100%);
    border: 1px solid rgba(255,255,255,0.9); border-radius: 28px; box-shadow: var(--shadow);
}
.pg-head-ico {
    flex: 0 0 56px; height: 56px; border-radius: 18px; display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #9378EC, #6747BD); box-shadow: 0 12px 22px -10px rgba(103,71,189,0.7);
}
.pg-head-ico svg { width: 28px; height: 28px; stroke: #fff; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.pg-head-title { color: var(--ink); font-size: 26px; font-weight: 800; letter-spacing: -0.02em; line-height: 1.25; }
.pg-head-desc { color: var(--ink-soft); font-size: 14px; margin-top: 4px; line-height: 1.6; }

/* ===== v2: Thẻ hiện đại cho nội dung từng mục ===== */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) { border-radius: 24px; }
div[data-testid="stVerticalBlockBorderWrapper"][class*="st-"] { background: var(--glass); border-color: var(--line); box-shadow: var(--shadow); }
.stApp h3 { position: relative; padding-left: 16px; margin-top: 1.4rem; font-size: 1.25rem !important; }
.stApp h3::before {
    content: ""; position: absolute; left: 0; top: 0.2em; bottom: 0.2em; width: 5px; border-radius: 999px;
    background: linear-gradient(180deg, var(--lav-400), var(--lav-700));
}
[data-testid="stTextArea"] textarea { min-height: 150px; font-size: 15px; line-height: 1.7; }
[data-testid="stFileUploaderDropzone"] { background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(243,238,255,0.9)); }
[data-testid="stAlert"] { background: rgba(255,255,255,0.8); box-shadow: var(--shadow); }
[data-testid="stMetric"] { transition: transform 0.2s ease; }
[data-testid="stMetric"]:hover { transform: translateY(-3px); }
[data-testid="stRadio"] [role="radiogroup"] label { border-radius: 14px; }
[data-testid="stSelectbox"] [data-baseweb="select"] > div { min-height: 46px; }
[data-testid="stSlider"] [role="slider"] { background: var(--lav-600); box-shadow: 0 0 0 5px rgba(159,132,230,0.25); }
[data-testid="stPlotlyChart"], [data-testid="stVegaLiteChart"], [data-testid="stImage"] img, [data-testid="stPyplot"] img {
    border-radius: 22px; }
[data-testid="stAudio"] audio { border-radius: 999px; width: 100%; }
@media (max-width: 760px) { .pg-head { padding: 16px; } .pg-head-title { font-size: 21px; } }

/* ===== FIX: luôn hiển thị thanh menu bên trái (màn hình rộng) ===== */
@media (min-width: 900px) {
    section[data-testid="stSidebar"] {
        transform: none !important;
        visibility: visible !important;
        display: flex !important;
        margin-left: 0 !important;
        min-width: 300px !important;
        width: 300px !important;
    }
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] { display: none !important; }
}
[data-testid="stSidebarCollapsedControl"] button, [data-testid="collapsedControl"] button { color: var(--lav-700); }

/* ===== v3: Giao diện theo mockup ===== */
[data-testid="stSidebar"] [role="radiogroup"] label :not(:has(p)):not(p):not(p *):not(input) { display: none !important; }
[data-testid="stSidebar"] [role="radiogroup"] label > *:has(p) { display: block !important; visibility: visible !important; opacity: 1 !important; }
[data-testid="stSidebar"] [role="radiogroup"] label p { visibility: visible !important; opacity: 1 !important; margin: 0; }
[data-testid="stSidebar"] [role="radiogroup"] label input[type="radio"] { position: absolute !important; opacity: 0 !important; width: 0 !important; height: 0 !important; pointer-events: none; }
.sw-brand-mark img { display: block; margin: 0 auto; }
.sw-brand { flex-direction: column; text-align: center; gap: 6px; padding: 4px 6px 14px; }
.sw-brand-mark { width: auto; height: auto; background: none; box-shadow: none; }
.sw-brand-mark svg { width: 46px; height: 46px; stroke: var(--lav-600); fill: rgba(159,132,230,0.18); stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
.sw-brand-name { font-size: 20px; color: var(--lav-700); }
.sw-brand-tag { font-size: 11.5px; line-height: 1.4; }
.sw-menu-label { color: var(--ink-mute); font-size: 11px; font-weight: 700; letter-spacing: 0.14em; padding: 6px 10px 8px; }

.tb { display: flex; align-items: center; justify-content: space-between; padding: 4px 4px 18px; margin-bottom: 18px; border-bottom: 1px solid var(--line); }
.tb-title { color: var(--ink); font-size: 22px; font-weight: 800; letter-spacing: -0.02em; }
.tb-title i { font-style: normal; color: var(--lav-600); margin-right: 6px; }
.tb-sub { color: var(--ink-mute); font-size: 13px; margin-top: 2px; }

[class*="st-key-card_"] {
    background: rgba(255,255,255,0.9); border: 1px solid var(--line); border-radius: 26px;
    padding: 22px 24px; box-shadow: var(--shadow);
}
.stApp h4 { color: var(--ink) !important; font-size: 1.05rem !important; font-weight: 700 !important; margin: 0 0 4px !important; }

.em-pill {
    display: inline-block; padding: 10px 26px; margin: 4px 0 14px; border-radius: 999px;
    background: linear-gradient(135deg, #F6DFF4, #E8DFFC); color: var(--lav-700);
    font-size: 20px; font-weight: 800; box-shadow: var(--shadow);
}
.em-label { color: var(--ink-mute); font-size: 12.5px; margin-bottom: 2px; }
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin: 6px 0 14px; }
.chip { padding: 6px 14px; border-radius: 999px; background: var(--lav-100); color: var(--lav-700); font-size: 13px; font-weight: 600; border: 1px solid var(--line); }
.chip.muted { background: #F4F2F8; color: var(--ink-mute); }
.tip-box { display: flex; gap: 12px; padding: 14px 16px; margin: 6px 0 12px; background: linear-gradient(135deg, #F1FBF3, #F3EEFF); border: 1px solid var(--line); border-radius: 18px; }
.tip-ico { flex: 0 0 34px; height: 34px; border-radius: 12px; background: #fff; display: flex; align-items: center; justify-content: center; font-size: 17px; }
.tip-title { color: var(--ink); font-size: 14px; font-weight: 700; }
.tip-text { color: var(--ink-soft); font-size: 13.5px; line-height: 1.65; margin-top: 2px; }
.res-empty { text-align: center; padding: 36px 12px; color: var(--ink-mute); font-size: 14px; line-height: 1.7; }
.res-empty .big { font-size: 38px; display: block; margin-bottom: 6px; }

/* ===== v3.1: ép giao diện sáng cho các thành phần (không phụ thuộc config.toml) ===== */
html, body, .stApp { color-scheme: light; }
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {
    background: #FFFFFF !important; color: var(--ink) !important; border: none !important;
}
[data-testid="stTextArea"] [data-baseweb="textarea"], [data-testid="stTextInput"] [data-baseweb="base-input"],
[data-testid="stTextArea"] [data-baseweb="base-input"] {
    background: #FFFFFF !important; border: 1px solid var(--line) !important; border-radius: 18px !important;
    box-shadow: var(--shadow);
}
[data-testid="stTextArea"] textarea::placeholder, [data-testid="stTextInput"] input::placeholder { color: var(--ink-mute) !important; opacity: 1; }
[data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within { border-color: var(--lav-400) !important; box-shadow: 0 0 0 4px rgba(159,132,230,0.22); }
[data-testid="stAlert"], [data-testid="stAlertContainer"] { background: rgba(255,255,255,0.92) !important; border: 1px solid var(--line); border-radius: 16px; }
[data-testid="stAlert"] *, [data-testid="stAlertContainer"] * { color: var(--ink) !important; }
[data-testid="stAlert"] div, [data-testid="stAlertContainer"] div { background: transparent !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]), [data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) { background: #EFFBF2 !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]), [data-testid="stAlertContainer"]:has([data-testid="stAlertContentInfo"]) { background: #F1EEFF !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]), [data-testid="stAlertContainer"]:has([data-testid="stAlertContentWarning"]) { background: #FFF8E6 !important; }
[data-testid="stAlert"]:has([data-testid="stAlertContentError"]), [data-testid="stAlertContainer"]:has([data-testid="stAlertContentError"]) { background: #FFEFF1 !important; }
[data-testid="stFileUploaderFile"], [data-testid="stFileUploaderFileData"] { background: #FFFFFF !important; border-radius: 14px; }
[data-testid="stFileUploaderFile"] *, [data-testid="stFileUploaderDropzone"] * { color: var(--ink) !important; }
[data-testid="stFileUploaderDropzone"] button { background: var(--lav-100) !important; border: 1px solid var(--line) !important; }
[data-testid="stAudio"] audio { background: #F3EEFF; color-scheme: light; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border-radius: 18px; overflow: hidden; border: 1px solid var(--line); background: #fff; }
[data-testid="stTable"] th, [data-testid="stTable"] td { background: #fff !important; color: var(--ink) !important; }
[data-testid="stMetric"] { background: #fff; }
</style>
"""


DARK_FALLBACK = """
<style>
@media (prefers-color-scheme: dark) {
    [data-testid="stDataFrame"], [data-testid="stVegaLiteChart"], [data-testid="stArrowVegaLiteChart"] {
        filter: invert(1) hue-rotate(180deg);
        background: #fff; border-radius: 18px;
    }
}
</style>
"""


def apply_theme():
    """Gọi 1 lần ngay sau st.set_page_config()."""
    st.markdown(CSS, unsafe_allow_html=True)
    # Nếu chưa đặt theme.base = "light" trong .streamlit/config.toml mà trình duyệt đang ở chế độ tối,
    # bảng và biểu đồ sẽ bị nền đen -> dùng bộ lọc để đưa về sáng.
    try:
        import streamlit as _st
        base = _st.get_option("theme.base")
    except Exception:
        base = None
    if base != "light":
        st.markdown(DARK_FALLBACK, unsafe_allow_html=True)


def sidebar_brand(name="SerenWize-AI", tagline="Understand Emotions. Empower Minds."):
    """Logo ở đầu thanh bên. Gọi bên trong `with st.sidebar:` trước st.radio."""
    heart = icon_img("heart", "#7F60D8", 46)
    st.html(
        f'<div class="sw-brand">'
        f'<div class="sw-brand-mark">{heart}</div>'
        f'<div><div class="sw-brand-name">{name}</div>'
        f'<div class="sw-brand-tag">{tagline}</div></div></div>'
        f'<div class="sw-menu-label">MENU</div>'
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


def _svg(name):
    paths = {
        "home": "<path d='m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z'/><polyline points='9 22 9 12 15 12 15 22'/>",
        "text": "<path d='M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5z'/><path d='M14 2v6h6'/><path d='M16 13H8'/><path d='M16 17H8'/><path d='M10 9H8'/>",
        "mic": "<path d='M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z'/><path d='M19 10v2a7 7 0 0 1-14 0v-2'/><line x1='12' x2='12' y1='19' y2='22'/>",
        "user": "<path d='M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2'/><circle cx='12' cy='7' r='4'/>",
        "chart": "<line x1='12' x2='12' y1='20' y2='10'/><line x1='18' x2='18' y1='20' y2='4'/><line x1='6' x2='6' y1='20' y2='16'/>",
        "heart": "<path d='M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z'/>",
        "wind": "<path d='M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2'/><path d='M9.6 4.6A2 2 0 1 1 11 8H2'/><path d='M12.6 19.4A2 2 0 1 0 14 16H2'/>",
        "info": "<circle cx='12' cy='12' r='10'/><path d='M12 16v-4'/><path d='M12 8h.01'/>",
    }
    return f'<svg viewBox="0 0 24 24">{paths[name]}</svg>'


_NUM = {"home": 1, "text": 2, "mic": 3, "user": 4, "chart": 5, "heart": 6, "wind": 7, "info": 8}


def icon_img(name, color="#6747BD", size=24, cls=""):
    """Icon dạng <img> data-URI (hiển thị chắc chắn trong st.html)."""
    from urllib.parse import quote
    inner = _svg(name)[len('<svg viewBox="0 0 24 24">'):-len("</svg>")].replace('"', "'")
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='{color}' "
           f"stroke-width='2' stroke-linecap='round' stroke-linejoin='round'>{inner}</svg>")
    c = f' class="{cls}"' if cls else ""
    return f'<img{c} width="{size}" height="{size}" alt="" src="data:image/svg+xml,{quote(svg, safe="/=:.,\'-")}">'


def page_header(icon, title, desc=""):
    """Thanh tiêu đề đầu trang có đánh số, ví dụ '3. Phân tích giọng nói'."""
    n = _NUM.get(icon)
    num = f"<i>{n}.</i>" if n else ""
    sub = f'<div class="tb-sub">{desc}</div>' if desc else ""
    st.html(f'<div class="tb"><div><div class="tb-title">{num}{title}</div>{sub}</div></div>')


def emotion_pill(text):
    from html import escape
    st.html(f'<div class="em-label">Cảm xúc chính</div><div class="em-pill">💜 {escape(str(text))}</div>')


def chips(items, tone=""):
    from html import escape
    cls = f"chip {tone}".strip()
    body = "".join(f'<span class="{cls}">{escape(str(x))}</span>' for x in items)
    st.html(f'<div class="chip-row">{body}</div>')


def tip_box(title, text, icon="🌿"):
    from html import escape
    st.html(
        f'<div class="tip-box"><div class="tip-ico">{icon}</div><div>'
        f'<div class="tip-title">{escape(str(title))}</div>'
        f'<div class="tip-text">{escape(str(text))}</div></div></div>'
    )


def empty_state(text, icon="✨"):
    from html import escape
    st.html(f'<div class="res-empty"><span class="big">{icon}</span>{escape(str(text))}</div>')


def sidebar_footer(version="Phiên bản thử nghiệm 1.0"):
    """Thẻ mẹo nhỏ + phiên bản ở cuối thanh bên (thay cho st.divider + st.caption)."""
    st.html(
        '<div class="sw-tip"><div class="sw-tip-ico">✨</div><div>'
        '<div class="sw-tip-title">Mẹo hôm nay</div>'
        '<div class="sw-tip-text">Hít vào 4 giây, giữ 4 giây, thở ra 6 giây. Lặp lại 5 lần để dịu lại.</div>'
        f'</div></div><div class="sw-ver">{version}</div>'
    )
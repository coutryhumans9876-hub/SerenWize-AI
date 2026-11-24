"""Chạy 1 lần trong thư mục chứa app.py:  python patch_v2.py
Tạo modules/layout.py và sửa app.py (bản gốc được lưu thành app_truoc_khi_vá_v2.py)."""
import os, re, shutil

LAYOUT = r'''"""
SerenWize-AI - Bố cục từng mục: thanh bên dạng ô chữ nhật + banner đầu trang
Đặt file này vào modules/layout.py
"""
import streamlit as st

CSS = """
<style>
/* ---------- Thanh bên: mỗi mục là một hình chữ nhật ---------- */
.stApp [data-testid="stSidebar"] [role="radiogroup"] { gap: 10px; }

.stApp [data-testid="stSidebar"] [role="radiogroup"] > label {
    display: flex;
    align-items: center;
    gap: 12px;
    width: 100%;
    padding: 10px 12px;
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid var(--line);
    border-radius: 16px;
    box-shadow: 0 1px 2px rgba(80, 50, 140, 0.05);
    cursor: pointer;
    transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
}
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label::before {
    content: "💜";
    flex: 0 0 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 11px;
    background: var(--lav-100);
    font-size: 17px;
}
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:nth-of-type(1)::before { content: "🏠"; }
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:nth-of-type(2)::before { content: "💬"; }
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:nth-of-type(3)::before { content: "🎙️"; }
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:nth-of-type(4)::before { content: "👤"; }
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:nth-of-type(5)::before { content: "📊"; }
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:nth-of-type(6)::before { content: "🌱"; }
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:nth-of-type(7)::before { content: "🌬️"; }
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:nth-of-type(8)::before { content: "💜"; }

.stApp [data-testid="stSidebar"] [role="radiogroup"] > label p {
    color: #4B3D6B;
    font-size: 14.5px;
    font-weight: 500;
    line-height: 1.35;
    margin: 0;
}
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:hover {
    background: #fff;
    border-color: var(--lav-400);
    transform: translateX(3px);
}
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(135deg, #EDE5FF, #F8EBFB);
    border: 1.5px solid var(--lav-400);
    box-shadow: 0 12px 24px -14px rgba(103, 71, 189, 0.6);
}
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked)::before {
    background: #fff;
    box-shadow: 0 4px 10px -4px rgba(103, 71, 189, 0.45);
}
.stApp [data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) p {
    color: var(--lav-700);
    font-weight: 700;
}

/* ---------- Banner đầu mỗi trang ---------- */
.pg-banner {
    position: relative;
    display: flex;
    align-items: center;
    gap: 18px;
    padding: 22px 28px;
    margin: 0 0 24px;
    background: linear-gradient(125deg, #EADFFF 0%, #F3E8FB 50%, #DDE6FF 100%);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 28px;
    box-shadow: var(--shadow);
    overflow: hidden;
}
.pg-icon {
    flex: 0 0 58px;
    height: 58px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.85);
    border-radius: 19px;
    font-size: 28px;
    box-shadow: 0 8px 18px -10px rgba(103, 71, 189, 0.5);
}
.pg-title {
    color: var(--ink);
    font-size: clamp(22px, 3vw, 30px);
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.25;
}
.pg-sub { color: var(--ink-soft); font-size: 14px; margin-top: 4px; }
.pg-orb {
    margin-left: auto;
    flex: 0 0 84px;
    height: 84px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 26%, #fff 0%, #E6DCFB 30%, #A78BF0 78%, #8466DB 100%);
    box-shadow: 0 18px 34px -14px rgba(103, 71, 189, 0.6), inset 0 -8px 18px rgba(103, 71, 189, 0.3);
}
@media (max-width: 760px) {
    .pg-banner { padding: 18px 20px; }
    .pg-orb { display: none; }
}

/* ---------- Khung thông báo đồng bộ tông tím ---------- */
.stApp [data-testid="stAlert"], .stApp [data-testid="stAlert"] > div { border-radius: 18px; }
.stApp [data-testid="stAlert"] { border: 1px solid var(--line); background: #F1EBFF; }
.stApp [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]) { background: #E8F6EF; }
.stApp [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) { background: #FFF3E6; }
.stApp [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) { background: #FDECF1; }
.stApp [data-testid="stAlert"] p { color: var(--ink); }

.stApp [data-testid="stForm"] {
    background: var(--glass);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 22px;
    box-shadow: var(--shadow);
}
</style>
"""


def apply_layout():
    """Gọi ngay sau apply_theme()."""
    st.markdown(CSS, unsafe_allow_html=True)


def page_banner(title, icon="💜", subtitle=""):
    """Banner đầu trang, thay cho st.title()."""
    sub = f'<div class="pg-sub">{subtitle}</div>' if subtitle else ""
    st.html(
        f'<div class="pg-banner"><div class="pg-icon">{icon}</div>'
        f'<div><div class="pg-title">{title}</div>{sub}</div>'
        f'<div class="pg-orb"></div></div>'
    )
'''

ICONS = {
    "Phân tích cảm xúc qua văn bản": "💬",
    "Phân tích giọng nói và cảm xúc": "🎙️",
    "Hồ sơ giọng nói cá nhân": "👤",
    "Báo cáo và theo dõi cảm xúc": "📊",
    "Chăm sóc và phục hồi cảm xúc": "🌱",
    "SerenWize Breathing Studio": "🌬️",
    "Giới thiệu SerenWize-AI": "💜",
}

os.makedirs("modules", exist_ok=True)
open(os.path.join("modules", "layout.py"), "w", encoding="utf-8", newline="\n").write(LAYOUT)

shutil.copy("app.py", "app_truoc_khi_vá_v2.py")
s = open("app.py", encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"

if "from modules.layout import" not in s:
    s = s.replace("from modules.theme import apply_theme, sidebar_brand",
                  "from modules.theme import apply_theme, sidebar_brand" + nl +
                  "from modules.layout import apply_layout, page_banner", 1)
if "apply_layout()" not in s:
    s = s.replace("apply_theme()", "apply_theme()" + nl + "apply_layout()", 1)

def banner(m):
    title = m.group(2)
    return m.group(1) + 'page_banner("%s", "%s")' % (title, ICONS.get(title, "💜"))

s, n = re.subn(r'([ \t]*)st\.title\("([^"]+)"\)', banner, s)
open("app.py", "w", encoding="utf-8", newline="").write(s)
print("Xong! Đã đổi", n, "tiêu đề trang. Chạy: streamlit run app.py")
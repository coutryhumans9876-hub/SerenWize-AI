"""
SerenWize-AI - Trang chủ dạng dashboard (lavender / tím pastel)
Đặt file này vào modules/home.py
"""
from html import escape
import streamlit as st
from modules.theme import icon_img

CSS = """
<style>
.hm-hero {
    position: relative;
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    align-items: center;
    gap: 16px;
    min-height: 380px;
    padding: 44px 48px;
    margin-bottom: 28px;
    background: linear-gradient(125deg, #EADFFF 0%, #F3E8FB 48%, #DDE6FF 100%);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 36px;
    box-shadow: var(--shadow);
    overflow: hidden;
}
.hm-hello { color: var(--ink-soft); font-size: 20px; font-weight: 400; margin-bottom: 8px; }
.hm-title {
    color: var(--ink-soft);
    font-size: clamp(30px, 4.4vw, 48px);
    font-weight: 300;
    line-height: 1.2;
    letter-spacing: -0.02em;
}
.hm-title b { color: var(--ink); font-weight: 700; }
.hm-desc { color: var(--ink-soft); font-size: 15px; line-height: 1.8; max-width: 480px; margin-top: 18px; }

.hm-orb-wrap { position: relative; height: 300px; display: flex; align-items: center; justify-content: center; }
.hm-orb {
    width: 220px; height: 220px; border-radius: 50%;
    background: radial-gradient(circle at 30% 26%, #fff 0%, #E6DCFB 30%, #A78BF0 78%, #8466DB 100%);
    box-shadow: 0 36px 70px -24px rgba(103, 71, 189, 0.6), inset 0 -14px 34px rgba(103, 71, 189, 0.3);
    animation: hm-breathe 8s ease-in-out infinite;
}
@keyframes hm-breathe { 0%, 100% { transform: scale(0.92); } 50% { transform: scale(1.05); } }

.hm-chip {
    position: absolute;
    min-width: 150px;
    padding: 14px 18px;
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(12px);
    border: 1px solid var(--line);
    border-radius: 20px;
    box-shadow: var(--shadow);
}
.hm-chip span { display: block; color: var(--ink-mute); font-size: 12.5px; }
.hm-chip b { display: block; color: var(--ink); font-size: 18px; font-weight: 700; margin-top: 4px; }
.hm-chip-a { top: 6%; left: -2%; }
.hm-chip-b { bottom: 4%; right: -2%; }

.hm-card {
    background: var(--glass);
    border: 1px solid var(--line);
    border-radius: 24px;
    padding: 22px;
    box-shadow: var(--shadow);
    min-height: 168px;
}
.hm-icon {
    width: 46px; height: 46px; margin-bottom: 14px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 15px; font-size: 22px;
    background: linear-gradient(135deg, var(--lav-200), var(--rose));
}
.hm-card-title { color: var(--ink); font-size: 16.5px; font-weight: 700; margin-bottom: 6px; }
.hm-card-desc { color: var(--ink-soft); font-size: 13.5px; line-height: 1.7; }

.hm-panel-title { color: var(--ink); font-size: 20px; font-weight: 700; letter-spacing: -0.02em; margin: 6px 0 4px; }
.hm-panel-sub { color: var(--ink-mute); font-size: 13.5px; margin-bottom: 16px; }
.hm-bar { position: relative; height: 56px; margin-bottom: 12px; background: var(--lav-100); border-radius: 18px; overflow: hidden; }
.hm-bar-fill { position: absolute; inset: 0 auto 0 0; background: linear-gradient(90deg, var(--lav-200), var(--lav-300)); }
.hm-bar-label { position: relative; padding: 0 20px; line-height: 56px; color: var(--ink); font-weight: 500; }
.hm-bar-val {
    position: absolute; top: 8px; right: 8px; bottom: 8px;
    padding: 0 16px; line-height: 40px;
    background: #fff; border-radius: 12px;
    color: var(--ink-soft); font-size: 13px; font-weight: 600;
}
.hm-bar-val.done { background: var(--lav-600); color: #fff; }

@media (max-width: 760px) {
    .hm-hero { grid-template-columns: 1fr; padding: 30px 22px; }
    .hm-orb-wrap { height: 260px; }
    .hm-chip-a { left: 0; }
    .hm-chip-b { right: 0; }
}
@media (prefers-reduced-motion: reduce) { .hm-orb { animation: none; } }

.hm-brand { font-size: clamp(38px, 5vw, 58px); font-weight: 800; letter-spacing: -0.03em; line-height: 1.1;
    background: linear-gradient(90deg, #6747BD, #A78BF0); -webkit-background-clip: text; background-clip: text; color: transparent; }
.hm-tag { color: var(--lav-700); font-size: clamp(18px, 2.2vw, 24px); font-weight: 700; line-height: 1.4; margin: 10px 0 12px; }
.hm-art { width: 270px; max-width: 100%; animation: hm-breathe 8s ease-in-out infinite; filter: drop-shadow(0 26px 30px rgba(103,71,189,0.28)); }
.hm-icon { background: var(--lav-100); }
.hm-icon svg { width: 24px; height: 24px; stroke: var(--lav-700); fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.hm-quote { text-align: center; color: var(--lav-700); font-style: italic; font-size: 14px; margin: 18px 0 6px; }
</style>
"""

FEATURES = [
    ("mic", "Phân tích giọng nói", "Ước lượng tín hiệu cảm xúc từ giọng nói.", "Phân tích giọng nói"),
    ("text", "Phân tích văn bản", "Khám phá cảm xúc qua nội dung bạn chia sẻ.", "Phân tích văn bản"),
    ("heart", "Gợi ý chăm sóc", "Hoạt động nhẹ nhàng phù hợp tâm trạng.", "Gợi ý chăm sóc"),
    ("chart", "Theo dõi tâm lý", "Xem lại kết quả và những thay đổi cảm xúc.", "Báo cáo tâm lý"),
]

_ART_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240">'
    '<defs><linearGradient id="hg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#CDBBFB"/>'
    '<stop offset="1" stop-color="#7F60D8"/></linearGradient>'
    '<radialGradient id="gl"><stop offset="0" stop-color="#fff" stop-opacity=".95"/>'
    '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>'
    '<circle cx="120" cy="124" r="112" fill="url(#gl)"/>'
    '<path d="M120 200C38 142 34 86 74 72c24-8 40 6 46 20 6-14 22-28 46-20 40 14 36 70-46 128z" fill="url(#hg)"/>'
    '<path d="M60 122C60 50 180 50 180 122" fill="none" stroke="#5B3FB0" stroke-width="9" stroke-linecap="round"/>'
    '<rect x="48" y="110" width="26" height="46" rx="13" fill="#7F60D8"/>'
    '<rect x="166" y="110" width="26" height="46" rx="13" fill="#7F60D8"/>'
    '<path d="M186 40l3 8 8 3-8 3-3 8-3-8-8-3 8-3z" fill="#C9B6FA"/>'
    '<path d="M44 58l2 5 5 2-5 2-2 5-2-5-5-2 5-2z" fill="#C9B6FA"/></svg>'
)


from urllib.parse import quote as _q

ART = '<img class="hm-art" alt="" src="data:image/svg+xml,' + _q(_ART_SVG, safe="/=:.,'-") + '">'


def _go(page):
    st.session_state["menu"] = page


def _text_emotion():
    r = st.session_state.get("text_result")
    if isinstance(r, dict) and r.get("emotion"):
        return escape(str(r["emotion"]))
    return "Chưa có"


def _voice_emotion():
    r = st.session_state.get("voice_emotion_result")
    if isinstance(r, dict) and r.get("success") and r.get("overall_emotion"):
        return escape(str(r["overall_emotion"]))
    return "Chưa có"


def _bar(label, done):
    width = "100%" if done else "0%"
    val = "Đã xong" if done else "Chưa làm"
    cls = "hm-bar-val done" if done else "hm-bar-val"
    return (
        f'<div class="hm-bar"><div class="hm-bar-fill" style="width:{width}"></div>'
        f'<div class="hm-bar-label">{label}</div><div class="{cls}">{val}</div></div>'
    )


def home_dashboard():
    st.markdown(CSS, unsafe_allow_html=True)

    st.html(
        '<div class="hm-hero">'
        '<div>'
        '<div class="hm-brand">SerenWize-AI</div>'
        '<div class="hm-tag">Lắng nghe cảm xúc – Thấu hiểu tâm lý – Đồng hành cùng bạn</div>'
        '<div class="hm-desc">Nền tảng hỗ trợ sức khỏe tinh thần cho học sinh thông qua phân tích giọng nói '
        'và văn bản, giúp bạn hiểu rõ cảm xúc, giảm căng thẳng và tìm lại sự cân bằng.</div>'
        '</div>'
        f'<div class="hm-orb-wrap">{ART}'
        f'<div class="hm-chip hm-chip-a"><span>Từ văn bản</span><b>{_text_emotion()}</b></div>'
        f'<div class="hm-chip hm-chip-b"><span>Từ giọng nói</span><b>{_voice_emotion()}</b></div>'
        '</div></div>'
    )
    st.button("Bắt đầu ngay  →", key="home_start", on_click=_go, args=("Phân tích văn bản",))

    cols = st.columns(4, gap="medium")
    for col, (icon, title, desc, page) in zip(cols, FEATURES):
        with col:
            st.html(
                f'<div class="hm-card"><div class="hm-icon">{icon_img(icon, "#6747BD", 24)}</div>'
                f'<div class="hm-card-title">{title}</div>'
                f'<div class="hm-card-desc">{desc}</div></div>'
            )
            st.button("Mở", key=f"home_open_{page}", on_click=_go, args=(page,), use_container_width=True)

    st.write("")
    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        st.html(
            '<div class="hm-panel-title">Tiến độ trong phiên này</div>'
            '<div class="hm-panel-sub">Các bước bạn đã hoàn thành kể từ khi mở ứng dụng.</div>'
            + _bar("Phân tích văn bản", st.session_state.get("text_result") is not None)
            + _bar("Phân tích giọng nói", st.session_state.get("voice_emotion_result") is not None
                   or st.session_state.get("voice_result") is not None)
            + _bar("Tổng hợp cảm xúc", st.session_state.get("combined_result") is not None)
        )
    with right:
        st.html(
            '<div class="hm-panel-title">Lưu ý</div>'
            '<div class="hm-panel-sub">Hiểu đúng vai trò của công cụ này.</div>'
            '<div class="sw-notice">SerenWize-AI là công cụ hỗ trợ tự khám phá cảm xúc, '
            'không thay thế đánh giá chuyên môn, chẩn đoán hoặc điều trị tâm lý. '
            'Nếu bạn đang thấy quá tải, hãy trò chuyện với người bạn tin tưởng '
            'hoặc chuyên gia tâm lý.</div>'
        )
    st.html('<div class="hm-quote">“Understand Emotions. Empower Minds.”</div>')
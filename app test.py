
import streamlit as st
import pandas as pd
from modules.text_analysis import analyze_text

# Cấu hình website
st.set_page_config(
    page_title="SerenWize-AI" ,
    page_icon="💙",
    layout="wide"
)

# Tiêu đề
st.title("💙 SerenWize-AI")
st.subheader("Hệ thống hỗ trợ phân tích cảm xúc và tâm lý học sinh")

st.markdown("""
Chào mừng bạn đến với SerenWize-AI!

Đây là hệ thống hỗ trợ học sinh tự tìm hiểu trạng thái cảm xúc
thông qua nội dung văn bản và giọng nói.

**Lưu ý:** Kết quả chỉ mang tính tham khảo, không thay thế
đánh giá hoặc chẩn đoán của chuyên gia tâm lý.
""")

st.divider()

# Thanh bên
st.sidebar.title("SerenWize-AI")
st.sidebar.write("Hệ thống phân tích cảm xúc")

menu = st.sidebar.radio(
    "Chọn chức năng",
    [
        "Trang chủ",
        "Phân tích văn bản",
        "Phân tích giọng nói",
        "Giới thiệu dự án"
    ]
)

if menu == "Trang chủ":
    st.header("Chào mừng bạn!")
    st.write("Hãy chọn một chức năng ở thanh bên để bắt đầu.")

elif menu == "Phân tích văn bản":
    st.header("Phân tích cảm xúc qua văn bản")

    content = st.text_area(
        "Hãy chia sẻ cảm xúc hoặc suy nghĩ của bạn:",
        height=180,
        placeholder="Ví dụ: Hôm nay mình cảm thấy khá áp lực..."
    )

    if st.button("Gửi nội dung"):
        if content.strip():
            st.info("Đã tiếp nhận nội dung. Chức năng phân tích AI sẽ được tích hợp ở bước tiếp theo.")
        else:
            st.warning("Bạn hãy nhập nội dung trước nhé!")

elif menu == "Phân tích giọng nói":
    st.header("Phân tích cảm xúc qua giọng nói")

    audio = st.file_uploader(
        "Tải tệp ghi âm lên",
        type=["wav", "mp3", "ogg", "flac"]
    )

    if audio is not None:
        st.audio(audio)
        st.success("Đã tiếp nhận tệp âm thanh.")

        st.info("Bộ phân tích giọng nói sẽ được tích hợp ở bước tiếp theo.")

elif menu == "Giới thiệu dự án":
    st.header("Giới thiệu SerenWize-AI")
    st.write("""
    SerenWize-AI hướng tới xây dựng một hệ thống hỗ trợ học sinh
    nhận diện và tìm hiểu cảm xúc của bản thân.

    Hệ thống dự kiến kết hợp:
    - Phân tích nội dung văn bản tiếng Việt.
    - Trích xuất đặc trưng từ giọng nói.
    - Tổng hợp thông tin cảm xúc.
    - Đưa ra gợi ý chăm sóc sức khỏe tinh thần.
    """)

import streamlit as st
import pandas as pd

# ==========================================
# 1. CAU HINH WEBSITE
# ==========================================

st.set_page_config(
    page_title="SerenWize-AI",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CSS - THIET KE GIAO DIEN
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #FAF9FF 0%,
        #F3F0FF 55%,
        #F8F9FF 100%
    );
    color: #292344;
}

[data-testid="stHeader"] {
    background: rgba(250,249,255,0.8);
}

[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #F0ECFF,
        #F8F7FF
    );
    border-right: 1px solid #E5DFFF;
}

[data-testid="stSidebar"] * {
    color: #403365;
}

h1, h2, h3 {
    color: #30264F !important;
    font-weight: 700 !important;
}

p {
    color: #665D82;
}

.hero {
    background: linear-gradient(
        115deg,
        #E7DEFF,
        #F4F0FF 55%,
        #E7F0FF
    );
    border: 1px solid #E3D9FF;
    border-radius: 24px;
    padding: 35px;
    margin-bottom: 25px;
    box-shadow: 0 8px 28px rgba(115, 87, 180, 0.09);
}

.hero h1 {
    color: #49347F !important;
    font-size: 35px;
}

.hero p {
    color: #695B8C;
    font-size: 16px;
}

.heart {
    font-size: 76px;
    text-align: center;
    color: #8D6BE0;
    padding: 10px;
    text-shadow: 0 8px 20px rgba(141,107,224,0.2);
}

.section-title {
    color: #44336D;
    font-size: 22px;
    font-weight: 700;
    margin: 18px 0;
}

.feature-card {
    background: rgba(255,255,255,0.85);
    border: 1px solid #E9E3FA;
    border-radius: 19px;
    padding: 22px;
    min-height: 175px;
    box-shadow: 0 5px 18px rgba(100,80,150,0.06);
    margin-bottom: 10px;
}

.feature-icon {
    font-size: 29px;
    margin-bottom: 12px;
}

.feature-card h3 {
    font-size: 17px;
    margin: 5px 0;
}

.feature-card p {
    font-size: 13px;
    line-height: 1.7;
}

.info-card {
    background: #FFFFFF;
    border: 1px solid #EAE5F8;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 5px 18px rgba(100,80,150,0.05);
    margin-bottom: 12px;
}

.stButton > button {
    background: linear-gradient(
        110deg,
        #9576E8,
        #7655CF
    );
    color: white;
    border: none;
    border-radius: 13px;
    padding: 10px 22px;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #6848BE;
    color: white;
    border: none;
    transform: translateY(-2px);
}

input, textarea {
    border-radius: 12px !important;
}

.footer {
    text-align: center;
    color: #8B80A8;
    font-size: 12px;
    padding: 25px 0 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. THANH DIEU HUONG
# ==========================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:20px 0;">
            <div style="font-size:48px; color:#8D6BE0;">
                ♡
            </div>
            <h2 style="color:#55418D !important;">
                SerenWize-AI
            </h2>
            <p style="font-size:12px;">
                Understand Emotions.<br>
                Empower Minds.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    menu = st.radio(
        "MENU",
        [
            "Trang chủ",
            "Phân tích văn bản",
            "Phân tích giọng nói",
            "Báo cáo tâm lý",
            "Gợi ý chăm sóc",
            "Giới thiệu dự án"
        ],
        index=0
    )

    st.divider()

    st.caption("SERENWIZE-AI")
    st.caption("Phiên bản thử nghiệm 1.0")


# ==========================================
# 4. TRANG CHU
# ==========================================

if menu == "Trang chủ":

    st.markdown("""
    <div class="hero">
        <div class="heart">♡</div>
        <h1>Xin chào! Chào mừng bạn đến với SerenWize-AI</h1>
        <p>
            Một người bạn đồng hành giúp bạn lắng nghe,
            khám phá và thấu hiểu thế giới cảm xúc của chính mình.
        </p>
        <p><b>Understand Emotions. Empower Minds.</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Khám phá các chức năng</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>Phân tích văn bản</h3>
            <p>
                Khám phá cảm xúc thông qua những
                dòng suy nghĩ và chia sẻ của bạn.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3>Báo cáo tâm lý</h3>
            <p>
                Xem lại kết quả và theo dõi
                những thay đổi cảm xúc.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎙️</div>
            <h3>Phân tích giọng nói</h3>
            <p>
                Khám phá các đặc trưng âm thanh
                từ giọng nói của bạn.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💜</div>
            <h3>Gợi ý chăm sóc</h3>
            <p>
                Tìm hiểu những phương pháp
                chăm sóc sức khỏe tinh thần.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Tổng quan hệ thống</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Dữ liệu phân tích", "Chưa có")
    c2.metric("Trạng thái hệ thống", "Đang thử nghiệm")
    c3.metric("Mô hình AI", "Đang phát triển")

    st.info(
        "SerenWize-AI hiện đang trong giai đoạn xây dựng. "
        "Các kết quả phân tích sẽ xuất hiện sau khi tích hợp mô hình AI."
    )


# ==========================================
# 5. PHAN TICH VAN BAN
# ==========================================

elif menu == "Phân tích văn bản":

    st.title("Phân tích cảm xúc qua văn bản")

    st.write(
        "Hãy chia sẻ suy nghĩ hoặc cảm xúc của bạn "
        "trong khoảng thời gian gần đây."
    )

    content = st.text_area(
        "Nội dung chia sẻ",
        height=200,
        placeholder="Hôm nay mình cảm thấy..."
    )

    if st.button("Tiếp nhận nội dung"):

        if content.strip():

            st.success(
                "Đã tiếp nhận nội dung thành công!"
            )

            st.info(
                "Bộ phân tích cảm xúc đang được phát triển. "
                "Hiện tại hệ thống chưa đưa ra kết luận cảm xúc."
            )

        else:
            st.warning("Bạn hãy nhập nội dung trước nhé!")


# ==========================================
# 6. PHAN TICH GIONG NOI
# ==========================================

elif menu == "Phân tích giọng nói":

    st.title("Phân tích cảm xúc qua giọng nói")

    st.write(
        "Tải lên một tệp ghi âm tiếng Việt "
        "để chuẩn bị phân tích đặc trưng âm thanh."
    )

    audio = st.file_uploader(
        "Chọn tệp âm thanh",
        type=["wav", "mp3", "ogg", "flac"]
    )

    if audio is not None:

        st.audio(audio)

        st.success("Đã tiếp nhận tệp ghi âm.")

        st.info(
            "Chức năng trích xuất đặc trưng và phân tích "
            "giọng nói sẽ được kết nối ở giai đoạn tiếp theo."
        )


# ==========================================
# 7. BAO CAO TAM LY
# ==========================================

elif menu == "Báo cáo tâm lý":

    st.title("Báo cáo và theo dõi cảm xúc")

    st.write(
        "Khu vực tổng hợp dữ liệu phân tích "
        "và theo dõi cảm xúc theo thời gian."
    )

    st.info(
        "Chưa có dữ liệu báo cáo. "
        "Hãy sử dụng các chức năng phân tích sau khi được tích hợp."
    )


# ==========================================
# 8. GOI Y CHAM SOC
# ==========================================

elif menu == "Gợi ý chăm sóc":

    st.title("Gợi ý chăm sóc sức khỏe tinh thần")

    suggestions = [
        ("🌿", "Nghỉ ngơi", "Dành thời gian thư giãn và ngủ đủ giấc."),
        ("🎵", "Âm nhạc", "Nghe những bản nhạc bạn yêu thích."),
        ("🌸", "Chia sẻ", "Trò chuyện với người mà bạn tin tưởng."),
        ("☀️", "Vận động", "Đi bộ hoặc vận động nhẹ nhàng."),
        ("💜", "Quan tâm bản thân", "Hãy cho phép bản thân được nghỉ ngơi.")
    ]

    for icon, title, description in suggestions:

        st.markdown(
            f"""
            <div class="info-card">
                <h3>{icon} {title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==========================================
# 9. GIOI THIEU DU AN
# ==========================================

elif menu == "Giới thiệu dự án":

    st.title("Giới thiệu SerenWize-AI")

    st.write("""
    **SerenWize-AI** là dự án hướng tới xây dựng
    một hệ thống hỗ trợ học sinh tìm hiểu và
    chăm sóc sức khỏe tinh thần.

    Hệ thống dự kiến kết hợp:

    - Phân tích nội dung văn bản tiếng Việt.
    - Trích xuất đặc trưng từ giọng nói.
    - Tổng hợp thông tin cảm xúc.
    - Trực quan hóa dữ liệu.
    - Đưa ra gợi ý chăm sóc tinh thần.
    """)

    st.warning(
        "SerenWize-AI không thay thế chuyên gia tâm lý "
        "và không đưa ra chẩn đoán bệnh lý."
    )


# ==========================================
# 10. CHAN TRANG
# ==========================================

st.markdown("""
<div class="footer">
    ♡ SerenWize-AI |
    Understand Emotions. Empower Minds.
    <br><br>
    Lắng nghe cảm xúc – Thấu hiểu tâm lý – Đồng hành cùng bạn
</div>
""", unsafe_allow_html=True)


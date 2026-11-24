import streamlit as st
import pandas as pd
import os
import tempfile
import subprocess

from modules.text_analysis import analyze_text
from modules.voice_analysis import analyze_audio
from modules.emotion_analysis import combine_analysis
from modules.emotion_fusion import fuse
from modules.voice_emotion import analyze_voice_emotion
from modules.voice_baseline import create_baseline, load_baseline
from modules.voice_comparison import compare_voice
from modules.theme import (
    apply_theme, sidebar_brand, page_header, sidebar_footer,
    emotion_pill, chips, tip_box, empty_state,
)
from modules.home import home_dashboard
from modules.practice import breathing_studio, recommend_exercise, practice_cta
from modules.recovery_history import (
    save_recovery_session,
    load_recovery_history
)
# ==========================================
# 1. CAU HINH WEBSITE
# ==========================================

st.set_page_config(
    page_title="SerenWize-AI",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Lưu kết quả phân tích trong phiên làm việc
if "text_result" not in st.session_state:
    st.session_state.text_result = None

if "voice_result" not in st.session_state:
    st.session_state.voice_result = None

if "combined_result" not in st.session_state:
    st.session_state.combined_result = None

if "voice_emotion_result" not in st.session_state:
    st.session_state.voice_emotion_result = None
if "recovery_started" not in st.session_state:
    st.session_state.recovery_started = False

if "recovery_session" not in st.session_state:
    st.session_state.recovery_session = None


# ==========================================
# 2. CSS - THIET KE GIAO DIEN
# ==========================================



apply_theme()


# ==========================================
# 3. THANH DIEU HUONG
# ==========================================

    
with st.sidebar:
    sidebar_brand()
    menu = st.radio(
        "Menu",
        [
            "Trang chủ",
            "Phân tích văn bản",
            "Phân tích giọng nói",
            "Hồ sơ giọng nói cá nhân",
            "Báo cáo tâm lý",
            "Gợi ý chăm sóc",
            "Phòng luyện tập",
            "Giới thiệu dự án"
        ],
        key="menu"
    )
    sidebar_footer("Phiên bản thử nghiệm 1.0")


# ==========================================
# 4. TRANG CHU
# ==========================================



if menu == "Trang chủ":

    page_header("home", "Trang chủ")
    home_dashboard()



# ==========================================
# 5. PHAN TICH VAN BAN
# ==========================================


elif menu == "Phân tích văn bản":

    page_header("text", "Phân tích văn bản")

    left, right = st.columns([1.05, 0.95], gap="large")

    with left:
        with st.container(key="card_text_input"):
            st.markdown("#### 📝 Nhập nội dung cần phân tích")
            st.caption("Hãy chia sẻ suy nghĩ hoặc cảm xúc của bạn trong khoảng thời gian gần đây.")
            content = st.text_area(
                "Nội dung chia sẻ",
                height=220,
                max_chars=1000,
                placeholder="Ví dụ: Tôi đang rất lo lắng vì bài kiểm tra sắp tới...",
                label_visibility="collapsed",
            )
            run = st.button("Phân tích văn bản", use_container_width=True, key="btn_text_run")

    empty_warn = False
    if run:
        if content.strip():
            result = analyze_text(content)
            st.session_state.text_result = result
            st.session_state.combined_result = combine_analysis(
                st.session_state.text_result,
                st.session_state.voice_result
            )
        else:
            empty_warn = True

    with right:
        with st.container(key="card_text_result"):
            st.markdown("#### Kết quả phân tích")
            result = st.session_state.text_result
            if empty_warn:
                st.warning("Bạn hãy nhập nội dung trước nhé!")
            elif result:
                emotion_pill(result["emotion"])

                if result["emotions"]:
                    st.markdown("**Các cảm xúc được nhận diện**")
                    chips(result["emotions"])

                if result["keywords"]:
                    st.markdown("**Từ khóa nổi bật**")
                    chips(result["keywords"])

                if result["negated_keywords"]:
                    st.markdown("**Từ khóa trong ngữ cảnh phủ định**")
                    chips(result["negated_keywords"], "muted")

                tip_box("Gợi ý cho bạn", result["suggestion"])
                practice_cta(result["emotion"], "cta_text_practice")
                st.caption(result["message"])
                st.caption(
                    "Kết quả dựa trên bộ từ khóa thử nghiệm, "
                    "không phải chẩn đoán tâm lý."
                )
            else:
                empty_state("Nhập nội dung ở bên trái rồi bấm “Phân tích văn bản” để xem kết quả.")


# ==========================================
# 6. PHAN TICH GIONG NOI
# ==========================================





    

elif menu == "Phân tích giọng nói":

    page_header("mic", "Phân tích giọng nói")

    st.write(
        "Tải lên một tệp ghi âm tiếng Việt để SerenWize-AI "
        "trích xuất đặc trưng âm thanh và nhận diện cảm xúc "
        "thông qua mô hình MERaLiON."
    )

    audio = st.file_uploader(
        "Chọn tệp âm thanh",
        type=["wav", "mp3", "ogg", "flac", "m4a"]
    )

    if audio is not None:

        st.audio(audio)
        st.success("Đã tiếp nhận tệp ghi âm.")

        transcript = st.text_area(
            "Nội dung lời nói (tùy chọn)",
            height=110,
            placeholder="Gõ lại nội dung bạn nói trong bản ghi để đối chiếu giữa lời nói và giọng điệu...",
            help="Nếu nhập, SerenWize-AI sẽ so sánh cảm xúc trong nội dung với cảm xúc trong giọng nói.",
        )

        if st.button("Bắt đầu phân tích giọng nói"):

            temp_path = None
            temp_wav_path = None

            try:
                # Lưu tệp âm thanh gốc
                suffix = os.path.splitext(audio.name)[1]

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=suffix
                ) as temp_file:
                    temp_file.write(audio.getvalue())
                    temp_path = temp_file.name

                # Tạo tệp WAV tạm
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".wav"
                ) as wav_file:
                    temp_wav_path = wav_file.name

                # Chuyển đổi âm thanh sang WAV
                with st.spinner("Đang chuyển đổi âm thanh..."):

                    subprocess.run(
                        [
                            "ffmpeg",
                            "-y",
                            "-i", temp_path,
                            "-ac", "1",
                            "-ar", "22050",
                            temp_wav_path
                        ],
                        capture_output=True,
                        text=True,
                        check=True
                    )

                # Phân tích đặc trưng âm thanh
                with st.spinner("Đang trích xuất đặc trưng giọng nói..."):

                    voice_result = analyze_audio(temp_wav_path)

                st.session_state.voice_result = voice_result
                comparison_result = None

                # Gửi âm thanh đến MERaLiON
                with st.spinner("MERaLiON đang nhận diện cảm xúc..."):

                    emotion_result = analyze_voice_emotion(
                        temp_wav_path
                    )

                st.session_state.voice_emotion_result = emotion_result

                # Tổng hợp kết quả văn bản và đặc trưng âm thanh
                st.session_state.combined_result = combine_analysis(
                    st.session_state.text_result,
                    voice_result
                )

                # Hiển thị đặc trưng âm thanh
                if voice_result.get("success"):

                    st.success(
                        "Trích xuất đặc trưng âm thanh thành công!"
                    )

                    st.subheader("1. Đặc trưng âm thanh")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Thời lượng",
                            f"{voice_result['duration']} giây"
                        )

                        st.metric(
                            "Cao độ trung bình",
                            f"{voice_result['pitch_mean']} Hz"
                        )

                        st.metric(
                            "Năng lượng RMS",
                            voice_result["rms_mean"]
                        )

                    with col2:
                        st.metric(
                            "Zero Crossing Rate",
                            voice_result["zcr_mean"]
                        )

                        st.metric(
                            "Spectral Centroid",
                            f"{voice_result['centroid_mean']} Hz"
                        )

                    st.subheader("13 hệ số MFCC")

                    mfcc_data = pd.DataFrame({
                        "Hệ số": [
                            f"MFCC {i + 1}"
                            for i in range(
                                len(voice_result["mfcc_mean"])
                            )
                        ],
                        "Giá trị": voice_result["mfcc_mean"]
                    })

                    st.bar_chart(
                        mfcc_data,
                        x="Hệ số",
                        y="Giá trị"
                    )

                    # So sánh với hồ sơ giọng nói cá nhân
                    st.divider()
                    st.subheader("2. So sánh với hồ sơ giọng nói cá nhân")

                    baseline = load_baseline()

                    if baseline is None:
                        st.info(
                            "Chưa có hồ sơ giọng nói cá nhân. "
                            "Hãy tạo hồ sơ trước khi thực hiện so sánh."
                        )

                    else:
                        comparison_result = compare_voice(
                            voice_result,
                            baseline
                        )

                        if comparison_result.get("success"):

                            st.success(
                                "Đã so sánh với hồ sơ giọng nói thành công!"
                            )

                            comparison_rows = []

                            for item in comparison_result[
                                "comparisons"
                            ].values():

                                percent = item["percent_change"]

                                comparison_rows.append({
                                    "Đặc trưng": item["label"],
                                    "Giọng nói bình thường": round(
                                        item["baseline"], 4
                                    ),
                                    "Giọng nói hiện tại": round(
                                        item["current"], 4
                                    ),
                                    "Thay đổi": round(
                                        item["difference"], 4
                                    ),
                                    "Thay đổi (%)": (
                                        "Không xác định"
                                        if percent is None
                                        else f"{percent:+.2f}%"
                                    )
                                })

                            st.dataframe(
                                pd.DataFrame(comparison_rows),
                                use_container_width=True,
                                hide_index=True
                            )

                            mfcc_difference = comparison_result.get(
                                "mfcc_mean_absolute_difference"
                            )

                            if mfcc_difference is not None:
                                st.metric(
                                    "Sai khác trung bình MFCC",
                                    f"{mfcc_difference:.4f}"
                                )

                            st.info(
                                "Kết quả thể hiện sự thay đổi đặc trưng "
                                "âm thanh so với hồ sơ cá nhân, không "
                                "tự động xác định cảm xúc hoặc mức độ "
                                "căng thẳng."
                            )

                        else:
                            st.warning(
                                "Không thể so sánh giọng nói."
                            )
                            st.code(
                                comparison_result.get(
                                    "error",
                                    "Không có thông tin lỗi."
                                )
                            )


                else:
                    st.error("Không thể trích xuất đặc trưng âm thanh.")
                    st.code(
                        voice_result.get(
                            "error",
                            voice_result.get(
                                "message",
                                "Không có thông tin lỗi."
                            )
                        )
                    )

                # Hiển thị kết quả nhận diện cảm xúc
                st.divider()
                st.subheader("3. Nhận diện cảm xúc bằng MERaLiON")
                emotion_translation = {
    "Neutral": "Bình thường",
    "Happy": "Vui vẻ",
    "Sad": "Buồn bã",
    "Angry": "Tức giận",
    "Surprised": "Ngạc nhiên",
    "Fearful": "Sợ hãi",
    "Disgusted": "Ghê sợ",
    "Uncertain": "Chưa xác định"
}

                if emotion_result.get("success"):

                    st.success("MERaLiON đã phân tích âm thanh thành công!")

                    overall_emotion = emotion_result.get(
                        "overall_emotion",
                        "Chưa xác định"
                    )

                    overall_confidence = emotion_result.get(
                        "overall_confidence"
                    )

                    translated_overall = emotion_translation.get(
                        overall_emotion,
                        overall_emotion
                    )

                    st.markdown(
                        f"### Cảm xúc tổng thể: {translated_overall}"
                    )

                    if overall_confidence is not None:
                        st.metric(
                            "Độ tin cậy tổng thể",
                            f"{overall_confidence * 100:.2f}%"
                        )

                    st.write("**Kết quả theo từng đoạn âm thanh:**")

                    segments = emotion_result.get("segments", [])
                    

                    if segments:

                        segment_data = []

                        for segment in segments:

                            confidence = segment.get("confidence", 0)

                            
                            segment_data.append({
                                "Thời gian": (
                                    f"{segment.get('start_time', 0):.1f}"
                                    f"–{segment.get('end_time', 0):.1f}s"
                                ),
                                "Cảm xúc": segment.get(
                                    "emotion",
                                    "Chưa xác định"
                                ),
                                "Độ tin cậy": (
                                    f"{confidence * 100:.2f}%"
                                )
                            })

                        st.dataframe(
                            pd.DataFrame(segment_data),
                            use_container_width=True,
                            hide_index=True
                        )

                    st.info(
                        "Đây là dự đoán cảm xúc từ mô hình AI, "
                        "không phải chẩn đoán tâm lý hoặc kết luận "
                        "về mức độ căng thẳng."
                    )

                    # ---- 4. Đối chiếu giọng điệu + nội dung + giọng gốc ----
                    st.divider()
                    st.subheader("4. Ước lượng tổng hợp")
                    transcript_result = analyze_text(transcript) if transcript.strip() else None
                    fusion = fuse(emotion_result, transcript_result, comparison_result)

                    if fusion.get("success"):
                        st.session_state.fusion_result = fusion
                        emotion_pill(fusion["emotion"])
                        st.markdown(
                            f"**Mức chắc chắn:** {fusion['confidence_level']}  ·  "
                            f"**Nguồn đã dùng:** {', '.join(fusion['sources'])}"
                        )
                        st.bar_chart(
                            pd.DataFrame({"Điểm": fusion["scores"]})
                        )
                        for line in fusion["explanations"]:
                            st.markdown(f"- {line}")
                        if not transcript.strip():
                            st.caption("Gợi ý: nhập nội dung lời nói ở phía trên để đối chiếu thêm với nội dung.")
                        if comparison_result is None or not comparison_result.get("success"):
                            st.caption("Gợi ý: tạo hồ sơ giọng nói cá nhân để so sánh với giọng bình thường của bạn.")
                        tip_box("Lưu ý", fusion["limitation"], icon="💡")
                        practice_cta(fusion["emotion"], "cta_voice_practice")
                    else:
                        st.info(fusion.get("error", "Chưa đủ dữ liệu để ước lượng tổng hợp."))

                else:
                    st.warning(
                        "Chưa nhận diện được cảm xúc từ giọng nói."
                    )
                    st.code(
                        emotion_result.get(
                            "error",
                            "Không có thông tin lỗi."
                        )
                    )

            except subprocess.CalledProcessError as error:

                st.error("FFmpeg không thể chuyển đổi tệp âm thanh.")
                st.code(error.stderr or str(error))

            except Exception as error:

                st.error("Đã xảy ra lỗi khi phân tích âm thanh.")
                st.code(str(error))

            finally:

                # Xóa các tệp tạm
                for path in [temp_path, temp_wav_path]:

                    if path and os.path.exists(path):
                          os.remove(path)


# ==========================================
# 7. HO SO GIONG NOI CA NHAN
# ==========================================

elif menu == "Hồ sơ giọng nói cá nhân":

    page_header("user", "Hồ sơ giọng nói cá nhân")

    st.write(
        "Tạo hồ sơ giọng nói bình thường để SerenWize-AI "
        "có thể so sánh những thay đổi trong các lần ghi âm sau."
    )


    
    st.info(
        "Hãy chuẩn bị ít nhất 3 mẫu ghi âm khi bạn cảm thấy "
        "bình thường và thoải mái."
    )

    baseline_audio = st.file_uploader(
        "Chọn các mẫu giọng nói bình thường",
        type=["wav", "mp3", "ogg", "flac", "m4a"],
        accept_multiple_files=True,
        key="baseline_audio"
    )

    if baseline_audio:

        st.write(
            f"Đã chọn {len(baseline_audio)} tệp ghi âm."
        )

        
        if st.button("Tạo hồ sơ giọng nói cá nhân"):

            voice_samples = []
            emotion_samples = []

            progress = st.progress(0)

            for index, audio_file in enumerate(baseline_audio):

                temp_path = None
                temp_wav_path = None

                try:
                    suffix = os.path.splitext(
                        audio_file.name
                    )[1]

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=suffix
                    ) as temp_file:

                        temp_file.write(audio_file.getvalue())
                        temp_path = temp_file.name

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".wav"
                    ) as wav_file:

                        temp_wav_path = wav_file.name

                    subprocess.run(
                        [
                            "ffmpeg",
                            "-y",
                            "-i", temp_path,
                            "-ac", "1",
                            "-ar", "22050",
                            temp_wav_path
                        ],
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    # 1. Trích xuất đặc trưng âm học
                    voice_result = analyze_audio(temp_wav_path)

                    if voice_result.get("success"):
                        voice_samples.append(voice_result)
                    else:
                        st.warning(
                            f"Không trích xuất được đặc trưng âm học: "
                            f"{audio_file.name}"
                        )

                    # 2. Nhận diện cảm xúc bằng MERaLiON
                    emotion_result = analyze_voice_emotion(
                        temp_wav_path
                    )

                    if emotion_result.get("success"):
                        emotion_samples.append(emotion_result)
                    else:
                        st.warning(
                            f"MERaLiON không phân tích được: "
                            f"{audio_file.name} - "
                            f"{emotion_result.get('error', 'Lỗi không xác định')}"
                        )

                except Exception as error:

                    st.warning(
                        f"Lỗi với {audio_file.name}: {error}"
                    )

                finally:

                    for path in [temp_path, temp_wav_path]:

                        if path and os.path.exists(path):
                            os.remove(path)

                progress.progress(
                    (index + 1) / len(baseline_audio)
                )

            # 3. Kiểm tra số lượng mẫu hợp lệ
            if (
                len(voice_samples) >= 3
                and len(emotion_samples) >= 3
            ):

                baseline_result = create_baseline(
                    voice_samples,
                    emotion_samples
                )

                if baseline_result.get("success"):

                    baseline = baseline_result["baseline"]

                    emotion_baseline = baseline.get(
                        "emotion_baseline"
                    )

                    if emotion_baseline:

                        st.success(
                            "Đã tạo hồ sơ giọng nói và cảm xúc cá nhân thành công!"
                        )

                        st.subheader("1. Hồ sơ đặc trưng âm học")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "Cao độ trung bình",
                                f"{baseline['pitch_mean']:.2f} Hz"
                            )

                            st.metric(
                                "Năng lượng RMS",
                                f"{baseline['rms_mean']:.5f}"
                            )

                        with col2:
                            st.metric(
                                "Zero Crossing Rate",
                                f"{baseline['zcr_mean']:.5f}"
                            )

                            st.metric(
                                "Spectral Centroid",
                                f"{baseline['centroid_mean']:.2f} Hz"
                            )

                        st.subheader("2. Hồ sơ cảm xúc MERaLiON")

                        distribution = emotion_baseline[
                            "emotion_distribution"
                        ]

                        emotion_translation = {
                            "Neutral": "Bình thường",
                            "Happy": "Vui vẻ",
                            "Sad": "Buồn bã",
                            "Angry": "Tức giận",
                            "Surprised": "Ngạc nhiên",
                            "Fearful": "Sợ hãi",
                            "Disgusted": "Ghê sợ"
                        }

                        for emotion, ratio in distribution.items():

                            translated = emotion_translation.get(
                                emotion,
                                emotion
                            )

                            st.write(
                                f"**{translated}:** {ratio * 100:.2f}%"
                            )

                        average_confidence = emotion_baseline.get(
                            "average_confidence"
                        )

                        if average_confidence is not None:
                            st.metric(
                                "Độ tin cậy trung bình của các đoạn hợp lệ",
                                f"{average_confidence * 100:.2f}%"
                            )

                        st.caption(
                            f"Số mẫu âm học hợp lệ: {len(voice_samples)}"
                        )

                        st.caption(
                            f"Số mẫu MERaLiON hợp lệ: "
                            f"{emotion_baseline['sample_count']}"
                        )

                        st.info(
                            "Hồ sơ cảm xúc là dữ liệu tham chiếu được "
                            "tổng hợp từ các lần ghi âm. Đây không phải "
                            "đánh giá cảm xúc cố định hay chẩn đoán tâm lý."
                        )

                    else:
                        st.error(
                            "Chưa thể tạo hồ sơ cảm xúc. "
                            "Các mẫu ghi âm không có đủ đoạn cảm xúc hợp lệ."
                        )

                else:
                    st.error(
                        baseline_result.get(
                            "error",
                            "Không thể tạo hồ sơ giọng nói."
                        )
                    )

            else:
                st.error(
                    "Cần ít nhất 3 mẫu âm học hợp lệ và "
                    "3 mẫu MERaLiON phân tích thành công. "
                    "Hãy kiểm tra lại các tệp ghi âm."
                )

    st.divider()

    st.subheader("Hồ sơ giọng nói đã lưu")

    saved_baseline = load_baseline()

    if saved_baseline:

        st.success("Đã tìm thấy hồ sơ giọng nói cá nhân.")

           

    else:

        st.info(
            "Bạn chưa tạo hồ sơ giọng nói cá nhân."
        )



# ==========================================
# 8. BAO CAO TAM LY
# ==========================================

elif menu == "Báo cáo tâm lý":

    # GIỮ NGUYÊN TOÀN BỘ NỘI DUNG
    # BÁO CÁO TÂM LÝ HIỆN CÓ CỦA BẠN Ở ĐÂY.
    st.write(
        "Tạo hồ sơ giọng nói bình thường để SerenWize-AI "
        "có thể so sánh những thay đổi trong các lần ghi âm sau."
    )

    st.info(
        "Hãy tải lên ít nhất 3 mẫu ghi âm khi bạn cảm thấy "
        "bình thường và thoải mái."
    )

    baseline_audio = st.file_uploader(
        "Chọn các mẫu giọng nói bình thường",
        type=["wav", "mp3", "ogg", "flac", "m4a"],
        accept_multiple_files=True,
        key="baseline_audio"
    )

    if baseline_audio:

        st.write(
            f"Đã chọn {len(baseline_audio)} tệp ghi âm."
        )

        if st.button("Tạo hồ sơ giọng nói cá nhân"):

            voice_samples = []
            emotion_samples = []

            progress = st.progress(0)

            for index, audio_file in enumerate(baseline_audio):

                temp_path = None
                temp_wav_path = None

                try:
                    suffix = os.path.splitext(
                        audio_file.name
                    )[1]

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=suffix
                    ) as temp_file:

                        temp_file.write(audio_file.getvalue())
                        temp_path = temp_file.name

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".wav"
                    ) as wav_file:

                        temp_wav_path = wav_file.name

                    subprocess.run(
                        [
                            "ffmpeg",
                            "-y",
                            "-i", temp_path,
                            "-ac", "1",
                            "-ar", "22050",
                            temp_wav_path
                        ],
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    result = analyze_audio(temp_wav_path)

                    if result.get("success"):
                        voice_samples.append(result)
                    else:
                        st.warning(
                            f"Không phân tích được: {audio_file.name}"
                        )

                except Exception as error:

                    st.warning(
                        f"Lỗi với {audio_file.name}: {error}"
                    )

                finally:

                    for path in [temp_path, temp_wav_path]:

                        if path and os.path.exists(path):
                            os.remove(path)

                progress.progress(
                    (index + 1) / len(baseline_audio)
                )

            if (
                len(voice_samples) >= 3
                and len(emotion_samples) >= 3
            ):

                baseline_result = create_baseline(
                    voice_samples,
                    emotion_samples
                )

                if baseline_result.get("success"):

                    st.success(
                        "Đã tạo hồ sơ giọng nói cá nhân thành công!"
                    )

                    st.write(
                        "Các giá trị dưới đây là mức tham chiếu "
                        "được tính từ những mẫu ghi âm của bạn."
                    )

                    baseline = baseline_result["baseline"]

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Cao độ trung bình",
                            f"{baseline['pitch_mean']:.2f} Hz"
                        )

                        st.metric(
                            "Năng lượng RMS",
                            f"{baseline['rms_mean']:.5f}"
                        )

                    with col2:
                        st.metric(
                            "Zero Crossing Rate",
                            f"{baseline['zcr_mean']:.5f}"
                        )

                        st.metric(
                            "Spectral Centroid",
                            f"{baseline['centroid_mean']:.2f} Hz"
                        )

                    st.caption(
                        f"Số mẫu âm học hợp lệ: {len(voice_samples)}"
                    )

                    st.caption(
                        f"Số mẫu MERaLiON hợp lệ: {len(emotion_samples)}"
                    )

                    if "emotion_baseline" in baseline:
                        st.subheader("Phân bố cảm xúc tham chiếu")
                        st.json(baseline["emotion_baseline"])

                else:

                    st.error(
                        baseline_result.get(
                            "error",
                            "Không thể tạo hồ sơ giọng nói."
                        )
                    )

            else:

                st.error(
                    "Chưa đủ dữ liệu để tạo hồ sơ cá nhân. "
                    "Cần ít nhất 3 mẫu âm học hợp lệ và "
                    "3 mẫu nhận diện cảm xúc MERaLiON thành công."
                )

                st.write(
                    f"Số mẫu âm học hợp lệ: {len(voice_samples)}"
                )

                st.write(
                    f"Số mẫu MERaLiON hợp lệ: {len(emotion_samples)}"
                )

            st.divider()

            st.subheader("Hồ sơ giọng nói đã lưu")

    saved_baseline = load_baseline()

    if saved_baseline:

        st.success("Đã tìm thấy hồ sơ giọng nói cá nhân.")

           

    else:

        st.info(
            "Bạn chưa tạo hồ sơ giọng nói cá nhân."
        )


    page_header("chart", "Báo cáo tâm lý")

    st.write(
        "Báo cáo tổng hợp kết quả phân tích văn bản, "
        "dự đoán cảm xúc từ giọng nói và đặc trưng âm thanh."
    )

    # Lấy dữ liệu từ session_state
    combined = st.session_state.combined_result
    voice_emotion = st.session_state.voice_emotion_result

    text_data = None
    voice_data = None

    if combined is not None:
        text_data = combined.get("text_analysis")
        voice_data = combined.get("voice_analysis")

    # Bản dịch cảm xúc từ MERaLiON
    emotion_translation = {
        "Neutral": "Bình thường",
        "Happy": "Vui vẻ",
        "Sad": "Buồn bã",
        "Angry": "Tức giận",
        "Surprised": "Ngạc nhiên",
        "Fearful": "Sợ hãi",
        "Disgusted": "Ghê sợ",
        "Uncertain": "Chưa xác định"
    }

    # ==========================================
    # 1. PHAN TICH CAM XUC TU VAN BAN
    # ==========================================

    st.subheader("1. Phân tích cảm xúc từ văn bản")

    if text_data is not None:

        st.markdown(
            f"### 💜 Cảm xúc chính: "
            f"{text_data.get('primary_emotion', 'Chưa xác định')}"
        )

        emotions = text_data.get("emotions", [])
        keywords = text_data.get("keywords", [])

        if emotions:
            st.write("**Các cảm xúc nhận diện:**")
            st.write(", ".join(emotions))

        if keywords:
            st.write("**Từ khóa liên quan:**")
            st.write(", ".join(keywords))

        suggestion = text_data.get("suggestion")

        if suggestion:
            st.info(suggestion)

    else:
        st.info(
            "Chưa có kết quả phân tích văn bản. "
            "Hãy thực hiện phân tích văn bản trước."
        )

    st.divider()

    # ==========================================
    # 2. DU DOAN CAM XUC TU GIONG NOI
    # ==========================================

    st.subheader("2. Dự đoán cảm xúc từ giọng nói (MERaLiON)")

    if voice_emotion and voice_emotion.get("success"):

        overall_emotion = voice_emotion.get(
            "overall_emotion",
            "Uncertain"
        )

        translated_emotion = emotion_translation.get(
            overall_emotion,
            overall_emotion
        )

        confidence = voice_emotion.get("overall_confidence")

        st.markdown(
            f"### 🎙️ Cảm xúc dự đoán: {translated_emotion}"
        )

        if confidence is not None:
            st.metric(
                "Độ tin cậy do mô hình trả về",
                f"{float(confidence) * 100:.1f}%"
            )

        st.caption(
            "Đây là kết quả dự đoán của mô hình AI, "
            "không phải kết luận chắc chắn về trạng thái tâm lý."
        )

        
        segments = voice_emotion.get("segments", [])

        if segments:
            st.write("**Diễn biến cảm xúc theo từng đoạn âm thanh:**")

            segment_rows = []

            for index, segment in enumerate(segments, start=1):

                raw_emotion = segment.get(
                    "emotion",
                    "Uncertain"
                )

                translated_segment_emotion = emotion_translation.get(
                    raw_emotion,
                    raw_emotion
                )

                segment_confidence = segment.get("confidence")

                if segment_confidence is not None:
                    try:
                        segment_confidence = (
                            f"{float(segment_confidence) * 100:.1f}%"
                        )
                    except (ValueError, TypeError):
                        segment_confidence = "Không rõ"
                else:
                    segment_confidence = "Không rõ"

                start_time = segment.get("start_time")
                end_time = segment.get("end_time")

                segment_rows.append({
                    "Đoạn": index,
                    "Thời gian": (
                        f"{float(start_time):.2f} – "
                        f"{float(end_time):.2f} giây"
                    ) if start_time is not None and end_time is not None
                    else "Không rõ",
                    "Giới tính dự đoán": segment.get(
                        "gender",
                        "Không rõ"
                    ),
                    "Cảm xúc": translated_segment_emotion,
                    "Độ tin cậy": segment_confidence
                })

            if segment_rows:
                segment_df = pd.DataFrame(segment_rows)
                st.table(segment_df)
            else:
                st.info("Không có dữ liệu phân đoạn âm thanh.")

    else:
        st.info(
            "Chưa có kết quả dự đoán cảm xúc từ giọng nói. "
            "Hãy tải lên bản ghi âm và thực hiện phân tích giọng nói."
        )

    st.divider()

    # ==========================================
    # 3. DAC TRUNG AM THANH
    # ==========================================

    st.subheader("3. Đặc trưng âm thanh")

    if (
        voice_data is not None
        and voice_data.get("success")
        and voice_data.get("features")
    ):

        features = voice_data["features"]

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Thời lượng",
                f"{features.get('duration', 0)} giây"
            )

            st.metric(
                "Cao độ trung bình",
                f"{features.get('pitch_mean', 0)} Hz"
            )

            st.metric(
                "Năng lượng RMS",
                features.get("rms_mean", 0)
            )

        with col2:
            st.metric(
                "Zero Crossing Rate",
                features.get("zcr_mean", 0)
            )

            st.metric(
                "Spectral Centroid",
                f"{features.get('centroid_mean', 0)} Hz"
            )

        st.caption(
            "Các chỉ số trên mô tả đặc điểm tín hiệu âm thanh. "
            "Chúng không tự xác định cảm xúc hoặc chẩn đoán căng thẳng."
        )

    else:
        st.info(
            "Chưa có dữ liệu đặc trưng âm thanh."
        )

    st.divider()

    # ==========================================
    # 4. DOI CHIEU KET QUA
    # ==========================================

    st.subheader("4. Đối chiếu kết quả phân tích")

    if (
        text_data is not None
        and voice_emotion
        and voice_emotion.get("success")
    ):

        text_emotion = text_data.get(
            "primary_emotion",
            "Chưa xác định"
        )

        voice_emotion_name = emotion_translation.get(
            voice_emotion.get("overall_emotion", "Uncertain"),
            voice_emotion.get("overall_emotion", "Uncertain")
        )

        st.write(
            f"**Từ văn bản:** {text_emotion}"
        )

        st.write(
            f"**Từ giọng nói:** {voice_emotion_name}"
        )

        if (
            text_emotion == voice_emotion_name
            and text_emotion != "Chưa xác định"
        ):
            st.success(
                "Hai nguồn phân tích đưa ra cùng một nhãn cảm xúc. "
                "Đây là sự tương đồng giữa hai kết quả dự đoán."
            )

        else:
            st.info(
                "Hai nguồn phân tích đưa ra kết quả khác nhau "
                "hoặc chưa xác định. Điều này có thể xảy ra vì "
                "văn bản và giọng nói phản ánh những thông tin khác nhau."
            )

    else:
        st.info(
            "Cần có cả kết quả phân tích văn bản và dự đoán "
            "cảm xúc từ giọng nói để thực hiện đối chiếu."
        )

    st.divider()

    # ==========================================
    # 5. LUU Y
    # ==========================================

    st.subheader("5. Lưu ý về kết quả")

    st.warning(
        "SerenWize-AI là công cụ hỗ trợ tìm hiểu cảm xúc, "
        "không thay thế chuyên gia tâm lý và không đưa ra "
        "chẩn đoán bệnh lý. Kết quả AI có thể chưa chính xác "
        "và cần được xem xét trong bối cảnh thực tế."
    )

    # ==========================================
    # 6. LICH SU PHUC HOI CAM XUC
    # ==========================================

    st.divider()

    st.subheader("6. Lịch sử phục hồi cảm xúc")

    recovery_history = load_recovery_history()

    if recovery_history:

        history_df = pd.DataFrame(recovery_history)

        # Chuyển đổi thời gian
        history_df["timestamp"] = pd.to_datetime(
            history_df["timestamp"],
            errors="coerce"
        )

        history_df = history_df.sort_values("timestamp")

        # Thống kê tổng quan
        total_sessions = len(history_df)

        average_before = history_df["intensity_before"].mean()
        average_after = history_df["intensity_after"].mean()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Số lần phục hồi",
                total_sessions
            )

        with col2:
            st.metric(
                "Trước hoạt động",
                f"{average_before:.1f}/10"
            )

        with col3:
            st.metric(
                "Sau hoạt động",
                f"{average_after:.1f}/10",
                delta=f"{average_before - average_after:.1f} điểm",
                delta_color="normal"
            )

        st.caption(
            "Mức thay đổi được tính từ đánh giá chủ quan "
            "của người dùng, không phải thước đo hiệu quả điều trị."
        )

        # Biểu đồ theo dõi
        st.subheader("Diễn biến mức độ khó chịu")

        chart_df = history_df[
            ["timestamp", "intensity_before", "intensity_after"]
        ].copy()

        chart_df = chart_df.dropna(subset=["timestamp"])

        chart_df = chart_df.rename(columns={
            "intensity_before": "Trước hoạt động",
            "intensity_after": "Sau hoạt động"
        })

        chart_df = chart_df.set_index("timestamp")

        st.line_chart(
            chart_df[["Trước hoạt động", "Sau hoạt động"]]
        )

        # Bảng lịch sử
        st.subheader("Chi tiết các lần phục hồi")

        display_df = history_df.rename(columns={
            "timestamp": "Thời gian",
            "feeling": "Cảm xúc ban đầu",
            "intensity_before": "Mức độ trước",
            "need": "Nhu cầu hỗ trợ",
            "activity": "Hoạt động",
            "intensity_after": "Mức độ sau",
            "feedback": "Phản hồi"
        })

        st.dataframe(
            display_df[
                [
                    "Thời gian",
                    "Cảm xúc ban đầu",
                    "Mức độ trước",
                    "Nhu cầu hỗ trợ",
                    "Hoạt động",
                    "Mức độ sau",
                    "Phản hồi"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Chưa có lịch sử phục hồi cảm xúc. "
            "Hãy thực hiện một hoạt động trong mục "
            "'Gợi ý chăm sóc' và lưu kết quả để bắt đầu theo dõi."
        )





# ==========================================
# 8. GOI Y CHAM SOC
# ==========================================


elif menu == "Gợi ý chăm sóc":

    page_header("heart", "Gợi ý chăm sóc")

    st.write(
        "SerenWize-AI muốn hiểu cảm xúc và nhu cầu của bạn "
        "trước khi đề xuất những hoạt động hỗ trợ phù hợp."
    )

    st.info(
        "Bạn là người hiểu rõ cảm xúc của mình nhất. "
        "Các kết quả AI chỉ mang tính tham khảo."
    )

    # 1. Tự đánh giá cảm xúc
    st.subheader("1. Bạn đang cảm thấy thế nào?")

    feeling = st.radio(
        "Hãy chọn cảm xúc gần nhất với trạng thái hiện tại:",
        [
            "Buồn bã",
            "Lo lắng",
            "Căng thẳng",
            "Mệt mỏi",
            "Tức giận",
            "Bình thường",
            "Khó xác định cảm xúc"
        ],
        key="self_feeling"
    )

    # 2. Đánh giá mức độ khó chịu
    st.subheader("2. Mức độ khó chịu hiện tại")

    intensity = st.slider(
        "Từ 0 (hoàn toàn thoải mái) đến 10 (rất khó chịu)",
        min_value=0,
        max_value=10,
        value=5,
        key="self_intensity"
    )

    # 3. Xác định nhu cầu hỗ trợ
    st.subheader("3. Bạn muốn được hỗ trợ điều gì?")

    need = st.radio(
        "Chọn nhu cầu phù hợp nhất:",
        [
            "Thư giãn cơ thể",
            "Giải tỏa cảm xúc",
            "Lấy lại sự tập trung",
            "Được lắng nghe và chia sẻ",
              "Nghỉ ngơi và phục hồi năng lượng"
    ]
)

    st.divider()

    # 4. Đề xuất hoạt động theo nhu cầu đã xác nhận
    if st.button("Tìm hoạt động phù hợp", use_container_width=True):

        st.session_state.recovery_started = True

        st.session_state.recovery_session = {
    "feeling": feeling,
    "intensity_before": intensity,
    "need": need,
    "activity": None,
    "saved": False
}

        st.subheader("Gợi ý dành cho bạn")

        activities = {
            "Thư giãn cơ thể":{
                "title": "Hít thở nhẹ nhàng",
                "duration": "2–3 phút",
                "steps": [
                    "Ngồi ở tư thế thoải mái.",
                    "Hít vào nhẹ nhàng trong khoảng 3 giây.",
                    "Thở ra chậm trong khoảng 4 giây.",
                    "Lặp lại theo nhịp tự nhiên, không cố nín thở."
                ]
            },

            "Giải tỏa cảm xúc": {
                "title": "Viết nhật ký cảm xúc",
                "duration": "5 phút",
                "steps": [
                    "Viết ra điều đang khiến bạn khó chịu.",
                    "Mô tả cảm xúc của bạn mà không tự phán xét.",
                    "Viết một điều bạn muốn thay đổi.",
                    "Nghĩ về một việc nhỏ bạn có thể làm ngay hôm nay."
                ]
            },

            "Lấy lại sự tập trung": {
                "title": "Bài tập tập trung 5-4-3-2-1",
                "duration": "3–5 phút",
                "steps": [
                    "Nhận biết 5 thứ bạn có thể nhìn thấy.",
                    "Nhận biết 4 thứ bạn có thể chạm vào.",
                    "Lắng nghe 3 âm thanh xung quanh.",
                    "Nhận biết 2 mùi hương.",
                    "Chú ý 1 cảm giác trong cơ thể."
                ]
            },

            "Được lắng nghe và chia sẻ": {
                "title": "Chia sẻ cảm xúc",
                "duration": "5–10 phút",
                "steps": [
                    "Chọn một người bạn tin tưởng.",
                    "Nói về điều đang khiến bạn bận tâm.",
                    "Chia sẻ điều bạn mong muốn được giúp đỡ.",
                    "Bạn không cần phải giải quyết mọi chuyện ngay lập tức."
                ]
            },

            "Nghỉ ngơi và phục hồi năng lượng": {
                "title": "Nghỉ ngơi có chủ đích",
                "duration": "5–10 phút",
                "steps": [
                    "Tạm dừng công việc hoặc bài tập.",
                    "Uống một chút nước.",
                    "Rời mắt khỏi màn hình.",
                    "Thư giãn ở nơi yên tĩnh và dễ chịu."
                ]
            }
        }

        activity = activities[need]
        st.session_state.recovery_session["activity"] = activity["title"]

        st.success(
            "Đã ghi nhận cảm xúc và nhu cầu hỗ trợ của bạn!"
        )

        st.markdown(f"### 🌿 {activity['title']}")

        st.caption(
            f"Thời lượng gợi ý: {activity['duration']}"
        )

        for index, step in enumerate(activity["steps"], 1):
            st.write(f"**{index}.** {step}")

        st.divider()

        st.write(f"**Cảm xúc bạn tự đánh giá:** {feeling}")
        st.write(f"**Mức độ khó chịu:** {intensity}/10")
        st.write(f"**Nhu cầu hỗ trợ:** {need}")

        if intensity >= 8:
            st.warning(
                "Bạn đang tự đánh giá mức độ khó chịu rất cao. "
                "Hãy cân nhắc chia sẻ với người thân, giáo viên "
                "hoặc chuyên gia tâm lý đáng tin cậy. "
                "Bạn không cần phải đối mặt với mọi chuyện một mình."
            )

        st.info(
            "Gợi ý trên mang tính hỗ trợ tự chăm sóc, không thay thế "
            "tư vấn của chuyên gia tâm lý. Nếu cảm thấy quá tải, hãy "
            "chia sẻ với người bạn tin tưởng."
        )
     
    # Đánh giá sau hoạt động
    if (
        st.session_state.recovery_session is not None
        and st.session_state.recovery_session.get("activity")
    ):
        st.divider()
        st.subheader("Đánh giá sau hoạt động")

        st.write(
            "Hãy đánh giá cảm xúc của bạn sau khi thực hiện "
            "hoạt động vừa được gợi ý."
        )

        intensity_after = st.slider(
            "Mức độ khó chịu hiện tại:",
            min_value=0,
            max_value=10,
            value=5,
            key="intensity_after"
        )

        feedback = st.radio(
            "Hoạt động này có giúp ích cho bạn không?",
            [
                "Rất hữu ích",
                "Có ích một phần",
                "Chưa cảm nhận được sự thay đổi",
                "Không phù hợp với tôi"
            ],
            key="recovery_feedback"
        )

        if st.button("Lưu kết quả phục hồi", use_container_width=True, key="btn_save_recovery"):
            session = st.session_state.recovery_session

            if session.get("saved"):
                st.info("Kết quả này đã được lưu rồi.")
            else:
                result = save_recovery_session(
                    feeling=session["feeling"],
                    intensity_before=session["intensity_before"],
                    need=session["need"],
                    activity=session["activity"],
                    intensity_after=intensity_after,
                    feedback=feedback
                )

                if result["success"]:
                    session["saved"] = True
                    st.success("Đã lưu kết quả phục hồi thành công!")
                else:
                    st.error(f"Không thể lưu: {result['error']}")


    

        



# ==========================================

# 9. GIOI THIEU DU AN
# ==========================================

elif menu == "Phòng luyện tập":

    page_header("wind", "Phòng luyện tập")

    st.write(
        "Không gian luyện tập hô hấp và thư giãn "
        "dành riêng cho bạn."
    )

    st.info(
        "Hãy ngồi ở tư thế thoải mái và luyện tập "
        "theo nhịp thở tự nhiên của bạn."
    )

    st.subheader("Chọn bài luyện tập")

    st.write(
        "Chọn một bài, chọn thời lượng, nhấn Bắt đầu và làm theo "
        "hướng dẫn trên màn hình."
    )

    _tr = st.session_state.get("fusion_result") or st.session_state.get("text_result")
    _emo = _tr.get("emotion") if isinstance(_tr, dict) else None
    _rec = recommend_exercise(_emo)
    if _rec:
        st.success(
            f"Dựa trên kết quả phân tích gần nhất (**{_emo}**), SerenWize gợi ý bài "
            f"**{_rec['name']}**: {_rec['reason']}"
        )
    breathing_studio(default_id=_rec["id"] if _rec else "calm")

    st.caption(
        "Lưu ý: Hãy duy trì nhịp thở thoải mái, "
        "không cố hít quá sâu hoặc nín thở quá lâu. "
        "Nếu cảm thấy chóng mặt hoặc khó chịu, hãy dừng lại."
    )




# ==========================================
# 10. GIOI THIEU DU AN
# ==========================================

elif menu == "Giới thiệu dự án":

    page_header("info", "Giới thiệu dự án")

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

    st.markdown("""
    <div class="footer">
        ♡ SerenWize-AI |
        Understand Emotions. Empower Minds.
        <br><br>
        Lắng nghe cảm xúc – Thấu hiểu tâm lý – Đồng hành cùng bạn
    </div>
    """, unsafe_allow_html=True)
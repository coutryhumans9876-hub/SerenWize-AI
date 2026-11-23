def combine_analysis(text_result, voice_result):
    """
    Kết hợp kết quả phân tích văn bản và đặc trưng giọng nói.

    Lưu ý:
    Đặc trưng âm thanh chưa được dùng để kết luận cảm xúc.
    """

    # Kiểm tra dữ liệu đầu vào
    if not isinstance(text_result, dict):
        text_result = {}

    if not isinstance(voice_result, dict):
        voice_result = {}

    # Lấy kết quả phân tích văn bản
    text_emotion = text_result.get(
        "emotion",
        "Chưa xác định"
    )

    text_emotions = text_result.get(
        "emotions",
        []
    )

    keywords = text_result.get(
        "keywords",
        []
    )

    suggestion = text_result.get(
        "suggestion",
        "Bạn có thể chia sẻ thêm về cảm xúc của mình."
    )

    # Kiểm tra kết quả phân tích giọng nói
    voice_success = voice_result.get(
        "success",
        False
    )

    if voice_success:
        voice_features = {
            "duration": voice_result.get("duration"),
            "pitch_mean": voice_result.get("pitch_mean"),
            "rms_mean": voice_result.get("rms_mean"),
            "zcr_mean": voice_result.get("zcr_mean"),
            "centroid_mean": voice_result.get("centroid_mean"),
            "mfcc_mean": voice_result.get("mfcc_mean")
        }
    else:
        voice_features = None

    # Tạo báo cáo tổng hợp
    return {
        "success": True,

        "text_analysis": {
            "primary_emotion": text_emotion,
            "emotions": text_emotions,
            "keywords": keywords,
            "suggestion": suggestion
        },

        "voice_analysis": {
            "success": voice_success,
            "features": voice_features
        },

        "overall_message": (
            "Đã tổng hợp kết quả phân tích văn bản "
            "và đặc trưng giọng nói."
        ),

        "limitation": (
            "Kết quả cảm xúc hiện dựa trên phân tích "
            "từ khóa văn bản. Đặc trưng âm thanh chỉ "
            "mang tính mô tả, chưa xác định cảm xúc "
            "hoặc mức độ căng thẳng."
        )
    }
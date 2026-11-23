
import re

# ==========================================
# 1. TU KHOA CAM XUC
# ==========================================

EMOTION_KEYWORDS = {
    "Vui vẻ": [
        "vui", "hạnh phúc", "phấn khởi", "hào hứng",
        "thoải mái", "yêu đời", "tuyệt vời",
        "sung sướng", "buồn cười", "phấn khích"
    ],

    "Buồn bã": [
        "buồn", "cô đơn", "thất vọng", "tủi thân",
        "chán nản", "đau lòng", "khóc", "bâng khuâng",
        "lụy", "rầu", "vô vọng", "tuyệt vọng",
        "mất mát", "trống trải"
    ],

    "Lo lắng": [
        "lo lắng", "bất an", "sợ hãi", "hồi hộp",
        "hoang mang", "không yên tâm", "sốt ruột",
        "bứt rứt", "thót tim"
    ],

    "Căng thẳng": [
        "căng thẳng", "áp lực", "mệt mỏi", "quá tải",
        "kiệt sức", "stress", "ngột ngạt"
    ],

    "Tức giận": [
        "tức giận", "bực bội", "khó chịu",
        "phẫn nộ", "ức chế", "cáu", "ấm ức",
        "căm phẫn", "nổi điên"
    ]
}


# ==========================================
# 2. GOI Y CHAM SOC
# ==========================================

EMOTION_SUGGESTIONS = {
    "Vui vẻ": (
        "Hãy duy trì những hoạt động tích cực "
        "và chia sẻ niềm vui với mọi người."
    ),

    "Buồn bã": (
        "Bạn có thể trò chuyện với người mình tin tưởng "
        "và dành thời gian chăm sóc bản thân."
    ),

    "Lo lắng": (
        "Hãy thử hít thở chậm, chia nhỏ vấn đề "
        "và tìm người đáng tin cậy để chia sẻ."
    ),

    "Căng thẳng": (
        "Bạn nên nghỉ ngơi hợp lý, chia nhỏ công việc "
        "và cân bằng thời gian học tập."
    ),

    "Tức giận": (
        "Hãy tạm dừng, hít thở sâu và cho bản thân "
        "thời gian bình tĩnh."
    )
}


# ==========================================
# 3. XU LY TU PHU DINH
# ==========================================

NEGATION_WORDS = [
    "không", "chẳng", "chưa", "đâu có",
    "không hề", "chẳng hề", "không còn",
    "chẳng còn"
]


def is_negated(text, start):
    """
    Kiểm tra từ khóa có đứng sau từ phủ định gần đó không.
    Đây là quy tắc thử nghiệm, chưa hiểu đầy đủ ngữ cảnh.
    """

    prefix = text[max(0, start - 30):start].strip()

    for negation in NEGATION_WORDS:
        if re.search(
            r"(?<!\w)" + re.escape(negation) + r"\s*$",
            prefix
        ):
            return True

    return False


# ==========================================
# 4. PHAN TICH CAM XUC VAN BAN
# ==========================================

def analyze_text(text):
    """
    Phân tích từ khóa cảm xúc trong văn bản tiếng Việt.

    Đây là hệ thống dựa trên từ khóa thử nghiệm,
    chưa phải mô hình AI được huấn luyện.
    """

    if not isinstance(text, str) or not text.strip():
        return {
            "emotion": "Chưa xác định",
            "emotions": [],
            "keywords": [],
            "negated_keywords": [],
            "suggestion": "Vui lòng nhập nội dung để phân tích.",
            "message": "Không có dữ liệu đầu vào."
        }

    normalized_text = re.sub(
        r"\s+", " ", text.lower()
    ).strip()

    emotion_matches = {}
    negated_keywords = []

    for emotion, keywords in EMOTION_KEYWORDS.items():

        matched = []

        for keyword in keywords:
            start = 0

            while True:
                position = normalized_text.find(
                    keyword, start
                )

                if position == -1:
                    break

                if is_negated(normalized_text, position):
                    if keyword not in negated_keywords:
                        negated_keywords.append(keyword)
                else:
                    if keyword not in matched:
                        matched.append(keyword)

                start = position + len(keyword)

        emotion_matches[emotion] = matched

    # Xác định các nhóm cảm xúc được nhận diện
    detected_emotions = [
        emotion
        for emotion, keywords in emotion_matches.items()
        if keywords
    ]

    if not detected_emotions:
        return {
            "emotion": "Chưa xác định",
            "emotions": [],
            "keywords": [],
            "negated_keywords": negated_keywords,
            "suggestion": (
                "Bạn có thể chia sẻ thêm về cảm xúc "
                "hoặc tình huống của mình."
            ),
            "message": "Chưa tìm thấy từ khóa cảm xúc phù hợp."
        }

    # Chọn nhóm có nhiều từ khóa nhất
    primary_emotion = max(
        detected_emotions,
        key=lambda emotion: len(emotion_matches[emotion])
    )

    # Thu thập toàn bộ từ khóa
    all_keywords = [
        keyword
        for emotion in detected_emotions
        for keyword in emotion_matches[emotion]
    ]

    return {
        "emotion": primary_emotion,
        "emotions": detected_emotions,
        "keywords": all_keywords,
        "negated_keywords": negated_keywords,
        "suggestion": EMOTION_SUGGESTIONS[primary_emotion],
        "message": (
            "Đã hoàn thành phân tích từ khóa cảm xúc thử nghiệm."
        )
    }

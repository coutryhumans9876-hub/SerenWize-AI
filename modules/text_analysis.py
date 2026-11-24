"""
Phân tích cảm xúc văn bản tiếng Việt bằng từ khóa (thử nghiệm).

Đây KHÔNG phải mô hình AI được huấn luyện. So với bản cũ, bản này:
- chuẩn hóa chữ hoa/thường, khoảng trắng
- hỗ trợ gõ không dấu ("toi rat buon")
- dò theo ranh giới từ, có danh sách loại trừ ("buồn ngủ", "tức là"...)
- xử lý phủ định qua các từ đệm ("chẳng thấy hạnh phúc", "không còn buồn")
- nhận mức độ qua từ nhấn mạnh ("rất", "quá", "hơi"...)
- trả về phân bố nhiều cảm xúc, mức độ, độ chắc chắn, chủ đề
- kiểm tra tín hiệu khẩn cấp (modules/safety.py) trước mọi thứ khác
"""

import re
import unicodedata

from modules.safety import detect_crisis


# ==========================================
# 1. TU KHOA CAM XUC
# ==========================================

# Từ khóa mạnh (trọng số 1.0)
EMOTION_KEYWORDS = {
    "Vui vẻ": [
        "vui", "vui vẻ", "hạnh phúc", "phấn khởi", "hào hứng",
        "thoải mái", "yêu đời", "tuyệt vời", "sung sướng",
        "buồn cười", "phấn khích", "nhẹ nhõm", "đỡ hơn", "yên tâm",
        "tự hào", "biết ơn", "háo hức", "thích thú", "hài lòng",
        "mừng", "bình yên", "thư thái", "ổn hơn",
    ],

    "Buồn bã": [
        "buồn", "cô đơn", "thất vọng", "tủi thân",
        "chán nản", "đau lòng", "khóc", "bâng khuâng",
        "lụy", "rầu", "vô vọng", "tuyệt vọng",
        "mất mát", "trống trải", "vô nghĩa", "tủi",
        "hụt hẫng", "tổn thương", "bơ vơ", "bị bỏ rơi",
        "không ai hiểu", "bị cô lập", "nặng nề",
    ],

    "Lo lắng": [
        "lo lắng", "bất an", "sợ hãi", "hồi hộp",
        "hoang mang", "không yên tâm", "sốt ruột",
        "bứt rứt", "thót tim", "lo sợ", "lo âu", "e ngại",
    ],

    "Căng thẳng": [
        "căng thẳng", "áp lực", "mệt mỏi", "quá tải",
        "kiệt sức", "stress", "ngột ngạt", "stress",
    ],

    "Tức giận": [
        "tức giận", "bực bội", "khó chịu",
        "phẫn nộ", "ức chế", "cáu", "ấm ức",
        "căm phẫn", "nổi điên", "bực mình", "giận", "ghét",
        "điên tiết",
    ],
}

# Từ khóa yếu (trọng số 0.5): hay dùng với nghĩa khác
WEAK_KEYWORDS = {
    "Buồn bã": ["chán"],
    "Lo lắng": ["lo", "sợ"],
    "Căng thẳng": ["mệt"],
    "Tức giận": ["bực", "tức", "điên"],
}

# Cụm cần loại trừ: không phải cảm xúc dù chứa từ khóa
EXCLUDE_PHRASES = [
    "buồn ngủ", "buồn tay", "buồn miệng", "buồn nôn", "buồn chân buồn tay",
    "tức là", "tức thì", "tức khắc", "tức thời",
    "lo liệu", "lo cho", "lo xong", "lo việc", "lo toan",
]

# Ở chế độ không dấu, các từ ngắn này dễ trùng từ khác nên giảm trọng số
STRIPPED_WEAK_KEYS = {"so", "chan", "buc", "tuc", "dien", "mung", "lo"}

EMOTION_PRIORITY = ["Buồn bã", "Lo lắng", "Căng thẳng", "Tức giận", "Vui vẻ"]


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
    ),
}


# ==========================================
# 3. TU PHU DINH, NHAN MANH, CHU DE
# ==========================================

# Giữ lại tên cũ để tương thích với mã khác
NEGATION_WORDS = [
    "không", "chẳng", "chả", "chưa", "đâu", "hết", "đừng", "đỡ",
]

# Từ đệm được phép đứng giữa từ phủ định và từ khóa
FILLER_WORDS = [
    "thấy", "cảm", "còn", "hề", "có", "được", "phải", "là",
    "quá", "thật", "mấy", "hơi", "cũng",
]

# "không còn buồn", "hết buồn", "đỡ buồn" => nhẹ nhõm
RELIEF_WORDS = ["còn", "hết", "đỡ"]

INTENSIFIERS = [
    "rất", "quá", "cực kỳ", "cực kì", "cực", "vô cùng", "lắm",
    "kinh khủng", "khủng khiếp", "hết sức", "siêu", "thực sự",
    "thật sự", "cực độ",
]
DIMINISHERS = ["hơi", "một chút", "chút", "phần nào", "đôi chút"]

TOPIC_KEYWORDS = {
    "Học tập": [
        "học", "thi", "kỳ thi", "kiểm tra", "bài kiểm tra", "điểm",
        "bài tập", "deadline", "thầy", "cô giáo", "lớp", "trường",
    ],
    "Bạn bè": [
        "bạn", "bạn bè", "bắt nạt", "bị cô lập", "người yêu", "nhóm",
    ],
    "Gia đình": [
        "bố", "mẹ", "ba mẹ", "bố mẹ", "cha mẹ", "gia đình", "ông bà",
    ],
    "Bản thân": [
        "bản thân", "ngoại hình", "tự ti", "cân nặng",
    ],
}


# ==========================================
# 4. XU LY VAN BAN
# ==========================================

def strip_diacritics(text):
    """Bỏ dấu tiếng Việt, giữ nguyên độ dài chuỗi (nếu đã ở dạng NFC)."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.replace("đ", "d").replace("Đ", "D")


def normalize(text):
    """Chuyển về chữ thường, NFC, gom khoảng trắng."""
    text = unicodedata.normalize("NFC", text).lower()
    return re.sub(r"\s+", " ", text).strip()


def diacritic_ratio(norm_text):
    """Tỉ lệ từ có dấu. Gần 0 nghĩa là người dùng gõ không dấu."""
    words = re.findall(r"\w+", norm_text)
    if not words:
        return 1.0
    marked = sum(1 for w in words if strip_diacritics(w) != w)
    return marked / len(words)


def _both(words):
    return {w for w in words} | {strip_diacritics(w) for w in words}


_NEG = _both(NEGATION_WORDS)
_FILLER = _both(FILLER_WORDS)
_RELIEF = _both(RELIEF_WORDS)

_INTENS_RE = re.compile(
    r"(?<!\w)(?:"
    + "|".join(
        re.escape(p) for p in sorted(_both(INTENSIFIERS), key=len, reverse=True)
    )
    + r")(?!\w)"
)
_DIMIN_RE = re.compile(
    r"(?<!\w)(?:"
    + "|".join(
        re.escape(p) for p in sorted(_both(DIMINISHERS), key=len, reverse=True)
    )
    + r")(?!\w)"
)

_PUNCT = re.compile(r"[,.;:!?…\n()]")


def _before_tokens(text, start, n):
    tail = _PUNCT.split(text[:start])[-1]
    return re.findall(r"\w+", tail)[-n:]


def _after_tokens(text, end, n):
    head = _PUNCT.split(text[end:])[0]
    return re.findall(r"\w+", head)[:n]


class _Lexicon:
    """Từ điển đã biên dịch cho một chế độ (có dấu hoặc không dấu)."""

    def __init__(self, stripped):
        self.stripped = stripped
        self.entries = {}

        def add(phrase, emotion, weight):
            key = strip_diacritics(phrase) if stripped else phrase
            if key in self.entries:
                return
            if stripped and emotion is not None and key in STRIPPED_WEAK_KEYS:
                weight = min(weight, 0.5)
            self.entries[key] = (emotion, weight, phrase)

        for emotion, words in EMOTION_KEYWORDS.items():
            for w in words:
                add(w, emotion, 1.0)
        for emotion, words in WEAK_KEYWORDS.items():
            for w in words:
                add(w, emotion, 0.5)
        for w in EXCLUDE_PHRASES:
            add(w, None, 0.0)

        keys = sorted(self.entries, key=len, reverse=True)
        self.regex = re.compile(
            r"(?<!\w)(?:" + "|".join(re.escape(k) for k in keys) + r")(?!\w)"
        )


_EXACT = _Lexicon(stripped=False)
_STRIPPED = _Lexicon(stripped=True)


def _negation(tokens):
    """
    Kiểm tra từ khóa có bị phủ định không, bỏ qua từ đệm.
    Trả về (bị_phủ_định, là_nhẹ_nhõm).
    """
    i = len(tokens) - 1
    used = []
    skipped = 0

    while i >= 0 and tokens[i] in _FILLER and skipped < 3:
        used.append(tokens[i])
        i -= 1
        skipped += 1

    if i >= 0 and tokens[i] in _NEG:
        used.append(tokens[i])
        return True, any(u in _RELIEF for u in used)

    return False, False


def _modifier(before, after):
    near_before = " ".join(before[-2:])
    near_after = " ".join(after[:2])
    joined = (near_before + " | " + near_after)

    if _INTENS_RE.search(joined):
        return 1.5
    if _DIMIN_RE.search(joined):
        return 0.7
    return 1.0


def _scan(text, lexicon, occupied):
    """Quét văn bản, trả về (danh_sách_hit, các_khoảng_đã_dùng)."""
    hits = []
    spans = []

    for m in lexicon.regex.finditer(text):
        start, end = m.span()

        if any(start < o_end and end > o_start for o_start, o_end in occupied):
            continue

        spans.append((start, end))

        emotion, weight, display = lexicon.entries[m.group(0)]
        if emotion is None:
            continue

        before = _before_tokens(text, start, 4)
        after = _after_tokens(text, end, 2)
        negated, relief = _negation(before)

        hits.append({
            "emotion": emotion,
            "display": display,
            "weight": weight,
            "negated": negated,
            "relief": relief,
            "multiplier": _modifier(before, after),
        })

    return hits, spans


def _detect_topics(norm, stripped, use_stripped):
    topics = []
    for topic, words in TOPIC_KEYWORDS.items():
        for w in words:
            pattern = r"(?<!\w)" + re.escape(w) + r"(?!\w)"
            found = re.search(pattern, norm)
            if not found and use_stripped:
                found = re.search(
                    r"(?<!\w)" + re.escape(strip_diacritics(w)) + r"(?!\w)",
                    stripped,
                )
            if found:
                topics.append(topic)
                break
    return topics


def _empty_result(message, suggestion, crisis=None):
    crisis = crisis or detect_crisis("")
    return {
        "emotion": "Chưa xác định",
        "emotions": [],
        "keywords": [],
        "negated_keywords": [],
        "scores": {},
        "distribution": {},
        "intensity": None,
        "confidence": "Thấp",
        "topics": [],
        "crisis": crisis,
        "suggestion": suggestion,
        "message": message,
    }


# ==========================================
# 5. PHAN TICH CAM XUC VAN BAN
# ==========================================

def analyze_text(text):
    """
    Phân tích từ khóa cảm xúc trong văn bản tiếng Việt.

    Đây là hệ thống dựa trên từ khóa thử nghiệm,
    chưa phải mô hình AI được huấn luyện.

    Giữ nguyên các khóa cũ (emotion, emotions, keywords,
    negated_keywords, suggestion, message) và bổ sung:
    scores, distribution, intensity, confidence, topics, crisis.
    """

    if not isinstance(text, str) or not text.strip():
        return _empty_result(
            "Không có dữ liệu đầu vào.",
            "Vui lòng nhập nội dung để phân tích.",
        )

    crisis = detect_crisis(text)

    norm = normalize(text)
    stripped = strip_diacritics(norm)
    use_stripped = diacritic_ratio(norm) < 0.5

    hits, spans = _scan(norm, _EXACT, [])

    if use_stripped:
        extra, _ = _scan(stripped, _STRIPPED, spans)
        hits += extra

    # Điểm trực tiếp: mỗi cụm từ tính một lần, lấy giá trị cao nhất
    best = {}
    negated_keywords = []
    inferred = {}

    for h in hits:
        if h["negated"]:
            if h["display"] not in negated_keywords:
                negated_keywords.append(h["display"])

            if h["emotion"] == "Vui vẻ":
                inferred[("Buồn bã", h["display"])] = 0.5
            elif h["relief"]:
                inferred[("Vui vẻ", h["display"])] = 0.5
            continue

        key = (h["emotion"], h["display"])
        value = h["weight"] * h["multiplier"]
        best[key] = max(best.get(key, 0.0), value)

    # Tín hiệu khủng hoảng thể hiện sự tuyệt vọng nặng nề
    if crisis["level"] == "high":
        for phrase in crisis["matched"]:
            best[("Buồn bã", phrase)] = max(
                best.get(("Buồn bã", phrase), 0.0), 2.0
            )

    scores = {}
    direct_total = 0.0

    for (emotion, _), value in best.items():
        scores[emotion] = scores.get(emotion, 0.0) + value
        direct_total += value

    for (emotion, _), value in inferred.items():
        scores[emotion] = scores.get(emotion, 0.0) + value

    if not scores:
        result = _empty_result(
            "Chưa tìm thấy từ khóa cảm xúc phù hợp.",
            (
                "Bạn có thể chia sẻ thêm về cảm xúc "
                "hoặc tình huống của mình."
            ),
            crisis,
        )
        result["negated_keywords"] = negated_keywords
        result["topics"] = _detect_topics(norm, stripped, use_stripped)
        if crisis["level"] == "high":
            result["suggestion"] = crisis["short_message"]
        return result

    order = {e: i for i, e in enumerate(EMOTION_PRIORITY)}
    detected = sorted(scores, key=lambda e: (-scores[e], order.get(e, 99)))
    primary = detected[0]

    total = sum(scores.values())
    distribution = {e: round(scores[e] / total, 2) for e in detected}

    top_share = scores[primary] / total
    if direct_total <= 0:
        confidence = "Thấp"
    elif top_share >= 0.6 and direct_total >= 1.5:
        confidence = "Cao"
    elif top_share >= 0.5:
        confidence = "Trung bình"
    else:
        confidence = "Thấp"

    if scores[primary] < 1.5:
        intensity = "Nhẹ"
    elif scores[primary] < 3:
        intensity = "Vừa"
    else:
        intensity = "Mạnh"

    keywords = []
    for emotion in detected:
        phrases = sorted(
            (p for (e, p), v in best.items() if e == emotion),
            key=lambda p: -best[(emotion, p)],
        )
        for p in phrases:
            if p not in keywords:
                keywords.append(p)

    message = "Đã hoàn thành phân tích từ khóa cảm xúc thử nghiệm."
    if inferred:
        message += " Một số cảm xúc được suy ra từ ngữ cảnh phủ định."

    suggestion = EMOTION_SUGGESTIONS[primary]
    if crisis["level"] == "high":
        suggestion = crisis["short_message"]

    return {
        "emotion": primary,
        "emotions": detected,
        "keywords": keywords,
        "negated_keywords": negated_keywords,
        "scores": {e: round(scores[e], 2) for e in detected},
        "distribution": distribution,
        "intensity": intensity,
        "confidence": confidence,
        "topics": _detect_topics(norm, stripped, use_stripped),
        "crisis": crisis,
        "suggestion": suggestion,
        "message": message,
    }
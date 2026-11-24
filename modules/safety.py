"""
Phát hiện tín hiệu cần quan tâm khẩn cấp trong văn bản của học sinh.

Đây là bộ lọc theo cụm từ, KHÔNG phải công cụ chẩn đoán. Nguyên tắc thiết kế:
thà báo nhầm (hiện lời quan tâm nhẹ nhàng) còn hơn bỏ sót.

Các mức:
- "high":      có dấu hiệu ý định tự tử / tự làm hại bản thân
- "attention": có dấu hiệu bị bắt nạt, bạo lực, xâm hại, đe dọa
- "check_in":  cách nói quá lời kiểu "mệt muốn chết", chỉ cần hỏi thăm nhẹ
- "none":      không phát hiện
"""

import re
import unicodedata


# ------------------------------------------------------------------
# Số hỗ trợ. HÃY KIỂM TRA LẠI trước khi triển khai thật cho học sinh.
# ------------------------------------------------------------------
RESOURCES = [
    {
        "name": "Tổng đài quốc gia bảo vệ trẻ em",
        "number": "111",
        "note": "Miễn phí, 24/7, dành cho trẻ em",
    },
    {
        "name": "Cấp cứu",
        "number": "115",
        "note": "Khi bạn hoặc ai đó đang gặp nguy hiểm ngay lúc này",
    },
]


# ------------------------------------------------------------------
# Xử lý văn bản
# ------------------------------------------------------------------
def _strip(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.replace("đ", "d").replace("Đ", "D")


def _normalize(text):
    text = unicodedata.normalize("NFC", text).lower()
    return re.sub(r"\s+", " ", text).strip()


def _diacritic_ratio(norm):
    words = re.findall(r"\w+", norm)
    if not words:
        return 1.0
    return sum(1 for w in words if _strip(w) != w) / len(words)


_PUNCT = re.compile(r"[,.;:!?…\n()]")


def _before(text, start, n):
    tail = _PUNCT.split(text[:start])[-1]
    return re.findall(r"\w+", tail)[-n:]


def _after(text, end, n):
    head = _PUNCT.split(text[end:])[0]
    return re.findall(r"\w+", head)[:n]


def _both(words):
    """Trả về tập gồm cả dạng có dấu và không dấu."""
    return {w for w in words} | {_strip(w) for w in words}


# ------------------------------------------------------------------
# Từ điển cụm từ
# ------------------------------------------------------------------
HIGH_PHRASES = [
    "tự tử", "tự sát", "muốn chết", "không muốn sống", "chán sống",
    "không muốn tồn tại", "muốn biến mất", "biến mất khỏi thế giới",
    "kết thúc cuộc đời", "kết thúc cuộc sống", "kết thúc tất cả",
    "chấm dứt cuộc đời", "chết đi cho rồi", "ước gì mình chết",
    "ước mình chết", "không muốn thức dậy nữa", "không muốn tỉnh dậy",
    "không còn lý do để sống", "không đáng sống", "sống không còn ý nghĩa",
    "tự làm đau", "tự làm hại", "tự hại", "làm hại bản thân",
    "rạch tay", "cắt tay", "nhảy lầu",
    "không có mình thì tốt hơn", "mọi người sẽ tốt hơn nếu không có",
]

# Cụm này khi gõ không dấu dễ trùng với từ khác ("từ từ"), nên chỉ dùng
# các dạng dài hơn ở chế độ không dấu.
STRIPPED_ONLY_PHRASES = [
    "muon tu tu", "nghi den tu tu", "nghi toi tu tu", "dinh tu tu", "se tu tu",
]
STRIPPED_SKIP = {"tu tu"}

ATTENTION_PHRASES = [
    "bắt nạt", "bạo hành", "bạo lực", "xâm hại", "quấy rối", "đe dọa",
    "bị đánh", "bị ép",
]

# Từ đứng ngay sau cụm làm cụm đó KHÔNG còn mang nghĩa nguy cơ.
NEXT_TOKEN_EXCLUDE = {
    "không muốn sống": {"ở", "cùng", "chung", "với", "tại", "trong", "gần", "xa"},
    "cắt tay": {"áo"},
    "bị đánh": {"giá", "trượt", "rớt", "bại", "bóng", "lừa"},
}

NEG_WORDS = _both(["không", "chẳng", "chả", "chưa", "đừng"])

# "mệt muốn chết", "buồn muốn chết"... thường chỉ là cách nói quá lời.
IDIOM_PREFIX = _both([
    "mệt", "đói", "buồn", "ngại", "xấu", "hổ", "sợ", "chán", "nóng", "lạnh",
    "ngủ", "khổ", "cực", "bực", "tức", "đau", "nhức", "lo", "stress",
    "căng", "thẳng", "mỏi", "chịu", "lực", "thèm", "cười",
])
IDIOM_PHRASES = {"muốn chết"}


# ------------------------------------------------------------------
# Thông điệp
# ------------------------------------------------------------------
def _resources_text():
    lines = [f"- **{r['name']} {r['number']}**: {r['note']}" for r in RESOURCES]
    return "\n".join(lines)


MESSAGES = {
    "high": {
        "title": "Mình rất quan tâm đến điều bạn vừa chia sẻ",
        "body": (
            "Có vẻ bạn đang rất đau và mệt mỏi. Bạn không cần phải chịu đựng "
            "điều này một mình.\n\n"
            "Hãy nói ngay với một người lớn bạn tin tưởng (bố mẹ, thầy cô, "
            "người thân) hoặc người đang ở gần bạn.\n\n"
        ),
        "tail": (
            "\n\nSerenWize-AI chỉ là công cụ hỗ trợ, không thay thế người thật "
            "hay chuyên gia."
        ),
        "short": "Hãy nói chuyện với một người lớn bạn tin tưởng ngay hôm nay. Bạn không phải một mình.",
    },
    "attention": {
        "title": "Điều bạn kể nghe có thể là một tình huống không an toàn",
        "body": (
            "Bạn không có lỗi khi bị đối xử như vậy. Hãy chia sẻ với một người "
            "lớn bạn tin tưởng như thầy cô, bố mẹ hoặc người thân.\n\n"
        ),
        "tail": "",
        "short": "Hãy chia sẻ với một người lớn bạn tin tưởng như thầy cô, bố mẹ hoặc người thân.",
    },
    "check_in": {
        "title": "Mình hỏi thăm bạn một chút nhé",
        "body": (
            "Có vẻ bạn đang rất mệt mỏi. Nếu đó chỉ là cách nói thì không sao. "
            "Nhưng nếu đôi khi bạn có suy nghĩ không muốn sống nữa, hãy chia sẻ "
            "với người lớn bạn tin tưởng.\n\n"
        ),
        "tail": "",
        "short": "Nếu bạn đang rất mệt mỏi, hãy chia sẻ với một người bạn tin tưởng.",
    },
}

_SEVERITY = {"none": 0, "check_in": 1, "attention": 2, "high": 3}


def _build(level, matched):
    if level == "none":
        return {"level": "none", "matched": [], "title": "", "message": "",
                "short_message": "", "resources": []}
    m = MESSAGES[level]
    return {
        "level": level,
        "matched": matched,
        "title": m["title"],
        "message": m["body"] + _resources_text() + m["tail"],
        "short_message": m["short"],
        "resources": RESOURCES,
    }


# ------------------------------------------------------------------
# Phát hiện
# ------------------------------------------------------------------
def _find(text, phrase):
    pattern = r"(?<!\w)" + re.escape(phrase) + r"(?!\w)"
    return [m.span() for m in re.finditer(pattern, text)]


def _scan(text, phrases, level, stripped_mode, found):
    for phrase in phrases:
        key = _strip(phrase) if stripped_mode else phrase
        if stripped_mode and key in STRIPPED_SKIP:
            continue
        for start, end in _find(text, key):
            nxt = _after(text, end, 1)
            excl = NEXT_TOKEN_EXCLUDE.get(phrase, set())
            if nxt and (nxt[0] in excl or _strip(nxt[0]) in excl):
                continue

            before = _before(text, start, 2)
            starts_negative = phrase.startswith("không")
            if not starts_negative and any(t in NEG_WORDS for t in before):
                continue

            this_level = level
            if phrase in IDIOM_PHRASES and any(t in IDIOM_PREFIX for t in before):
                this_level = "check_in"

            found.append((this_level, phrase))


def detect_crisis(text):
    """
    Trả về dict: level, matched, title, message, short_message, resources.
    """
    if not isinstance(text, str) or not text.strip():
        return _build("none", [])

    norm = _normalize(text)
    stripped = _strip(norm)
    use_stripped = _diacritic_ratio(norm) < 0.5

    found = []
    _scan(norm, HIGH_PHRASES, "high", False, found)
    _scan(norm, ATTENTION_PHRASES, "attention", False, found)

    if use_stripped:
        _scan(stripped, HIGH_PHRASES, "high", True, found)
        _scan(stripped, ATTENTION_PHRASES, "attention", True, found)
        for phrase in STRIPPED_ONLY_PHRASES:
            if _find(stripped, phrase):
                found.append(("high", phrase))

    if not found:
        return _build("none", [])

    level = max((lv for lv, _ in found), key=lambda lv: _SEVERITY[lv])
    matched = []
    for lv, ph in found:
        if lv == level and ph not in matched:
            matched.append(ph)
    return _build(level, matched)


# ------------------------------------------------------------------
# Hiển thị trong Streamlit
# ------------------------------------------------------------------
def show_crisis_banner(crisis):
    """Hiện khung quan tâm nếu có tín hiệu. Không làm gì nếu level = none."""
    if not crisis or crisis.get("level", "none") == "none":
        return

    import streamlit as st

    text = f"**💜 {crisis['title']}**\n\n{crisis['message']}"
    if crisis["level"] == "high":
        st.error(text)
    else:
        st.warning(text)
        
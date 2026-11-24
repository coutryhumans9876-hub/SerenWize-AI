"""
SerenWize-AI - Đối chiếu 3 nguồn để ước lượng cảm xúc:
  1. Giọng điệu hiện tại  (kết quả MERaLiON theo từng đoạn)
  2. Nội dung lời nói     (văn bản -> analyze_text)
  3. Độ lệch so với giọng gốc (compare_voice)

Đây là ước lượng dựa trên quy tắc, KHÔNG phải chẩn đoán tâm lý.
"""

CATEGORIES = ["Vui vẻ", "Bình thường", "Buồn bã", "Lo lắng", "Căng thẳng", "Tức giận"]
NEGATIVE = {"Buồn bã", "Lo lắng", "Căng thẳng", "Tức giận"}
HIGH_AROUSAL = {"Vui vẻ", "Lo lắng", "Căng thẳng", "Tức giận"}
LOW_AROUSAL = {"Bình thường", "Buồn bã"}

# Nhãn MERaLiON -> (nhãn của app, hệ số tin cậy). None = bỏ qua.
VOICE_MAP = {
    "Happy": ("Vui vẻ", 1.0),
    "Neutral": ("Bình thường", 1.0),
    "Sad": ("Buồn bã", 1.0),
    "Angry": ("Tức giận", 1.0),
    "Fearful": ("Lo lắng", 1.0),
    "Disgusted": ("Tức giận", 0.6),
    "Surprised": None,
    "Uncertain": None,
}

W_VOICE = 0.55
W_TEXT = 0.45


def _normalize(d):
    total = sum(d.values())
    if total <= 0:
        return {}
    return {k: v / total for k, v in d.items()}


def voice_distribution(emotion_result):
    """Phân bố cảm xúc từ các đoạn MERaLiON, có trọng số theo độ tin cậy và độ dài đoạn."""
    if not isinstance(emotion_result, dict) or not emotion_result.get("success"):
        return {}, []
    scores, trend = {}, []
    for seg in emotion_result.get("segments", []) or []:
        label = seg.get("emotion", "Uncertain")
        conf = float(seg.get("confidence", 0) or 0)
        length = max(float(seg.get("end_time", 0) or 0) - float(seg.get("start_time", 0) or 0), 0.0)
        mapped = VOICE_MAP.get(label)
        trend.append((seg.get("start_time", 0), seg.get("end_time", 0), mapped[0] if mapped else None, conf))
        if mapped:
            scores[mapped[0]] = scores.get(mapped[0], 0.0) + conf * mapped[1] * max(length, 1.0)
    return _normalize(scores), trend


def text_distribution(text_result):
    if not isinstance(text_result, dict):
        return {}
    primary = text_result.get("emotion")
    scores = {}
    if primary in CATEGORIES:
        scores[primary] = 1.0
    for e in text_result.get("emotions", []) or []:
        if e in CATEGORIES and e not in scores:
            scores[e] = 0.5
    return _normalize(scores)


def baseline_shift(comparison_result):
    """Trả về (độ lệch 0..1, hướng kích thích -1..1) hoặc (None, None)."""
    if not isinstance(comparison_result, dict) or not comparison_result.get("success"):
        return None, None
    comps = comparison_result.get("comparisons", {})
    devs, signed = [], []
    for key in ("pitch_mean", "rms_mean", "zcr_mean", "centroid_mean"):
        item = comps.get(key)
        if not item or item.get("percent_change") is None:
            continue
        pc = max(-50.0, min(50.0, float(item["percent_change"]))) / 50.0
        devs.append(abs(pc))
        if key in ("pitch_mean", "rms_mean"):
            signed.append(pc)
    if not devs:
        return None, None
    return sum(devs) / len(devs), (sum(signed) / len(signed) if signed else 0.0)


def _trend_text(trend):
    labels = [t[2] for t in trend if t[2]]
    if len(labels) < 2:
        return None
    half = len(labels) // 2
    first = max(set(labels[:half]), key=labels[:half].count)
    last = max(set(labels[half:]), key=labels[half:].count)
    if first != last:
        return f"Giọng điệu có xu hướng chuyển từ **{first}** sang **{last}** trong bản ghi."
    return None


def fuse(emotion_result, text_result=None, comparison_result=None):
    """Kết hợp 3 nguồn. Trả về dict kết quả có kèm lời giải thích."""
    V, trend = voice_distribution(emotion_result)
    T = text_distribution(text_result)
    dev, arousal = baseline_shift(comparison_result)

    explain, used = [], []
    if not V and not T:
        return {"success": False, "error": "Chưa đủ dữ liệu để đối chiếu (thiếu kết quả giọng điệu và nội dung)."}

    wv, wt = (W_VOICE if V else 0.0), (W_TEXT if T else 0.0)
    total_w = wv + wt
    scores = {c: (wv * V.get(c, 0) + wt * T.get(c, 0)) / total_w for c in CATEGORIES}

    v_top = max(V, key=V.get) if V else None
    t_top = max(T, key=T.get) if T else None
    if V:
        used.append("giọng điệu (MERaLiON)")
        explain.append(f"Giọng điệu nghiêng về **{v_top}** ({V[v_top]*100:.0f}% số đoạn có trọng số).")
    if T:
        used.append("nội dung lời nói")
        explain.append(f"Nội dung lời nói nghiêng về **{t_top}**.")

    if dev is not None:
        used.append("so sánh với giọng gốc")
        if dev >= 0.2 and arousal is not None and abs(arousal) >= 0.15:
            boost = 1 + 0.5 * min(abs(arousal), 1.0)
            targets = HIGH_AROUSAL if arousal > 0 else LOW_AROUSAL
            for c in targets:
                scores[c] *= boost
            direction = "cao hơn" if arousal > 0 else "thấp hơn"
            explain.append(f"Cao độ/âm lượng {direction} đáng kể so với giọng bình thường của bạn "
                           f"(độ lệch trung bình {dev*100:.0f}%).")
        else:
            explain.append("Đặc trưng giọng nói gần với giọng bình thường của bạn.")
    scores = _normalize(scores)
    top = max(scores, key=scores.get)

    mismatch = bool(v_top and t_top and v_top != t_top and (v_top in NEGATIVE or t_top in NEGATIVE))
    if v_top and t_top:
        level = "Cao" if v_top == t_top else "Thấp"
    else:
        vconf = float(emotion_result.get("overall_confidence", 0) or 0) if V else 0
        level = "Trung bình" if vconf >= 0.6 else "Thấp"
    if V and float(emotion_result.get("overall_confidence", 1) or 0) < 0.5 and level == "Cao":
        level = "Trung bình"

    if mismatch:
        explain.append("Nội dung và giọng điệu chưa khớp nhau, nên kết quả chỉ mang tính tham khảo. "
                       "Bạn có thể chia sẻ thêm với người mình tin tưởng.")
    t = _trend_text(trend)
    if t:
        explain.append(t)

    return {
        "success": True,
        "emotion": top,
        "confidence_level": level,
        "scores": dict(sorted(scores.items(), key=lambda kv: -kv[1])),
        "mismatch": mismatch,
        "sources": used,
        "explanations": explain,
        "limitation": "Đây là ước lượng từ mô hình AI và quy tắc đối chiếu, không phải chẩn đoán tâm lý.",
    }
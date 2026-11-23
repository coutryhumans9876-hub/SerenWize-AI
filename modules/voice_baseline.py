
import json
import os
import numpy as np


BASELINE_PATH = "data/voice_baseline.json"


def summarize_emotion_results(emotion_results):
    """
    Tổng hợp phân bố cảm xúc từ nhiều mẫu ghi âm.

    Tính theo thời lượng các đoạn hợp lệ.
    Loại bỏ đoạn Uncertain và low_vad.
    """

    emotion_duration = {}
    total_duration = 0.0
    confidence_total = 0.0
    confidence_duration = 0.0
    valid_samples = 0

    for result in emotion_results:

        if not result or not result.get("success"):
            continue

        valid_samples += 1

        for segment in result.get("segments", []):

            emotion = segment.get("emotion", "Uncertain")

            if emotion == "Uncertain":
                continue

            if segment.get("low_vad", False):
                continue

            try:
                start = float(segment["start_time"])
                end = float(segment["end_time"])
                confidence = float(segment["confidence"])
            except (KeyError, TypeError, ValueError):
                continue

            duration = end - start

            if (
                duration <= 0
                or not np.isfinite(duration)
                or not np.isfinite(confidence)
            ):
                continue

            emotion_duration[emotion] = (
                emotion_duration.get(emotion, 0.0) + duration
            )

            total_duration += duration
            confidence_total += confidence * duration
            confidence_duration += duration

    if total_duration <= 0:
        return None

    distribution = {
        emotion: duration / total_duration
        for emotion, duration in emotion_duration.items()
    }

    average_confidence = (
        confidence_total / confidence_duration
        if confidence_duration > 0
        else None
    )

    return {
        "sample_count": valid_samples,
        "emotion_distribution": distribution,
        "average_confidence": average_confidence,
        "valid_audio_duration": total_duration
    }

def create_baseline(voice_results, emotion_results=None):
    """
    Tạo hồ sơ giọng nói cá nhân từ nhiều mẫu ghi âm.
    """

    if not voice_results:
        return {
            "success": False,
            "error": "Chưa có dữ liệu ghi âm."
        }

    features = [
        "pitch_mean",
        "rms_mean",
        "zcr_mean",
        "centroid_mean"
    ]

    baseline = {}

    try:
        for feature in features:

            values = [
                float(result[feature])
                for result in voice_results
                if result.get(feature) is not None
            ]

            if not values:
                return {
                    "success": False,
                    "error": f"Thiếu dữ liệu {feature}."
                }

            baseline[feature] = float(np.mean(values))

        mfcc_values = [
            result["mfcc_mean"]
            for result in voice_results
            if result.get("mfcc_mean") is not None
        ]

        if mfcc_values:
            baseline["mfcc_mean"] = np.mean(
                mfcc_values,
                axis=0
            ).tolist()
                    # Tạo hồ sơ cảm xúc MERaLiON
        if emotion_results is not None:

            emotion_result = create_emotion_baseline(
                emotion_results
            )

            if not emotion_result.get("success"):
                return {
                    "success": False,
                    "error": emotion_result.get(
                        "error",
                        "Không thể tạo hồ sơ cảm xúc."
                    )
                }

            baseline["emotion_baseline"] = (
                emotion_result["baseline"]
            )

        # Tạo hồ sơ cảm xúc MERaLiON
        if emotion_results:
            emotion_baseline = summarize_emotion_results(
                emotion_results
            )

            if emotion_baseline is not None:
                baseline["emotion_baseline"] = emotion_baseline

        os.makedirs("data", exist_ok=True)

        with open(
            BASELINE_PATH,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                baseline,
                file,
                ensure_ascii=False,
                indent=4
            )

        return {
            "success": True,
            "baseline": baseline
        }

    except (KeyError, TypeError, ValueError) as error:
        return {
            "success": False,
            "error": str(error)
        }


def load_baseline():
    """Đọc hồ sơ giọng nói đã lưu."""

    if not os.path.exists(BASELINE_PATH):
        return None

    with open(
        BASELINE_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def create_emotion_baseline(emotion_results):
    """
    Tạo hồ sơ cảm xúc cá nhân từ nhiều bản ghi MERaLiON.

    Bỏ qua đoạn Uncertain và đoạn có low_vad = True.
    Mỗi bản ghi có trọng số ngang nhau khi tổng hợp.
    """

    if not emotion_results:
        return {
            "success": False,
            "error": "Chưa có dữ liệu cảm xúc."
        }

    sample_distributions = []
    sample_confidences = []

    try:
        for result in emotion_results:

            if not isinstance(result, dict):
                continue

            if not result.get("success"):
                continue

            segments = result.get("segments", [])

            emotion_weights = {}
            total_weight = 0.0
            confidence_values = []

            for segment in segments:

                if not isinstance(segment, dict):
                    continue

                if segment.get("low_vad") is True:
                    continue

                emotion = segment.get("emotion")

                if not emotion or emotion == "Uncertain":
                    continue

                confidence = float(segment.get("confidence", 0))

                start_time = float(segment.get("start_time", 0))
                end_time = float(segment.get("end_time", 0))

                duration = end_time - start_time

                if (
                    not np.isfinite(confidence)
                    or not np.isfinite(duration)
                    or confidence <= 0
                    or duration <= 0
                ):
                    continue

                weight = duration * confidence

                emotion_weights[emotion] = (
                    emotion_weights.get(emotion, 0.0) + weight
                )

                total_weight += weight
                confidence_values.append((confidence, duration))

            if total_weight <= 0:
                continue

            distribution = {
                emotion: weight / total_weight
                for emotion, weight in emotion_weights.items()
            }

            sample_confidence = sum(
                confidence * duration
                for confidence, duration in confidence_values
            ) / sum(
                duration
                for _, duration in confidence_values
            )

            sample_distributions.append(distribution)
            sample_confidences.append(sample_confidence)

        if not sample_distributions:
            return {
                "success": False,
                "error": "Không có bản ghi cảm xúc hợp lệ."
            }

        all_emotions = set()

        for distribution in sample_distributions:
            all_emotions.update(distribution.keys())

        emotion_distribution = {
            emotion: float(
                np.mean([
                    distribution.get(emotion, 0.0)
                    for distribution in sample_distributions
                ])
            )
            for emotion in all_emotions
        }

        return {
            "success": True,
            "baseline": {
                "sample_count": len(sample_distributions),
                "emotion_distribution": emotion_distribution,
                "average_confidence": float(
                    np.mean(sample_confidences)
                )
            }
        }

    except (TypeError, ValueError, ZeroDivisionError) as error:
        return {
            "success": False,
            "error": str(error)
        }

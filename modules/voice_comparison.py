
import numpy as np


def compare_voice(current_result, baseline):
    """
    So sánh đặc trưng giọng nói hiện tại với hồ sơ
    giọng nói bình thường của cùng một người.

    Không chẩn đoán cảm xúc hoặc bệnh lý.
    """

    if not current_result or not baseline:
        return {
            "success": False,
            "error": "Thiếu dữ liệu giọng nói để so sánh."
        }

    features = {
        "pitch_mean": "Cao độ trung bình",
        "rms_mean": "Năng lượng RMS",
        "zcr_mean": "Zero Crossing Rate",
        "centroid_mean": "Spectral Centroid"
    }

    comparisons = {}

    try:
        for feature, label in features.items():

            baseline_value = float(baseline[feature])
            current_value = float(current_result[feature])

            if not np.isfinite(baseline_value) or not np.isfinite(current_value):
                raise ValueError(f"Dữ liệu {label} không hợp lệ.")

            difference = current_value - baseline_value

            if abs(baseline_value) < 1e-10:
                percent_change = None
            else:
                percent_change = (
                    difference / abs(baseline_value)
                ) * 100

            comparisons[feature] = {
                "label": label,
                "baseline": baseline_value,
                "current": current_value,
                "difference": difference,
                "percent_change": percent_change
            }

        # So sánh MFCC nếu cả hai bên đều có dữ liệu
        baseline_mfcc = baseline.get("mfcc_mean")
        current_mfcc = current_result.get("mfcc_mean")

        mfcc_difference = None

        if baseline_mfcc and current_mfcc:

            baseline_array = np.array(
                baseline_mfcc,
                dtype=float
            )

            current_array = np.array(
                current_mfcc,
                dtype=float
            )

            if baseline_array.shape != current_array.shape:
                raise ValueError("Số lượng hệ số MFCC không khớp.")

            mfcc_difference = float(
                np.mean(np.abs(current_array - baseline_array))
            )

        return {
            "success": True,
            "comparisons": comparisons,
            "mfcc_mean_absolute_difference": mfcc_difference,
            "message": (
                "Đã hoàn thành so sánh đặc trưng giọng nói."
            )
        }

    except (KeyError, TypeError, ValueError) as error:

        return {
            "success": False,
            "error": str(error)
        }

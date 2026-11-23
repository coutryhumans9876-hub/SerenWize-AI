
import json
import os
from datetime import datetime


HISTORY_PATH = "data/recovery_history.json"


def save_recovery_session(
    feeling,
    intensity_before,
    need,
    activity,
    intensity_after,
    feedback
):
    """
    Lưu thông tin tự đánh giá trước và sau bài tập.
    Không lưu bản ghi âm hoặc thông tin định danh.
    """

    try:
        os.makedirs("data", exist_ok=True)

        session = {
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "feeling": feeling,
            "intensity_before": int(intensity_before),
            "need": need,
            "activity": activity,
            "intensity_after": int(intensity_after),
            "feedback": feedback
        }

        history = load_recovery_history()

        history.append(session)

        with open(
            HISTORY_PATH,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                history,
                file,
                ensure_ascii=False,
                indent=4
            )

        return {
            "success": True,
            "message": "Đã lưu lịch sử phục hồi."
        }

    except (OSError, TypeError, ValueError) as error:
        return {
            "success": False,
            "error": str(error)
        }


def load_recovery_history():
    """Đọc lịch sử phục hồi đã lưu."""

    if not os.path.exists(HISTORY_PATH):
        return []

    try:
        with open(
            HISTORY_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            history = json.load(file)

        return history if isinstance(history, list) else []

    except (OSError, json.JSONDecodeError):
        return []

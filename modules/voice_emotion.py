
import base64
import requests
import streamlit as st


API_URL = "https://api.meralion.ai/v1/audio/emotion_gender"


def analyze_voice_emotion(audio_path):
    """
    Gửi tệp WAV đến MERaLiON để nhận diện cảm xúc giọng nói.
    Trả về cảm xúc tổng thể và kết quả từng đoạn.
    """

    try:
        # Lấy API key từ secrets.toml
        api_key = st.secrets["MERALION_API_KEY"]

        # Đọc âm thanh và chuyển thành Base64
        with open(audio_path, "rb") as audio_file:
            audio_b64 = base64.b64encode(
                audio_file.read()
            ).decode("utf-8")

        # Gửi yêu cầu đến MERaLiON
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "audio_url": audio_b64,
            "filename": "voice.wav",
            "segment_length": 4,
            "confidence_threshold": 0.1,
            "vad_threshold": 0.3,
            "post_process": True,
            "er_len_threshold": 5000,
            "gr_len_threshold": 5000,
            "emotion_confidence_threshold": 0.4
        }

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=120
        )

        response.raise_for_status()
        result = response.json()

        if not result.get("success"):
            return {
                "success": False,
                "error": result.get(
                    "message",
                    "MERaLiON không phân tích được âm thanh."
                )
            }

        return result

    except KeyError:
        return {
            "success": False,
            "error": "Không tìm thấy MERALION_API_KEY trong secrets.toml."
        }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "API phản hồi quá lâu. Hãy thử lại."
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Lỗi kết nối MERaLiON: {str(e)}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Lỗi phân tích: {str(e)}"
        }

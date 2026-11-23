
import numpy as np
import librosa


def analyze_audio(audio_file):
    """
    Trích xuất đặc trưng âm thanh từ tệp ghi âm.
    Chưa thực hiện chẩn đoán hoặc phân loại cảm xúc.
    """

    try:
        # Đọc tệp âm thanh
        y, sr = librosa.load(
            audio_file,
            sr=22050,
            mono=True
        )

        # Kiểm tra dữ liệu
        if len(y) == 0:
            raise ValueError("Tệp âm thanh không có dữ liệu.")

        duration = librosa.get_duration(
            y=y,
            sr=sr
        )

        # 1. Cao độ Pitch
        pitch = librosa.yin(
            y,
            fmin=65,
            fmax=500,
            sr=sr
        )

        valid_pitch = pitch[
            np.isfinite(pitch)
        ]

        valid_pitch = valid_pitch[
            (valid_pitch >= 65) &
            (valid_pitch <= 500)
        ]

        mean_pitch = (
            float(np.mean(valid_pitch))
            if len(valid_pitch) > 0
            else 0.0
        )

        # 2. Năng lượng âm thanh RMS
        rms = librosa.feature.rms(y=y)[0]

        mean_rms = float(np.mean(rms))

        # 3. Zero Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]

        mean_zcr = float(np.mean(zcr))

        # 4. Spectral Centroid
        centroid = librosa.feature.spectral_centroid(
            y=y,
            sr=sr
        )[0]

        mean_centroid = float(np.mean(centroid))

        # 5. MFCC
        mfcc = librosa.feature.mfcc(
            y=y,
            sr=sr,
            n_mfcc=13
        )

        mean_mfcc = np.mean(
            mfcc,
            axis=1
        )

        # Trả về kết quả
        return {
            "success": True,
            "duration": round(float(duration), 2),
            "pitch_mean": round(mean_pitch, 2),
            "rms_mean": round(mean_rms, 4),
            "zcr_mean": round(mean_zcr, 4),
            "centroid_mean": round(mean_centroid, 2),
            "mfcc_mean": [
                round(float(value), 4)
                for value in mean_mfcc
            ],
            "message": "Trích xuất đặc trưng âm thanh thành công."
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
            "message": "Không thể xử lý tệp âm thanh."
        }

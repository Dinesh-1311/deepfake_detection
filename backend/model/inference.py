import torch
import numpy as np
import torch.nn as nn
from pathlib import Path
from backend.utils.preprocess import preprocess_audio
from backend.utils.loader import load_model
from backend.utils.audio import extract_audio_from_video, reduce_noise


def predict_deepfake(file_path: str, model_type: str) -> dict:
    try:
        suffix = Path(file_path).suffix.lower()

        # Step 1: If video, extract audio
        if suffix in [".mp4", ".mov"]:
            audio_path = str(Path(file_path).with_suffix(".wav"))
            extract_audio_from_video(file_path, audio_path)
            file_path = audio_path  # use the extracted .wav

        # Step 2: Load model
        model, input_type = load_model(model_type)
        model.eval()

        # Step 3: Preprocess input
        x = preprocess_audio(file_path, input_type)

        # Step 4: Optional noise reduction
        if input_type == "raw" and x.ndim == 2:  # raw waveform
            x = reduce_noise(x)

        if isinstance(x, np.ndarray):
            x = torch.from_numpy(x)
        if x.ndim == 1:
            x = x.unsqueeze(0)
        elif x.ndim == 2 and x.shape[0] != 1:
            x = x.unsqueeze(0)

        # Step 5: Predict
        with torch.no_grad():
            output = model(x)

            if model_type == "wav2vec":
                prob = output.item()
                prediction = "REAL" if prob >= 0.5 else "FAKE"
                confidence = prob if prediction == "REAL" else 1 - prob

            elif model_type == "lstm":
                prob = torch.sigmoid(output).item()
                prediction = "REAL" if prob > 0.5 else "FAKE"
                confidence = prob if prediction == "REAL" else 1 - prob

            else:
                probs = torch.nn.functional.softmax(output, dim=1).squeeze().cpu().numpy()
                predicted_class = np.argmax(probs)
                prediction = "REAL" if predicted_class == 0 else "FAKE"
                confidence = float(probs[predicted_class])

        return {
            "prediction": prediction,
            "confidence": f"{round(confidence * 100, 2)}%"
        }

    except Exception as e:
        return {"error": f"Inference failed: {str(e)}"}


# -------------------------
# (Optional) Redundant model classes (can be removed if unused)
# -------------------------

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.net(x)


class CRNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.net(x)


class Wav2VecClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.net(x)

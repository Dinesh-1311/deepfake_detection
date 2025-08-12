import torch
import numpy as np
import torch.nn as nn
from backend.utils.preprocess import preprocess_audio
from backend.utils.loader import load_model

# -------------------------
# Main prediction function
# -------------------------
def predict_deepfake(file_path: str, model_type: str) -> dict:
    try:
        # Load model and input type
        model, input_type = load_model(model_type)
        model.eval()

        # Preprocess the input
        x = preprocess_audio(file_path, input_type)
        if isinstance(x, np.ndarray):
            x = torch.from_numpy(x)
        if x.ndim == 1:
            x = x.unsqueeze(0)  # (1, features)
        elif x.ndim == 2 and x.shape[0] != 1:
            x = x.unsqueeze(0)  # add batch dim if needed

        with torch.no_grad():
            output = model(x)

            if model_type == "wav2vec":
                # Binary classifier already includes sigmoid in final layer
                prob = output.item()
                prediction = "REAL" if prob >= 0.5 else "FAKE"
                confidence = prob if prediction == "REAL" else 1 - prob

            elif model_type == "lstm":
                # Binary classifier: output is raw logit, apply sigmoid here
                prob = torch.sigmoid(output).item()
                prediction = "REAL" if prob > 0.5 else "FAKE"
                confidence = prob if prediction == "REAL" else 1 - prob


            else:
                # Multi-class classifier with softmax
                probs = torch.nn.functional.softmax(output, dim=1).squeeze().cpu().numpy()
                predicted_class = np.argmax(probs)
                prediction = "REAL" if predicted_class == 0 else "FAKE"
                confidence = float(probs[predicted_class])

        return {
            "prediction": prediction,
            "confidence": f"{round(confidence * 100, 2)}%"
        }

    except Exception as e:
        return {"error": f"Failed to load model: {str(e)}"}

# -------------------------
# Model Definitions
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

# -------------------------
# Model path mapping
# -------------------------
MODEL_PATHS = {
    "cnn": "model/cnn_full.pt",
    "crnn": "model/crnn_full.pt",
    "wav2vec": "model/wav2vec_mlp.pt",
    "lstm": "model/wav2vec_lstm_balanced.pt"
}

# backend/model/inference.py
import torch
import numpy as np

from utils.loader import load_model
from utils.preprocess import preprocess_file


def predict_deepfake(file_path: str, model_type: str) -> dict:
    model, input_type = load_model(model_type)
    model.eval()

    # Preprocess input
    x = preprocess_file(file_path, input_type)
    x = torch.from_numpy(x).unsqueeze(0)  # Add batch dim

    with torch.no_grad():
        logits = model(x)
        probs = torch.nn.functional.softmax(logits, dim=1).squeeze().cpu().numpy()

    prediction = "REAL" if np.argmax(probs) == 0 else "FAKE"
    confidence = float(np.max(probs))

    return {
        "prediction": prediction,
        "confidence": round(confidence, 4)
    }

import torch
import torchaudio
import librosa
import numpy as np
import os

from utils.loader import load_model
from utils.preprocess import preprocess_audio

MODEL_PATHS = {
    "cnn": "models/cnn_model.pt",
    "crnn": "models/crnn_model.pt",
    "wav2vec": "models/wav2vec_model.pt"
}

def predict_deepfake(file_path: str, model_type: str):
    model_type = model_type.lower()

    if model_type not in MODEL_PATHS:
        return {"error": f"Model '{model_type}' not supported."}

    try:
        # Load model
        model = load_model(model_type, MODEL_PATHS[model_type])
        model.eval()

        # Preprocess input
        input_tensor = preprocess_audio(file_path, model_type)

        # Add batch dimension
        input_tensor = input_tensor.unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)
            probs = torch.softmax(output, dim=1).cpu().numpy()[0]
            predicted_class = int(np.argmax(probs))

        label = "REAL" if predicted_class == 0 else "FAKE"
        confidence = float(probs[predicted_class])

        return {
            "prediction": label,
            "confidence": round(confidence, 4)
        }

    except Exception as e:
        return {"error": str(e)}

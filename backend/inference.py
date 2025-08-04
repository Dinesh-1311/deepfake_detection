import torch
import numpy as np
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
        # Load model and input type (spectrogram/raw)
        model, input_type = load_model(model_type, MODEL_PATHS[model_type])
        model.eval()

        # Preprocess input
        input_tensor = preprocess_audio(file_path, input_type)

        # Add batch dimension
        input_tensor = input_tensor.unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)

            if model_type == "wav2vec":
                # Binary classification with sigmoid
                prob = torch.sigmoid(output).item()
                prediction = "REAL" if prob >= 0.5 else "FAKE"
                confidence = round(prob if prediction == "REAL" else 1 - prob, 4)
            else:
                # Multiclass (e.g. CNN/CRNN) with softmax
                probs = torch.softmax(output, dim=1).squeeze().cpu().numpy()
                predicted_class = int(np.argmax(probs))
                prediction = "REAL" if predicted_class == 0 else "FAKE"
                confidence = round(float(probs[predicted_class]), 4)

        return {
            "prediction": prediction,
            "confidence": confidence
        }

    except Exception as e:
        return {"error": f"Failed to load model: {str(e)}"}

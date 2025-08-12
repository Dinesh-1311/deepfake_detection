# backend/utils/loader.py
import torch
from backend.model.architecture import CNN, CRNN, Wav2VecClassifier, MODEL_PATHS, Wav2VecLSTMClassifier


def load_model(model_type: str):
    if model_type == "cnn":
        model = CNN()
        input_type = "spectrogram"
    elif model_type == "crnn":
        model = CRNN()
        input_type = "spectrogram"
    elif model_type == "wav2vec":
        model = Wav2VecClassifier()
        input_type = "raw"
    elif model_type == "lstm":
         model = Wav2VecLSTMClassifier()
         input_type = "raw"
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    try:
        model.load_state_dict(
            torch.load(MODEL_PATHS[model_type], map_location=torch.device("cpu"))
        )
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {e}")

    model.eval()
    return model, input_type

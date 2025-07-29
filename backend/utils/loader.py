import torch
from model.inference import CNN, CRNN, Wav2VecClassifier


def load_model(model_type: str, path: str):
    model = None
    if model_type == "cnn":
        model = CNN()
    elif model_type == "crnn":
        model = CRNN()
    elif model_type == "wav2vec":
        model = Wav2VecClassifier()
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    model.load_state_dict(torch.load(path, map_location=torch.device("cpu")))
    model.eval()
    return model

import os
import torch
import torchaudio
import librosa
import numpy as np
from torchvision import transforms

def load_audio(file_path, sr=16000):
    """
    Loads audio and returns waveform (Tensor) and sample rate.
    Converts to mono and resamples to 16kHz.
    """
    waveform, sample_rate = torchaudio.load(file_path)
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)  # mono
    if sample_rate != sr:
        waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=sr)(waveform)
    return waveform, sr

def extract_mel_spectrogram(file_path, n_mels=128, sr=16000, n_fft=1024, hop_length=512):
    """
    Loads audio and returns mel spectrogram (Tensor).
    """
    y, _ = librosa.load(file_path, sr=sr)
    mel_spec = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    mel_db = librosa.power_to_db(mel_spec, ref=np.max)
    mel_tensor = torch.tensor(mel_db).unsqueeze(0)  # shape: (1, mel, time)
    return mel_tensor

def prepare_input(file_path: str, model_type: str):
    """
    Routes audio preprocessing based on model type.
    Returns processed input tensor.
    """
    if model_type in ["cnn", "crnn"]:
        return extract_mel_spectrogram(file_path)
    elif model_type == "wav2vec":
        waveform, _ = load_audio(file_path)
        return waveform
    else:
        raise ValueError(f"Unknown model type: {model_type}")

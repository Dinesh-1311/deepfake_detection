import os
import torch
import torchaudio
import librosa
import numpy as np
from transformers import Wav2Vec2Processor, Wav2Vec2Model

# Constants
SAMPLE_RATE = 16000
N_MELS = 128
N_FFT = 1024
HOP_LENGTH = 512

# Global cache for model and processor
_processor = None
_model = None

def init_wav2vec():
    global _processor, _model
    if _processor is None:
        _processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
    if _model is None:
        _model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base")
        _model.eval()

def load_audio(file_path, sr=SAMPLE_RATE):
    """Load mono audio and resample to 16kHz."""
    waveform, original_sr = torchaudio.load(file_path)
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    if original_sr != sr:
        resampler = torchaudio.transforms.Resample(orig_freq=original_sr, new_freq=sr)
        waveform = resampler(waveform)
    return waveform, sr

def extract_mel_spectrogram(file_path):
    """Return mel spectrogram tensor for CNN/CRNN input."""
    y, _ = librosa.load(file_path, sr=SAMPLE_RATE)
    mel_spec = librosa.feature.melspectrogram(
        y=y, sr=SAMPLE_RATE, n_mels=N_MELS, n_fft=N_FFT, hop_length=HOP_LENGTH
    )
    mel_db = librosa.power_to_db(mel_spec, ref=np.max)
    mel_tensor = torch.tensor(mel_db).unsqueeze(0).float()  # (1, n_mels, time)
    return mel_tensor

def extract_wav2vec_features(file_path):
    """Return pooled Wav2Vec2 embeddings (1D tensor of size 768)."""
    global _processor, _model

    if _processor is None:
        _processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base")
    if _model is None:
        _model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base")
        _model.eval()

    waveform, _ = load_audio(file_path)

    # ✅ Apply VAD to remove silence/background
    try:
        from torchaudio.functional import vad
        waveform = waveform * (32768.0 / waveform.abs().max())  # Normalize for VAD
        vad_waveform = vad(waveform, sample_rate=SAMPLE_RATE)
        if vad_waveform.numel() > 0:
            waveform = vad_waveform
        else:
            print("⚠️ VAD removed all audio — using original waveform.")
    except Exception as e:
        print(f"⚠️ VAD failed: {e} — using original waveform.")

    input_values = _processor(
        waveform.squeeze().numpy(),
        return_tensors="pt",
        sampling_rate=SAMPLE_RATE
    ).input_values

    with torch.no_grad():
        hidden_states = _model(input_values).last_hidden_state
        pooled = hidden_states.mean(dim=1)  # (1, 768)

    return pooled.squeeze(0)  # shape: (768,)


def preprocess_audio(file_path: str, input_type: str) -> torch.Tensor:
    """
    Unified function to prepare model input.
    - For 'spectrogram': returns (1, mel, time)
    - For 'raw': returns (768,)
    """
    if input_type == "spectrogram":
        return extract_mel_spectrogram(file_path)
    elif input_type == "raw":
        return extract_wav2vec_features(file_path)
    else:
        raise ValueError(f"Unsupported input type: {input_type}")

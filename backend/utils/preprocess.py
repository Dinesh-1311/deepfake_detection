import os
import threading
import urllib.request
import torch
import torchaudio
import librosa
import numpy as np

# NOTE: we import transformers lazily inside init_wav2vec() so /health stays instant
# from transformers import Wav2Vec2Processor, Wav2Vec2Model  # <- moved inside

# Constants
SAMPLE_RATE = 16000
N_MELS = 128
N_FFT = 1024
HOP_LENGTH = 512
HF_MODEL_ID = "facebook/wav2vec2-base"

# Global cache for model and processor
_processor = None
_model = None
_init_lock = threading.Lock()

def _hf_reachable(timeout: float = 5.0) -> bool:
    """Quick connectivity check to avoid long hangs when offline or blocked."""
    try:
        urllib.request.urlopen("https://huggingface.co", timeout=timeout)
        return True
    except Exception:
        return False

def init_wav2vec():
    """
    Lazily initialize Wav2Vec2. This:
      - Avoids heavy imports at module load (so /health stays fast)
      - Checks HF reachability and fails fast instead of hanging
      - Uses a lock so multiple requests don’t double-initialize
      - Uses default HF cache (online), no local snapshot required
    """
    global _processor, _model

    if _processor is not None and _model is not None:
        return

    with _init_lock:
        if _processor is not None and _model is not None:
            return

        # Optional: enable faster downloader if installed (no harm if not)
        os.environ.setdefault("HF_HUB_ENABLE_HF_TRANSFER", "1")

        # Fail fast if HF is unreachable (prevents 30+ min hangs)
        if not _hf_reachable(timeout=5.0):
            raise RuntimeError(
                "Hugging Face is not reachable. Check your internet / firewall. "
                "Tried to load model online: facebook/wav2vec2-base"
            )

        # Lazy import so app startup is instant
        from transformers import Wav2Vec2Processor, Wav2Vec2Model

        # Online load (uses HF default cache under user profile)
        _processor = Wav2Vec2Processor.from_pretrained(
            HF_MODEL_ID,
            # cache_dir=None,            # default cache
            local_files_only=False,       # force online if not cached
            trust_remote_code=False
        )
        _model = Wav2Vec2Model.from_pretrained(
            HF_MODEL_ID,
            local_files_only=False,
            trust_remote_code=False
        )
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
    y, _ = librosa.load(file_path, sr=SAMPLE_RATE, mono=True)
    mel_spec = librosa.feature.melspectrogram(
        y=y, sr=SAMPLE_RATE, n_mels=N_MELS, n_fft=N_FFT, hop_length=HOP_LENGTH
    )
    mel_db = librosa.power_to_db(mel_spec, ref=np.max)
    mel_tensor = torch.tensor(mel_db, dtype=torch.float32).unsqueeze(0)  # (1, n_mels, time)
    return mel_tensor

def extract_wav2vec_features(file_path):
    """
    Return pooled Wav2Vec2 embeddings (1D tensor of size 768).
    Loads the model ONLINE via Hugging Face (cached under user profile).
    """
    global _processor, _model
    init_wav2vec()  # will raise fast if HF unreachable

    waveform, _ = load_audio(file_path)

    # Keep it simple & robust for testing: skip VAD to avoid edge-case stalls
    input_values = _processor(
        waveform.squeeze().numpy(),
        return_tensors="pt",
        sampling_rate=SAMPLE_RATE
    ).input_values

    with torch.no_grad():
        hidden_states = _model(input_values).last_hidden_state  # (1, T, 768)
        pooled = hidden_states.mean(dim=1)                      # (1, 768)

    return pooled.squeeze(0)  # shape: (768,)

def preprocess_audio(file_path: str, input_type: str) -> torch.Tensor:
    """
    Unified function to prepare model input.
    - For 'spectrogram': returns (1, mel, time)
    - For 'raw': returns (768,)
    """
    itype = (input_type or "").lower().strip()
    if itype == "spectrogram":
        return extract_mel_spectrogram(file_path)
    elif itype == "raw":
        return extract_wav2vec_features(file_path)
    else:
        raise ValueError(f"Unsupported input type: {input_type}")

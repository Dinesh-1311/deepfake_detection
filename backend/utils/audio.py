import subprocess
from pathlib import Path
import torchaudio
import torch
import noisereduce as nr

# Full path to your local ffmpeg.exe
FFMPEG_PATH = r"C:\Users\visha\Downloads\ffmpeg\ffmpeg\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"

def extract_audio_from_video(video_path: str, output_wav_path: str, sr: int = 16000):
    """
    Extract mono 16kHz WAV audio from a video file using ffmpeg.
    """
    command = [
        FFMPEG_PATH,
        "-y",                    # overwrite output file if exists
        "-i", video_path,       # input file
        "-vn",                  # no video
        "-acodec", "pcm_s16le", # audio codec: raw PCM
        "-ar", str(sr),         # sample rate
        "-ac", "1",             # mono channel
        output_wav_path         # output file
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print("FFmpeg error:", result.stderr.decode())  # Log to console
        raise RuntimeError(f"FFmpeg failed: {result.stderr.decode()}")


def reduce_noise(waveform, sr=16000):
    """
    Apply basic spectral gating noise reduction.
    """
    y = waveform.numpy().squeeze()
    y_denoised = nr.reduce_noise(y=y, sr=sr)
    return torch.tensor(y_denoised).unsqueeze(0)

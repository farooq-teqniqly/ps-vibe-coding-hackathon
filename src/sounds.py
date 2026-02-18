"""Play round result sounds: trumpet for win, splat for lose."""

import math
import os
import random
import struct
import sys
import wave


def _sounds_dir():
    """Directory for WAV files (project root / sounds)."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "sounds")
    os.makedirs(path, exist_ok=True)
    return path


def _write_wav(path: str, sample_rate: int, samples: list[int]) -> None:
    """Write 16-bit mono WAV from a list of sample values (-32768..32767)."""
    with wave.open(path, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        for s in samples:
            wav.writeframes(struct.pack("<h", max(-32768, min(32767, int(s)))))


def _ensure_trumpet_wav() -> str:
    """Generate a short fanfare WAV if missing; return path."""
    path = os.path.join(_sounds_dir(), "trumpet.wav")
    if os.path.isfile(path):
        return path
    rate = 22050
    # Short fanfare: ascending notes (C5, E5, G5, C6) with simple envelope
    freqs = [523, 659, 784, 1047]
    samples = []
    for freq in freqs:
        duration = 0.15
        n = int(rate * duration)
        for i in range(n):
            t = i / rate
            # Slight attack/decay per note
            env = 1.0
            if n > 0:
                if i < n * 0.1:
                    env = i / (n * 0.1)
                elif i > n * 0.7:
                    env = (n - i) / (n * 0.3)
            sample = 0.25 * 32767 * env * math.sin(2 * math.pi * freq * t)
            samples.append(int(sample))
        # Short gap
        for _ in range(int(rate * 0.03)):
            samples.append(0)
    _write_wav(path, rate, samples)
    return path


def _ensure_splat_wav() -> str:
    """Generate a short splat/thud WAV if missing; return path."""
    path = os.path.join(_sounds_dir(), "splat.wav")
    if os.path.isfile(path):
        return path
    rate = 22050
    duration = 0.25
    n = int(rate * duration)
    freq = 80
    samples = []
    for i in range(n):
        t = i / rate
        # Fast decay (thud)
        env = math.exp(-t * 15)
        # Mix in a bit of noise for "splat"
        noise = (random.random() - 0.5) * 8000 * env if i < n // 2 else 0
        sample = 0.4 * 32767 * env * math.sin(2 * math.pi * freq * t) + noise
        samples.append(int(sample))
    _write_wav(path, rate, samples)
    return path


def _play_wav(path: str) -> None:
    """Play WAV file. Uses winsound on Windows; no-op elsewhere."""
    if sys.platform == "win32":
        try:
            import winsound
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_NOSTOP)
        except Exception:
            pass
    else:
        # Optional: afplay on macOS, aplay on Linux
        try:
            import subprocess
            if sys.platform == "darwin":
                subprocess.run(["afplay", path], check=False, capture_output=True)
            else:
                subprocess.run(["aplay", "-q", path], check=False, capture_output=True)
        except Exception:
            pass


def play_win() -> None:
    """Play trumpet sound for a round win."""
    try:
        path = _ensure_trumpet_wav()
        _play_wav(path)
    except Exception:
        pass


def play_lose() -> None:
    """Play splat sound for a round loss."""
    try:
        path = _ensure_splat_wav()
        _play_wav(path)
    except Exception:
        pass

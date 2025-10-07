"""
speech_to_text.py
-----------------
Speech-to-text transcription using Meta's SeamlessM4T.
"""

import torch
import numpy as np
import pyaudio
from transformers import AutoProcessor, SeamlessM4Tv2Model

# Load model and processor (only once)
print("🔄 Loading SeamlessM4T model (this may take a few seconds)...")
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")

def record_audio(seconds: int = 5, rate: int = 16000):
    """Record audio from the system microphone."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate,
                    input=True, frames_per_buffer=1024)
    print(f"🎤 Recording for {seconds} seconds...")
    frames = [stream.read(1024) for _ in range(0, int(rate / 1024 * seconds))]
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Convert to float waveform
    audio_data = np.frombuffer(b"".join(frames), dtype=np.int16).astype(np.float32) / 32768.0
    return audio_data, rate

def transcribe_with_seamless():
    """Record user's speech and transcribe using SeamlessM4T."""
    audio_data, sample_rate = record_audio(seconds=5)
    print("🧠 Processing audio with SeamlessM4T...")

    inputs = processor(audios=audio_data, sampling_rate=sample_rate, return_tensors="pt")

    with torch.no_grad():
        output_tokens = model.generate(**inputs, task="asr")  # ASR = automatic speech recognition

    text = processor.decode(output_tokens[0].tolist()[0], skip_special_tokens=True)
    print(f"🗣️ Transcribed: {text}")
    return text

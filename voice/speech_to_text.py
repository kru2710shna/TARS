"""
speech_to_text.py
-----------------
Offline Speech-to-Text for TARS using Vosk.
"""

import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

# Path to the downloaded Vosk model
MODEL_PATH = os.path.join("models", "vosk-model-small-en-us-0.15")

# Lazy global cache
_model = None
_recognizer = None

def load_vosk():
    """Load the Vosk model once and keep in memory."""
    global _model, _recognizer
    if _model is None:
        print("🔄 Loading Vosk model (first time only)...")
        _model = Model(MODEL_PATH)
        _recognizer = KaldiRecognizer(_model, 16000)
        print("✅ Vosk model loaded successfully.")
    return _recognizer

def transcribe_with_vosk(seconds: int = 5):
    """Record microphone audio for `seconds` and transcribe using Vosk."""
    rec = load_vosk()
    rate = 16000
    chunk = 4000

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=rate,
                    input=True, frames_per_buffer=chunk)
    stream.start_stream()

    print(f"🎤 Recording for {seconds} seconds...")
    for _ in range(int(rate / chunk * seconds)):
        data = stream.read(chunk, exception_on_overflow=False)
        if len(data) == 0:
            continue
        rec.AcceptWaveform(data)

    result = json.loads(rec.FinalResult())
    stream.stop_stream()
    stream.close()
    p.terminate()

    text = result.get("text", "").strip()
    print(f"🗣️ Transcribed: {text}")
    return text

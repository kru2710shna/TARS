"""
text_to_speech.py
-----------------
TARS Voice Output Module using pyttsx3.
"""

import pyttsx3

def speak_text(text: str):
    """Convert text to speech using system TTS."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)     # speed (default ~200)
        engine.setProperty('volume', 1.0)   # volume (0.0–1.0)

        voices = engine.getProperty('voices')
        # Try to use a clear English voice
        for v in voices:
            if "Alex" in v.name or "Samantha" in v.name:
                engine.setProperty('voice', v.id)
                break

        print(f"🗣️ TARS speaking: {text}")
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        print("❌ TTS Error:", e)

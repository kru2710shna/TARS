"""
main.py
--------
T.A.R.S. Assistant: Wake Word → Speech-to-Text → Brain → (TTS)
"""

import os, time
from dotenv import load_dotenv
from wake_word.wake_word import WakeWordDetector
from voice.speech_to_text import transcribe_with_seamless
from brain.brain import process_command
from voice.text_to_speech import speak_text


load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")

def main():
    detector = WakeWordDetector(
        keyword_path="models/HEY-TARS_en_mac_v3_0_0.ppn",
        access_key=ACCESS_KEY
    )
    detector.setup()

    print("🤖 TARS is on standby. Say 'Hey TARS' to activate.")

    while True:
        if detector.listen():
            print("✅ Wake word detected! Activating assistant...")
            
            # Record & transcribe
            user_text = transcribe_with_seamless()
            print(f"🗣️ You said: {user_text}")

            # Send to brain
            response = process_command(user_text)
            print(f"🧠 TARS: {response}")
            speak_text(response)

            # Keep TARS active for 10 seconds before going back to listening
            print("🕐 TARS active for next 10 seconds...")
            time.sleep(10)

            print("😴 Deactivating. Waiting for 'Hey TARS' again...")

if __name__ == "__main__":
    main()

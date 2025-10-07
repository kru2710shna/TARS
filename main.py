"""
main.py
--------
T.A.R.S. Assistant: Wake Word → Speech-to-Text → Brain → (TTS)
"""

import os
from dotenv import load_dotenv
from wake_word.wake_word import WakeWordDetector
from voice.speech_to_text import transcribe_with_vosk
from voice.text_to_speech import speak_text
from brain.brain import process_command

load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")

def handle_command():
    """Capture, process, and respond once wake word triggers."""
    user_text = transcribe_with_vosk()
    print(f"🗣️ You said: {user_text}")

    response = process_command(user_text)
    print(f"🧠 TARS: {response}")
    speak_text(response)

    return response  # 👈 Return so main() can check for shutdown commands


def main():
    detector = WakeWordDetector(
        keyword_path="models/HEY-TARS_en_mac_v3_0_0.ppn",
        access_key=ACCESS_KEY
    )
    detector.setup()
    print("🤖 TARS is on standby. Say 'Hey TARS' to activate.")

    try:
        while True:
            if detector.listen():  # blocks until wake word
                print("✅ Wake word detected! Activating assistant...")
                response = handle_command()  # get the response text

                # 👇 Graceful shutdown trigger
                if "goodbye" in response.lower() or "deactivating" in response.lower():
                    print("🛑 Shutting down TARS...")
                    detector.cleanup()
                    break  # end the loop cleanly

                print("😴 Returning to standby...\n")
                detector.reset()  # reopen mic safely for next activation

    except KeyboardInterrupt:
        print("🛑 Exiting...")
    finally:
        detector.cleanup()


if __name__ == "__main__":
    main()

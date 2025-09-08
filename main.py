"""
main.py
--------
Main entry point for the T.A.R.S. Assistant (Wake Word → Assistant Pipeline)
"""

from wake_word.wake_word import WakeWordDetector
import os
from dotenv import load_dotenv

load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")

def main():
    detector = WakeWordDetector(
        keyword_path="models/HEY-TARS_en_mac_v3_0_0.ppn",
        access_key=ACCESS_KEY
    )
    detector.setup()
    if detector.listen():
        print("🔁 Wake word detected. Launching assistant...")

if __name__ == "__main__":
    main()

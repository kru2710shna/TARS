"""
wake_word.py
-------------
Wake Word Detection Module for T.A.R.S. Assistant
Uses Porcupine SDK to detect the phrase: "Hey TARS"
"""

import os
import struct
import pyaudio
import pvporcupine
from dotenv import load_dotenv

load_dotenv()
ACCESS_KEY = os.getenv("ACCESS_KEY")

KEYWORD_PATH = "models/HEY-TARS_en_mac_v3_0_0.ppn"

class WakeWordDetector:
    def __init__(self, keyword_path: str, access_key: str):
        self.keyword_path = keyword_path
        self.access_key = access_key
        self.porcupine = None
        self.pa = None
        self.audio_stream = None

    def setup(self):
        print("🔧 Initializing Porcupine...")
        self.porcupine = pvporcupine.create(
            access_key=self.access_key,
            keyword_paths=[self.keyword_path]
        )
        self.pa = pyaudio.PyAudio()
        self._open_stream()
        print("🟢 Wake word system ready. Say: 'Hey TARS'")

    def _open_stream(self):
        """(Re)open a new audio stream safely for macOS."""
        if self.audio_stream:
            try:
                self.audio_stream.stop_stream()
                self.audio_stream.close()
            except Exception:
                pass

        # Automatically select the correct mic
        input_device_index = 0  # ✅ MacBook Pro Microphone
        channels = 1            # ✅ confirmed from list_devices.py

        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=channels,
            format=pyaudio.paInt16,
            input=True,
            input_device_index=input_device_index,
            frames_per_buffer=self.porcupine.frame_length,
        )

    def listen(self):
        try:
            while True:
                pcm = self.audio_stream.read(
                    self.porcupine.frame_length, exception_on_overflow=False
                )
                pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                result = self.porcupine.process(pcm)
                if result >= 0:
                    print("✅ Wake word detected!")
                    return True
        except KeyboardInterrupt:
            print("🛑 Stopped by user.")
        except Exception as e:
            print("❌ Audio error:", e)
        finally:
            # Fully close stream to avoid CoreAudio error
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None
            print("🧹 Closed audio stream (ready to reopen).")

    def reset(self):
        """Reopen a fresh audio stream (safe on macOS)."""
        print("🔁 Resetting wake word system...")
        self._open_stream()
        print("🟢 Wake word listener restarted.")

    def cleanup(self):
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        if self.pa:
            self.pa.terminate()
        if self.porcupine:
            self.porcupine.delete()
        print("🧹 Cleaned up all audio resources.")

"""
brain.py
--------
TARS Brain Module — Processes user input and generates responses.
"""

from Utils.weather.weather import get_weather

def process_command(command: str) -> str:
    """
    Core logic for TARS' brain.
    In a real system, this could route to LLM, API, or internal logic.
    """
    command = command.lower()

    if "time" in command:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."

    elif "your name" in command:
        return "I am TARS, your voice-activated AI assistant."

    elif "weather" in command:
        # Try to extract city name after the word "in"
        city = "San Jose"
        words = command.split()
        for i, w in enumerate(words):
            if w == "in" and i + 1 < len(words):
                city = words[i + 1].capitalize()
        return get_weather(city)

    elif "exit" in command or "stop" in command:
        return "Deactivating. Goodbye!"

    else:
        return f"You said: {command}"

"""
brain.py
--------
TARS Brain Module — Processes user input and generates responses.
"""

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
        return "Currently, I can’t fetch live weather data yet — but it’s probably sunny somewhere!"

    elif "exit" in command or "stop" in command:
        return "Deactivating. Goodbye!"

    else:
        return f"You said: {command}"

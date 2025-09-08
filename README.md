# 🤖 TARS: Voice-Activated AI Assistant

TARS is a modular, intelligent assistant system designed to emulate a personalized AI experience — starting with a simple wake word and growing into a full conversational assistant.

---

## 🛠️ Project Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/tars-ai-assistant.git
cd tars-ai-assistant

# 2. Setup virtual environment (recommended)
conda create -n tars python=3.11
conda activate tars

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run device check (optional)
python list_devices.py

# 5. Run the assistant
python main.py
```

---

## ✅ Current Progress

### ✅ Step 1: Wake Word Detection (Complete)
- Using Picovoice Porcupine with custom `Hey TARS` model.
- Microphone streaming via PyAudio.
- Wake word triggers the assistant pipeline.
- Keyword model: `models/HEY-TARS_en_mac_v3_0_0.ppn`

---

## 🧭 Roadmap

### 🔄 Step 2: Speech-to-Text
- Use Whisper / Google STT API
- Transcribe user command after wake word

### 🧠 Step 3: Brain Module
- Route text to `brain/personality.py`
- Generate responses (rule-based or LLM-powered)

### 🎙️ Step 4: Text-to-Speech
- Output audio response using pyttsx3 / ElevenLabs

### 🌐 Step 5: Web Search Module (optional)
- Add real-time web retrieval via DuckDuckGo / SerpAPI

### 💬 Step 6: Chat History / Memory
- Maintain context over conversations

---

## 🗂️ Folder Structure

```
TARS/
├── brain/                    # Personality logic and response system
│   └── personality.py
├── wake_word/               # Wake word listener using Porcupine
│   └── wake_word.py
├── models/                  # Wake word model files (.ppn)
│   └── HEY-TARS_en_mac_v3_0_0.ppn
├── voice/                   # (Future) Voice reply modules
├── config/                  # (Deprecated) Config settings (replaced with folder logic)
├── main.py                  # Entry point
├── list_devices.py          # Tool to inspect microphone device indices
├── requirements.txt
├── .env                     # Environment file for secrets
└── README.md
```

---

## 👨‍💻 Author

**Krushna Thakkar**  
AI Researcher | MSAI @ SJSU | Hobbyist Builder  
[GitHub](https://github.com/kru2710shna) • [Website](https://localhost0027.netlify.app)

---

## 📜 License

MIT License. See `LICENSE` file.
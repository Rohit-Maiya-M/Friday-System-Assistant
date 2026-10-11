<div align="center">

# 🎙️ Friday — AI Desktop System Assistant

**A local AI-powered Windows desktop assistant that lives in the system tray.**

Voice-controlled interaction · Local LLM reasoning · Desktop automation

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Electron](https://img.shields.io/badge/Electron-Desktop_App-47848F?logo=electron&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![llama.cpp](https://img.shields.io/badge/LLM-llama.cpp-111827)
![Whisper.cpp](https://img.shields.io/badge/STT-Whisper.cpp-5B6DCD)
![Vosk](https://img.shields.io/badge/STT-Vosk-2E8B57)

</div>

---

## ✨ Overview

Friday is a local AI-powered desktop assistant designed to run from the Windows system tray. It combines voice input, local language-model reasoning, and desktop automation through a desktop interface.

Friday uses **Vosk** for lightweight speech recognition where configured, **Whisper.cpp** for voice transcription, and **llama.cpp** to run a local GGUF language model. A Python backend coordinates the assistant's processing and execution, while the Electron/React frontend provides the desktop interface.

## 🚀 Features

- 🎤 **Voice interaction** — speech input using Vosk and Whisper.cpp.
- 🧠 **Local AI reasoning** — run a local GGUF model through llama.cpp.
- 🖥️ **Desktop automation** — execute supported desktop actions.
- 🪟 **Desktop interface** — Electron and React frontend with a system-tray-oriented workflow.
- 🔌 **Local API** — FastAPI backend for communication between components.
- 🔒 **Local-first setup** — model inference and speech processing can run locally; no cloud inference is required for the local model workflow.

> Features depend on the current implementation and local configuration. A system-tray workflow does not necessarily mean every component runs as a Windows service.

## 🏗️ Architecture

```text
Microphone
    │
    ▼
Vosk — lightweight speech recognition / wake phrase flow
    │
    ▼
Whisper.cpp — voice transcription
    │
    ▼
Local LLM via llama.cpp
    │
    ▼
Planner / task execution
    │
    ├── Desktop automation
    ├── FastAPI backend
    └── Electron + React desktop interface
```

The exact path through Vosk and Whisper.cpp depends on the voice workflow configured in the backend.

## 🧰 Tech Stack

| Component | Technology |
|---|---|
| Desktop UI | Electron, React |
| Backend API | Python, FastAPI |
| Local LLM runtime | llama.cpp |
| Speech recognition | Vosk, Whisper.cpp |
| Desktop automation | PyAutoGUI and other configured utilities |
| Configuration | Environment variables in `.env` |

## 📁 Project Structure

```text
Friday-System-Assistant/
├── backend/
│   ├── app_resolver/                 # Application resolution
│   ├── capabilities/                  # Assistant capabilities
│   ├── llm_server/                    # Local LLM server integration
│   ├── planner/                       # Planning and task execution logic
│   ├── runtime/                       # Runtime state and communication files
│   ├── utils/                         # Shared utilities
│   ├── voice/
│   │   ├── models/                    # Voice-related model assets
│   │   ├── sample-audio/              # Audio samples / temporary audio
│   │   ├── vosk-model-small-en-us-0.15/
│   │   ├── whisper.cpp/
│   │   │   └── ggml-base.en.bin       # Whisper model (if stored here)
│   │   ├── executor.py
│   │   ├── extractor.py
│   │   ├── reasoning_engine.py
│   │   └── wake_word.py
│   ├── workflows/                     # Workflow definitions
│   ├── api.py                         # FastAPI application
│   ├── config.py                      # Environment-based configuration
│   ├── launcher.py                    # Starts the required backend processes
│   ├── main.py                        # Main assistant entry point
│   └── recents.json                   # Recent activity data
├── frontend/                          # Electron / React application
├── .env                               # Local configuration (not committed)
├── requirements.txt                   # Python dependencies
└── README.md
```

This tree reflects the current backend layout; some model files and generated runtime files may be omitted from Git or created locally.

## 🖥️ Requirements

- Windows
- Python 3.10
- Node.js and npm
- Git
- A compatible local GGUF model
- A working llama.cpp build (`llama-server.exe`)
- Whisper.cpp and its downloaded model
- Vosk model files

GPU acceleration is optional but recommended when supported by your hardware and llama.cpp build.

## ⚙️ Setup

### 1. Clone the repository

```powershell
git clone https://github.com/Rohit-Maiya-M/Friday-System-Assistant.git
cd Friday-System-Assistant
```

### 2. Create and activate a Python environment

```powershell
py -3.10 -m venv .venv310
.\.venv310\Scripts\Activate.ps1
```

If PowerShell blocks script execution for this session, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv310\Scripts\Activate.ps1
```

### 3. Install Python dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If the assistant reports that `psutil` is missing, install it and add it to `requirements.txt`:

```powershell
python -m pip install psutil
```

### 4. Install frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

If PowerShell blocks `npm.ps1`, use `npm.cmd` instead.

### 5. Configure the local LLM

Build or download a compatible llama.cpp release and obtain a GGUF model. Create a `.env` file in the repository root:

```dotenv
LLM_URL=http://127.0.0.1:8080/v1/chat/completions
LLM_SERVER_PATH=C:\path\to\llama-server.exe
MODEL_PATH=C:\path\to\your-model.gguf
```

Replace the example paths with paths on your machine. Keep `.env` local and do not commit real secrets or machine-specific configuration.

### 6. Configure speech models

Ensure the Vosk model directory is available at:

```text
backend/voice/vosk-model-small-en-us-0.15/
```

The Whisper model used in the current setup is:

```text
backend/voice/whisper.cpp/ggml-base.en.bin
```

If your downloaded Whisper model is stored elsewhere, update the path in the relevant backend configuration/code to match the actual location. The `whisper.cpp` source/build directory and the downloaded model file are separate things.

## ▶️ Run Friday

From the repository root, with the Python virtual environment activated:

```powershell
python backend/launcher.py
```

In a separate terminal, start the frontend:

```powershell
cd frontend
npm start
```

Use the frontend command configured in `frontend/package.json` if it differs from `npm start`.

## 🛠️ Troubleshooting

### Local LLM does not start
- Confirm `LLM_SERVER_PATH` points to `llama-server.exe`.
- Confirm `MODEL_PATH` points to an existing `.gguf` file.
- Check whether port `8080` is already in use.
- Review the launcher and llama.cpp console output.

### Speech recognition does not work
- Confirm the Vosk model directory and Whisper model file exist.
- Check microphone permissions and audio-device selection.
- Confirm the configured Whisper executable and model paths match your installation.

### Backend returns an error
- Activate the correct Python environment and install `requirements.txt`.
- Check that runtime JSON files contain valid JSON if the API reads them.
- Inspect the backend traceback before changing configuration.

### Frontend does not start
- Run `npm install` from `frontend/`.
- Check the scripts in `frontend/package.json`.
- If PowerShell blocks npm, try `npm.cmd start`.

## 🗺️ Roadmap

Potential future improvements include:
- More reliable voice activation and transcription handoff.
- More robust task planning and execution.
- Improved error reporting and runtime diagnostics.
- Docker support, if added to the project later.

## 📄 License

Add a `LICENSE` file to the repository if you intend to distribute Friday under a specific open-source license.

---

<div align="center">

**Built to bring local AI assistance to the desktop.** 🤖

</div>

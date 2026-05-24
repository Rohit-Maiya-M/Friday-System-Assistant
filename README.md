# Friday - AI Desktop System Assistant

Friday is a local AI-powered desktop assistant built using:

* Python
* Electron
* React
* FastAPI
* llama.cpp
* Whisper.cpp
* Vosk Speech Recognition

It supports:

* Voice activation
* Desktop automation
* Local LLM reasoning
* Modern desktop overlay UI
* Toast notifications
* Dependency-aware task execution (DAG system)

---

# Features

## Voice Assistant

* Wake word activation ("Friday")
* Real-time voice overlay
* Speech-to-text transcription using Whisper.cpp
* Low-latency wake-word detection using Vosk

## Desktop Automation

* Open applications
* Close applications
* Search the web
* Open Task Manager
* Write notes
* Take screenshots

## AI Reasoning

* Coding assistance
* Technical explanations
* Productivity help
* Local LLM-powered responses

## Modern UI

* Electron desktop overlay
* Glassmorphism chat interface
* Voice assistant overlay
* Windows-style toast notifications

---

# Architecture

Wake Word Detection
↓
Whisper.cpp Transcription
↓
LLM Planner
↓
DAG Task Execution
↓
Electron UI + Toast System

---

# Tech Stack

## Frontend

* React
* Electron
* TailwindCSS

## Backend

* Python
* FastAPI

## AI Stack

* llama.cpp
* Whisper.cpp
* Vosk

---

# IMPORTANT

Large AI models are NOT included in this repository.

You MUST manually download:

* GGUF LLM model
* Whisper model
* Build llama.cpp
* Build whisper.cpp

This keeps the repository lightweight and GitHub-compatible.

---

# Setup Guide

# 1. Clone Repository

```bash
git clone <your-repository-url>
cd friday-system-assistant
```

---

# 2. Create Python Virtual Environment

```bash
python -m venv .venv310
```

Activate venv:

## Windows

```bash
.venv310\Scripts\activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

---

# 3. Frontend Setup

```bash
cd frontend
npm install
```

---

# 4. Download GGUF LLM Model

Recommended model:

```text
Mistral-7B-Instruct-v0.3.Q4_0.gguf
```

Place the downloaded model inside:

```text
backend/
```

Example:

```text
backend/mistral-7b-instruct-v0.3.Q4_0.gguf
```

You may also use other GGUF models compatible with llama.cpp.

---

# 5. Build llama.cpp

Friday uses llama.cpp to run local GGUF models.

## Clone llama.cpp

```bash
git clone https://github.com/ggerganov/llama.cpp
```

---

## Build llama.cpp

### Windows (CMake)

```bash
cmake -B build
cmake --build build --config Release
```

After building, you should get:

```text
llama-server.exe
```

inside:

```text
build/bin/Release/
```

---

# 6. Configure llama.cpp Path

Update your config paths to point to:

* `llama-server.exe`
* your downloaded GGUF model

inside:

```text
backend/config.py
```

---

# 7. Build whisper.cpp

Friday uses whisper.cpp for speech transcription.

## Clone whisper.cpp

```bash
git clone https://github.com/ggerganov/whisper.cpp
```

---

## Build whisper.cpp

```bash
cmake -B build
cmake --build build --config Release
```

After building:

```text
whisper-cli.exe
```

should exist inside:

```text
build/bin/Release/
```

---

# 8. Download Whisper Model

Recommended:

```text
ggml-base.en.bin
```

Place inside:

```text
backend/voice/whisper.cpp/models/
```

---

# 9. Vosk Model

For lower latency, use:

```text
vosk-model-small-en-us-0.15
```

Place inside:

```text
backend/voice/
```

Recommended path:

```text
backend/voice/vosk-model-small-en-us-0.15
```

---

# Voice Directory Structure

All voice-related dependencies, models, and assets should remain inside:

```text
backend/voice/
```

Recommended structure:

```text
backend/
└── voice/
    ├── vosk-model-small-en-us-0.15/
    ├── whisper.cpp/
    │   ├── build/
    │   └── models/
    │       └── ggml-base.en.bin
    ├── sample-audio/
    └── executor.py
```

This is important because:

* the launcher
* transcription pipeline
* wake-word system
* executor logic

currently rely on these relative paths.

Changing the structure may break:

* voice activation
* transcription
* model loading
* automation execution

If you modify directory structure,
make sure to also update:

* `main.py`
* `launcher.py`
* `config.py`
* `executor.py`
* Whisper/Vosk model paths

---

# Browser Keyword Support

Currently supported browser/app keywords are configured manually inside:

```text
backend/voice/executor.py
```

If you want support for:

* Brave
* Opera
* Arc
* custom browsers
* additional applications

you must manually add:

* executable names
* paths
* aliases

inside:

```python
APP_ALIASES = {
    ...
}
```

and/or related executor logic.

---

# Runtime Files

Friday uses runtime JSON files for inter-process communication between:

* FastAPI
* Voice assistant
* Electron frontend

Create the following directory:

```text
backend/runtime/
```

Inside it, create these files:

---

## voice_state.json

Path:

```text
backend/runtime/voice_state.json
```

Content:

```json
{
    "state": "idle",
    "transcript": ""
}
```

Used for:

* voice overlay state
* transcription updates
* assistant execution status

---

## toast.json

Path:

```text
backend/runtime/toast.json
```

Content:

```json
{
    "visible": false,
    "message": ""
}
```

Used for:

* Windows-style toast notifications
* reasoning responses
* automation confirmations
* execution feedback

---

These files are automatically updated while Friday is running.

Do NOT delete them while the application is active.

---

# Accessing Friday from System Tray

When Friday starts, the Electron application runs from the Windows System Tray.

To open Friday:

1. Look at the bottom-right corner of the Windows taskbar.
2. Click the `^` arrow icon to open hidden tray icons.
3. Find the Friday icon.
4. Click the icon to open or hide the assistant overlay.

The assistant currently runs as a tray application instead of a normal taskbar application to provide:

* lightweight background execution
* always-on-top overlay support
* persistent voice assistant behavior

Future updates may include:

* dedicated taskbar pinning
* startup integration
* custom tray animations
* notification center integration

---

# Run Friday

## Start Frontend

```bash
cd frontend
npm start
```

---

## Start Backend

```bash
py backend/launcher.py
```

---

# Current Status

Project is under active development.

Planned improvements:

* Better planner optimization
* Streaming responses
* Smarter desktop automation
* Windows startup integration
* Packaging into executable
* Plugin system
* Dockerized backend

---

# License

MIT License

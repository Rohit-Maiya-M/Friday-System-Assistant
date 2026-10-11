import queue
import sounddevice as sd
import json
import wave
import subprocess
import numpy as np
import os

from vosk import Model, KaldiRecognizer

from planner.planner import build_dag
from planner.executor import execute_dag

from utils.voice_state import (
    update_voice_state
)

VOSK_MODEL_PATH = (
    r"backend\voice\vosk-model-small-en-us-0.15"
)

WHISPER_PATH = (
    r"backend\voice\whisper.cpp\build\bin\Release\whisper-cli.exe"
)

WHISPER_MODEL = (
    r"backend\voice\whisper.cpp\ggml-base.en.bin"
)

TEMP_AUDIO = (
    r"backend\voice\sample-audio\temp.wav"
)

WAKE_WORD = "friday"

VOLUME_THRESHOLD = 500

COMMAND_DURATION = 5


q = queue.Queue()


def callback(indata, frames, time, status):

    volume = np.linalg.norm(indata)

    if volume > VOLUME_THRESHOLD:

        q.put(bytes(indata))


def save_audio(audio_chunks):

    wf = wave.open(
        TEMP_AUDIO,
        "wb"
    )

    wf.setnchannels(1)

    wf.setsampwidth(2)

    wf.setframerate(16000)

    for chunk in audio_chunks:

        wf.writeframes(chunk)

    wf.close()


def run_whisper():

    try:

        subprocess.run(
            [
                WHISPER_PATH,

                "-m",
                WHISPER_MODEL,

                "-f",
                TEMP_AUDIO,

                "--output-txt",

                "--no-timestamps"
            ],

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL
        )

        txt_file = (
            TEMP_AUDIO + ".txt"
        )

        if not os.path.exists(txt_file):

            return ""

        with open(

            txt_file,

            "r",

            encoding="utf-8"
        ) as f:

            return f.read().strip()

    except:

        return ""


def record_command():

    print("🎧 Listening for command...")

    audio_chunks = []

    target_chunks = int(

        (16000 / 8000)
        * COMMAND_DURATION
    )

    for _ in range(target_chunks):

        data = q.get()

        audio_chunks.append(data)

    save_audio(audio_chunks)


def main():

    model = Model(
        VOSK_MODEL_PATH
    )

    rec = KaldiRecognizer(
        model,
        16000
    )

    with sd.RawInputStream(

        samplerate=16000,

        blocksize=8000,

        dtype="int16",

        channels=1,

        callback=callback
    ):

        print(
            "🎤 Say 'Friday' to activate..."
        )

        while True:

            data = q.get()

            rec.AcceptWaveform(data)

            partial = json.loads(

                rec.PartialResult()
            )

            text = partial.get(

                "partial",

                ""
            ).lower()

            if text:

                print(

                    f"⚡ {text}",

                    end="\r"
                )

            if WAKE_WORD in text:

                print(
                    "\n🟢 Activated"
                )

                update_voice_state(

                    state="listening",

                    transcript=""
                )

                while not q.empty():

                    q.get()

                record_command()

                final_command = (
                    run_whisper()
                )

                update_voice_state(

                    transcript=final_command
                )

                print(

                    f"\n🎯 Final Command: "

                    f"{final_command}"
                )

                update_voice_state(

                    state="processing"
                )

                tasks = build_dag(
                    final_command
                )

                print("\n📋 DAG:\n")

                for task in tasks:

                    print(task)

                update_voice_state(

                    state="executing"
                )

                execute_dag(tasks)

                rec.Reset()

                update_voice_state(

                    state="idle",

                    transcript=""
                )

                print(

                    "\n🎤 Waiting for "

                    "wake word..."
                )


if __name__ == "__main__":

    main()
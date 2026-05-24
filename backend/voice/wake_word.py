import sounddevice as sd
import numpy as np

from openwakeword.model import Model

model = Model(
    wakeword_models=[
        r"backend\voice\models\hey_jarvis_v0.1.onnx"
    ],
    inference_framework="onnx"
)

def listen_for_wake_word():

    print("🎤 Waiting for wake word...")
    samplerate = 16000
    chunk_duration = 0.08

    while True:
        audio = sd.rec(
            chunk_duration * samplerate,
            samplerate,
            channels=1,
            dtype="int16"
        )

        sd.wait()
        audio = audio.flatten()
        prediction = model.predict(audio)

        for wakeword, score in prediction.items():
            if score > 0.5:

                print(
                    f"🟢 Wake word detected: "
                    f"{wakeword}"
                )

                return

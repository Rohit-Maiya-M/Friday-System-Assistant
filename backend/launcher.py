import subprocess
import time
import requests

from config import settings


LLM_SERVER_PATH = settings.llm_server_path

MODEL_PATH = settings.model_path

LLM_URL = settings.llm_url


def start_llm_server():

    subprocess.Popen([

        LLM_SERVER_PATH,

        "-m",
        MODEL_PATH,

        "--n-gpu-layers",
        "12"
    ])

    print("🧠 Starting LLM server...")


def wait_for_server():

    print("⏳ Waiting for server...")

    while True:

        try:

            response = requests.post(

                LLM_URL,

                json={
                    "prompt": "hi",
                    "n_predict": 1
                }
            )

            if response.status_code == 200:

                print(
                    "✅ LLM server ready"
                )

                return

        except:
            pass

        time.sleep(2)


def start_api():

    print("🌐 Starting API server...")

    subprocess.Popen(

        [
            "py",
            "-m",
            "uvicorn",
            "api:app",
            "--reload"
        ],

        cwd="backend"
    )


def start_friday():

    print("🚀 Starting Friday...")

    subprocess.Popen([

        "py",
        "backend/main.py"
    ])


def main():

    start_llm_server()

    wait_for_server()

    start_api()

    start_friday()


if __name__ == "__main__":

    main()
import time
import requests
import subprocess
from  config import settings



def start_llm_server():        
    command = [
        settings.llm_server_path,
        "-m", settings.model_path,
        "--n-gpu-layers", "20"
    ]

    subprocess.Popen(command)

    print("🚀 Starting LLM server...")

    while True:
        try:
            requests.get(settings.llm_url + "/health")
            print("✅ LLM Server Ready")

            break
        except:
            time.sleep(1)
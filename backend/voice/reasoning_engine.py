import requests
from config import settings


URL = settings.llm_url


SYSTEM_PROMPT = """
You are Friday, a smart local AI desktop assistant.

Be concise, intelligent, and helpful.

Answer naturally like a modern AI assistant.
"""


def handle_reasoning(user_text):

    prompt = f"""
{SYSTEM_PROMPT}

User: {user_text}

Assistant:
"""

    payload = {
        "prompt": prompt,
        "n_predict": 256,
        "temperature": 0.7,
        "cache_prompt": False,
        "stop": ["User:"]
    }

    response = requests.post(URL, json=payload)

    data = response.json()

    answer = data["content"].strip()

    print("\n🤖 Friday:\n")
    print(answer)

    return answer
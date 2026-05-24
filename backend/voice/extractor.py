import requests
from config import settings


URL = settings.llm_url


def extract_app(user_text):

    prompt = f"""
You are an app name extractor.

Return ONLY the app name.
No explanation.
Single line only.

Examples:
Input: open chrome
Output: chrome

Input: fire up vscode
Output: vscode

Input: launch notion
Output: notion

Now extract:

Input: {user_text}
Output:
"""

    payload = {
        "prompt": prompt,
        "n_predict": 20,
        "temperature": 0.1,
        "cache_prompt": False,
        "stop": ["\n"]
    }

    response = requests.post(URL, json=payload)

    data = response.json()

    return data["content"].strip()
from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

import requests

from config import settings
from utils.voice_state import (
    get_voice_state
)
from utils.toast_state import (
    get_toast
)

app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)

URL = settings.llm_url

llm_busy = False


SYSTEM_PROMPT = """
You are Friday, an AI desktop system assistant.

Your responsibilities:
- help users with coding
- explain technical concepts
- solve programming problems
- assist with productivity
- answer clearly and concisely
- format responses properly

Behavior Rules:
- answer like ChatGPT or Copilot
- be professional and helpful
- keep responses concise unless detail is needed
- use markdown formatting
- use bullet points when useful
- use code blocks for code
- explain step-by-step when teaching
- avoid unnecessary filler text
- do not invent information
- stay focused on the user's request
"""


@app.get("/voice-state")
def voice_state():

    return get_voice_state()

@app.get("/toast")
def toast():

    return get_toast()


@app.post("/chat")
def chat(data: dict):

    global llm_busy

    if llm_busy:

        return {

            "response":
                "⚠️ Friday is currently processing another request."
        }

    llm_busy = True

    try:

        user_message = data["message"]

        payload = {

            "prompt": f"""
{SYSTEM_PROMPT}

User:
{user_message}

Assistant:
""",

            "n_predict": 128,

            "temperature": 0.3,

            "stop": [

                "User:",
                "Assistant:"
            ]
        }

        response = requests.post(

            URL,

            json=payload
        )

        result = response.json()

        assistant_response = (

            result["content"]
            .strip()
        )

        return {

            "response":
                assistant_response
        }

    except Exception as e:

        return {

            "response":
                f"❌ Backend Error: {str(e)}"
        }

    finally:

        llm_busy = False
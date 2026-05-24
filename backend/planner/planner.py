import json
import requests

from planner.task import Task
from config import settings


URL = settings.llm_url


def build_dag(user_command):

    prompt = f"""
You are a JSON task planner.

Convert the user request into a dependency-aware JSON task graph.

Return ONLY:
- valid JSON array
OR
- NOT_DEFINED

Never explain.
Never add markdown.
Never add extra text.

Supported capabilities:
- OPEN_APP
- CLOSE_APP
- SEARCH_WEB
- REASONING
- CALCULATE
- TAKE_SCREENSHOT
- WRITE_NOTE
- OPEN_TASK_MANAGER

Rules:
- Only use supported capabilities
- Never invent capabilities
- Every task must contain:
  - id
  - capability
  - params
  - depends_on
- depends_on must contain task ids
- Independent tasks use:
  "depends_on": []

- SEARCH_WEB depends on browser opening
only if browser is explicitly opened before it

- If request is:
  - incomplete
  - random
  - unclear
  - missing important information

Return ONLY:
NOT_DEFINED

- If the request is:
  - informational
  - conversational
  - explanation based
  - question based
  - knowledge based

ALWAYS use:
REASONING

Format:

[
  {{
    "id": 1,
    "capability": "OPEN_APP",
    "params": {{
      "app": "chrome"
    }},
    "depends_on": []
  }}
]

Examples:

User: open chrome

Output:
[
  {{
    "id": 1,
    "capability": "OPEN_APP",
    "params": {{
      "app": "chrome"
    }},
    "depends_on": []
  }}
]

User: open edge and search transformers

Output:
[
  {{
    "id": 1,
    "capability": "OPEN_APP",
    "params": {{
      "app": "edge"
    }},
    "depends_on": []
  }},
  {{
    "id": 2,
    "capability": "SEARCH_WEB",
    "params": {{
      "query": "transformers"
    }},
    "depends_on": [1]
  }}
]

User: calculate 2 + 3

Output:
[
  {{
    "id": 1,
    "capability": "CALCULATE",
    "params": {{
      "expression": "2 + 3"
    }},
    "depends_on": []
  }}
]

User: write hello world in notepad

Output:
[
  {{
    "id": 1,
    "capability": "WRITE_NOTE",
    "params": {{
      "text": "hello world"
    }},
    "depends_on": []
  }}
]

User: open task manager

Output:
[
  {{
    "id": 1,
    "capability": "OPEN_TASK_MANAGER",
    "params": {{}},
    "depends_on": []
  }}
]

User: what is an algorithm

Output:
[
  {{
    "id": 1,
    "capability": "REASONING",
    "params": {{
      "query": "what is an algorithm"
    }},
    "depends_on": []
  }}
]

User: tell me about elon musk

Output:
[
  {{
    "id": 1,
    "capability": "REASONING",
    "params": {{
      "query": "tell me about elon musk"
    }},
    "depends_on": []
  }}
]

User: open and search for

Output:
NOT_DEFINED

User: can you uh maybe

Output:
NOT_DEFINED

User:
{user_command}

Output:
"""

    payload = {

        "prompt": prompt,

        "n_predict": 256,

        "temperature": 0,

        "cache_prompt": False,

        "stop": [
            "User:"
        ]
    }

    try:

        response = requests.post(

            URL,

            json=payload
        )

        data = response.json()

        raw_output = (
            data["content"]
            .strip()
        )

        if not raw_output:

            print(
                "\n⚠️ Empty planner response"
            )

            return []

        if raw_output == "NOT_DEFINED":

            print(
                "\n⚠️ Command not understood"
            )

            return []

        start = raw_output.find("[")

        end = (
            raw_output.rfind("]")
            + 1
        )

        if start == -1 or end == 0:

            print(
                "\n⚠️ Invalid planner output"
            )

            print(raw_output)

            return []

        raw_output = (
            raw_output[start:end]
        )

        print("\n🧠 RAW PLAN:\n")

        print(raw_output)

        parsed = json.loads(
            raw_output
        )

        tasks = []

        for item in parsed:

            task = Task(

                task_id=item["id"],

                capability=item["capability"],

                params=item["params"],

                dependencies=item["depends_on"]
            )

            tasks.append(task)

        return tasks

    except Exception as e:

        print(
            "\n❌ Failed to parse DAG"
        )

        print(e)

        return []
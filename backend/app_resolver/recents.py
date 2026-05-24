import json
import os
from .config import RECENTS_FILE

def load_recents():
    if os.path.exists(RECENTS_FILE):
        with open(RECENTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_recents(data):
    with open(RECENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)
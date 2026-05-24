import os
from .config import VALID_DIRS

def find_executables(app_name):
    candidates = []

    for base in VALID_DIRS:
        if not os.path.exists(base):
            continue

        for root, dirs, files in os.walk(base):
            for file in files:
                if file.lower().endswith(".exe") and app_name in file.lower():
                    full_path = os.path.join(root, file)
                    candidates.append(full_path)

    return candidates
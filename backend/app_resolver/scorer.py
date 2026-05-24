import os
from rapidfuzz import fuzz
from .config import GOOD_FOLDERS, BAD_FOLDERS, BAD_KEYWORDS

def score_exe(path, app_name):
    score = 0
    path_lower = path.lower()
    filename = os.path.basename(path_lower)

    # Name similarity
    score += fuzz.partial_ratio(app_name, filename)

    # Clean filename bonus
    if "-" not in filename and "_" not in filename:
        score += 5

    # Good folder boost
    for folder in GOOD_FOLDERS:
        if f"\\{folder}\\" in path_lower:
            score += 10

    # Bad folder penalty
    for folder in BAD_FOLDERS:
        if f"\\{folder}\\" in path_lower:
            score -= 15

    # Bad keyword penalty
    for word in BAD_KEYWORDS:
        if word in filename:
            score -= 20

    # Depth penalty
    depth = path.count("\\")
    score -= depth * 0.5

    return score

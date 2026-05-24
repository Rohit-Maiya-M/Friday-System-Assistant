import os

VALID_DIRS = [
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs")
]

GOOD_FOLDERS = ["bin", "app", "application"]
BAD_FOLDERS = ["temp", "cache", "installer", "setup", "uninstall", "include", "lib", "resources"]

BAD_KEYWORDS = ["setup", "install", "update", "uninstall", "helper", "crash"]

RECENTS_FILE = "backend/recents.json"
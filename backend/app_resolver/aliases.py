import os

ALIASES_COMMANDS = {
    "chatgpt": "start chatgpt",
    "terminal": "start wt",
    "cmd": "start cmd",
    "powershell": "start powershell",
    "whatsapp": "start whatsapp"
}

def handle_alias(app_name):
    app_name = app_name.lower()

    if app_name in ALIASES_COMMANDS:
        print(f"⚡ Launching alias app: {app_name}")
        os.system(ALIASES_COMMANDS[app_name])
        return True

    return False
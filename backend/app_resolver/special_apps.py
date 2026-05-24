import os

SPECIAL_APPS = {
    "calculator": "calc",
    "calc": "calc",
    "explorer": "explorer",
    "file explorer": "explorer",
    "settings": "start ms-settings:",
    "store": "start ms-windows-store:",
    "microsoft store": "start ms-windows-store:"
}

def handle_special_app(app_name):
    app_name = app_name.lower()

    if app_name in SPECIAL_APPS:
        print(f"⚡ Launching special app: {app_name}")
        os.system(SPECIAL_APPS[app_name])
        return True

    return False
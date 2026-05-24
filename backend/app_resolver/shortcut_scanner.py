import os
import win32com.client

# Start Menu paths
START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
]

# Desktop path
DESKTOP_PATH = os.path.expandvars(r"%USERPROFILE%\Desktop")


def get_shortcut_target(lnk_path):
    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(lnk_path)
        return shortcut.Targetpath
    except:
        return None


def scan_shortcuts(app_name):
    app_name = app_name.lower()
    candidates = []

    paths_to_scan = START_MENU_PATHS + [DESKTOP_PATH]

    for base in paths_to_scan:
        if not os.path.exists(base):
            continue

        for root, dirs, files in os.walk(base):
            for file in files:
                if file.lower().endswith(".lnk"):

                    if app_name in file.lower():
                        lnk_path = os.path.join(root, file)
                        target = get_shortcut_target(lnk_path)

                        if target:
                            candidates.append((file, target))

    return candidates
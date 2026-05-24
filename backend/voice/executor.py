import os
import time
import subprocess
import psutil
import webbrowser
import urllib.parse
import win32gui
import win32process
import win32con

from app_resolver.resolver import resolve_app
from planner.context import context

from capabilities.focus_app import (
    focus_app
)

from capabilities.press_keys import (
    press_keys
)

from capabilities.press_key import (
    press_key
)

from capabilities.type_text import (
    type_text
)


BROWSER_KEYWORDS = [
    "chrome",
    "edge",
    "brave",
    "firefox",
    "opera"
]


def is_process_alive(pid):

    return psutil.pid_exists(pid)


def cleanup_context(app_name):

    context["running_apps"].pop(
        app_name,
        None
    )

    active = context.get(
        "active_browser"
    )

    if active and active["name"] == app_name:

        context["active_browser"] = None


def is_browser(app_name):

    app_name = app_name.lower()

    return any(
        browser in app_name
        for browser in BROWSER_KEYWORDS
    )


def get_visible_windows():

    windows = {}

    def enum_windows(hwnd, _):

        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd)

        if not title.strip():
            return

        windows[hwnd] = title

    win32gui.EnumWindows(
        enum_windows,
        None
    )

    return windows


def find_window_by_exe(exe_name):

    matched_hwnd = None

    matched_title = None

    def enum_windows(hwnd, _):

        nonlocal matched_hwnd
        nonlocal matched_title

        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd)

        if not title.strip():
            return

        try:

            _, pid = (
                win32process
                .GetWindowThreadProcessId(hwnd)
            )

            process = psutil.Process(pid)

            process_name = (
                process.name().lower()
            )

            if process_name == exe_name:

                matched_hwnd = hwnd

                matched_title = title

        except:
            pass

    win32gui.EnumWindows(
        enum_windows,
        None
    )

    return matched_hwnd, matched_title


def open_app(app_name):

    mode, path = resolve_app(app_name)

    if mode != "exe" or not path:

        print("❌ Could not open app")

        return

    process = subprocess.Popen([path])

    exe_name = os.path.basename(
        path
    ).lower()

    time.sleep(2)


    hwnd = None
    title = None

    for _ in range(20):

        hwnd, title = find_window_by_exe(
            exe_name
        )

        if hwnd:
            break

        time.sleep(0.3)

    title = win32gui.GetWindowText(
        hwnd
    )


    print(f"🚀 Opened {app_name}")

    context["running_apps"][app_name] = {

        "pid": process.pid,

        "path": path,

        "exe_name": exe_name,

        "hwnd": hwnd,

        "title": title
    }

    if is_browser(app_name):

        context["active_browser"] = {

            "name": app_name,

            "pid": process.pid,

            "path": path,

            "exe_name": exe_name,

            "hwnd": hwnd,

            "title": title
        }

        print(
            f"🌐 Active Browser: "
            f"{app_name}"
        )

    if hwnd:

        print(
            f"🪟 Window Tracked: "
            f"{title}"
        )

    else:

        print(
            "⚠️ Failed to detect window"
        )


def close_app(app_name):

    app = context["running_apps"].get(
        app_name
    )

    if not app:

        print("⚠️ App not tracked")

        return

    hwnd = app.get("hwnd")

    if not hwnd:

        print(
            f"❌ No HWND stored for "
            f"{app_name}"
        )

        return

    try:

        win32gui.PostMessage(
            hwnd,
            win32con.WM_CLOSE,
            0,
            0
        )

        print(f"❌ Closed {app_name}")

    except Exception as e:

        print("❌ Failed to close app")

        print(e)

    finally:

        cleanup_context(app_name)


def search_web(query):

    active_browser = context.get(
        "active_browser"
    )

    if not active_browser:

        encoded = urllib.parse.quote(query)

        url = (
            f"https://www.google.com/search?q="
            f"{encoded}"
        )

        webbrowser.open(url)

        print(f"🌐 Searching: {query}")

        return

    browser_name = active_browser["name"]

    focus_app(browser_name)

    time.sleep(1)

    press_keys(["ctrl", "t"])

    time.sleep(0.1)

    press_keys(["ctrl", "l"])

    time.sleep(0.1)

    type_text(query)

    time.sleep(0.1)

    press_key("enter")

    print(
        f"🔎 Searching in "
        f"{browser_name}: {query}"
    )
import win32gui
import win32con

from planner.context import context


def focus_app(app_name):

    app = context["running_apps"].get(
        app_name
    )

    if not app:

        print(
            f"❌ App not tracked: "
            f"{app_name}"
        )

        return False

    hwnd = app.get("hwnd")

    if not hwnd:

        print(
            f"❌ No HWND stored for "
            f"{app_name}"
        )

        return False

    try:

        win32gui.ShowWindow(
            hwnd,
            win32con.SW_MAXIMIZE
        )

        win32gui.SetForegroundWindow(
            hwnd
        )

        title = win32gui.GetWindowText(
            hwnd
        )

        print(
            f"🪟 Focused: {title}"
        )

        return True

    except Exception as e:

        print(
            "❌ Failed to focus app"
        )

        print(e)

        return False
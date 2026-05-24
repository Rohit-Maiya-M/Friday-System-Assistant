import pygetwindow as gw


def focus_window(title):

    windows = gw.getAllWindows()

    target = None

    for window in windows:

        if title.lower() in window.title.lower():

            target = window

            break

    if not target:

        print(
            f"❌ No window found: {title}"
        )

        return False

    try:

        if target.isMinimized:
            target.restore()

        target.activate()

        print(
            f"🪟 Focused: {target.title}"
        )

        return True

    except Exception as e:

        print(
            "❌ Failed to focus window"
        )

        print(e)

        return False
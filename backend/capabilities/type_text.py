import pyautogui


def type_text(text):

    pyautogui.write(
        text,
        interval=0.02
    )

    print(f"⌨️ Typed: {text}")
import pyautogui


def press_keys(keys):

    pyautogui.hotkey(*keys)

    print(f"⌨️ Pressed: {keys}")
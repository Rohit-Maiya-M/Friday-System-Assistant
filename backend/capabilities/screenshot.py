import pyautogui

def take_screenshot():
    image = pyautogui.screenshot()
    image.save("screenshot.png")
    print("📸 Screenshot saved")


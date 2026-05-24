import webbrowser

WEB_APPS = {
    "youtube": "https://youtube.com",
    "gmail": "https://mail.google.com",
    "google": "https://google.com"
}

def handle_web_app(app_name):
    app_name = app_name.lower()

    if app_name in WEB_APPS:
        print(f"🌐 Opening web app: {app_name}")
        webbrowser.open(WEB_APPS[app_name])
        return True

    return False
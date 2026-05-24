import time

from voice.executor import open_app

from capabilities.focus_app import (
    focus_app
)

from capabilities.type_text import (
    type_text
)


def write_note(text):

    open_app("notepad")

    time.sleep(1)

    focus_app("notepad")

    time.sleep(0.5)

    type_text(text)

    print("📝 Note written")
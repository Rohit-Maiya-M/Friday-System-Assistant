from pathlib import Path
import json


BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

VOICE_STATE_PATH = (
    BASE_DIR
    / "runtime"
    / "voice_state.json"
)


def update_voice_state(

    state=None,
    transcript=None
):

    with open(

        VOICE_STATE_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    if state is not None:

        data["state"] = state

    if transcript is not None:

        data["transcript"] = transcript

    with open(

        VOICE_STATE_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )


def get_voice_state():

    with open(

        VOICE_STATE_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)
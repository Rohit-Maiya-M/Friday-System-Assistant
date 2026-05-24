from pathlib import Path

import json


BASE_DIR = (

    Path(__file__)
    .resolve()
    .parent
    .parent
)

TOAST_PATH = (

    BASE_DIR
    / "runtime"
    / "toast.json"
)


def update_toast(

    visible=None,

    message=None
):

    with open(

        TOAST_PATH,

        "r",

        encoding="utf-8"
    ) as f:

        data = json.load(f)

    if visible is not None:

        data["visible"] = visible

    if message is not None:

        data["message"] = message

    with open(

        TOAST_PATH,

        "w",

        encoding="utf-8"
    ) as f:

        json.dump(

            data,

            f,

            indent=4
        )


def get_toast():

    with open(

        TOAST_PATH,

        "r",

        encoding="utf-8"
    ) as f:

        return json.load(f)
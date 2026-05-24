import socketio


sio = socketio.Server(

    cors_allowed_origins="*"
)

app = socketio.WSGIApp(sio)


def emit_state(state):

    sio.emit(

        "voice_state",

        {
            "state": state
        }
    )


def emit_transcript(text):

    sio.emit(

        "transcript",

        {
            "text": text
        }
    )
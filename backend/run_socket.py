import eventlet
import socketio

from socket_server import sio


app = socketio.WSGIApp(sio)

print("🔌 Socket server running...")

eventlet.wsgi.server(

    eventlet.listen(
        ("127.0.0.1", 9000)
    ),

    app
)
from flask import Flask
from flask_socketio import SocketIO
from threading import Lock
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_config_secret_zoom'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
async_mode = None
socket_app = SocketIO(app, async_mode=async_mode, manage_session=True,
                      cors_allowed_origins="*")
thread = None
thread_lock = Lock()

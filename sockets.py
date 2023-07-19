from config import *
from flask import request, session, jsonify
from flask_socketio import Namespace, emit, join_room
from data import db_session
from data.logs import Log
from random import choices
from datetime import datetime


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socket_app.sleep(10)
        count += 1
        socket_app.emit('my_response',
                        {'data': 'Server generated event', 'count': count},
                        namespace='/test')


class SocketClass(Namespace):
    def on_connect(self):
        global thread
        with thread_lock:
            if thread is None:
                thread = socket_app.start_background_task(background_thread)
        print('Client connected', request.sid)

    def on_disconnect(self):
        print('Client disconnected', request.sid)

    def on_filling(self):
        db_session.global_init("db/network.db")
        db_ses = db_session.create_session()
        log = db_ses.query(Log).all()[-1]
        emit('update_users',
             {"users": [user.to_dict(rules=('-log',)) for user in log.users]},
             broadcast=True)

    def on_start_roulette(self):
        db_session.global_init("db/network.db")
        db_ses = db_session.create_session()
        log = db_ses.query(Log).all()[-1]
        usernames = [i for i in range(len(log.users))]
        weights = [user.prc for user in log.users]
        winner_id = choices(usernames, weights=weights)[0]
        log.winner_id = log.users[winner_id].id
        log.datetime = datetime.now()
        db_ses.commit()
        new_log = Log()
        db_ses.add(new_log)
        db_ses.commit()
        emit("roulette",
             {"win_id": winner_id, "win_summ": round(log.summ * (100 - log.com) / 100, 2),
              "win_photo": log.users[winner_id].photo,
              "win_username": log.users[winner_id].username, "len_users": len(log.users), "win_prc": log.users[winner_id].prc}, broadcast=True)

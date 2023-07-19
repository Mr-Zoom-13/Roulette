from config import *
from flask import render_template, request
from sockets import SocketClass
from TiktokApi import *
from data import db_session
from data.users import User
from data.logs import Log


@app.route('/')
def sockets():
    db_ses = db_session.create_session()
    logs = []
    for log in db_ses.query(Log).all():
        if log.winner_id:
            logs.append(log.to_dict(rules=('-users.log',)))
            logs[-1]['winner'] = db_ses.query(User).get(log.winner_id).to_dict(rules=("-log",))
    logs = logs[::-1]
    return render_template('index.html', logs=logs)


@app.route('/manage', methods=['GET', 'POST'])
def manage_page():
    db_ses = db_session.create_session()
    log = db_ses.query(Log).all()[-1]
    if request.method == 'POST':
        if request.values.get('com'):
            log.com = request.values.get('com')
            db_ses.commit()
        else:
            username = request.values.get('username')
            summ = int(request.values.get('summ'))
            if username and summ:
                user = User()
                user.username = username
                user.summ = summ
                log.summ += summ
                api = Tiktok()
                user_tiktok = api.getInfoUser(username=username)
                if user_tiktok:
                    user.photo = user_tiktok['users'][username]['avatarLarger']
                    log.users.append(user)
                    db_ses.add(user)
                    db_ses.commit()
                    for tmp_user in log.users:
                        tmp_user.prc = round(tmp_user.summ / (log.summ * 0.01), 2)
                    db_ses.commit()

                    socket_app.emit('update_users', {
                        "users": [user.to_dict(rules=('-log',)) for user in log.users]},
                                    broadcast=True)
    return render_template('manage.html', com=log.com)


@app.route('/history/<int:log_id>')
def history_current_page(log_id):
    db_ses = db_session.create_session()
    log = db_ses.query(Log).get(log_id)
    return render_template('history_current.html',
                           users=[user.to_dict(rules=('-log',)) for user in log.users])


if __name__ == "__main__":
    db_session.global_init('db/roulette.db')
    socket_app.on_namespace(SocketClass('/'))
    socket_app.run(app, port=5000)

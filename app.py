# _*_ coding: utf-8 _*_
from flask import Flask, render_template, session, request, redirect, g
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
app.secret_key = "super secret key"
socketio = SocketIO(app)
DATABASE = 'test.db'

#db functions
def init_db():
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table';")
    tb_lst = cur.fetchone()[0]
    if(tb_lst == 0):
        print("> created DB")
        cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY AUTOINCREMENT, userid VARCHAR(12) NOT NULL, pwd TEXT NOT NULL, email TEXT NOT NULL, username TEXT);")
    db.commit()
    cur.close()
    db.close()
    
@app.route('/')
def index():
    if session.get("account_id") is not None:
        return render_template('index.html')
    else :
        return render_template('login.html')

# login function
@app.route('/account/login', methods=["POST"])
def login():
    db = sqlite3.connect("test.db")
    cur = db.cursor()
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]
    
    
    cur.execute("SELECT EXISTS (SELECT * FROM user WHERE userid = ? AND pwd = ?);", (user_id, user_pw))
    flag = cur.fetchone()[0]
    if flag == 1:
        session["account_id"] = user_id
        cur.execute("SELECT username FROM user WHERE userid = ?;", [user_id])
        session["user_id"] = cur.fetchone()
        print('> session : ' + session['account_id'])
        return redirect('/', code=302)
    else:
        return redirect('/', code=302)

@app.route('/account/signup', methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route('/account/create', methods=["POST"])
def create():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]
    user_em = request.form["user_email"]
    user_name = request.form["user_name"]
    
    db = sqlite3.connect('test.db')
    cur = db.cursor()
    cur.execute("INSERT INTO user(userid, pwd, email, username) VALUES(?, ?, ?, ?)", (user_id, user_pw, user_em, user_name))
    db.commit()
    cur.close()
    db.close()

    return redirect('/', code=302)

#Socketio Part
@socketio.on('connect', namespace='/chat')
def connect():
    print("Connected ...")

@socketio.on('first', namespace='/chat')
def test(data):
    print(data)
    sess = str(session['user_id'])
    sess = sess[2:-3]
    print(sess)
    mes = sess + " 님 께서 입장하셨습니다."
    emit('makechat',{'type': 'connect', 'name': 'SERVER', 'message': mes} , broadcast = True)

@socketio.on('message', namespace='/chat')
def message(data):
    print(data)
    ty = data['type']
    msg = data['message']
    sess = str(session['user_id'])
    sess = sess[2:-3]
    emit('makechat',{'type': ty, 'name': sess, 'message': msg}, broadcast = True, include_self=False)

#app start
if __name__ == '__main__':
    init_db()
    socketio.run(app, port=9001, debug=True)
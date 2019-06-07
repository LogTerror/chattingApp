# _*_ coding: utf-8 _*_
from flask import Flask, render_template, session, request, redirect, g
from flask_socketio import SocketIO, emit
import sqlite3

app = Flask(__name__)
socketio = SocketIO(app)
DATABASE = 'test.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(Exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    if session.get("account_id") is not None:
        return render_template('signup.html')
    else :
        return render_template('login.html')

# login function
@app.route('/account/login')
def login():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]

    '''
    @TODO : db connect and compare user id and pw
    '''
    # session['account_id'] = 
    '''
    @TODO : session create with db
    '''
    return redirect('/', code=302)

@app.route('/account/login')
def login():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]

    '''
    @TODO : db connect and compare user id and pw
    '''
    # session['account_id'] = 
    '''
    @TODO : session create with db
    '''
    return redirect('/', code=302)

@app.route('/account/signup', methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route('/account/create', methods=["POST"])
def create():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]
    user_em = request.form["user.email"]
    user_name = request.form["user_name"]

    '''
    @TODO : 디비에 user 추가
    '''

    return

#app start
if __name__ == '__main__':
    socketio.run(app, port=9001, debug=True)
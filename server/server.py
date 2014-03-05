from flask import *
import sqlite3

DATABASE = 'users.db'

app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def get_users():
	db = connect_db()
	cur = db.execute('SELECT user_name, user_pass FROM users')
	users = {}
	
	for row in cur.fetchall():
		users[row[0]] = {'password' : row[1]}
	db.close()
	
	return users
	
def get_online_users():
	db = connect_db()
	cur = db.execute("SELECT 'user_name', 'user_token' FROM sqlite_master WHERE type='table' AND name='online_users'")
	online_users = {}
	
	
	
	for row in cur.fetchall():
		online_users[row[0]] = {'token' : row[1]}
		print(online_users)
		print(row[0])
		print(online_users[row[0]])

	db.close()
	
	return online_users
	
def is_online(username):
	online_users = get_online_users()
	return online_users.__contains__(username)
	
def get_user_token(username):
	online_users = get_online_users()
	
	return online_users[username]['token']

	
def set_user_signed_in(username, token):
	db = connect_db()
	cur = db.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS online_users(user_name TEXT, user_token TEXT)")
	cur.execute("INSERT INTO online_users (user_name, user_token) VALUES(?,?)", (username, token))
	db.commit()
	db.close()
	

def sign_in(username, password):
	users = get_users()
	

	
	if is_online(username):
		return {'status' : 'Fail', 'msg' : 'User already signed in.'}
	
	if users.__contains__(username):
		if users[username]['password'] == password:
			set_user_signed_in(username,'1234')
			return {'status' : 'Success', 'msg' : 'Signed in.', 'data' : 'token'}
			
	return {'status' : 'Fail', 'msg' : 'Wrong username or password.'}

def sign_out(token):
	users = get_users()
	
	
	
@app.route('/')	
def test():

	return str(sign_in('Gustaf','pass'))
	
if __name__ == '__main__':
    app.run()
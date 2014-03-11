
import sqlite3
import re

DATABASE = 'users.db'

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

#Returns all registered users in a dictonary {email : {email, password, firstname, lastname, gender, city, country}}
def get_users():
	db = connect_db()
	cur = db.execute('SELECT * FROM users')
	users = {}
	
	for row in cur.fetchall():
		users[row[0]] = {'email' : row[0], 'password' : row[1], 'firstname' : row[2], 'lastname' : row[3], 'gender' : row[4], 'city' : row[5], 'country' : row[6]}
	db.close()
	
	return users
	
#Returns all online users in a dictonary {token : email }
def get_online_users():
	db = connect_db()
	cur = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND tbl_name='online_users'")
	
	online_users = {}
	
	if cur.fetchall() != []:
		cur = db.execute("SELECT user_email, user_token FROM online_users")
		for row in cur.fetchall():
			online_users[row[1]] = row[0]

	db.close()
	
	return online_users
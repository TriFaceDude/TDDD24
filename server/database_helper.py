from server import connect_db
import sqlite3
import re



'''
Database Access Methods
'''	

#Adds user to online users
def set_user_signed_in(email, token):
	db = connect_db()
	cur = db.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS online_users(user_email TEXT, user_token TEXT)")
	cur.execute("INSERT INTO online_users (user_email, user_token) VALUES(?,?)", (email, token))
	db.commit()
	db.close()
	
def set_user_offline(token):
	db = connect_db()
	db.execute('DELETE FROM online_users WHERE user_token=?', (token,))
	db.commit()
	db.close()

def create_user(email, password, firstname, lastname, gender, city, country):

	user = (email, password, firstname, lastname, gender, city, country)
	db = connect_db()
	cur = db.cursor()
	cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", user)
	db.commit()
	db.close()
	
def set_user_password(email, new_password):
	
	db = connect_db()
	cur = db.cursor()
	cur.execute("UPDATE users SET user_pass=? WHERE user_email=?", (new_password,email))
	db.commit()
	db.close()
	
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
	
def write_message(token, email, msg):

	db = connect_db()	
	cur = db.cursor()	
	cur.execute("CREATE TABLE IF NOT EXISTS user_messages (receiver_email TEXT, msg_index INTEGER, sender_email TEXT, msg_content TEXT)")
	
	cur.execute("SELECT COUNT(*) FROM user_messages WHERE receiver_email=?", (email,))
	cur.execute("INSERT INTO user_messages VALUES(?, ?, ?, ?)", (email, msg_index, token_to_email(token), msg))
	db.commit()
	cur.close()
	
	return online_users
	
def retrive_messages(email):

	db = connect_db()	
	cur = db.cursor()
	cur.execute("SELECT msg_index, sender_email, msg_content FROM user_messages WHERE receiver_email=?", (email,))
	
	messages = []
	for row in cur.fetchall():
		messages.append({'msg_id' : row[0], 'sender_email' : row[1], 'msg_content' : row[2]})
	
	return messages	
	
	
'''
Database Access Methods End Region 
'''	
	
	
'''
Help Methods
'''	
	
def user_exists(email):
	users = get_users()
	
	return users.__contains__(email)

def get_user_data_by_token(token):
	users = get_users()	
	return users[token_to_email(token)]
	
def get_user_data_by_email(token, email):
	
	if is_online_by_token(token):
		users = get_users()
		return users[email]

#Returns bool, true if token belongs to online user
def is_online_by_token(token):
	online_users = get_online_users()
	return online_users.__contains__(token)
	
#Returns bool, true if email belongs to online user
def is_online_by_email(email):
	online_users = get_online_users()
	return online_users.values().__contains__(email)

#Takes token, returns email
def token_to_email(token):
	online_users = get_online_users()
	
	return online_users[token]
	
#Takes email, returns token
def email_to_token(email):
	online_users = get_online_users()
	
	return online_users[email]['token']
	
'''
Help Methods End Region 
'''	

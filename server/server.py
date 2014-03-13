import sqlite3
from flask import *
import database_helper as db

DATABASE = 'users.db'
	
app = Flask(__name__)
app.debug = True
app.config.from_object(__name__)


def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

	

	
def valid_password(email, password):
	users = db.get_users()
	return users[email]['password'] == password
	
#Validates login and sets user online,
#if success returns {status, msg, data}
#if fail returns {status, msg}
def sign_in(email, password):
	users = db.get_users()
	
	if db.is_online_by_email(email):
		return {'status' : 'Fail', 'msg' : 'User already signed in.'}
	
	if users.__contains__(email):
		if valid_password(email, password):
			db.set_user_signed_in(email,'1234')
			return {'status' : 'Success', 'msg' : 'Signed in.', 'data' : 'token'}
			
	return {'status' : 'Fail', 'msg' : 'Wrong email or password.'}
	
	
#Sets user offline, returns {status, msg}
def sign_out(token):

	if not db.is_online_by_token(token):
		return {'status' : 'Fail', 'msg' : 'Token not valid.'}

	online_users = db.get_online_users()
	
	if online_users.__contains__(token):
		db.set_user_offline(token)
		
	return {'status' : 'Success', 'msg' : 'User signed out.'}
	
def valid_user_data(email, password, firstname, lastname, gender, city, country):

	#Email pattern, password pattern and string pattern
	ep = "[^@]+@[^@]+\.[^@]+"
	pp = "[A-Za-z0-9!@#$%5&/=?]{9,}"
	sp = "^[a-zA-Z]+$"

	return bool(re.match(ep, email)) and  bool(re.match(pp, password)) and  bool(re.match(sp, firstname)) and  bool(re.match(sp, lastname)) and  bool(re.match(sp, gender)) and  bool(re.match(sp, country))
	
def sign_up(email, password, firstname, lastname, gender, city, country):

	if db.user_exists(email):
		return {'status' : 'Fail', 'msg' : 'User already exists.'}
		
	if not valid_user_data(email, password, firstname, lastname, gender, city, country):
		return {'status' : 'Fail', 'msg' : 'Invalid user data.'}

	db.create_user(email, password, firstname, lastname, gender, city, country)
	return {'status' : 'Success', 'msg' : 'User registered.'}


	
def change_password(token, old_password, new_password):
	
	if not db.is_online_by_token(token):
		return {'status' : 'Fail', 'msg' : 'User not signed in.'}
	
	if not valid_password(token_to_email(token), old_password):
		return {'status' : 'Fail', 'msg' : 'Wrong password.'}
		
	db.set_user_password(token_to_email(token), new_password)
	return {'status' : 'Success', 'msg' : 'Password changed.'}


def get_user_messages_by_token(token):
	return db.get_user_messages_by_email(token, token_to_email(token))
	
def get_user_messages_by_email(token, email):
	
	if not db.is_online_by_token(token):
		return {'status' : 'Fail', 'msg' : 'User not signed in.'}
		
	return db.retrive_messages(email)
	
def post_message(token, email, msg):
	
	if not db.is_online_by_token(token):
		return {'status' : 'Fail', 'msg' : 'User not signed in.'}
		
	db.write_message(token, email, msg)
	
	return {'status' : 'Success', 'msg' : 'Message posted.'}
		

	
	
#Test method, will run on page refresh	
@app.route('/')	
def test():

	#return str(get_user_data_by_token('1234'))
	#return str(get_user_data_by_email('1234', 'Samuel@'))
	#return str(sign_out('1234'))
	print(str(sign_in('Gustaf@','pass')))
	#return str(sign_up('Guuuuuustaf@', 'pasujs', 'Gusujutaf', 'Svanerujuud', 'Mujuale', 'Linkujuoping', 'Swedujuen'))
	#return str(change_password('1234', 'pass', 'padd'))
	#return str(post_message('1234', 'Gustaf@', 'hej'))
	return str(get_user_messages_by_email('1234', 'Gustaf@'))
	
if __name__ == '__main__':
	app.run()
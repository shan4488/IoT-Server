import pymongo
from flask import request
from uuid import uuid4


client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
userdb = client['iot_server']
users = userdb.user


def insert_data():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['pass']

		reg_user = {}
		reg_user['name'] = name
		reg_user['email'] = email
		reg_user['password'] = password
		reg_user['token'] = str(uuid4())
		reg_user['devices'] = {}

		if users.find_one({"email":email}) == None:
			users.insert_one(reg_user)
			return True
		else:
			return False


def check_user():

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['pass']

		user = {
			"email": email,
			"password": password
		}

		user_data = users.find_one(user)
		if user_data == None:
			return False, ""
		else:
			return True, user_data["name"], user_data["token"]
		

def store_device_data():
	token = request.form["token"]
	device_id = request.form['device_id']
	temperature = request.form['temperature']

	userToken = {
		"token": token
	}

	user_data = users.find_one(userToken)
	if user_data == None:
		return False, "Token not found"
	else:
		users.update_one(
			{'token': token},
        	{'$push': {'devices.' + device_id + '.temp': temperature}}
    	)

		return True, 'Device data stored successfully!'
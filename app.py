import db
import json
from flask import Flask, request, render_template

app = Flask(__name__)

token = ''

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("signin.html")

@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    return render_template("Dashboard.html", token = token)


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")



@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    status, username, tempToken = db.check_user()
    global token
    token = tempToken

    data = {
        "username": username,
        "status": status
    }

    return json.dumps(data)



@app.route('/register', methods = ['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)


# Route to handle storing device data
@app.route('/store_device_data', methods=['POST'])
def store_device_data():
    status, message = db.store_device_data()

    data  = {
        "status": status,
        "message": message
    }

    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug = True)
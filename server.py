"""This code can create document for each individual user with user name provided. (Authentication is not provided, but should be provided).
The document of the user will contain all the device list and temperature data of each device. The data on mongo looks like this.

[
  {
    _id: ObjectId("6469151762e462a2e8327e46"),
    user_id: 'shan',
    devices: { resp1: { temp: [ '48', '44' ] }, esp1: { temp: [ '44' ] } }
  }
]

Postman is used to mimic the IoT device or a post request. Post request looks like this:

user_id = shan
device_id = esp1
temperature = 44

"""


from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = client['iot_server']  # Replace 'iot_server' with your database name

# Route to handle storing device data
@app.route('/store_device_data', methods=['POST'])
def store_device_data():
    # Get the user ID, device ID, and temperature value from the request
    user_id = request.form.get('user_id')
    device_id = request.form.get('device_id')
    temperature = request.form.get('temperature')
    print(user_id + " " + device_id + " " + temperature)

    # Check if the user document exists, create it if needed
    if not db['user_devices'].count_documents({'user_id': user_id}):
        db['user_devices'].insert_one({
            'user_id': user_id,
            'devices': {}
        })

    # Append temperature data to the device's 'temp' array
    db['user_devices'].update_one(
        {'user_id': user_id},
        {'$push': {'devices.' + device_id + '.temp': temperature}}
    )

    return 'Device data stored successfully!'


if __name__ == '__main__':
    app.run()

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_wtf.csrf import CSRFProtect
import boto3
from datetime import datetime
import uuid
import os
import yaml

# Read the config file
try:
    with open('config/config_basic.yml', 'r') as file:
        config = yaml.safe_load(file)
except FileNotFoundError as e:
    print(e)

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = config['appconfigsecretkey']

# AWS DynamoDB configurations
dynamodb = boto3.resource(
                        config['db'],
                        region_name = config['region'], 
                        aws_access_key_id = config['keyid'],
                        aws_secret_access_key = config['key'])
table = dynamodb.Table('dates')
userids = dynamodb.Table('userids')

# Welcome page
@app.route('/')
def welcome():
    return render_template('index.html')

# User page with id
@app.route('/d/<user_id>')
def user_page(user_id):
    if "Item" in userids.get_item(Key={'userID': str(user_id)}):
        return render_template('d.html')
        
    else:
        return render_template('404.html')

# Create new user page
@app.route('/createnew')
def call_create_new_page():
    return render_template('create_new.html')

#Post new user id
@app.route('/create_new', methods=['POST'])
def save_data():
    # Function checks if userid is reserved
    def is_uuid_reserved(check_uuid):
        response = userids.get_item(Key={'userID': str(check_uuid)})
        return 'Item' in response
    
    newID = str(uuid.uuid4())
    if (is_uuid_reserved(newID)):
        while is_uuid_reserved(newID):
            newID = str(uuid.uuid4())

    try:
        new_item = {
            'userID': newID,
            'name': request.form.get('dataName'),
            'date': str(datetime.now())
        }
        userids.put_item(Item=new_item)
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        return {'error': str(e)}

# File getter
@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

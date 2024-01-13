from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_wtf.csrf import CSRFProtect
import boto3
from datetime import datetime
import uuid

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'your_random_secret_key' #TODO need to be changed

# AWS DynamoDB configurations
dynamodb = boto3.resource(
    'dynamodb',
    region_name='eu-north-1',
    aws_access_key_id='AKIAYH4CNSTBQAJ5LWIH',
    aws_secret_access_key='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'
)
table = dynamodb.Table('dates')
userids = dynamodb.Table('userids')

# Welcome page
@app.route('/')
def welcome():
    return render_template('index.html')

# User page with id
@app.route('/d/<user_id>')
def user_page(user_id):
    return render_template('d.html')

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

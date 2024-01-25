from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_wtf.csrf import CSRFProtect
import psycopg2
from datetime import datetime
import uuid
import os
import yaml

# config to postgres
try:
    with open('config/conf_pgre_conn.yml', 'r') as file:
        config = yaml.safe_load(file)
except FileNotFoundError as e:
    print(e)

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = config['appconfigsecretkey']

try:
    db_host = config['host']
    db_port = config['port']
    db_user = config['user']
    db_password = config['password']
    db_name = config['database']

    connection = psycopg2.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = connection.cursor()
except Exception as e:
    print(f"Error: {e}")

# Welcome page
@app.route('/')
def welcome():
    return render_template('index.html')

# User page with id
@app.route('/d/<user_id>')
def user_page(user_id):
    try:
        cursor.execute(f'select user_id from users where user_id = {user_id}')
        if len(cursor.fetchall()) == 1:
            return render_template('d.html')
        else: return render_template('404.html')
    except Exception as e:
        print(e)
        return render_template('404.html')

# Create new user page
@app.route('/createnew')
def call_create_new_page():
    return render_template('create_new.html')

#Post new user id
@app.route('/create_new', methods=['POST'])
def save_data():
    try:
        cursor.execute(f"insert into users (username, creationdate) values ('{request.form.get('dataName')}', '{str(datetime.now())}')")
        return jsonify({'message': 'Data saved successfully'})
    except Exception as e:
        return {'error': str(e)}

# File getter
@app.route('/static/<filename>')
def serve_static(filename):
    print(f"getting file {filename}")
    return send_from_directory('templates', filename)

# 404 error
@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

@app.route("/api/data/<user_id>/getsaveddatas")
def getsaveddatas(user_id):
    cursor.execute(f"select * from dates where userid = {user_id}")
    list = []
    for record in cursor.fetchall():
        act_rec = []
        for item in record:
            act_rec.append(str(item))
        list.append(act_rec)
    print("now ", list)
    return jsonify(list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

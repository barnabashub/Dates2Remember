import sqlite3
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import uuid
import os
import yaml
import DatesHark

# config to postgres
try:
    with open('config/conf_pgre_conn.yml', 'r') as file:
        config = yaml.safe_load(file)
except FileNotFoundError as e:
    print(e)

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = config['appconfigsecretkey']

# Assuming your SQLite DB file is named 'database.db'
DATABASE = 'dates-dev.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

get_db_connection()

# Welcome page
@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/<user_id>')
def render_userpage(user_id):
    return render_template('userdashboard.html', datelib = get_user_dashboard(user_id))

@app.route('/datepage_<date_id>')
def render_datepage(date_id):
    cursor = get_db_connection().cursor()
    cursor.execute(f"select date from Dates where date_id = {date_id};")
    mydate = cursor.fetchall()[0][0]

    return render_template('datepage.html', info = get_date_info(date_id), datelib = get_next_dates(mydate, 5))

# User page with id
@app.route('/d/<user_id>')
def user_page(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"select user_id from users where user_id = '{user_id}'")
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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"insert into users (username, creationdate) values ('{request.form.get('dataName')}', '{str(datetime.now())}')")
        cursor.execute("select * from users")
        return jsonify({'message': 'Data saved successfully', 'select': cursor.fetchall()})
    except Exception as e:
        return {'error': str(e)}

# File getter
@app.route('/static/<filename>')
def serve_static(filename):
    return send_from_directory('templates', filename)

# 404 error
@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

@app.route("/api/data/<user_id>/getsaveddatas")
def getsaveddatas(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"select * from dates where userid = '{user_id}'")
    list = []
    for record in cursor.fetchall():
        act_rec = []
        for item in record:
            act_rec.append(str(item))
        list.append(act_rec)
    return jsonify(list)

@app.route("/api/<user_id>_dashboard", methods=['GET'])
def get_user_dashboard(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT name, date, date_id FROM Dates WHERE user_id = {user_id}")
        dates = cursor.fetchall()
        datelib = []
        for i in range(len(dates)):
            jubibool = DatesHark.DatesHark.is_jubilee(dates[i][1], datetime.now())
            nextdate = DatesHark.DatesHark.get_next_dates(dates[i][1], 1)
            if len(nextdate) == 1:
                nextdate = nextdate[0]
            datelib.append({
                'date': dates[i][1],
                'name': dates[i][0],
                'is_jubilee': jubibool,
                'next_date': nextdate,
                'date_id': dates[i][2]
            })
        return datelib
    except Exception as e:
        return {'error': str(e)}
    
def get_date_info(date_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"select name, date, description from Dates where date_id = {date_id};")
    selected = cursor.fetchall()
    return {
        'name': selected[0][0],
        'date': selected[0][1],
        'description': selected[0][2]
    }
    
@app.route("/api/<date>/get_howold_inmonths", methods=['GET'])
def get_howold_inmonts(date):
    return DatesHark.DatesHark.get_howold_inmonths(date, datetime.now())

@app.route("/api/<date>/get_howold_indays", methods=['GET'])
def get_howold_indays(date):
    return DatesHark.DatesHark.get_howold_indays(date, datetime.now())

@app.route("/api/<date>/any_jubilee", methods=['GET'])
def any_jubilee(date):
    return DatesHark.DatesHark.any_jubilee(date, datetime.now())

@app.route("/api/<date>/get_next_dates_<quantity>", methods=['GET'])
def get_next_dates(date, quantity):
    return DatesHark.DatesHark.get_next_dates(date, quantity)

@app.route("/api/<user_id>/get_next_dates_<quantity>", methods=['GET'])
def get_next_dates_user(user_id, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"select date, name from dates where user_id = '{user_id}'")
    dates = cursor.fetchall()
    returnable = []
    for i in range(len(dates)):
        pre_dates = DatesHark.DatesHark.get_next_dates(dates[i][0], quantity)
        for x in range(len(pre_dates)):
            returnable.append({
                'name': dates[i][1],
                'date': pre_dates[x]
            })
    returnable.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
    return jsonify(returnable)

@app.route('/api/get_when_will', methods=['GET'])
def get_when_will():
    day = request.args.get('day')
    date = request.args.get('date')
    return DatesHark.DatesHark.when_will_day_basedon_day(date, day)


if __name__ == '__main__':
    app.run(debug=True, port=5000, use_debugger=True)

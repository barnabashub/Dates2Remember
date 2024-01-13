from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'your_random_secret_key' #TODO need to be changed

# Üdvözlő oldal
@app.route('/')
def welcome():
    return render_template('index.html')

# Felhasználói oldal
@app.route('/d/<user_id>')
def user_page(user_id):
    return render_template('d.html')

@app.route('/createnew')
def call_create_new_page():
    return render_template('create_new.html')

@app.route('/create_new', methods=['POST'])
def save_data():
    data_name = request.form.get('dataName')
    email = request.form.get('email')
    
    # Add your logic to save data to the database here
    
    # For now, let's just print the values
    print(f"Data Name: {data_name}, Email: {email}")

    return jsonify({'message': 'Data saved successfully'})

@app.route('/static/<filename>')
def serve_static(filename):
    print("called")
    #if filename[-3:-1] == ".js":
        #return send_from_directory('templates', filename)
    return send_from_directory('templates', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

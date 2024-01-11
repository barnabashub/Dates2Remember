from flask import Flask, render_template

app = Flask(__name__)

# Üdvözlő oldal
@app.route('/')
def welcome():
    return render_template('index.html')

# Felhasználói oldal
@app.route('/d/<user_id>')
def user_page(user_id):
    return render_template('d.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

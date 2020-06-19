from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# App instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///log_db.db'




# Data Model
db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_string = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.now())




# Routes
@app.route('/')
def index():
    return render_template("base.html")

@app.route('/log_form/')
def log_form():
    return render_template("log_form.html")

@app.route('/log_action', methods=['POST'])
def log_action():
    log_string = request.form['log_string']

    # Adding to the database
    row = Log(log_string = log_string)
    db.session.add(row)
    db.session.commit()

    return 'Added to database: ' + log_string

if __name__ == '__main__':
    app.run(debug=True)

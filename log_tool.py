from flask import Flask, render_template, request, redirect, url_for
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



##########
# Routes #
##########

# Index Route
@app.route('/')
def index():
    return render_template('base.html')



# Log Form
@app.route('/log_form/')
def log_form():
    return render_template('log_form.html')



# Log Action
@app.route('/log_action', methods=['POST'])
def log_action():
    log_string = request.form['log_string']

    # Adding to the database
    row = Log(log_string = log_string)
    db.session.add(row)
    db.session.commit()

    return redirect(url_for('current_logs'))



# Show current logs
@app.route('/current_logs')
def current_logs():
    rows = Log.query.all()
    return render_template('current_logs.html', rows = rows)

if __name__ == '__main__':
    app.run(debug=True)

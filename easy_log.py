import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from sql_strings import logs_per_day


# App instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///easylog_database.sqlite3'
app.config['SECRET_KEY'] = 'aklsdjlaksjdlaksjdlaskjdoiqueqzxzcmnz'



#######################################
# DATA MODEL AND LOGIN MANAGER CONFIG #
#######################################

db = SQLAlchemy(app)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log_string = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default = lambda:datetime.now())
    user_id = db.Column(db.Integer)


# User Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##########
# ROUTES #
##########

# Index Route
@app.route('/')
def index():
    return render_template('index.html')



# Log Form
@app.route('/log_form')
@login_required
def log_form():
    return render_template('log_form.html')



# Log Action
@app.route('/log_action', methods=['POST'])
@login_required
def log_action():
    log_string = request.form['log_string']

    # Adding to the database
    row = Log(log_string = log_string, user_id = current_user.id)
    db.session.add(row)
    db.session.commit()

    return redirect(url_for('current_logs'))



# Show current logs
@app.route('/current_logs')
@login_required
def current_logs():
    rows = Log.query.all()
    return render_template('current_logs.html', rows = rows)


# Insights page
@app.route('/insights')
@login_required
def insights():
    
    results = db.session.execute(logs_per_day())
    x = []
    y = []
    for r in results:
        x.append(str(r.log_string))
        y.append(r.log_count)

    print(x)
    print(y)
    return render_template('insights.html', xset = x, yset = y)

# Log event web function
@app.route('/log_event', methods=['POST'])
@login_required
def log_event():
    data = request.get_json()
    event = Log(log_string = data['log_string'], user_id = current_user.id)
    db.session.add(event)
    db.session.commit()

    return jsonify({'success': True})



################
# LOGIN ROUTES #
################

# Login form
@app.route('/login')
def login():

    return render_template('login_form.html')

# Authenticate
@app.route('/app_authenticate', methods=['POST'])
def app_authenticate():
    user = User.query.filter_by(username=request.form['username']).first()

    if not user:
        return render_template('login_form.html', err_message='User not found!')

    login_user(user)

    return redirect(url_for('login'))

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login_form.html', err_message='You are now logged out!')

#################
# Start the App #
#################

if __name__ == '__main__':
    app.run(debug=True)

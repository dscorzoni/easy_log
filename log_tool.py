from flask import Flask, render_template, request

# App instance
app = Flask(__name__)

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
    return 'Log string is: ' + log_string

app.run()

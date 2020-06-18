from flask import Flask, render_template

# App instance
app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return render_template("base.html")

app.run()

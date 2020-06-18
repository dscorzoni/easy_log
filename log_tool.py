from flask import Flask

# App instance
app = Flask(__name__)

# Routes
@app.route('/')
def index():
    return 'Hello world!'

app.run()

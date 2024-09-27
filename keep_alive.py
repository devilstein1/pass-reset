from flask import Flask
from threading import Thread

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return "Alive"  # The message that confirms the bot is running

# Function to run the Flask app
def run():
    app.run(host='0.0.0.0', port=8080)

# Function to start the Flask server in a new thread
def keep_alive():
    t = Thread(target=run)
    t.start()

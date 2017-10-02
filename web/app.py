from flask import Flask
from time import sleep
app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/index.php')
def hello_world():
    return 'Hello, World!'


@app.route('/jobs')
def status_page():
    raise NotImplementedError


@app.route('/login')
def login():
    raise NotImplementedError


@app.route('/logout')
def logout():
    raise NotImplementedError


@app.route('/authcallback')
def authcallback():
    raise NotImplementedError


@app.route('/howto')
@app.route('/help')
def help():
    raise NotImplementedError


@app.route('/about')
def about():
    raise NotImplementedError


def authenticated(function):
    def wrapper(*args, **kwargs):
        sleep(2)
        return function(*args, **kwargs)
    return wrapper

from flask import Flask, render_template, request, redirect
from time import sleep
import os
import json
app = Flask(__name__)


@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/index.php')
def hello_world():
    return render_template("home.html")


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


@app.route('/newjob')
def submit_page():
    return render_template('submit.html')


@app.route('/script', methods=["POST"])
def script_handler():
    print(request.args)
    print(request.files)
    jobname = dict(request.form).get('job_name', "job")
    script = dict(request.files)['0'][0]
    print(script, jobname)
    return redirect('/newjob')


def authenticated(function):
    """I will have a decorator that determines whether a user is authenticated
    to the application. That way, I can just put @authenticated over the
    functions returning  authendicated pages"""
    def wrapper(*args, **kwargs):
        sleep(2)
        return function(*args, **kwargs)
    return wrapper

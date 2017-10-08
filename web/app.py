from flask import Flask, render_template, request, redirect
import sqlite3
from time import sleep
from werkzeug import secure_filename

import os
import json
app = Flask(__name__)

app.config["db_cursor"] = sqlite3.connect("interface.db").cursor()


@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/index.php')
@app.route('/home')
@app.route('/home.html')
def hello_world():
    return render_template("home.html")


@app.route('/filesystem_generator')
def fs_gen():
    raise NotImplementedError


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


def sanitize(string):
    string = string.decode("utf8", "ignore")


def sanitize_for_filename(filename):
    keepcharacters = (' ', '.', '_')
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).rstrip()


@app.route('/script', methods=["POST", "GET"])
def script_handler():
    jobname = dict(request.form).get('job_name', ["job"])[0]
    filename = dict(request.form).get('filename', ['script'])[0]
    fs = dict(request.files).get("filestructure")
    script = dict(request.files).get("executable")[0]
    print(request.form, "\n", script, "\n", fs)
    script.save(sanitize_for_filename(filename))
    return redirect('/newjob')


def authenticated(function):
    """I will have a decorator that determines whether a user is authenticated
    to the application. That way, I can just put @authenticated over the
    functions returning  authendicated pages"""
    def wrapper(*args, **kwargs):
        sleep(2)
        return function(*args, **kwargs)
    return wrapper

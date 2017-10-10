from flask import Flask, render_template, request, redirect
import sqlite3
from werkzeug import secure_filename
import os
import glob
import uuid
import json

app = Flask(__name__)

app.config["db_cursor"] = sqlite3.connect("interface.db").cursor()
app.config['upload_base_dir'] = "/Users/ben/Google Drive/class/y2/ind_study/workspace/uploads/"


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
    keepcharacters = [' ', '.', '_']
    safe = "".join(c for c in filename if c.isalnum()
                   or c in keepcharacters).rstrip()
    return safe.replace(" ", "_")


@app.route('/script', methods=["POST"])
def script_handler():
    jobname = sanitize_for_filename(
        dict(request.form).get('job_name', ["job"])[0])
    filename = sanitize_for_filename(
        dict(request.form).get('filename', ['script'])[0])
    fs = dict(request.files).get("filestructure", None)[0]
    script = dict(request.files).get("executable")[0]
    job_uuid = uuid.uuid1()
    jobname = make_job_base_dir(filename, jobname, script)
    if fs:
        fs.save(app.config["upload_base_dir"] +
                jobname + "/filestructure.json")
        parse_filesystem(jobname)
    return redirect('/newjob')


def make_job_base_dir(filename, jobname, script):
    if not os.path.exists(app.config['upload_base_dir'] + jobname):
        os.makedirs(app.config['upload_base_dir'] +
                    sanitize_for_filename(jobname))
    else:
        full_job_name_list = (
            app.config['upload_base_dir'] + jobname).split("_")[:-1]
        full_job_name = '_'.join(full_job_name_list) + "*"
        numruns = str(len(glob.glob(full_job_name)) + 1)
        print(numruns)
        jobname = jobname + "_" + numruns
        os.makedirs(app.config['upload_base_dir'] +
                    sanitize_for_filename(jobname))
    script.save(app.config['upload_base_dir'] + jobname + "/" + filename)
    return jobname


def parse_filesystem(jobname):
    dirpath = app.config["upload_base_dir"] + jobname + "/"
    try:
        fs_desc = json.load(open((dirpath + "filestructure.json", "r")))
    except Exception as e:
        print("No FS_desc provided")
    for object in fs_desc():
        pass


def authenticated(function):
    """I will have a decorator that determines whether a user is authenticated
    to the application. That way, I can just put @authenticated over the
    functions returning  authendicated pages"""
    def wrapper(*args, **kwargs):
        sleep(2)
        return function(*args, **kwargs)
    return wrapper

from flask import Flask, render_template, request, redirect, session, url_for, Response
import sqlite3
from werkzeug import secure_filename
from functools import wraps
import os
import glob
import uuid
import json

app = Flask(__name__)

app.config["db_cursor"] = sqlite3.connect("interface.db").cursor()
app.config['upload_base_dir'] = "/Users/ben/Google Drive/class/y2/ind_study/workspace/uploads/"
app.secret_key = b'\x9b4\xf8%\x1b\x90\x0e[?\xbd\x14\x7fS\x1c\xe7Y\xd8\x1c\xf9\xda\xb0K=\xba'
# I will obviously change this secret key before we go live


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not check_auth(session.get('username', None)):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


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
    return render_template("login.html")


@app.route('/login_test', methods=["POST"])
def login_test():
    uname = request.form['uname']
    passwd = request.form['passwd']
    print(uname, passwd)
    record = app.config['db_cursor'].execute(
        "select * from users where username=?", (uname,)).fetchone()
    if record:
        print(record)
        if passwd == record[4]:
            session['username'] = uname
            session["display_name"] = record[3]
            session['uuid'] = record[1]
            return "pass"
    return "fail"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("hello_world"))


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
@requires_auth
def submit_page():
    print(session)
    return render_template('submit.html')


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
    fs = dict(request.files).get("filestructure", [None])[0]
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
        app.logger.info("No FS_desc provided for job {}".format(jobname))
    for object in fs_desc():
        pass


def check_auth(username):
    """This function is called to check if a username /
    password combination is valid.
    """
    print(username)
    record = app.config['db_cursor'].execute(
        "select * from users where username=?", (username,)).fetchone()
    print(record)
    if not record:
        return False
    return username == record[0]


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 403,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

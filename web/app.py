from flask import Flask, render_template, request, redirect, session, url_for
import uuid
import sqlite3
import hashlib
import smtplib
from email.mime.text import MIMEText
import random
import hashids
import os

from database_helpers import db_save_job, increment_job_counter, get_all_jobs,\
    get_my_jobs, get_user_record, get_uname_record, get_all_users, add_users, \
    single_update
from security_helpers import sanitize_for_filename, requires_auth, authenticate
from exec_helpers import parse_filesystem, make_job_base_dir


app = Flask(__name__)

app.config['db_conn'] = sqlite3.connect("interface.db")
app.config["db_cursor"] = app.config['db_conn'].cursor()
app.config["admin_email"] = "glick@lclark.edu"
app.config['upload_base_dir'] = "/Users/ben/Google Drive/class/y2/ind_study/workspace/uploads/"
app.secret_key = b'\x9b4\xf8%\x1b\x90\x0e[?\xbd\x14\x7fS\x1c\xe7Y\xd8\x1c\xf9\xda\xb0K=\xba'
app.config['hashids'] = hashids.Hashids()
# I will obviously change this secret key before we go live


@app.route('/')
@app.route('/index')
@app.route('/index.html')
@app.route('/index.php')
@app.route('/home')
@app.route('/home.html')
def hello_world():
    """Home Page"""
    return render_template("home.html")


@app.route('/filesystem_generator')
def fs_gen():
    raise NotImplementedError


@app.route('/job<jid>')
def status_page(jid):
    return "Status Page"


@app.route('/login')
def login():
    """Render login page"""
    return render_template("login.html")


@app.route('/login_test', methods=["POST"])
def login_test():
    """Check if login was successful or not. Takes a post request, returns
    'pass' or 'fail'"""
    uname = sanitize_for_filename(request.form['uname'])
    passwd = hashlib.sha224(request.form['passwd'].encode('utf-8')).hexdigest()
    record = get_uname_record(uname)
    if record:
        if passwd == record[4]:
            session['username'] = uname
            session["display_name"] = record[3]
            session['uuid'] = record[1]
            session['email'] = record[5]
            return "pass"
    return "fail"


@app.route('/logout')
def logout():
    """Log out. Clear session and redirect to homepage."""
    session.clear()
    return redirect(url_for("hello_world"))


@app.route('/authcallback')
def authcallback():
    raise NotImplementedError


@app.route('/howto')
@app.route('/help')
def help():
    """Help Page"""
    return "Help you?! We can't even help ourselves!"


@app.route('/about')
def about():
    """About Page"""
    return "No About Yet. Come Back Later."


@app.route('/myjobs')
@requires_auth
def all_jobs2():
    """Render user jobs page."""
    uname = session.get('display_name')
    alljobs = get_my_jobs(session.get("uuid"))
    return render_template("all_my_jobs.html", all_jobs=alljobs, u_name=uname)


@app.route('/jobs')
@requires_auth
def all_jobs():
    """Render all jobs page"""
    alljobs = get_all_jobs()
    return render_template("all_jobs.html", all_jobs=alljobs)


@app.route('/newjob')
@requires_auth
def submit_page():
    """Show submit page"""
    print(session)
    return render_template('submit.html')


@app.route('/script', methods=["POST"])
@requires_auth
def script_handler():
    """Handle script submission. Save incoming files, prepare filesystem, add
    to database"""
    jn = sanitize_for_filename(
        dict(request.form).get('job_name', ["job"])[0])
    fn = sanitize_for_filename(
        dict(request.form).get('filename', ['script'])[0])
    fs = dict(request.files).get("filestructure", [None])[0]
    print(fs)
    script = dict(request.files).get("executable", [None])[0]
    desc = request.form.get("desc", [None])
    cli = request.form.get("cli", [None])
    jn, b_dir = make_job_base_dir(fn, jn, script)
    db_save_job(jn, fn, cli,
                session["uuid"], desc, b_dir)
    increment_job_counter(session.get('uuid'))
    if fs:
        fs.save(app.config["upload_base_dir"] +
                jn + "/filestructure.json")
        parse_filesystem(jn)
    return redirect('/newjob')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Render registration page and also handle registratin requests.
    Returns an error string to be shown to the user by the frontend js
    or returns 'pass'"""
    if request.method == 'GET':
        return render_template("register.html")
    uname = sanitize_for_filename(request.form['uname'])
    pw1 = request.form['passwd1']
    pw2 = request.form['passwd2']
    email = request.form['email']
    d_name = request.form['d_name']
    u_id = str(uuid.uuid1())
    if pw1 != pw2:
        return "Passwords do not match."
    if uname in get_all_users():
        return "Username Taken. Choose another one."
    add_users(uname, u_id, 0, d_name, str(
        hashlib.sha224(pw1.encode("utf-8")).hexdigest()), email)
    session['username'] = uname
    session['uuid'] = u_id
    session['display_name'] = d_name
    session['email'] = email
    return "pass"


@app.route('/changepass', methods=['POST', "GET"])
@requires_auth
def change_password():
    """Renders change password page, also handles requests
    to change passwords"""
    if request.method == 'GET':
        return render_template("change_pass.html")
    uname = request.form.get("uname")
    old_pass = hashlib.sha224(request.form.get(
        "old_passwd").encode('utf-8')).hexdigest()
    new_pass = hashlib.sha224(request.form.get(
        "passwd").encode('utf-8')).hexdigest()
    if uname != session['username']:
        return "fail"
    old_hash = get_user_record(session.get('uuid'))[4]
    if old_pass != old_hash:
        return "fail"
    single_update('users', 'passwd', (new_pass, session['uuid']))
    return "pass"


@app.route('/docs')
def docs():
    """Docs Page"""
    return "No Docs Yet. Come Back Later."


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact page and contact requests"""
    if request.method == "GET":
        return render_template("contact.html")
    name = request.form['uname']
    from_email = request.form['email']
    to_email = app.config['admin_email']
    message = MIMEText(request.form['msg'])

    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = "LC Cluster Interface Feedback Email [{}]".format(
        app.config['hashids'].encode(
            random.getrandbits(16)))
    print(message)
    s = smtplib.SMTP('aspmx.l.google.com')
    s.sendmail(from_email, [to_email], "Name: {}".format(
        name) + message.as_string())
    s.quit()
    return ""

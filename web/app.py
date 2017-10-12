from flask import Flask, render_template, request, redirect, session, url_for
import time
import uuid
import sqlite3
import hashlib
from database_helpers import db_save_job, increment_job_counter, get_all_jobs, get_my_jobs
from security_helpers import sanitize_for_filename, requires_auth
from exec_helpers import parse_filesystem, make_job_base_dir


app = Flask(__name__)

app.config['db_conn'] = sqlite3.connect("interface.db")
app.config["db_cursor"] = app.config['db_conn'].cursor()
app.config["admin_email"] = "glick@lclark.edu"
app.config['upload_base_dir'] = "/Users/ben/Google Drive/class/y2/ind_study/workspace/uploads/"
app.secret_key = b'\x9b4\xf8%\x1b\x90\x0e[?\xbd\x14\x7fS\x1c\xe7Y\xd8\x1c\xf9\xda\xb0K=\xba'
# I will obviously change this secret key before we go live


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


@app.route('/job<jid>')
def status_page(jid):
    return "Status Page"


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/login_test', methods=["POST"])
def login_test():
    uname = request.form['uname']
    passwd = hashlib.sha224(request.form['passwd'].encode('utf-8')).hexdigest()
    print(uname, passwd)
    record = app.config['db_cursor'].execute(
        "select * from users where username=?", (uname,)).fetchone()
    if record:
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
    return "Help you?! We can't even help ourselves!"


@app.route('/about')
def about():
    return "No About Yet. Come Back Later."


@app.route('/myjobs')
@requires_auth
def all_jobs2():
    uname = session.get('display_name')
    alljobs = app.config["db_cursor"].execute(
        """select job_name, display_name, cli_invoc, time_created, status, size,
        time_finished, desc
        from jobs
        join users on jobs.creator_uuid=users.user_uuid
        where users.user_uuid=?""", (session.get('uuid'),)).fetchall()
    return render_template("all_my_jobs.html", all_jobs=alljobs, u_name=uname)


@app.route('/jobs')
@requires_auth
def all_jobs():
    alljobs = get_all_jobs()
    return render_template("all_jobs.html", all_jobs=alljobs)


@app.route('/newjob')
@requires_auth
def submit_page():
    print(session)
    return render_template('submit.html')


@app.route('/script', methods=["POST"])
@requires_auth
def script_handler():
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
    if request.method == 'GET':
        return render_template("register.html")
    uname = request.form['uname']
    pw1 = request.form['passwd1']
    pw2 = request.form['passwd2']
    d_name = request.form['d_name']
    u_id = str(uuid.uuid1())
    if pw1 != pw2:
        return "Passwords do not match."
    if uname in app.config['db_cursor'].execute(
            "select username from users").fetchone():
        return "Username Taken. Choose another one."
    app.config['db_cursor'].execute("""insert into users (
    username, user_uuid, jobs_executed, display_name, passwd
    ) values (?,?,?,?,?)""", (uname, u_id, 0, d_name,
                              str(hashlib.sha224(
                                  pw1.encode("utf-8")).hexdigest())))
    app.config['db_conn'].commit()
    session['username'] = uname
    session['uuid'] = u_id
    session['display_name'] = d_name
    return "pass"


@app.route('/changepass', methods=['POST', "GET"])
@requires_auth
def change_password():
    if request.method == 'GET':
        return render_template("change_pass.html")
    uname = request.form.get("uname")
    old_pass = hashlib.sha224(request.form.get(
        "old_passwd").encode('utf-8')).hexdigest()
    new_pass = hashlib.sha224(request.form.get(
        "passwd").encode('utf-8')).hexdigest()
    if uname != session['username']:
        return "fail"
    old_hash = app.config['db_cursor'].execute(
        "select * from users where user_uuid=?",
        (session['uuid'],)
    ).fetchone()[4]
    if old_pass != old_hash:
        return "fail"
    app.config['db_cursor'].execute(
        "update users set passwd=? where user_uuid=?",
        (new_pass, session['uuid']))
    app.config['db_conn'].commit()
    return "pass"


@app.route('/docs')
def docs():
    return "No Docs Yet. Come Back Later."


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "GET":
        # We render the modal
        pass
    elif request.method == "POST":
        # we handle the contact form and send an email
        pass
    else:
        # 405 method not allowed
        return "405 Method Not Allowed"

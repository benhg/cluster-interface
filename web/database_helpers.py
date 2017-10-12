# helper functions for the database accesses
import app
import sqlite3
import uuid
import time


def db_save_job(jn, fn, cli, u_uuid, desc, b_dir):
    job_uuid = str(uuid.uuid1())
    now = str(time.ctime())
    app.app.config['db_cursor'].execute("""insert into jobs (job_name, cli_invoc, 
    time_created, j_id, creator_uuid, status, base_dir,
    exe_filename, size, desc) VALUES (?,?,?,?,?,?,?,?,?,?) """, (
        jn, cli, now, job_uuid, u_uuid, "Pending", b_dir, fn, 1, desc)
    )
    app.app.config['db_conn'].commit()


def increment_job_counter(user_id):
    current = int(app.app.config['db_cursor'].execute(
        'select jobs_executed from users where user_uuid=?', (user_id,)).fetchone()[0]) + 1
    app.app.config['db_cursor'].execute(
        "update users set jobs_executed=? where user_uuid=?", (current, user_id))
    app.app.config['db_conn'].commit()


def get_all_jobs():
    return app.app.config["db_cursor"].execute(
        """select job_name, display_name, cli_invoc, time_created, status, size,
        time_finished, desc
        from jobs
        join users on jobs.creator_uuid=users.user_uuid""").fetchall()


def get_my_jobs(uuid):
    return app.app.config["db_cursor"].execute(
        """select job_name, display_name, cli_invoc, time_created, status, size,
        time_finished, desc
        from jobs
        join users on jobs.creator_uuid=users.user_uuid
        where users.user_uuid=?""", (uuid,)).fetchall()


def get_user_record(uuid):
    return app.app.config['db_cursor'].execute(
        "select * from users where user_uuid=?",
        (uuid,)
    ).fetchone()


def get_uname_record(uname):
    return app.app.config['db_cursor'].execute(
        "select * from users where username=?", (uname,)).fetchone()


def get_all_users():
    return app.app.config['db_cursor'].execute(
        "select username from users").fetchone()


def add_users(uname, u_id, num, d_name, passw):
    app.app.config['db_cursor'].execute("""insert into users (
    username, user_uuid, jobs_executed, display_name, passwd
    ) values (?,?,?,?,?)""", (uname, u_id, num, d_name, passw))
    app.app.config['db_conn'].commit()

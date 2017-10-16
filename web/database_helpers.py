# helper functions for the database accesses
import app
import sqlite3
import uuid
import time


def db_save_job(jn, fn, cli, u_uuid, desc, b_dir):
    """Save a job to the jobs database
    :param jn jobname, :param fn filename of executable, :param u_uid user uuid
    :param desc job description string, :param b_dir base directory of job.
    returns nothing, commits to database."""
    job_uuid = str(uuid.uuid1())
    now = str(time.ctime())
    app.app.config['db_cursor'].execute("""insert into jobs (job_name, cli_invoc,
    time_created, j_id, creator_uuid, status, base_dir,
    exe_filename, size, desc) VALUES (?,?,?,?,?,?,?,?,?,?) """, (
        jn, cli, now, job_uuid, u_uuid, "Pending", b_dir, fn, 1, desc)
    )
    app.app.config['db_conn'].commit()


def increment_job_counter(user_id):
    """Add 1 to the user's 'jobs submitted' column in the database.
    :param user_id uuid of the user.
    returns nothing, commits to db"""
    current = int(app.app.config['db_cursor'].execute(
        'select jobs_executed from users where user_uuid=?', (user_id,)).fetchone()[0]) + 1
    app.app.config['db_cursor'].execute(
        "update users set jobs_executed=? where user_uuid=?", (current, user_id))
    app.app.config['db_conn'].commit()


def get_all_jobs():
    """Gets all jobs from database.
    returns 2d tuple of results"""
    return app.app.config["db_cursor"].execute(
        """select job_name, display_name, cli_invoc, time_created, status, size,
        time_finished, desc
        from jobs
        join users on jobs.creator_uuid=users.user_uuid""").fetchall()


def get_my_jobs(uuid):
    """Gets all jobs from database where user is identified by :param uuid.
    returns 2d tuple of results"""
    return app.app.config["db_cursor"].execute(
        """select job_name, display_name, cli_invoc, time_created, status, size,
        time_finished, desc
        from jobs
        join users on jobs.creator_uuid=users.user_uuid
        where users.user_uuid=?""", (uuid,)).fetchall()


def get_user_record(uuid):
    """Get the db row of a user identified by :param uuid"""
    return app.app.config['db_cursor'].execute(
        "select * from users where user_uuid=?",
        (uuid,)
    ).fetchone()


def get_uname_record(uname):
    """Get the db row of a user identified by :param uname (username)
    Avoid using this, instead use the one with a uuid. We need this
    for login testing before we know the user's uuid from the session"""
    return app.app.config['db_cursor'].execute(
        "select * from users where username=?", (uname,)).fetchone()


def get_all_users():
    """Select list of usernames from database.
    returns 2d tuple"""
    users = app.app.config['db_cursor'].execute(
        "select username from users").fetchall()
    return [user[0] for user in users]


def add_users(uname, u_id, num, d_name, passw, email, salt):
    """Add user to the table users.
    :param uname usernam, :param u_id user uuid, :param num number of jobs,
    :param d_name display name, :param passw salted hash of password,
    :param email user's email address"""
    app.app.config['db_cursor'].execute("""insert into users (
    username, user_uuid, jobs_executed, display_name, passwd, email, salt
    ) values (?,?,?,?,?,?,?)""", (uname, u_id, num, d_name, passw, email, salt))
    app.app.config['db_conn'].commit()


def single_update(table_name, col_name, data_tuple):
    """Update a single table, changing one column
    :param """
    app.app.config['db_cursor'].execute(
        "update ?  set ?=? where user_uuid=?",
        (table_name, col_name) + data_tuple)
    app.app.config['db_conn'].commit()

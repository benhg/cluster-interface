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

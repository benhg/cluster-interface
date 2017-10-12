# helpers for job execution
import os
import json
import glob
import app
from security_helpers import sanitize_for_filename


def make_job_base_dir(filename, jobname, script):
    if not os.path.exists(app.app.config['upload_base_dir'] + jobname):
        os.makedirs(app.app.config['upload_base_dir'] +
                    sanitize_for_filename(jobname))
    else:
        full_job_name_list = (
            app.app.config['upload_base_dir'] + jobname).split("_")[:-1]
        full_job_name = '_'.join(full_job_name_list) + "*"
        numruns = str(len(glob.glob(full_job_name)) + 1)
        print(numruns)
        jobname = jobname + "_" + numruns
        os.makedirs(app.app.config['upload_base_dir'] +
                    sanitize_for_filename(jobname))
    script.save(app.app.config['upload_base_dir'] + jobname + "/" + filename)
    return jobname, app.app.config['upload_base_dir'] + sanitize_for_filename(jobname)


def parse_filesystem(jobname):
    fs_desc = []
    dirpath = app.app.config["upload_base_dir"] + jobname + "/"
    try:
        fs_desc = json.load(open((dirpath + "filestructure.json", "r")))
    except Exception as e:
        app.app.logger.info("No FS_desc provided for job {}".format(jobname))
    for object in fs_desc:
        pass

# helpers for job execution
import os
import json
import glob
import app
from urllib.parse import urlparse
from security_helpers import sanitize_for_filename
from database_helpers import change_job_status


def make_job_base_dir(filename, jobname, script):
    """make base directory for job containing script/exe, filesystem description
    and generated filename
    :param filename name to save script as, :param jobname, name of job,
    :param script werkzeug FileStorage object containing script/exe"""
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
    return jobname, app.app.config['upload_base_dir'] + \
        sanitize_for_filename(jobname)


def parse_filesystem(jobname, postfix='', fs_desc=None):
    """Parse JSON filesystem representation and create filesystem.
    :param jobname name of job in question
    :param postfix addition to be made to file path
    :param fs_desc JSON description of filesystem

    Look, I know this sucks. I promise when I have better ideas, 
    I will fix this function.
    """
    change_job_status(jobname, "Staging Inputs")
    dirpath = app.app.config["upload_base_dir"] + jobname + "/" + postfix
    if type(fs_desc) != dict:
        try:
            fs_desc = json.load(open(dirpath + "filestructure.json", "r"))
        except Exception as e:
            app.app.logger.info(
                "No FS_desc provided for job {}".format(jobname))
            raise e
    if fs_desc == {}:
        return jobname
    current_dirs = fs_desc.get("subdirs")
    if not os.path.exists(dirpath + fs_desc['name']):
        os.makedirs(dirpath + fs_desc['name'])
    dirpath += fs_desc['name'] + "/"
    for dir in current_dirs:
        current_files = dir.get("subfiles")
        if not os.path.exists(dirpath + dir['name']):
            os.makedirs(dirpath + dir['name'])
        parse_filesystem(jobname, dir['name'], dir.get('subdirs'))
        if len(current_files) > 0:
            parse_files(current_files, dirpath + dir['name'])
    change_job_status(jobname, "Pending (Unsched)")
    return jobname


def parse_files(list_of_files, basedir):
    """Parse JSON filesystem description for flat files"""
    for file in list_of_files:
        path = os.path.abspath(basedir).replace(
            ' ', r"\ ") + '/' + file['name']
        if not os.path.exists(path):
            if file['type'] == 'wget':
                os.system(
                    r"wget {}  --output-document={}".format(urlparse(file['source']).geturl(), path))
            elif file['type'] == 'cp':
                os.system("cp {} {}".format(file['source'], path))
            elif file['type'] == 'globus':
                raise NotImplementedError
            return True

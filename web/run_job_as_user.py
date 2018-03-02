from libsubmit import GridEngine
import sys
import os
import json
import pwd
import time
import app
from database_helpers import db_save_job, increment_job_counter, get_all_jobs,\
    get_my_jobs, get_user_record, get_uname_record, get_all_users, add_users, \
    update_pass
from security_helpers import sanitize_for_filename, requires_auth
from exec_helpers import parse_filesystem, make_job_base_dir
uname = sys.argv[1]
size = int(sys.argv[4])
uid = pwd.getpwnam(uname)[2]
home = pwd.getpwnam(uname)[5]
gid = 2001
os.setgid(gid)
os.setuid(uid)
os.environ['PATH'] = "/local/cluster/bin/:/local/cluster/sge/bin/lx-amd64/"+os.environ['PATH']
b_dir = sys.argv[2]
cli = sys.argv[3]
cmd_str = """                                                                             
PATH=/local/cluster/bin/:/local/cluster/sge/bin/lx-amd64/:$PATH
export PATH                                                                                  
export LD_LIBRARY_PATH=/local/cluster/lib/:$LD_LIBRARY_PATH
cd {}                                                                                         
{}
python3 /local/cluster/share/send_completion_email.py '{}' '{}'
""".format(b_dir, cli, b_dir, uname)
provider = GridEngine(config=json.load(open("/var/www/cluster-interface/sge_config.json")))
j_id = provider.submit(cmd_str, blocksize=size)
print(j_id)


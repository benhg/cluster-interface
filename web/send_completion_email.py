#!/local/cluster/bin/python3
import app
from email.mime.text import MIMEText
import smtplib
import sys

name = sys.argv[2]
from_email = app.app.config['admin_email']
to_email = sys.argv[2]+'@lclark.edu'
base_dir = sys.argv[1]
job_name = base_dir.split('/')[-1:][0]
msg = """
Hello {},

This email is to let you know that your job {} has been completed.
You can find the output of this job in the directory '{}' on mayo.blt.lclark.edu.

If you have any problems, please report them using this link:
http://mayo.blt.lclark.edu/webjobs/contact

Thank you for using BLT and have a nice day.
""".format(name,job_name, base_dir)
message = MIMEText(msg)
message['From'] = from_email
message['To'] = to_email
message['Subject'] = "LC Cluster Job Exited"

s = smtplib.SMTP('aspmx.l.google.com')
s.sendmail(from_email, [to_email], "Name: {}".format(
    name) + message.as_string())
s.quit()

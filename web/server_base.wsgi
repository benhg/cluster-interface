import sys
sys.path.insert(0, '/var/www/cluster-interface/')
sys.path.extend(['',
 '/local/cluster/bin',
 '/local/cluster/lib/python36.zip',
 '/local/cluster/lib/python3.6',
 '/local/cluster/lib/python3.6/lib-dynload',
 '/home/users/glick/.local/lib/python3.6/site-packages',
 '/local/cluster/lib/python3.6/site-packages',
 '/local/cluster/lib/python3.6/site-packages/libsubmit-0.3.0-py3.6.egg',
 '/local/cluster/lib/python3.6/site-packages/Flask_PAM-0.1-py3.6.egg',
 '/local/cluster/lib/python3.6/site-packages/python_jose-2.0.2-py3.6.egg',
 '/local/cluster/lib/python3.6/site-packages/Flask-0.12.2-py3.6.egg',
 '/local/cluster/lib/python3.6/site-packages/simplepam-0.1.5-py3.6.egg',
 '/local/cluster/lib/python3.6/site-packages/pycryptodome-3.4.11-py3.6-linux-x86_64.egg',
 '/local/cluster/lib/python3.6/site-packages/future-0.16.0-py3.6.egg',
 '/local/cluster/lib/python3.6/site-packages/ecdsa-0.13-py3.6.egg',
 '/local/cluster/lib/python3.6/site-packages/itsdangerous-0.24-py3.6.egg',
 '/local/cluster/lib/python3.6/site-packages/click-6.7-py3.6.egg',
 '/home/users/glick/.local/lib/python3.6/site-packages/IPython/extensions',
 '/home/users/glick/.ipython'])

from app import app as application
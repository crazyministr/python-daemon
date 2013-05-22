#!/usr/bin/python
"""
example for daemon launch in the system
1) apt-get install python-daemon
2) touch file /var/run/copy-daemon.pid and edit it any random number and save it
3) launch this script ./copy-daem.py start/stop in console and close console without exit from session
"""

"""
    1. Должен быть создан файл .netrc, c логином и паролем от git'a
"""

import os, time, subprocess, sys
from daemon import runner
# import git, ConfigParser

class Daemon():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/copy-daemon.log'
        self.stderr_path = '/var/log/copy-daemon.log'
        self.pidfile_path = '/var/run/copy-daemon.pid'
        self.pidfile_timeout = 5

        self.git_pull = '/var/www/rep/press/'
        self.main_dir = '/var/www/press/'

    def copy(self):
        os.chdir(self.git_pull)
        try:
            p = subprocess.Popen("git pull origin test", shell = True)
            p.wait()
        except Exception, e:
            sys.stderr.write("git pull failed: %d (%s)\n" % (e.errno, e.strerror))

    def run(self):
        os.chdir(self.git_pull)
        try:
            p = subprocess.Popen("git checkout test", shell = True)
            p.wait()
        except Exception, e:
            sys.stderr.write("git checkout failed: %d (%s)\n" % (e.errno, e.strerror))

        while True:
            self.copy()
            # p = subprocess.Popen('/etc/init.d/gunicorn restart', shell = True)
            # p.wait()
            # p = subprocess.Popen('/etc/init.d/celeryd restart', shell = True)
            # p.wait()
            # p = subprocess.Popen('/etc/init.d/nginx restart', shell = True)
            # p.wait()
            # p = subprocess.Popen('python manage.py collectstatic')
            # p.wait()
            time.sleep(60) # 1 minute

if __name__ == "__main__":
    daemon = Daemon()
    daemon_runner = runner.DaemonRunner(daemon)
    daemon_runner.do_action()

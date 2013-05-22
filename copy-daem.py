#!/usr/bin/python
import os, time, subprocess, sys
from daemon import runner

class Daemon():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/copy-daemon.log'
        self.stderr_path = '/var/log/copy-daemon.log'
        self.pidfile_path = '/var/run/copy-daemon.pid'
        self.pidfile_timeout = 5

        self.git_pull = '/var/www/rep/press/'
        self.main_dir = '/var/www/press/'

    def gitPull(self):
        os.chdir(self.git_pull)
        try:
            p = subprocess.Popen("git pull origin test", shell = True)
            p.wait()
        except Exception, e:
            sys.stderr.write("git pull failed: %d (%s)\n" % (e.errno, e.strerror))

    def copy(self):
        os.chdir(self.main_dir)
        p = subprocess.Popen("rm -r apps/", shell = True)
        p.wait()
        p = subprocess.Popen("rm -r templates/", shell = True)
        p.wait()
        p = subprocess.Popen("cp -r " + self.git_pull + "apps/" + " " + self.main_dir, shell = True)
        p.wait()
        p = subprocess.Popen("cp -r " + self.git_pull + "templates/" + " " + self.main_dir, shell = True)
        p.wait()

    def run(self):
        os.chdir(self.git_pull)
        try:
            p = subprocess.Popen("git checkout test", shell = True)
            p.wait()
        except Exception, e:
            sys.stderr.write("git checkout failed: %d (%s)\n" % (e.errno, e.strerror))

        while True:
            self.gitPull()
            self.copy()
            # p = subprocess.Popen('python manage.py collectstatic', shell = True)
            # p.wait()
            # p = subprocess.Popen('/etc/init.d/gunicorn restart', shell = True)
            # p.wait()
            # p = subprocess.Popen('/etc/init.d/celeryd restart', shell = True)
            # p.wait()
            # p = subprocess.Popen('/etc/init.d/nginx restart', shell = True)
            # p.wait()
            time.sleep(60) # 1 minute

if __name__ == "__main__":
    daemon = Daemon()
    daemon_runner = runner.DaemonRunner(daemon)
    daemon_runner.do_action()

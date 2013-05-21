#!/usr/bin/python
"""
example for daemon launch in the system
1) apt-get install python-daemon
2) touch file /var/run/copy-daemon.pid and edit it any random number and save it
3) launch this script ./copy-daem.py start/stop in console and close console without exit from session
"""

"""
    sudo apt-get install python-git
"""

import os, time, subprocess, sys, atexit
from daemon import runner
from ftplib import FTP
import git
# import redis

# FTP_HOST = "46.182.26.90"
# FTP_USER_INPUT = "input"
# FTP_USER_OUTPUT = "output"
# FTP_PASSWORD = "Kdm147def"
# INPUT_DIR = "/home/oshikuru/Workflow/file_reactor/input/"
# OUTPUT_DIR = "/home/oshikuru/Workflow/file_reactor/output/"
# REDIS_HOST = 'localhost'
# REDIS_PORT = 6379
# REDIS_DB_ID = 0

# db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_ID)


# def upload():
#     ftp = FTP(FTP_HOST, FTP_USER_INPUT, FTP_PASSWORD)
#     input_dir = os.listdir(INPUT_DIR)
#     for file_name in input_dir:
#         tmp_name, file_extension = os.path.splitext(file_name)
#         if file_extension == '.pdf':
#             if db.exists("file:" + tmp_name):
#                 if db.hget("file:" + tmp_name, "status") != "in_check_system" and db.hget("file:" + tmp_name, "status") != "processed":
#                     try:
#                         ftp.storbinary('STOR '+ file_name, open(INPUT_DIR + file_name, 'rb'))
#                         db.hset("file:" + tmp_name, "status", "in_check_system")
#                     except:
#                         db.hset("file:" + tmp_name, "status", "error")
#                         print("error")
#                     finally:
#                         print("file " + tmp_name)
#             else:
#                 try:
#                     db.hset("file:" + tmp_name, "ext", "pdf")
#                     db.hset("file:" + tmp_name, "status", "in_input_dir")
#                     ftp.storbinary('STOR '+ file_name, open(INPUT_DIR + file_name, 'rb'))
#                     db.hset("file:" + tmp_name, "status", "in_check_system")
#                 except:
#                     db.hset("file:" + tmp_name, "status", "error")
#                     print("error")
#                 finally:
#                     print("file " + tmp_name)

# def download():
#     ftp = ftp = FTP(FTP_HOST, FTP_USER_OUTPUT, FTP_PASSWORD)
#     ftp.cwd('/')
#     output_dir = OUTPUT_DIR
#     dbfiles = db.keys("file:*")
#     ftpfiles = ftp.nlst('*_NOK_original.pdf')
#     for dbfile in dbfiles:
#         if db.hget(dbfile, "status") == "in_check_system":
#             file_name = dbfile[5:]
#             if file_name + "_NOK_original.pdf" in ftpfiles:
#                 orig_handle = open(output_dir + file_name + "_NOK_original.pdf", 'wb')
#                 ftp.retrbinary('RETR ' + file_name + "_NOK_original.pdf", orig_handle.write)
#                 orig_handle.close()
#                 db.hset(dbfile, "status", "processed")
#                 xml_handle = open(output_dir + file_name + "_NOK_xml_report.xml", 'wb')
#                 ftp.retrbinary('RETR ' + file_name + "_NOK_xml_report.xml", xml_handle.write)
#                 xml_handle.close()
#                 db.hset(dbfile, "xml", "ok")

class Daemon():
    def __init__(self):
        self.stdin = '/dev/null'
        self.stdout = '/var/log/copy-daemon.log'
        self.stderr = '/var/log/copy-daemon.log'
        self.pidfile = '/var/run/copy-daemon.pid'
        self.pidfile_timeout = 5

        self.git_pull = '/var/www/rep/press/'
        self.main_dir = '/var/www/press/'

    def git_init():
        subprocess.Popen("git pull", stdout = subprocess.PIPE, shell = True)
        os.chdir(self.git_pull)
        git.Git().init()
        git.Git().clone('git://ruslux/press')

    def pid():
        # перенаправление стандартного ввода/вывода
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
    
        # записываем pidfile
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid():
        os.remove(self.pidfile)

    def copy():
        # to be continued...
        os.chdir(self.git_pull);
        try:
            git.Git().pull("origin test");
        except Exception, e:
            sys.stderr.write("git pull failed: %d (%s)\n" % (e.errno, e.strerror))

    def run(self):
        self.pid()
        self.git_init()
        while True:
            self.copy()
            p = subprocess.Popen('/etc/init.d/gunicorn restart', shell = True)
            p.wait()
            p = subprocess.Popen('/etc/init.d/celeryd restart', shell = True)
            p.wait()
            p = subprocess.Popen('/etc/init.d/nginx restart', shell = True)
            p.wait()
            time.sleep(self.pidfile_timeout)

if __name__ == "__main__":
    daemon = Daemon()
    daemon_runner = runner.DaemonRunner(daemon)
    daemon_runner.do_action()

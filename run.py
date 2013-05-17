#!/usr/bin/env python
 
import sys, time
from daemon import Daemon
 
class MyDaemon(Daemon):
	def run(self):
		while True:
			time.sleep(1)
 
if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command\nUsage: %s start|stop|restart" % sys.argv[0]
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)

	# subprocess.Popen('/etc/init.d/gunicorn restart', shell = True)
	# subprocess.Popen('/etc/init.d/celeryd restart', shell = True)
	# subprocess.Popen('/etc/init.d/nginx restart', shell = True)

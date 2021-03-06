#!/usr/bin/env python

import sys, time
from Daemon import Daemon

class MyDaemon(Daemon):
	def run(self):
		while True:
			time.sleep(1)

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/secmon.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		elif 'status' == sys.argv[1]:
			daemon.status()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart|status" % sys.argv[0]
		sys.exit(2)

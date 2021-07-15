
import os, sys
from pydaemon import Daemon

class Process(Daemon):

	def run(self):
		self.log_status("entered application")

if __name__ == "__main__":
	if len(sys.argv) == 2:
		psu = Process('/tmp/pythond.pid', '/tmp/pythond.log')
		if 'start' == sys.argv[1]: psu.start()
		elif 'stop' == sys.argv[1]: psu.stop()
		elif 'restart' == sys.argv[1]: psu.restart()
	else: print("usage: %s start|stop|restart" % sys.argv[0])

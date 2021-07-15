
import os, sys
from pydaemon import Daemon

class Process(Daemon):

	def run(self):
		try:
			with open("testlog.txt", "w") as filestr:
				filestr.write("System daemon active")
			pid = os.fork()
			if pid == 0:
				with open("childlog.txt", "a") as filestr:
					filestr.write("Success child")
			else:
				with open("parentlog.txt", 'a') as filestr:
					filestr.write("Success parent")
		except Exception as err:
			self.log_error("Application error encountered: {0}".format(err))

if __name__ == "__main__":
	if len(sys.argv) == 2:
		psu = Process('/tmp/pythond.pid', '/tmp/pythond.log')
		if 'start' == sys.argv[1]: psu.start()
		elif 'stop' == sys.argv[1]: psu.stop()
		elif 'restart' == sys.argv[1]: psu.restart()
	else: print("usage: %s start|stop|restart" % sys.argv[0])

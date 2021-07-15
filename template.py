
import os, sys
from pydaemon import Daemon

class Process(Daemon):

	"""
	Implementation Template. Must subclass Daemon class. Method run
	overrides empty Daemon.run method. Recommended use Daemon.log_status,
	Daemon.log_warning, Daemon.log_error, Daemon.log_debug methods for
	application logging.
	"""

	def run(self):
		""" Daemon application entry """
		pass

if __name__ == "__main__":
	if len(sys.argv) == 2:
		psu = Process('/tmp/pythond.pid', '/tmp/pythond.log')
		if 'start' == sys.argv[1]: psu.start()
		elif 'stop' == sys.argv[1]: psu.stop()
		elif 'restart' == sys.argv[1]: psu.restart()
		else print("usage: %s start|stop|restart" % sys.argv[0])
	else: print("usage: %s start|stop|restart" % sys.argv[0])


import os
from pydaemon import Daemon

class Process(Daemon):

	def logerr(self, msg):
		with open('/tmp/pythond.log', 'a') as filestr:
			filestr.write(msg)

	def run(self):
		self.logerr("Running application")
		while True: pass
		# try:
		# 	with open("testlog.txt", "w") as filestr:
		# 		filestr.write("System daemon active")
		# 	pid = os.fork()
		# 	if pid == 0:
		# 		count = 0
		# 		while count < 10:
		# 			with open("testlog.txt", "a") as filestr:
		# 				filestr.write("Successful process fork iter")
		# 			count += 1
		# except Exception as err:
		# 	self.logerr("Application error encountered: {0}".format(err))

if __name__ == "__main__":
	psu = Daemon('/tmp/pythond.pid', '/tmp/pythond.log')
	psu.start()

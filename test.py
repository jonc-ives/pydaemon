
import os
from pydaemon import Daemon

class Process(Daemon):

	def run():
		with open("testlog.txt", "w") as filestr:
			filestr.write("System daemon active\n")
		pid = os.fork()
		if pid == 0:
			count = 0
			while count < 10:
				with open("testlog.txt", "a") as filestr:
					filestr.write("Successful process fork iter")
				count += 1

if __name__ == "__main__":
	psu = Daemon('/tmp/pythond.pid', '/tmp/pythond.log')
	psu.start()

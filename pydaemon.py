# pydaemon.py

# pydaemon -- JT Ives
# Daemonizes python process with linux system. No license necessary;
# this is pretty standard stuff, I just got tired of rewriting it.

import sys, os, time, atexit, signal
from datetime import datetime

class Daemon:
    """ a custom daemon class.

    Usage: subclass this daemon class and override the run() method."""

    def __init__(self, pidfile, logfile, appname=""):
        self.appname = appname
        self.logfile = logfile
        self.pidfile = pidfile 

    def append_log_header(self):
        """ Append process execution header to log file """
        write_flag = 'a' if os.path.isfile(self.logfile) else "w"
        with open(self.logfile, write_flag) as logstr:
            logstr.write("\nPYDAEMON EXEC %s %s\n" % (datetime.now().strftime("%m:%d:%Y %H:%M:%S"), self.appname))

    def log_error(self, msg):
        with open(self.logfile, 'a') as logstr:
            logstr.write("[ERROR] %s %s\n" % (datetime.now().strftime("%m:%d:%Y %H:%M:%S"), msg))

    def log_debug(self, msg):
        with open(self.logfile, 'a') as logstr:
            logstr.write("[DEBUG] %s %s\n" % (datetime.now().strftime("%m:%d:%Y %H:%M:%S"), msg))

    def log_status(self, msg):
        with open(self.logfile, 'a') as logstr:
            logstr.write("[STATUS] %s %s\n" % (datetime.now().strftime("%m:%d:%Y %H:%M:%S"), msg))            

    def log_warning(self, msg):
        with open(self.logfile, 'a') as logstr:
            logstr.write("[WARNING] %s\t%s\n" % (datetime.now().strftime("%m:%d:%Y %H:%M:%S"), msg))

    def daemonize(self):
        """ Daemonize class. Employs UNIX double fork mechanism """
        self.log_status("daemonizing application...")

        try:
            pid = os.fork()
            if pid > 0: sys.exit(0)
            self.log_debug("instantiated primary fork")
        except OSError as err:
            self.log_error('primary fork failed: {0}'.format(err))
            sys.exit(1)

        # decouple from parent env
        os.chdir('/')
        os.setsid()
        os.umask(0)
        self.log_debug("decoupled process from parent environment")

        try:
            pid = os.fork()
            if pid > 0: sys.exit(0)
            self.log_debug("instantiated redundant fork")
        except OSError as err:
            self.log_error('redundant fork failed: {0}'.format(err))
            sys.exit(1)

        # redirect std file desc.
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(os.devnull, 'r')
        so = open(os.devnull, 'a+')
        se = open(os.devnull, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
        self.log_debug("redirected standard file descriptors")

        # write pidfile
        self.log_debug("registering process id")
        atexit.register(self.delpid)
        pid = str(os.getpid())
        with open(self.pidfile, 'w') as pf:
            pf.write(pid + '\n')
        self.log_status("starting application...")

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        """ start the daemon """

        # if logging to file, append log header
        self.append_log_header()

        try: # check for runstate with pidfile
            with open(self.pidfile, 'w+') as pf:
                raw = pf.read().strip()
                pid = int(raw) if raw.isdigit() else None
        except:
            self.log_debug("verified unique application instance")
            pid = None

        if pid:
            message = "pidfile {0} already exists. Daemon already running?"
            self.log_error(message.format(self.pidfile))
            sys.exit(1)

        # start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """ stop the daemon """

        try: # check for runstate with pidfile
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "kill failed. pidfile {0} does not exist. Daemon not running?\n"
            self.log_warning(message.format(self.pidfile))
            return # usually happens in restarts -- not an error
        
        try: # try killing daemon process
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            e = str(err.args)
            if e.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

    def restart(self):
        """ Restart the daemon. """
        self.stop()
        self.start()

   
    def run(self):
        """ This needs to be overridden when Daemon is subclasses
        It will only be called after the process is daemonized by start() or restart()"""
        self.log_error("Method 'run' must be overridden when Daemon is subclassed")

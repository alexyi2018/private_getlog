#!/home/alexyi/python2.7/local/bin/python
#coding: utf-8

import sys
import os
import time
import shutil
import logging
import getpass

class MyLog(object):
    def __init__(self):
        user = getpass.getuser()
        self.logger = logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        #logfile = './' + sys.argv[0][0:-3] + '.log'
        logfile = sys.argv[0][0:-3] + '.log'
        logexit = os.path.lexists(logfile)
        #formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s')
        formatter = logging.Formatter('%(asctime)-12s %(message)-12s')

        logHand = logging.FileHandler(logfile)
        logHand.setFormatter(formatter)
        logHand.setLevel(logging.INFO)

        logHandSt = logging.StreamHandler()
        logHandSt.setFormatter(formatter)

        self.logger.addHandler(logHand)
        #self.logger.addHandler(logHandSt) #Display the log info to screen

	if not logexit:    #Change the log file permission to 777
            os.chmod(logfile, 0777)
        else:
            #if log file over 1M, will rename it.
            logfileSize = os.path.getsize(logfile)
            if logfileSize > 1048576:    #1M=1048576K
                newfile = '{}_getfile.log'.format(int(time.time()))
                shutil.move(logfile,newfile)

    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warn(self,msg):
        self.logger.warn(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)

if __name__ == "__main__":
    mylog = MyLog()
    mylog.debug("I'm debug")
    mylog.info("I'm info")
    mylog.warn("I'm warn")
    mylog.error("I'm error")
    mylog.critical("I'm critical")

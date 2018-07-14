#!/usr/bin/env /home/alexyi/python2.7/local/bin/python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import ftplib
import zipfile
import subprocess
import platform
from myLog import MyLog    #Self customize module
from EXIT import EXIT     #Self customize module
from font import UseStyle    #Self customize module
from getLogPath import GetLogPath    #Self customize module
from getPCSN import GetPCSN    #Self customize module
from mailVerify import MailVerify    #Self customize module

class LoginFTP(object):
    def __init__(self):
        self.host = "10.79.221.67"
        #self.user = "administrator"
        self.user = "cppadmin"
        self.passw = "!4produse"

    def ftpserver(self):
        try:
            ftp = ftplib.FTP(self.host, self.user, self.passw)
        except socket.error, socket.gaierror:
            outStr = "!!!FTP is unaviable, plese check the host, user and passw"
            print UseStyle(outStr, mode='bold', fore='white', back='red')
            EXIT()
        return ftp

class DLFtpFile(object):
    def __init__(self):
        pass

    def downloadFile(self, ftp, filename):
        try:
            ftp.retrbinary('RETR %s'%filename, open(filename,'wb').write, 1024)
        except Exception, err:
            outStr = "!!!Get file failed n_n!: %s" %err
            print UseStyle(outStr, mode='bold', fore='white', back='red')
            EXIT()
        finally:
            pass
            #ftp.quit()
        return True 

class ScanSernum(object):
    def __init__(self):
        self.sn_sample = re.compile(r'^FDO\d{4}\w{4}$')

    def scanMain(self):
        while True:
            sernum = (raw_input("Enter Sernum[0=EXIT,f=File]==>")).upper()
            try:
                if sernum == '0':
                    sys.exit()
                if sernum == 'F':
                    sernum = raw_input("Enter file path[eg.'/usr/auto/a.txt']==>")
		    outStr = "File Path:[%s]"% sernum
		    print UseStyle(outStr, fore='blue')
		    break
                if self.sn_sample.match(sernum):
                    outStr = "Scanned sernum[%s]"% sernum
                    print UseStyle(outStr, fore='blue')
                    break
                else:
                    print "Scanned wrong format-->%s"% sernum
            except ValueError:
                print "Scaned wrong format"
                continue
        return sernum

class ScanAreaType(object):
    def __init__(self):
        self.logarea = {
        "0":"EXIT",
        "1":"BST",
        "2":"2C",
        "3":"ASSY",
        "4":"RUNIN",
        "5":"FQA",
        "6":"ALL"
        }
        self.logtype = {
        "0":"EXIT",
        "1":"MVIEW",
        "2":"MTYPE",
        "3":"MVIEW&MTYPE",
        }

    def displayItem(self, items):
        outStr = '||'*30
        print UseStyle(outStr, fore='blue')
        outStr = '||' + 'List as below'
        print UseStyle(outStr, fore='blue')
        for item in sorted(items):
            outStr = '||' + item + '=' + items.get(item)
            print UseStyle(outStr, fore='blue')
        outStr = '||'*30
        print UseStyle(outStr, fore='blue')

    def askArea(self):
        self.displayItem(self.logarea)
        while True:
            area = raw_input("Enter AREA[0=EXIT]==>")
            try:
                if area == '0':
                    sys.exit()
                if self.logarea.get(area):
                    outStr = "Scanned area[%s]"% self.logarea.get(area)
                    print UseStyle(outStr, fore='blue')
                    break
                else:
                    print "Selected wrong option-->%s"% area
            except ValueError:
                print "Input wrong option"
                continue
        return self.logarea.get(area)

    def asklogType(self):
        self.displayItem(self.logtype)
        while True:
            logType = raw_input("Enter find log type[0=EXIT]==>")
            try:
                if logType == '0':
                    sys.exit()
                if self.logtype.get(logType):
                    outStr = "Scanned area[%s]"% self.logtype.get(logType)
                    print UseStyle(outStr, fore='blue')
                    break
                else:
                    print "Selected wrong option-->%s"% logType
            except ValueError:
                print "Input wrong option"
                continue
        return self.logtype.get(logType)

class zipFile(object):
    def __init__(self):
        pass

    def zipFileList(self, filelist):
        zipFileName = "log.zip"
        zf = zipfile.ZipFile(zipFileName, "a", zipfile.ZIP_DEFLATED)
        for logFile in filelist:
            zf.write(logFile)
        zf.close()
        return zipFileName

    def getFilename(self, filelist):
        zipFileList = []
        for azipfile in filelist:
            zfile = zipfile.ZipFile(azipfile)
            for aZipFile in zfile.namelist(): 
                zipFileList.append(aZipFile)
            zfile.close()
        return zipFileList

    def extraFile(self, filelist):
        for azipfile in filelist:
            zfile = zipfile.ZipFile(azipfile)
            zfile.extractall()
            zfile.close()

class GetFtpFile(object):
    def __init__(self):
        self.baseFtpFolder = "BU3"

    def clear(self):
        OS = platform.system()
        if (OS == u"Windows"):
            os.system('cls')
        else:
            os.system('clear')

    def chDir(self):
        os.chdir('/usr/auto')
        if 'testlog' not in os.listdir('.'):
            os.mkdir('testlog')
            os.chmod('testlog',0777)
        os.chdir('testlog')

    def getFtpFileMain(self):
        while True:
            ml = MyLog()
            scanSN = ScanSernum()
            SN = scanSN.scanMain()
            snlist = []
            if "/" in SN:	#Input file
                with open(SN,'r') as snfile:
                   for asn in snfile.readlines():
                       if "FDO" in asn:
                           snlist.append(asn.strip())
            else:
                snlist.append(SN)
            myarea = ScanAreaType()
            logarea = myarea.askArea()
            logtype = myarea.asklogType().lower()
            if "&" in logtype:
                logtype = "FDO"   #Copy mview and mtype
            else:
                logtype = logtype[1:]   #the logtype finally value is type or view
	    logList = []
            for sn in snlist:
	            pcsn = GetPCSN()
	            pcsntuple = pcsn.getMain(sn)
	            childsn = pcsntuple[0]
	            parentsn = pcsntuple[1]
	            self.chDir()
	            getlogpath = GetLogPath()
	            childFolderList = getlogpath.getMain(parentsn,childsn,logarea)
	            input_str = '>>>>Start find SN: %s/%s test log in ftp server'%(childsn, parentsn)
	            ml.info(input_str)
	            print UseStyle(input_str, fore='blue')
	            for childFolder in childFolderList:
	                if "KFCR" in childFolder:
	                    KFCRYear = int(childFolder.split('/')[1])
	                    KFCRWeek = int(childFolder.split('/')[3][2:])
	                    #Rename the KFCR log name during copying it to ftp server on 2018/3/2
	                    if KFCRYear <= 2018 and KFCRWeek < 10 or KFCRYear == 2017:
	                        logtype = "FDO"    #Both mtype and mview will in zip file, eg:FDO2114B0KD_1491454226.zip
	                myftp = LoginFTP()
	                ftp = myftp.ftpserver()
                        ftp.cwd('/')	#Enter the FTP top folder
	                ftp.cwd(self.baseFtpFolder)
	                try:
	                    ftp.cwd(childFolder)
	                    for fileList in ftp.nlst():
	                        if (childsn in fileList or parentsn in fileList) and logtype in fileList:
	                            input_str = '--->Copy file:%s to %s'%(fileList,os.getcwd())
	                            print UseStyle(input_str, fore='blue')
	                            ml.info(input_str)
				    if not os.path.lexists(fileList):    #Log already exist in /usr/auto/testlog
	                                mydlfile = DLFtpFile()
	                                mydlfile.downloadFile(ftp, fileList)
	                            logList.append(fileList)
	                except Exception, err:	#The script still running although met error
	                    outStr = r"!!!No file in C:/Backup/BU3/%s in FTP server, ERR:%s"%(childFolder,err)
	                    print UseStyle(outStr, fore='black', back='yellow')
	                    if len(childFolderList) == 1: break
	                finally:
                            pass
	                    #ftp.quit()
            else:    #Run after for finished
                ftp.quit()
                if len(logList) >0:
                    mymail = MailVerify()
                    mailResult = ()
                    mailResult = mymail.mailVf()
                    zfClass = zipFile()
		    zipOriFileName = zfClass.getFilename(logList)	
                    zfClass.extraFile(logList)
                    if mailResult[0] == "N" or len(snlist) > 1:	#Avoid hurge attachment, option f=File will not send mail
                        outStr = "----------------------------------------------------------------------------"
                        print UseStyle(outStr, fore='blue')
                        outStr = "--->The log saved in local folder:%s, file name as below" % os.getcwd()
                        print UseStyle(outStr, fore='blue')
                        for aFile in zipOriFileName:
                            outStr = "|| {0}".format(aFile)
                            print UseStyle(outStr, fore='blue')
                        outStr = "----------------------------------------------------------------------------"
                        print UseStyle(outStr, fore='blue')
                    else:
                        if "Linux" in platform.system():    #Only send mail in linux
                            outStr = "----------------------------------------------------------------------------"
                            print UseStyle(outStr, fore='blue')
                            mailAdd = mailResult[1]
                            mailAttachment = zfClass.zipFileList(zipOriFileName)
                            mailSubject = "{0} TestLog".format(snlist[0])
                            pp = subprocess.Popen("echo 'TestLog' | mutt -s '%s' -a %s %s"%(mailSubject,mailAttachment,mailAdd),\
                                                  stdout=subprocess.PIPE, shell=True)
                            pp.communicate()
                            time.sleep(15)
                            if pp.returncode != 0:
                                outStr = "####Send mail failed, ending the routine....\n"
                                print UseStyle(outStr, mode='bold', fore='white', back='red')
                                ml.info(outStr)
                                EXIT()
                            else:
                                outStr = "|| Send mail successfully: %s"% mailAdd
                                print UseStyle(outStr, fore='blue')
                                ml.info(outStr)
                                for alog in zipOriFileName:	#Remove decompress log file in local server
                                    os.remove(alog)
                                os.remove(mailAttachment)	#Remove the mail attachment in local server
                            outStr = "----------------------------------------------------------------------------"
                            print UseStyle(outStr, fore='blue')
                        else:
                            outStr = "###This script only can be used in Linux, no mail will be sent###"
                            print UseStyle(outStr, mode='bold', fore='white', back='red')

                    for blog in logList:	#Remove zip log file at finally
                        os.remove(blog)
                else:
                    outStr = "#####No log be found for %s in FTP server"%sn
                    print UseStyle(outStr, mode='bold', fore='white', back='yellow')
	 	    pass

            canswer = (raw_input("Continue or 0=End ==>")).upper()
            if canswer == "E": sys.exit()
            else:
                self.clear()

if __name__ == "__main__":
    getf = GetFtpFile()
    getf.getFtpFileMain()

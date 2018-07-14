#!/home/alexyi/python2.7/local/bin/python
# -*- coding: utf-8 -*

import sys
import subprocess
from datetime import date
from products import products     #Self customize module
from font import UseStyle    #Self customize module
from EXIT import EXIT     #Self customize module

class GetLogPath(object):
    def __init__(self):
        pass

    def getMain(self, psernum, csernum, area='ALL'):
        logList = []
        sernumlist = []
        sernumlist.append(psernum)
        sernumlist.append(csernum)
        sernumlist = set(sernumlist)
        for sernum in sernumlist:
            OUTPUT = self.getOutput(sernum)
            LOGLIST = self.getLogList(OUTPUT,area)
            for loglt in LOGLIST:
                logList.append(loglt)
        return set(logList)
            

    def getLogList(self, output, area):
        loglist = []
        alst = output.split('\n')
        for lst in alst:
            blst = lst.split()
            if "S" in blst:
                DATE = blst[0]
                YW = self.getYearWeek(DATE)
                Year = YW[0]
                Week = YW[1]
                UUTtype = blst[5]
                #KFCR use PID as UUTTYPE
                if not "WS" in UUTtype and not "C6800" in UUTtype:
                    UUTtype = blst[5][:-3]
	        UUTTYPE = products.get(UUTtype)
		if UUTTYPE != "None":    #None means the UUT be tested in DF site             
	            #Define the log directory in ftp server
	            AREA = blst[7]
	            astr = ""
	            if area == "ALL":
	                AREANAME = self.getFTPAreaName(AREA, UUTTYPE)
                        if AREANAME != "":
		            astr = "%s/%s/%s/%s"%(UUTTYPE,Year,AREANAME,Week)
		            #Hipot and ORT don't archive log in local server
		            if astr not in loglist: #Exclude duplicate item
		                loglist.append(astr)
	            else:
	                if area == "RUNIN": area = "BI"
	                if area == "FQA": area = "SYSDL;SYSFT;PCBDL;PCBFT"
	                if area in AREA or AREA in area:
	                    AREANAME = self.getFTPAreaName(AREA, UUTTYPE)
                            if AREANAME != "":
	                        astr = "%s/%s/%s/%s"%(UUTTYPE,Year,AREANAME,Week)
	                        loglist.append(astr)
        #logList = ['CSR/2017/ASSY/WK47']
        return loglist

    def getOutput(self,sernum):
        #Already do snpull in getPCSN.py
        #p = subprocess.Popen(['agen.exe','snpull','MAN~',sernum], stdout=subprocess.PIPE)
        #output, error = p.communicate()
        #if p.returncode != 0:
        #    outStr = "snpull failed"
        #    print UseStyle(outStr, fore='black', back='yellow')
        p1 = subprocess.Popen(['/usr/auto/bin/snfind', sernum, ' 0'], stdout=subprocess.PIPE)
        output = p1.communicate()[0]
        if p1.returncode != 0:
            outStr = "####snfind failed, ending the routine....\n"
            print UseStyle(outStr, mode='bold', fore='black', back='red')
            EXIT()
        return output

    def getYearWeek(self,DATE):
        YearWeekList = []
        Date = DATE.split('/')
        month = int(Date[0])
        day = int(Date[1])
        year = int("20" + Date[2])
        YEAR = str(year)
        YearWeekList.append(YEAR)
        dt = date(year,month,day)
        Week = dt.isocalendar()[1]
        WEEK = 'WK' + str(Week)
        YearWeekList.append(WEEK)
        return YearWeekList

    def getFTPAreaName(self, Area, UUTTYPE):    #Define the test area name in FTP server
        AREANAME = ""
        if Area == "PCBST": AREANAME = "BST"
        if Area == "PCB2C": AREANAME = "2C"
        if Area == "ASSY": AREANAME = "ASSY"
        if Area == "SYSBI" or Area == "PCBBI": AREANAME = "RI"
        #Only for KFCR, exclude DF SYSFT test
        if Area == "SYSFT" and UUTTYPE == "KFCR": AREANAME = "FQA"
        if Area == "PCBDL" or Area == "PCBFT" or Area == "SYSDL":
            AREANAME = "FQA"
        return AREANAME

if __name__ == "__main__":
    myRun = GetLogPath()
    sn = sys.argv[1:]
    psn = sn[0]
    if len(sn) == 1: csn = psn
    else:
        csn = sn[1]
    logarea = "ALL"
    if len(sn) == 3: logarea = sn[2]
    print myRun.getMain(psn,csn, logarea)

#!/usr/bin/env /home/alexyi/python2.7/local/bin/python
# -*- coding: utf-8 -*

import os
import sys
import subprocess
from products import products    #Self customize module
from font import UseStyle    #Self customize module
from EXIT import EXIT     #Self customize module

class GetPCSN(object):
    def __init__(self):
	#Compile the agen file
	#orgPath = os.path.abspath('.')
	#os.chdir('/home/alexyi/py/getlog')    #Change to genparent.agen path
        #For other user using this script, change to genparent.agen path
	os.chdir('/home/alexyi/CMN/getlog')
	p = subprocess.Popen(['/usr/auto/bin/agencmp', 'genparent'],stdout=subprocess.PIPE)
	output, error = p.communicate()
	if p.returncode != 0:
            outStr = "genparent.agen complie fail"
	    print UseStyle(outStr, fore='black', back='yellow')
	#os.chdir(orgPath)

    def getMain(self, sernum):
        TYPE = "P"
        if ord(sernum[7]) > 64: TYPE = "C"
	#Do snpull
        if TYPE == "P":
            pp = subprocess.Popen(['agen.exe','snpull','MAN~',sernum], stdout=subprocess.PIPE)
	else:
            pp = subprocess.Popen(['agen.exe','snpull','MAN~', '-c', sernum], stdout=subprocess.PIPE)
        output, error = pp.communicate()
        if pp.returncode != 0:
            outStr = "snpull failed"
            print UseStyle(outStr, fore='black', back='yellow')

        #Capture parenet SN/Children SN
        p1 = subprocess.Popen(['agend.exe','genparent',TYPE,sernum],stdout=subprocess.PIPE)
        output = p1.communicate()[0]
        if p1.returncode != 0:
            outStr = "####Get parent/child fail, ending the routine....\n"
            print UseStyle(outStr, mode='bold', fore='white', back='red')
            EXIT()
        csn = ''
        psn = ''
        if TYPE == "C":
            psn = sernum
            alst = output.split('\n')
            for astr in alst:
                if '->' in astr:
                    #blst = ['->', 'FDO2146KG85,', 'BLWR-RPS2300=', '(ASSY)']
                    blst = astr.split()
                    if products.get(blst[2][:-3]):
                        csn = blst[1][:-1]
        else:
            csn = sernum
            #alst = ['Top', 'Level', 'S/N', ':', 'FDT2149PG0C,', 'PWR-RPS2300', '(ASSY)']
            alst = output.split('\n')[0].split()
            psn = alst[4][:-1]

        csn = pcn if csn == "NONE" else csn
        psn = csn if psn == "NONE" else psn
        csn = psn if csn == "" else csn
        psn = csn if psn == "" else psn

        return (csn,psn)

if __name__ == "__main__":
    myRun = GetPCSN()
    sn = sys.argv[1:]
    #print myRun.getMain("FDO2148B08X")
    print myRun.getMain(sn[0])

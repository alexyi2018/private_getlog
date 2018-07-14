#!/usr/bin/env /home/alexyi/python2.7/local/bin/python
# -*- coding: utf-8 -*-

import re

class MailVerify(object):
    def __init__(self):
        self.maddress = re.compile(r'[^\._][\w\._-]+@[A-Za-z0-9]+\.+[A-Za-z]+$')
    
    def mailVf(self):
        while True:
            answer = (raw_input("Send Mail[Y=Yes, N=No] ==>")).upper()
            try:
                if answer == "Y":
                    #pls use space as delim if you want to send to multiple person
                    mailadd = (raw_input("Enter your mail address==>")).lower()
                    maillist = mailadd.split()
                    for maila in maillist:
                        if self.maddress.match(maila):
                            validate_result = True
                        else:
                            validate_result = False
                            break
                    if validate_result: break
                elif answer == "N":
                    mailadd = ""
                    break
                else:
                    print "Input wrong option,pls input Y/N"
            except ValueError:
                print "Input wrong value"
                continue
        return (answer,mailadd)

if __name__ == "__main__":
    mymail = MailVerify()
    mymail.mailVerify()

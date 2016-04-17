# /usr/bin/vrc2ftpComplete.py
# derived from vrc2ftp.py (2014-11-14)
# 2016-04-17
# Michael Gries
# depending on cronjob the complete day data 
# will be stored separatly at 00:00h

sourcefile = "vrcDayDetailed.txt"
targetfile = "vrcDayDetailed.txt"

import sys
# filenameArgv1 = str(sys.argv[1])
# print("argv[1]: " + filenameArgv1)

command = "STOR " + targetfile 
print("ftp: " + command)

fobj_in = open(sourcefile)

from ftplib import FTP
ftp=FTP("www.gries.name")
ftp.login("3376-227","45780176")
ftp.cwd("/VRC")
ftp.storlines(command, fobj_in)
ftp.close()
print("ftp: done")

fobj_in.close()

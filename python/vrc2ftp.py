# /usr/bin/ftpTransferDataViaArgv1.py
# 2014-11-14
# Michael Gries

sourcefile = "vrc2008day.txt"

import sys
# sys.path.insert(0, '/usr/lib/python2.7/bridge/')
#csys.path.append ('/usr/lib/python2.7/bridge/')
# filenameArgv1 = str(sys.argv[1])
# print("argv[1]: " + filenameArgv1)

command = "STOR " + sourcefile
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

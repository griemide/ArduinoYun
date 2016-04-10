# /usr/bin/ftpDataViaArgv1.py
# 2014-09-25
# Michael Gries

import StringIO
from ftplib import FTP

import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge/')                                          
#sys.path.append ('/usr/lib/python2.7/bridge/')                                          
from bridgeclient import BridgeClient as bridgeclient

value = bridgeclient()
ScetchVersion = value.get("version")

testString = "T[1][244]=8.5; T[2][244]=65.1; T[3][244]=83.1; T[4][244]=76.5; S[1][244]=1026;"

filenameArgv1 = str(sys.argv[1])
print("argv[1]: " + filenameArgv1)
ftpAppendFile = "APPE " + filenameArgv1 

myFileIO = StringIO.StringIO()

#myFileIO.write("TestFTPviaPython")
#myFileIO.write(",")
#myFileIO.write(ScetchVersion)
myFileIO.write(testString)
myFileIO.write('\n')
myFileIO.seek(0)
ftp=FTP("www.gries.name")
ftp.login("3376-227","45780176")
ftp.cwd("/VRC")
ftp.storlines(ftpAppendFile ,myFileIO)
ftp.close()
myFileIO.close()

#-------------------------------------------------------------------------------
# Name:       vrcTest.py
# Purpose:    build javascript file of data records to be displayed
#
# Author:     Michael Gries (griemide)
# Copyright:  (c) 2014, Michael Gries
#
# History:
# 2015-02-21  test records to check javascript array object handling
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

sourcefilename = "vrc_2014-11-07.log"  # default
destinationfilename = "vrc2008day.txt" # standard output file
ftpTransferScript = "vrc2ftp.py"
datagramSize = 67

import sys
cntArgv = len(sys.argv)
if (cntArgv > 1):
   sourcefilename = str(sys.argv[1])
   print("argv[1]: " + sourcefilename)
else:
   print("argv[1]: n/a \n")
print("Source : " + sourcefilename)


posStatus  = 18
posSekunde = 22
posMinute  = 23
posStunde  = 24
posAussen  = 32
posWasser  = 35
posKessel  = 38
posHeiz_k  = 47
posBetrieb = 65

lastMinuteHex = "FF"
h1hhmmss  = "24:59:59" # 24 h Format
t1Aussen  = 10
t2Wasser  = 50
t3Kessel  = 80
t4Heiz_k  = 99
s1Status  = 00
b1Betrieb = 99

headerTxt = "// H[1]=Zeitstempel;   T[1]=Aussentemp;  T[2]=Wassertemp; T[3]=Kesseltemp; T[4]=Heizkurve;  S[1]=B.-Status;  // line\n"
layoutOld = "T[1][i]  =10.0; T[2][i]  =50.0; T[3][i]  =80.0; T[4][i]  =99.0; S[1][i]  =0; "
layoutNew = "H[1][iiii]='24:59:59'; T[1][iiii]=+ 9.9; T[2][iiii]=50.0; T[3][iiii]=80.0; T[4][iiii]=99.0; S[1][iiii]=0000; // zzzz"

iHHMM = "000000000"

T1 = 10
T2 = 20
T3 = 30
T4 = 40

# Function definition

def checkNextMinute(datagram, pos):
    "extract minute value out of dataset"
    result = False
    datagramRawDataLength = 203
    if ( len(datagram) == datagramRawDataLength):
       dataset = datagram.split()
       global lastMinuteHex
       minuteHex = dataset[pos]
       print minuteHex
       if (minuteHex != lastMinuteHex):
          result = True
          lastMinuteHex = minuteHex
    return result

def getTimestamp(dataset, posSekunde, posMinute, posStunde):
    intHex = dataset[posSekunde]
    intSekunde = int(intHex, base=16)
    intHex = dataset[posMinute]
    intMinute = int(intHex, base=16)
    intHex = dataset[posStunde]
    intStunde = int(intHex, base=16)
    Timestamp = "%02d" % intStunde + ":" + "%02d" % intMinute + ":" + "%02d" % intSekunde
    return Timestamp

def getByte(dataset, pos):
    "build integer string out of one datagram bytes"
    byteHex = dataset[pos]
    integerValue = int(byteHex, base=16)
    return "%02d" % integerValue

def getWord(dataset, pos):
    "build integer string out of two datagram bytes"
    wordHex = dataset[pos] + dataset[pos +1]
    integerValue = int(wordHex, base=16)
    return "%04d" % integerValue

def getFloat(dataset, pos):
    "build float string out of two datagram bytes"
    wordHex = dataset[pos] + dataset[pos +1]
    integerValue = int(wordHex, base=16)
    floatValue = float(float(integerValue) / 16)
    floatValueString = "%04.1f" % floatValue
    return floatValueString

def getFloatSigned(dataset, pos):
    "build float string out of two datagram bytes"
    wordHex = dataset[pos] + dataset[pos +1]
    integerValue = int(wordHex, base=16)
    if ((integerValue & 0x8000) > 0 ):
        integerValue = integerValue - 0x10000
    floatValue = float(float(integerValue) / 16)
    floatValueString = "%+ 5.1f" % floatValue
    return floatValueString

def aggregateData(noOfTimestamps, line, datagram):
   " build aggregated dat out of datagram"
   global b1Betrieb # for last record in destination file
   global iHHMM # record position in array H[1][iHHMM]
   datagramRawDataLength = 203
   if ( len(datagram) == datagramRawDataLength):
      dataset = datagram.split()
      h1hhmmss = getTimestamp(dataset, posSekunde, posMinute, posStunde)
      iHHMM = h1hhmmss[:2] + h1hhmmss[3:5]  # nur Stunde und Minute ohne Trennzeichen
      h1Timestamp  = "H[1][" + "%04d" % noOfTimestamps + "]='" + h1hhmmss + "'; "
      t1Aussen = getFloatSigned(dataset, posAussen)
      t1AussenText = "T[1][" + "%04d" % noOfTimestamps + "]=" + t1Aussen + "; "
      t2Wasser = getFloat(dataset, posWasser)
      t2WasserText = "T[2][" + "%04d" % noOfTimestamps + "]=" + t2Wasser + "; "
      t3Kessel = getFloat(dataset, posKessel)
      t3KesselText = "T[3][" + "%04d" % noOfTimestamps + "]=" + t3Kessel + "; "
      t4Heiz_k = getFloat(dataset, posHeiz_k)
      t4Heiz_kText = "T[4][" + "%04d" % noOfTimestamps + "]=" + t4Heiz_k + "; "
      s1Status = getWord(dataset, posStatus)
      s1StatusText = "S[1][" + "%04d" % noOfTimestamps + "]=" + s1Status + "; "
      commentText = "// %4d" % line + " %4s" % iHHMM
      aggregatedRow = h1Timestamp + t1AussenText + t2WasserText + t3KesselText + t4Heiz_kText + s1StatusText + commentText
      b1Betrieb = getByte(dataset, posBetrieb) # for last record in destination file
   else:
      aggregatedRow = "Error"
   return aggregatedRow;

def aggregateFillingData(noOfTimestamps, line, pseudotimestamp):
   " build aggregated filling data with out of Spec values"
   global T1
   global T2
   global T3
   global T4
   if (True):
      h1hhmmss = pseudotimestamp[:2] + ":" + pseudotimestamp[2:4] + ":00"
      h1Timestamp  = "H[1][" + "%04d" % noOfTimestamps + "]='" + h1hhmmss + "'; "
      t1Aussen = str(T1)
      t1AussenText = "T[1][" + "%04d" % noOfTimestamps + "]=" + t1Aussen + "; "
      t2Wasser = str(T2)
      t2WasserText = "T[2][" + "%04d" % noOfTimestamps + "]=" + t2Wasser + "; "
      t3Kessel = str(T3)
      t3KesselText = "T[3][" + "%04d" % noOfTimestamps + "]=" + t3Kessel + "; "
      t4Heiz_k = str(T4)
      t4Heiz_kText = "T[4][" + "%04d" % noOfTimestamps + "]=" + t4Heiz_k + "; "
      s1Status = "0000"
      s1StatusText = "S[1][" + "%04d" % noOfTimestamps + "]=" + s1Status + "; "
      commentText = "// %4d" % line
      aggregatedRow = h1Timestamp + t1AussenText + t2WasserText + t3KesselText + t4Heiz_kText + s1StatusText + commentText
   else:
      aggregatedRow = "Error"
   return aggregatedRow;

# main

fobj_in = open(sourcefilename)
fobj_out = open(destinationfilename,"w")

from datetime import datetime
import time
timestamp = datetime.now()
timeStarted = time.time()
vrcSource = "// Sourcefile: %s \n" % sourcefilename
vrcStamp1 = "// generation: %s started \n" % timestamp.strftime('%Y-%m-%d %H:%M:%S')
vrcAuthor = "// (c) 2014, Michael Gries \n"
vrcBlank0 = "//  \n"
vrcHeader = vrcSource + vrcStamp1 + vrcAuthor + vrcBlank0
fobj_out.write(vrcHeader)
vrcRefNo1 = "// http://de.selfhtml.org/javascript/objekte/array.htm#assoziative_arrays \n"
vrcRefNo2 = "// Anm.1: in eckiger Klammer nur Zahlen oder Strings in Hochkommas. \n"
vrcRefNo3 = "// Anm.2: verschiedene Arrays m?glich (hier T[] und V[] \n"
vrcReference = vrcRefNo1 + vrcRefNo2 + vrcRefNo3
fobj_out.write(vrcReference)
vrcVar_B_ = "var B = new Array();     // Betriebsart des letzten Datensatzes \n"
vrcNew_B1 = "    B[1] = new Object(); // Beispiel '00'=Sommerbetrieb, '01'=Winterbetrieb \n"
vrcVar_N_ = "var N = new Array();     // Dateiname der Quelldatensaetze \n"
vrcNew_N1 = "    N[1] = new Object(); // Beispiel vrc_2014-09-30.log \n"
vrcVar_H_ = "var H = new Array();     // Zeitstempel \n"
vrcNew_H1 = "    H[1] = new Object(); // hh:mm:ss \n"
vrcVarXXX = vrcVar_B_ + vrcNew_B1 + vrcVar_N_ + vrcNew_N1 + vrcVar_H_ + vrcNew_H1
fobj_out.write(vrcVarXXX)
vrcVar_T_ = "var T = new Array();     // Temperaturwerte \n"
vrcNew_T1 = "    T[1] = new Object(); // Aussentemperatur \n"
vrcNew_T2 = "    T[2] = new Object(); // Wassertemperatur \n"
vrcNew_T3 = "    T[3] = new Object(); // Kesseltemperatur \n"
vrcNew_T4 = "    T[4] = new Object(); // Heizkurve \n"
vrcVar_S_ = "var S = new Array();     // Statuswerte \n"
vrcNew_S1 = "    S[1] = new Object(); // Betriebszustand \n"
vrcVarXXX = vrcVar_T_ + vrcNew_T1 + vrcNew_T2 + vrcNew_T3 + vrcNew_T4 + vrcVar_S_ + vrcNew_S1
fobj_out.write(vrcVarXXX)
vrcBlank1 = "// Allgemeiner Parameter zur Darstellung der Quelldatendatei \n"
vrcN1Para = "   N[1][1]='%s';         // Name der Quelldatei auf Server\n" % sourcefilename
vrcHeader = vrcBlank1 + vrcN1Para + headerTxt
fobj_out.write(vrcHeader)

print(vrcStamp1)

i = 1000
hh = 0
while(hh < 24):
    mm = 0
    T1 = 10; T2 = 20; T3 = 30; T4 = 40
    while(mm < 60):
        count = hh * 100 + mm
        countTimestamp = "%02d" % hh + "%02d" % mm
        vrcFillingData = aggregateFillingData(i, count, countTimestamp)
        print(vrcFillingData)
        fobj_out.write(vrcFillingData  + "\n")
        i = i + 1
        T1=T1+1; T2=T2+1; T3=T3+1; T4=T4+1
        mm = mm + 1
    hh = hh + 1

vrcBlank2 = "// Betriebsart auf Basis des letzten Datensatzes darstellen \n"
vrcB1Para = "   B[1][1]='%s'; // Betriebsart: '00'=Sommerbetrieb; '01'=Winterbetrieb \n" % b1Betrieb
timestamp = datetime.now()
timeEnded = time.time()
timeTotal = timeEnded - timeStarted
vrcStamp2 = "// generation: %s ended " % timestamp.strftime('%Y-%m-%d %H:%M:%S') + "(%.1f seconds)\n" % timeTotal
vrcEOFdef = "// EOF \n"
vrcFooter = vrcBlank2 + vrcB1Para + vrcStamp2 + vrcEOFdef
fobj_out.write(vrcFooter)
fobj_in.close()
fobj_out.close()

print("\n")
vrcStatus = vrcStamp2 + "// %s " % sourcefilename + "-> vrc2008day.txt \n"
print(vrcStatus)
vrcScript = "start transfering 'vrc2008day.txt' via script '" + ftpTransferScript + "' ...\n"
print(vrcScript)
execfile("vrc2ftp.py")

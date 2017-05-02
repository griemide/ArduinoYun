#-------------------------------------------------------------------------------
# Name:       vrc.py
# Purpose:    build javascript file of data records to be displayed
#
# Author:     Michael Gries (griemide)
# Copyright:  (c) 2014-2017, Michael Gries
#
# History:
# 2014-11-09  first creation
# 2014-11-27  support for neg. outdoor values - def getFloatSigned()
# 2015-02-19  Var objects added (to be independent
#             to SSI support on hosted web sites)
# 2015-02-20  filling lines (for pixels) if empty data records identified
# 2015-03-15  calculation total heating time per day
# 2015-03-17  calculation total heating periods per day
# 2015-03-23  execution of servicemail.py added
# 2015-03-28  Arduino Yun bridgeClient of python added
# 2015-03-30  Min/Max values (Aussentemperatur) added
# 2015-04-04  service request via SMS added (Nexmo)
# 2017-01-29  service notification modified (send only at given time 20:00h)
# 2017-02-07  service notification modified (send only once after detection)
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

DEBUG = False      # False == ignore Yun specific commands when running on PC

version = "17.1.29"

sourcefilename = "vrc_2015-01-27.log"  # default
destinationfilename = "vrc2008day.txt" # standard output file
serviceStatusFilename = "service.ini"  # stores service related data
ftpTransferScript = "vrc2ftp.py"
fileServiceScript = "service/servicemail.py"
fileSendSMSScript = "service/sendSMSviaNexmo.py"
datagramSize = 67

import sys
cntArgv = len(sys.argv)
if (cntArgv > 1):
   sourcefilename = str(sys.argv[1])
   print("argv[1]: " + sourcefilename)
else:
   print("argv[1]: n/a (using default file) \n")
print("Source : " + sourcefilename)

#2015-03-28 {
if DEBUG:
    sys.path.insert(0, 'C:/Users/Public/Downloads/PortablePython/Portable Python 2.7.6.1/App/Lib/bridge/')
else:
    sys.path.insert(0, '/usr/lib/python2.7/bridge/')
from bridgeclient import BridgeClient as bridgeclient
value = bridgeclient()
if not DEBUG:
    value.put("scriptname","vrc.py")
    value.put("scriptversion",version)
#2015-03-28 }

posStatus  = 18
posSekunde = 22
posMinute  = 23
posStunde  = 24
posAussen  = 32
posWasser  = 35
posKessel  = 38
posHeiz_k  = 47
posBetrieb = 65

# initialising globals
lastMinuteHex = "FF"
iHHMM = "0000"
sYYYYMMDD  = "2015-00-00"
sH1hhmmss  = "24:59:59" # 24 h Format
sT1Aussen  = "-10"
sT1AusMin  = "n/a"
sT1AusMax  = "n/a"
sT2Wasser  = "-10"
sT3Kessel  = "90.0"
sT4Heiz_k  = "70.9"
sS1Status  = "Bereitschaft"
sB1Betrieb = "01"
sL1Status  = "lamp_off"
sL2Service = "lamp_off"
sC1Brennerdauer = "0"
sC2Brennerstarts = "0"

# calculation globals
fT1Aussen = 99.9        # float value for min/max comparison
t1AussenMin = +99.9     # default (first values will overright default)
t1AussenMax = -99.9     # default (first values will overright default)
c0Service = 0           # manage service detection (default no service)
c0ServiceOnce = False   # send service notification on first detection
c0ServiceSMS = False    # send service notification via SMS only once
c1Seconds = 10          # sample rate of monitoring system in seconds
c1Totals  = 0           # totals of heading time per sample rate in seconds
c2PeriodTotals = 0      # totals of heading period per day
c2PeriodStatus = False  # status of new  checked sample (0-no heating / 1-heating)
c2PeriodLast   = False  # status of last checked sample (0-no heating / 1-heating)
                        # heating period: count on rising edge of c1PeriodStatus^c1PeriodLast (NOR gate)

headerTxt = "// H[1]=Zeitstempel;   T[1]=Aussentemp;  T[2]=Wassertemp; T[3]=Kesseltemp; T[4]=Heizkurve;  S[1]=B.-Status;  // line hhmm\n"
layoutOld = "T[1][i]  =10.0; T[2][i]  =50.0; T[3][i]  =80.0; T[4][i]  =99.0; S[1][i]  =0; "
layoutNew = "H[1][iiii]='24:59:59'; T[1][iiii]=+ 9.9; T[2][iiii]=50.0; T[3][iiii]=80.0; T[4][iiii]=99.0; S[1][iiii]=0000; // zzzz hhmm"
# Attention: usage of array index iiii only with non leading zeros to avoid misalignments within the array
# use Javascript Debugger of IE9 (F12 Entwicklertools) for array debugging


# Function definition

def checkService(datagram, pos):
    import binascii
    "extract status value out of dataset"
    result = False
    datagramRawDataLength = 203
    if ( len(datagram) == datagramRawDataLength):
       dataset = datagram.split()
       wordHex = dataset[pos]
       print wordHex
       intHex = int(wordHex)
       binMask = intHex & 0b00000001 # LSB of [pos]
       if (binMask != 0):
          result = True # entspricht Wartung
    return result

def checkHeatingTime(datagram, pos):
    "extract status value out of dataset"
    result = False
    datagramRawDataLength = 203
    if ( len(datagram) == datagramRawDataLength):
       dataset = datagram.split()
       wordHex = dataset[pos] + dataset[pos +1]
       print wordHex
       intHex = int(wordHex)
       intMask = intHex & 3
       if (intMask != 0):
          result = True
    return result

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
    global fT1Aussen
    wordHex = dataset[pos] + dataset[pos +1]
    integerValue = int(wordHex, base=16)
    if ((integerValue & 0x8000) > 0 ):
        integerValue = integerValue - 0x10000
    floatValue = float(float(integerValue) / 16)
    fT1Aussen = floatValue
    floatValueString = "%+ 5.1f" % floatValue
    return floatValueString

def aggregateData(noOfTimestamps, recordNo, datagram):
   " build aggregated dat out of datagram"
   global b1Betrieb # for last record in destination file
   global iHHMM # record position in array H[1][iHHMM]
   global sH1hhmmss, sT1Aussen, sT2Wasser, sT3Kessel, sT4Heiz_k, sS1Status
   global fT1Aussen, t1AussenMin , t1AussenMax
   datagramRawDataLength = 203
   if ( len(datagram) == datagramRawDataLength):
      dataset = datagram.split()
      h1hhmmss = getTimestamp(dataset, posSekunde, posMinute, posStunde)
      iHHMM = h1hhmmss[:2] + h1hhmmss[3:5]  # nur Stunde und Minute ohne Trennzeichen
      h1Timestamp  = "H[1][" + "%04d" % noOfTimestamps + "]='" + h1hhmmss + "'; "
      sH1hhmmss = "%s" % h1hhmmss # for bridge.put
      t1Aussen = getFloatSigned(dataset, posAussen)
      if (fT1Aussen < t1AussenMin):
          t1AussenMin = fT1Aussen
      if (fT1Aussen > t1AussenMax):
          t1AussenMax = fT1Aussen
      t1AussenText = "T[1][" + "%04d" % noOfTimestamps + "]=" + t1Aussen + "; "
      sT1Aussen = "%s" % t1Aussen # for bridge.put
      t2Wasser = getFloat(dataset, posWasser)
      t2WasserText = "T[2][" + "%04d" % noOfTimestamps + "]=" + t2Wasser + "; "
      sT2Wasser = "%s" % t2Wasser # for bridge.put
      t3Kessel = getFloat(dataset, posKessel)
      t3KesselText = "T[3][" + "%04d" % noOfTimestamps + "]=" + t3Kessel + "; "
      sT3Kessel = "%s" % t3Kessel # for bridge.put
      t4Heiz_k = getFloat(dataset, posHeiz_k)
      t4Heiz_kText = "T[4][" + "%04d" % noOfTimestamps + "]=" + t4Heiz_k + "; "
      sT4Heiz_k = "%s" % t4Heiz_k # for bridge.put
      s1Status = getWord(dataset, posStatus)
      s1StatusText = "S[1][" + "%04d" % noOfTimestamps + "]=" + s1Status + "; "
      sS1Status = "%s" % s1Status # for bridge.put
      commentText = "// %4d" % recordNo + " %4s" % iHHMM
      aggregatedRow = h1Timestamp + t1AussenText + t2WasserText + t3KesselText + t4Heiz_kText + s1StatusText + commentText
      b1Betrieb = getByte(dataset, posBetrieb) # for last record in destination file
   else:
      aggregatedRow = "Error"
   return aggregatedRow;

def aggregateFillingData(noOfTimestamps, pseudoRecordNo, pseudotimestamp):
   " build aggregated filling data with out of Spec values"
   if (True):
      h1hhmmss = pseudotimestamp[:2] + ":" + pseudotimestamp[2:4] + ":00"
      h1Timestamp  = "H[1][" + "%04d" % noOfTimestamps + "]='" + h1hhmmss + "'; "
      t1Aussen = " +0.0"
      t1AussenText = "T[1][" + "%04d" % noOfTimestamps + "]=" + t1Aussen + "; "
      t2Wasser = " 0.0"
      t2WasserText = "T[2][" + "%04d" % noOfTimestamps + "]=" + t2Wasser + "; "
      t3Kessel = " 0.0"
      t3KesselText = "T[3][" + "%04d" % noOfTimestamps + "]=" + t3Kessel + "; "
      t4Heiz_k = " 0.0"
      t4Heiz_kText = "T[4][" + "%04d" % noOfTimestamps + "]=" + t4Heiz_k + "; "
      s1Status = "0000"
      s1StatusText = "S[1][" + "%04d" % noOfTimestamps + "]=" + s1Status + "; "
      commentText = "// %4s" % pseudoRecordNo + " %4s" % pseudotimestamp
      aggregatedRow = h1Timestamp + t1AussenText + t2WasserText + t3KesselText + t4Heiz_kText + s1StatusText + commentText
   else:
      aggregatedRow = "Error"
   return aggregatedRow;

def increaseCount(countervalue):
    "counts 24 hour and 60 minutes in format 'hhmm' "
    hh = countervalue/100
    mm = countervalue%100
    mm = mm +1
    if(mm > 59):
        mm = 0
        hh = hh + 1
        if(hh > 23):
            hh = 0
    countervalue = hh * 100 + mm
    return countervalue;

# main

fobj_in = open(sourcefilename)
fobj_out = open(destinationfilename,"w")

from datetime import datetime
import time
timestamp = datetime.now()
timeStarted = time.time()
vrcSource = "// Sourcefile: %s \n" % sourcefilename
vrcStamp1 = "// generation: %s started \n" % timestamp.strftime('%Y-%m-%d %H:%M:%S')
vrcProgNo = "// Python 2.7.6.1 script 'vrc.py' version %s \n" % version
vrcAuthor = "// (c) 2014-2015, Michael Gries \n"
vrcBlank0 = "//  \n"
vrcHeader = vrcSource + vrcStamp1 + vrcProgNo + vrcAuthor + vrcBlank0
fobj_out.write(vrcHeader)
vrcRefNo1 = "// http://de.selfhtml.org/javascript/objekte/array.htm#assoziative_arrays \n"
vrcRefNo2 = "// Anm.1: in eckiger Klammer nur Zahlen oder Strings in Hochkommas. \n"
vrcRefNo3 = "// Anm.2: verschiedene Arrays m?glich (hier T[] und V[] \n"
vrcReference = vrcRefNo1 + vrcRefNo2 + vrcRefNo3
fobj_out.write(vrcReference)
vrcVar_B_ = "var B = new Array();     // Betriebsart des letzten Datensatzes \n"
vrcNew_B1 = "    B[1] = new Object(); // Beispiel '00'=Sommerbetrieb, '01'=Winterbetrieb \n"
vrcVar_C_ = "var C = new Array();     // Kalkulierte Werte aus Datensaetzen\n"
vrcNew_C1 = "    C[1] = new Object(); // Kummulierte Brennerdauer in Sekunden\n"
vrcNew_C2 = "    C[2] = new Object(); // Anzahl Brennerstarts \n"
vrcVar_N_ = "var N = new Array();     // Dateiname der Quelldatensaetze \n"
vrcNew_N1 = "    N[1] = new Object(); // Beispiel vrc_2014-09-30.log \n"
vrcVar_H_ = "var H = new Array();     // Zeitstempel \n"
vrcNew_H1 = "    H[1] = new Object(); // hh:mm:ss \n"
vrcVarXXX = vrcVar_B_ + vrcNew_B1 + vrcVar_C_ + vrcNew_C1 + vrcNew_C2 + vrcVar_N_ + vrcNew_N1 + vrcVar_H_ + vrcNew_H1
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

marker = "-"
noOfTimestamps = 1000
RecordID = 0
count = 0

for line in fobj_in:
    RecordID = RecordID + 1
    debugLine = "\n" + str(RecordID) + ": "+ line.rstrip()
    print(debugLine)
    firstRow = line.split(' ', datagramSize)
    if checkService(line, posStatus):
        c0Service = 1 # service detected
    if checkHeatingTime(line, posStatus):
        c1Totals = c1Totals + c1Seconds
        sC1Brennerdauer = "%d s" % c1Totals
        if (not (c2PeriodStatus or c2PeriodLast)): # NOR gate
           c2PeriodStatus = True   # starts heating period
           c2PeriodTotals = c2PeriodTotals + 1
           sC2Brennerstarts = "%d" % c2PeriodTotals
    else:
        c2PeriodStatus = False  # ends heating period
    if checkNextMinute(line, posMinute):
       vrcData = aggregateData(noOfTimestamps, RecordID, line)
       countRecord = int(iHHMM)
       while(count < countRecord):
            countTimestamp = "%04d" % count
            vrcFillingData = aggregateFillingData(noOfTimestamps, marker, countTimestamp)
            print(vrcFillingData)
            fobj_out.write(vrcFillingData  + "\n")
            noOfTimestamps = noOfTimestamps + 1
            count = increaseCount(count)
       debugVRCdata = str(RecordID) + ": "+ vrcData
       print(debugVRCdata)
       vrcRecord = vrcData + "\n"
       fobj_out.write(vrcRecord)
       noOfTimestamps = noOfTimestamps + 1
       count = increaseCount(count)

vrcBlank2 = "// Betriebsart auf Basis des letzten Datensatzes darstellen \n"
vrcB1Para = "   B[1][1]='%s'; // Betriebsart: '00'=Sommerbetrieb; '01'=Winterbetrieb \n" % b1Betrieb
vrcC1text = "// Kalkulierte Brennerdauer aus allen relevanten Status Datensatz berechnen \n"
vrcC1Para = "   C[1][1]='%s'; // Kalkulierte Brennerdauer (in Sekunden) \n" % c1Totals
vrcC2text = "// Anzahl Brennerstarts aus allen relevanten Status Datensatz berechnen \n"
vrcC2Para = "   C[2][1]='%s'; // Anzahl Brennerstarts \n" % c2PeriodTotals
timestamp = datetime.now()
timeEnded = time.time()
timeTotal = timeEnded - timeStarted
vrcStamp2 = "// generation: %s ended " % timestamp.strftime('%Y-%m-%d %H:%M:%S') + "(%.1f seconds)\n" % timeTotal
vrcEOFdef = "// EOF \n"
vrcFooter = vrcBlank2 + vrcB1Para + vrcC1text + vrcC1Para + vrcC2text + vrcC2Para + vrcStamp2 + vrcEOFdef
fobj_out.write(vrcFooter)
fobj_in.close()
fobj_out.close()

print("\n")
vrcStatus = vrcStamp2 + "// %s " % sourcefilename + "-> vrc2008day.txt \n"
print(vrcStatus)
vrcScript = "start transfering 'vrc2008day.txt' via script '" + ftpTransferScript + "' ...\n"
print(vrcScript)
execfile(ftpTransferScript)

#2017-05-03 {
import subprocess
print("test subprocess.call(ts.py)")
#execfile("ts.py")
#subprocess.call(['./abc.py', arg1, arg2])
subprocess.call([sys.executable,'./ts.py', sT1Aussen, sT2Wasser, sT3Kessel, sT4Heiz_k, sL1Status])
#2017-05-03 }

#2017-01-29 {
if  c0Service:
    print("service request detected ...")
    if not DEBUG:
        fobj_ser = open(serviceStatusFilename)
        if  c0ServiceOnce:
            print("sending service request once ...")
            execfile(fileServiceScript)
            c0ServiceOnce = False
        else:
            print("... service request already notified")
        SMStime = timestamp.strftime('%H')
        if (SMStime == '20'):
            print("sending service request at predefined time ...")
            execfile(fileServiceScript)
            if  c0ServiceSMS:
                print("sending service SMS notification at predefined time ...")
                execfile(fileSendSMSScript)
                c0ServiceSMS = false
else:
    print("no service request detected")
    c0ServiceOnce = True #activate for first shot after service detection
    c0ServiceSMS  = True #activate for first shot after service detection (SMS)

#2017-01-29 }

#2015-03-28 {
if not DEBUG:
    sYYYYMMDD = sourcefilename[4:14]
    value.put("Datum", sYYYYMMDD)
    value.put("Aktualisierung", sH1hhmmss)
    value.put("Log-Datei", sourcefilename)
    value.put("Betriebsart", sB1Betrieb)
    value.put("Betriebszustand", sS1Status)
    value.put("Brennerdauer", sC1Brennerdauer)
    value.put("Brennerstarts", sC2Brennerstarts)
    value.put("Aussentemperatur", sT1Aussen)
    value.put("Warmwassertemperatur", sT2Wasser)
    value.put("Kesseltemperatur", sT3Kessel)
    value.put("Heizkurve", sT4Heiz_k)
    value.put("Status", sL1Status)
    value.put("Service", sL2Service)
#2015-03-28 }

#2015-03-30 {
if not DEBUG:
    sT1AusMin = "%.1f" % t1AussenMin
    sT1AusMax = "%.1f" % t1AussenMax
    value.put("AussenMin", sT1AusMin)
    value.put("AussenMax", sT1AusMax)
#2015-03-30 }

# EOF

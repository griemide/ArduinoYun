#Vaiilant iroVIT VRC 410  Monitor

[Visualisation](http://www.gries.name/VRC/VRCday.shtm) of heating system **VKO unit** by monitoring data of **VRC 410** control unit.


## Short Description
Data of VRC 410 device will monitored, stored and and some parameters (outside temperature, boiler temp, ...) will be analysed aby an linux based embedded system and displayed on a public web service.

Following process steps required:
* permanently monitoring of received data transferred between VKO unit and VRC 410 control unit
* storing of raw data on µSDcard of embedded system for later evaluation 
* evaluation and analysing of stored data within a configured time period
* sending human readable data to external (public) web service
* Email or smsm notifications for special case (e.g. maintainance)

## Process Description
A crontab task will call periodicaly a linux script (vrc) which runs a python script (vrc.py). This python scripts reads the log-files on µSDcard and copies relevant data into a new textfile. Afterwards this textfile will be transfered to a ftp-repository on a public web server.

### Cron-Daemon (Cronjobs)

Description of **cron** syntax see [Cron](https://de.wikipedia.org/wiki/Cron)

Arduino Yun (linino folder): /etc/crontabs

File: root
Modificationcould be done via SSH or LuCI

file content:

```unix
*/5 * * * * /usr/bin/vrc
#
```

I.e. script /usr/bin/Vrc will be called every 5 minutes. It dependen on the amoung of traffic for the associated web service used how often the script should be called. For initial evaluation a 5 minutes period is choosen. later on an update period of one hour is more likely.

The Arduino Yun web interface LuCI is more convenient to set, update, activate or monitor the cron daemon.
Use:
> * **System - Scheduled Task** to set or update a secific cronjob
> * **System - Startup** to restart cron daemon
> * **Status - System Log** to check successfull restart of cron daemon (Arduino cron.info crond)


###Linux script

```script
# /usr/bin
# 2014-11-14 creaion
# 2015-02-19 copy result to 'txt' folder on local sd-card
pwd
cd /mnt/sda1/arduino/www/vrc
#
dateOfLogfile=$(date +%Y-%m-%d)
echo $dateOfLogfile
#
#
filename="vrc_"$dateOfLogfile".log"
textfile="txt/vrc_"$dateOfLogfile".txt"
echo $filename
#
python vrc.py $filename
#
cp vrc2008day.txt txt/vrc2008day.txt
cp vrc2008day.txt $textfile
echo $textfile
# 
```

Atributes of scrip file **vrc** needs to be changed to execute (chmod 755) or via FileZilla (see picture)
![chmod 755](images/vrcChangedAttributes.png)


###Python

recommended Python version 2.7.6.1

The both python scripts 
* vrc.py
* vrc2ftp.py

needs to be located in folder /mnt/sda1/arduino/www/vrc

Evaluated data will be stored in /txt/vrc_YYYY-MM-DD.log and into
file vrc2008day.txt for the ftp transfer to the outside web service repository.

#### Example of output file **http://www.gries.name/VRC/vrc2008day.txt** after transfer to web service

```javascript
// Sourcefile: vrc_2016-04-11.log 
// generation: 2016-04-11 00:10:02 started 
// Python 2.7.6.1 script 'vrc.py' version 15.4.5 
// (c) 2014-2015, Michael Gries 
//  
// http://de.selfhtml.org/javascript/objekte/array.htm#assoziative_arrays 
// Anm.1: in eckiger Klammer nur Zahlen oder Strings in Hochkommas. 
// Anm.2: verschiedene Arrays m?glich (hier T[] und V[] 
var B = new Array();     // Betriebsart des letzten Datensatzes 
    B[1] = new Object(); // Beispiel '00'=Sommerbetrieb, '01'=Winterbetrieb 
var C = new Array();     // Kalkulierte Werte aus Datensaetzen
    C[1] = new Object(); // Kummulierte Brennerdauer in Sekunden
    C[2] = new Object(); // Anzahl Brennerstarts 
var N = new Array();     // Dateiname der Quelldatensaetze 
    N[1] = new Object(); // Beispiel vrc_2014-09-30.log 
var H = new Array();     // Zeitstempel 
    H[1] = new Object(); // hh:mm:ss 
var T = new Array();     // Temperaturwerte 
    T[1] = new Object(); // Aussentemperatur 
    T[2] = new Object(); // Wassertemperatur 
    T[3] = new Object(); // Kesseltemperatur 
    T[4] = new Object(); // Heizkurve 
var S = new Array();     // Statuswerte 
    S[1] = new Object(); // Betriebszustand 
// Allgemeiner Parameter zur Darstellung der Quelldatendatei 
   N[1][1]='vrc_2016-04-11.log';         // Name der Quelldatei auf Server
// H[1]=Zeitstempel;   T[1]=Aussentemp;  T[2]=Wassertemp; T[3]=Kesseltemp; T[4]=Heizkurve;  S[1]=B.-Status;  // line hhmm
H[1][1000]='00:00:00'; T[1][1000]= +0.0; T[2][1000]= 0.0; T[3][1000]= 0.0; T[4][1000]= 0.0; S[1][1000]=0000; //    - 0000
H[1][1000]='00:01:03'; T[1][1000]= +6.9; T[2][1000]=45.1; T[3][1000]=72.4; T[4][1000]=44.7; S[1][1000]=0000; //    1 0001
H[1][1002]='00:02:07'; T[1][1002]= +6.9; T[2][1002]=45.1; T[3][1002]=72.3; T[4][1002]=45.4; S[1][1002]=0000; //    7 0002
H[1][1003]='00:03:01'; T[1][1003]= +6.9; T[2][1003]=45.1; T[3][1003]=72.1; T[4][1003]=45.4; S[1][1003]=0000; //   12 0003
H[1][1004]='00:04:05'; T[1][1004]= +6.9; T[2][1004]=45.1; T[3][1004]=72.0; T[4][1004]=45.4; S[1][1004]=0000; //   18 0004
H[1][1005]='00:05:09'; T[1][1005]= +6.9; T[2][1005]=45.1; T[3][1005]=72.0; T[4][1005]=45.4; S[1][1005]=0000; //   24 0005
H[1][1006]='00:06:04'; T[1][1006]= +6.9; T[2][1006]=45.1; T[3][1006]=71.9; T[4][1006]=45.4; S[1][1006]=0000; //   29 0006
H[1][1007]='00:07:08'; T[1][1007]= +6.9; T[2][1007]=45.1; T[3][1007]=71.8; T[4][1007]=45.4; S[1][1007]=0000; //   35 0007
H[1][1008]='00:08:02'; T[1][1008]= +6.9; T[2][1008]=45.1; T[3][1008]=71.8; T[4][1008]=45.4; S[1][1008]=0000; //   40 0008
H[1][1009]='00:09:06'; T[1][1009]= +6.9; T[2][1009]=45.1; T[3][1009]=71.6; T[4][1009]=45.4; S[1][1009]=0000; //   46 0009
// Betriebsart auf Basis des letzten Datensatzes darstellen 
   B[1][1]='01'; // Betriebsart: '00'=Sommerbetrieb; '01'=Winterbetrieb 
// Kalkulierte Brennerdauer aus allen relevanten Status Datensatz berechnen 
   C[1][1]='0'; // Kalkulierte Brennerdauer (in Sekunden) 
// Anzahl Brennerstarts aus allen relevanten Status Datensatz berechnen 
   C[2][1]='0'; // Anzahl Brennerstarts 
// generation: 2016-04-11 00:10:02 ended (0.1 seconds)
// EOF 
```

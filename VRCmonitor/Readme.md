#VRC Monitor

crontab task will call periodicaly a linux script with performs a python script (vrc.py). thispython scripts raeds the log-files on µSDcard and copies relevant data into a new textfile. Afterwards this textfile will be transfered to a ftp-repository on an web server 

## Cron-Daemon (Cronjobs)

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


##Linux script

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


##Python

recommended Python version 2.7.6.1

The both python scripts 
* vrc.py
* vrc2ftp.py

needs to be located in folder /mnt/sda1/arduino/www/vrc

Evaluated data will be stored in /txt/vrc_YYYY-MM-DD.log and into
file vrc2008day.txt for the ftp transfer to the outside web service repository.

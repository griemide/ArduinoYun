#VRC Monitor

crontab task will call periodicaly a linux script with performs a python script (vrc.py). thispython scripts raeds the log-files on µSDcard and copies relevant data into a new textfile. Afterwards this textfile will be transfered to a ftp-repository on an web server 

## Crontab service
... to be added

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

Atributes of \`vrc\`needs to be changed to execute (chmod 755) or via FileZilla (see picture)
![chmod 755](images/vrcChangedAttributes.png)



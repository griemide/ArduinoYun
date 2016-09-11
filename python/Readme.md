#Python scripts


### Starting a script after the CPU Linino boot 
Just add the script to the /etc/rc.local file
Note: the stdout and stderr get redirected to a log file in /tmp (ramdisk)

use touch /tmp/begin and touch /tmp/end 
at the beginning of rc.local resp. at the end

example
touch /tmp/begin
wifi-live-or-reset
boot-complete-notify
sleep 5s
cd /www/sd/IFTTT
./arp2ifttt.py 1> /tmp/IFTTT.log 2>&1 &
touch /tmp/end
exit 0

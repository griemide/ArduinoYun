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


## initial rc.local file
```script
# Put your custom commands here that should be executed once
# the system init finished. By default this file does nothing.

wifi-live-or-reset
boot-complete-notify

# Uncomment the following line in order to reset the microntroller
# right after linux becomes ready

#reset-mcu

# Uncomment the following line in order to disable kernel console
# debug messages, thus having a silent and clean serial communication
# with the microcontroller

#echo 0 > /proc/sys/kernel/printk

exit 0
```

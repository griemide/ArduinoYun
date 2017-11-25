
Title:    periodical NTP synchronsation  
Date:    2017-11-25  
Author:    Michael Gries  
Keywords:  NTP, Arduino Yun, sync  


# ntpclient

[blog reference](http://martybugs.net/wireless/openwrt/timesync.cgi "martybugs.net")

Create init script /etc/init.d/S55ntpclient, with following lines   

``` script
  #!/bin/sh
  # kill any existing ntpclient processes
  # (they can get stuck if no route to target host)
  /usr/bin/killall ntpclient
  # do time sync
  /usr/sbin/ntpclient -l -h 10.60.74.2 -c 1 -s &
```

***
Periodic Time Synchronisation  Create /etc/crontabs/root with the following contents:   

``` script
 # to timesync every 10 minutes
 */10 * * * * /etc/init.d/S55ntpclient
```  

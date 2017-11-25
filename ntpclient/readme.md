Title:␣␣␣␣periodical NTP synchronsation␣␣⏎
Date:␣␣␣␣␣2017-11-25␣␣⏎
Author:␣␣␣Michael Gries␣␣⏎
Keywords:␣_NTP, Arduino Yun, sync__⏎

# ntpclient

[blog reference](http://martybugs.net/wireless/openwrt/timesync.cgi "martybugs.net")

The init script, /etc/init.d/S55ntpclient, is modified to the following:   #!/bin/sh
Inline-`**[Code][]**`

  # kill any existing ntpclient processes
  # (they can get stuck if no route to target host)
  /usr/bin/killall ntpclient

  # do time sync
  /usr/sbin/ntpclient -l -h 10.60.74.2 -c 1 -s &

---
Periodic Time Synchronisation  Create /etc/crontabs/root with the following contents:   # to timesync every 10 minutes
  */10 * * * * /etc/init.d/S55ntpclient
  
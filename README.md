# Arduino Yun
Projects using Arduino Yun platform - Link: [Yun Localhost](http://192.168.0.10)

follwing projects currently implemented [x] / planned [ ]:
- [x] :one: [VRC Monitor](https://github.com/griemide/ArduinoYun/tree/master/VRCmonitor) :file_folder:  
- [x] :two: logging on µSD card :floppy_disk:
- [ ] :three: VRC statistics :chart_with_upwards_trend:

## Installation hints

### Telnet
Telnet session on serial monitor (Arduino bridge):

Within SSH session (like PuTTY) type in:
```C++
telnet Localhost 6571
```
or
type shortcut command **tn** to run script on /usr/bin (needs to be installed once)

```C++
#/usr/bin
#
echo ""
echo "tn, 2014-07-28, Michael Gries"
echo ""
echo "running 'telnet localhost 6571' "
echo ""
#
telnet localhost 6571
```

Script **tn** must be copied once from SD card folder wwww/TelnetLocalhost6571 by executing file **runOnceTransferScript**

```C++
#/www/sd/TelnetLocalhost6571/runOnceTransferScript
#
cp tn /usr/bin
#
echo "file 'tn' copied to /usr/bin"
echo "run 'tn' only if Console is available"
echo ""
echo "2014-07-28, Michael Gries"
echo ""
```

Used SSH-Tools:
* PuTTY...............(Windows system :computer: )
* Serveraudithor...(IOS devices :iphone: )

### SFTP-Server
the Linino package does nott come with SFTP support. But it can be installed via SSH session or via LuCI web interface (System/Software).

Within SSH session (like PuTTY) type in:
```C++
opkg update
opkg install openssh-sftp-server
```

SFTP service can than be used instandly (i.e. without booting the system) by using a SFTP programm (like FileZilla). Installed version of `\openssh-sftp-server`\ can be checked by using above mentioned LuCI web interface (System/Software/Installed Packages).

used SFTP tools:
* FileZilla............(Windows system :computer: )
* 

### Arduino Library restrictions for Arduino Yun vs. VRC application

RX-buffer size mu AltSoftSerial-Library must be increased to 266 Bytes (default = 80 Bytes).
Calculation: VRC 410 datagram = 67 octets. For better visualisation via RS-232 transfer these 67 octes will be presented in Hex-format plus blank. So 67 * 3 characters will be at least 201 charcters which needs to be bufferd within a 10 seconds period.



##### Common


[GitHub griemide](https://github.com/griemide)  - [EMOJ I](http://www.emoji-cheat-sheet.com/) :blush:


:copyright: 2016, Michael Gries 

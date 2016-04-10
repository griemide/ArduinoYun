# Arduino Yun
Projects using Arduino Yun platform - Link: [Yun Localhost](http://192.168.0.10)

follwing projects currently implemented [x] / planned [ ]:
- [x] :one: VRC Monitor :file_folder:
- [x] :two: logging on µSD card :floppy_disk:
- [ ] :three: VRC statistics :chart_with_upwards_trend:

## Installation hints

### Telnet
Telnet session on serial monitor (Arduino bridge):
use ssh-server tool to open ssh session. Type shortcut comand 'tn' to run script on /usr/bin.
Script must be copyied once from SD card folder wwww/TelnetLocalhost6571 by executing file 'runOnceTransferScript'
used SSH-Tools:
* PuTTY           .(Windows system :computer: )
* Serveraudithor  .(IOS devices :iphone: )

### SFTP-Server
the Linino package does nott come with SFTP support. But it can be installed via SSH session or via LuCI web interface (System/Software).

Within SSH session (like PuTTY) type in:
```C++
opkg update
opkg install openssh-sftp-server
```

SFTP service can than be used instandly (i.e. without booting the system) by using a SFTP programm (like FileZilla). Installed version of `\openssh-sftp-server`\ can be checked by using above mentioned LuCI web interface (System/Software/Installed Packages).

[GitHub griemide](https://github.com/griemide)


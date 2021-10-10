# Bandit
## Level 0
* use `bandit0` as password to login.
```
$ ssh bandit0@bandit.labs.overthewire.org -p 2220
```
## Level 0 - 1
* The password for the next level is stored in a file called `readme` located in the home directory.
```
$ cat readme
boJ9jbbUNNfktd78OOpsqOltutMc3MY1
```
## Level 1 - 2
* The password for the next level is stored in a file called `-` located in the home directory.
```
$ cat ./-
CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
```
## Level 2 - 3
* The password for the next level is stored in a file called `spaces in this filename` located in the home directory.
```
$ cat spaces\ in\ this\ filename
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
```
## Level 3 - 4
* The password for the next level is stored in a `hidden` file in the `inhere` directory.
```
$ cat .hidden
pIwrPrtPN36QITSp3EQaw936yaFoFgAB
```
## Level 4 - 5
* The password for the next level is stored in the only `human-readable` file in the inhere directory.
* use `file` command to check file type
```
$ file ./*
./-file00: data
./-file01: data
./-file02: data
./-file03: data
./-file04: data
./-file05: data
./-file06: data
./-file07: ASCII text
./-file08: data
./-file09: data
```
```
$ cat ./-file07
koReBOKuIDDepwhWk7jZC0RTdopnAYKh
```
## Level 5 - 6
* The password for the next level is stored in a file somewhere under the inhere directory and has all of the following properties:
    * human-readable
    * 1033 bytes in size
    * not executable
* use `find` command to find the file.
    * `-type f`: file type is file.
    * `-size 1033c`: file size is 1033 bytes.
    * `-name "[[:print:]]*"`: file name is human-readable.
    * `! -executable`: not executable.
```
$ find . -type f -size 1033c -name "[[:print:]]*" ! -executable
./maybehere07/.file2
```
```
$ cat ./maybehere07/.file2
DXjZPULLxYr17uwoI01bNLQbtFemEgo7
```
## Level 6 - 7
* The password for the next level is stored somewhere on the server and has all of the following properties:
    * owned by user bandit7
    * owned by group bandit6
    * 33 bytes in size
* use `find` command to find the file.
    * `-user bandit7`: owned by user bandit7
    * `-group bandit6`: owned by group bandit6
    * `2>/dev/null` : std error send to /dev/null
```
$ find / -type f -size 33c -user bandit7 -group bandit6 2>/dev/null
/var/lib/dpkg/info/bandit7.password
```
```
$ cat /var/lib/dpkg/info/bandit7.password
HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs
```
## Level 7 - 8
* The password for the next level is stored in the file `data.txt` next to the word `millionth`.
* use `grep` command to find keyword.
    * usage: `grep <keyword> <file>`
```
bandit7@bandit:~$ grep millionth data.txt
millionth       cvX2JJa4CFALtqS87jk27qwqGhBM9plV
```
## Level 8 - 9
* The password for the next level is stored in the file `data.txt` and is the only line of text that occurs only once.
* use `uniq -u` find occurs only once, but we need to use the `sort` command to sort the file first.
```
$ sort data.txt | uniq -u
UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR
```
## Level 9 - 10
* The password for the next level is stored in the file `data.txt` in one of the few human-readable strings, preceded by several ‘=’ characters.
* use `strings` and `grep` command to find the password.
```
$ strings data.txt | grep "="
========== the*2i"4
=:G e
========== password
<I=zsGi
Z)========== is
A=|t&E
Zdb=
c^ LAh=3G
*SF=s
&========== truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk
S=A.H&^
```
## Level 10 - 11
* The password for the next level is stored in the file **data.txt**, which contains base64 encoded data.
* use `base64` command to decode data.
```
bandit10@bandit:~$ base64 -d data.txt
The password is IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
```
## Level 11 - 12
* The password for the next level is stored in the file **data.txt**, where all lowercase (a-z) and uppercase (A-Z) letters have been rotated by 13 positions.
```
bandit11@bandit:~$ cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
The password is 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
```

## Level 12 - 13
* The password for the next level is stored in the file **data.txt**, which is a hexdump of a file that has been repeatedly compressed. For this level it may be useful to create a directory under /tmp in which you can work using mkdir. For example: mkdir /tmp/myname123. Then copy the datafile using cp, and rename it using mv (read the manpages!).
* use `xxd -r` recover hexdump file to original binary file.
* use `gzip -d`, `bzip2 -d` and `tar -xvf` to unzip file
```
bandit12@bandit:~$ cp data.txt /tmp/abcd123
```
```
bandit12@bandit:/tmp/abcd123$ xxd -r data.txt data
bandit12@bandit:/tmp/abcd123$ file data
data: gzip compressed data, was "data2.bin", last modified: Thu May  7 18:14:30 2020, max compression, from Unix
```
```
bandit12@bandit:/tmp/abcd123$ mv data data.gz
bandit12@bandit:/tmp/abcd123$ gzip -d data.gz
bandit12@bandit:/tmp/abcd123$ file data
data: bzip2 compressed data, block size = 900k
```
```
bandit12@bandit:/tmp/abcd123$ mv data data.bz
bandit12@bandit:/tmp/abcd123$ bzip2 -d data.bz
bandit12@bandit:/tmp/abcd123$ file data
data: gzip compressed data, was "data4.bin", last modified: Thu May  7 18:14:30 2020, max compression, from Unix
```
```
bandit12@bandit:/tmp/abcd123$ mv data data.gz
bandit12@bandit:/tmp/abcd123$ gzip -d data.gz
bandit12@bandit:/tmp/abcd123$ file data
data: POSIX tar archive (GNU)
```
```
bandit12@bandit:/tmp/abcd123$ tar -xvf data
data5.bin
bandit12@bandit:/tmp/abcd123$ file data5.bin
data5.bin: POSIX tar archive (GNU)
```
```
bandit12@bandit:/tmp/abcd123$ tar -xvf data5.bin
data6.bin
bandit12@bandit:/tmp/abcd123$ file data6.bin
data6.bin: bzip2 compressed data, block size = 900k
```
```
bandit12@bandit:/tmp/abcd123$ mv data6.bin data6.bz
bandit12@bandit:/tmp/abcd123$ bzip2 -d data6.bz
bandit12@bandit:/tmp/abcd123$ file data6
data6: POSIX tar archive (GNU)
```
```
bandit12@bandit:/tmp/abcd123$ tar -xvf data6
data8.bin
bandit12@bandit:/tmp/abcd123$ file data8.bin
data8.bin: gzip compressed data, was "data9.bin", last modified: Thu May  7 18:14:30 2020, max compression, from Unix
```
```
bandit12@bandit:/tmp/abcd123$ mv data8.bin data8.gz
bandit12@bandit:/tmp/abcd123$ gzip -d data8.gz
bandit12@bandit:/tmp/abcd123$ file data8
data8: ASCII text
bandit12@bandit:/tmp/abcd123$ cat data8
The password is 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
```
## Level 13 - 14
* The password for the next level is stored in **/etc/bandit_pass/bandit14 and can only be read by user bandit14**. For this level, you don’t get the next password, but you get a private SSH key that can be used to log into the next level. **Note: localhost** is a hostname that refers to the machine you are working on.
```
bandit13@bandit:~$ ls
sshkey.private
bandit13@bandit:~$ ssh bandit14@localhost -i sshkey.private
```
## Level 14 - 15
* The password for the next level can be retrieved by submitting the password of the current level to **port 30000 on localhost**.
```
bandit14@bandit:~$ cat /etc/bandit_pass/bandit14 | nc localhost 30000
Correct!
BfMYroe26WYalil77FoDi9qh59eK5xNr
```
## Level 15 - 16
* The password for the next level can be retrieved by submitting the password of the current level to **port 30001 on localhost** using SSL encryption.
* Helpful note: Getting “HEARTBEATING” and “Read R BLOCK”? Use -ign_eof and read the “CONNECTED COMMANDS” section in the manpage. Next to ‘R’ and ‘Q’, the ‘B’ command also works in this version of that command…
* use `openssl s_client -connect <ip>:<port>` to connect the host.
```
bandit15@bandit:~$ openssl s_client -connect localhost:30001
CONNECTED(00000003)
depth=0 CN = localhost
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = localhost
verify return:1

...

---
BfMYroe26WYalil77FoDi9qh59eK5xNr
Correct!
cluFn7wTiGryunymYOu4RcffSxQluehd

closed
```
## Level 16 - 17
* The credentials for the next level can be retrieved by submitting the password of the current level to **a port on localhost in the range 31000 to 32000**. First find out which of these ports have a server listening on them. Then find out which of those speak SSL and which don’t. There is only 1 server that will give the next credentials, the others will simply send back to you whatever you send to it.
```
bandit16@bandit:~$ nmap localhost -p 31000-32000 -T5 -Pn

Starting Nmap 7.40 ( https://nmap.org ) at 2021-10-10 09:47 CEST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00032s latency).
Not shown: 996 closed ports
PORT      STATE SERVICE
31046/tcp open  unknown
31518/tcp open  unknown
31691/tcp open  unknown
31790/tcp open  unknown
31960/tcp open  unknown
```
```
bandit16@bandit:~$ nmap localhost -p 31046,31518,31691,31790,31960 -A -T5 -Pn

Starting Nmap 7.40 ( https://nmap.org ) at 2021-10-10 09:48 CEST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00087s latency).
PORT      STATE SERVICE     VERSION
31046/tcp open  echo
31518/tcp open  ssl/echo
| ssl-cert: Subject: commonName=localhost
| Subject Alternative Name: DNS:localhost
| Not valid before: 2021-09-30T04:46:02
|_Not valid after:  2022-09-30T04:46:02
|_ssl-date: TLS randomness does not represent time
31691/tcp open  echo
31790/tcp open  ssl/unknown
| fingerprint-strings:
|   FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, Kerberos, LDAPSearchReq, LPDString, RTSPRequest, SIPOptions, SSLSessionReq, TLSSessionReq:
|_    Wrong! Please enter the correct current password
| ssl-cert: Subject: commonName=localhost
| Subject Alternative Name: DNS:localhost
| Not valid before: 2021-09-30T04:46:02
|_Not valid after:  2022-09-30T04:46:02
|_ssl-date: TLS randomness does not represent time
31960/tcp open  echo
```
```
bandit16@bandit:~$ openssl s_client -connect localhost:31790
---
cluFn7wTiGryunymYOu4RcffSxQluehd
Correct!
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----

closed
```
```
C:\Users\root>ssh -i ./Desktop/key bandit17@bandit.labs.overthewire.org -p 2220
```
```
bandit17@bandit:~$ cat /etc/bandit_pass/bandit17
xLYVMN9WE5zQ5vHacb0sZEVqbrp7nBTn
```
## Level 17 - 18
* There are 2 files in the homedirectory: **passwords.old and passwords.new**. The password for the next level is in passwords.new and is the only line that has been changed between **passwords.old and passwords.new**.
* NOTE: if you have solved this level and see ‘Byebye!’ when trying to log into bandit18, this is related to the next level, bandit19.
```
bandit17@bandit:~$ diff passwords.new passwords.old
42c42
< kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
---
> w0Yfolrc5bwjS4qw5mq1nnQi6mF03bii
```
## Level 18 - 19
* The password for the next level is stored in a file **readme** in the homedirectory. Unfortunately, someone has modified **.bashrc** to log you out when you log in with SSH.
* use `-t` flag to specify the shell.
```
C:\Users\root>ssh bandit18@bandit.labs.overthewire.org -p 2220 -t /bin/sh
```
```
$ cat readme
IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
```
## Level 19 - 20
* To gain access to the next level, you should use the setuid binary in the homedirectory. Execute it without arguments to find out how to use it. The password for this level can be found in the usual place (/etc/bandit_pass), after you have used the setuid binary.
```
bandit19@bandit:~$ ls -l
total 8
-rwsr-x--- 1 bandit20 bandit19 7296 May  7  2020 bandit20-do
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
GbKksEFF4yrVs6il55v6gwY5aVje5f0j
```
## Reference 
* [Overthewire Bandit Wargames walkthrough Series' Articles](https://dev.to/kkaosninja/series/1395)
* [OverTheWire :- Bandit (Level 0–10) [CTF]](https://dev.to/shubham2503/overthewire-bandit-level-0-10-ctf-4mli)
* [OverTheWire - Bandit Walkthrough](https://home.adelphi.edu/~ni21347/cybersecgames/OverTheWire/Bandit/index.html)
* [OverTheWire: Bandit Level 18 - Level 19](https://therandomier.medium.com/overthewire-bandit-level-18-level-19-2f0db0c63f40)
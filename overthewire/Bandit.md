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
## Reference 
* [Overthewire Bandit Wargames walkthrough Series' Articles](https://dev.to/kkaosninja/series/1395)
* [OverTheWire :- Bandit (Level 0–10) [CTF]](https://dev.to/shubham2503/overthewire-bandit-level-0-10-ctf-4mli)
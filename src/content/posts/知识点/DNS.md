---
title: "DNS"
image: ''
pinned: false
comment: true
published: 2026-07-23
updated: 2026-07-23
description: "dns"
category: 知识点
tags: [知识点]
---

## DNS 是什么？

它的作用是把域名：

```text
www.baidu.com
```

转换成计算机通信所需要的 IP 地址：

```text
110.242.68.66
```



## DNS 查询大概怎么进行？

执行：

```bash
ping www.baidu.com
```

系统需要先查到 `www.baidu.com` 的 IP：

```text
程序
  ↓
检查 /etc/hosts
  ↓
询问 DNS 服务器
  ↓
获得 IP 地址
  ↓
连接该 IP
```



当然了，更完整的 DNS 查询可能涉及：

```text
本机 → DNS 递归服务器 → 根 DNS → .com DNS → baidu.com 权威 DNS
```



## `/etc/resolv.conf`

这是 Linux 中常见的 **DNS 解析配置文件**。

查看：

```bash
cat /etc/resolv.conf
```

看到：

```text
nameserver 127.0.0.53
search localdomain
options edns0
```

### `nameserver`

```text
nameserver 8.8.8.8
```

表示系统查询域名时，向 `8.8.8.8` 这台 DNS 服务器询问。



常见公共 DNS：

```text
8.8.8.8       Google DNS
1.1.1.1       Cloudflare DNS
223.5.5.5     阿里公共 DNS
119.29.29.29  腾讯公共 DNS
```



```text
nameserver 127.0.0.11
```

这是 Docker 提供的内部 DNS。



## `search`

例如：

```text
search example.com
```

当你查询：

```bash
ping server
```

系统可能尝试查询：

```text
server.example.com
```



## `/etc/hosts`

`/etc/hosts` 是本机的静态域名映射文件。

查看：

```bash
cat /etc/hosts
```

常见内容：

```text
127.0.0.1 localhost
::1       localhost
```

格式：

```text
IP地址 域名
```

例如加入：

```text
192.168.1.20 test.local
```

以后执行：

```bash
ping test.local
```

系统会把它解析为：

```text
192.168.1.20
```

这就是涉及一个dns优先解析的说法了，之前大学长给我提一个在白宫官网挂黑页的时候，我一开始就是学习到了这个方法，就是让白宫这个域名指向我们本地弄好的黑页网站。



通常系统会先查询 `/etc/hosts`，再查询 DNS。



## `dig`

功能最完整，适合查看 DNS 详细信息：

```bash
dig baidu.com
```

只看返回的 IP：

```bash
dig +short baidu.com
```

可能输出：

```text
110.242.68.66
39.156.66.10
```

指定 DNS 服务器查询：

```bash
dig @8.8.8.8 baidu.com
```

其中：

```text
@8.8.8.8
```

表示向 `8.8.8.8` 查询。





## `nslookup`

比较容易使用：

```bash
nslookup baidu.com
```

可能显示：

```text
Server:  127.0.0.53
Address: 127.0.0.53

Name:    baidu.com
Address: 110.242.68.66
```

其中：

- `Server`：当前使用的 DNS 服务器
- `Name`：查询的域名
- `Address`：解析出的 IP

指定服务器：

```bash
nslookup baidu.com 8.8.8.8
```



## `host`

输出比较简洁：

```bash
host baidu.com
```

可能显示：

```text
baidu.com has address 110.242.68.66
```

反向查询 IP 对应的域名：

```bash
host 8.8.8.8
```



## 常见 DNS 记录类型

| 类型    | 作用                  |
| ------- | --------------------- |
| `A`     | 域名指向 IPv4 地址    |
| `AAAA`  | 域名指向 IPv6 地址    |
| `CNAME` | 域名指向另一个域名    |
| `MX`    | 邮件服务器            |
| `NS`    | 域名使用的 DNS 服务器 |
| `TXT`   | 文本信息、域名验证等  |
| `PTR`   | IP 反向解析为域名     |

查询指定记录：

```bash
dig baidu.com A
dig baidu.com AAAA
dig baidu.com MX
dig baidu.com NS
dig baidu.com TXT
```

![image-20260723184148397](/images/image-20260723184148397.png)



---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

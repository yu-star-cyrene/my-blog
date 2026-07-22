---
title: "暑假学习之conf"
image: ''
pinned: false
comment: true
published: 2026-07-21
updated: 2026-07-21
description: "conf"
category: 知识点
tags: [知识点]
---



`.conf` 

它主要用来保存程序或系统的设置，例如：

- 端口号
- 日志路径
- 用户权限
- 功能开关
- 网络参数
- 服务启动选项

例如：

```bash
/etc/ssh/sshd_config
/etc/resolv.conf
/etc/systemd/system.conf
```

`.conf` 一般是纯文本文件，可以这样查看：

```bash
cat 文件.conf
```

`.conf` 只是一个常见后缀。存在其他语法的配置文件后缀。

```conf
port=8080
enabled=true
```

或者：

```conf
server {
    listen 80;
}
```



---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

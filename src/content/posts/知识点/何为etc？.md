---
title: "何为etc？"
image: ''
pinned: false
comment: true
published: 2026-07-20
updated: 2026-07-20
description: "linux——etc"
category: 知识点
tags: [知识点]
---



`/etc` 不是一个文件，而是 Linux 系统文件夹。

它主要存放：

- 系统配置文件
- 软件配置文件
- 用户和权限相关配置
- 网络配置
- 服务启动配置

例如：

```
/etc/passwd
```

记录系统用户信息。

```
/etc/hostname
```

记录主机名。

```
/etc/hosts
```

记录本机域名和 IP 映射。

```
/etc/ssh/sshd_config
```

SSH 服务端配置。



查看 `/etc` 目录：

```
ls /etc
```

进入 `/etc`：

```
cd /etc
```

查看某个配置文件内容：

```
cat /etc/hostname
```

注意：普通用户通常可以读取很多 `/etc` 文件，但修改它们一般需要管理员权限：

```
sudo nano /etc/hosts
```



简单说这个文件就是一个系统文件，是你不能删除的文件。

毕竟电脑不会自带很多配置信息，而是写在文件存储的。





---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

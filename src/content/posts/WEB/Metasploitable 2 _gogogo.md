---
title: "Metasploitable 2 _gogogo"
image: '/images/144942196_p0_master1200.jpg'
pinned: false
comment: true
published: 2026-06-16
updated: 2026-06-16
description: "渗透gogogo_day2"
category: WEB
tags: [WEB]
---

# Metasploitable 2

![image-20260616185133476](/images/image-20260616185133476.png)

![image-20260616185306217](/images/image-20260616185306217.png)



## 用ifconfig查询靶机ip

```
ifconfig
ip addr
```

`linux` 的查询 `ip` 命令

得到远程靶机的 `ip` 地址： `192.168.138.131`



## 使用ping确认服务是否连通

![image-20260616185838584](/images/image-20260616185838584.png)

在kali中确认远程服务跟攻击机相通。

```
ping -c 2 192.168.138.131 #只发两个包来确认服务器
```

当然可以一直发包了。

![image-20260616190005848](/images/image-20260616190005848.png)



## 使用nmap直接扫ip

```
nmap -sV -Pn 192.168.138.131
```

```
-sV
作用：识别开放端口对应的服务版本。

-Pn
作用：跳过主机存活探测，直接把目标当成在线来扫。

192.168.138.131
作用：指定要扫描的目标 IP。
```

![image-20260616190205583](/images/image-20260616190205583.png)

直接扫出了很多服务。



## 直连blindshell

最直接的就是那个1524，就写着 `Metasploitable root shell` ，具有远程服务管理员权限的shell。

![image-20260616190341687](/images/image-20260616190341687.png)

直接连接上这个端口，就得到了一个远程的shell。



### 信息搜集：

```
id
作用：查看当前 shell 的用户 ID、组 ID 和权限信息。
uid=0(root) gid=0(root) groups=0(root)
作用：说明当前 shell 已经是 root 权限。

whoami
作用：查看当前 shell 正在以哪个用户名运行。
root
作用：说明当前登录身份就是 root 用户。

uname -a
作用：查看目标系统的内核、系统类型和架构信息。
Linux metasploitable 2.6.24-16-server ... i686 GNU/Linux
作用：说明目标是一台 Linux 靶机，并给出具体内核版本和架构。

pwd
作用：查看当前 shell 所在的工作目录。
/
作用：说明当前所在目录是系统根目录。
```



```
ls
作用：查看当前目录下有哪些文件和目录。
实际含义：你当前在 / 根目录，说明这台 Linux 主机的顶层目录结构都能直接看到，比如 etc、home、var、root 等。
```

![image-20260616190904798](/images/image-20260616190904798.png)



```
ls /home
作用：查看 /home 目录下有哪些用户主目录。
实际含义：这台机器里有 ftp、msfadmin、service、user 这些账户对应的家目录，说明除了系统账户外，还有几个可登录或可利用的普通用户。
```

![image-20260616190930227](/images/image-20260616190930227.png)



```
cat /etc/passwd
作用：查看系统中的用户列表、用户 ID、家目录和默认 shell。
实际含义：你看到了这台机器上有哪些本地用户，比如 root、msfadmin、user、service、postgres、mysql、tomcat55 等，也能判断哪些账户可能值得后续关注。
```

![image-20260616191021063](/images/image-20260616191021063.png)



```
cat /etc/shadow
作用：查看系统用户的密码哈希。
实际含义：因为你当前已经是 root，所以可以直接读到敏感的密码哈希文件；这说明当前权限已经足够高，可以接触到系统最核心的认证信息。
```

![image-20260616191106684](/images/image-20260616191106684.png)



```
find / -name "*.conf" 2>/dev/null | head
作用：在整个系统里查找 .conf 配置文件，并只显示前几条结果。
实际含义：这是在快速找配置文件入口，方便后续查看服务配置、账号信息、路径、端口等内容；2>/dev/null 是把报错丢掉，| head 是只看前面几条，避免输出太多刷屏。
```

![image-20260616191137482](/images/image-20260616191137482.png)



## 直接对ip进行访问

![image-20260616191350586](/images/image-20260616191350586.png)

![image-20260616191601878](/images/image-20260616191601878.png)

由于之前扫描的结果，8180这个端口上明显存在一个apache tomcat服务。

直接尝试访问。

![image-20260616191655758](/images/image-20260616191655758.png)



















---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

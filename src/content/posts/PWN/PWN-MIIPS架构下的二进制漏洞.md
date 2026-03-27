---
title: "PWN-MIPS架构下的二进制漏洞"
image: ''
pinned: false
comment: true
published: 2026-03-26
description: "PWN"
category: PWN
tags: [PWN]
---



![image-20260326154452938](/images/image-20260326154452938.png) 

在做内部赛的babystack下遇见，非x86架构，一下子给我打懵了，我都准备写脚本了。

先简述一下思路：

![image-20260326160030726](/images/image-20260326160030726.png)

根据源码和安全查看，我可以确认是ret2libc的题目，也给了libc文件，第一步就是利用第二次的打印函数打印出libc的地址，然后根据libc文件里面的函数偏移，直接pop_rdi+binsh_system。

可惜做一半时，发现ropper和ROPgadget查不到我们能用的gadget。

后来才发现架构不同，我去了。



> https://blog.csdn.net/qq_38154820/article/details/147891063
>

![image-20260326170911919](/images/image-20260326170911919.png)

**在 MIPS 调用约定中，main 函数通常不会主动取出或恢复存放到寄存器 `$a0-$a3` 中的参数值**





























---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

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

![image-20260304185547856](C:\Users\yu\AppData\Roaming\Typora\typora-user-images\image-20260304185547856.png)

虽然这一题是溢出的题目，但关键的考点还是在rop的使用。

直接通过ida和ubuntu的指令进行分析，可以很明显的发现存在栈溢出的点，但不存在直接system("/bin/sh")给我用，仅仅只有一个notbackdoor的函数直接包含了ls的system指令，所以正常的栈溢出，是无法直接得到flag的，只能看见根目录的各种文件并发现有个名字就叫flag的文件。

















---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。


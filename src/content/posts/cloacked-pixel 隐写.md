---
title: "cloacked-pixel 隐写"
image: ''
pinned: false
comment: true
published: 2025-12-11
description: "CTF 学习笔记与技术复盘"
category: 知识点
tags: [知识点]
---

# #cloacked-pixel

![alt text](/images/QQ20251211-211642.png)

真是服了这个出题人，ISCTF上的misc，只要是它出的，我就直接裂开。

这一题附件是一个加密的压缩包，爆破后得到一张图片，然后图片是lsb隐写加AES加密，即cloacked-pixel 隐写。

这边就算是学到了一个爆破工具的运用，如果遇到lsb隐写内容没法轻易解出，那就用一下，这个。

"C:\Users\G1731\工具\cloackedpixelbreak\cloacked-pixel-decoder.py"

这是出题人github上的一个爆破工具，挺好用的，默认的密码词典就是rock。

以后要再看见这个题目就用这个工具秒了。

---

---

---

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

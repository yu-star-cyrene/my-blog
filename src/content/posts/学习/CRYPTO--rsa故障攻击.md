---
title: "CRYPTO--rsa故障攻击"
image: ''
pinned: false
comment: true
published: 2026-04-24
updated: 2026-04-25
description: "一类利用 CRT-RSA 故障签名直接分解模数的例题整理"
category: 学习
tags: [学习]
---

这篇记一类我觉得辨识度特别高的 RSA 题：题面里一旦同时出现“正常签名”和“故障签名”，而且源码又带 CRT 结构，那基本就该往故障攻击上想了。

# 题目类型

这是典型的 `RSA-CRT 故障攻击` 例题。

题目常见配置一般是：

- 公钥参数
- 一条消息
- 一份正确签名
- 一份故障签名
- 可能再额外给一段密文

这种题最重要的不是爆破，而是识别模型。

# 为什么会出问题

CRT-RSA 会把签名拆成两个模数分支来算，然后再合并。

如果其中一边因为故障注入、硬件错误或者人为扰动出了偏差，就会出现一种非常危险的情况：

- 在模一个素数的意义下，签名还是对的
- 在模另一个素数的意义下，签名已经错了

这会导致一个非常经典的结果：

```text
gcd(错误签名^e - m, n)
```

能直接拉出一个素因子。

# 我会怎么判断这题能不能走这条链

我现在会优先看三件事：

1. 是否给了两份签名，而且其中一份明显是 fault
2. 是否出现了 `dp / dq / p / q` 这类 CRT 相关变量
3. 故障是不是只打在某一个模分支上

如果这三个点都成立，那这题大概率就不是普通 RSA，而是 Bellcore 这一类故障攻击。

# 一个通用的恢复顺序

这类题我一般按这个顺序来：

```text
先确认故障模型
-> 用 gcd 拉一个素因子
-> 还原 p 和 q
-> 求 phi 和 d
-> 再去解密剩余密文
```

顺着这个流程走会很稳。

# 复现框架

下面放一份通用脚本框架：

```python
from math import gcd


N = 0
E = 65537
MESSAGE = 0
FAULT_SIGNATURE = 0
CIPHER = 0


def recover_prime(n: int, e: int, message: int, fault_signature: int) -> int:
    return gcd(pow(fault_signature, e, n) - message, n)


def recover_plaintext(n: int, e: int, p: int, cipher: int) -> int:
    q = n // p
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    return pow(cipher, d, n)


def int_to_bytes(value: int) -> bytes:
    hex_text = hex(value)[2:]
    if len(hex_text) % 2:
        hex_text = "0" + hex_text
    return bytes.fromhex(hex_text)


def main() -> None:
    p = recover_prime(N, E, MESSAGE, FAULT_SIGNATURE)
    plaintext_int = recover_plaintext(N, E, p, CIPHER)
    plaintext = int_to_bytes(plaintext_int)
    print(plaintext)
    print(plaintext.decode())


if __name__ == "__main__":
    main()
```

# 这类题最容易踩的地方

- 没认出“故障签名”才是真正入口
- 先去折腾正常签名，结果绕远路
- 分解出模数后忘了题目还额外给了密文

我现在更习惯先问自己一句：

> 题目既然把 fault 明着给出来，那是不是就在暗示我直接从 gcd 下手？

很多时候这句一问，方向就清了。

# 总结

这类题的精髓不是复杂计算，而是模型识别：

- 看到 CRT
- 看到 fault
- 就想到 gcd 分解模数

只要第一反应对了，后面通常都不长。

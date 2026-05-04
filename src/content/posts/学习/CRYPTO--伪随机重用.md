---
title: "CRYPTO--伪随机重用"
image: ''
pinned: false
comment: true
published: 2026-04-24
updated: 2026-04-25
description: "一类把普通伪随机数直接拿来做掩码的例题整理"
category: 学习
tags: [学习]
---

这篇记一类很适合练思维的密码题：看上去像是“密文加校验码”，但真正的问题根本不在加密算法，而在伪随机数被重复拿来做了太多事情。

# 题目类型

可以把它当成一道典型的 `Python random 可预测` 例题。

这种题常见的结构是：

- 用固定 seed 初始化随机数
- 先用随机流生成一些“业务字段”
- 再继续用同一条随机流生成加密掩码

只要 seed 来源可知，整个随机过程就能被重放。

# 这类题为什么危险

因为很多人会下意识觉得：

> 只要我用随机数把明文异或掉，看起来就挺像加密了。

但如果这个随机数来自普通伪随机数生成器，而且 seed 又能被推回去，那这条随机流其实是完全可预测的。

更糟糕的是，如果同一条随机流还被拿去生成别的东西，比如：

- 验证码
- 校验码
- 订单号后缀
- 调试标识

那这些“前置输出”反而会帮我们更准确地定位随机状态。

# 我会怎么做

这类题我现在会先问自己两个问题：

1. seed 是不是能算出来
2. 随机流在生成掩码之前，已经被消费了多少次

第二个问题特别重要。

因为很多题不是“seed 已知就行”，而是：

- 先出 6 次十进制随机数
- 再出若干字节

如果你恢复时少走了前面的步骤，后面的 mask 就全部错位。

# 一个通用的恢复顺序

我比较习惯按这个顺序来：

```text
先确定 seed
-> 再确认前置随机输出
-> 再重放同样的消费顺序
-> 最后恢复掩码并异或
```

这类题看起来像密码题，其实很像“状态机复盘题”。

# 复现框架

下面放一份通用的恢复框架：

```python
import random


TIMESTAMP = 0
ORDER_ID = 0
CIPHER_HEX = "<cipher_hex>"


def recover_plaintext(ts: int, order_id: int, cipher_hex: str) -> bytes:
    cipher = bytes.fromhex(cipher_hex)
    random.seed(ts ^ order_id)
    _ = "".join(str(random.randint(0, 9)) for _ in range(6))
    mask = bytes(random.randint(0, 255) for _ in range(len(cipher)))
    return bytes(c ^ mask[i] for i, c in enumerate(cipher))


def main() -> None:
    plain = recover_plaintext(TIMESTAMP, ORDER_ID, CIPHER_HEX)
    print(plain)
    print(plain.decode())


if __name__ == "__main__":
    main()
```

# 我会特别注意的点

- `random.seed(...)` 的参数是否完全可知
- `random` 在生成密钥流之前有没有先被别的逻辑消费
- 是否把普通伪随机数直接拿来当一次性掩码使用

这种题经常不是“算法太弱”，而是“工程实现把随机状态暴露得太干净”。

# 总结

这类题的重点不是复杂密码学，而是：

- 伪随机数可预测
- 随机流被复用
- 状态推进顺序可还原

只要把这三件事想明白，很多看起来像“密文恢复”的题，最后其实都只是一次很规整的随机过程重放。

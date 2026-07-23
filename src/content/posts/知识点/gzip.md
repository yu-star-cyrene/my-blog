---
title: "gzip"
image: ''
pinned: false
comment: true
published: 2026-07-23
updated: 2026-07-23
description: "gzip"
category: 知识点
tags: [知识点]
---



`gzip` 全称通常解释为 **GNU zip**。

它的核心作用只有一个：

> 把一个文件压小。

例如：

```bash
gzip a.txt
```

执行后通常变成：

```text
a.txt.gz
```

原来的 `a.txt` 默认会消失，只留下压缩后的文件。

解压：

```bash
gunzip a.txt.gz
```

或者：

```bash
gzip -d a.txt.gz
```





## `tar`：负责打包

`tar` 把多个文件、目录合并成一个文件：

```bash
tar -cf archive.tar dir/
```

结果：

```text
多个文件 → archive.tar
```

但这个 `.tar` 文件不一定变小，它主要只是“装在一起”。



## `gzip`：负责压缩

再对 `.tar` 文件压缩：

```bash
gzip archive.tar
```

结果：

```text
archive.tar.gz
```

所以：

```text
.tar.gz = 先 tar 打包，再 gzip 压缩
```

命令：

```bash
tar -czf archive.tar.gz dir/
```

其中：

- `c`：创建 tar 包
- `z`：使用 gzip 压缩
- `f`：指定文件名

解压时：

```bash
tar -xzf archive.tar.gz
```

- `x`：从 tar 包中提取
- `z`：先用 gzip 解压
- `f`：指定压缩包



## gzip 和 zip 的区别

| 对比                 | gzip             | zip    |
| -------------------- | ---------------- | ------ |
| 能否直接包含多个文件 | 通常不能         | 可以   |
| 能否保存目录结构     | 单独使用不能     | 可以   |
| 是否需要搭配 tar     | 多文件时通常需要 | 不需要 |
| 常见后缀             | `.gz`、`.tar.gz` | `.zip` |
| Linux 中常见程度     | 很常见           | 也常见 |
| Windows 兼容性       | 一般             | 很好   |



形象理解：

```text
a.txt
b.txt
c.txt
```

`tar` 相当于先把它们装进一个箱子：

```text
[a.txt + b.txt + c.txt] → archive.tar
```

`gzip` 相当于把这个箱子压扁：

```text
archive.tar → archive.tar.gz
```

而 `zip` 相当于直接把多个文件分别压缩后装进一个压缩包：

```text
a.txt + b.txt + c.txt → archive.zip
```



---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

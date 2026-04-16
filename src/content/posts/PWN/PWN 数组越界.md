---
title: "PWN 数组越界"
image: ''
pinned: false
comment: true
published: 2026-03-24
updated: 2026-04-16
description: "PWN"
category: PWN
tags: [PWN]
---

**new 的知识点**

这是一个关于pwn的数组越权的漏洞文章。

因为遇到了，而且相较于之前的pwn题，我的思路并不够清晰，因此可以算是在结果论上的学习。

首先对于知识的一个阐明。

> https://www.cnblogs.com/GGbomb/p/17830055.html

![image-20260324194052918](/images/image-20260324194052918.png)

这是某一题的实际运行，在现在的我看来，其实很像canary绕过的题目，利用后续的读取数据和答应数据找到canary的地址，获取canary，从而绕过canary。

```
int sub_8048BD0()
{
  int v0; // eax
  FILE *stream; // [esp+Ch] [ebp-53Ch]
  int v3; // [esp+10h] [ebp-538h]
  _BYTE v4[1328]; // [esp+18h] [ebp-530h] BYREF

  v3 = 0;
  memset(v4, 0, 0x528u);
  stream = fopen("/dev/null", "a");
  if ( !stream )
    sub_804868B();
  sub_8048856();
  sleep(2u);
  while ( !v3 )
  {
    sub_804888F();
    v0 = sub_80486AB();
    if ( v0 == 2 )
    {
      sub_8048A08(v4);
    }
    else if ( v0 > 2 )
    {
      if ( v0 == 3 )
      {
        sub_8048ADA(v4, stream);
      }
      else if ( v0 == 4 )
      {
        v3 = 1;
      }
    }
    else if ( v0 == 1 )
    {
      sub_8048941(v4);
    }
  }
  puts("Thank you for using our service :)");
  fclose(stream);
  return 0;
}
```

这边给出一开始的源码，这个不算难懂，就是定义一个v0用来接收我们的输入，从而调用对应菜单的功能。

这边最主要的就是输入1对应菜单的写入数据功能。

```
int __cdecl sub_8048941(int a1)
{
  int i; // [esp+Ch] [ebp-Ch]

  for ( i = 0; i <= 4 && *(_DWORD *)(264 * i + a1); ++i )
    ;
  if ( i == 5 )
    return puts("Too many letters :P");
  printf("\nInput your contents: ");
  *(_DWORD *)(264 * i + a1 + 4) = sub_80486D9(264 * i + a1 + 8, 256);
  *(_DWORD *)(264 * i + a1) = 1;
  return puts("\nDone!");
}
```

感觉这么久以来，二进制程序的漏洞大部分都是在于读取我们输入数据的地方，特别喜欢`get`和`puts`。

这个菜单的功能其实就一个我们可以写入一个信件给程序。

` for ( i = 0; i <= 4 && *(_DWORD *)(264 * i + a1); ++i )`

看这一段，一个循坏，实际上就是去寻找，我们是否有输入过文件，从0开始，一直到4，一共可以写5个信件，当i的值超过4到5时，就会报错，显示`Too many letters`。

其实最后攻击还会用到其他的功能。但这边先具体讲解这边的写信件的功能。

正常写入时，程序调用一个自定义读入函数，去看一下。

```
unsigned int __cdecl sub_80486D9(int a1, int a2)
{
  unsigned int v2; // eax
  char ptr; // [esp+Bh] [ebp-Dh] BYREF
  unsigned int v5; // [esp+Ch] [ebp-Ch]

  v5 = 0;
  while ( a2 - 1 > v5 )
  {
    if ( fread(&ptr, 1u, 1u, stdin) != 1 )
      sub_804868B();
    if ( ptr == 10 )
      break;
    v2 = v5++;
    *(_BYTE *)(v2 + a1) = ptr;
  }
  *(_BYTE *)(a1 + v5) = 0;
  return v5;
}
```

在这，因为程序之前的(264 * i + a1)这个实际上相当于，一个信件序号的4字节，一个信件名称的4字节，一个信件内容的256字节，然后这边v5<a2-1，那说明v5最大达到255，说明下面的从键盘读取数据的fread函数最多运行255次，即最多读入255字节的数据，而这边还有一个对于换行的检测，当ptr==10时，也就是ascill码的换行时，程序就会接受到换行视作我们已经写完了数据，写完后，程序就会在我们写入的数据末尾自动加上\0，然后完成数据的读入。

所以实际上最终我们的letters是255个我们输入的字节加上/0组成。

我去，直接研究成形题目给我干傻了，回归一下底层。



> https://hello-ctf.com/hc-pwn/Stack_Overflow/#_4

探姬师傅，救救我。















---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

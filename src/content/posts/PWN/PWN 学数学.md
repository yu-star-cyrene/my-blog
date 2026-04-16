---
title: "PWN 学数学"
image: ''
pinned: false
comment: true
published: 2026-03-22
updated: 2026-04-16
description: "PWN"
category: PWN
tags: [PWN]
---

说来忏愧，直接整数溢出我是会的，直接canary，pie绕过我回的，直接ret2libc之类的我也会。

然后我就遇到一个题目三个整数溢出，我没招了。

所以就留一个文章用来搜集一下这些奇怪的整数溢出问题。



## 一.减法溢出

#### 源码：

```
_BOOL8 sub_9C0()
{
  int v1; // [rsp+8h] [rbp-38h]
  int v2; // [rsp+Ch] [rbp-34h]
  char s[8]; // [rsp+10h] [rbp-30h] BYREF
  __int64 v4; // [rsp+18h] [rbp-28h]
  __int64 v5; // [rsp+20h] [rbp-20h]
  int v6; // [rsp+28h] [rbp-18h]
  __int16 v7; // [rsp+2Ch] [rbp-14h]
  unsigned __int64 v8; // [rsp+38h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  puts("1.a-b=9,0<=a<9,0<=b<9");
  *(_QWORD *)s = 0;
  v4 = 0;
  v5 = 0;
  v6 = 0;
  v7 = 0;
  printf("a:");
  __isoc99_scanf("%20s", s);
  if ( strchr(s, 45) )
    return 0;
  v1 = atoi(s);
  printf("b:");
  __isoc99_scanf("%20s", s);
  if ( strchr(s, 45) )
    return 0;
  v2 = atoi(s);
  return v1 <= 8 && v2 <= 8 && v1 - v2 == 9;
}
```

#### 解释：

首先a和b为整数且都小于9却大于等于0，要是a-b=9，这是在正常思路上不可能的事，最大仅为8.

这边还有个45，是用来阻止我们输入-的情况。

关键在于a = atoi(s);	这段代码，它将我们输入的数据直接转化为int的类型，又因为程序本身是没有在代码中加入检查a，b是否大于等于0的情况，如果我们输入一个很大的数，atoi在转化时，就既有可能发生截断，造成我们输入了一个很大的数然后到后续就变成了-3之类的数。

这边举个数值，2^31-1，这是整型能存放的最大正数数字**(不包括符号位)**，别问为什么，就是这样，然后机器看的其实是补码，如果我们输入2^31-9，那在化作原码后再化作补码后就变成了-9的值，机器就把其当作-9来用。

这就是我们输入0和2^31-9能完成题目要求的原因。



## 二.乘法溢出

#### 源码：

```
_BOOL8 sub_AEE()
{
  int v1; // [rsp+0h] [rbp-10h] BYREF
  int v2; // [rsp+4h] [rbp-Ch] BYREF
  unsigned __int64 v3; // [rsp+8h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  puts("2.a*b=9,a>9,b>9");
  printf("a:");
  __isoc99_scanf("%d", &v1);
  printf("b:");
  __isoc99_scanf("%d", &v2);
  return v1 > 9 && v2 > 9 && v1 * v2 == 9;
}
```

#### 解释：

a，b都大于9，却要求两者相乘为9，这同样不是正常做法，怎么算两者相乘的结果都大于81，还是要用到整数溢出的情况。

根据第一个数学问题的解释中，我们可以得到，要是v1 * v2= 9，利用整数溢出，实际上得到的是v1 * v2 ≡ 9  (mod 2^32)，他们相乘的结果除以2^31要等于9。

**2^32=4294967296->v1*v2=x/4294967296=9**

**0x100000000+9 = 4294967305 = 5 * 9629 * 89209**

a=5*9629	b=89209



## 三.除法溢出

#### 源码：

```
__int64 sub_BA3()
{
  int v1; // [rsp+Ch] [rbp-14h] BYREF
  _DWORD v2[2]; // [rsp+10h] [rbp-10h] BYREF
  unsigned __int64 v3; // [rsp+18h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  puts("3.a/b=ERROR,b!=0");
  printf("a:");
  __isoc99_scanf("%d", &v1);
  printf("b:");
  __isoc99_scanf("%d", v2);
  if ( v2[0] )
  {
    signal(8, (__sighandler_t)handler);
    v2[1] = v1 / v2[0];
    signal(8, 0);
  }
  return 0;
}
```

#### 解释：

b!=0，有要求触发报错，明显就不是用除以0的思路，这边采用的是除法溢出，如果结果一个超过类型范围的数，就会产生sigfpe也就是溢出了，就会满足题意。

因此只要结果超过int范围-2147483648 ~ 2147483647的数就行了。

这边可以用-2147483648/-1就完成了。













---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

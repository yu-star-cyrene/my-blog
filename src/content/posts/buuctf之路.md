---
title: "buuctf之路"
image: '/images/138339300_p0_master1200.jpg'
pinned: false
comment: true
published: 2025-11-11
description: "刷题"
category: 刷题
tags: [刷题]
---

个人的刷题之旅，尽量的写的清晰明了一些，也是一种对知识回顾和学习的方法。



---



# #1.假如给我三天光明

![alt text](/images/QQ20251111-153946.png)
题目所给的附件内有两个文件，一张图片，一个压缩包文件，打开图片
![alt text](/images/QQ20251111-153946.png)
很明显图片中存在盲文，上网随便搜一个盲文表，解密一下，得到kmdonowg。
压缩包直接打开提示错误，说明有问题，拉到010editor一看
![alt text](/images/QQ20251111-161425.png)
原来压缩包是rar格式的，改个后缀就可以了。
打开压缩包输入一下我们刚才解密的密码，压缩成功，是一个wav的音频文件，而且一听就知道是莫斯密码，用audacity打开
![alt text](/images/QQ20251111-161732-1.png)
手敲一波，-.-.  -  ..-.  .--  .--.  .  ..  -----  ---..  --...  ...--  ..---  ..--..  ..---  ...--  -..  --..
然后解码，得到CTFWPEI08732?23DZ
最后根据题目的用flag包裹，再加上试了一次大写字母不行，得到flag
flag{wpei08732?23dz}

---

# #2.[SWPU2019]神奇的二维码

附件给了一个二维码，用qr扫一下
![alt text](/images/QQ20251111-192300.png)
swpuctf{flag_is_not_here} 虽然它都说不在这里了，但我还是试了一试，wrong！
所以直接扫是不对的，扔到随波逐流里面看看
![alt text](/images/QQ20251111-193617.png)
隐藏文件，一般要binwalk，但我懒得开wsl了，提取一下
![alt text](/images/QQ20251111-193843.png)
四个包，都看看
![alt text](/images/QQ20251111-193942.png)
![alt text](/images/QQ20251111-193950.png)
要密码
![alt text](/images/QQ20251111-194100.png)
一眼base64 解码得到asdfghjkl1234567890 扔到上面那个加密的看看
![alt text](/images/QQ20251111-194251.png) 
又假，看看第三个包，
"C:\Users\G1731\Downloads\神奇的二维码\_BitcoinPay.png.extracted\flag.doc" 是一个doc文件，里面是一串长的要死的字符串，先不管，看看第四个包
![alt text](/images/QQ20251111-194405.png)
一个音频 ，需要密码，那估计就是第三个包的字符串了，
虽然不想说，但看着很像base64，估计是多次加密的，所以那么长，一顿解密后得到comEON_YOuAreSOSoS0great
还被调侃了，解压一下那个音频 ，一听，又是莫斯，手敲得到-- --- .-. ... . .. ... ...- . .-. -.-- ...- . .-. -.-- . .- ... -.--
解密一下，MORSEISVERYVERYEASY
试了几次，得到flag{morseisveryveryeasy}
也不知道为什么大写不行。



---



# #3.Java逆向解密

题目给了一个class文件，是java编译后的，我们用jadx反编译一下
即打开jadx，然后打开一下题目给的class文件。

``` 
package defpackage;

import java.util.ArrayList;
import java.util.Scanner;

/* loaded from: Reverse.class */
public class Reverse {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        System.out.println("Please input the flag ：");
        String str = s.next();
        System.out.println("Your input is ：");
        System.out.println(str);
        char[] stringArr = str.toCharArray();
        Encrypt(stringArr);
    }
    public static void Encrypt(char[] arr) {
        ArrayList<Integer> Resultlist = new ArrayList<>();
        for (char c : arr) {
            int result = (c + '@') ^ 32;
            Resultlist.add(Integer.valueOf(result));
        }
        int[] KEY = {180, 136, 137, 147, 191, 137, 147, 191, 148, 136, 133, 191, 134, 140, 129, 135, 191, 65};
        ArrayList<Integer> KEYList = new ArrayList<>();
        for (int i : KEY) {
            KEYList.add(Integer.valueOf(i));
        }
        System.out.println("Result:");
        if (Resultlist.equals(KEYList)) {
            System.out.println("Congratulations！");
        } else {
            System.err.println("Error！");
        }
    }
}
```
得到代码这样
分析一下
result = (c + '@') ^ 32
@的ascll码为64，输入的先加64 然后跟32异或  
即 c = (result ^ 32) - 64
将180, 136, 137, 147, 191, 137, 147, 191, 148, 136, 133, 191, 134, 140, 129, 135, 191, 65这些均操作一番，得到This_is_the_flag_!
所以flag为flag{This_is_the_flag_!}
``` 

---

3.[GXYCTF2019]luck_guy
题目给了一个附件，"C:\Users\G1731\Downloads\attachment\luck_guy"
先用pe看一下
![alt text](/images/QQ20251111-205049.png)
很正常，没壳，打开ida，扔进去
![alt text](/images/QQ20251111-205216.png)


```int __fastcall main(int argc, const char **argv, const char **envp)
{
  int v4; // [rsp+14h] [rbp-Ch] BYREF
  unsigned __int64 v5; // [rsp+18h] [rbp-8h]

  v5 = __readfsqword(0x28u);
  welcome();
  puts("_________________");
  puts("try to patch me and find flag");
  v4 = 0;
  puts("please input a lucky number");
  __isoc99_scanf("%d", &v4);
  patch_me(v4);
  puts("OK,see you again");
  return 0;
}
```
有个比较，patch_me，点点看
```
int __fastcall patch_me(int a1)
{
  if ( a1 % 2 == 1 )
    return puts("just finished");
  else
    return get_flag();
}```

又有一个get_flag，再点点看

```unsigned __int64 get_flag()
{
  unsigned int v0; // eax
  int i; // [rsp+4h] [rbp-3Ch]
  int j; // [rsp+8h] [rbp-38h]
  __int64 s; // [rsp+10h] [rbp-30h] BYREF
  char v5; // [rsp+18h] [rbp-28h]
  unsigned __int64 v6; // [rsp+38h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  v0 = time(0);
  srand(v0);
  for ( i = 0; i <= 4; ++i )
  {
    switch ( rand() % 200 )
    {
      case 1:
        puts("OK, it's flag:");
        memset(&s, 0, 0x28u);
        strcat((char *)&s, f1);
        strcat((char *)&s, &f2);
        printf("%s", (const char *)&s);
        break;
      case 2:
        printf("Solar not like you");
        break;
      case 3:
        printf("Solar want a girlfriend");
        break;
      case 4:
        s = 0x7F666F6067756369LL;
        v5 = 0;
        strcat(&f2, (const char *)&s);
        break;
      case 5:
        for ( j = 0; j <= 7; ++j )
        {
          if ( j % 2 == 1 )
            *(&f2 + j) -= 2;
          else
            --*(&f2 + j);
        }
        break;
      default:
        puts("emmm,you can't find flag 23333");
        break;
    }
  }
  return __readfsqword(0x28u) ^ v6;
}```
              

三个代码只要看一个就好了，最后一个。
rand() % 200 == 1，看到这个了吧，随机case，只有先4，后5，再1，才有flag，真是考验运气。
所以我选择直接静态分析，case4的初值为0x7F666F6067756369LL，反编译这个要反着看，然后转化成字符，得到icugof\x7F
```在通过case 5:
        for ( j = 0; j <= 7; ++j )
        {
          if ( j % 2 == 1 )
            *(&f2 + j) -= 2;
          else
            --*(&f2 + j);
        }
```

奇数-2,偶数-1，对刚才的字符进行操作，得到hate_me}，少一半，如果题目狠点心就只能动态分析了，但是它还是太善良了，我翻了翻ida，成功在
![alt text](/images/QQ20251111-205246.png)
这里，太直接了，根据buuctf的要求，最后得到flag，为flag{do_not_hate_me}

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

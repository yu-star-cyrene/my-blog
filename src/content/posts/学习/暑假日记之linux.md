---
title: "暑假日记之linux"
image: ''
pinned: false
comment: true
published: 2026-07-20
updated: 2026-07-23
description: "linux学习"
category: 学习
tags: [学习]
---

![image-20260720153718675](/images/image-20260720153718675.png)

稍微画一些时间学习一下，这边预计3天学习完吧。



## 1.输出echo

![image-20260720153802898](/images/image-20260720153802898.png)

```
pwd:显示当前目录
whoami:显示当前登入用户
echo:输出内容
>:定向符号
```

![image-20260720154214650](/images/image-20260720154214650.png)

讲讲一下问题：
就是我一开始想要试着执行这个文本文件所有使用我会的chmod指令，但是后来一下这不是可执行的文件啊。应该用cat或者vim查看。



## 2.$(指令)

![image-20260720154355114](/images/image-20260720154355114.png)

```
$(命令) 是命令替换，会先执行括号内的命令，再将结果替换到外层命令中
```

![image-20260720154644774](/images/image-20260720154644774.png)

讲一讲问题：
其实这个部分很简单，因为echo我本来就会，就是这个$后面的指令先执行我确实不懂。还有一个点就是echo+文件怎么就光输出文件名了。另外，其实~这个代指根目录，没有讲其实，不过正常也直到。echo只是用来输出文本内容。。。。。。。



## 3.help

![image-20260720155047096](/images/image-20260720155047096.png)

```
--help — 查看简要帮助
```

![image-20260720155144424](/images/image-20260720155144424.png)

讲一讲问题：
这关没什么好说的，其实最主要的就是学会打开手册，然后就是直接>，使用这个定向符号可以直接保存内容。



## 4.ls和cd

![image-20260720155312463](/images/image-20260720155312463.png)

```
ls — 列出当前目录
ls -l — 长格式（权限、大小、时间）
ls -a — 显示隐藏文件（以 . 开头）
ls -la — 长格式 + 隐藏文件
ls -lh — 人类可读的文件大小

cd /path — 切换到指定目录
cd .. — 返回上级目录
cd ~ 或 cd — 回到家目录
```

![image-20260720155419433](/images/image-20260720155419433.png)

讲一讲问题：

其实这个我感觉比较关键的是etc这个文件。

在这里，我就不列举etc是什么了。[etc](/posts/知识点/何为etc/)



## 5.mkdir和touch

![image-20260720162138998](/images/image-20260720162138998.png)

```
mkdir 创建目录
mkdir dir — 创建单个目录
mkdir -p a/b/c — 递归创建多级目录
touch — 创建空文件
touch file.txt — 创建空文件
&& — 连续执行 eg:cmd1 && cmd2 — cmd1 成功后才执行 cmd2
```

![image-20260720162717086](/images/image-20260720162717086.png)

讲一讲问题：

这边有一个小点 我就是利用mkdir创建了两个目录，导致不满足写入文件的条件，就导致一直报错说这个是一个目录，之后rm的用法也不对，我以前的印象里面rm就是用来删除文件的，但是这边rm删除不了目录，或者说rm+文件名这个用法不适合删除目录，其实目录就是一个文件夹拉，所以实际删除文件夹的命令是用rmdir，dir：direction。

然后就是这边我没有使用到touch这个创建空文件的命令，以及&&这个连续执行我没有使用到，下一次我会注意点，至少当前关卡给出的命令都要使用到。



## 6.cp和mv

![image-20260720163149213](/images/image-20260720163149213.png)

```
cp src dst — 复制文件
cp -r dir1 dir2 — 递归复制目录

mv old new — 重命名文件
mv file dir/ — 移动文件到目录
```

![image-20260720163456012](/images/image-20260720163456012.png)

讲一讲问题：

其实看到这个mv我就想起之前isctf上的一题web利用mv移动相同名字的文件会产生碰撞的情况，产生webshell。

嘶，我记得我写过文章，怎么不见了。

![image-20260720163930722](/images/image-20260720163930722.png)

![image-20260720164001472](/images/image-20260720164001472.png)

![image-20260720164107722](/images/image-20260720164107722.png)

稍微贴下别人的博客。

> https://g3rling.top/598

讲回命令学习，一开始犯下的错误就是敲键盘敲得太快，想当然的敲指令，造成的错误。

对了对了，cp这个指令容易复制不了太大的文件，因为我以前试过。



## 7.rm

![image-20260720164522549](/images/image-20260720164522549.png)

```
rm file — 删除文件
rm -r dir — 递归删除目录及其内容
rm -f file — 强制删除，不提示
rmdir dir — 删除空目录
```

![image-20260720173907517](/images/image-20260720173907517.png)

讲一讲问题：
首先其实在创建没有内容的文件时，直接用touch就行了。其次，其实一开始比较不理解的是touch能不能递归创建？一般我用的是nano，和vim，这边看了一下，其实是我的指令有用问题，要`mkdir olddir && touch olddir/a.txt`这样。

还有就是在删除的时候，我老是喜欢/文件名，但这个不是指当前文件的根目录下的文件，而是系统根目录，根据pwd来看其实，如果非要这样，就得 `/home/student/olddir `，不然就到系统根目录去了。

如果非要用/文件名，那就要~/文件名。



## 8.cat，less，more

![image-20260720174600630](/images/image-20260720174600630.png)

```
cat file — 一次性输出全部内容
less file — 分页查看（q 退出，空格翻页）
more file — 类似 less 的简化版
```

![image-20260720174815859](/images/image-20260720174815859.png)

讲一讲问题：
没什么，我唯一新奇就是less这个按页读取有点意思。more其实实际操作起来感觉就是cat。



## 9.head和tail

![image-20260720174944735](/images/image-20260720174944735.png)

```
head -n 3 file — 显示前 3 行
tail -n 3 file — 显示最后 3 行
tail -f file — 实时跟踪文件末尾（日志常用）
```

![image-20260720175217634](/images/image-20260720175217634.png)

讲一讲问题：
其实感觉起来，这个tail指令有点意思，ctf简单的比赛里面还能遇到，比如cat吃ban的时候。总体而言，tail和head这两个指令就是用于查看大内容的细致部分。



## 9.nano

![image-20260720175347317](/images/image-20260720175347317.png)

```
nano file — 打开或创建文件
Ctrl+O — 保存文件
Ctrl+X — 退出编辑器
Ctrl+K — 剪切当前行
Ctrl+U — 粘贴
```

![image-20260720175455860](/images/image-20260720175455860.png)

没什么问题，nano我很经常用。



## 10.vim

![image-20260720175727315](/images/image-20260720175727315.png)

```
vim 基础
vim 是 Linux 最强大的文本编辑器之一。

三种模式
普通模式 — 默认模式，用于导航和命令
插入模式 — 按 i 进入，用于输入文字
命令模式 — 按 : 进入，用于保存退出等
常用操作
i — 进入插入模式
Esc — 回到普通模式
:w — 保存
:q — 退出
:wq — 保存并退出
:q! — 不保存强制退出
dd — 删除当前行
yy — 复制当前行
p — 粘贴
```

有点意思的是，这个靶场的容器无法自带vim得自己下载，其实有点不符合教学用意，或者说应该在旁边的教学给出下载的指令，这个靶场是面向新手的的，所以应该认真一点，不是吗，不过首领大人没改，应该是觉得没有必要了。

这个靶场是河南的一个师傅做的。

sudo更新一下软件园，然install就行了。

![image-20260720180428871](/images/image-20260720180428871.png)

讲一讲问题：

有点卡，导致一开始vim必须强制不保存退出来，在创建功能下nano比vim好用，但是在编辑功能下，vim就更加有优势了。



## 11.grep

![image-20260721145606928](/images/image-20260721145606928.png)

```
grep pattern file — 搜索匹配行
grep -i — 忽略大小写
grep -n — 显示行号
grep -r — 递归搜索目录
grep -v — 反向匹配（不包含的行）
grep -c — 只显示匹配行数
```

![image-20260721145727544](/images/image-20260721145727544.png)

讲一讲问题：
其实说实话，很像string，我之前在windows下安装过这个程序便能跟linux系统一样直接搜索，其实这个就是一个搜索的指令。



## 12.find

![image-20260721145848444](/images/image-20260721145848444.png)

```
find /path -name 'pattern' — 按文件名查找
find /path -type f — 只查找文件
find /path -type d — 只查找目录
find /path -size +1M — 查找大于 1MB 的文件
find /path -mtime -7 — 最近 7 天修改过的文件
```

目录查询，也是文件夹内查询。

![image-20260721150137598](/images/image-20260721150137598.png)

讲一讲问题：
首先find，string，grep这个三个都是搜索的指令，第一个find是目录种搜索文件，string就是选择字符串，其实感觉grep跟string是一样的功能。

之后就是一个问题，就是一个是 `find /etc -name '*.conf'` ，这边多了一个星号。

星号在这边是匹配字符的意思，或者说它是一个占位符，表示 `xxx.conf`。

星号 `*` 是**通配符**，表示：

> 匹配任意数量的任意字符，包括 0 个字符。

之后有一个需要了解的是conf是什么文件？

[conf](/posts/知识点/暑假学习之conf/)



## 13. 管道符|

![image-20260721151030890](/images/image-20260721151030890.png)

```
管道 |
管道将前一个命令的输出作为后一个命令的输入。

ls | wc -l — 统计文件数量
cat file | grep pattern — 搜索文件内容
ps aux | grep nginx — 查找进程
history | tail -20 — 查看最近 20 条历史命令
```

![image-20260721151312642](/images/image-20260721151312642.png)

讲一讲问题：
其实没什么，就是一个连续使用命令的方法而已，关键应该是记一下这个 `wc -l` 这个指令我还真不知道，统计数量。

![image-20260721151441030](/images/image-20260721151441030.png)

这还有个看进程的说法，其实一般不都是直接ps的吗？

[进程的简单了解](/posts/知识点/linux之进程/)



## 14.重定向和追加

![image-20260721152236291](/images/image-20260721152236291.png)

```
重定向
> — 覆盖写入文件（文件已有内容会被清空）
>> — 追加到文件末尾

输入重定向
< — 从文件读取输入

错误重定向
2> — 将错误输出重定向到文件
2>&1 — 将错误输出合并到标准输出
```

![image-20260721152357742](/images/image-20260721152357742.png)

讲一讲问题：

个人感觉比较重要的就是这个错误重定向。

[错误重定向了解](/posts/知识点/错误重定向/)



## 15.sort和uniq和wc

![image-20260721162910538](/images/image-20260721162910538.png)

```
sort file — 按字母排序
sort -n — 按数字排序
sort -r — 逆序

uniq — 去除相邻重复行（需先排序）
uniq -c — 显示重复次数

wc -l — 统计行数
wc -w — 统计单词数
wc -c — 统计字节数
```

![image-20260721164452637](/images/image-20260721164452637.png)

讲一讲问题：
我去，被阴到了，这个\n就是换行，我还以为就是直接这么输入的。



## 16.chmod

![image-20260721164549604](/images/image-20260721164549604.png)

```
chmod 用于修改文件权限。

4 — 读 (r)
2 — 写 (w)
1 — 执行 (x)

三位数字分别代表：属主、属组、其他人
644 — 属主读写，其他人只读
755 — 属主全部，其他人读+执行
600 — 仅属主读写
700 — 仅属主全部权限
```

![image-20260721164835258](/images/image-20260721164835258.png)



## 17.chown

![image-20260721164851472](/images/image-20260721164851472.png)

```
chown 用于修改文件的属主和属组。

chown user file — 修改属主
chown user:group file — 同时修改属主和属组
chown -R user dir — 递归修改目录
```

![image-20260721165348486](/images/image-20260721165348486.png)

讲一讲问题：
首先就是创建这个用户，题目没有给代码，我是自己查询得到的代码，创建了一个普通用户，之后就是正常创建文件，写入内容。然后就是在修改用户属性的时候，权限不够，需要sudo提权一下。

```
sudo useradd -m xxx
```



## 18.useradd和groupadd

![image-20260721165651341](/images/image-20260721165651341.png)

```
用户管理
useradd user — 创建用户
userdel user — 删除用户
passwd user — 设置密码
id user — 查看用户信息

组管理
groupadd group — 创建组
usermod -aG group user — 将用户加入组
groups user — 查看用户所属组
```

![image-20260721170203643](/images/image-20260721170203643.png)

讲一讲问题：

有点卡管理员权限了，所有操作都要提权sudo。



## 19.sudo和su

![image-20260721170350651](/images/image-20260721170350651.png)

```
sudo 与 su
sudo — 以其他用户身份执行命令
sudo command — 以 root 身份执行
sudo -u user command — 以指定用户身份执行
需要当前用户在 sudo 组中
su — 切换用户
su user — 切换到指定用户
su - user — 切换并加载用户环境
su - user -c 'cmd' — 以指定用户执行命令
区别
sudo 执行单条命令，不切换 shell
su 切换整个用户会话
```

![image-20260721203010701](/images/image-20260721203010701.png)

讲一讲问题：
首先就是创建用户后，忘记设置密码，导致无法使用账号，然后就是我犯了个打错就是直接切换用户进行操作了，什么权限都没有。



## 20.ps和top

![image-20260721203123499](/images/image-20260721203123499.png)

```
ps — 进程快照
ps — 当前终端的进程
ps aux — 所有进程详细信息
ps -ef — 另一种格式显示所有进程

top — 实时监控
top — 实时显示进程（按 q 退出）

ps aux 输出列
USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
```

![image-20260721204223900](/images/image-20260721204223900.png)

讲一下问题：
嘶这个默认student用户不是root很烦，虽然权限很高但是根本没有ps到root的进程，我一开始或许就需要用 `su - root -c 'ps aux'` 来做。



## 21.kill

![image-20260721204417128](/images/image-20260721204417128.png)

```
kill PID — 发送 SIGTERM（15），请求终止
kill -9 PID — 发送 SIGKILL，强制终止
kill -HUP PID — 发送 SIGHUP，重新加载配置
kill -l — 列出所有信号

pgrep name — 按名称查找进程 PID
pkill name — 按名称终止进程
killall name — 终止所有同名进程
```

![image-20260721205451944](/images/image-20260721205451944.png)



## 22.jobs后台任务

![image-20260721205751672](/images/image-20260721205751672.png)

```
command & — 在后台运行命令
Ctrl+Z — 暂停当前前台任务

jobs — 查看后台任务列表
fg %n — 将任务 n 调到前台
bg %n — 让暂停的任务在后台继续运行

nohup command & — 退出终端后继续运行
```

![image-20260723170025005](/images/image-20260723170025005_20260723_204408.png)

好吧，感觉这个任务描述不对，第四点完全没有用，还会误导。



## 23.systemctl

![image-20260723170125455](/images/image-20260723170125455_20260723_204408.png)

```
systemctl start name — 启动服务
systemctl stop name — 停止服务
systemctl restart name — 重启服务
systemctl status name — 查看状态
systemctl enable name — 开机自启
systemctl disable name — 取消自启

查看服务列表
systemctl list-units --type=service
service --status-all（兼容旧系统）
```

![image-20260723170902029](/images/image-20260723170902029_20260723_204408.png)

讲一讲问题：

感觉不出这个 `systemctl` 有什么用，没有感觉出这个会在ctf做题中起到的作用，没有什么意思。

然后就是应该就是单纯版本问题ubuntu的版本过新，导致这个项目一直弹一些没有用的信息。



## 24.cron定时任务

![image-20260723171113434](/images/image-20260723171113434_20260723_204408.png)

```
分 时 日 月 周 命令

*  *  *  *  *  command
常用操作
crontab -e — 编辑当前用户的定时任务
crontab -l — 列出当前定时任务
crontab -r — 删除所有定时任务

时间示例
* * * * * — 每分钟
0 * * * * — 每小时
0 0 * * * — 每天午夜
0 0 * * 0 — 每周日午夜

```

![image-20260723172511695](/images/image-20260723172511695_20260723_204408.png)

讲一讲问题：

我快被这个linux终端的显示搞死了，长指令无法换行导致我看的巨难受。

然后就是依旧是没有 `cron` 这个定时任务，还得我自己装。

最后就是，我tf的crontab控制，没有全是所有都得sudo然后指定用户。

```
printf '%s\n' '* * * * * date >> ~/cron_log.txt' | sudo crontab -u student -
sudo crontab -u student -l > /home/student/my_crontab.txt
cat /home/student/my_crontab.txt
```

最后还是小小借助ai整合了一下指令。



## 25.ip和ifconfig

![image-20260723172835713](/images/image-20260723172835713_20260723_204408.png)

```
- `ip addr` — 查看所有网络接口和 IP 地址
- `ip link` — 查看网络接口状态
- `ip route` — 查看路由表

- `ifconfig` — 查看所有网络接口
- `ifconfig eth0` — 查看指定接口

- `lo` — 本地回环 127.0.0.1
- `eth0` — 第一个以太网接口
- `wlan0` — 无线网卡
```

![image-20260723173046836](/images/image-20260723173046836_20260723_204408.png)



## 26.ping和traceroute追踪

![image-20260723173122459](/images/image-20260723173122459_20260723_204408.png)

```
ping 与 traceroute

ping — 测试连通性
ping host — 持续 ping（Ctrl+C 停止）
ping -c 3 host — 只 ping 3 次
ping -W 2 host — 超时 2 秒

traceroute — 路由追踪
traceroute host — 显示到目标的路由路径
tracepath host — 类似 traceroute
```

![image-20260723173232224](/images/image-20260723173232224_20260723_204408.png)



## 27.curl和wget

![image-20260723173345427](/images/image-20260723173345427_20260723_204408.png)

```
curl — 传输数据
curl url — 获取页面内容
curl -O url — 下载文件（保留原名）
curl -o file url — 下载并指定文件名
curl -I url — 只获取响应头
curl -X POST url — 发送 POST 请求

wget — 下载文件
wget url — 下载文件
wget -O file url — 指定保存文件名
```

![image-20260723173554582](/images/image-20260723173554582_20260723_204408.png)



## 28.ss和netstat监听

![image-20260723173650030](/images/image-20260723173650030_20260723_204408.png)

```
ss — Socket Statistics（推荐）
ss -t — 显示 TCP 连接
ss -u — 显示 UDP 连接
ss -l — 只显示监听端口
ss -n — 显示数字端口号
ss -p — 显示进程信息
ss -tlnp — 常用组合：TCP 监听端口+进程

netstat（旧版）
netstat -tlnp — 类似 ss -tlnp
```

![image-20260723174327669](/images/image-20260723174327669_20260723_204408.png)

讲一讲问题：
监听还蛮有用的，一般是需要用临时服务来接收对方信息，或者来构造一个服务向对方发送信息的。我还没有搞一台服务器，之后得搞一下了，日本的vps存在断连，顶多拿来当梯子勉强用了。



## 29.dns和dig

![image-20260723174530242](/images/image-20260723174530242_20260723_204408.png)

```
DNS 配置文件
/etc/resolv.conf — DNS 服务器配置
/etc/hosts — 本地主机名映射

查询工具
dig domain — 详细 DNS 查询
nslookup domain — 简单 DNS 查询
host domain — 最简洁的查询

/etc/hosts 格式
127.0.0.1  localhost
::1        localhost
```

![image-20260723175725398](/images/image-20260723175725398_20260723_204408.png)

讲一讲问题：

这关没做好啊，感觉 ，应该更有教学感一点，比如dns是什么有什么意思，这个配置文件是什么？

[DNS](/posts/知识点/dns/)



## 30.apt包管理

![image-20260723184702844](/images/image-20260723184702844.png)

```
apt 包管理
apt update — 更新包索引
apt install pkg — 安装包
apt remove pkg — 卸载包
apt search keyword — 搜索包
apt list --installed — 列出已安装的包

dpkg
dpkg -l — 列出所有已安装包
dpkg -i file.deb — 安装 deb 包
dpkg -L pkg — 查看包安装的文件
```

![image-20260723185115682](/images/image-20260723185115682.png)

讲一讲问题：

其实就是一个简单查看项目包，嘶，这个到底怎么讲，不是很清楚，就叫库或者包吧，最常用的操作，因为有有很多简化的操作都是利用这些包来完成的。



## 31.环境变量env![image-20260723185359959](/images/image-20260723185359959.png)

```
环境变量
env — 查看所有环境变量
echo $VAR — 查看单个变量
printenv VAR — 另一种查看方式

设置环境变量
export VAR=value — 设置并导出
VAR=value — 仅在当前 shell 有效
unset VAR — 删除变量

常见环境变量
HOME — 家目录
PATH — 命令搜索路径
USER — 当前用户
SHELL — 当前 shell
```

![image-20260723185602175](/images/image-20260723185602175.png)

讲一讲问题：

环境变量，在ctf里面还挺经常出现的，很多时候都会看看环境变量是否有什么比较重要的信息，比如key密钥，目录啊，甚至flag。



## 32.path和alias

![image-20260723185706607](/images/image-20260723185706607.png)

![image-20260723185755094](/images/image-20260723185755094.png)

![image-20260723193355648](/images/image-20260723193355648.png)

讲一讲问题：
首先就是path，前面讲过了。![image-20260723193450601](/images/image-20260723193450601.png)

这个就是设置搜索目录的。

然后就是比这个别名，我猜到了，就是讲长指令用简单的来代替，就像是你的名和你的字，无论叫哪一个都是在叫你。



## 33.打包和压缩

![image-20260723193628982](/images/image-20260723193628982.png)

![image-20260723193721823](/images/image-20260723193721823.png)

![image-20260723194135985](/images/image-20260723194135985.png)

讲一讲问题：

这次是让ai帮我直接做的，因为一开始报错后，我喂给ai就变成直接命令。

首先讲一讲ai给的，前两步跟我自己的一样，而后面的打包压缩我就有点不明白了，一个czf一个xzf，不过狗来我也明白了，c指的是create创建，z指的是gzip，f指的是指定文件夹，后面-C是指文件夹，而不是文件。

至于mkdir的-p其实没有什么用，按ai讲法就是创建目录所在的父目录，已经有了就没有什么用创建的就是student这个目录。

tar的-x就是解开的意思，我其实好奇一个点gzip压缩跟zip压缩有什么区别呢？

[gzip](/posts/知识点/gzip/)



## 34.shell变量

![image-20260723201926304](/images/image-20260723201926304.png)

```
Shell 变量与引号
VAR=value — 定义变量（等号两边不能有空格）
$VAR 或 ${VAR} — 引用变量
readonly VAR — 只读变量

双引号 "" — 变量会被展开
单引号 '' — 原样输出，不展开变量
反引号 ` ` 或 $() — 命令替换
eg：
NAME="World"
echo "Hello $NAME"   # Hello World
echo 'Hello $NAME'   # Hello $NAME
```

![image-20260723202550047](/images/image-20260723202550047.png)

讲一讲问题：

其实就是一个单引号和双引号的问题，其他比如这个shell我其实觉得没有体现。

然后就是这个执行文件是~/vars.sh，而不是我自己虚拟机里面linux的使用方法。

然后就是一个cat >  xxx << 'EOF'，这个是直接使用直接创建的，也是ai特别喜欢给我的答案。



## 35.条件判断

![image-20260723202823566](/images/image-20260723202823566.png)

```
if基本语法
if [ 条件 ]; then
    命令
elif [ 条件 ]; then
    命令
else
    命令
fi

文件测试
[ -f file ] — 文件存在且是普通文件
[ -d dir ] — 目录存在
[ -e path ] — 路径存在
[ -r file ] — 文件可读

字符串比较
[ "$a" = "$b" ] — 相等
[ -z "$a" ] — 为空
[ -n "$a" ] — 非空

数字比较
[ $a -eq $b ] — 等于
[ $a -gt $b ] — 大于
[ $a -lt $b ] — 小于
```

![image-20260723203313934](/images/image-20260723203313934.png)



## 36.循环

![image-20260723203335013](/images/image-20260723203335013.png)

```
for循环
for i in 1 2 3 4 5; do
    echo $i
done

for i in $(seq 1 5); do
    echo $i
done

for file in *.txt; do
    echo $file
done

while 循环
i=1
while [ $i -le 5 ]; do
    echo $i
    i=$((i+1))
done
```

![image-20260723203654889](/images/image-20260723203654889.png)

![image-20260723203700954](/images/image-20260723203700954.png)

讲一讲问题：

我用vscode来写指令了。说实话，有点尴尬，我不是学指令，怎么像学代码了。



## 37.函数和脚本

![image-20260723203807895](/images/image-20260723203807895.png)

```
定义函数
greet() {
    echo "Hello, $1!"
}
greet World

脚本参数
$0 — 脚本名
$1, $2, ... — 第 1、2 个参数
$# — 参数个数
$@ — 所有参数
$? — 上一条命令的返回码

返回值
return 0 — 函数返回成功
return 1 — 函数返回失败
```

![image-20260723204119967](/images/image-20260723204119967.png)

![image-20260723204128711](/images/image-20260723204128711.png)

讲一讲问题：

其实关于使用这个函数，是~/文件 参数，这个参数是我们输入的也就是我们输入给函数的，所以第二个参数的输入应该是~/文件 参数1 参数2。



## ![image-20260723204309708](/images/image-20260723204309708.png)

结束，学的还行，马马虎虎。













---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

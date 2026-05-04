---
title: "WEB_发包的各种信息和形式"
image: ''
pinned: false
comment: true
published: 2026-04-19
updated: 2026-04-19
description: "WEB"
category: WEB
tags: [WEB]
---



# 



# 修改特定信息：



| name                | **作用**                 | **常用数据**                            | **渗透/测试点**                                       |
| ------------------- | ------------------------ | --------------------------------------- | ----------------------------------------------------- |
| **X-Forwarded-For** | 伪造客户端 IP            | `127.0.0.1`, `8.8.8.8`, `10.0.0.1`      | **绕过 IP 限制**（如后台限内网访问）、SQL 注入、XSS。 |
| **User-Agent**      | 声明浏览器/系统身份      | `Mozilla/5.0...`, `Googlebot`, `iPhone` | **绕过设备检测**、爬虫检测；UA 注入。                 |
| **Referer**         | 告诉服务器你从哪跳过来的 | `http://localhost/admin`, `目标域名`    | **绕过防盗链**、测试 CSRF 校验逻辑。                  |
| **Origin**          | 标识请求发起的源域名     | `http://evil.com`, `null`               | **CORS（跨域）漏洞测试**，看服务器是否盲目信任来源。  |



要求 `Only admin from 127.0.0.1 using 'CTF-Browser' can see the flag.`

bp修改数据例子：

```
POST /check_flag.php HTTP/1.1
Host: challenge.ctf
Content-Type: application/x-www-form-urlencoded
User-Agent: CTF-Browser
X-Forwarded-For: 127.0.0.1
Referer: http://127.0.0.1/admin.php
Origin: http://127.0.0.1
```









| **name**             | **作用**             | **常用数据**                          | **渗透/测试点**                                          |
| -------------------- | -------------------- | ------------------------------------- | -------------------------------------------------------- |
| **Accept**           | 客户端想接收的格式   | `application/json`, `*/*`, `text/xml` | **信息泄露**：强制服务器返回 JSON 结果；XXE 探测。       |
| **Accept-Encoding**  | 客户端支持的压缩算法 | `gzip, deflate, br`                   | **绕过 WAF**：测试防御设备是否能解压并审计流量。         |
| **Accept-Language**  | 语言偏好             | `zh-CN`, `en-US`                      | 探测不同语言环境下的报错信息，甚至注入。                 |
| **X-Requested-With** | 标识是否为 Ajax 请求 | `XMLHttpRequest`                      | **绕过 CSRF 防护**（有些后端只针对非 Ajax 请求做防护）。 |



**Accept：** 回显的格式数据

- **操作：** 在 **Repeater** 中找到这一行，直接修改。
- **Payload：**
  - `application/json`：探测 API 接口。
  - `application/xml`：探测是否支持 XML（XXE 注入）。
  - `*/*`：均可，有时能绕过 406 Not Acceptable 错误。



**Accept-Encoding：** 支持哪种压缩算法。

- **操作：** 在 **Repeater** 中修改。
- **Payload：**
  - `identity`：告诉服务器不要压缩。
  - `compress`, `deflate`：尝试不同的压缩方式。



**Accept-Language：** 支持语言

- **操作：** **Intruder** 爆破。
- **常用数据（Payload）：**
  - `en-US`, `zh-CN`, `ja-JP`, `../../../../etc/passwd`。



**X-Requested-With： **Ajax 请求的防伪标识。

- **操作：** 在 **Repeater** 中手动添加这一行。
- **Payload：**
  - `XMLHttpRequest`









| **Header 名称**            | **核心作用**          | **常用数据**         | **渗透/测试点**                                        |
| -------------------------- | --------------------- | -------------------- | ------------------------------------------------------ |
| **If-None-Match**          | 匹配 ETag（资源指纹） | `W/"5d-5c..."`       | Web 缓存。                                             |
| **Pragma / Cache-Control** | 强制不缓存            | `no-cache`           | 确保每次请求都能直达服务器，避免被旧缓存干扰测试结果。 |
| **Keep-Alive**             | 保持长连接            | `timeout=5, max=100` | 配合 `Content-Length` 测试 HTTP 请求走私。             |



**`If-None-Match` 与 `Cache-Control`**：

`A. If-None-Match (ETag 校验)`

- **使用方法：** 当第一次访问资源时，服务器会返回一个 `ETag`。下次请求时，你在 Header 里带上 `If-None-Match: [ETag值]`。
- **逻辑：**
  - **探测缓存一致性：** 如果服务器返回 `304 Not Modified`，说明你拿到的是缓存。
  - **绕过缓存：** 在 BP 中将这个 Header 删掉或者修改它的值。这样服务器就会认为你没有这个资源，被迫重新生成一份最新的数据发给你。这在测试页面是否有动态变化（如通过个 Payload 触发了不同的报错）时非常重要。

`B. Pragma / Cache-Control`

- **使用方法：** 手动在请求中添加 `Cache-Control: no-cache` 或 `Pragma: no-cache`。
- **逻辑：**
  - **确保 Payload 生效：** 在做 XSS 或 SQL 注入探测时，如果中间有 CDN，请求可能根本没到达后端。加上 `no-cache` 可以强制请求穿透缓存直达服务器。
  - **Web 缓存：** 尝试通过修改这些头，诱导缓存服务器把恶意响应存储下来。



**连接控制模块：`Keep-Alive`**

**使用方法：**

- 1. Header 中包含 `Connection: keep-alive`。
  2. 配合 `Keep-Alive: timeout=5, max=100`（指定超时时间和最大请求数）。

**用来进行 `http` 请求走私**

由于前端服务器（如 Nginx）和后端服务器（如 Tomcat）对“请求结束”的判断标准不同，可以利用长连接把一个请求“塞”进另一个请求里。

**BP 里的例子：**

假设要进行 CL.TE 型走私测试，你在 Repeater 中构造如下数据包：

```
POST / HTTP/1.1
Host: victim.com
Connection: keep-alive
Content-Length: 6
Transfer-Encoding: chunked

0

G
```

**原理：**

1. **前端服务器（CL）**：看到 `Content-Length: 6`，认为包体到 `0\r\n\r\n` 就结束了，把这部分发给后端。**(csrf)**
2. **后端服务器（TE）**：看到 `Transfer-Encoding: chunked`，它优先处理分块。看到 `0` 认为第一个请求结束了，但后面还有一个 `G`。
3. **结果**：这个 `G` 就留在了服务器的缓冲区里。当下一个请求过来时，这个 `G` 会拼在请求的最前面，导致请求变成 `GGET / ...` 。









| **Header 名称**    | **核心作用**    | **渗透/测试点**                                |
| ------------------ | --------------- | ---------------------------------------------- |
| **Content-Length** | Body 的字节长度 | **请求走私**：通过构造错误的长度骗过前端代理。 |
| **Content-Type**   | Body 的数据类型 | 配合文件上传漏洞，修改此处绕过后缀名检测。     |
| **Upgrade**        | 升级协议        | 测试协议切换时的安全缺陷。                     |



**Content-Length：** 

在 BP 中如何修改：

1. 发送请求到 **Repeater**。
2. **关键操作：** 点击菜单栏 **"Repeater"** -> 取消勾选 **"Update Content-Length"**。
3. 手动在 Header 修改数字。

**常用数据与实战例子：**

```
POST / HTTP/1.1
Content-Length: 4  (实际 Body 只有 1 字节)

1
```

- **效果：** 前端代理服务器会等第 4 个字节，导致连接挂起，或者把下一个用户的请求“拼接”到这 1 字节后面。



**Content-Type：** 指定格式。

在 BP 中如何修改：

- 在 **Repeater** 中直接修改该行。

**常用数据与实战例子：**

- **绕过文件上传限制：**

  上传一个 `webshell.php`，后端检测到后缀名不合法。

  修改： 将 `Content-Type: application/octet-stream` 改为 `image/jpeg`。

- **强制切换解析器：**

  原本是表单提交，你强行改为 `application/json` 或 `application/xml`，配合你修改后的 Body 内容。

  诱导服务器调用 JSON 或 XML 解析引擎。

  

**Upgrade：**

将当前的 HTTP 连接升级为其他协议（如 WebSocket 或 HTTP/2）。

**在 BP 中如何修改：**

- 通常需要配合 `Connection: Upgrade` 一起出现。
- 在 **Repeater** 中手动添加这两行。

**常用数据与实战例子：**

```
GET / HTTP/1.1
Host: target.com
Connection: Upgrade, HTTP2-Settings
Upgrade: h2c
```

尝试利用一些代理服务器不完全支持 `h2c`（非加密 HTTP/2）的缺陷，绕过访问控制规则，直接访问后端管理接口。







----

---

----

# 数据格式：



### 1. 数据交换格式

| **数据格式**   | **对应 MIME Type**              | **常用场景**                    |
| -------------- | ------------------------------- | ------------------------------- |
| **JSON**       | `application/json`              | Web 应用、RESTful API。         |
| **XML**        | `application/xml` 或 `text/xml` | 旧式接口、SOAP 协议。XXE 注入。 |
| **JavaScript** | `application/javascript`        | 动态加载脚本，探测敏感 JS。     |



### 2. 文本与网页格式

当你修改 `Accept` 头时，可以尝试强制服务器返回这些格式，看是否能绕过前端渲染直接看源码。

| **数据格式** | **对应 MIME Type** | **常用场景**                          |
| ------------ | ------------------ | ------------------------------------- |
| **HTML**     | `text/html`        | 标准网页。                            |
| **纯文本**   | `text/plain`       | 调试信息、日志输出、简单的 API 返回。 |
| **CSS**      | `text/css`         | 样式表。                              |
| **Markdown** | `text/markdown`    | 有时用于探测文档泄露。                |





### 3. 表单提交格式

Repeater 构造 POST 请求时，必须正确设置这些 `Content-Type`。

| **数据格式**   | **对应 MIME Type**                  | **常用场景**                       |
| -------------- | ----------------------------------- | ---------------------------------- |
| **标准表单**   | `application/x-www-form-urlencoded` | 常见的 POST 提交（如 `a=1&b=2`）。 |
| **多部分表单** | `multipart/form-data`               | 文件上传。                         |



### 4. 二进制与文件格式

| **数据格式**   | **对应 MIME Type**         | **常用场景**                           |
| -------------- | -------------------------- | -------------------------------------- |
| **二进制流**   | `application/octet-stream` | 未知类型文件、下载文件、恶意脚本伪装。 |
| **PDF**        | `application/pdf`          | PDF 解析漏洞。                         |
| **ZIP 压缩包** | `application/zip`          | 探测备份文件、测试 Zip Slip 漏洞。     |
| **图片 (PNG)** | `image/png`                | 伪装图片。                             |
| **图片 (JPG)** | `image/jpeg`               | 伪装图片。                             |



### 5. 特殊的格式

在一些特殊的漏洞（如 Hessian 反序列化、Java 相关漏洞）中会用到。

- **PDF/Word:** `application/msword`
- **YAML:** `application/x-yaml`（Spring Boot 配置漏洞会用到）
- **Hessian:** `application/x-hessian`













---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

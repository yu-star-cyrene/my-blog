import os
import re

def site_info_fix():
    print("🛠️ 博客标题修复工具 (穿透版)")
    config_path = os.path.join('src', 'config', 'siteConfig.ts')
    
    if not os.path.exists(config_path):
        print(f"❌ 找不到文件: {config_path}")
        return

    with open(config_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- 1. 获取当前值 ---
    # 正则逻辑：匹配 navbar: {...} 内部的 title
    # (navbar: ... title:)
    nav_pattern = r'(navbar:\s*\{[\s\S]*?title:\s*)["\'](.*?)["\']'
    
    match = re.search(nav_pattern, content)
    curr_val = "未找到"
    if match:
        curr_val = match.group(2)

    print(f"\n当前 [导航栏标题]: {curr_val}")
    print("-" * 30)
    
    # --- 2. 输入新标题 ---
    new_val = input("请输入新标题 (例如 '在下余林阳'): ").strip()
    
    if not new_val:
        print("未输入，已取消。")
        return

    # --- 3. 执行替换 ---
    # 直接全文替换，不再截取片段
    if match:
        # group(1) 是 `navbar: .... title:` 这部分前缀
        # 我们把它拼接上新值 f'"{new_val}"'
        new_content = re.sub(nav_pattern, f'\\1"{new_val}"', content, count=1)
        
        if new_content != content:
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"\n✅ 修改成功！")
            print(f"导航栏标题已变为: \"{new_val}\"")
            print("请运行 manager.bat 发布生效。")
        else:
            print("\n⚠️ 内容未发生变化 (可能新旧标题一致)。")
    else:
        print("\n❌ 严重错误：正则未匹配到 navbar.title 配置。")
        print("请手动检查 siteConfig.ts 是否缺少 'navbar' 或 'title' 字段。")

if __name__ == "__main__":
    site_info_fix()
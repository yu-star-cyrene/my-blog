import os
import re
import shutil
import time
import glob
from datetime import datetime

# --- 基础配置 ---
BASE_DIR = os.getcwd()
POSTS_DIR = os.path.join('src', 'content', 'posts')
CONFIG_PATH = os.path.join('src', 'config', 'siteConfig.ts')
PROFILE_CONFIG_PATH = os.path.join('src', 'config', 'profileConfig.ts')
AD_CONFIG_PATH = os.path.join('src', 'config', 'adConfig.ts')
WALLPAPER_CONFIG_PATH = os.path.join('src', 'config', 'backgroundWallpaper.ts')
PUBLIC_IMG_DIR = os.path.join('public', 'images')
ASSETS_DIR = os.path.join('public', 'assets', 'images')
WALLPAPER_DIR = os.path.join('public', 'assets', 'images')
BACKUP_DIR = r"C:\Users\G1731\Blog_Backups"
CATEGORIES = ["秘籍", "刷题", "学习", "知识点"]
COPYRIGHT = "- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。"

# ==================== 🕵️‍♂️ 辅助函数 ====================
def find_profile_config():
    if os.path.exists(PROFILE_CONFIG_PATH): return PROFILE_CONFIG_PATH
    search_dir = os.path.join('src', 'config')
    if os.path.exists(search_dir):
        for root, _, files in os.walk(search_dir):
            for f in files:
                if f.endswith('.ts'):
                    path = os.path.join(root, f)
                    try:
                        with open(path, 'r', encoding='utf-8') as file:
                            if 'name:' in file.read(): return path
                    except: pass
    return None

def auto_fix_corrupted_config(silent=False):
    if not os.path.exists(CONFIG_PATH): return
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    if re.search(r'themeColor:\s*\{\s*[a-zA-Z],', content):
        if not silent: print("\n🚑 自动修复主题色配置...")
        new_content = re.sub(r'(themeColor:\s*\{\s*)[a-zA-Z],', r'\1hue: 250,', content)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(new_content)

# ==================== 📦 备份模块 ====================
def run_backup():
    print(f"\n=== 📦 正在备份到 {BACKUP_DIR} ... ===")
    if not os.path.exists(BACKUP_DIR): os.makedirs(BACKUP_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"Blog_Backup_{timestamp}"
    zip_path = os.path.join(BACKUP_DIR, zip_name)
    try:
        temp_dir = os.path.join(BACKUP_DIR, "temp_pack")
        if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        for item in ['src', 'public', 'astro.config.mjs', 'package.json', 'tsconfig.json']:
            if os.path.exists(item):
                if os.path.isdir(item): shutil.copytree(item, os.path.join(temp_dir, item))
                else: shutil.copy2(item, temp_dir)
        shutil.make_archive(zip_path, 'zip', temp_dir)
        shutil.rmtree(temp_dir)
        print(f"✅ 备份成功: {zip_name}.zip")
    except Exception as e: print(f"❌ 备份失败: {e}")

# ==================== 🌅 壁纸管理模块 ====================
def manage_wallpaper():
    if not os.path.exists(WALLPAPER_DIR): os.makedirs(WALLPAPER_DIR)
    print("\n=== 🌅 壁纸更换中心 ===")
    print("1. 🖥️ 更换电脑端壁纸\n2. 📱 更换手机端壁纸\n3. 返回")
    c = input("请选择: ")
    if c == '3': return
    prefix = 'd' if c == '1' else 's'
    target = 'desktop' if c == '1' else 'mobile'
    
    # 不显示列表，直接操作
    print(f"\n[当前操作: {('电脑' if c=='1' else '手机')}端壁纸]")
    inp = input("👉 请拖入图片文件 (或输入文件名): ").strip().strip('"\'')
    
    if os.path.exists(inp) and os.path.isfile(inp):
        idx = 1
        while os.path.exists(os.path.join(WALLPAPER_DIR, f"{prefix}{idx}{os.path.splitext(inp)[1]}")): idx += 1
        new_name = f"{prefix}{idx}{os.path.splitext(inp)[1]}"
        shutil.copy2(inp, os.path.join(WALLPAPER_DIR, new_name))
        print(f"✅ 已导入: {new_name}")
        update_wp_conf(target, f"/assets/images/{new_name}")
    elif os.path.exists(os.path.join(WALLPAPER_DIR, inp)):
         update_wp_conf(target, f"/assets/images/{inp}")
    else:
         print("❌ 文件不存在")

def update_wp_conf(target, path):
    if not os.path.exists(WALLPAPER_CONFIG_PATH): return
    with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
    c = re.sub(r'('+target+r':\s*["\']).*?(["\'])', f'\\1{path}\\2', c)
    with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
    print("✅ 配置已更新")

# ==================== ⚙️ 配置模块 ====================
def set_logo(path, type="image"):
    if not os.path.exists(CONFIG_PATH): return
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
    nl = f'logo: {{\n\t\t\ttype: "{type}",\n\t\t\tvalue: "{path}",\n\t\t\talt: "Logo",\n\t\t}},'
    c = re.sub(r'logo:\s*\{[\s\S]*?\},', nl, c)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
    print(f"✅ Logo updated: {path}")

def update_profile_card():
    target_file = find_profile_config() or PROFILE_CONFIG_PATH
    if not os.path.exists(target_file): print("❌ 找不到 profileConfig.ts"); return
    
    print(f"\n=== 👤 个人资料卡装修 ===")
    with open(target_file, 'r', encoding='utf-8') as f: content = f.read()
    
    print("1. ✏️ 修改昵称")
    print("2. 📝 修改个人简介")
    print("3. 🖼️ 更换头像")
    c = input("👉 选择: ")
    
    new_content = content
    modified = False
    
    if c == '1':
        v = input("新昵称: ").strip()
        if v: new_content = re.sub(r'(name:\s*)["\'].*?["\']', f'\\1"{v}"', new_content); modified=True
    elif c == '2':
        v = input("新简介: ").strip()
        if v:
            if 'bio:' in new_content: new_content = re.sub(r'(bio:\s*)["\'][\s\S]*?["\']', f'\\1"{v}"', new_content)
            elif 'subtitle:' in new_content: new_content = re.sub(r'(subtitle:\s*)["\'][\s\S]*?["\']', f'\\1"{v}"', new_content)
            modified=True
    elif c == '3':
        s = input("拖入头像图片: ").strip().strip('"\'')
        if os.path.exists(s):
            if not os.path.exists(ASSETS_DIR): os.makedirs(ASSETS_DIR)
            tn = f"avatar_new{os.path.splitext(s)[1]}"
            shutil.copy2(s, os.path.join(ASSETS_DIR, tn))
            new_content = re.sub(r'(avatar:\s*["\']).*?(["\'])', f'\\1/assets/images/{tn}\\2', new_content)
            print(f"✅ 头像已更新: {tn}"); modified=True

    if modified:
        with open(target_file, 'w', encoding='utf-8') as f: f.write(new_content)
        print("✅ 资料已保存！")

def update_ad_image():
    if not os.path.exists(AD_CONFIG_PATH): print("❌ 找不到 src/config/adConfig.ts"); return
    print("\n=== 🎁 更换夸夸(侧边栏)图片 ===")
    src = input("👉 请拖入新的图片文件: ").strip().strip('"\'')
    if os.path.exists(src):
        if not os.path.exists(ASSETS_DIR): os.makedirs(ASSETS_DIR)
        ext = os.path.splitext(src)[1]
        target_name = f"praise{ext}"
        shutil.copy2(src, os.path.join(ASSETS_DIR, target_name))
        with open(AD_CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
        if 'adConfig2' in content:
            new_path = f"/assets/images/{target_name}"
            pattern = r'(adConfig2[\s\S]*?src:\s*["\']).*?(["\'])'
            if re.search(pattern, content):
                content = re.sub(pattern, f'\\1{new_path}\\2', content, count=1)
                with open(AD_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
                print(f"✅ 夸夸图已更新为: {target_name}")
            else: print("❌ 未找到 src 属性")
        else: print("❌ 未找到 adConfig2")
    else: print("❌ 文件不存在")

def disable_banner_credit():
    """隐藏横幅上的图片来源信息"""
    if not os.path.exists(WALLPAPER_CONFIG_PATH): print("❌ 找不到壁纸配置"); return
    
    with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    
    # 查找 credit 配置块，并将 enable 下的 desktop 和 mobile 设为 false
    # 使用比较宽泛的匹配，只替换 credit 下面的 enable
    if 'credit:' in content:
        # 1. 尝试找到 credit 块里的 enable
        # 替换 desktop: true -> false (只在 credit 范围内)
        pattern_d = r'(credit:[\s\S]*?enable:[\s\S]*?desktop:\s*)true'
        content = re.sub(pattern_d, r'\1false', content)
        
        # 替换 mobile: true -> false
        pattern_m = r'(credit:[\s\S]*?enable:[\s\S]*?mobile:\s*)true'
        content = re.sub(pattern_m, r'\1false', content)
        
        with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
        print("✅ 已隐藏横幅上的图片来源信息！")
    else:
        print("⚠️ 未找到 credit 配置项。")

def update_site_config():
    auto_fix_corrupted_config(silent=True)
    print("\n=== ⚙️ 博客设置中心 ===")
    print("1. 修改博客标题       2. 🔮 头像转Logo")
    print("3. 🦋 蝴蝶转Logo      4. 🍀 四叶草转Logo")
    print("5. 📂 自定义Logo      6. 🔤 纯文字Logo")
    print("7. 🎨 更改主题色      8. 修改横幅标题")
    print("9. 👤 装修个人资料    10.🎁 更换夸夸封面")
    print("11.🚫 隐藏横幅来源 (删掉右下角文字)")
    print("0. 返回")
    op = input("👉 选择: ")
    
    modified = False
    if op == '1':
        n = input("新标题: ").strip()
        if n: 
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
            c = re.sub(r'(title:\s*)["\'].*?["\']', f'\\1"{n}"', c)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
            modified = True
    elif op in ['2','3','4','5','6']:
        if op=='2': set_logo("/assets/images/avatar.webp")
        elif op=='3': set_logo("/assets/images/firefly.png")
        elif op=='4': set_logo("/assets/images/favicon.ico")
        elif op=='5':
            s = input("拖入图片: ").strip().strip('"\'')
            if os.path.exists(s):
                if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
                shutil.copy2(s, os.path.join(PUBLIC_IMG_DIR, os.path.basename(s)))
                set_logo(f"/images/{os.path.basename(s)}")
        elif op=='6': set_logo("My Blog", "text")
        modified = True
    elif op == '7':
        v = input("Hue (0-360): ").strip()
        if v.isdigit():
             with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
             c = re.sub(r'hue:\s*\d+', f'hue: {v}', c, count=1)
             with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
             modified = True
    elif op == '8':
        if os.path.exists(WALLPAPER_CONFIG_PATH):
            t = input("横幅标题: ").strip()
            with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
            c = re.sub(r'(homeText:\s*\{[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{t}"', c)
            with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
            modified = True
    elif op == '9':
        update_profile_card()
    elif op == '10':
        update_ad_image()
        modified = True
    elif op == '11':
        disable_banner_credit()
        modified = True

    if modified: 
        if input("立即预览? (y/n): ").lower() == 'y': run_dev()

# ==================== 文章管理 ====================
def process_posts(mode='format'):
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    if mode == 'new':
        t = input("标题: ").strip()
        if not t: return
        p = os.path.join(POSTS_DIR, f"{t}.md")
        with open(p, 'w', encoding='utf-8') as f: f.write(f"---\ntitle: \"{t}\"\ncategory: 学习\ntags: [学习]\n---\n\n内容...\n\n---\n\n{COPYRIGHT}\n")
        print(f"✅ Created: {p}"); return
    print("正在格式化...")
    for r, _, fs in os.walk(POSTS_DIR):
        for f in fs:
            if f.endswith('.md'):
                p = os.path.join(r, f)
                try:
                    with open(p, 'r', encoding='utf-8') as file: c = file.read()
                    if COPYRIGHT not in c: 
                        with open(p, 'a', encoding='utf-8') as file: file.write(f"\n\n---\n\n{COPYRIGHT}\n")
                except: pass
    print("✅ 完成")

# ==================== 🚀 运行模块 ====================
def run_dev():
    os.system("start http://localhost:4321")
    os.system("start cmd /k pnpm dev")

def run_deploy():
    run_backup()
    os.system("git add .")
    os.system('git commit -m "update"')
    os.system("git push origin main")
    input("Done. Enter to exit.")

if __name__ == "__main__":
    auto_fix_corrupted_config(silent=True)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*40 + "\n      🔥 Firefly 全能助手 v9.0\n" + "="*40)
        print(" 1. 📝 新建文章    5. 🗑️ 删除文章")
        print(" 2. 🧹 格式化      6. 🚀 本地预览")
        print(" 3. ⚙️  博客设置    7. ☁️ 发布博客")
        print(" 4. 🌅 换壁纸      8. 📦 手动备份")
        print("-" * 40 + "\n Q. 退出\n" + "="*40)
        c = input("👉 选择: ").lower()
        if c=='q': break
        elif c=='1': process_posts('new'); input("Ent...")
        elif c=='2': process_posts('format'); input("Ent...")
        elif c=='3': update_site_config()
        elif c=='4': manage_wallpaper(); input("Ent...")
        elif c=='5': pass 
        elif c=='6': run_dev()
        elif c=='7': run_deploy()
        elif c=='8': run_backup(); input("Ent...")
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

# ==================== 🖼️ 图片自动搬运逻辑 (核心新增) ====================
def fix_and_transport_images():
    """
    扫描所有文章，搬运 Typora 等本地绝对路径图片到博客目录并改写链接
    """
    print("\n🔍 正在扫描文章中的本地绝对路径图片...")
    if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)

    count = 0
    for root, _, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                file_path = os.path.join(root, file)
                modified = False
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 正则匹配：![alt](C:\路径\图片.png)
                pattern = r'(!\[.*?\]\()([a-zA-Z]:[\\/].*?\.(?:png|jpg|jpeg|webp|gif|svg))(\))'
                matches = re.findall(pattern, content)
                
                for prefix, local_path, suffix in matches:
                    clean_local_path = local_path.strip('"\'')
                    if os.path.exists(clean_local_path):
                        img_name = os.path.basename(clean_local_path)
                        target_path = os.path.join(PUBLIC_IMG_DIR, img_name)
                        new_web_path = f"/images/{img_name}"

                        try:
                            # 执行物理搬运
                            if not os.path.exists(target_path):
                                shutil.copy2(clean_local_path, target_path)
                            # 改写内容
                            content = content.replace(local_path, new_web_path)
                            modified = True
                            count += 1
                            print(f"  ✅ 已搬运并修复: {img_name}")
                        except Exception as e:
                            print(f"  ❌ 搬运失败 [{img_name}]: {e}")

                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
    if count > 0: print(f"✨ 图片修复完毕：共处理 {count} 张图片。")

# ==================== 🧩 Logo 核心逻辑 ====================
def scan_images():
    images = []
    if os.path.exists(PUBLIC_IMG_DIR):
        for f in os.listdir(PUBLIC_IMG_DIR):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.ico', '.svg')):
                images.append({'name': f, 'path': f'/images/{f}', 'full': os.path.join(PUBLIC_IMG_DIR, f)})
    if os.path.exists(ASSETS_DIR):
        for f in os.listdir(ASSETS_DIR):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.ico', '.svg')):
                images.append({'name': f, 'path': f'/assets/images/{f}', 'full': os.path.join(ASSETS_DIR, f)})
    return images

def pick_image_ui():
    while True:
        print("\n[📂 请选择一张图片]")
        images = scan_images()
        if not images:
            print("   (暂无图片，请使用上传功能)")
        else:
            for i, img in enumerate(images):
                print(f"   {i+1}. {img['name']}  \t({img['path']})")
        print("\nU. 📤 上传新图片\n0. 🔙 取消")
        choice = input("👉 指令: ").strip().upper()
        if choice == '0': return None
        elif choice == 'U':
            src = input("👉 拖入图片: ").strip().strip('"\'')
            if os.path.exists(src):
                if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
                fname = os.path.basename(src)
                shutil.copy2(src, os.path.join(PUBLIC_IMG_DIR, fname))
                print(f"✅ 上传成功: {fname}")
                return f"/images/{fname}"
            else: print("❌ 文件不存在"); time.sleep(1)
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(images): return images[idx]['path']
            else: print("❌ 无效序号")
        else: print("❌ 无效输入")

def set_site_logo(path):
    if not os.path.exists(CONFIG_PATH): return
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    new_block = f'logo: {{\n\t\t\ttype: "image",\n\t\t\tvalue: "{path}",\n\t\t\talt: "Logo",\n\t\t}},'
    content = re.sub(r'logo:\s*\{[\s\S]*?\},', new_block, content)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
    print(f"✅ 站点 Logo 已更新为: {path}")

def set_profile_avatar(path):
    target_file = find_profile_config() or PROFILE_CONFIG_PATH
    if not os.path.exists(target_file): return
    with open(target_file, 'r', encoding='utf-8') as f: content = f.read()
    new_content = re.sub(r'(avatar:\s*["\']).*?(["\'])', f'\\1{path}\\2', content)
    with open(target_file, 'w', encoding='utf-8') as f: f.write(new_content)
    print(f"✅ 简介头像已更新为: {path}")

def set_favicon(path):
    if not os.path.exists(CONFIG_PATH): return
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    pattern = r'(favicon:[\s\S]*?src:\s*["\']).*?(["\'])'
    if re.search(pattern, content):
        content = re.sub(pattern, f'\\1{path}\\2', content)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
        print(f"✅ 网页图标已更新为: {path}")
    else: print("❌ 未能定位 Favicon 配置")

def manage_logo_center():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== 🧩 Logo 管理中心 ===")
        print("1. 🏠 修改【站点 Logo】")
        print("2. 👤 修改【简介 Logo】")
        print("3. 🍀 修改【网页图标】")
        print("0. 🔙 返回")
        op = input("👉 选择: ")
        if op == '0': break
        elif op == '1':
            path = pick_image_ui()
            if path: set_site_logo(path); run_if_user_wants()
        elif op == '2':
            path = pick_image_ui()
            if path: set_profile_avatar(path); run_if_user_wants()
        elif op == '3':
            path = pick_image_ui()
            if path: set_favicon(path); run_if_user_wants()

# ==================== 📢 公告管理模块 ====================
def manage_announcement():
    if not os.path.exists(CONFIG_PATH): print("❌ 找不到配置"); return
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== 📢 站点公告管理 ===")
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
        content_match = re.search(r'notice:[\s\S]*?content:\s*["\'](.*?)["\']', content)
        current_msg = content_match.group(1) if content_match else "(未找到公告内容)"
        print(f"📜 当前公告: {current_msg}\n" + "-" * 30)
        print("1. ✏️ 修改公告内容\n2. 🟢 开启公告\n3. 🔴 关闭公告\n0. 🔙 返回")
        op = input("👉 选择: ")
        if op == '0': break
        modified = False
        if op == '1':
            new_msg = input("请输入新公告: ").strip()
            if new_msg:
                content = re.sub(r'(notice:[\s\S]*?content:\s*)["\'].*?["\']', f'\\1"{new_msg}"', content)
                modified = True
                print("✅ 内容已更新")
        elif op == '2' or op == '3':
            val = "true" if op == '2' else "false"
            if 'notice:' in content:
                pattern = r'(notice:[\s\S]*?enable:\s*)(?:true|false)'
                if re.search(pattern, content):
                    content = re.sub(pattern, rf'\1{val}', content)
                    modified = True
                    print(f"✅ 公告已{'开启' if op=='2' else '关闭'}")
        if modified:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
            run_if_user_wants()
        else: time.sleep(1)

# ==================== 🌅 壁纸管理模块 ====================
def manage_wallpaper():
    if not os.path.exists(WALLPAPER_DIR): os.makedirs(WALLPAPER_DIR)
    print("\n=== 🌅 壁纸更换中心 ===")
    print("1. 🖥️ 更换电脑端壁纸\n2. 📱 更换手机端壁纸\n3. 返回")
    c = input("请选择: ")
    if c == '3': return
    prefix = 'd' if c == '1' else 's'
    target = 'desktop' if c == '1' else 'mobile'
    inp = input("👉 请拖入图片: ").strip().strip('"\'')
    if os.path.exists(inp) and os.path.isfile(inp):
        idx = 1
        while os.path.exists(os.path.join(WALLPAPER_DIR, f"{prefix}{idx}{os.path.splitext(inp)[1]}")): idx += 1
        new_name = f"{prefix}{idx}{os.path.splitext(inp)[1]}"
        shutil.copy2(inp, os.path.join(WALLPAPER_DIR, new_name))
        print(f"✅ 已导入: {new_name}")
        update_wp_conf(target, f"/assets/images/{new_name}")
    elif os.path.exists(os.path.join(WALLPAPER_DIR, inp)):
         update_wp_conf(target, f"/assets/images/{inp}")
    else: print("❌ 文件不存在")

def update_wp_conf(target, path):
    if not os.path.exists(WALLPAPER_CONFIG_PATH): return
    with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
    c = re.sub(r'('+target+r':\s*["\']).*?(["\'])', f'\\1{path}\\2', c)
    with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
    print("✅ 配置已更新")

# ==================== 其他功能 ====================
def update_ad_image():
    if not os.path.exists(AD_CONFIG_PATH): print("❌ 找不到 adConfig.ts"); return
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
    else: print("❌ 文件不存在")

def disable_banner_credit():
    if not os.path.exists(WALLPAPER_CONFIG_PATH): return
    with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    if 'credit:' in content:
        content = re.sub(r'(credit:[\s\S]*?desktop:\s*)true', r'\1false', content)
        content = re.sub(r'(credit:[\s\S]*?mobile:\s*)true', r'\1false', content)
        with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
        print("✅ 已隐藏横幅来源文字！")

def run_if_user_wants():
    if input("👉 是否立即预览? (y/n): ").lower() == 'y': run_dev()

# ==================== 主菜单逻辑 ====================
def update_site_config():
    auto_fix_corrupted_config(silent=True)
    print("\n=== ⚙️ 博客设置中心 ===")
    print("1. 🔤 修改标题\n2. 📢 公告管理\n3. 🧩 Logo 管理中心\n4. 🎨 更改主题色\n5. 修改横幅标题\n6. 🎁 更换夸夸封面\n7. 🚫 隐藏横幅来源\n0. 返回")
    op = input("👉 选择: ")
    modified = False
    if op == '1':
        print("\n1. 👑 主标题\n2. 🥈 副标题\n3. 🧭 导航标题")
        sub = input("👉 选择: ")
        n = input("请输入新内容: ").strip()
        if n:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
            if sub == '1': c = re.sub(r'(siteConfig[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{n}"', c, count=1)
            elif sub == '2': c = re.sub(r'(subtitle:\s*)["\'].*?["\']', f'\\1"{n}"', c, count=1)
            elif sub == '3': c = re.sub(r'(navbar:[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{n}"', c, count=1)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
            modified = True
    elif op == '2': manage_announcement()
    elif op == '3': manage_logo_center()
    elif op == '4':
        v = input("Hue (0-360): ").strip()
        if v.isdigit():
             with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
             c = re.sub(r'hue:\s*\d+', f'hue: {v}', c, count=1)
             with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
             modified = True
    elif op == '5':
        t = input("横幅标题: ").strip()
        with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
        c = re.sub(r'(homeText:[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{t}"', c)
        with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
        modified = True
    elif op == '6': update_ad_image(); modified = True
    elif op == '7': disable_banner_credit(); modified = True
    if modified: run_if_user_wants()

# ==================== 文章管理 ====================
def process_posts(mode='format'):
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    if mode == 'new':
        t = input("标题: ").strip()
        if not t: return
        p = os.path.join(POSTS_DIR, f"{t}.md")
        with open(p, 'w', encoding='utf-8') as f: f.write(f"---\ntitle: \"{t}\"\ncategory: 刷题\ntags: [刷题]\npublished: {datetime.now().strftime('%Y-%m-%d')}\n---\n\n内容...\n\n---\n\n{COPYRIGHT}\n")
        print(f"✅ Created: {p}"); return
    
    # 核心增强：先执行图片自动搬运
    fix_and_transport_images()

    print("正在检查版权声明...")
    for r, _, fs in os.walk(POSTS_DIR):
        for f in fs:
            if f.endswith('.md'):
                p = os.path.join(r, f)
                try:
                    with open(p, 'r', encoding='utf-8') as file: c = file.read()
                    if COPYRIGHT not in c: 
                        with open(p, 'a', encoding='utf-8') as file: file.write(f"\n\n---\n\n{COPYRIGHT}\n")
                except: pass
    print("✅ 格式化维护完成")

# ==================== 🚀 运行模块 ====================
def run_dev():
    os.system("start http://localhost:4321")
    os.system("start cmd /k pnpm dev")

def run_deploy():
    run_backup()
    os.system("git add .")
    os.system('git commit -m "update blog"')
    os.system("git push origin main")
    input("Done. Enter to exit.")

if __name__ == "__main__":
    auto_fix_corrupted_config(silent=True)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*40 + "\n      🔥 余林阳 全能博客助手 \n" + "="*40)
        print(" 1. 📝 新建文章      5. 🗑️ 删除文章")
        print(" 2. 🧹 格式化         6. 🚀 本地预览")
        print(" 3. ⚙️  博客设置     7. ☁️ 发布博客")
        print(" 4. 🌅 换壁纸         8. 📦 手动备份")
        print("-" * 40 + "\n Q. 退出\n" + "="*40)
        c = input("👉 选择: ").lower()
        if c=='q': break
        elif c=='1': process_posts('new'); input("回车继续...")
        elif c=='2': process_posts('format'); input("回车继续...")
        elif c=='3': update_site_config()
        elif c=='4': manage_wallpaper(); input("回车继续...")
        elif c=='6': run_dev()
        elif c=='7': run_deploy()
        elif c=='8': run_backup(); input("回车继续...")
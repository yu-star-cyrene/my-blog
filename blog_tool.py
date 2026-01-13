import os
import re
import shutil
import time
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

# ==================== 🖼️ 图片自动搬运逻辑 ====================
def fix_and_transport_images():
    print("\n🔍 正在扫描文章中的本地绝对路径图片...")
    if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
    count = 0
    for root, _, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                file_path = os.path.join(root, file)
                modified = False
                with open(file_path, 'r', encoding='utf-8') as f: content = f.read()
                pattern = r'(!\[.*?\]\()([a-zA-Z]:[\\/].*?\.(?:png|jpg|jpeg|webp|gif|svg))(\))'
                matches = re.findall(pattern, content)
                for prefix, local_path, suffix in matches:
                    clean_local_path = local_path.strip('"\'')
                    if os.path.exists(clean_local_path):
                        img_name = os.path.basename(clean_local_path)
                        target_path = os.path.join(PUBLIC_IMG_DIR, img_name)
                        new_web_path = f"/images/{img_name}"
                        try:
                            if not os.path.exists(target_path): shutil.copy2(clean_local_path, target_path)
                            content = content.replace(local_path, new_web_path)
                            modified = True
                            count += 1
                            print(f"  ✅ 已搬运并修复: {img_name}")
                        except Exception as e: print(f"  ❌ 搬运失败 [{img_name}]: {e}")
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f: f.write(content)
    if count > 0: print(f"✨ 图片修复完毕：共处理 {count} 张图片。")

# ==================== 🧩 图片选择与 UI 逻辑 ====================
def scan_images():
    images = []
    if os.path.exists(PUBLIC_IMG_DIR):
        for f in os.listdir(PUBLIC_IMG_DIR):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.ico', '.svg')):
                images.append({'name': f, 'path': f'/images/{f}'})
    if os.path.exists(ASSETS_DIR):
        for f in os.listdir(ASSETS_DIR):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.ico', '.svg')):
                images.append({'name': f, 'path': f'/assets/images/{f}'})
    return images

def pick_image_ui():
    while True:
        print("\n[📂 请选择一张图片]")
        images = scan_images()
        if not images: print("   (暂无图片，请使用上传功能)")
        else:
            for i, img in enumerate(images):
                print(f"   {i+1}. {img['name']} \t({img['path']})")
        print("\nU. 📤 上传/拖入新图片\n0. 🔙 取消")
        choice = input("👉 指令: ").strip().upper()
        if choice == '0': return None
        elif choice == 'U':
            src = input("👉 请直接拖入本地图片文件: ").strip().strip('"\'')
            if os.path.exists(src):
                if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
                fname = os.path.basename(src)
                target = os.path.join(PUBLIC_IMG_DIR, fname)
                shutil.copy2(src, target)
                print(f"✅ 成功搬运至: /images/{fname}")
                return f"/images/{fname}"
            else: print("❌ 文件不存在")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(images): return images[idx]['path']
    return None

# ==================== 🎨 封面管理 (核心新增) ====================
def set_post_cover():
    """ 为已有文章设置封面 """
    print("\n=== 🖼️ 设置文章封面 ===")
    posts = []
    for root, _, files in os.walk(POSTS_DIR):
        for f in files:
            if f.endswith(('.md', '.mdx')):
                posts.append({'name': f, 'full': os.path.join(root, f)})
    if not posts: print("❌ 未找到文章"); return
    for i, p in enumerate(posts): print(f"  {i+1}. {p['name']}")
    
    choice = input("\n👉 请选择文章序号 (0取消): ").strip()
    if not choice or choice == '0': return
    try:
        post_path = posts[int(choice)-1]['full']
        img_path = pick_image_ui() # 这里会处理图片搬运
        if not img_path: return
        
        with open(post_path, 'r', encoding='utf-8') as f: content = f.read()
        # 智能替换或插入 image 字段
        if re.search(r'^image\s*:', content, re.MULTILINE):
            content = re.sub(r'(image:\s*).*', f'\\1"{img_path}"', content)
        else:
            content = re.sub(r'(title:.*)', f'\\1\nimage: "{img_path}"\npinned: true\ncomment: true', content)
            
        with open(post_path, 'w', encoding='utf-8') as f: f.write(content)
        print(f"✅ 封面已更新: {img_path}")
        time.sleep(1)
    except: print("❌ 操作失败")

# ==================== 🛠️ 其它设置逻辑 ====================
def set_site_logo(path):
    if not os.path.exists(CONFIG_PATH): return
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    new_block = f'logo: {{\n\t\t\ttype: "image",\n\t\t\tvalue: "{path}",\n\t\t\talt: "Logo",\n\t\t}},'
    content = re.sub(r'logo:\s*\{[\s\S]*?\},', new_block, content)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
    print(f"✅ Logo 已更新: {path}")

def set_profile_avatar(path):
    target_file = find_profile_config() or PROFILE_CONFIG_PATH
    if not os.path.exists(target_file): return
    with open(target_file, 'r', encoding='utf-8') as f: content = f.read()
    new_content = re.sub(r'(avatar:\s*["\']).*?(["\'])', f'\\1{path}\\2', content)
    with open(target_file, 'w', encoding='utf-8') as f: f.write(new_content)
    print(f"✅ 头像已更新: {path}")

def set_favicon(path):
    if not os.path.exists(CONFIG_PATH): return
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    pattern = r'(favicon:[\s\S]*?src:\s*["\']).*?(["\'])'
    if re.search(pattern, content):
        content = re.sub(pattern, f'\\1{path}\\2', content)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
        print(f"✅ Favicon 已更新: {path}")

def manage_logo_center():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== 🧩 Logo 管理中心 ===\n1. 修改【站点 Logo】\n2. 修改【简介 Logo】\n3. 修改【网页图标】\n0. 返回")
        op = input("👉 选择: ")
        if op == '0': break
        path = pick_image_ui()
        if path:
            if op == '1': set_site_logo(path)
            elif op == '2': set_profile_avatar(path)
            elif op == '3': set_favicon(path)
            run_if_user_wants()

def manage_announcement():
    if not os.path.exists(CONFIG_PATH): return
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
        content_match = re.search(r'notice:[\s\S]*?content:\s*["\'](.*?)["\']', content)
        current_msg = content_match.group(1) if content_match else "(空)"
        print(f"\n=== 📢 公告管理 ===\n📜 当前: {current_msg}\n1. 修改内容\n2. 开启\n3. 关闭\n0. 返回")
        op = input("👉 选择: ")
        if op == '0': break
        if op == '1':
            msg = input("新公告: ").strip()
            content = re.sub(r'(notice:[\s\S]*?content:\s*)["\'].*?["\']', f'\\1"{msg}"', content)
        elif op in ['2','3']:
            val = "true" if op == '2' else "false"
            content = re.sub(r'(notice:[\s\S]*?enable:\s*)(?:true|false)', rf'\1{val}', content)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
        run_if_user_wants()

def manage_wallpaper():
    print("\n=== 🌅 壁纸更换 ===\n1. 电脑端\n2. 手机端\n0. 返回")
    c = input("👉 选择: ")
    if c == '0': return
    target = 'desktop' if c == '1' else 'mobile'
    path = pick_image_ui()
    if path:
        with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
        content = re.sub(r'('+target+r':\s*["\']).*?(["\'])', f'\\1{path}\\2', content)
        with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
        print("✅ 壁纸更新成功")

def update_ad_image():
    path = pick_image_ui()
    if path:
        with open(AD_CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
        content = re.sub(r'(adConfig2[\s\S]*?src:\s*["\']).*?(["\'])', f'\\1{path}\\2', content)
        with open(AD_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
        print("✅ 夸夸图更新成功")

def disable_banner_credit():
    if not os.path.exists(WALLPAPER_CONFIG_PATH): return
    with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    content = re.sub(r'(credit:[\s\S]*?desktop:\s*)true', r'\1false', content)
    content = re.sub(r'(credit:[\s\S]*?mobile:\s*)true', r'\1false', content)
    with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
    print("✅ 已隐藏来源")

def run_if_user_wants():
    if input("👉 是否立即预览? (y/n): ").lower() == 'y': run_dev()

def update_site_config():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== ⚙️ 博客设置中心 ===\n1. 修改标题\n2. 公告管理\n3. Logo/图标管理\n4. 修改主题色\n5. 修改横幅文字\n6. 更换夸夸图\n7. 隐藏横幅来源\n0. 返回")
        op = input("👉 选择: ")
        if op == '0': break
        elif op == '1':
            n = input("新主标题: ").strip()
            if n:
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
                c = re.sub(r'(siteConfig[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{n}"', c, count=1)
                with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
        elif op == '2': manage_announcement()
        elif op == '3': manage_logo_center()
        elif op == '4':
            v = input("色调 Hue (0-360): ").strip()
            if v.isdigit():
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
                c = re.sub(r'hue:\s*\d+', f'hue: {v}', c, count=1)
                with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
        elif op == '5':
            t = input("横幅文字: ").strip()
            with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
            c = re.sub(r'(homeText:[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{t}"', c)
            with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
        elif op == '6': update_ad_image()
        elif op == '7': disable_banner_credit()
        run_if_user_wants()

# ==================== 文章管理 ====================
def process_posts(mode='format'):
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    if mode == 'new':
        t = input("文章标题: ").strip()
        if not t: return
        img_field = ""
        if input("👉 是否设置封面? (y/n): ").lower() == 'y':
            path = pick_image_ui()
            if path: img_field = f'image: "{path}"\n'
        
        p = os.path.join(POSTS_DIR, f"{t}.md")
        with open(p, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: \"{t}\"\n{img_field}category: 刷题\ntags: [刷题]\npublished: {datetime.now().strftime('%Y-%m-%d')}\npinned: false\ncomment: true\n---\n\n内容...\n\n---\n\n{COPYRIGHT}\n")
        print(f"✅ 已创建: {p}"); return
    
    fix_and_transport_images()
    for r, _, fs in os.walk(POSTS_DIR):
        for f in fs:
            if f.endswith('.md'):
                p = os.path.join(r, f)
                with open(p, 'r', encoding='utf-8') as file: c = file.read()
                if COPYRIGHT not in c:
                    with open(p, 'a', encoding='utf-8') as file: file.write(f"\n\n---\n\n{COPYRIGHT}\n")
    print("✅ 格式化完成")

def run_dev():
    os.system("start http://localhost:4321")
    os.system("start cmd /k pnpm dev")

def run_deploy():
    run_backup()
    os.system("git add .")
    os.system('git commit -m "update blog"')
    os.system("git push origin main")
    input("Done. Enter to exit.")

# ==================== 入口 ====================
if __name__ == "__main__":
    auto_fix_corrupted_config(silent=True)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*45 + "\n      🔥 余林阳 全能博客助手 \n" + "="*45)
        print("  1. 📝 新建文章       5. 🗑️ 删除文章")
        print("  2. 🧹 格式化维护     6. 🚀 本地预览")
        print("  3. ⚙️  博客设置       7. ☁️ 发布博客")
        print("  4. 🌅 换壁纸中心     8. 📦 手动备份")
        print("  9. 🖼️ 设置文章封面")
        print("-" * 45 + "\n  Q. 退出\n" + "="*45)
        c = input("👉 选择: ").lower()
        if c=='q': break
        elif c=='1': process_posts('new'); input("回车继续...")
        elif c=='2': process_posts('format'); input("回车继续...")
        elif c=='3': update_site_config()
        elif c=='4': manage_wallpaper(); input("回车继续...")
        elif c=='6': run_dev()
        elif c=='7': run_deploy()
        elif c=='8': run_backup(); input("回车继续...")
        elif c=='9': set_post_cover(); input("回车继续...")
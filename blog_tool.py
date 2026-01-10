import os
import re
import shutil
import time
import glob
from datetime import datetime

# --- 基础配置 ---
POSTS_DIR = os.path.join('src', 'content', 'posts')
CONFIG_PATH = os.path.join('src', 'config', 'siteConfig.ts')
WALLPAPER_CONFIG_PATH = os.path.join('src', 'config', 'backgroundWallpaper.ts')
PUBLIC_IMG_DIR = os.path.join('public', 'images')
WALLPAPER_DIR = os.path.join('public', 'assets', 'images')
BACKUP_DIR = r"C:\Users\G1731\Blog_Backups"
CATEGORIES = ["秘籍", "刷题", "学习", "知识点"]
COPYRIGHT = "- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。"

# ==================== 🚑 自动修复模块 (增强版) ====================
def auto_fix_corrupted_config(silent=False):
    """检测并修复被损坏的配置文件"""
    if not os.path.exists(CONFIG_PATH): return
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找 themeColor 块
    theme_match = re.search(r'themeColor:\s*\{([\s\S]*?)\},', content)
    if theme_match:
        block_content = theme_match.group(1)
        if "hue:" not in block_content or re.search(r'\s+[a-zA-Z],\s+', block_content):
            if not silent: print("\n🚑 检测到配置异常，正在自动修复...")
            default_theme_block = """themeColor: {
        hue: 250,
        fixed: false,
        defaultMode: "system",
    },"""
            new_content = re.sub(r'themeColor:\s*\{[\s\S]*?\},', default_theme_block, content)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(new_content)
            if not silent: print("✅ 文件已修复。")

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
    except Exception as e: print(f"❌ 备份失败: {e}"); return
    try:
        files = glob.glob(os.path.join(BACKUP_DIR, "Blog_Backup_*.zip"))
        files.sort(key=os.path.getmtime)
        if len(files) > 5:
            print("🧹 清理旧备份...")
            for f in files[:-5]: os.remove(f)
    except Exception as e: print(f"⚠️ 清理出错: {e}")

# ==================== 🌅 壁纸管理模块 ====================
def get_next_wallpaper_index(prefix):
    if not os.path.exists(WALLPAPER_DIR): os.makedirs(WALLPAPER_DIR)
    existing_files = glob.glob(os.path.join(WALLPAPER_DIR, f"{prefix}*.*"))
    max_idx = 0
    for f in existing_files:
        match = re.search(f"{prefix}(\d+)", os.path.basename(f))
        if match:
            idx = int(match.group(1))
            if idx > max_idx: max_idx = idx
    return max_idx + 1

def update_wallpaper_config_file(target_type, new_path):
    if not os.path.exists(WALLPAPER_CONFIG_PATH): print("❌ 找不到配置"); return
    with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    if target_type == 'desktop':
        pattern = r'(desktop:\s*["\']).*?(["\'])'
        replacement = f'\\1{new_path}\\2'
    else:
        pattern = r'(mobile:\s*["\']).*?(["\'])'
        replacement = f'\\1{new_path}\\2'
    new_content = re.sub(pattern, replacement, content)
    with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(new_content)
    print("✅ 配置文件已自动更新！")

def manage_wallpaper():
    if not os.path.exists(WALLPAPER_DIR): os.makedirs(WALLPAPER_DIR)
    print("\n=== 🌅 壁纸更换中心 ===")
    print("1. 🖥️ 更换电脑端壁纸 (d系列)")
    print("2. 📱 更换手机端壁纸 (s系列)")
    print("3. 返回")
    choice = input("请选择: ")
    if choice == '3': return
    
    if choice == '1': prefix = 'd'; target_type = 'desktop'; desc = "电脑"
    elif choice == '2': prefix = 's'; target_type = 'mobile'; desc = "手机"
    else: return

    print(f"\n--- {desc}壁纸库 ---")
    all_files = glob.glob(os.path.join(WALLPAPER_DIR, f"{prefix}*.*"))
    all_files.sort(key=lambda x: int(re.search(f"{prefix}(\d+)", os.path.basename(x)).group(1)) if re.search(f"{prefix}(\d+)", os.path.basename(x)) else 0)
    for f in all_files: print(f"   📄 {os.path.basename(f)}")
    print("-" * 30)
    print("👉 你可以直接拖入图片文件，或者输入 [S] 切换已有壁纸")
    user_input = input("请输入: ").strip().strip('"\'')

    if os.path.exists(user_input) and os.path.isfile(user_input):
        idx = get_next_wallpaper_index(prefix)
        ext = os.path.splitext(user_input)[1]
        if not ext: ext = ".jpg"
        new_name = f"{prefix}{idx}{ext}"
        new_path_abs = os.path.join(WALLPAPER_DIR, new_name)
        shutil.copy2(user_input, new_path_abs)
        print(f"✅ 图片已导入并重命名为: {new_name}")
        rel_path = f"/assets/images/{new_name}"
        update_wallpaper_config_file(target_type, rel_path)
    elif user_input.upper() == 'S':
        name = input(f"请输入库中已有的文件名 (例如 {prefix}1.webp): ").strip()
        full_path = os.path.join(WALLPAPER_DIR, name)
        if os.path.exists(full_path):
            rel_path = f"/assets/images/{name}"
            update_wallpaper_config_file(target_type, rel_path)
        else: print("❌ 找不到该文件")
    else:
        full_path = os.path.join(WALLPAPER_DIR, user_input)
        if os.path.exists(full_path):
             rel_path = f"/assets/images/{user_input}"
             update_wallpaper_config_file(target_type, rel_path)
        else: print("❌ 无效输入。")

# ==================== 📝 文章管理模块 ====================
def standardize_header(fm, path):
    raw_title = fm.get('title', os.path.basename(path).replace(".md", ""))
    title = str(raw_title).strip('"\'')
    image_val = fm.get('image', "''")
    pinned_val = 'true' if str(fm.get('pinned', 'false')).lower() == 'true' else 'false'
    date_val = fm.get('published', datetime.now().strftime('%Y-%m-%d'))
    desc_val = fm.get('description', f'"{title} 的技术复盘"')
    cat_val = fm.get('category', '学习')
    tags_val = fm.get('tags', f'[{cat_val}]')
    lines = ["---", f"title: \"{title}\"", f"image: {image_val}", f"pinned: {pinned_val}", f"comment: true", f"published: {date_val}", f"description: {desc_val}", f"category: {cat_val}", f"tags: {tags_val}", "---"]
    return "\n".join(lines)

def process_posts(mode='format'):
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    if mode == 'new':
        print("\n=== 📝 新建文章 ===")
        title = input("文章标题: ").strip()
        if not title: return
        print("分类: " + " ".join([f"[{i+1}]{c}" for i,c in enumerate(CATEGORIES)]))
        cid = input("选择分类: ")
        cat = CATEGORIES[int(cid)-1] if cid.isdigit() and 0 < int(cid) <= len(CATEGORIES) else "学习"
        path = os.path.join(POSTS_DIR, f"{title}.md")
        with open(path, 'w', encoding='utf-8') as f: f.write(f"---\ntitle: \"{title}\"\ncategory: {cat}\ntags: [{cat}]\n---\n\n## 正文\n\n在这里写内容...\n\n---\n\n{COPYRIGHT}\n")
        print(f"✅ 创建成功: {path}"); return

    print("\n=== 🧹 正在全站标准化... ===")
    count = 0
    for root, _, files in os.walk(POSTS_DIR):
        for f in files:
            if f.endswith('.md'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8') as file: content = file.read()
                    parts = content.split('---', 2)
                    header = parts[1] if len(parts) > 1 else ""
                    body = parts[2] if len(parts) > 2 else content
                    fm = {}
                    for line in header.strip().split('\n'):
                        if ':' in line: k, v = line.split(':', 1); fm[k.strip().lower()] = v.strip()
                    body_clean = "\n".join([l for l in body.split('\n') if "版权声明" not in l and "余林阳" not in l]).strip()
                    for src in re.findall(r'!\[.*?\]\((.*?)\)', body_clean):
                        src = src.strip('"\'')
                        if os.path.exists(src) and os.path.isabs(src):
                            fname = os.path.basename(src)
                            if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
                            shutil.copy2(src, os.path.join(PUBLIC_IMG_DIR, fname))
                            body_clean = body_clean.replace(src, f"/images/{fname}")
                    new_header = standardize_header(fm, path)
                    with open(path, 'w', encoding='utf-8') as file: file.write(new_header + "\n\n" + body_clean + "\n\n---\n\n" + COPYRIGHT + "\n")
                    count += 1
                except Exception as e: print(f"❌ 失败: {e}")
    print(f"✅ 已规范化 {count} 篇文章。")

# ==================== ⚙️ 配置模块 (Logo 管理) ====================
def set_logo(path_val, type_val="image"):
    """通用设置 Logo 函数"""
    if not os.path.exists(CONFIG_PATH): return
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    
    # 构造新的配置块
    new_logo = f'logo: {{\n\t\t\ttype: "{type_val}",\n\t\t\tvalue: "{path_val}",\n\t\t\talt: "Logo",\n\t\t}},'
    content = re.sub(r'logo:\s*\{[\s\S]*?\},', new_logo, content)
    
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
    print(f"✅ Logo 已设置为: {path_val}")

def update_site_config():
    auto_fix_corrupted_config(silent=True)
    if not os.path.exists(CONFIG_PATH): print("❌ 找不到配置"); return
    
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
    
    print("\n=== ⚙️ 博客设置中心 ===")
    print("1. 修改博客标题")
    print("2. 🔮 设置【头像】为 Logo (avatar.webp)")
    print("3. 🦋 设置【Firefly】为 Logo (firefly.png)")
    print("4. 🍀 设置【四叶草/Favicon】为 Logo (favicon.ico)")
    print("5. 📂 自定义 Logo 图片 (拖入文件)")
    print("6. 🔤 使用纯文字 Logo")
    print("7. 🎨 更改主题色 (Hue)")
    print("8. 修改主页横幅大标题")
    print("9. 返回")
    op = input("👉 请选择: ")
    
    modified = False
    
    if op == '1':
        name = input("请输入新名称: ").strip()
        if name:
            content = re.sub(r'(export\s+const\s+siteConfig[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{name}"', content, count=1)
            content = re.sub(r'(navbar:\s*\{[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{name}"', content, count=1)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
            print("✅ 标题已更新！"); modified = True

    elif op == '2':
        set_logo("/assets/images/avatar.webp"); modified = True
        
    elif op == '3':
        set_logo("/assets/images/firefly.png"); modified = True
        
    elif op == '4':
        set_logo("/assets/images/favicon.ico"); modified = True

    elif op == '5':
        src = input("👉 请拖入图片文件: ").strip().strip('"\'')
        if os.path.exists(src):
            if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
            fname = os.path.basename(src)
            shutil.copy2(src, os.path.join(PUBLIC_IMG_DIR, fname))
            set_logo(f"/images/{fname}"); modified = True
        else: print("❌ 文件不存在")

    elif op == '6':
        title_match = re.search(r'export\s+const\s+siteConfig[\s\S]*?title:\s*["\'](.*?)["\']', content)
        current_title = title_match.group(1) if title_match else "My Blog"
        set_logo(current_title, "text"); modified = True

    elif op == '7':
        print("\n🎨 主题色 (Hue) 范围 0 - 360")
        current_match = re.search(r'hue:\s*(\d+)', content)
        curr_val = current_match.group(1) if current_match else "未知"
        print(f"当前 Hue 值: {curr_val}")
        new_val = input("👉 请输入新数值: ").strip()
        if new_val.isdigit() and 0 <= int(new_val) <= 360:
            content = re.sub(r'hue:\s*\d+', f'hue: {new_val}', content, count=1)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)
            print(f"✅ 主题色已更新！"); auto_fix_corrupted_config(silent=False); modified = True
        else: print("❌ 无效数值")

    elif op == '8':
        if not os.path.exists(WALLPAPER_CONFIG_PATH): print("❌ 找不到壁纸配置"); return
        new_title = input("请输入新标题: ").strip()
        if new_title:
            with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: wp_content = f.read()
            wp_content = re.sub(r'(homeText:\s*\{[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{new_title}"', wp_content, count=1)
            with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(wp_content)
            print(f"✅ 横幅标题已更新！"); modified = True

    if modified:
        ask = input("\n👉 是否立即预览? (y/n): ").lower()
        if ask == 'y': run_dev()

# ==================== 🚀 运行模块 ====================
def run_dev():
    print("\n=== 🚀 正在启动本地预览... ===")
    print("✅ 服务将在新窗口运行，请稍候...")
    os.system("start http://localhost:4321")
    os.system("start cmd /k pnpm dev")

def run_deploy():
    print("\n=== ☁️ 准备发布... ===")
    run_backup()
    process_posts('format')
    print("\n提交到 GitHub...")
    os.system("git add ."); os.system('git commit -m "update blog"'); os.system("git push origin main")
    print("\n✅ 发布完成！"); input("按回车返回...")

if __name__ == "__main__":
    auto_fix_corrupted_config(silent=True)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*40)
        print("      🔥 Firefly 博客全能助手 v5.0")
        print("="*40)
        print(" 1. 📝 新建文章        5. 🗑️  删除文章")
        print(" 2. 🧹 格式化文章      6. 🚀 本地预览")
        print(" 3. ⚙️  博客设置        7. ☁️  发布博客")
        print(" 4. 🌅 更改壁纸        8. 📦 手动备份")
        print("-" * 40)
        print(" Q. 退出")
        print("="*40)
        
        c = input("👉 请选择: ").lower()
        if c == 'q': break
        elif c == '1': process_posts('new'); input("\n按回车...")
        elif c == '2': process_posts('format'); input("\n按回车...")
        elif c == '3': update_site_config()
        elif c == '4': manage_wallpaper(); input("\n按回车...")
        elif c == '5': delete_post(); input("\n按回车...")
        elif c == '6': run_dev()
        elif c == '7': run_deploy()
        elif c == '8': run_backup(); input("\n按回车...")
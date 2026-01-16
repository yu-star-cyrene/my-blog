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
# 初始分类列表
CATEGORIES = ["秘籍", "刷题", "学习", "知识点"]
COPYRIGHT = "- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。"

# ==================== 🛠️ 严格标准排版引擎 ====================
def standardize_frontmatter(content, default_title=""):
    """
    强制执行 SQL类 标准排版：
    顺序：title, image, pinned, comment, published, description, category, tags
    引号规则：title/description双引号，image单引号
    """
    parts = re.split(r'---\s*\n', content, maxsplit=2)
    if len(parts) < 3: return content
    
    header_str = parts[1]
    body = parts[2].strip()
    
    # 提取现有数据
    data = {}
    for line in header_str.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"\'')

    # 数据补全与纠错
    title = data.get('title', default_title)
    image = data.get('image', '')
    
    # 修正置顶逻辑
    pinned_raw = str(data.get('pinned', 'false')).lower()
    pinned = "true" if "tru" in pinned_raw else "false"
    
    comment_raw = str(data.get('comment', 'true')).lower()
    comment = "false" if comment_raw == "false" else "true"
    
    published = data.get('published', datetime.now().strftime('%Y-%m-%d'))
    # description 逻辑
    description = data.get('description', title)
    category = data.get('category', '刷题')
    tags = data.get('tags', f'[{category}]')

    # 生成 SQL类 标准头部
    new_header = (
        f'---\n'
        f'title: "{title}"\n'
        f'image: \'{image}\'\n'
        f'pinned: {pinned}\n'
        f'comment: {comment}\n'
        f'published: {published}\n'
        f'description: "{description}"\n'
        f'category: {category}\n'
        f'tags: {tags}\n'
        f'---'
    )
    return f"{new_header}\n\n{body}\n"

# ==================== 🕵️‍♂️ 辅助工具 ====================
def get_all_posts():
    posts = []
    if os.path.exists(POSTS_DIR):
        for f in os.listdir(POSTS_DIR):
            if f.endswith(('.md', '.mdx')):
                posts.append({'name': f, 'path': os.path.join(POSTS_DIR, f)})
    return posts

def auto_fix_corrupted_config(silent=False):
    if not os.path.exists(CONFIG_PATH): return
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
        if re.search(r'themeColor:\s*\{\s*[a-zA-Z],', content):
            new_content = re.sub(r'(themeColor:\s*\{\s*)[a-zA-Z],', r'\1hue: 250,', content)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(new_content)
    except: pass

# ==================== 📌 置顶管理 ====================
def manage_pinned_status():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        posts = get_all_posts()
        print("\n=== 📌 置顶状态管理 ===\nID   | 状态   | 文章标题\n" + "-"*40)
        for i, p in enumerate(posts):
            with open(p['path'], 'r', encoding='utf-8') as f:
                c = f.read()
                is_p = "[置顶]" if "pinned: true" in c else "[普通]"
                print(f"{i+1:<4} | {is_p:<6} | {p['name']}")
        
        c = input("\n👉 输入序号切换状态 (0返回): ").strip()
        if c == '0' or not c: break
        if c.isdigit() and 0 < int(c) <= len(posts):
            p_path = posts[int(c)-1]['path']
            with open(p_path, 'r', encoding='utf-8') as f: content = f.read()
            # 状态反转
            if "pinned: true" in content: content = content.replace("pinned: true", "pinned: false")
            else: content = content.replace("pinned: false", "pinned: true")
            # 重新校对格式
            with open(p_path, 'w', encoding='utf-8') as f: f.write(standardize_frontmatter(content, posts[int(c)-1]['name']))
            print("✅ 状态已切换。")
            time.sleep(0.5)

# ==================== 🖼️ 图片与封面 ====================
def pick_image_ui():
    print("\n[📂 选择图片]")
    images = []
    if os.path.exists(PUBLIC_IMG_DIR):
        for f in os.listdir(PUBLIC_IMG_DIR):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                images.append(f)
    for i, img in enumerate(images): print(f"  {i+1}. {img}")
    print("\nU. 📤 拖入/上传新图片 | 0. 跳过")
    c = input("👉 指令: ").strip().upper()
    if c == '0': return ""
    if c == 'U':
        src = input("👉 请拖入图片: ").strip().strip('"\'')
        if os.path.exists(src):
            fname = os.path.basename(src)
            shutil.copy2(src, os.path.join(PUBLIC_IMG_DIR, fname))
            return f"/images/{fname}"
    elif c.isdigit() and 0 < int(c) <= len(images):
        return f"/images/{images[int(c)-1]}"
    return ""

def set_post_cover():
    posts = get_all_posts()
    for i, p in enumerate(posts): print(f"{i+1}. {p['name']}")
    c = input("\n👉 选择文章序号: ")
    if c.isdigit() and 0 < int(c) <= len(posts):
        img = pick_image_ui()
        if img:
            p_path = posts[int(c)-1]['path']
            with open(p_path, 'r', encoding='utf-8') as f: content = f.read()
            if 'image:' in content: content = re.sub(r'image:.*', f"image: '{img}'", content)
            else: content = content.replace('---', f'---\nimage: \'{img}\'', 1)
            with open(p_path, 'w', encoding='utf-8') as f: f.write(standardize_frontmatter(content, posts[int(c)-1]['name']))
            print("✅ 封面已更新并自动对齐排版。")

# ==================== 📝 文章管理逻辑 (交互式新建) ====================
def process_posts(mode='format'):
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    
    if mode == 'new':
        # 1. 标题
        t = input("\n👉 请输入文章标题: ").strip()
        if not t: return
        
        # 2. 描述 (Description)
        desc = input(f"👉 请输入描述 (默认为 {t}): ").strip() or t
        
        # 3. 分类 (Category)
        print("\n--- 选择分类 ---")
        for i, cat in enumerate(CATEGORIES): print(f"  {i+1}. {cat}")
        print("  0. ➕ 新建分类")
        cat_c = input("👉 请选择序号: ").strip()
        if cat_c == '0':
            category = input("👉 请输入新分类名称: ").strip() or "刷题"
            if category not in CATEGORIES: CATEGORIES.append(category)
        else:
            category = CATEGORIES[int(cat_c)-1] if cat_c.isdigit() and 0 < int(cat_c) <= len(CATEGORIES) else "刷题"

        # 4. 置顶
        pinned = "true" if input("👉 是否置顶? (y/n): ").lower() == 'y' else "false"
        
        # 5. 封面
        img = pick_image_ui() if input("👉 是否设置封面? (y/n): ").lower() == 'y' else ""

        # 6. 生成并对齐
        p = os.path.join(POSTS_DIR, f"{t}.md")
        template = f"""---
title: "{t}"
image: '{img}'
pinned: {pinned}
comment: true
published: {datetime.now().strftime('%Y-%m-%d')}
description: "{desc}"
category: {category}
tags: [{category}]
---

内容...

---

{COPYRIGHT}"""
        with open(p, 'w', encoding='utf-8') as f: f.write(template)
        print(f"✅ 文章《{t}》已按标准格式创建成功！")
        return

    # 全站格式化维护
    print("🧹 正在全站深度格式化...")
    for p in get_all_posts():
        with open(p['path'], 'r', encoding='utf-8') as f: content = f.read()
        new = standardize_frontmatter(content, p['name'])
        if COPYRIGHT not in new: new = new.rstrip() + f"\n\n---\n\n{COPYRIGHT}\n"
        with open(p['path'], 'w', encoding='utf-8') as f: f.write(new)
    print("✅ 全站已成功校对为 SQL类 排版标准。")

# ==================== ⚙️ 设置中心功能补完 ====================
def update_site_config():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== ⚙️ 博客设置中心 ===\n1. 修改主标题\n2. 修改公告内容\n3. 修改主题色(Hue)\n4. 修改横幅文字\n0. 返回")
        op = input("👉 选择: ")
        if op == '0': break
        
        if op == '1':
            n = input("新主标题: ").strip()
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
            c = re.sub(r'(siteConfig[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{n}"', c, count=1)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
        elif op == '2':
            msg = input("新公告内容: ").strip()
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
            c = re.sub(r'(notice:[\s\S]*?content:\s*)["\'].*?["\']', f'\\1"{msg}"', c)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
        elif op == '3':
            h = input("新Hue值 (0-360): ").strip()
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
            c = re.sub(r'hue:\s*\d+', f'hue: {h}', c)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
        elif op == '4':
            t = input("横幅新文字: ").strip()
            with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
            c = re.sub(r'(homeText:[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{t}"', c)
            with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
        print("✅ 设置已保存。"); time.sleep(1)

# ==================== 🚀 运行模块 ====================
def run_dev():
    os.system("start http://localhost:4321")
    os.system("start cmd /k pnpm dev")

def run_deploy():
    os.system("git add .")
    os.system('git commit -m "update content"')
    os.system("git push origin main")
    print("✅ 发布指令已发出。")

if __name__ == "__main__":
    auto_fix_corrupted_config(silent=True)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*45 + "\n      🔥 余林阳 全能博客助手 v12.7\n" + "="*45)
        print("  1. 📝 新建文章       5. 🗑️ 删除文章")
        print("  2. 🧹 全站格式校对   6. 🚀 本地预览")
        print("  3. ⚙️  设置中心       7. ☁️ 发布博客")
        print("  4. 🌅 换壁纸中心     8. 📦 手动备份")
        print("  9. 🖼️ 设置文章封面   10. 📌 置顶管理")
        print("-" * 45 + "\n  Q. 退出\n" + "="*45)
        
        c = input("👉 选择: ").lower()
        if c == 'q': break
        elif c == '1': process_posts('new'); input("回车继续...")
        elif c == '2': process_posts('format'); input("回车继续...")
        elif c == '3': update_site_config()
        elif c == '6': run_dev()
        elif c == '7': run_deploy(); input("回车继续...")
        elif c == '9': set_post_cover(); input("回车继续...")
        elif c == '10': manage_pinned_status()
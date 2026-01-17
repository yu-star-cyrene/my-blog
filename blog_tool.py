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

# ==================== 🛠️ 严格标准排版引擎 ====================
def standardize_frontmatter(content, default_title=""):
    """ 强制执行 SQL类 标准排版 """
    parts = re.split(r'---\s*\n', content, maxsplit=2)
    if len(parts) < 3: return content
    header_str, body = parts[1], parts[2].strip()
    data = {}
    for line in header_str.split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"\'')

    title = data.get('title', default_title)
    image = data.get('image', '')
    pinned = "true" if "tru" in str(data.get('pinned', 'false')).lower() else "false"
    comment = "false" if str(data.get('comment', 'true')).lower() == "false" else "true"
    published = data.get('published', datetime.now().strftime('%Y-%m-%d'))
    description = data.get('description', title)
    category = data.get('category', '刷题')
    tags = data.get('tags', f'[{category}]')

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
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()
        if re.search(r'themeColor:\s*\{\s*[a-zA-Z],', content):
            new_content = re.sub(r'(themeColor:\s*\{\s*)[a-zA-Z],', r'\1hue: 250,', content)
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(new_content)
    except: pass

def get_all_posts():
    posts = []
    if os.path.exists(POSTS_DIR):
        for f in os.listdir(POSTS_DIR):
            if f.endswith(('.md', '.mdx')):
                posts.append({'name': f, 'path': os.path.join(POSTS_DIR, f)})
    return posts

# ==================== 📦 备份模块 (修复版) ====================
def run_backup():
    print(f"\n=== 📦 正在备份到 {BACKUP_DIR} ... ===")
    if not os.path.exists(BACKUP_DIR): 
        try: os.makedirs(BACKUP_DIR)
        except: print("❌ 无法创建备份目录"); return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"Blog_Backup_{timestamp}"
    zip_path = os.path.join(BACKUP_DIR, zip_name)
    
    try:
        # 创建临时打包目录，避开 node_modules
        temp_dir = os.path.join(BACKUP_DIR, "temp_pack")
        if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)
        
        # 仅备份核心文件和文件夹
        core_items = ['src', 'public', 'astro.config.mjs', 'package.json', 'tsconfig.json']
        for item in core_items:
            src_path = os.path.join(BASE_DIR, item)
            if os.path.exists(src_path):
                if os.path.isdir(src_path): shutil.copytree(src_path, os.path.join(temp_dir, item))
                else: shutil.copy2(src_path, temp_dir)
        
        shutil.make_archive(zip_path, 'zip', temp_dir)
        shutil.rmtree(temp_dir)
        print(f"✅ 备份成功: {zip_name}.zip")
    except Exception as e: print(f"❌ 备份失败: {e}")

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
        c = input("\n👉 输入序号切换 (0返回): ").strip()
        if c == '0' or not c: break
        if c.isdigit() and 0 < int(c) <= len(posts):
            p_path = posts[int(c)-1]['path']
            with open(p_path, 'r', encoding='utf-8') as f: content = f.read()
            content = content.replace("pinned: false", "pinned: true") if "pinned: false" in content else content.replace("pinned: true", "pinned: false")
            with open(p_path, 'w', encoding='utf-8') as f: f.write(standardize_frontmatter(content, posts[int(c)-1]['name']))
            print("✅ 状态已切换。")
            time.sleep(0.5)

# ==================== 🖼️ 图片与封面 ====================
def pick_image_ui():
    images = []
    if os.path.exists(PUBLIC_IMG_DIR):
        images = [f for f in os.listdir(PUBLIC_IMG_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    for i, img in enumerate(images): print(f"  {i+1}. {img}")
    print("\nU. 📤 拖入图片 | 0. 跳过")
    c = input("👉 指令: ").strip().upper()
    if c == '0': return ""
    if c == 'U':
        src = input("👉 请拖入图片: ").strip().strip('"\'')
        if os.path.exists(src):
            fname = os.path.basename(src)
            shutil.copy2(src, os.path.join(PUBLIC_IMG_DIR, fname))
            return f"/images/{fname}"
    elif c.isdigit() and 0 < int(c) <= len(images): return f"/images/{images[int(c)-1]}"
    return ""

def set_post_cover():
    posts = get_all_posts()
    for i, p in enumerate(posts): print(f"{i+1}. {p['name']}")
    c = input("\n👉 选择序号: ")
    if c.isdigit() and 0 < int(c) <= len(posts):
        img = pick_image_ui()
        if img:
            p_path = posts[int(c)-1]['path']
            with open(p_path, 'r', encoding='utf-8') as f: content = f.read()
            if 'image:' in content: content = re.sub(r'image:.*', f"image: '{img}'", content)
            else: content = content.replace('---', f'---\nimage: \'{img}\'', 1)
            with open(p_path, 'w', encoding='utf-8') as f: f.write(standardize_frontmatter(content, posts[int(c)-1]['name']))
            print("✅ 封面已更新。")

# ==================== 📝 文章管理逻辑 ====================
def process_posts(mode='format'):
    if mode == 'new':
        t = input("\n👉 文章标题: ").strip()
        if not t: return
        desc = input(f"👉 描述 (默认 {t}): ").strip() or t
        print("\n--- 选择分类 ---")
        for i, cat in enumerate(CATEGORIES): print(f"  {i+1}. {cat}")
        print("  0. ➕ 新建分类")
        cat_c = input("👉 选择: ").strip()
        if cat_c == '0':
            category = input("👉 新分类名: ").strip() or "刷题"
            if category not in CATEGORIES: CATEGORIES.append(category)
        else: category = CATEGORIES[int(cat_c)-1] if cat_c.isdigit() and 0 < int(cat_c) <= len(CATEGORIES) else "刷题"
        pinned = "true" if input("👉 是否置顶? (y/n): ").lower() == 'y' else "false"
        img = pick_image_ui() if input("👉 是否封面? (y/n): ").lower() == 'y' else ""
        p = os.path.join(POSTS_DIR, f"{t}.md")
        template = f'---\ntitle: "{t}"\nimage: \'{img}\'\npinned: {pinned}\ncomment: true\npublished: {datetime.now().strftime("%Y-%m-%d")}\ndescription: "{desc}"\ncategory: {category}\ntags: [{category}]\n---\n\n内容...\n\n---\n\n{COPYRIGHT}\n'
        with open(p, 'w', encoding='utf-8') as f: f.write(standardize_frontmatter(template, t))
        print(f"✅ 《{t}》创建成功！")
        return
    
    # 2. 全站校对时同时进行图片搬运
    print("\n🔍 扫描图片并校对排版...")
    # (图片搬运代码集成)
    for p in get_all_posts():
        with open(p['path'], 'r', encoding='utf-8') as f: content = f.read()
        # 自动搬运正文中的本地路径图片
        local_imgs = re.findall(r'(!\[.*?\]\()([a-zA-Z]:[\\/].*?\.(?:png|jpg|jpeg|webp|gif|svg))(\))', content)
        for _, lp, _ in local_imgs:
            clp = lp.strip('"\'')
            if os.path.exists(clp):
                fn = os.path.basename(clp)
                shutil.copy2(clp, os.path.join(PUBLIC_IMG_DIR, fn))
                content = content.replace(lp, f"/images/{fn}")
        new = standardize_frontmatter(content, p['name'])
        if COPYRIGHT not in new: new = new.rstrip() + f"\n\n---\n\n{COPYRIGHT}\n"
        with open(p['path'], 'w', encoding='utf-8') as f: f.write(new)
    print("✅ 全站校对完成。")

# ==================== ⚙️ 设置中心 ====================
def update_site_config():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n=== ⚙️ 设置中心 ===\n1. 改标题\n2. 改公告\n3. 改Hue(色调)\n4. 改横幅文字\n0. 返回")
        op = input("👉 选择: ")
        if op == '0': break
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f: c = f.read()
        if op == '1':
            n = input("新标题: ").strip()
            c = re.sub(r'(title:\s*)["\'].*?["\']', f'\\1"{n}"', c, count=1)
        elif op == '2':
            msg = input("新公告: ").strip()
            c = re.sub(r'(content:\s*)["\'].*?["\']', f'\\1"{msg}"', c, count=1)
        elif op == '3':
            h = input("Hue值: ").strip()
            c = re.sub(r'hue:\s*\d+', f'hue: {h}', c)
        elif op == '4':
            t = input("横幅文字: ").strip()
            with open(WALLPAPER_CONFIG_PATH, 'r', encoding='utf-8') as f: wc = f.read()
            wc = re.sub(r'(title:\s*)["\'].*?["\']', f'\\1"{t}"', wc, count=1)
            with open(WALLPAPER_CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(wc)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(c)
        print("✅ 已保存。"); time.sleep(1)

# ==================== 🚀 运行 ====================
def run_dev():
    os.system("start http://localhost:4321")
    os.system("start cmd /k pnpm dev")

def run_deploy():
    run_backup() # 发布前强制备份一次
    os.system("git add .")
    os.system('git commit -m "update blog content"')
    os.system("git push origin main")
    print("✅ 发布成功。")

if __name__ == "__main__":
    auto_fix_corrupted_config(silent=True)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n" + "="*45 + "\n      🔥 余林阳 全能博客助手 v12.8\n" + "="*45)
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
        elif c == '8': run_backup(); input("回车继续...")
        elif c == '9': set_post_cover(); input("回车继续...")
        elif c == '10': manage_pinned_status()
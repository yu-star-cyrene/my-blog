import os
import re
import shutil
import time
import glob
from datetime import datetime

# --- 基础配置 ---
# 博客内容目录
POSTS_DIR = os.path.join('src', 'content', 'posts')
# 配置文件路径
CONFIG_PATH = os.path.join('src', 'config', 'siteConfig.ts')
# 图片存放目录
PUBLIC_IMG_DIR = os.path.join('public', 'images')
# 备份存放目录 (你指定的路径)
BACKUP_DIR = r"C:\Users\G1731\Blog_Backups"
# 文章分类
CATEGORIES = ["秘籍", "刷题", "学习", "知识点"]
# 版权声明
COPYRIGHT = "- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。"

# ==================== 📦 备份模块 (新增) ====================

def run_backup():
    """执行本地备份 (保留最新5份)"""
    print(f"\n=== 📦 正在备份到 {BACKUP_DIR} ... ===")
    
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"创建备份目录: {BACKUP_DIR}")

    # 1. 生成备份文件名 (时间戳)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"Blog_Backup_{timestamp}"
    zip_path = os.path.join(BACKUP_DIR, zip_name)

    # 2. 打包关键目录 (src 和 public)
    # 为了防止把 node_modules 打包进去导致过大，我们只打包核心代码
    try:
        # 创建临时目录用于打包
        temp_dir = os.path.join(BACKUP_DIR, "temp_pack")
        if os.path.exists(temp_dir): shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        # 复制关键文件/文件夹
        for item in ['src', 'public', 'astro.config.mjs', 'package.json', 'tsconfig.json']:
            if os.path.exists(item):
                if os.path.isdir(item):
                    shutil.copytree(item, os.path.join(temp_dir, item))
                else:
                    shutil.copy2(item, temp_dir)
        
        # 压缩
        shutil.make_archive(zip_path, 'zip', temp_dir)
        
        # 清理临时目录
        shutil.rmtree(temp_dir)
        print(f"✅ 备份成功: {zip_name}.zip")

    except Exception as e:
        print(f"❌ 备份失败: {e}")
        return

    # 3. 自动清理旧备份 (只保留最新 5 个)
    try:
        # 获取所有 zip 备份
        files = glob.glob(os.path.join(BACKUP_DIR, "Blog_Backup_*.zip"))
        # 按修改时间排序 (新的在后)
        files.sort(key=os.path.getmtime)
        
        if len(files) > 5:
            print("🧹 清理旧备份...")
            # 删除多余的 (保留最后5个)
            files_to_delete = files[:-5]
            for f in files_to_delete:
                os.remove(f)
                print(f"   已删除过期备份: {os.path.basename(f)}")
    except Exception as e:
        print(f"⚠️ 清理旧备份出错: {e}")

# ==================== 📝 文章管理模块 ====================

def standardize_header(fm, path):
    """生成标准文章头部"""
    # 预处理字段，避免 f-string 语法错误
    raw_title = fm.get('title', os.path.basename(path).replace(".md", ""))
    title = str(raw_title).strip('"\'')
    
    image_val = fm.get('image', "''")
    pinned_val = 'true' if str(fm.get('pinned', 'false')).lower() == 'true' else 'false'
    date_val = fm.get('published', datetime.now().strftime('%Y-%m-%d'))
    
    default_desc = f'"{title} 的技术复盘"'
    desc_val = fm.get('description', default_desc)
    
    cat_val = fm.get('category', '学习')
    tags_val = fm.get('tags', f'[{cat_val}]')

    lines = [
        "---",
        f"title: \"{title}\"",
        f"image: {image_val}",
        f"pinned: {pinned_val}",
        f"comment: true",
        f"published: {date_val}",
        f"description: {desc_val}",
        f"category: {cat_val}",
        f"tags: {tags_val}",
        "---"
    ]
    return "\n".join(lines)

def process_posts(mode='format'):
    """处理文章：新建 或 格式化"""
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    
    if mode == 'new':
        print("\n=== 📝 新建文章 ===")
        title = input("文章标题: ").strip()
        if not title: return
        print("分类: " + " ".join([f"[{i+1}]{c}" for i,c in enumerate(CATEGORIES)]))
        cid = input("选择分类(默认学习): ")
        cat = CATEGORIES[int(cid)-1] if cid.isdigit() and 0 < int(cid) <= len(CATEGORIES) else "学习"
        
        path = os.path.join(POSTS_DIR, f"{title}.md")
        content = f"---\ntitle: \"{title}\"\ncategory: {cat}\ntags: [{cat}]\n---\n\n## 正文\n\n在这里写内容...\n\n---\n\n{COPYRIGHT}\n"
        with open(path, 'w', encoding='utf-8') as f: f.write(content)
        print(f"✅ 创建成功: {path}")
        return

    # 格式化模式
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
                        if ':' in line:
                            k, v = line.split(':', 1)
                            fm[k.strip().lower()] = v.strip()
                    
                    # 移除旧版权，避免重复
                    body_clean = "\n".join([l for l in body.split('\n') if "版权声明" not in l and "余林阳" not in l]).strip()
                    
                    # 搬运图片逻辑
                    img_matches = re.findall(r'!\[.*?\]\((.*?)\)', body_clean)
                    for src in img_matches:
                        src = src.strip('"\'')
                        if os.path.exists(src) and os.path.isabs(src):
                            fname = os.path.basename(src)
                            if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
                            shutil.copy2(src, os.path.join(PUBLIC_IMG_DIR, fname))
                            body_clean = body_clean.replace(src, f"/images/{fname}")
                    
                    new_header = standardize_header(fm, path)
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_header + "\n\n" + body_clean + "\n\n---\n\n" + COPYRIGHT + "\n")
                    count += 1
                except Exception as e: print(f"❌ 处理 {f} 失败: {e}")
    print(f"✅ 已规范化 {count} 篇文章。")

# ==================== ⚙️ 配置模块 ====================

def update_site_config():
    """配置管理中心"""
    if not os.path.exists(CONFIG_PATH):
        print("❌ 找不到 siteConfig.ts")
        return

    with open(CONFIG_PATH, 'r', encoding='utf-8') as f: content = f.read()

    print("\n=== ⚙️ 博客设置中心 ===")
    print("1. 修改博客标题")
    print("2. 更换 Logo 图片")
    print("3. 【关闭 Logo】 (修复裂图)")
    print("4. 返回")
    
    op = input("请选择: ")

    if op == '1':
        name = input("请输入新名称 (如 '在下余林阳'): ").strip()
        if name:
            content = re.sub(r'(export\s+const\s+siteConfig[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{name}"', content, count=1)
            content = re.sub(r'(navbar:\s*\{[\s\S]*?title:\s*)["\'].*?["\']', f'\\1"{name}"', content, count=1)
            print("✅ 标题已更新！")

    elif op == '2':
        src = input("拖入 Logo 图片: ").strip().strip('"\'')
        if os.path.exists(src):
            if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
            fname = os.path.basename(src)
            shutil.copy2(src, os.path.join(PUBLIC_IMG_DIR, fname))
            new_logo_block = f'logo: {{\n\t\t\ttype: "image",\n\t\t\tvalue: "/images/{fname}",\n\t\t\talt: "Logo",\n\t\t}},'
            content = re.sub(r'logo:\s*\{[\s\S]*?\},', new_logo_block, content)
            print("✅ Logo 已更换！")

    elif op == '3':
        new_logo_block = 'logo: {\n\t\t\ttype: "text",\n\t\t\tvalue: "",\n\t\t\talt: "",\n\t\t},'
        content = re.sub(r'logo:\s*\{[\s\S]*?\},', new_logo_block, content)
        print("✅ Logo 已关闭！(已强制设为纯文字模式)")

    with open(CONFIG_PATH, 'w', encoding='utf-8') as f: f.write(content)

def delete_post():
    """删除文章"""
    print("\n=== 🗑️ 删除文章 ===")
    posts = []
    for root, _, files in os.walk(POSTS_DIR):
        for f in files:
            if f.endswith('.md'):
                posts.append(os.path.join(root, f))
    
    for i, p in enumerate(posts):
        print(f"[{i+1}] {os.path.basename(p)}")
        
    idx = input("输入编号删除 (回车取消): ")
    if idx.isdigit() and 0 < int(idx) <= len(posts):
        target = posts[int(idx)-1]
        os.remove(target)
        print(f"✅ 已删除: {os.path.basename(target)}")

# ==================== 🚀 运行模块 ====================

def run_dev():
    """启动预览"""
    print("\n=== 🚀 正在启动本地预览... ===")
    os.system("start http://localhost:4321")
    os.system("pnpm dev")

def run_deploy():
    """发布到 GitHub (含自动备份)"""
    print("\n=== ☁️ 准备发布... ===")
    
    # 1. 先备份
    run_backup()
    
    print("\n[2/4] 规范化文章格式...")
    process_posts('format')
    
    print("\n[3/4] 提交到 GitHub...")
    os.system("git add .")
    os.system('git commit -m "update blog"')
    os.system("git push origin main")
    print("\n✅ 发布完成！")
    input("按回车键返回...")

# ==================== 主菜单 ====================

if __name__ == "__main__":
    while True:
        # 清屏 (兼容 Windows)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "="*35)
        print("   🔥 Firefly 博客全能助手")
        print("="*35)
        print(" 1. 📝 新建文章")
        print(" 2. 🧹 格式化文章 (修复版权/图片)")
        print(" 3. ⚙️  博客设置 (改名/修Logo)")
        print(" 4. 🗑️  删除文章")
        print("-" * 35)
        print(" 5. 🚀 本地预览 (Dev)")
        print(" 6. ☁️  发布博客 (Deploy+备份)")
        print(" 7. 📦 手动备份博客")
        print("-" * 35)
        print(" Q. 退出")
        print("="*35)
        
        c = input("👉 请选择: ").lower()
        
        if c == 'q': break
        elif c == '1': process_posts('new'); input("\n按回车继续...")
        elif c == '2': process_posts('format'); input("\n按回车继续...")
        elif c == '3': update_site_config(); input("\n按回车继续...")
        elif c == '4': delete_post(); input("\n按回车继续...")
        elif c == '5': run_dev()
        elif c == '6': run_deploy()
        elif c == '7': run_backup(); input("\n按回车继续...")
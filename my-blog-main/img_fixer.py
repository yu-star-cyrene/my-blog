import os
import re
import shutil
from datetime import datetime

# --- 配置区 ---
POSTS_DIR = os.path.join('src', 'content', 'posts')
PUBLIC_IMG_DIR = os.path.join('public', 'images')
# 你的基础分类
CATEGORIES = ["秘籍", "刷题", "学习", "知识点"]

def standardize_header(fm_dict, file_path):
    """强制规范化 Frontmatter 结构顺序"""
    raw_title = fm_dict.get('title', os.path.basename(file_path).replace(".md",""))
    clean_title = str(raw_title).strip('"').strip("'")
    
    title = f'"{clean_title}"'
    image = fm_dict.get('image', "''")
    
    # 置顶逻辑转换：确保是布尔值字符串
    pinned = str(fm_dict.get('pinned', 'false')).lower()
    if 'sticky' in fm_dict:
        sticky_val = fm_dict.pop('sticky')
        pinned = 'true' if str(sticky_val) == '1' else 'false'
    
    published = fm_dict.get('published', datetime.now().strftime('%Y-%m-%d'))
    
    # 处理描述，避开 Python 低版本的 f-string 语法限制
    default_desc = f'"{clean_title} 的技术复盘"'
    description = fm_dict.get('description', default_desc)
    
    category = fm_dict.get('category', '学习')
    tags = fm_dict.get('tags', f'[{category}]')

    lines = [
        "---",
        f"title: {title}",
        f"image: {image}",
        f"pinned: {pinned}",
        f"published: {published}",
        f"description: {description}",
        f"category: {category}",
        f"tags: {tags}",
        "---"
    ]
    return "\n".join(lines)

def safe_save(file_path, updates, body_text=None, is_new=False):
    """执行保存并规范化结构"""
    content = ""
    if not is_new and os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except: pass

    if '---' in content:
        parts = content.split('---', 2)
        header_part = parts[1]
        body = parts[2]
    else:
        header_part = ""
        body = body_text if body_text else content

    fm_dict = {}
    for line in header_part.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm_dict[k.strip().lower()] = v.strip()

    for k, v in updates.items():
        fm_dict[k.lower()] = v

    final_header = standardize_header(fm_dict, file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(final_header + "\n" + body.lstrip())

def create_new_post():
    """新建文章：支持从序号选分类或手动输入新分类"""
    print("\n" + "="*30 + "\n ✨ 新建规范化文章\n" + "="*30)
    title = input("📝 文章标题: ").strip()
    if not title: return

    file_path = os.path.join(POSTS_DIR, f"{title}.md")
    
    # 安全检查：防止覆盖
    if os.path.exists(file_path):
        confirm = input(f"⚠️ 文件 [{title}.md] 已存在，是否覆盖？(y/n): ")
        if confirm.lower() != 'y': return

    print("\n📂 请选择分类:")
    for i, c in enumerate(CATEGORIES):
        print(f"  [{i+1}] {c}")
    print("  [0] ➕ 手动输入新分类")
    
    choice = input("请输入编号 (默认3): ")
    
    if choice == '0':
        new_cat = input("请输入新分类名称: ").strip() or "随笔"
        category = new_cat
        if new_cat not in CATEGORIES:
            CATEGORIES.append(new_cat)
    elif choice.isdigit() and 0 < int(choice) <= len(CATEGORIES):
        category = CATEGORIES[int(choice)-1]
    else:
        category = "学习"

    body_content = f"\n## 正文开始\n\n在这里书写内容...\n\n---\n\n- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。\n"
    
    init_fm = {
        'title': f'"{title}"',
        'image': "''",
        'pinned': 'false',
        'published': datetime.now().strftime('%Y-%m-%d'),
        'category': category,
        'tags': f'[{category}]'
    }
    
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    safe_save(file_path, init_fm, body_text=body_content, is_new=True)
    print(f"\n[OK] 文章已按规范创建！分类为: {category}")

def relocate_images(file_path):
    """扫描并搬运本地图片"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'!\[.*?\]\((.*?)\)', content)
    if not matches:
        print("[提示] 正文无本地图片引用。")
        return
    
    if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
    changed = False
    for old_path in matches:
        clean_p = old_path.strip().strip('"').strip("'")
        if os.path.exists(clean_p) and os.path.isabs(clean_p):
            fname = os.path.basename(clean_p)
            dest = os.path.join(PUBLIC_IMG_DIR, fname)
            try:
                shutil.copy2(clean_p, dest)
                content = content.replace(old_path, f"/images/{fname}")
                changed = True
                print(f"  -> 已搬运图片: {fname}")
            except Exception as e:
                print(f"  !! 搬运失败: {e}")
    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    while True:
        # 获取最新文章列表
        posts = []
        for root, _, files in os.walk(POSTS_DIR):
            for f in files:
                if f.endswith(('.md', '.mdx')):
                    posts.append(os.path.join(root, f))
        
        # 按照修改时间排序
        posts.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        print("\n" + "="*40 + "\n   余林阳 博客管理工具\n" + "="*40)
        print(" [N] 🆕 新建文章 (规范格式+版权)")
        print(" [F] 🛠️  一键规范化全站文章结构")
        print("-" * 40)
        
        # --- 核心修改：去掉 15 篇限制，展示全部文章 ---
        for i, p in enumerate(posts):
            print(f" [{i+1}] {os.path.relpath(p, POSTS_DIR)}")
        print("-" * 40)
        print(f" 当前共计: {len(posts)} 篇文章")
        
        cmd = input("\n请输入编号/字母 (Q退出): ").lower()
        if cmd == 'q': break
        if cmd == 'n': 
            create_new_post()
            continue
        if cmd == 'f': 
            print("\n正在对齐全站结构...")
            for p in posts: safe_save(p, {})
            print("✨ 全站结构已整齐划一！")
            continue

        if cmd.isdigit() and 0 < int(cmd) <= len(posts):
            target = posts[int(cmd)-1]
            print(f"\n选中: {os.path.basename(target)}")
            print(" 1.修改标题 | 2.置顶切换 | 3.设置封面 | 4.搬运正文图片")
            sub = input("请选择功能: ")
            if sub == '1':
                new_t = input("请输入新标题: ")
                safe_save(target, {'title': f'"{new_t}"'})
            elif sub == '2':
                is_p = input("是否置顶? (y/n): ").lower() == 'y'
                safe_save(target, {'pinned': 'true' if is_p else 'false'})
            elif sub == '3':
                img_p = input("请拖入封面图: ").strip().strip('"').strip("'")
                if os.path.exists(img_p):
                    fname = os.path.basename(img_p)
                    if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
                    shutil.copy2(img_p, os.path.join(PUBLIC_IMG_DIR, fname))
                    safe_save(target, {'image': f"'/images/{fname}'"})
                    print("✅ 封面已规范更新")
            elif sub == '4':
                relocate_images(target)
                print("✅ 图片搬运检查完成")
            input("\n操作完成，回车返回主菜单...")
import os
import re
import shutil
from datetime import datetime

# --- 配置 ---
POSTS_DIR = os.path.join('src', 'content', 'posts')
PUBLIC_IMG_DIR = os.path.join('public', 'images')
CATEGORIES = ["秘籍", "刷题", "学习", "知识点"]
COPYRIGHT = "- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。"

def standardize_header(fm, path):
    """统一头部格式"""
    title = str(fm.get('title', os.path.basename(path).replace(".md",""))).strip('"\'')
    
    # 字段处理
    pinned = 'true' if str(fm.get('pinned', 'false')).lower() == 'true' or str(fm.get('sticky', '0')) == '1' else 'false'
    comment = str(fm.get('comment', 'true')).lower()
    cat = fm.get('category', '学习')

    # 固定顺序
    lines = [
        "---",
        f"title: \"{title}\"",
        f"image: {fm.get('image', \"''\")}",
        f"pinned: {pinned}",
        f"comment: {comment}",
        f"published: {fm.get('published', datetime.now().strftime('%Y-%m-%d'))}",
        f"description: {fm.get('description', f'\"{title} 的技术复盘\"')}",
        f"category: {cat}",
        f"tags: {fm.get('tags', f'[{cat}]')}",
        "---"
    ]
    return "\n".join(lines)

def safe_save(path, updates, body=None, is_new=False):
    """保存文章 (自动清理旧声明)"""
    content = ""
    if not is_new and os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f: content = f.read()
        except: pass

    # 分离头部和正文
    parts = content.split('---', 2)
    header_raw = parts[1] if len(parts) > 1 else ""
    body = body if body else (parts[2] if len(parts) > 2 else content)

    # 清理正文中的旧声明
    body_lines = [line for line in body.split('\n') if "版权声明" not in line and "白白毛毛" not in line]
    clean_body = "\n".join(body_lines).strip()

    # 解析旧头部
    fm = {}
    for line in header_raw.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip().lower()] = v.strip()
    
    # 更新字段
    for k, v in updates.items(): fm[k.lower()] = v

    # 写入文件
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(standardize_header(fm, path) + "\n" + clean_body + "\n\n---\n\n" + COPYRIGHT + "\n")
        if not is_new: print(f"[OK] {os.path.basename(path)}")
    except Exception as e: print(f"[错误] {e}")

def create_post():
    """新建文章"""
    print("\n--- 新建文章 ---")
    title = input("标题: ").strip()
    if not title: return
    
    print("分类: " + ", ".join([f"{i+1}.{c}" for i, c in enumerate(CATEGORIES)]))
    c_idx = input("选择(默认学习): ")
    cat = CATEGORIES[int(c_idx)-1] if c_idx.isdigit() and 0 < int(c_idx) <= len(CATEGORIES) else "学习"

    path = os.path.join(POSTS_DIR, f"{title}.md")
    init_fm = {'title': f'"{title}"', 'category': cat, 'tags': f'[{cat}]', 'comment': 'true'}
    safe_save(path, init_fm, body="\n## 正文\n\n内容...", is_new=True)
    print(f"[完成] {title}.md")

def move_images(path):
    """搬运图片到 public"""
    with open(path, 'r', encoding='utf-8') as f: content = f.read()
    matches = re.findall(r'!\[.*?\]\((.*?)\)', content)
    if not matches: return print("无本地图片")
    
    if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
    changed = False
    for src in matches:
        src = src.strip('"\'')
        if os.path.exists(src) and os.path.isabs(src):
            fname = os.path.basename(src)
            shutil.copy2(src, os.path.join(PUBLIC_IMG_DIR, fname))
            content = content.replace(src, f"/images/{fname}")
            changed = True
            print(f"搬运: {fname}")
    
    if changed:
        with open(path, 'w', encoding='utf-8') as f: f.write(content)
        print("路径已更新")

if __name__ == "__main__":
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    while True:
        posts = sorted([os.path.join(r, f) for r, _, fs in os.walk(POSTS_DIR) for f in fs if f.endswith('.md')], key=os.path.getmtime, reverse=True)
        
        print(f"\n=== 博客管理 ({len(posts)}篇) ===")
        print("N. 新建 | F. 格式化全站 | Q. 退出")
        for i, p in enumerate(posts): print(f"[{i+1}] {os.path.relpath(p, POSTS_DIR)}")
        
        cmd = input("指令: ").lower()
        if cmd == 'q': break
        if cmd == 'n': create_post(); continue
        if cmd == 'f': 
            [safe_save(p, {}) for p in posts]
            print("全站格式化完成"); continue
        
        if cmd.isdigit() and 0 < int(cmd) <= len(posts):
            p = posts[int(cmd)-1]
            print(f"\n操作: {os.path.basename(p)}")
            op = input("1.标题 2.置顶 3.封面 4.搬图 5.评论(y/n): ")
            if op == '1': safe_save(p, {'title': f'"{input("新标题: ")}"' })
            if op == '2': safe_save(p, {'pinned': 'true' if input("置顶(y/n)? ")=='y' else 'false'})
            if op == '3': 
                src = input("图片路径: ").strip('"\'')
                if os.path.exists(src):
                    dst = os.path.join(PUBLIC_IMG_DIR, os.path.basename(src))
                    shutil.copy2(src, dst)
                    safe_save(p, {'image': f"'/images/{os.path.basename(src)}'"})
            if op == '4': move_images(p)
            if op == '5': safe_save(p, {'comment': 'true' if input("开启评论(y/n)? ")=='y' else 'false'})
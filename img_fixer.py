import os
import re
import shutil

# 路径配置
POSTS_DIR = os.path.join('src', 'content', 'posts')
PUBLIC_IMG_DIR = os.path.join('public', 'images')

def force_fix_frontmatter(file_path, key, value):
    """强制修复并更新 Frontmatter 格式，支持 pinned 布尔值"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 检查分隔符
    if not content.startswith('---'):
        content = "---\n" + content
    
    parts = content.split('---')
    if len(parts) < 3:
        header_end = content.find('\n\n')
        if header_end != -1:
            content = content[:header_end] + "\n---" + content[header_end:]
        else:
            content = content + "\n---"

    # 2. 兼容性处理：将旧的 sticky 字段直接替换为 pinned
    content = re.sub(r'^sticky:.*', f'pinned: {value}', content, flags=re.M)
    
    # 3. 精准修改目标字段
    pattern = rf'^{key}:.*'
    if re.search(pattern, content, re.M):
        content = re.sub(pattern, f'{key}: {value}', content, flags=re.M)
    else:
        # 插入到 title 之后
        content = re.sub(r'(title:.*)', rf'\1\n{key}: {value}', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return content

def relocate_images(file_path):
    """【找回的功能】自动搬运正文中的本地图片"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 Markdown 图片语法: ![alt](path)
    img_regex = r'!\[.*?\]\((.*?)\)'
    matches = re.findall(img_regex, content)
    
    if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
    
    changed = False
    for old_path in matches:
        # 清理路径中的引号
        clean_path = old_path.strip().strip('"').strip("'")
        
        # 识别是否为本地绝对路径
        if os.path.exists(clean_path) and os.path.isabs(clean_path):
            file_name = os.path.basename(clean_path)
            dest_path = os.path.join(PUBLIC_IMG_DIR, file_name)
            
            # 执行物理搬运
            try:
                shutil.copy2(clean_path, dest_path)
                print(f"[OK] 搬运成功: {file_name}")
                # 替换为博客内部路径
                new_url = f"/images/{file_name}"
                content = content.replace(old_path, new_url)
                changed = True
            except Exception as e:
                print(f"[错误] 搬运 {file_name} 失败: {e}")

    if changed:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("\n[成功] 正文图片已全部物理搬运并修复路径！")
    else:
        print("\n[提示] 未在正文中发现本地图片路径。")

def handle_cover(file_path):
    path = input("请拖入封面图路径: ").strip().strip('"').strip("'")
    if os.path.exists(path):
        if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
        fname = os.path.basename(path)
        shutil.copy2(path, os.path.join(PUBLIC_IMG_DIR, fname))
        force_fix_frontmatter(file_path, 'image', f"'/images/{fname}'")
        print("[OK] 封面已设置")

if __name__ == "__main__":
    posts = []
    for root, _, files in os.walk(POSTS_DIR):
        for f in files:
            if f.endswith(('.md', '.mdx')): posts.append(os.path.join(root, f))
    
    print("\n--- 博客文章管理 (含图片自动搬运) ---")
    for i, p in enumerate(posts):
        print(f"[{i+1}] {os.path.relpath(p, POSTS_DIR)}")
    
    idx = input("\n请输入编号: ")
    if idx.isdigit() and 0 < int(idx) <= len(posts):
        target = posts[int(idx)-1]
        print("\n1.修改标题 | 2.一键置顶(y/n) | 3.设置封面 | 4.搬运正文图片")
        sub = input("请选择: ")
        if sub == '1':
            new_title = input("请输入新标题: ")
            force_fix_frontmatter(target, 'title', f'"{new_title}"')
        elif sub == '2':
            is_pinned = input("是否置顶? (y/n): ").lower() == 'y'
            val = 'true' if is_pinned else 'false'
            force_fix_frontmatter(target, 'pinned', val)
            print(f"[成功] 置顶状态已更新为 {val}")
        elif sub == '3':
            handle_cover(target)
        elif sub == '4':
            relocate_images(target)
        
        input("\n处理完成，按回车返回菜单...")
import os
import re
import shutil
from datetime import datetime

# --- 基础设置 ---
# 文章存放目录
POSTS_DIR = os.path.join('src', 'content', 'posts')
# 图片存放目录
PUBLIC_IMG_DIR = os.path.join('public', 'images')
# 文章分类选项
CATEGORIES = ["秘籍", "刷题", "学习", "知识点"]
# 自动添加的版权声明
STANDARD_COPYRIGHT = "- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。"

def standardize_header(fm_dict, file_path):
    """
    功能：统一文章头部的格式
    让所有文章的开头字段顺序都一样，治愈强迫症。
    """
    # 获取标题，如果没有就用文件名
    raw_title = fm_dict.get('title', os.path.basename(file_path).replace(".md",""))
    clean_title = str(raw_title).strip('"').strip("'")
    
    # --- 整理各个字段 ---
    title_val = f'"{clean_title}"'
    image_val = fm_dict.get('image', "''")
    
    # 处理置顶 (兼容旧写法)
    pinned_val = str(fm_dict.get('pinned', 'false')).lower()
    if 'sticky' in fm_dict:
        sticky_val = fm_dict.pop('sticky')
        pinned_val = 'true' if str(sticky_val) == '1' else 'false'
    
    # 处理评论开关 (默认开启)
    comment_val = str(fm_dict.get('comment', 'true')).lower()

    published_val = fm_dict.get('published', datetime.now().strftime('%Y-%m-%d'))
    description_val = fm_dict.get('description', f'"{clean_title} 的技术复盘"')
    
    category_val = fm_dict.get('category', '学习')
    tags_val = fm_dict.get('tags', f'[{category_val}]')

    # --- 按照这个顺序重新组合 ---
    lines = [
        "---",
        f"title: {title_val}",       # 1. 标题
        f"image: {image_val}",       # 2. 封面图
        f"pinned: {pinned_val}",     # 3. 是否置顶
        f"comment: {comment_val}",   # 4. 评论开关 (记得这里!)
        f"published: {published_val}", # 5. 发布时间
        f"description: {description_val}", # 6. 描述
        f"category: {category_val}", # 7. 分类
        f"tags: {tags_val}",         # 8. 标签
        "---"
    ]
    return "\n".join(lines)

def safe_save(file_path, updates, body_text=None, is_new=False):
    """
    功能：保存文章
    会自动清理旧的版权声明，然后加上新的，保证不重复。
    """
    content = ""
    # 如果不是新文章，先读取旧内容
    if not is_new and os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[出错] 读文件失败: {e}")
            return

    # 分离头部(header)和正文(body)
    if '---' in content:
        parts = content.split('---', 2)
        header_part = parts[1] if len(parts) > 1 else ""
        body = parts[2] if len(parts) > 2 else ""
    else:
        header_part = ""
        body = body_text if body_text else content

    # --- 清理正文逻辑 ---
    body_lines = body.split('\n')
    new_body_lines = []
    for line in body_lines:
        # 如果这一行有“版权声明”字样，直接删掉
        if "版权声明" in line or "白白毛毛" in line:
            continue
        new_body_lines.append(line)
    
    # 删掉末尾多余的空行
    clean_body = "\n".join(new_body_lines).rstrip()
    while clean_body.endswith("---") or clean_body.endswith("\n"):
        clean_body = clean_body.rsplit("---", 1)[0].rstrip() if clean_body.endswith("---") else clean_body.rstrip()

    # 在末尾加上标准的版权声明
    body = clean_body + "\n\n---\n\n" + STANDARD_COPYRIGHT + "\n"

    # --- 整理头部逻辑 ---
    fm_dict = {}
    for line in header_part.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm_dict[k.strip().lower()] = v.strip()
    
    # 更新修改的字段
    for k, v in updates.items():
        fm_dict[k.lower()] = v

    # 生成标准的头部
    final_header = standardize_header(fm_dict, file_path)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_header + "\n" + body.lstrip())
        if not is_new:
            print(f"[完成] 更新了: {os.path.basename(file_path)}")
    except Exception as e:
        print(f"[出错] 写文件失败: {e}")

def create_new_post():
    """
    功能：新建文章
    """
    print("\n" + "="*30 + "\n ✨ 新建文章\n" + "="*30)
    title = input("📝 输入标题: ").strip()
    if not title: return
    file_path = os.path.join(POSTS_DIR, f"{title}.md")

    print("\n📂 选择分类:")
    for i, c in enumerate(CATEGORIES): print(f"  [{i+1}] {c}")
    print("  [0] ➕ 手动输入")
    choice = input("编号: ")
    if choice == '0':
        category = input("输入新分类: ").strip() or "随笔"
    elif choice.isdigit() and 0 < int(choice) <= len(CATEGORIES):
        category = CATEGORIES[int(choice)-1]
    else: category = "学习"

    body_content = f"\n## 正文开始\n\n在这里写内容...\n"
    
    # 默认设置：评论开启，不置顶
    init_fm = {
        'title': f'"{title}"', 
        'image': "''", 
        'pinned': 'false', 
        'comment': 'true',
        'published': datetime.now().strftime('%Y-%m-%d'), 
        'category': category, 
        'tags': f'[{category}]'
    }
    
    safe_save(file_path, init_fm, body_text=body_content, is_new=True)
    print(f"\n[完成] 文章已创建，分类是: {category}")

def relocate_images(file_path):
    """
    功能：搬运图片到 public 目录
    """
    with open(file_path, 'r', encoding='utf-8') as f: content = f.read()
    # 找所有 Markdown 图片链接
    matches = re.findall(r'!\[.*?\]\((.*?)\)', content)
    if not matches: 
        print("没发现本地图片链接。")
        return
    
    if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
    changed = False
    for old_path in matches:
        clean_p = old_path.strip().strip('"').strip("'")
        # 只有本地绝对路径才搬运
        if os.path.exists(clean_p) and os.path.isabs(clean_p):
            fname = os.path.basename(clean_p)
            shutil.copy2(clean_p, os.path.join(PUBLIC_IMG_DIR, fname))
            # 替换路径为博客可用的 /images/xxx
            content = content.replace(old_path, f"/images/{fname}")
            changed = True
            print(f"搬运了: {fname}")
    if changed:
        with open(file_path, 'w', encoding='utf-8') as f: f.write(content)
        print("图片路径已自动修正。")

if __name__ == "__main__":
    if not os.path.exists(POSTS_DIR): os.makedirs(POSTS_DIR)
    while True:
        posts = []
        for root, _, files in os.walk(POSTS_DIR):
            for f in files:
                if f.endswith(('.md', '.mdx')):
                    posts.append(os.path.join(root, f))
        
        # 按时间排序，最新的在前面
        posts.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        print("\n" + "="*45)
        print("      博客管理工具 (Comment增强版)")
        print("="*45)
        print(" [N] 🆕 新建文章 (自动开评论)")
        print(" [F] 🛠️  一键整理全站 (统一格式+补全字段)")
        print("-" * 45)
        
        for i, p in enumerate(posts): 
            print(f" [{i+1}] {os.path.relpath(p, POSTS_DIR)}")
        
        cmd = input("\n输入编号/字母 (Q退出): ").lower()
        if cmd == 'q': break
        if cmd == 'n': create_new_post(); continue
        
        if cmd == 'f': 
            print("\n🔍 正在整理所有文章...")
            for p in posts: safe_save(p, {}) # 只是为了触发保存逻辑
            print("\n✨ 整理完成：所有文章格式统一，评论字段已补全！"); continue
        
        if cmd.isdigit() and 0 < int(cmd) <= len(posts):
            target = posts[int(cmd)-1]
            print(f"\n选中: {os.path.basename(target)}")
            print("-" * 30)
            print(" 1.改标题   | 2.改置顶   | 3.设封面")
            print(" 4.搬图片   | 5.改评论开关")
            print("-" * 30)
            
            sub = input("选功能: ")
            
            if sub == '1': 
                safe_save(target, {'title': f'"{input("新标题: ")}"'})
            
            elif sub == '2': 
                is_pin = input("是否置顶? (y=是 / n=否): ").lower() == 'y'
                safe_save(target, {'pinned': 'true' if is_pin else 'false'})
            
            elif sub == '3':
                img_p = input("把图片拖进来: ").strip().strip('"').strip("'")
                if os.path.exists(img_p):
                    fname = os.path.basename(img_p)
                    if not os.path.exists(PUBLIC_IMG_DIR): os.makedirs(PUBLIC_IMG_DIR)
                    shutil.copy2(img_p, os.path.join(PUBLIC_IMG_DIR, fname))
                    safe_save(target, {'image': f"'/images/{fname}'"})
                    print("[OK] 封面已设置")
                else:
                    print("[错误] 图片没找到")
            
            elif sub == '4': 
                relocate_images(target)
            
            elif sub == '5':
                is_comment = input("开启评论? (y=开 / n=关): ").lower() == 'y'
                safe_save(target, {'comment': 'true' if is_comment else 'false'})
            
            input("\n按回车返回...")
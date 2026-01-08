import os
import re
import shutil

# 配置路径
POSTS_DIR = os.path.join('src', 'content', 'posts')
PUBLIC_IMG_DIR = os.path.join('public', 'images')

def fix_images_in_post(file_path):
    try:
        if not os.path.exists(PUBLIC_IMG_DIR):
            os.makedirs(PUBLIC_IMG_DIR)

        # 强制使用 UTF-8 读取内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 匹配 Markdown 图片语法: ![alt](path)
        img_regex = r'!\[.*?\]\((.*?)\)'
        matches = re.findall(img_regex, content)
        
        changed = False
        for old_path in matches:
            # 移除路径中的引号
            clean_old_path = old_path.strip().strip('"').strip("'")
            
            # 只有当它是有效的本地磁盘路径时才处理
            if os.path.exists(clean_old_path) and os.path.isfile(clean_old_path):
                file_name = os.path.basename(clean_old_path)
                new_dest_path = os.path.join(PUBLIC_IMG_DIR, file_name)
                
                # 执行物理搬运
                if not os.path.exists(new_dest_path):
                    shutil.move(clean_old_path, new_dest_path)
                    print(f"[OK] 已搬运: {file_name}")
                else:
                    print(f"[跳过] 目标已存在: {file_name}")
                
                # 替换为博客网页路径
                new_url = f"/images/{file_name}"
                content = content.Replace(old_path, new_url) if hasattr(content, 'Replace') else content.replace(old_path, new_url)
                changed = True

        if changed:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("\n[成功] 文章图片路径已全部修复并完成物理搬运！")
        else:
            print("\n[提示] 未在文中发现需要搬运的本地本地路径。")
            
    except Exception as e:
        print(f"\n[错误] 处理失败: {e}")

if __name__ == "__main__":
    # 列出所有文章
    posts = []
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                posts.append(os.path.join(root, file))
    
    if not posts:
        print("未发现文章。")
    else:
        print("\n--- 请选择要修复图片的文章 ---")
        for i, p in enumerate(posts):
            print(f"[{i+1}] {os.path.relpath(p, POSTS_DIR)}")
        
        idx = input("\n请输入文章编号 (回车退出): ")
        if idx.isdigit() and 0 < int(idx) <= len(posts):
            fix_images_in_post(posts[int(idx)-1])
            input("\n处理完毕，按回车键返回...")
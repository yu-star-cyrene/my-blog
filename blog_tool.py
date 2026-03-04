import os
import re
import shutil
import time
import subprocess
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# ==================== ⚙️ 基础配置 ====================

@dataclass
class Settings:
    base_dir: Path = Path.cwd()
    posts_dir: Path = Path("src/content/posts")
    config_path: Path = Path("src/config/siteConfig.ts")
    profile_config_path: Path = Path("src/config/profileConfig.ts")
    ad_config_path: Path = Path("src/config/adConfig.ts")
    wallpaper_config_path: Path = Path("src/config/backgroundWallpaper.ts")
    public_img_dir: Path = Path("public/images")
    wallpaper_dir: Path = Path("public/assets/images")
    backup_dir: Path = Path(os.environ.get("USERPROFILE", str(Path.home()))) / "Blog_Backups"
    categories: list = None
    copyright_line: str = "- **版权声明**：本文由 **余林阳** 创作，转载请注明出处。"

    def __post_init__(self):
        if self.categories is None:
            self.categories = ["秘籍", "刷题", "学习", "知识点"]


S = Settings()
IS_WIN = os.name == "nt"


# ==================== 🧱 基础工具 ====================

def clear_screen():
    os.system("cls" if IS_WIN else "clear")


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def write_text_if_changed(p: Path, content: str):
    """只有内容变了才写回，减少IO/减少格式漂移风险"""
    old = p.read_text(encoding="utf-8") if p.exists() else ""
    if old != content:
        p.write_text(content, encoding="utf-8")


def safe_int(s: str, default: int = 0) -> int:
    try:
        return int(s)
    except:
        return default


def now_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ==================== 🧾 Frontmatter 解析/写回（稳） ====================

FM_RE = re.compile(r"(?s)^\s*---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$")

def parse_frontmatter(content: str):
    """
    返回 (meta:dict, body:str, has_fm:bool)
    只支持你现在这种 k: v 的简单风格（足够用了），并兼容 CRLF。
    """
    m = FM_RE.match(content)
    if not m:
        return {}, content.strip(), False

    header = m.group(1)
    body = m.group(2).strip()

    meta = {}
    for line in header.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()

        # 去引号
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]

        meta[k] = v
    return meta, body, True


def normalize_tags(tags: str, category: str) -> str:
    """
    保证 tags 最终输出为类似: [刷题] / [刷题, 学习]
    """
    t = (tags or "").strip()
    if not t:
        return f"[{category}]"
    if t.startswith("[") and t.endswith("]"):
        return t
    # 允许 "刷题" 这种
    return f"[{t}]"


def truthy(v: str) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}


def standardize_frontmatter(content: str, default_title: str = "") -> str:
    meta, body, has_fm = parse_frontmatter(content)

    title = meta.get("title", default_title).strip() or default_title
    image = meta.get("image", "").strip()
    pinned = "true" if truthy(meta.get("pinned", "false")) else "false"
    comment = "false" if str(meta.get("comment", "true")).strip().lower() == "false" else "true"
    published = meta.get("published", now_date()).strip() or now_date()
    description = meta.get("description", title).strip() or title
    category = meta.get("category", "刷题").strip() or "刷题"
    tags = normalize_tags(meta.get("tags", ""), category)

    new_header = (
        "---\n"
        f'title: "{title}"\n'
        f"image: '{image}'\n"
        f"pinned: {pinned}\n"
        f"comment: {comment}\n"
        f"published: {published}\n"
        f'description: "{description}"\n'
        f"category: {category}\n"
        f"tags: {tags}\n"
        "---"
    )

    return f"{new_header}\n\n{body}\n"


def update_frontmatter_field(content: str, key: str, value: str) -> str:
    meta, body, _ = parse_frontmatter(content)
    meta[key] = value

    # 用 standardize 统一输出顺序/格式
    # 这里把 meta 先写回一个临时 frontmatter 再 normalize
    temp = ["---"]
    for k, v in meta.items():
        # 尽量保留原来的写法：title/description 用双引号，image 用单引号，其它原样
        if k in {"title", "description"}:
            temp.append(f'{k}: "{v}"')
        elif k == "image":
            temp.append(f"image: '{v}'")
        else:
            temp.append(f"{k}: {v}")
    temp.append("---\n")
    temp.append(body)
    return standardize_frontmatter("\n".join(temp), meta.get("title", ""))


# ==================== 🕵️‍♂️ 配置修复 ====================

def auto_fix_corrupted_config():
    if not S.config_path.exists():
        return
    try:
        c = read_text(S.config_path)
        # 你原来的修复：themeColor: { a, ... } 这种损坏
        if re.search(r"themeColor:\s*\{\s*[a-zA-Z]\s*,", c):
            c2 = re.sub(r"(themeColor:\s*\{\s*)[a-zA-Z]\s*,", r"\1hue: 250,", c)
            write_text_if_changed(S.config_path, c2)
    except Exception:
        pass


# ==================== 📚 文章扫描 ====================

def get_all_posts():
    posts = []
    if S.posts_dir.exists():
        for p in S.posts_dir.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".md", ".mdx"}:
                posts.append({"name": p.name, "path": p})
    # 稳定排序：先文件名
    posts.sort(key=lambda x: x["name"].lower())
    return posts


def get_post_title_from_file(p: Path) -> str:
    try:
        meta, _, has_fm = parse_frontmatter(read_text(p))
        if has_fm and meta.get("title"):
            return meta["title"]
    except:
        pass
    return p.stem


# ==================== 📦 备份模块（更快：过滤大目录） ====================

def run_backup():
    ensure_dir(S.backup_dir)
    print(f"\n=== 📦 正在备份到 {S.backup_dir} ... ===")

    temp_dir = S.backup_dir / "temp_pack"
    zip_base = S.backup_dir / f"Blog_Backup_{now_stamp()}"

    def ignore_patterns(dirpath, names):
        # 过滤常见大目录/构建产物
        ignores = {
            "node_modules", ".git", ".astro", "dist", "build", ".next",
            ".DS_Store", "pnpm-lock.yaml"  # 这个你要不要备份随意；不要就留这里
        }
        return {n for n in names if n in ignores}

    try:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)

        core_items = ["src", "public", "astro.config.mjs", "package.json", "tsconfig.json"]
        for item in core_items:
            src_path = S.base_dir / item
            if not src_path.exists():
                continue
            dst_path = temp_dir / item
            if src_path.is_dir():
                shutil.copytree(src_path, dst_path, ignore=ignore_patterns)
            else:
                shutil.copy2(src_path, dst_path)

        shutil.make_archive(str(zip_base), "zip", str(temp_dir))
        shutil.rmtree(temp_dir)
        print(f"✅ 备份成功: {zip_base.name}.zip")
    except Exception as e:
        print(f"❌ 备份失败: {e}")


# ==================== 📌 置顶管理（更稳） ====================

def manage_pinned_status():
    while True:
        clear_screen()
        posts = get_all_posts()
        print("\n=== 📌 置顶状态管理 ===\nID   | 状态    | 标题 (文件)\n" + "-" * 60)
        for i, p in enumerate(posts):
            try:
                c = read_text(p["path"])
                is_p = "[置顶]" if re.search(r"(?m)^\s*pinned:\s*true\s*$", c) else "[普通]"
                title = get_post_title_from_file(p["path"])
                print(f"{i+1:<4} | {is_p:<6} | {title} ({p['name']})")
            except:
                print(f"{i+1:<4} | {'[?]':<6} | {p['name']}")

        c = input("\n👉 输入序号切换 (0返回): ").strip()
        if c == "0" or not c:
            break
        idx = safe_int(c, -1) - 1
        if 0 <= idx < len(posts):
            p_path = posts[idx]["path"]
            content = read_text(p_path)

            meta, body, has_fm = parse_frontmatter(content)
            cur = truthy(meta.get("pinned", "false"))
            meta["pinned"] = "true" if not cur else "false"

            # 重新组装再标准化
            temp = ["---"]
            for k, v in meta.items():
                if k in {"title", "description"}:
                    temp.append(f'{k}: "{v}"')
                elif k == "image":
                    temp.append(f"image: '{v}'")
                else:
                    temp.append(f"{k}: {v}")
            temp.append("---\n")
            temp.append(body)
            newc = standardize_frontmatter("\n".join(temp), get_post_title_from_file(p_path))
            write_text_if_changed(p_path, newc)

            print("✅ 状态已切换。")
            time.sleep(0.5)


# ==================== 🖼️ 图片与封面 ====================

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}

def list_public_images():
    ensure_dir(S.public_img_dir)
    imgs = [p for p in S.public_img_dir.iterdir() if p.is_file() and p.suffix.lower() in IMG_EXTS]
    imgs.sort(key=lambda x: x.name.lower())
    return imgs


def copy_image_to_public(src: Path) -> str:
    ensure_dir(S.public_img_dir)
    if not src.exists():
        return ""

    dst = S.public_img_dir / src.name
    if dst.exists():
        # 避免覆盖：加时间戳后缀
        stem = src.stem
        dst = S.public_img_dir / f"{stem}_{now_stamp()}{src.suffix}"

    shutil.copy2(src, dst)
    return f"/images/{dst.name}"


def pick_image_ui() -> str:
    imgs = list_public_images()
    print("\n=== 🖼️ 选择封面 ===")
    if not imgs:
        print("（public/images 里暂无图片）")
    else:
        for i, img in enumerate(imgs):
            print(f"  {i+1}. {img.name}")

    print("\nU. 📤 拖入图片路径 | 0. 跳过")
    c = input("👉 指令: ").strip().upper()
    if c == "0" or not c:
        return ""
    if c == "U":
        src = input("👉 请拖入图片: ").strip().strip('"\'')
        p = Path(src)
        return copy_image_to_public(p)
    if c.isdigit():
        idx = int(c) - 1
        if 0 <= idx < len(imgs):
            return f"/images/{imgs[idx].name}"
    return ""


def set_post_cover():
    posts = get_all_posts()
    if not posts:
        print("❌ 没找到文章。")
        return

    print("\n=== 🖼️ 设置文章封面 ===")
    for i, p in enumerate(posts):
        print(f"{i+1}. {get_post_title_from_file(p['path'])} ({p['name']})")

    c = input("\n👉 选择序号 (0返回): ").strip()
    if c == "0" or not c:
        return
    idx = safe_int(c, -1) - 1
    if not (0 <= idx < len(posts)):
        return

    img = pick_image_ui()
    if not img:
        print("✅ 已取消（未选择封面）。")
        return

    p_path = posts[idx]["path"]
    content = read_text(p_path)
    newc = update_frontmatter_field(content, "image", img)
    write_text_if_changed(p_path, newc)
    print("✅ 封面已更新。")


# ==================== 📝 文章管理逻辑 ====================

def ensure_copyright_block(content: str) -> str:
    """
    保证文末只有一份版权声明（你原来是用分隔线 + COPYRIGHT）
    """
    # 去掉重复的版权块（粗暴但有效）
    content2 = re.sub(r"(?s)\n---\s*\n\n- \*\*版权声明\*\*:.*?$", "", content.strip())
    content2 = content2.rstrip() + f"\n\n---\n\n{S.copyright_line}\n"
    return content2


def process_posts(mode="format"):
    ensure_dir(S.posts_dir)
    ensure_dir(S.public_img_dir)

    if mode == "new":
        t = input("\n👉 文章标题: ").strip()
        if not t:
            return
        desc = input(f"👉 描述 (默认 {t}): ").strip() or t

        print("\n--- 选择分类 ---")
        for i, cat in enumerate(S.categories):
            print(f"  {i+1}. {cat}")
        print("  0. ➕ 新建分类")
        cat_c = input("👉 选择: ").strip()

        if cat_c == "0":
            category = input("👉 新分类名: ").strip() or "刷题"
            if category not in S.categories:
                S.categories.append(category)
        else:
            idx = safe_int(cat_c, 1) - 1
            category = S.categories[idx] if 0 <= idx < len(S.categories) else "刷题"

        pinned = "true" if input("👉 是否置顶? (y/n): ").strip().lower() == "y" else "false"

        img = ""
        if input("👉 是否设置封面? (y/n): ").strip().lower() == "y":
            img = pick_image_ui()

        # 文件名清洗（避免 Windows 特殊字符）
        safe_name = re.sub(r'[\\/:*?"<>|]', "_", t).strip()
        p = S.posts_dir / f"{safe_name}.md"

        template = (
            "---\n"
            f'title: "{t}"\n'
            f"image: '{img}'\n"
            f"pinned: {pinned}\n"
            "comment: true\n"
            f"published: {now_date()}\n"
            f'description: "{desc}"\n'
            f"category: {category}\n"
            f"tags: [{category}]\n"
            "---\n\n"
            "内容...\n"
        )
        final = standardize_frontmatter(template, t)
        final = ensure_copyright_block(final)

        write_text_if_changed(p, final)
        print(f"✅ 《{t}》创建成功！")
        return

    # ========== 全站校对 ==========
    print("\n🔍 扫描图片并校对排版...")

    for p in get_all_posts():
        content = read_text(p["path"])

        # 1) 把正文里 Windows 绝对路径图片复制到 public/images 并替换成 /images/xxx
        #    只替换 markdown 图片语法里括号的路径
        local_imgs = re.findall(
            r"(!\[.*?\]\()([a-zA-Z]:[\\/].*?\.(?:png|jpg|jpeg|webp|gif|svg))(\))",
            content,
            flags=re.IGNORECASE,
        )
        for _, lp, _ in local_imgs:
            clp = Path(lp.strip().strip('"\''))
            if clp.exists():
                new_url = copy_image_to_public(clp)
                if new_url:
                    content = content.replace(lp, new_url)

        # 2) 统一 frontmatter
        content = standardize_frontmatter(content, get_post_title_from_file(p["path"]))

        # 3) 补版权
        content = ensure_copyright_block(content)

        write_text_if_changed(p["path"], content)

    print("✅ 全站校对完成。")


# ==================== 🗑️ 删除文章 ====================

def delete_post():
    posts = get_all_posts()
    if not posts:
        print("❌ 没找到文章。")
        return

    clear_screen()
    print("\n=== 🗑️ 删除文章 ===")
    for i, p in enumerate(posts):
        print(f"{i+1}. {get_post_title_from_file(p['path'])} ({p['name']})")
    c = input("\n👉 选择序号删除 (0返回): ").strip()
    if c == "0" or not c:
        return
    idx = safe_int(c, -1) - 1
    if not (0 <= idx < len(posts)):
        return

    p_path = posts[idx]["path"]
    sure = input(f"⚠️ 确认删除《{get_post_title_from_file(p_path)}》? (y/n): ").strip().lower()
    if sure == "y":
        try:
            p_path.unlink()
            print("✅ 已删除。")
        except Exception as e:
            print(f"❌ 删除失败: {e}")
    time.sleep(1)


# ==================== 🌅 换壁纸中心（可用版） ====================

def wallpaper_center():
    """
    你的 wallpaper_config_path 看起来是 TS 配置，这里做一个“改 title + 改图片路径”的通用替换：
    - title: "xxx"
    - image: "xxx" 或 wallpaper: "xxx"（如果你项目字段不是 image，就按你实际字段改下面两行 regex）
    """
    if not S.wallpaper_config_path.exists():
        print(f"❌ 找不到壁纸配置: {S.wallpaper_config_path}")
        time.sleep(1.2)
        return

    while True:
        clear_screen()
        print("\n=== 🌅 换壁纸中心 ===")
        print("1. 改横幅标题(title)")
        print("2. 选择壁纸图片(从 public/assets/images 或 public/images)")
        print("3. 随机壁纸")
        print("0. 返回")

        op = input("👉 选择: ").strip()
        if op == "0":
            return

        c = read_text(S.wallpaper_config_path)

        if op == "1":
            t = input("新标题: ").strip()
            if t:
                c2 = re.sub(r'(title:\s*)["\'].*?["\']', rf'\1"{t}"', c, count=1)
                write_text_if_changed(S.wallpaper_config_path, c2)
                print("✅ 已保存。")
                time.sleep(1)

        elif op in {"2", "3"}:
            # 允许从 wallpaper_dir / public_img_dir 两处选
            candidates = []
            if S.wallpaper_dir.exists():
                candidates += [p for p in S.wallpaper_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMG_EXTS]
            candidates += list_public_images()

            candidates = list({p.resolve() for p in candidates})
            candidates.sort(key=lambda x: x.name.lower())

            if not candidates:
                print("❌ 没找到可用壁纸图片。")
                time.sleep(1.2)
                continue

            if op == "3":
                import random
                pick = random.choice(candidates)
            else:
                for i, p in enumerate(candidates[:200]):
                    print(f"{i+1}. {p.name}")
                if len(candidates) > 200:
                    print("（图片太多，只显示前200个）")

                idx = safe_int(input("\n👉 选择序号: ").strip(), 0) - 1
                if not (0 <= idx < min(len(candidates), 200)):
                    continue
                pick = candidates[idx]

            # 统一把壁纸路径写成相对 public 的 URL
            # 如果 pick 在 public/assets/images 下 -> /assets/images/xxx
            # 如果 pick 在 public/images 下 -> /images/xxx
            pick_str = str(pick).replace("\\", "/")
            if "/public/assets/" in pick_str:
                url = pick_str.split("/public", 1)[1]
            elif "/public/" in pick_str:
                url = pick_str.split("/public", 1)[1]
            else:
                # 外部图片：复制到 public/images
                url = copy_image_to_public(pick)

            if not url.startswith("/"):
                url = "/" + url

            # ⚠️ 这里假设你的 wallpaper ts 里有 image: "..."
            # 如果你实际字段叫 wallpaper / background / src，自行把 image 改成对应字段
            c2 = re.sub(r'(image:\s*)["\'].*?["\']', rf'\1"{url}"', c, count=1)
            if c2 == c:
                # 如果没 image 字段，尝试 wallpaper 字段
                c2 = re.sub(r'(wallpaper:\s*)["\'].*?["\']', rf'\1"{url}"', c, count=1)

            write_text_if_changed(S.wallpaper_config_path, c2)
            print(f"✅ 壁纸已更新: {url}")
            time.sleep(1.2)


# ==================== ⚙️ 设置中心 ====================

def update_site_config():
    if not S.config_path.exists():
        print(f"❌ 找不到配置文件: {S.config_path}")
        time.sleep(1.2)
        return

    while True:
        clear_screen()
        print("\n=== ⚙️ 设置中心 ===\n1. 改标题\n2. 改公告\n3. 改Hue(色调)\n0. 返回")
        op = input("👉 选择: ").strip()
        if op == "0":
            break

        c = read_text(S.config_path)

        if op == "1":
            n = input("新标题: ").strip()
            if n:
                c = re.sub(r'(title:\s*)["\'].*?["\']', rf'\1"{n}"', c, count=1)

        elif op == "2":
            msg = input("新公告: ").strip()
            if msg:
                c = re.sub(r'(content:\s*)["\'].*?["\']', rf'\1"{msg}"', c, count=1)

        elif op == "3":
            h = input("Hue值: ").strip()
            if h.isdigit():
                c = re.sub(r"hue:\s*\d+", f"hue: {h}", c)

        write_text_if_changed(S.config_path, c)
        print("✅ 已保存。")
        time.sleep(1)


# ==================== 🚀 运行与发布（更稳） ====================

def run_dev():
    # 打开浏览器
    try:
        webbrowser.open("http://localhost:4321")
    except:
        pass

    # 启动 pnpm dev
    try:
        if IS_WIN:
            os.system("start cmd /k pnpm dev")
        else:
            subprocess.Popen(["pnpm", "dev"], cwd=str(S.base_dir))
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        time.sleep(1.2)


def has_git_changes() -> bool:
    try:
        r = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        return bool(r.stdout.strip())
    except:
        return True  # 不确定就当有变化


def run_deploy():
    run_backup()

    if not has_git_changes():
        print("✅ 没有检测到改动，无需提交。")
        return

    def run_cmd(cmd):
        return subprocess.run(cmd, check=False, capture_output=True, text=True)

    r = run_cmd(["git", "add", "."])
    if r.returncode != 0:
        print("❌ git add 失败：", r.stderr.strip() or r.stdout.strip())
        return

    msg = f"update blog content {now_stamp()}"
    r = run_cmd(["git", "commit", "-m", msg])
    if r.returncode != 0:
        # 可能是 no changes / hooks 等
        out = (r.stderr.strip() or r.stdout.strip())
        print("⚠️ git commit 提示：", out)
        # 不直接 return，尝试 push（有时你本地 commit hook 拦了）
    r = run_cmd(["git", "push", "origin", "main"])
    if r.returncode != 0:
        print("❌ git push 失败：", r.stderr.strip() or r.stdout.strip())
        return

    print("✅ 发布成功。")


# ==================== 🧭 主菜单 ====================

def main():
    auto_fix_corrupted_config()
    ensure_dir(S.posts_dir)
    ensure_dir(S.public_img_dir)

    while True:
        clear_screen()
        print("\n" + "=" * 45 + "\n      🔥 余林阳 全能博客助手 v13.0\n" + "=" * 45)
        print("  1. 📝 新建文章       5. 🗑️ 删除文章")
        print("  2. 🧹 全站格式校对    6. 🚀 本地预览")
        print("  3. ⚙️  设置中心       7. ☁️ 发布博客")
        print("  4. 🌅 换壁纸中心      8. 📦 手动备份")
        print("  9. 🖼️ 设置文章封面    10. 📌 置顶管理")
        print("-" * 45 + "\n  Q. 退出\n" + "=" * 45)

        c = input("👉 选择: ").strip().lower()
        if c == "q":
            break
        elif c == "1":
            process_posts("new")
            input("回车继续...")
        elif c == "2":
            process_posts("format")
            input("回车继续...")
        elif c == "3":
            update_site_config()
        elif c == "4":
            wallpaper_center()
        elif c == "5":
            delete_post()
            input("回车继续...")
        elif c == "6":
            run_dev()
        elif c == "7":
            run_deploy()
            input("回车继续...")
        elif c == "8":
            run_backup()
            input("回车继续...")
        elif c == "9":
            set_post_cover()
            input("回车继续...")
        elif c == "10":
            manage_pinned_status()
        else:
            pass


if __name__ == "__main__":
    main()
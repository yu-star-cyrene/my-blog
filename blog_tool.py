import os
import re
import json
import shutil
import time
import subprocess
import webbrowser
import getpass
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# ==================== ⚙️ 基础配置 ====================

def _default_base_dir() -> Path:
    try:
        return Path(__file__).resolve().parent
    except:
        return Path.cwd()

@dataclass
class Settings:
    base_dir: Path = _default_base_dir()
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
        # 把相对路径统一挂到 base_dir 下，避免你不在仓库根目录运行就崩
        def join_if_rel(p: Path) -> Path:
            return p if p.is_absolute() else (self.base_dir / p)

        self.posts_dir = join_if_rel(self.posts_dir)
        self.config_path = join_if_rel(self.config_path)
        self.profile_config_path = join_if_rel(self.profile_config_path)
        self.ad_config_path = join_if_rel(self.ad_config_path)
        self.wallpaper_config_path = join_if_rel(self.wallpaper_config_path)
        self.public_img_dir = join_if_rel(self.public_img_dir)
        self.wallpaper_dir = join_if_rel(self.wallpaper_dir)

        if self.categories is None:
            self.categories = ["秘籍", "刷题", "学习", "知识点"]


S = Settings()
IS_WIN = os.name == "nt"

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}

# ==================== 🧱 基础工具 ====================

def clear_screen():
    os.system("cls" if IS_WIN else "clear")

def ensure_dir(p: Path) -> bool:
    try:
        p.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")

def write_text_if_changed(p: Path, content: str):
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

        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        meta[k] = v

    return meta, body, True

def truthy(v: str) -> bool:
    return str(v).strip().lower() in {"1", "true", "yes", "y", "on"}

def normalize_tags(tags: str, category: str) -> str:
    t = (tags or "").strip()
    if not t:
        return f"[{category}]"
    if t.startswith("[") and t.endswith("]"):
        return t
    return f"[{t}]"

def standardize_frontmatter(content: str, default_title: str = "") -> str:
    meta, body, _ = parse_frontmatter(content)

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
    return standardize_frontmatter("\n".join(temp), meta.get("title", ""))

# ==================== 🧹 配置修复 ====================

def auto_fix_corrupted_config():
    if not S.config_path.exists():
        return
    try:
        c = read_text(S.config_path)
        if re.search(r"themeColor:\s*\{\s*[a-zA-Z]\s*,", c):
            c2 = re.sub(r"(themeColor:\s*\{\s*)[a-zA-Z]\s*,", r"\1hue: 250,", c)
            write_text_if_changed(S.config_path, c2)
    except:
        pass

# ==================== 📚 文章扫描 ====================

DEFAULT_CATEGORY = "刷题"

def normalize_category(category: str) -> str:
    cat = (category or "").strip()
    return cat or DEFAULT_CATEGORY

def get_post_rel_path(p: Path) -> str:
    try:
        return p.relative_to(S.posts_dir).as_posix()
    except Exception:
        return p.name

def get_category_dir(category: str) -> Path:
    return S.posts_dir / normalize_category(category)

def ensure_unique_post_path(target: Path) -> Path:
    if not target.exists():
        return target
    stamp = now_stamp()
    candidate = target.with_name(f"{target.stem}_{stamp}{target.suffix}")
    i = 1
    while candidate.exists():
        candidate = target.with_name(f"{target.stem}_{stamp}_{i}{target.suffix}")
        i += 1
    return candidate

def relocate_post_by_category(post_path: Path, category: str) -> Path:
    dst_dir = get_category_dir(category)
    ensure_dir(dst_dir)
    if post_path.parent == dst_dir:
        return post_path
    dst = dst_dir / post_path.name
    if dst.exists():
        dst = ensure_unique_post_path(dst)
    shutil.move(str(post_path), str(dst))
    return dst

def get_all_posts():
    posts = []
    if S.posts_dir.exists():
        for p in S.posts_dir.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".md", ".mdx"}:
                posts.append({"name": p.name, "path": p, "rel": get_post_rel_path(p)})
    posts.sort(key=lambda x: x["rel"].lower())
    return posts

def get_post_title_from_file(p: Path) -> str:
    try:
        meta, _, has_fm = parse_frontmatter(read_text(p))
        if has_fm and meta.get("title"):
            return meta["title"]
    except:
        pass
    return p.stem

# ==================== 🏷️ 分类自动读取（你要的核心） ====================

CATEGORY_COUNTS = {}

def refresh_categories():
    global CATEGORY_COUNTS
    counts = {}

    posts = get_all_posts()
    for p in posts:
        try:
            meta, _, has_fm = parse_frontmatter(read_text(p["path"]))
            cat = (meta.get("category") or "").strip() if has_fm else ""
            cat = normalize_category(cat)
            counts[cat] = counts.get(cat, 0) + 1
        except:
            counts[DEFAULT_CATEGORY] = counts.get(DEFAULT_CATEGORY, 0) + 1

    CATEGORY_COUNTS = dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
    S.categories = list(CATEGORY_COUNTS.keys()) if CATEGORY_COUNTS else [DEFAULT_CATEGORY]

# ==================== 📦 备份模块 ====================

def run_backup():
    if not ensure_dir(S.backup_dir):
        print(f"⚠️ 无法创建备份目录：{S.backup_dir}（已跳过备份，不影响继续）")
        return

    print(f"\n=== 📦 正在备份到 {S.backup_dir} ... ===")

    temp_dir = S.backup_dir / "temp_pack"
    zip_base = S.backup_dir / f"Blog_Backup_{now_stamp()}"

    def ignore_patterns(_dirpath, names):
        ignores = {"node_modules", ".git", ".astro", "dist", "build", ".next", ".DS_Store"}
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

# ==================== 📌 置顶管理 ====================

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
                print(f"{i+1:<4} | {is_p:<6} | {title} ({p['rel']})")
            except:
                print(f"{i+1:<4} | {'[?]':<6} | {p['rel']}")

        c = input("\n👉 输入序号切换 (0返回): ").strip()
        if c == "0" or not c:
            break
        idx = safe_int(c, -1) - 1
        if 0 <= idx < len(posts):
            p_path = posts[idx]["path"]
            content = read_text(p_path)

            meta, body, _ = parse_frontmatter(content)
            cur = truthy(meta.get("pinned", "false"))
            meta["pinned"] = "true" if not cur else "false"

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
        return copy_image_to_public(Path(src))
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
        print(f"{i+1}. {get_post_title_from_file(p['path'])} ({p['rel']})")

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

# ==================== 🚚 搬运图片（独立按键） ====================

def migrate_images_in_posts():
    r"""
    仅搬运 Markdown 图片语法里的 Windows 绝对路径图片：
    ![](C:\xxx\1.png) -> ![](/images/1.png)
    并复制到 public/images
    """
    ensure_dir(S.public_img_dir)
    posts = get_all_posts()
    if not posts:
        print("❌ 没找到文章。")
        return

    total_hits, total_copied = 0, 0
    print("\n🚚 正在搬运图片...")

    for p in posts:
        path = p["path"]
        content = read_text(path)
        changed = False

        local_imgs = re.findall(
            r"(!\[.*?\]\()([a-zA-Z]:[\\/].*?\.(?:png|jpg|jpeg|webp|gif|svg))(\))",
            content,
            flags=re.IGNORECASE,
        )
        if not local_imgs:
            continue

        for _, lp, _ in local_imgs:
            total_hits += 1
            clp = Path(lp.strip().strip('"\''))
            if clp.exists():
                new_url = copy_image_to_public(clp)
                if new_url:
                    content = content.replace(lp, new_url)
                    changed = True
                    total_copied += 1

        if changed:
            write_text_if_changed(path, content)

    print(f"✅ 搬运完成：匹配到 {total_hits} 处，本次成功搬运 {total_copied} 张。")

# ==================== 🧾 版权（只在没有时追加一次） ====================

COPY_RE = re.compile(r"(?mi)^\s*-\s*\*\*版权声明\*\*\s*[:：].*$")

def has_copyright(content: str) -> bool:
    if COPY_RE.search(content):
        return True
    if "本文由 **余林阳** 创作" in content:
        return True
    return False

def ensure_copyright_once(content: str) -> str:
    if has_copyright(content):
        return content if content.endswith("\n") else content + "\n"
    tail = content.rstrip()
    return tail + f"\n\n---\n\n{S.copyright_line}\n"

# ==================== 📝 文章管理逻辑 ====================

def process_posts(mode="format"):
    ensure_dir(S.posts_dir)
    ensure_dir(S.public_img_dir)

    if mode == "new":
        refresh_categories()  # ✅ 新建前刷新分类统计

        t = input("\n👉 文章标题: ").strip()
        if not t:
            return
        desc = input(f"👉 描述 (默认 {t}): ").strip() or t

        print("\n--- 选择分类（自动统计） ---")
        for i, cat in enumerate(S.categories):
            cnt = CATEGORY_COUNTS.get(cat, 0)
            print(f"  {i+1}. {cat} ({cnt})")
        print("  0. ➕ 新建分类")
        cat_c = input("👉 选择: ").strip()

        if cat_c == "0":
            category = input("👉 新分类名: ").strip() or DEFAULT_CATEGORY
            if category not in S.categories:
                S.categories.append(category)
        else:
            idx = safe_int(cat_c, 1) - 1
            category = S.categories[idx] if 0 <= idx < len(S.categories) else DEFAULT_CATEGORY
        category = normalize_category(category)

        pinned = "true" if input("👉 是否置顶? (y/n): ").strip().lower() == "y" else "false"

        img = ""
        if input("👉 是否设置封面? (y/n): ").strip().lower() == "y":
            img = pick_image_ui()

        safe_name = re.sub(r'[\\/:*?"<>|]', "_", t).strip()
        post_dir = get_category_dir(category)
        ensure_dir(post_dir)
        p = ensure_unique_post_path(post_dir / f"{safe_name}.md")

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
        final = ensure_copyright_once(final)  # ✅ 只加一次
        write_text_if_changed(p, final)
        print(f"✅ 《{t}》创建成功：{get_post_rel_path(p)}")
        return

    # ========== 全站格式对齐（不搬运图片！不重复加版权！） ==========
    print("\n🔍 正在全站格式对齐...")
    posts = get_all_posts()
    for p in posts:
        content = read_text(p["path"])
        content = standardize_frontmatter(content, get_post_title_from_file(p["path"]))
        content = ensure_copyright_once(content)  # ✅ 没有才加
        write_text_if_changed(p["path"], content)
        meta, _, has_fm = parse_frontmatter(content)
        category = normalize_category(meta.get("category", "") if has_fm else "")
        relocate_post_by_category(p["path"], category)
    print("✅ 全站格式对齐完成。")
    refresh_categories()

# ==================== 🗑️ 删除文章 ====================

def delete_post():
    posts = get_all_posts()
    if not posts:
        print("❌ 没找到文章。")
        return

    clear_screen()
    print("\n=== 🗑️ 删除文章 ===")
    for i, p in enumerate(posts):
        print(f"{i+1}. {get_post_title_from_file(p['path'])} ({p['rel']})")
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
    refresh_categories()

# ==================== 🌅 换壁纸中心 ====================

def wallpaper_center():
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
            import random

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

            pick_str = str(pick).replace("\\", "/")
            if "/public/assets/" in pick_str:
                url = pick_str.split("/public", 1)[1]
            elif "/public/" in pick_str:
                url = pick_str.split("/public", 1)[1]
            else:
                url = copy_image_to_public(pick)

            if not url.startswith("/"):
                url = "/" + url

            c2 = re.sub(r'(image:\s*)["\'].*?["\']', rf'\1"{url}"', c, count=1)
            if c2 == c:
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

# ==================== 🚀 本地预览 ====================

def run_dev():
    try:
        webbrowser.open("http://localhost:4321")
    except:
        pass

    try:
        if IS_WIN:
            # 在新窗口里先 cd 到仓库根目录再启动 pnpm
            cmd = f'start "pnpm dev" cmd /k "cd /d {str(S.base_dir)} && pnpm dev"'
            os.system(cmd)
        else:
            subprocess.Popen(["pnpm", "dev"], cwd=str(S.base_dir))
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        time.sleep(1.2)

# ==================== ☁️ 发布（修复：无改动但 ahead 也会 push；push 不 capture） ====================

def run_cmd_capture(cmd, cwd=None):
    # Always capture raw bytes and decode ourselves.
    # This avoids Python's locale-dependent text decoding (e.g. GBK) from throwing
    # UnicodeDecodeError in subprocess reader threads on Windows.
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    r = subprocess.run(
        cmd,
        check=False,
        capture_output=True,
        text=False,
        cwd=cwd or str(S.base_dir),
        env=env,
    )

    stdout = r.stdout.decode("utf-8", errors="replace") if isinstance(r.stdout, (bytes, bytearray)) else str(r.stdout or "")
    stderr = r.stderr.decode("utf-8", errors="replace") if isinstance(r.stderr, (bytes, bytearray)) else str(r.stderr or "")
    return subprocess.CompletedProcess(r.args, r.returncode, stdout, stderr)

def has_git_changes() -> bool:
    try:
        r = run_cmd_capture(["git", "status", "--porcelain"])
        return bool(r.stdout.strip())
    except:
        return True

def git_ahead_count() -> int:
    """
    返回 HEAD 比上游 @{u} 多多少个 commit
    """
    try:
        r = run_cmd_capture(["git", "rev-list", "--count", "@{u}..HEAD"])
        if r.returncode != 0:
            return 0
        return safe_int(r.stdout.strip(), 0)
    except:
        return 0

def git_push_main_interactive() -> int:
    env = os.environ.copy()
    env.pop("GIT_ASKPASS", None)
    env.pop("SSH_ASKPASS", None)
    env["GIT_TERMINAL_PROMPT"] = "1"
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    # 不 capture_output，让 git 走正常凭据弹窗/输入
    r = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=str(S.base_dir),
        env=env,
        check=False,
    )
    return r.returncode

def run_deploy():
    run_backup()

    changed = has_git_changes()
    ahead = git_ahead_count()

    if not changed and ahead <= 0:
        print("✅ 没有检测到改动，且没有待推送的提交。")
        return

    if changed:
        r = run_cmd_capture(["git", "add", "."])
        if r.returncode != 0:
            print("❌ git add 失败：", (r.stderr.strip() or r.stdout.strip()))
            return

        msg = f"update blog content {now_stamp()}"
        r = run_cmd_capture(["git", "commit", "-m", msg])
        if r.returncode != 0:
            out = (r.stderr.strip() or r.stdout.strip())
            print("⚠️ git commit 提示：", out)
            # 不直接 return，仍可能需要 push（比如已有提交）

    # push（允许交互）
    code = git_push_main_interactive()
    if code != 0:
        print("❌ git push 失败：请在仓库目录手动执行一次 `git push origin main` 完成授权后再试。")
        return

    print("✅ 发布成功。")

# ==================== 🧹 GitHub Actions 清理（删除记录/日志/Artifacts） ====================

def get_origin_owner_repo():
    """
    从 `git remote get-url origin` 解析 owner/repo
    支持：
      https://github.com/owner/repo.git
      git@github.com:owner/repo.git
    """
    r = run_cmd_capture(["git", "remote", "get-url", "origin"])
    if r.returncode != 0:
        return None, None
    url = (r.stdout.strip() or "").strip()

    m = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)", url)
    if not m:
        return None, None
    return m.group("owner"), m.group("repo")

def get_github_token() -> str:
    """
    优先读环境变量：GITHUB_TOKEN / GH_TOKEN
    否则安全输入（不回显）
    """
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok and tok.strip():
        return tok.strip()
    print("\n⚠️ 需要 GitHub Token 才能操作 Actions 记录（建议设置环境变量 GITHUB_TOKEN）。")
    return getpass.getpass("👉 请输入 Token（不会回显）：").strip()

def gh_request(method: str, path: str, token: str, params: dict | None = None):
    base = "https://api.github.com"
    url = base + path
    if params:
        url += "?" + urlencode(params)

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "blog-tool",
    }

    req = Request(url, headers=headers, method=method.upper())
    try:
        with urlopen(req, timeout=20) as resp:
            data = resp.read()
            if not data:
                return resp.status, None
            try:
                return resp.status, json.loads(data.decode("utf-8"))
            except:
                return resp.status, data.decode("utf-8", errors="ignore")
    except HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="ignore")
        except:
            body = ""
        return e.code, body
    except URLError as e:
        return 0, f"Network error: {e}"

def iso_to_dt(s: str):
    # GitHub 返回 "2026-03-04T12:34:56Z"
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except:
        return None

def list_workflow_runs(owner: str, repo: str, token: str, per_page=30, page=1):
    path = f"/repos/{owner}/{repo}/actions/runs"
    status, data = gh_request("GET", path, token, params={"per_page": per_page, "page": page})
    return status, data

def delete_workflow_run(owner: str, repo: str, token: str, run_id: int):
    path = f"/repos/{owner}/{repo}/actions/runs/{run_id}"
    return gh_request("DELETE", path, token)

def delete_workflow_run_logs(owner: str, repo: str, token: str, run_id: int):
    path = f"/repos/{owner}/{repo}/actions/runs/{run_id}/logs"
    return gh_request("DELETE", path, token)

def list_artifacts(owner: str, repo: str, token: str, per_page=30, page=1):
    path = f"/repos/{owner}/{repo}/actions/artifacts"
    status, data = gh_request("GET", path, token, params={"per_page": per_page, "page": page})
    return status, data

def delete_artifact(owner: str, repo: str, token: str, artifact_id: int):
    path = f"/repos/{owner}/{repo}/actions/artifacts/{artifact_id}"
    return gh_request("DELETE", path, token)

def confirm_dangerous(op_name: str) -> bool:
    print(f"\n⚠️ 危险操作：{op_name}（不可恢复）")
    w = input("输入 DELETE 确认继续，否则取消：").strip()
    return w == "DELETE"

def actions_cleanup_center():
    owner, repo = get_origin_owner_repo()
    if not owner or not repo:
        print("❌ 无法从 git remote origin 解析 owner/repo。请确保在仓库目录运行且已配置 origin。")
        time.sleep(1.5)
        return

    token = get_github_token()
    if not token:
        print("❌ 没有 token，已取消。")
        time.sleep(1.2)
        return

    while True:
        clear_screen()
        print("\n=== 🧹 Actions 清理中心 ===")
        print(f"Repo: {owner}/{repo}")
        print("1. 列出最近 Workflow Runs（记录）")
        print("2. 删除指定 Run（按 run_id）")
        print("3. 批量删除早于 N 天的 Runs")
        print("4. 仅删除指定 Run 的 Logs（不删 Run 记录）")
        print("5. 列出 Artifacts")
        print("6. 批量删除早于 N 天的 Artifacts")
        print("0. 返回")

        op = input("👉 选择: ").strip()
        if op == "0":
            return

        if op == "1":
            n = safe_int(input("显示多少条（建议 20/50）: ").strip(), 20)
            per_page = min(max(n, 1), 100)
            st, data = list_workflow_runs(owner, repo, token, per_page=per_page, page=1)
            if st != 200 or not isinstance(data, dict):
                print(f"❌ 拉取失败：HTTP {st}\n{data}")
                input("回车继续...")
                continue

            runs = data.get("workflow_runs", [])[:n]
            print("\nID | created | name | status | conclusion")
            print("-" * 90)
            for r in runs:
                rid = r.get("id")
                created = r.get("created_at", "")
                name = (r.get("name") or r.get("display_title") or "")[:30]
                status = r.get("status", "")
                concl = r.get("conclusion", "")
                print(f"{rid} | {created} | {name} | {status} | {concl}")
            input("\n回车继续...")

        elif op == "2":
            run_id = safe_int(input("输入要删除的 run_id: ").strip(), 0)
            if run_id <= 0:
                continue
            if not confirm_dangerous(f"删除 Workflow Run: {run_id}"):
                continue
            st, data = delete_workflow_run(owner, repo, token, run_id)
            if st == 204:
                print("✅ 删除成功。")
            else:
                print(f"❌ 删除失败：HTTP {st}\n{data}")
            input("回车继续...")

        elif op == "3":
            days = safe_int(input("删除早于多少天（例如 30）: ").strip(), 30)
            cutoff = datetime.now(timezone.utc) - timedelta(days=days)

            if not confirm_dangerous(f"批量删除早于 {days} 天的 Runs"):
                continue

            deleted = 0
            page = 1
            while True:
                st, data = list_workflow_runs(owner, repo, token, per_page=100, page=page)
                if st != 200 or not isinstance(data, dict):
                    print(f"\n❌ 拉取失败：HTTP {st}\n{data}")
                    break

                runs = data.get("workflow_runs", [])
                if not runs:
                    break

                for r in runs:
                    rid = r.get("id")
                    dt = iso_to_dt(r.get("created_at", "") or "")
                    if dt and dt < cutoff:
                        st2, d2 = delete_workflow_run(owner, repo, token, int(rid))
                        if st2 == 204:
                            deleted += 1
                            print(f"🗑️ 删除 run {rid} OK")
                        else:
                            print(f"❌ 删除 run {rid} 失败：HTTP {st2} {d2}")

                page += 1

            print(f"\n✅ 批量删除完成：共删除 {deleted} 条。")
            input("回车继续...")

        elif op == "4":
            run_id = safe_int(input("输入要删 logs 的 run_id: ").strip(), 0)
            if run_id <= 0:
                continue
            if not confirm_dangerous(f"仅删除 Run Logs: {run_id}"):
                continue
            st, data = delete_workflow_run_logs(owner, repo, token, run_id)
            if st == 204:
                print("✅ Logs 删除成功。")
            else:
                print(f"❌ 删除失败：HTTP {st}\n{data}")
            input("回车继续...")

        elif op == "5":
            n = safe_int(input("显示多少条（建议 20/50）: ").strip(), 20)
            per_page = min(max(n, 1), 100)
            st, data = list_artifacts(owner, repo, token, per_page=per_page, page=1)
            if st != 200 or not isinstance(data, dict):
                print(f"❌ 拉取失败：HTTP {st}\n{data}")
                input("回车继续...")
                continue

            arts = data.get("artifacts", [])[:n]
            print("\nID | created | name | expired | size(bytes)")
            print("-" * 90)
            for a in arts:
                aid = a.get("id")
                created = a.get("created_at", "")
                name = (a.get("name") or "")[:30]
                expired = a.get("expired", "")
                sizeb = a.get("size_in_bytes", "")
                print(f"{aid} | {created} | {name} | {expired} | {sizeb}")
            input("\n回车继续...")

        elif op == "6":
            days = safe_int(input("删除早于多少天（例如 30）: ").strip(), 30)
            cutoff = datetime.now(timezone.utc) - timedelta(days=days)

            if not confirm_dangerous(f"批量删除早于 {days} 天的 Artifacts"):
                continue

            deleted = 0
            page = 1
            while True:
                st, data = list_artifacts(owner, repo, token, per_page=100, page=page)
                if st != 200 or not isinstance(data, dict):
                    print(f"\n❌ 拉取失败：HTTP {st}\n{data}")
                    break

                arts = data.get("artifacts", [])
                if not arts:
                    break

                for a in arts:
                    aid = a.get("id")
                    dt = iso_to_dt(a.get("created_at", "") or "")
                    if dt and dt < cutoff:
                        st2, d2 = delete_artifact(owner, repo, token, int(aid))
                        if st2 == 204:
                            deleted += 1
                            print(f"🗑️ 删除 artifact {aid} OK")
                        else:
                            print(f"❌ 删除 artifact {aid} 失败：HTTP {st2} {d2}")

                page += 1

            print(f"\n✅ 批量删除完成：共删除 {deleted} 个 artifacts。")
            input("回车继续...")

        else:
            pass

# ==================== 🧭 主菜单 ====================

def main():
    auto_fix_corrupted_config()
    ensure_dir(S.posts_dir)
    ensure_dir(S.public_img_dir)
    refresh_categories()

    while True:
        clear_screen()
        print("\n" + "=" * 45 + "\n       YU's 博客助手 v13.1\n" + "=" * 45)
        print("  1. 📝 新建文章       5. 🗑️ 删除文章")
        print("  2. 🧹 全站格式对齐    6. 🚀 本地预览")
        print("  3. ⚙️  设置中心       7. ☁️ 发布博客")
        print("  4. 🌅 换壁纸中心      8. 📦 手动备份")
        print("  9. 🖼️ 设置文章封面    10. 📌 置顶管理")
        print("  11. 🚚 搬运文章图片   12. 🧹 Actions 记录清理")
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
        elif c == "11":
            migrate_images_in_posts()
            input("回车继续...")
        elif c == "12":
            actions_cleanup_center()
        else:
            pass


if __name__ == "__main__":
    main()

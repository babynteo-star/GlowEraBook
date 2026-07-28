"""
Create and publish a new Glow Era blog post in one step.

Usage:
  python new_blog_post.py "Post Title" "Excerpt" "Category Label" "category-id" body.txt
  python new_blog_post.py "Post Title" "Excerpt" "Category Label" "category-id" body.txt --image images/foo.jpg --tags "tag1,tag2,tag3" --no-push

category-id must be one of the ids in blog/categories-data.js (radical-self-care,
deep-self-love, healing-boundaries, confidence-glow).

Body file format (plain text, see content_render.py):
  - Blank line = new paragraph
  - "## " = <h2>, "### " = <h3>, "> " = blockquote
  - "- " consecutive = <ul>, "1. " consecutive = <ol>
  - **bold**, [text](url)
"""
import sys
import subprocess
from pathlib import Path
from datetime import datetime

from content_render import render_body, slugify

ROOT = Path(__file__).parent
BLOG_DIR = ROOT / "blog"
POSTS_DATA = BLOG_DIR / "posts-data.js"
SITEMAP = ROOT / "sitemap.xml"
SITE_URL = "https://glowerabook.com"


def js_esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def html_esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def read_time(text):
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}, Glow Era Blog | Prudence Nteo</title>
<meta name="description" content="{excerpt}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Playfair+Display:wght@500;600;700;800&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
</head>
<body>

<div class="grain-overlay"></div>

<header class="site-header" id="siteHeader">
  <div class="container header-inner">
    <a href="/" class="logo">Glow&nbsp;Era</a>
    <nav class="main-nav">
      <a href="/#about-book">The Book</a>
      <a href="/#who">Who It's For</a>
      <a href="/#author">Author</a>
      <a href="/blog/">Blog</a>
      <a href="/#contact">Contact</a>
    </nav>
    <a href="https://www.amazon.com/dp/B0GZKK3TYL/" class="btn btn-small btn-outline" target="_blank" rel="noopener">Buy the Book</a>
  </div>
</header>

<main>
  <section class="article-hero">
    <div class="container">
      <!-- breadcrumb -->
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
        <a href="/blog/">Blog</a> <span aria-hidden="true">&rsaquo;</span>
        <a href="/category/{category_id}/">{category}</a> <span aria-hidden="true">&rsaquo;</span>
        <span aria-current="page">{title}</span>
      </nav>
      <a href="/blog/" class="article-back">&larr; Back to the Blog</a>
      <div class="article-meta"><a href="/category/{category_id}/" class="article-meta-category">{category}</a><span>&middot;</span><span>{date_display}</span><span>&middot;</span><span>{read_time}</span></div>
      <h1>{title}</h1>
{hero_img_html}
    </div>
  </section>

  <section class="article-body">
    <div class="container">
{body_html}

      <div class="article-cta">
        <h3>Ready to start your glow era?</h3>
        <p>Grab your copy of Glow Era by Prudence Nteo and begin your own journey back to yourself.</p>
        <a href="https://www.amazon.com/dp/B0GZKK3TYL/" class="btn btn-primary" target="_blank" rel="noopener">Read the Book</a>
      </div>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="container footer-inner">
    <span class="logo footer-logo">Glow&nbsp;Era</span>
    <p>&copy; <span id="year"></span> Glow Era by Prudence Nteo. All rights reserved.</p>
  </div>
</footer>

<script src="../script.js"></script>
</body>
</html>
"""


def insert_post_entry(slug, title, excerpt, category, category_id, date_iso, rtime, image, tags):
    content = POSTS_DATA.read_text(encoding="utf-8")
    entry_lines = [
        "  {",
        f'    slug: "{js_esc(slug)}",',
        f'    categoryId: "{js_esc(category_id)}",',
        f'    title: "{js_esc(title)}",',
        f'    excerpt: "{js_esc(excerpt)}",',
        f'    date: "{date_iso}",',
        f'    readTime: "{rtime}",',
        f'    category: "{js_esc(category)}",',
    ]
    if image:
        entry_lines.append(f'    image: "{js_esc(image)}",')
    if tags:
        tag_list = ", ".join(f'"{js_esc(t.strip())}"' for t in tags.split(",") if t.strip())
        entry_lines.append(f"    tags: [{tag_list}],")
    # drop trailing comma on last field, close object
    entry_lines[-1] = entry_lines[-1].rstrip(",")
    entry_lines.append("  },")
    entry = "\n".join(entry_lines) + "\n"

    marker = "const BLOG_POSTS = [\n"
    idx = content.index(marker) + len(marker)
    new_content = content[:idx] + entry + content[idx:]
    POSTS_DATA.write_text(new_content, encoding="utf-8")


def rebuild_sitemap():
    urls = [f"{SITE_URL}/", f"{SITE_URL}/blog/"]
    for f in sorted(BLOG_DIR.glob("*.html")):
        if f.name == "index.html":
            continue
        urls.append(f"{SITE_URL}/blog/{f.name}")
    cat_dir = ROOT / "category"
    if cat_dir.exists():
        for f in sorted(cat_dir.glob("*/index.html")):
            urls.append(f"{SITE_URL}/category/{f.parent.name}/")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url><loc>{u}</loc></url>")
    lines.append("</urlset>")
    SITEMAP.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    raw_args = sys.argv[1:]
    no_push = "--no-push" in raw_args
    image = ""
    tags = ""
    if "--image" in raw_args:
        image = raw_args[raw_args.index("--image") + 1]
    if "--tags" in raw_args:
        tags = raw_args[raw_args.index("--tags") + 1]

    positional = []
    skip_next = False
    for a in raw_args:
        if skip_next:
            skip_next = False
            continue
        if a in ("--image", "--tags"):
            skip_next = True
            continue
        if a.startswith("--"):
            continue
        positional.append(a)

    if len(positional) < 5:
        print(__doc__)
        sys.exit(1)

    title, excerpt, category, category_id, body_path = positional[:5]
    body_text = Path(body_path).read_text(encoding="utf-8")

    slug = slugify(title)
    date_iso = datetime.now().strftime("%Y-%m-%d")
    date_display = datetime.now().strftime("%B %-d, %Y") if sys.platform != "win32" else datetime.now().strftime("%B %#d, %Y")
    rtime = read_time(body_text)
    body_html = render_body(body_text)
    hero_img_html = f'      <img src="{image.replace("blog/", "")}" alt="{title}" class="article-hero-img">' if image else ""

    out_path = BLOG_DIR / f"{slug}.html"
    html = ARTICLE_TEMPLATE.format(
        title=html_esc(title), excerpt=html_esc(excerpt), category=html_esc(category), category_id=category_id,
        date_display=date_display, read_time=rtime, body_html=body_html,
        hero_img_html=hero_img_html,
    )
    out_path.write_text(html, encoding="utf-8")

    insert_post_entry(slug, title, excerpt, category, category_id, date_iso, rtime, image, tags)
    rebuild_sitemap()

    # SEO + internal-linking enrichment (canonical/OG/JSON-LD, author box, related posts)
    subprocess.run([sys.executable, str(ROOT / "enrich_blog_seo.py")], cwd=ROOT, check=True)

    print(f"Created blog/{slug}.html")
    print(f"Updated blog/posts-data.js and sitemap.xml")

    if not no_push:
        subprocess.run(["git", "add", "-A"], cwd=ROOT, check=True)
        subprocess.run(["git", "commit", "-m", f"Add blog post: {title}"], cwd=ROOT, check=True)
        subprocess.run(["git", "push"], cwd=ROOT, check=True)
        print(f"Pushed. Live at {SITE_URL}/blog/{slug}.html (may take ~1 min to build)")
    else:
        print("Skipped git push (--no-push). Run 'git add -A && git commit -m ... && git push' when ready.")


if __name__ == "__main__":
    main()

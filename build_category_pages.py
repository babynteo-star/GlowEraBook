"""
Generate the four Glow Era category landing pages (category/<slug>/index.html)
from blog/categories-data.js + blog/posts-data.js.

Idempotent: safe to re-run any time new posts are added (rerun after every
new_blog_post.py call, or just at the end of a batch).

Usage: python build_category_pages.py
"""
import re
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
BLOG_DIR = ROOT / "blog"
CATEGORY_DIR = ROOT / "category"
SITE_URL = "https://glowerabook.com"
AUTHOR = "Prudence Nteo"

# The one legacy article that lives outside blog/ (root-level, predates the
# blog/ collection) but is tagged Deep Self-Love on the homepage. Injected
# manually since it isn't in posts-data.js.
ROOT_EXTRA_POSTS = [
    {
        "slug": "7-ways-to-rebuild-a-relationship-with-yourself",
        "categoryId": "deep-self-love",
        "title": "7 Ways to Rebuild a Relationship with Yourself",
        "excerpt": "Life gets busy and we drift away from ourselves. Here are 7 cozy, gentle ways to come home to the wonderful person you are.",
        "date": "2026-07-18",
        "readTime": "4 min read",
        "category": "Deep Self-Love",
        "image": "rebuild.jpeg",
        "url": f"{SITE_URL}/7-ways-to-rebuild-a-relationship-with-yourself.html",
        "imgBase": "/images/",
    }
]


def esc(s):
    return (s or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def load_js_objects(path, extra_string_fields, extra_raw_fields=None):
    txt = path.read_text(encoding="utf-8")
    items = []
    depth = 0
    start = None
    for i, ch in enumerate(txt):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                items.append(txt[start:i + 1])
                start = None
    objs = []
    for block in items:
        def g(key):
            m = re.search(rf'{key}:\s*"((?:[^"\\]|\\.)*)"', block)
            return m.group(1) if m else ""
        obj = {f: g(f) for f in extra_string_fields}
        objs.append(obj)
    return objs


def load_categories():
    raw = load_js_objects(
        BLOG_DIR / "categories-data.js",
        ["id", "name", "slug", "icon", "featuredArticleId", "description"],
    )
    # displayOrder is numeric, parse separately
    txt = (BLOG_DIR / "categories-data.js").read_text(encoding="utf-8")
    blocks = re.findall(r"\{[^{}]*\}", txt, re.S)
    for obj, block in zip(raw, blocks):
        m = re.search(r"displayOrder:\s*(\d+)", block)
        obj["displayOrder"] = int(m.group(1)) if m else 0
    raw.sort(key=lambda c: c["displayOrder"])
    return raw


def load_posts():
    posts = load_js_objects(
        BLOG_DIR / "posts-data.js",
        ["slug", "categoryId", "title", "excerpt", "date", "readTime", "category", "image"],
    )
    posts = [p for p in posts if p["slug"]]
    for p in posts:
        p["url"] = f"{SITE_URL}/blog/{p['slug']}.html"
        p["imgBase"] = "/blog/"
    return posts + ROOT_EXTRA_POSTS


def fmt_date(iso):
    try:
        return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %d, %Y").replace(" 0", " ")
    except ValueError:
        return iso


def media_html(p, cls="blog-card-media"):
    if p.get("image"):
        img = p["image"] if p["image"].startswith("images/") else f"images/{p['image']}"
        src = f"{p['imgBase']}{img}" if not p["image"].startswith("http") else p["image"]
        # image field for blog posts already includes "images/..."; for root extra it's bare filename
        if p is ROOT_EXTRA_POSTS[0] if False else False:
            pass
        return f'<div class="{cls}"><img src="{src}" alt="{esc(p["title"])}" loading="lazy"></div>'
    return f'<div class="{cls}"><span>Glow Era</span></div>'


def fix_image_src(p):
    """Return an absolute-from-root image src for a post (blog/ posts vs the one root post)."""
    if not p.get("image"):
        return None
    img = p["image"]
    if p["imgBase"] == "/blog/":
        return f"/blog/{img}" if not img.startswith("images/") else f"/blog/{img}"
    return f"/images/{img}"


def card_html(p):
    src = fix_image_src(p)
    media = f'<img src="{src}" alt="{esc(p["title"])}" loading="lazy">' if src else "<span>Glow Era</span>"
    return (
        f'        <a class="blog-card" href="{p["url"]}">\n'
        f'          <div class="blog-card-media">{media}</div>\n'
        f'          <div class="blog-card-body">\n'
        f'            <div class="blog-card-meta"><span>{fmt_date(p["date"])}</span><span class="dot">&middot;</span><span>{p["readTime"]}</span></div>\n'
        f'            <h3>{esc(p["title"])}</h3>\n'
        f'            <p>{esc(p["excerpt"])}</p>\n'
        f'            <span class="blog-card-link">Read Article</span>\n'
        f'          </div>\n'
        f'        </a>'
    )


def featured_html(p):
    src = fix_image_src(p)
    media = f'<img src="{src}" alt="{esc(p["title"])}" loading="lazy">' if src else "<span>Glow Era</span>"
    return f"""      <div class="featured-card">
        <div class="featured-card-media">{media}</div>
        <div class="featured-card-body">
          <span class="category-featured-label">Featured Article</span>
          <div class="featured-card-meta"><span>{fmt_date(p["date"])}</span><span>&middot;</span><span>{p["readTime"]}</span></div>
          <h2>{esc(p["title"])}</h2>
          <p>{esc(p["excerpt"])}</p>
          <a href="{p["url"]}" class="btn btn-primary">Read Article</a>
        </div>
      </div>"""


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{seo_title}</title>
<meta name="description" content="{seo_description}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Playfair+Display:wght@500;600;700;800&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../style.css">
<meta property="og:type" content="website">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{seo_description}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Glow Era">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{seo_description}">
<script type="application/ld+json">{breadcrumb_ld}</script>
<script type="application/ld+json">{collection_ld}</script>
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
  <section class="category-hero">
    <div class="container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>
        <a href="/blog/">Blog</a> <span aria-hidden="true">&rsaquo;</span>
        <span aria-current="page">{name}</span>
      </nav>
      <div class="cat-icon">{icon}</div>
      <p class="eyebrow center">Glow Era Journal</p>
      <h1>{name}</h1>
      <p>{description}</p>
      <p class="category-count">{count_label}</p>
    </div>
  </section>

{featured_section}

  <section class="category-list">
    <div class="container">
      <h2>{grid_heading}</h2>
      <div class="blog-grid">
{grid_cards}
      </div>
{empty_state}
    </div>
  </section>

  <section class="related-categories">
    <div class="container">
      <h2>Explore More of Glow Era</h2>
      <div class="related-categories-grid">
{related_cards}
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="container cta-inner">
      <p class="eyebrow center light">Ready When You Are</p>
      <h2>Start Your Glow Era Today</h2>
      <p class="cta-sub">Your softest, most confident chapter is waiting. Grab your copy of Glow Era and begin.</p>
      <div class="hero-actions center">
        <a href="https://www.amazon.com/dp/B0GZKK3TYL/" class="btn btn-primary btn-light" target="_blank" rel="noopener">Read the Book</a>
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

<script src="../../script.js"></script>
</body>
</html>
"""


def build_category(cat, posts):
    cat_posts = [p for p in posts if p["categoryId"] == cat["id"]]
    cat_posts.sort(key=lambda p: p["date"], reverse=True)

    featured = None
    if cat.get("featuredArticleId"):
        featured = next((p for p in cat_posts if p["slug"] == cat["featuredArticleId"]), None)
    if not featured and cat_posts:
        featured = cat_posts[0]

    grid_posts = [p for p in cat_posts if not featured or p["slug"] != featured["slug"]]

    canonical = f"{SITE_URL}/category/{cat['slug']}/"
    name = cat["name"]
    seo_title = f"{name} Articles, Glow Era Blog | {AUTHOR}"
    seo_description = cat["description"][:157].rsplit(" ", 1)[0] + "..." if len(cat["description"]) > 160 else cat["description"]

    if featured:
        featured_section = f"""  <section class="category-featured">
    <div class="container">
{featured_html(featured)}
    </div>
  </section>"""
    else:
        featured_section = ""

    if grid_posts:
        grid_cards = "\n".join(card_html(p) for p in grid_posts)
        empty_state = ""
        grid_heading = "More in " + name
    elif featured:
        grid_cards = ""
        empty_state = ""
        grid_heading = "More in " + name + " Coming Soon"
    else:
        grid_cards = ""
        grid_heading = name
        empty_state = f'      <div class="category-empty"><p>New {esc(name)} articles are on their way. In the meantime, explore the <a href="/blog/">full Glow Era journal</a>.</p></div>'

    count = len(cat_posts)
    count_label = f"{count} article{'s' if count != 1 else ''} in this category"

    related = [c for c in ALL_CATEGORIES if c["id"] != cat["id"]]
    related_cards = "\n".join(
        f'        <a class="related-category-card" href="/category/{r["slug"]}/" aria-label="Explore {esc(r["name"])} articles">'
        f'<h3>{esc(r["name"])}</h3><span>Explore Articles &rarr;</span></a>'
        for r in related
    )

    breadcrumb_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE_URL + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": name, "item": canonical},
        ],
    })
    collection_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": seo_title,
        "description": seo_description,
        "url": canonical,
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": p["url"]}
                for i, p in enumerate(cat_posts)
            ],
        },
    })

    html = PAGE_TEMPLATE.format(
        seo_title=esc(seo_title), seo_description=esc(seo_description), canonical=canonical,
        og_title=esc(seo_title), breadcrumb_ld=breadcrumb_ld, collection_ld=collection_ld,
        name=esc(name), icon=cat["icon"], description=esc(cat["description"]),
        count_label=count_label, featured_section=featured_section,
        grid_heading=grid_heading, grid_cards=grid_cards, empty_state=empty_state,
        related_cards=related_cards,
    )

    out_dir = CATEGORY_DIR / cat["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    return count


def main():
    global ALL_CATEGORIES
    ALL_CATEGORIES = load_categories()
    posts = load_posts()
    print(f"Loaded {len(ALL_CATEGORIES)} categories, {len(posts)} posts.")
    for cat in ALL_CATEGORIES:
        n = build_category(cat, posts)
        print(f"  category/{cat['slug']}/index.html  ({n} articles)")


if __name__ == "__main__":
    main()

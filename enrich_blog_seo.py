"""
Idempotent SEO + navigation enrichment for every Glow Era blog article.

For each blog/*.html (except index.html) it injects/refreshes:
  - canonical + robots index,follow, OG/Twitter tags, BlogPosting JSON-LD   (once)
  - breadcrumb nav + a category link in the article meta line               (once, legacy retrofit)
  - a table of contents, for articles with 3+ h2 sections                   (refreshed)
  - a visible "Written by Prudence Nteo" author box (E-E-A-T)               (once)
  - social share links (X / Facebook / Pinterest / email)                  (once)
  - previous/next article nav within the same category                    (refreshed every run)
  - a "Continue Reading" block of 3 related posts, same-category first     (refreshed every run)

Safe to run repeatedly. new_blog_post.py calls this before committing.
"""
import re
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import quote

ROOT = Path(__file__).parent
BLOG_DIR = ROOT / "blog"
POSTS_DATA = BLOG_DIR / "posts-data.js"
SITE_URL = "https://glowerabook.com"
AUTHOR = "Prudence Nteo"

HEAD_MARK = "<!-- seo-enrich -->"
BREADCRUMB_MARK = "<!-- breadcrumb -->"
TOC_MARK = "<!-- toc -->"
AUTHOR_MARK = "<!-- author-box -->"
SHARE_MARK = "<!-- share -->"
PREVNEXT_MARK = "<!-- prevnext -->"
RELATED_MARK = "<!-- related-posts -->"


def esc(s):
    return (s or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def load_posts():
    txt = POSTS_DATA.read_text(encoding="utf-8")
    posts = []
    for block in re.findall(r"\{(.*?)\}", txt, re.S):
        def g(key):
            m = re.search(rf'{key}:\s*"((?:[^"\\]|\\.)*)"', block)
            return m.group(1).replace('\\"', '"') if m else ""
        slug = g("slug")
        if not slug:
            continue
        posts.append({
            "slug": slug, "title": g("title"), "excerpt": g("excerpt"),
            "date": g("date"), "readTime": g("readTime"),
            "category": g("category"), "categoryId": g("categoryId"),
            "image": g("image"),
        })
    return posts


def fmt_date(iso):
    try:
        return datetime.strptime(iso, "%Y-%m-%d").strftime("%B %d, %Y").replace(" 0", " ")
    except ValueError:
        return iso


def head_block(p):
    url = f"{SITE_URL}/blog/{p['slug']}.html"
    title = f"{p['title']}, Glow Era Blog | {AUTHOR}"
    desc = p["excerpt"]
    img_abs = f"{SITE_URL}/blog/{p['image']}" if p["image"] else ""
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": p["title"],
        "description": desc,
        "datePublished": p["date"],
        "dateModified": p["date"],
        "articleSection": p["category"],
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "author": {"@type": "Person", "name": AUTHOR, "url": f"{SITE_URL}/#author"},
        "publisher": {"@type": "Organization", "name": "Glow Era", "url": SITE_URL},
    }
    if img_abs:
        ld["image"] = img_abs
    breadcrumb_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE_URL}/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["category"], "item": f"{SITE_URL}/category/{p['categoryId']}/"},
            {"@type": "ListItem", "position": 4, "name": p["title"], "item": url},
        ],
    }
    lines = [
        HEAD_MARK,
        f'<link rel="canonical" href="{url}">',
        '<meta name="robots" content="index, follow">',
        '<meta property="og:type" content="article">',
        f'<meta property="og:title" content="{esc(p["title"])}">',
        f'<meta property="og:description" content="{esc(desc)}">',
        f'<meta property="og:url" content="{url}">',
        '<meta property="og:site_name" content="Glow Era">',
        f'<meta property="article:published_time" content="{p["date"]}">',
        f'<meta property="article:author" content="{AUTHOR}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(p["title"])}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
    ]
    if img_abs:
        lines.insert(7, f'<meta property="og:image" content="{img_abs}">')
        lines.append(f'<meta name="twitter:image" content="{img_abs}">')
    lines.append('<script type="application/ld+json">' + json.dumps(ld) + '</script>')
    lines.append('<script type="application/ld+json">' + json.dumps(breadcrumb_ld) + '</script>')
    return "\n".join(lines) + "\n"


def breadcrumb_block(p):
    return (
        f'      {BREADCRUMB_MARK}\n'
        '      <nav class="breadcrumb" aria-label="Breadcrumb">\n'
        '        <a href="/">Home</a> <span aria-hidden="true">&rsaquo;</span>\n'
        '        <a href="/blog/">Blog</a> <span aria-hidden="true">&rsaquo;</span>\n'
        f'        <a href="/category/{p["categoryId"]}/">{esc(p["category"])}</a> <span aria-hidden="true">&rsaquo;</span>\n'
        f'        <span aria-current="page">{esc(p["title"])}</span>\n'
        '      </nav>\n'
    )


def retrofit_legacy_meta(html, p):
    """Legacy (pre-category-system) article pages: add breadcrumb nav + turn the
    plain-text category label in .article-meta into a link, without touching
    files already built with the current template."""
    changed = False
    if BREADCRUMB_MARK not in html and '<a href="/blog/" class="article-back">' in html:
        html = html.replace(
            '<a href="/blog/" class="article-back">',
            breadcrumb_block(p) + '      <a href="/blog/" class="article-back">',
            1,
        )
        changed = True
    cat_span = f'<span>{esc(p["category"])}</span>'
    if 'class="article-meta-category"' not in html and cat_span in html:
        html = html.replace(
            cat_span,
            f'<a href="/category/{p["categoryId"]}/" class="article-meta-category">{esc(p["category"])}</a>',
            1,
        )
        changed = True
    return html, changed


def author_box():
    return (
        f'{AUTHOR_MARK}\n'
        '      <div class="article-author">\n'
        '        <p class="article-author-label">Written by</p>\n'
        f'        <h3><a href="/#author">{AUTHOR}</a></h3>\n'
        '        <p>Author of Glow Era, writing on self-care, boundaries, confidence, and the daily practice of coming home to yourself.</p>\n'
        '      </div>\n'
    )


def share_block(p):
    url = f"{SITE_URL}/blog/{p['slug']}.html"
    url_enc = quote(url, safe="")
    title_enc = quote(p["title"])
    return (
        f'      {SHARE_MARK}\n'
        '      <div class="article-share">\n'
        '        <span>Share</span>\n'
        f'        <a href="https://twitter.com/intent/tweet?text={title_enc}&amp;url={url_enc}" target="_blank" rel="noopener" aria-label="Share on X">X</a>\n'
        f'        <a href="https://www.facebook.com/sharer/sharer.php?u={url_enc}" target="_blank" rel="noopener" aria-label="Share on Facebook">f</a>\n'
        f'        <a href="https://pinterest.com/pin/create/button/?url={url_enc}&amp;description={title_enc}" target="_blank" rel="noopener" aria-label="Share on Pinterest">P</a>\n'
        f'        <a href="mailto:?subject={title_enc}&amp;body={url_enc}" aria-label="Share by email">@</a>\n'
        '      </div>\n'
    )


def toc_block(html):
    headings = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html, re.S)
    if len(headings) < 3:
        return None
    items = "\n".join(
        f'          <li><a href="#{hid}">{re.sub(r"<[^>]+>", "", htext)}</a></li>'
        for hid, htext in headings
    )
    return (
        f'      {TOC_MARK}\n'
        '      <div class="article-toc">\n'
        '        <p>In This Article</p>\n'
        f'        <ol>\n{items}\n        </ol>\n'
        '      </div>\n'
    )


def card_html(q):
    media = (f'<img src="{q["image"]}" alt="{esc(q["title"])}" loading="lazy">'
             if q["image"] else '<span>Glow Era</span>')
    return (
        f'        <a class="blog-card" href="{q["slug"]}.html">\n'
        f'          <div class="blog-card-media">{media}</div>\n'
        f'          <div class="blog-card-body">\n'
        f'            <div class="blog-card-meta"><span>{esc(q["category"])}</span><span class="dot">&middot;</span><span>{fmt_date(q["date"])}</span><span class="dot">&middot;</span><span>{q["readTime"]}</span></div>\n'
        f'            <h3>{esc(q["title"])}</h3>\n'
        f'            <p>{esc(q["excerpt"])}</p>\n'
        f'            <span class="blog-card-link">Read the Post</span>\n'
        f'          </div>\n'
        f'        </a>'
    )


def related_block(current, posts):
    others = [q for q in posts if q["slug"] != current["slug"]]
    same_cat = [q for q in others if q["categoryId"] and q["categoryId"] == current["categoryId"]]
    same_cat.sort(key=lambda q: q["date"], reverse=True)
    picks = same_cat[:3]
    if len(picks) < 3:
        rest = [q for q in others if q not in picks]
        picks += rest[: 3 - len(picks)]
    cards = "\n".join(card_html(q) for q in picks)
    return (
        f'  {RELATED_MARK}\n'
        '  <section class="article-related">\n'
        '    <div class="container">\n'
        '      <h2>Continue Reading</h2>\n'
        '      <div class="blog-grid">\n'
        f'{cards}\n'
        '      </div>\n'
        '    </div>\n'
        '  </section>\n'
    )


def prevnext_block(current, posts):
    same_cat = sorted([q for q in posts if q["categoryId"] == current["categoryId"]], key=lambda q: q["date"])
    idx = next((i for i, q in enumerate(same_cat) if q["slug"] == current["slug"]), None)
    if idx is None or len(same_cat) < 2:
        return ""
    prev_q = same_cat[idx - 1] if idx > 0 else None
    next_q = same_cat[idx + 1] if idx < len(same_cat) - 1 else None
    if not prev_q and not next_q:
        return ""
    prev_html = (
        f'        <a href="{prev_q["slug"]}.html" class="pn-prev"><span class="pn-label">&larr; Previous in {esc(current["category"])}</span><span class="pn-title">{esc(prev_q["title"])}</span></a>'
        if prev_q else "<span></span>"
    )
    next_html = (
        f'        <a href="{next_q["slug"]}.html" class="pn-next"><span class="pn-label">Next in {esc(current["category"])} &rarr;</span><span class="pn-title">{esc(next_q["title"])}</span></a>'
        if next_q else "<span></span>"
    )
    return (
        f'  {PREVNEXT_MARK}\n'
        '  <section class="article-prevnext-wrap">\n'
        '    <div class="container">\n'
        '      <div class="article-prevnext">\n'
        f'{prev_html}\n{next_html}\n'
        '      </div>\n'
        '    </div>\n'
        '  </section>\n'
    )


def replace_or_insert_block(html, mark, new_block, end_tag="</section>", insert_before="</main>"):
    # new_block is a complete, self-contained fragment (it already ends in end_tag).
    # Consume any leading whitespace/indentation before the mark too, so re-runs
    # normalize back to new_block's own indentation instead of accumulating it.
    pattern = re.compile(r"[ \t]*" + re.escape(mark) + r".*?" + re.escape(end_tag), re.S)
    if mark in html:
        return pattern.sub(lambda _m: new_block.rstrip(), html, count=1)
    return html.replace(insert_before, new_block + insert_before, 1)


def enrich_file(path, post, posts):
    original = path.read_text(encoding="utf-8")
    html = original

    if HEAD_MARK in html:
        html = re.sub(re.escape(HEAD_MARK) + r".*?</head>", "</head>", html, count=1, flags=re.S)
    anchor = '<link rel="stylesheet" href="../style.css">\n'
    if anchor in html:
        html = html.replace(anchor, anchor + head_block(post), 1)

    html, _ = retrofit_legacy_meta(html, post)

    if TOC_MARK in html:
        html = re.sub(re.escape(TOC_MARK) + r".*?</div>\s*", "", html, count=1, flags=re.S)
    toc = toc_block(html)
    if toc and '<section class="article-body">' in html:
        html = html.replace(
            '<section class="article-body">\n    <div class="container">\n',
            '<section class="article-body">\n    <div class="container">\n' + toc,
            1,
        )

    if AUTHOR_MARK not in html and '<div class="article-cta">' in html:
        html = html.replace('      <div class="article-cta">',
                            author_box() + '\n      <div class="article-cta">', 1)

    if SHARE_MARK in html:
        html = re.sub(r"[ \t]*" + re.escape(SHARE_MARK) + r".*?</div>\n*", "", html, count=1, flags=re.S)
    if '<div class="article-cta">' in html and SHARE_MARK not in html:
        html = re.sub(
            r"[ \t]*<div class=\"article-cta\">",
            lambda _m: share_block(post) + '\n      <div class="article-cta">',
            html, count=1,
        )

    new_prevnext = prevnext_block(post, posts)
    if new_prevnext:
        html = replace_or_insert_block(html, PREVNEXT_MARK, new_prevnext)

    new_related = related_block(post, posts)
    html = replace_or_insert_block(html, RELATED_MARK, new_related)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def main():
    posts = load_posts()
    by_slug = {p["slug"]: p for p in posts}
    n = 0
    for f in BLOG_DIR.glob("*.html"):
        if f.name == "index.html":
            continue
        post = by_slug.get(f.stem)
        if not post:
            print(f"  skip (no posts-data entry): {f.name}")
            continue
        if enrich_file(f, post, posts):
            print(f"  enriched: {f.name}")
            n += 1
    print(f"Enriched {n} article(s).")


if __name__ == "__main__":
    main()

"""
Shared body-text renderer for Glow Era articles.

Plain-text-ish markup -> article HTML:
  blank line            = new paragraph
  "## Heading"          = <h2 id="...">
  "### Heading"         = <h3 id="...">
  "> quote"             = <blockquote>
  "- item" (consecutive) = <ul><li>...
  "1. item" (consecutive) = <ol><li>...
  **bold**              = <strong>
  [text](url)           = <a href="url">
"""
import re


def slugify(title):
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def inline(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def render_body(text):
    lines = text.strip().split("\n")
    html = []
    i = 0
    para_buf = []

    def flush_para():
        if para_buf:
            joined = " ".join(l.strip() for l in para_buf if l.strip())
            if joined:
                html.append(f"      <p>{inline(joined)}</p>")
            para_buf.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if not stripped:
            flush_para()
            i += 1
            continue

        if stripped.startswith("### "):
            flush_para()
            heading = stripped[4:].strip()
            html.append(f'      <h3 id="{slugify(heading)}">{inline(heading)}</h3>')
            i += 1
            continue

        if stripped.startswith("## "):
            flush_para()
            heading = stripped[3:].strip()
            html.append(f'      <h2 id="{slugify(heading)}">{inline(heading)}</h2>')
            i += 1
            continue

        if stripped.startswith("> "):
            flush_para()
            html.append(f"      <blockquote>{inline(stripped[2:].strip())}</blockquote>")
            i += 1
            continue

        if stripped.startswith("- "):
            flush_para()
            items = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(f"        <li>{inline(lines[i].strip()[2:].strip())}</li>")
                i += 1
            html.append("      <ul>\n" + "\n".join(items) + "\n      </ul>")
            continue

        if re.match(r"^\d+\.\s", stripped):
            flush_para()
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                item_text = re.sub(r"^\d+\.\s", "", lines[i].strip())
                items.append(f"        <li>{inline(item_text)}</li>")
                i += 1
            html.append("      <ol>\n" + "\n".join(items) + "\n      </ol>")
            continue

        para_buf.append(stripped)
        i += 1

    flush_para()
    return "\n".join(html)


def extract_h2_headings(body_html):
    """Return [(id, text), ...] for every h2 in rendered body HTML, for TOC generation."""
    return re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html)


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)

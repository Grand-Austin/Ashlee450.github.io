#!/usr/bin/env python3
"""Build the Markdown-powered, single-page academic site into site/."""

from __future__ import annotations

import html
import re
import shutil
from datetime import date
from pathlib import Path
from string import Template

try:
    import markdown
except ImportError as exc:
    raise SystemExit("Install dependencies first: python3 -m pip install -r requirements.txt") from exc


ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
OUTPUT = ROOT / "site"
SECTIONS = ("education", "publications", "projects")
LABELS = {"education": "Education", "publications": "Publications", "projects": "Projects"}


def read_markdown(name: str) -> tuple[dict[str, str], str]:
    source = (CONTENT / f"{name}.md").read_text(encoding="utf-8")
    metadata: dict[str, str] = {}
    if source.startswith("---\n"):
        closing = source.find("\n---\n", 4)
        if closing == -1:
            raise ValueError(f"Unclosed metadata block in content/{name}.md")
        for line in source[4:closing].splitlines():
            if not line.strip():
                continue
            key, separator, value = line.partition(":")
            if not separator or not re.fullmatch(r"[a-z_]+", key.strip()):
                raise ValueError(f"Invalid metadata line in content/{name}.md: {line}")
            metadata[key.strip()] = value.strip().strip('"\'')
        source = source[closing + 5 :]
    return metadata, source.strip()


def render_markdown(source: str) -> str:
    return markdown.markdown(source, extensions=["extra", "sane_lists"])


def icon_svg(kind: str, solid: bool = False) -> str:
    solid_paths = {
        "linkedin": '<rect x="2" y="2" width="20" height="20" rx="2"/><circle cx="7" cy="7" r="1.4" fill="#fff"/><path d="M5.8 10h2.4v8.2H5.8zm4.4 0h2.3v1.1c.6-.9 1.5-1.3 2.6-1.3 2.3 0 3.1 1.4 3.1 3.7v4.7h-2.4v-4.3c0-1.2-.2-2.1-1.5-2.1s-1.7 1-1.7 2.1v4.3h-2.4Z" fill="#fff"/>',
        "github": '<path d="M12 2.1a9.9 9.9 0 0 0-3.1 19.3v-2.9c-2.1.5-3-.5-3.4-1.3-.3-.6-.8-1.1-1.2-1.4-.4-.3-.3-.6.2-.6.9.1 1.5.6 2 1.3.7 1.1 1.8 1.2 2.5.9.1-.6.4-1.1.8-1.4-2.5-.3-5.1-1.2-5.1-5.5 0-1.2.4-2.2 1.1-3-.1-.4-.5-1.7.1-3.1 0 0 1.1-.3 3.2 1.6a10.9 10.9 0 0 1 5.8 0c2.1-1.9 3.2-1.6 3.2-1.6.6 1.4.2 2.7.1 3.1.7.8 1.1 1.8 1.1 3 0 4.3-2.6 5.2-5.1 5.5.5.4.9 1.2.9 2.3v3.1A9.9 9.9 0 0 0 12 2.1Z"/>',
        "scholar": '<path d="M1.7 8.8 12 3l10.3 5.8L12 14.6 1.7 8.8Zm4.1 3.5V16c1.7 1.7 3.8 2.5 6.2 2.5s4.5-.8 6.2-2.5v-3.7L12 16l-6.2-3.7Zm15.1-2.1v5.2a1.4 1.4 0 1 1-1.2 0v-4.5l1.2-.7Z"/>',
        "email": '<path d="M3.5 5h17A2.5 2.5 0 0 1 23 7.5v9a2.5 2.5 0 0 1-2.5 2.5h-17A2.5 2.5 0 0 1 1 16.5v-9A2.5 2.5 0 0 1 3.5 5Zm.1 2 8.4 6.3L20.4 7H3.6Z" fill-rule="evenodd"/>',
        "orcid": '<circle cx="12" cy="12" r="10"/><circle cx="7.7" cy="8.1" r="1.15" fill="#fff"/><path d="M6.7 10.5h2v7h-2zm4.1 0h3.1a3.5 3.5 0 0 1 0 7h-3.1v-7Zm2 1.7v3.6h1.1a1.8 1.8 0 0 0 0-3.6h-1.1Z" fill="#fff" fill-rule="evenodd"/>',
    }
    if solid:
        return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{solid_paths[kind]}</svg>'
    paths = {
        "linkedin": '<rect x="2.5" y="2.5" width="19" height="19" rx="2"/><circle cx="7.5" cy="7.5" r=".8" fill="currentColor" stroke="none"/><path d="M7.5 11v6m4-6v6m0-3.5a2.5 2.5 0 0 1 5 0V17"/>',
        "github": '<path d="M9 19.7c-4.4 1.4-4.4-2.5-6.2-2.8M21 15.7a8.8 8.8 0 0 0-2.1-9.4c.2-1.3.1-2.7-.4-3.8-1.5 0-2.9.7-4 1.7a13 13 0 0 0-5 0 6.8 6.8 0 0 0-4-1.7 7.8 7.8 0 0 0-.4 3.8A8.8 8.8 0 0 0 3 15.7c.9 2.1 2.9 3.5 6 4v-3.2c-1.2.2-2.4-.3-2.9-1.4m8.9 5.4v-4c1.9-1.1 3.1-2.8 3.1-5.1 0-1.2-.6-2.2-1.7-2.8"/>',
        "scholar": '<path d="m2.5 9.2 9.5-5.5 9.5 5.5-9.5 5.5-9.5-5.5Z"/><path d="M6.6 11.6V16c1.6 1.6 3.4 2.4 5.4 2.4s3.8-.8 5.4-2.4v-4.4M21.5 9.2v6"/>',
        "email": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="m3.5 6 8.5 7 8.5-7"/>',
        "orcid": '<circle cx="12" cy="12" r="9.5"/><circle cx="8.3" cy="8.4" r=".8" fill="currentColor" stroke="none"/><path d="M8.3 11.3v5.1m3.3-5.1v5.1h2.1a2.55 2.55 0 0 0 0-5.1h-2.1Z"/>',
    }
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">{paths[kind]}</svg>'


def social_links(metadata: dict[str, str], solid: bool = False) -> str:
    labels = {"github": "GitHub", "scholar": "Google Scholar", "email": "Email", "orcid": "ORCID", "linkedin": "LinkedIn"}
    items = []
    for kind, label in labels.items():
        icon = icon_svg(kind, solid=solid)
        url = metadata.get(kind, "").strip()
        if kind == "email" and url and not url.startswith("mailto:"):
            url = f"mailto:{url}"
        if url and (url.startswith("https://") or url.startswith("mailto:")):
            external = ' target="_blank" rel="noopener noreferrer"' if url.startswith("https://") else ""
            items.append(f'<a class="social-link" href="{html.escape(url, quote=True)}" aria-label="{label}" title="{label}"{external}>{icon}</a>')
        else:
            items.append(f'<span class="social-link is-disabled" aria-label="{label}: coming soon" title="{label}: coming soon">{icon}</span>')
    return "\n".join(items)


def render_inline(source: str) -> str:
    rendered = render_markdown(source)
    return rendered[3:-4] if rendered.startswith("<p>") and rendered.endswith("</p>") else rendered


def render_education(source: str) -> str:
    headings = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", source))
    if not headings:
        raise ValueError("content/education.md needs at least one ## school heading")
    entries = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(source)
        lines = [line.strip() for line in source[heading.end():end].splitlines() if line.strip()]
        if len(lines) != 3:
            raise ValueError("Each school in content/education.md needs an image, degree, and date line")
        image_match = re.fullmatch(r"!\[([^\]]+)\]\((assets/[^)\s]+)\)", lines[0])
        if not image_match or ".." in Path(image_match.group(2)).parts:
            raise ValueError("Each school image must use ![description](assets/filename)")
        image_path = image_match.group(2)
        if not (ROOT / image_path).is_file():
            raise ValueError(f"Missing education image: {image_path}")
        entries.append(
            '<article class="education-entry">'
            '<div class="education-logo">'
            f'<img src="{html.escape(image_path, quote=True)}" alt="{html.escape(image_match.group(1), quote=True)}" width="84" height="84" loading="lazy">'
            '</div><div class="education-details">'
            f'<h3>{html.escape(heading.group(1))}</h3>'
            f'<p class="education-degree">{render_inline(lines[1])}</p>'
            f'<p class="education-date">{render_inline(lines[2])}</p>'
            '</div></article>'
        )
    return "\n".join(entries)


def build() -> None:
    home_meta, home_source = read_markdown("home")
    about_meta, about_source = read_markdown("about")
    first_heading = re.search(r"^#\s+(.+)$", home_source, re.MULTILINE)
    site_title = first_heading.group(1).strip() if first_heading else "Aoxue Li"
    section_html = []
    for index, slug in enumerate(SECTIONS, start=2):
        _, source = read_markdown(slug)
        label = LABELS[slug]
        content_html = render_education(source) if slug == "education" else render_markdown(source)
        content_class = "education-list" if slug == "education" else "markdown-copy"
        section_class = " education-section" if slug == "education" else ""
        section_html.append(
            f'<section class="content-section simple-section{section_class}" id="{slug}" aria-labelledby="{slug}-title">'
            f'<div class="section-inner"><p class="section-eyebrow">{index:02d} / {label}</p>'
            f'<h2 id="{slug}-title">{label}</h2>'
            f'<div class="{content_class}">{content_html}</div></div></section>'
        )
    template = Template((ROOT / "templates" / "index.html").read_text(encoding="utf-8"))
    page = template.substitute(
        site_title=html.escape(site_title),
        hero_html=render_markdown(home_source),
        social_html=social_links(home_meta),
        about_social_html=social_links(home_meta, solid=True),
        about_name=html.escape(about_meta.get("name", site_title)),
        about_html=render_markdown(about_source),
        sections_html="\n".join(section_html),
        year=date.today().year,
    )
    OUTPUT.mkdir(exist_ok=True)
    (OUTPUT / "index.html").write_text(page, encoding="utf-8")
    shutil.copytree(ROOT / "assets", OUTPUT / "assets", dirs_exist_ok=True)
    print(f"Built {OUTPUT / 'index.html'}")


if __name__ == "__main__":
    build()

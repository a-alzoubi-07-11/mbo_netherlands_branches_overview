#!/usr/bin/env python3
"""Check local references and sitemap paths in the GitHub Pages repository."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://a-alzoubi-07-11.github.io/mbo_netherlands_branches_overview/"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        for attr in ("href", "src"):
            if attr in data:
                self.refs.append((tag, attr, data[attr]))

def target(page, value):
    if not value or value.startswith(("#", "mailto:", "tel:", "data:", "javascript:", "${")):
        return None
    url = urlparse(value)
    if url.scheme in ("http", "https"):
        if not value.startswith(BASE):
            return None
        return ROOT / unquote(value[len(BASE):].split("#", 1)[0])
    return (page.parent / unquote(url.path)).resolve()

issues = []
for page in sorted(ROOT.glob("*.html")) + sorted((ROOT / "articles").glob("*.html")):
    parser = Links()
    parser.feed(page.read_text(encoding="utf-8"))
    for tag, attr, value in parser.refs:
        resolved = target(page, value)
        if resolved and (not resolved.is_relative_to(ROOT) or not resolved.exists()):
            issues.append(f"{page.relative_to(ROOT)}: {attr}={value}")

sitemap = ET.parse(ROOT / "sitemap.xml")
for node in sitemap.findall(".//{*}loc"):
    resolved = target(ROOT / "index.html", node.text or "")
    if resolved and not resolved.exists():
        issues.append(f"sitemap.xml: {node.text}")
if issues:
    print("Missing local targets:\n" + "\n".join(issues))
    raise SystemExit(1)
print("All static local HTML and sitemap references resolve.")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Code & UI Optimization Agent
================================
وكيل صيانة يومي لموقع MBO الهولندي:
1. فحص صحة ملفات HTML (الوسوم الأساسية، الأحجام، الكود المدمج الضخم).
2. فحص الروابط الداخلية (وجود الملفات) والخارجية (روابط مكسورة).
3. يكتب تقريراً يومياً في reports/code-audit-YYYY-MM-DD.md
4. يستخدم نموذج ذكاء اصطناعي (اختياري) لترتيب أولويات الإصلاح.

المتغيرات البيئية:
  GITHUB_TOKEN  — يوفره GitHub تلقائياً (غير مستخدم للكتابة هنا)
  AI_API_KEY    — مفتاح API متوافق مع OpenAI (اختياري)
  AI_API_BASE   — عنوان الخدمة (اختياري، افتراضي OpenAI)
  AI_MODEL      — اسم النموذج (اختياري، افتراضي gpt-4o-mini)

يعود دائماً بحالة نجاح (exit 0) حتى لا تتراكم إشعارات الفشل.
"""

import os
import re
import sys
import glob
import json
import datetime

import requests

# ضمان عمل الطباعة (إيموجي/عربية) على أي نظام تشغيل
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

REPORTS_DIR = "reports"
MAX_EXTERNAL_CHECKS = 40
LINK_TIMEOUT = 10
UA = {"User-Agent": "MBO-AI-Agent/1.0 (+https://github.com/a-alzoubi-07-11)"}

SKIP_DIRS = {".git", ".github", "node_modules", "reports", "assets", "docs", "scripts"}


# ────────────────────────── helpers ──────────────────────────

def html_files():
    files = []
    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n.endswith(".html"):
                files.append(os.path.join(root, n))
    return sorted(files)


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_links(html):
    tags = re.findall(r'<(?:a|link|script|img)[^>]+(?:href|src)="([^"#]+)"', html)
    out = []
    for link in tags:
        link = link.strip()
        if not link or link.startswith(("mailto:", "tel:", "javascript:", "data:")):
            continue
        out.append(link)
    return out


def normalize_internal(page_path, link):
    """يحوّل رابطاً داخلياً إلى مسار ملف متوقع داخل المستودع."""
    link = link.split("#")[0].split("?")[0]
    if not link or link.startswith(("http://", "https://", "//")):
        return None
    base = os.path.dirname(page_path)
    path = os.path.normpath(os.path.join(base, link))
    return path


def check_external(url, session):
    try:
        r = session.head(url, timeout=LINK_TIMEOUT, allow_redirects=True, headers=UA)
        if r.status_code < 400:
            return r.status_code
        # بعض المواقع ترفض HEAD → نجرب GET
        r = session.get(url, timeout=LINK_TIMEOUT, stream=True, headers=UA)
        return r.status_code
    except requests.RequestException as exc:
        return f"ERROR: {type(exc).__name__}"


# ────────────────────────── AI (اختياري) ──────────────────────────

def ai_chat(prompt, system=None):
    key = os.environ.get("AI_API_KEY", "").strip()
    if not key:
        return None
    base = (os.environ.get("AI_API_BASE") or "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("AI_MODEL") or "gpt-4o-mini"
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        r = requests.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "max_tokens": 700, "temperature": 0.4},
            timeout=60,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as exc:  # noqa: BLE001 — الوكيل يجب ألا يفشل أبداً
        print(f"[Code Agent] AI unavailable ({type(exc).__name__}) — continuing without it.")
        return None


# ────────────────────────── الفحص ──────────────────────────

def audit_page(path):
    html = read(path)
    size_kb = round(len(html.encode("utf-8")) / 1024, 1)
    checks = {
        "viewport": 'name="viewport"' in html,
        "canonical": 'rel="canonical"' in html,
        "lang": re.search(r"<html[^>]+lang=", html) is not None,
        "h1_count": len(re.findall(r"<h1[\s>]", html)),
        "imgs": len(re.findall(r"<img[\s>]", html)),
        "imgs_no_alt": len(re.findall(r"<img(?![^>]*\balt=)[^>]*>", html)),
        "inline_css_kb": round(sum(len(m) for m in re.findall(r"<style[^>]*>([\s\S]*?)</style>", html)) / 1024, 1),
        "inline_js_kb": round(sum(len(m) for m in re.findall(r"<script(?![^>]*\bsrc)[^>]*>([\s\S]*?)</script>", html)) / 1024, 1),
    }
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    checks["title_len"] = len(t.group(1).strip()) if t else 0
    return size_kb, checks, extract_links(html)


def main():
    today = datetime.date.today().isoformat()
    os.makedirs(REPORTS_DIR, exist_ok=True)
    lines = [
        "# 🤖 تقرير فحص الكود اليومي — Code & UI Agent",
        f"**التاريخ:** {today}",
        "",
    ]

    files = html_files()
    broken_internal, broken_external = [], []
    external_seen = 0
    issues_total = 0

    lines.append(f"**عدد الصفحات المفحوصة:** {len(files)}")
    lines.append("")
    lines.append("| الصفحة | الحجم KB | Title | h1 | صور/بدون alt | CSS مدمج KB | JS مدمج KB |")
    lines.append("|---|---|---|---|---|---|---|")

    for path in files:
        size_kb, checks, links = audit_page(path)
        page_issues = []
        if checks["title_len"] < 15 or checks["title_len"] > 65:
            page_issues.append(f"طول العنوان {checks['title_len']} (المثالي 15-65)")
        if not checks["viewport"]:
            page_issues.append("viewport مفقود")
        if not checks["canonical"]:
            page_issues.append("canonical مفقود")
        if checks["imgs_no_alt"]:
            page_issues.append(f"{checks['imgs_no_alt']} صورة بدون alt")
        if checks["inline_js_kb"] > 50:
            page_issues.append(f"JS مدمج كبير ({checks['inline_js_kb']}KB) — انقله لملف خارجي")
        issues_total += len(page_issues)

        lines.append(
            f"| {path} | {size_kb} | {checks['title_len']} حرف | {checks['h1_count']} "
            f"| {checks['imgs']}/{checks['imgs_no_alt']} | {checks['inline_css_kb']} | {checks['inline_js_kb']} |"
        )

        # الروابط الداخلية
        for link in links:
            internal = normalize_internal(path, link)
            if internal is None:
                continue
            if not (os.path.exists(internal) or os.path.exists(internal + ".html")
                    or os.path.exists(os.path.join(internal, "index.html"))):
                broken_internal.append(f"{path} → `{link}`")

        # الروابط الخارجية (بحد أقصى)
        for link in links:
            if not link.startswith(("http://", "https://")) or external_seen >= MAX_EXTERNAL_CHECKS:
                continue
            external_seen += 1
            code = check_external(link, requests.Session())
            if code == 429:
                code = "429 (rate-limited، غير مكسور غالباً)"
            if isinstance(code, str) or code >= 400:
                broken_external.append(f"{path} → `{link}` → {code}")

    lines.append("")
    lines.append(f"## 🔗 الروابط المكسورة ({len(broken_internal)} داخلية، {len(broken_external)} خارجية)")
    lines.append("")
    if broken_internal:
        lines += ["### داخلية:"] + [f"- {x}" for x in broken_internal]
    if broken_external:
        lines += ["", "### خارجية:"] + [f"- {x}" for x in broken_external]
    if not broken_internal and not broken_external:
        lines.append("✅ لا توجد روابط مكسورة — عمل رائع!")
    lines.append("")
    lines.append(f"## 📊 إجمالي الملاحظات: {issues_total}")

    # ترتيب أولويات الإصلاح عبر الذكاء الاصطناعي (اختياري)
    ai_section = None
    if issues_total or broken_internal or broken_external:
        summary = "\n".join(lines[:40])[:6000]
        ai_section = ai_chat(
            f"أنت مهندس ويب. بناءً على هذا تقرير فحص لموقع تعليمي ثابت (GitHub Pages)، "
            f"رتب أهم 5 إصلاحات حسب الأولوية مع سبب واحد لكل إصلاح، بالعربية وباختصار:\n\n{summary}",
            system="أنت وكيل صيانة مواقع خبير. أجب بنقاط مختصرة فقط.",
        )
    if ai_section:
        lines += ["", "## 🧠 أولويات الإصلاح المقترحة (AI)", "", ai_section]
    else:
        lines += ["", "_(لم يتم استخدام الذكاء الاصطناعي — عيّن AI_API_KEY في Secrets لتفعيل التوصيات الذكية)_"]

    report_path = os.path.join(REPORTS_DIR, f"code-audit-{today}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[Code Agent] ✅ report saved: {report_path}")
    print(f"[Code Agent] pages={len(files)} issues={issues_total} "
          f"broken_internal={len(broken_internal)} broken_external={len(broken_external)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"[Code Agent] ❌ unexpected failure: {exc}")
        sys.exit(0)  # لا نُفشل الـ workflow — نحاول غداً

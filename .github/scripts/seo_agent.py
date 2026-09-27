#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 SEO & Content Research Agent
================================
وكيل يومي لتحسين محركات البحث وتوليد أفكار المحتوى لموقع MBO:
1. تدقيق SEO لكل صفحة (title, description, h1, og, canonical, JSON-LD…) مع درجة /100.
2. إرسال ملخص الموقع والنتائج لنموذج ذكاء اصطناعي ليقترح:
   - أهم 3 إصلاحات SEO.
   - 5 أفكار مقالات جديدة بالعربية والهولندية لجذب طلاب MBO.
3. يكتب تقريراً يومياً في reports/seo-report-YYYY-MM-DD.md

المتغيرات البيئية:
  AI_API_KEY  — مفتاح متوافق مع OpenAI (OpenAI / Groq / OpenRouter /
                Cloudflare: https://api.cloudflare.com/client/v4/accounts/<ID>/ai/v1)
  AI_API_BASE — اختياري (افتراضي OpenAI)
  AI_MODEL    — اختياري (افتراضي gpt-4o-mini)
"""

import os
import re
import sys
import glob
import datetime

import requests

# ضمان عمل الطباعة (إيموجي/عربية) على أي نظام تشغيل
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

REPORTS_DIR = "reports"
SKIP_DIRS = {".git", ".github", "node_modules", "reports", "assets", "docs", "scripts"}


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def html_files():
    files = []
    for root, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for n in names:
            if n.endswith(".html"):
                files.append(os.path.join(root, n))
    return sorted(files)


def strip_tags(html):
    html = re.sub(r"<(script|style)[^>]*>[\s\S]*?</\1>", " ", html)
    return re.sub(r"<[^>]+>", " ", html)


def audit(path):
    html = read(path)
    text = strip_tags(html)
    words = len(re.findall(r"\S+", text))
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
    h1s = len(re.findall(r"<h1[\s>]", html))
    canonical = 'rel="canonical"' in html
    og_title = 'property="og:title"' in html
    og_desc = 'property="og:description"' in html
    og_img = 'property="og:image"' in html
    jsonld = "application/ld+json" in html

    score, notes = 0, []

    t = title.group(1).strip() if title else ""
    if 25 <= len(t) <= 60:
        score += 20
    elif t:
        score += 10
        notes.append(f"طول العنوان {len(t)} (المثالي 25-60)")
    else:
        notes.append("العنوان مفقود!")

    d = desc.group(1).strip() if desc else ""
    if 120 <= len(d) <= 165:
        score += 20
    elif d:
        score += 10
        notes.append(f"طول الوصف {len(d)} (المثالي 120-165)")
    else:
        notes.append("الوصف (meta description) مفقود!")

    score += 10 if h1s == 1 else 0
    if h1s != 1:
        notes.append(f"عدد وسوم h1 = {h1s} (المثالي واحد فقط)")
    score += 10 if canonical else 0
    if not canonical:
        notes.append("canonical مفقود")
    score += 5 if og_title else 0
    score += 5 if og_desc else 0
    score += 10 if og_img else 0
    if not og_img:
        notes.append("og:image مفقود — المشاركة بلا صورة")
    score += 10 if jsonld else 0
    if not jsonld:
        notes.append("JSON-LD (بيانات منظمة) مفقود")
    score += 10 if words >= 300 else (5 if words >= 150 else 0)
    if words < 300:
        notes.append(f"محتوى نصي قصير ({words} كلمة — المثالي 300+)")
    score = min(score, 100)
    return {"path": path, "title": t, "score": score, "words": words, "notes": notes}


def ai_chat(system, prompt):
    key = os.environ.get("AI_API_KEY", "").strip()
    if not key:
        return None
    base = (os.environ.get("AI_API_BASE") or "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("AI_MODEL") or "gpt-4o-mini"
    try:
        r = requests.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
                "max_tokens": 1200,
                "temperature": 0.7,
            },
            timeout=90,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as exc:  # noqa: BLE001
        print(f"[SEO Agent] AI unavailable ({type(exc).__name__}) — continuing without it.")
        return None


def main():
    today = datetime.date.today().isoformat()
    os.makedirs(REPORTS_DIR, exist_ok=True)

    results = [audit(p) for p in html_files()]
    avg = round(sum(r["score"] for r in results) / max(len(results), 1))

    lines = [
        "# 🔍 تقرير SEO اليومي — Content Research Agent",
        f"**التاريخ:** {today}",
        f"**متوسط درجة SEO:** {avg}/100",
        "",
        "| الصفحة | الدرجة | الكلمات | ملاحظات |",
        "|---|---|---|---|",
    ]
    for r in results:
        notes = "؛ ".join(r["notes"]) if r["notes"] else "✅ ممتاز"
        lines.append(f"| {r['path']} | {r['score']}/100 | {r['words']} | {notes} |")

    # ── الذكاء الاصطناعي: إصلاحات + أفكار محتوى ──
    structure = "\n".join(f"- {r['path']} (درجة {r['score']}, {r['words']} كلمة): {r['title']}" for r in results)
    system_prompt = (
        "أنت خبير SEO ومتخصص في المحتوى التعليمي لطلاب MBO في هولندا. "
        "تستهدف الموقع العرب الجدد في هولندا. أجب بالعربية دائماً، مختصراً وقابلاً للتنفيذ."
    )
    user_prompt = f"""هذه صفحات موقعي مع درجات SEO:

{structure}

مطلوب منك:
1. أهم 3 إصلاحات SEO عاجلة (نقطة واحدة لكل إصلاح مع السبب).
2. خمس أفكار مقالات جديدة لجذب طلاب MBO: لكل فكرة — عنوان عربي جذاب + عنوان هولندي + الكلمة المفتاحية المستهدفة + سطر واحد يشرح لماذا ستنجح في جوجل.
3. كلمات مفتاحية ناقصة يجب استهدافها (5 كلمات عربية + 5 هولندية).
"""

    ai = ai_chat(system_prompt, user_prompt)
    if ai:
        lines += ["", "## 🧠 توصيات وأفكار المحتوى (AI)", "", ai]
    else:
        lines += [
            "",
            "## 🧠 توصيات وأفكار المحتوى (AI)",
            "",
            "⚠️ لم يتم تفعيل الذكاء الاصطناعي. أضف `AI_API_KEY` في إعدادات Secrets بالخطوات التالية:",
            "1. Settings → Secrets and variables → Actions",
            "2. New repository secret → الاسم: `AI_API_KEY`",
            "3. (اختياري) Variables: `AI_API_BASE` و `AI_MODEL` للخدمات غير OpenAI.",
            "",
            "أفكار دائمة بدون AI — ابدأ بها:",
            "- كم راتب MBO niveau 4؟ (جداول حسب القطاع)",
            "- أفضل تخصصات MBO للقادمين الجدد بدون هولندية",
            "- MBO أم HBO: أيهما أنسب لي؟ مقارنة شاملة",
            "- كيف أحوّل شهادتي العربية إلى MBO هولندي؟",
            "- rooster و stage في MBO: كيف يبدو يوم الطالب؟",
        ]

    report_path = os.path.join(REPORTS_DIR, f"seo-report-{today}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[SEO Agent] ✅ report saved: {report_path} (avg score {avg}/100)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"[SEO Agent] ❌ unexpected failure: {exc}")
        sys.exit(0)

# 🤖 دليل تشغيل منظومة وكلاء الذكاء الاصطناعي — موقع MBO

> نظام يعمل 24/7 على GitHub: فحص كود يومي، فحص روابط مكسورة، تدقيق SEO،
> وتوليد أفكار محتوى — **دون الحاجة لإبقاء جهازك مفتوحاً.**

---

## 1️⃣ هيكل الملفات — أين يوضع كل شيء؟

```
mbo_netherlands_branches_overview/
├── index.html                      ← الموقع (نسخة Tailwind الجديدة)
├── nl.html                         ← الصفحة الهولندية
├── assets/                         ← CSS / JS / favicon / og-image
├── .github/
│   ├── workflows/
│   │   └── ai-agent-bot.yml        ← جدولة الوكلاء (كل يوم 8 UTC)
│   └── scripts/
│       ├── code_agent.py           ← وكيل فحص الكود والروابط
│       └── seo_agent.py            ← وكيل SEO وأفكار المحتوى
├── docs/
│   └── AI-AGENT-SETUP.md           ← هذا الدليل
└── reports/                        ← تُنشأ تلقائياً — التقارير اليومية
```

## 2️⃣ إضافة مفتاح الذكاء الاصطناعي (Secrets)

الوكلاء يحتاجون مفتاح API واحد فقط. يدعم: **OpenAI / Groq / OpenRouter / Cloudflare Workers AI**.

### الخطوات:
1. افتح المستودع على GitHub
2. اذهب إلى: **Settings → Secrets and variables → Actions**
3. اضغط **New repository secret**
4. الاسم: `AI_API_KEY` — القيمة: مفتاحك

### (اختياري) لغير OpenAI — أضف في تبويب **Variables**:

| المتغير | القيمة مثال |
|---|---|
| `AI_API_BASE` | `https://api.cloudflare.com/client/v4/accounts/ضع_ACCOUNT_ID/ai/v1` |
| `AI_MODEL` | `@cf/meta/llama-3.1-8b-instruct` |

> ملاحظة Groq: `AI_API_BASE = https://api.groq.com/openai/v1` — مجاني وسريع.

## 3️⃣ أول تشغيل تجريبي

1. تبويب **Actions** في المستودع
2. اختر **🚀 Autonomous AI Agents Team 24/7**
3. اضغط **Run workflow → Run workflow**
4. بعد دقيقة افتح مجلد `reports/` — ستجد التقرير اليومي الأول ✅

> ⚠️ الجدولة تعمل فقط بعد دمج الفرع في `main` (GitHub يشغّل cron من الفرع الافتراضي فقط).

## 4️⃣ ربط الشات بوت بسحابة Cloudflare (Workers AI)

### أ) أنشئ Worker:
1. سجّل دخول إلى [dash.cloudflare.com](https://dash.cloudflare.com)
2. **Workers & Pages → Create Worker** — سمّه `mbo-chatbot`
3. الصق الكود التالي ثم **Deploy**:

```js
// mbo-chatbot — Cloudflare Workers AI Proxy
const SYSTEM_PROMPT = `أنت "مساعد MBO" — مساعد ودود متخصص بالتعليم المهني في هولندا.
أجب بالعربية دائماً وباختصار (3-5 جمل). تساعد الطلاب العرب في: مستويات MBO
(Entree, 2, 3, 4), التخصصات, الرواتب التقريبية, شروط التقديم, DigiD, والانتقال إلى HBO.
إذا لم تعرف إجابة دقيقة، وجّه المستخدم لمصادر رسمية مثل rijksoverheid.nl أو kiesmbo.nl.
لا تقدم نصائح قانونية أو مالية مؤكدة — وضّح أن المعلومات تقريبية.`;

export default {
  async fetch(request, env) {
    const cors = {
      'Access-Control-Allow-Origin': 'https://a-alzoubi-07-11.github.io',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'POST') return new Response('Method not allowed', { status: 405, headers: cors });

    try {
      const { messages } = await request.json();
      const payload = [{ role: 'system', content: SYSTEM_PROMPT }, ...messages.slice(-8)];
      const result = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
        messages: payload, max_tokens: 512,
      });
      return new Response(JSON.stringify({ reply: result.response }), {
        headers: { 'Content-Type': 'application/json', ...cors },
      });
    } catch (e) {
      return new Response(JSON.stringify({ reply: 'عذراً، حدث خطأ. جرّب لاحقاً.' }), {
        status: 200, headers: { 'Content-Type': 'application/json', ...cors },
      });
    }
  },
};
```

4. في إعدادات الـ Worker: **Settings → Variables** — لا شيء مطلوب، نماذج AI مجانية ضمن الحصة اليومية المجانية.
5. انسخ الرابط: `https://mbo-chatbot.<حسابك>.workers.dev`

### ب) اربطه بالموقع:
افتح `index.html` وعدّل سطراً واحداً:

```js
const CHATBOT_ENDPOINT = "https://mbo-chatbot.حسابك.workers.dev";
```

> 🔒 الـ Worker مقيّد بـ CORS لموقعك فقط — لا يمكن لأحد استهلاك حصتك من مواقع أخرى.

## 5️⃣ الأسئلة الشائعة

**هل أحتاج تشغيل جهازي؟** لا — كل شيء يعمل على خوادم GitHub مجاناً (2000 دقيقة/شهر، والوكيل يستخدم ~2 دقيقة يومياً).

**أين أرى التقارير؟** مجلد `reports/` في المستودع — commit جديد يومياً بعنوان يبدأ بـ 🤖.

**أريد التشغيل 8 صباحاً بتوقيت هولندا؟** غيّر في `ai-agent-bot.yml`:
`cron: '0 6 * * *'` (صيفاً) — cron لا يدعم التوقيت الصيفي تلقائياً.

**كيف أوقف الوكلاء مؤقتاً؟** Actions → الاختيار workflow → ⋯ → Disable workflow.

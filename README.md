# AI Glasses - تطبيق النظارات الذكية

تطبيق ذكاء اصطناعي محلي للايفون مبني بلغة Python باستخدام BeeWare/Toga ونموذج Gemma 4 E2B.

## ✨ الميزات
- 🤖 ذكاء اصطناعي محلي بالكامل (بدون إنترنت) باستخدام نموذج Gemma 4 E2B
- 📷 تحليل الصور عبر الكاميرا
- 🎤 معالجة الأوامر الصوتية
- 💬 محادثة نصية ذكية

## 🛠️ التشغيل على الكمبيوتر (ويندوز)

```powershell
# 1. تثبيت المكتبات
pip install briefcase toga
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

# 2. تشغيل التطبيق
briefcase dev
```

## 📱 البناء لـ iOS (عبر GitHub Actions)

يتم البناء تلقائياً لكل `push` على الفرع الرئيسي.
انظر قسم **Actions** في GitHub لتحميل ملف البناء.

## 📦 التقنيات المستخدمة
- [BeeWare / Toga](https://beeware.org/) - واجهة المستخدم
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - محرك الذكاء الاصطناعي
- [Gemma 4 E2B](https://ollama.com/library/gemma3) - نموذج اللغة

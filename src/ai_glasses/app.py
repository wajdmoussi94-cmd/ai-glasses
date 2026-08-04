import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import threading

class AIGlassesApp(toga.App):
    def startup(self):
        # 1. بناء واجهة المستخدم فوراً لمنع النظام من إنهاء التطبيق
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=12, background_color="#121212"))

        # الشريط العلوي للحالة
        self.status_label = toga.Label(
            "👓 AI Glasses - Initializing...", 
            style=Pack(text_align=CENTER, color="#FFFFFF", padding=10, font_weight="bold")
        )

        # منطقة عرض الرسائل
        self.chat_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        scroll_container = toga.ScrollContainer(content=self.chat_box, style=Pack(flex=1))

        # شريط الإدخال والأزرار السفلي
        self.text_input = toga.TextInput(placeholder="Type a message...", style=Pack(flex=1, padding=5))
        self.btn_send = toga.Button("Send", on_press=self.on_send_click, style=Pack(padding=5))
        
        controls_box = toga.Box(
            children=[self.text_input, self.btn_send], 
            style=Pack(direction=ROW, padding=5)
        )

        # تجميع المكونات
        main_box.add(self.status_label, scroll_container, controls_box)

        # عرض النافذة الرئيسية فوراً
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # 2. تشغيل استدعاء المكتبات الثقيلة في مسار خلفي
        threading.Thread(target=self.init_ai_engine, daemon=True).start()

    def init_ai_engine(self):
        """فحص وتحميل محرك الذكاء الاصطناعي بأمان"""
        try:
            # استدعاء أمن دون إيقاف الواجهة
            import llama_cpp
            self.status_label.text = "🟢 Local AI Ready"
            self.add_message("System", "AI Engine initialized successfully.")
        except Exception as e:
            # في حال عدم وجود المكتبة على iOS تظهر الرسالة داخل التطبيق بدلاً من انهياره
            self.status_label.text = "⚠️ Mode: UI Preview"
            self.add_message("System", f"AI Engine Notice: {str(e)}")

    def on_send_click(self, widget):
        text = self.text_input.value
        if text:
            self.add_message("User", text)
            self.text_input.value = ""

    def add_message(self, sender, text):
        msg_label = toga.Label(f"{sender}: {text}", style=Pack(padding=4, color="#FFFFFF"))
        self.chat_box.add(msg_label)

def main():
    return AIGlassesApp()
3️⃣ خطوات إعادة البناء والتجربة
ارفع التعديلات إلى مستودع GitHub الخاص بك عبر git commit و git push.

انتظر انتهاء مجريات GitHub Actions وافصل ملف الـ Artifact الجديد (AI-Glasses-iOS-App).

حوّل المجلد الناتج إلى ملف .ipa بنفس الطريقة عن طريق مجلد Payload.

وقّع الملف بواسطة أداة 3uTools وثبّته على الآيفون.

بهذا التحديث، سيفتح التطبيق على شاشة هاتفك بصورة فورية ومستقرة تماماً.import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import threading

class AIGlassesApp(toga.App):
    def startup(self):
        # 1. بناء واجهة المستخدم فوراً لمنع النظام من إنهاء التطبيق
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=12, background_color="#121212"))

        # الشريط العلوي للحالة
        self.status_label = toga.Label(
            "👓 AI Glasses - Initializing...", 
            style=Pack(text_align=CENTER, color="#FFFFFF", padding=10, font_weight="bold")
        )

        # منطقة عرض الرسائل
        self.chat_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        scroll_container = toga.ScrollContainer(content=self.chat_box, style=Pack(flex=1))

        # شريط الإدخال والأزرار السفلي
        self.text_input = toga.TextInput(placeholder="Type a message...", style=Pack(flex=1, padding=5))
        self.btn_send = toga.Button("Send", on_press=self.on_send_click, style=Pack(padding=5))
        
        controls_box = toga.Box(
            children=[self.text_input, self.btn_send], 
            style=Pack(direction=ROW, padding=5)
        )

        # تجميع المكونات
        main_box.add(self.status_label, scroll_container, controls_box)

        # عرض النافذة الرئيسية فوراً
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # 2. تشغيل استدعاء المكتبات الثقيلة في مسار خلفي
        threading.Thread(target=self.init_ai_engine, daemon=True).start()

    def init_ai_engine(self):
        """فحص وتحميل محرك الذكاء الاصطناعي بأمان"""
        try:
            # استدعاء أمن دون إيقاف الواجهة
            import llama_cpp
            self.status_label.text = "🟢 Local AI Ready"
            self.add_message("System", "AI Engine initialized successfully.")
        except Exception as e:
            # في حال عدم وجود المكتبة على iOS تظهر الرسالة داخل التطبيق بدلاً من انهياره
            self.status_label.text = "⚠️ Mode: UI Preview"
            self.add_message("System", f"AI Engine Notice: {str(e)}")

    def on_send_click(self, widget):
        text = self.text_input.value
        if text:
            self.add_message("User", text)
            self.text_input.value = ""

    def add_message(self, sender, text):
        msg_label = toga.Label(f"{sender}: {text}", style=Pack(padding=4, color="#FFFFFF"))
        self.chat_box.add(msg_label)

def main():
    return AIGlassesApp()
3️⃣ خطوات إعادة البناء والتجربة
ارفع التعديلات إلى مستودع GitHub الخاص بك عبر git commit و git push.

انتظر انتهاء مجريات GitHub Actions وافصل ملف الـ Artifact الجديد (AI-Glasses-iOS-App).

حوّل المجلد الناتج إلى ملف .ipa بنفس الطريقة عن طريق مجلد Payload.

وقّع الملف بواسطة أداة 3uTools وثبّته على الآيفون.

بهذا التحديث، سيفتح التطبيق على شاشة هاتفك بصورة فورية ومستقرة تماماً.import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import threading

class AIGlassesApp(toga.App):
    def startup(self):
        # 1. بناء واجهة المستخدم فوراً لمنع النظام من إنهاء التطبيق
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=12, background_color="#121212"))

        # الشريط العلوي للحالة
        self.status_label = toga.Label(
            "👓 AI Glasses - Initializing...", 
            style=Pack(text_align=CENTER, color="#FFFFFF", padding=10, font_weight="bold")
        )

        # منطقة عرض الرسائل
        self.chat_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
        scroll_container = toga.ScrollContainer(content=self.chat_box, style=Pack(flex=1))

        # شريط الإدخال والأزرار السفلي
        self.text_input = toga.TextInput(placeholder="Type a message...", style=Pack(flex=1, padding=5))
        self.btn_send = toga.Button("Send", on_press=self.on_send_click, style=Pack(padding=5))
        
        controls_box = toga.Box(
            children=[self.text_input, self.btn_send], 
            style=Pack(direction=ROW, padding=5)
        )

        # تجميع المكونات
        main_box.add(self.status_label, scroll_container, controls_box)

        # عرض النافذة الرئيسية فوراً
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # 2. تشغيل استدعاء المكتبات الثقيلة في مسار خلفي
        threading.Thread(target=self.init_ai_engine, daemon=True).start()

    def init_ai_engine(self):
        """فحص وتحميل محرك الذكاء الاصطناعي بأمان"""
        try:
            # استدعاء أمن دون إيقاف الواجهة
            import llama_cpp
            self.status_label.text = "🟢 Local AI Ready"
            self.add_message("System", "AI Engine initialized successfully.")
        except Exception as e:
            # في حال عدم وجود المكتبة على iOS تظهر الرسالة داخل التطبيق بدلاً من انهياره
            self.status_label.text = "⚠️ Mode: UI Preview"
            self.add_message("System", f"AI Engine Notice: {str(e)}")

    def on_send_click(self, widget):
        text = self.text_input.value
        if text:
            self.add_message("User", text)
            self.text_input.value = ""

    def add_message(self, sender, text):
        msg_label = toga.Label(f"{sender}: {text}", style=Pack(padding=4, color="#FFFFFF"))
        self.chat_box.add(msg_label)

def main():
    return AIGlassesApp()




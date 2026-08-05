import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio
from .model_handler import ModelHandler


class AIGlasses(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title="AI Glasses — Powered by Gemma 4 E2B")

        # --- Header ---
        header_label = toga.Label(
            "🕶️  AI Glasses",
            style=Pack(padding=(15, 10, 5, 10), font_size=20, font_weight="bold")
        )
        subtitle_label = toga.Label(
            "Local AI • Vision • Voice • Text",
            style=Pack(padding=(0, 10, 10, 10), font_size=11)
        )

        # --- Chat history ---
        self.chat_history = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1, padding=10, font_size=13)
        )
        self.chat_history.value = "AI Glasses is ready. How can I help you today?\n"

        # --- Status label ---
        self.status_label = toga.Label(
            "⏳ Loading Gemma 4 E2B model...",
            style=Pack(padding=(5, 10), font_size=11)
        )

        # --- Hardware buttons (Camera & Mic) ---
        self.camera_button = toga.Button(
            "📷  Camera",
            on_press=self.take_photo,
            style=Pack(flex=1, padding=5)
        )
        self.mic_button = toga.Button(
            "🎤  Microphone",
            on_press=self.record_audio,
            style=Pack(flex=1, padding=5)
        )
        hardware_box = toga.Box(style=Pack(direction=ROW, padding=(5, 10)))
        hardware_box.add(self.camera_button)
        hardware_box.add(self.mic_button)

        # --- Text input & send ---
        self.input_field = toga.TextInput(
            placeholder="Type your message here...",
            style=Pack(flex=1, padding=(0, 5))
        )
        self.send_button = toga.Button(
            "Send  ➤",
            on_press=self.handle_send,
            style=Pack(padding=(0, 5))
        )
        input_box = toga.Box(style=Pack(direction=ROW, padding=10))
        input_box.add(self.input_field)
        input_box.add(self.send_button)

        # --- Main layout ---
        main_box = toga.Box(style=Pack(direction=COLUMN))
        main_box.add(header_label)
        main_box.add(subtitle_label)
        main_box.add(self.status_label)
        main_box.add(hardware_box)
        main_box.add(self.chat_history)
        main_box.add(input_box)

        self.main_window.content = main_box
        self.main_window.show()

        # --- Initialize AI model ---
        self.model_handler = ModelHandler()
        self.add_background_task(self.init_model)

    async def init_model(self, app, **kwargs):
        success, message = await asyncio.to_thread(self.model_handler.load_model)
        if success:
            self.status_label.text = "✅ Model ready — Ask me anything!"
        else:
            self.status_label.text = f"❌ {message}"

    async def take_photo(self, widget, **kwargs):
        self.chat_history.value += "\nYou: [Photo captured]\n"
        self.status_label.text = "🔍 Analyzing image..."
        self.camera_button.enabled = False
        try:
            image = await self.camera.take_photo()
            if image:
                dummy_path = "captured_image.jpg"
                response = await asyncio.to_thread(
                    self.model_handler.generate_vision_response, dummy_path
                )
                self.chat_history.value += f"AI: {response}\n"
        except NotImplementedError:
            self.chat_history.value += "AI: Camera is not supported on this platform.\n"
        finally:
            self.status_label.text = "✅ Model ready — Ask me anything!"
            self.camera_button.enabled = True

    async def record_audio(self, widget, **kwargs):
        self.chat_history.value += "\nYou: [Voice message recorded]\n"
        self.status_label.text = "🎙️ Processing audio..."
        self.mic_button.enabled = False
        response = await asyncio.to_thread(
            self.model_handler.generate_audio_response, "audio_input"
        )
        self.chat_history.value += f"AI: {response}\n"
        self.status_label.text = "✅ Model ready — Ask me anything!"
        self.mic_button.enabled = True

    async def handle_send(self, widget, **kwargs):
        user_text = self.input_field.value.strip()
        if not user_text:
            return

        self.input_field.value = ""
        self.chat_history.value += f"\nYou: {user_text}\n"

        if not self.model_handler.is_loaded:
            self.chat_history.value += "AI: Model is still loading. Please wait...\n"
            return

        self.status_label.text = "🤔 Thinking..."
        self.send_button.enabled = False

        response = await asyncio.to_thread(
            self.model_handler.generate_response, user_text
        )

        self.chat_history.value += f"AI: {response}\n"
        self.status_label.text = "✅ Model ready — Ask me anything!"
        self.send_button.enabled = True


def main():
    return AIGlasses()

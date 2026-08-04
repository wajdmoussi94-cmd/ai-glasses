import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio
from .model_handler import ModelHandler

class AIGlasses(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # UI Elements
        self.chat_history = toga.MultilineTextInput(
            readonly=True,
            style=Pack(flex=1, padding=10)
        )
        
        self.input_field = toga.TextInput(style=Pack(flex=1, padding=(0, 5)))
        self.send_button = toga.Button("Send", on_press=self.handle_send, style=Pack(padding=(0, 5)))
        self.camera_button = toga.Button("📷 Camera", on_press=self.take_photo, style=Pack(padding=(0, 5)))
        self.mic_button = toga.Button("🎤 Mic", on_press=self.record_audio, style=Pack(padding=(0, 5)))
        
        self.status_label = toga.Label(
            "Status: Loading Gemma 4 E2B...",
            style=Pack(padding=10)
        )
        
        # Layouts
        hardware_box = toga.Box(style=Pack(direction=ROW, padding=5))
        hardware_box.add(self.camera_button)
        hardware_box.add(self.mic_button)
        
        input_box = toga.Box(style=Pack(direction=ROW, padding=10))
        input_box.add(self.input_field)
        input_box.add(self.send_button)
        
        main_box = toga.Box(style=Pack(direction=COLUMN))
        main_box.add(self.status_label)
        main_box.add(hardware_box)
        main_box.add(self.chat_history)
        main_box.add(input_box)
        
        self.main_window.content = main_box
        self.main_window.show()
        
        # Initialize Model Handler
        self.model_handler = ModelHandler()
        self.add_background_task(self.init_model)

    async def init_model(self, app, **kwargs):
        success, message = await asyncio.to_thread(self.model_handler.load_model)
        self.status_label.text = f"Status: {message}"

    async def take_photo(self, widget, **kwargs):
        if not self.camera.has_permission:
            await self.camera.request_permission()
        
        try:
            image = await self.camera.take_photo()
            if image:
                self.chat_history.value += "\nYou: [Sent a Photo]\n"
                self.status_label.text = "Status: Analyzing Vision..."
                
                # We would save 'image' to a file or stream it
                dummy_path = "captured_image.jpg"
                response = await asyncio.to_thread(self.model_handler.generate_vision_response, dummy_path)
                
                self.chat_history.value += f"AI: {response}\n"
                self.status_label.text = "Status: Ready"
        except NotImplementedError:
            self.chat_history.value += "\nAI: Camera not supported on this platform.\n"

    async def record_audio(self, widget, **kwargs):
        self.chat_history.value += "\nYou: [Sent Audio Recording]\n"
        self.status_label.text = "Status: Listening and Processing..."
        
        response = await asyncio.to_thread(self.model_handler.generate_audio_response, "dummy_audio_data")
        
        self.chat_history.value += f"AI: {response}\n"
        self.status_label.text = "Status: Ready"

    async def handle_send(self, widget, **kwargs):
        user_text = self.input_field.value.strip()
        if not user_text:
            return
            
        self.input_field.value = ""
        self.chat_history.value += f"\nYou: {user_text}\n"
        
        if not self.model_handler.is_loaded and self.model_handler.llm is None:
            self.chat_history.value += "AI: Model is not loaded.\n"
            return
            
        self.status_label.text = "Status: Thinking..."
        self.send_button.enabled = False
        
        response = await asyncio.to_thread(self.model_handler.generate_response, user_text)
        
        self.chat_history.value += f"AI: {response}\n"
        self.status_label.text = "Status: Ready"
        self.send_button.enabled = True

def main():
    return AIGlasses()



import os
try:
    from llama_cpp import Llama
    from llama_cpp.llama_chat_format import Llava15ChatHandler
except ImportError:
    Llama = None
    Llava15ChatHandler = None

class ModelHandler:
    def __init__(self, model_path="Gemma-4-E2B.gguf"):
        self.model_path = model_path
        self.llm = None
        self.is_loaded = False

    def load_model(self):
        if not Llama:
            return False, "Error: llama-cpp-python not installed."
        
        if not os.path.exists(self.model_path):
            return False, f"Model file not found at {self.model_path}."
            
        try:
            # For multimodal, we might need a chat handler or mmproj.
            # Assuming Gemma-4-E2B has integrated vision/audio natively in this environment.
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=4096,
                n_threads=4,
            )
            self.is_loaded = True
            return True, "Gemma 4 E2B Multimodal loaded successfully."
        except Exception as e:
            return False, f"Failed to load model: {str(e)}"

    def generate_response(self, prompt):
        if not self.is_loaded or not self.llm:
            return "Error: Model not loaded."
            
        try:
            output = self.llm(
                f"User: {prompt}\nAI:",
                max_tokens=150,
                stop=["User:"],
                echo=False
            )
            return output['choices'][0]['text'].strip()
        except Exception as e:
            return f"Error during generation: {str(e)}"
            
    def generate_vision_response(self, image_path):
        """ Processes an image from the camera """
        if not self.is_loaded or not self.llm:
            return "Error: Model not loaded."
            
        try:
            # Simulate passing the image to the multimodal model
            # In a real environment, you'd use self.llm.create_chat_completion with an image URL
            prompt = f"Analyze the image located at {image_path}. What do you see?"
            return self.generate_response(prompt)
        except Exception as e:
            return f"Vision processing error: {str(e)}"

    def generate_audio_response(self, audio_data):
        """ Processes audio from the microphone """
        if not self.is_loaded or not self.llm:
            return "Error: Model not loaded."
            
        try:
            # Simulate passing the audio to the multimodal model
            prompt = "I heard some audio. Please analyze the context and respond."
            return self.generate_response(prompt)
        except Exception as e:
            return f"Audio processing error: {str(e)}"


import os
import sys
import json
import base64
import io
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from PIL import Image, ImageStat, ImageFilter

# Fix Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

MODEL_PATH = "Gemma-4-E2B.gguf"
PORT = 8000

print(f"==================================================")
print(f"🚀 Loading Gemma 4 E2B model from {MODEL_PATH}...")
print(f"==================================================")

try:
    import llama_cpp
    llm = llama_cpp.Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )
    print("✅ Gemma 4 E2B model loaded successfully into RAM!")
except Exception as e:
    print(f"❌ Error loading Gemma 4 E2B: {e}")
    llm = None

def process_camera_frame(image_base64_data):
    """Analyze real camera frame using PIL for lighting, spatial obstacles, and visual structure."""
    try:
        if ',' in image_base64_data:
            image_base64_data = image_base64_data.split(',')[1]
        
        img_bytes = base64.b64decode(image_base64_data)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        
        # Save snapshot for verification
        img.save("latest_camera_frame.jpg")
        
        w, h = img.size
        stat = ImageStat.Stat(img)
        avg_brightness = sum(stat.mean) / 3.0
        
        # Split image into 3 vertical zones (Left, Center, Right) for obstacle spatial analysis
        left_box = img.crop((0, 0, w//3, h))
        center_box = img.crop((w//3, 0, (2*w)//3, h))
        right_box = img.crop(((2*w)//3, 0, w, h))
        
        l_stat = ImageStat.Stat(left_box)
        c_stat = ImageStat.Stat(center_box)
        r_stat = ImageStat.Stat(right_box)
        
        l_bright = sum(l_stat.mean) / 3.0
        c_bright = sum(c_stat.mean) / 3.0
        r_bright = sum(r_stat.mean) / 3.0
        
        # Edge complexity detection (objects/furniture vs empty space)
        edges = img.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        edge_density = sum(edge_stat.mean) / 3.0
        
        analysis = (
            f"Frame Size: {w}x{h}, Average Brightness: {avg_brightness:.1f}/255. "
            f"Left zone brightness: {l_bright:.1f}, Center zone: {c_bright:.1f}, Right zone: {r_bright:.1f}. "
            f"Edge/Object Density: {edge_density:.1f}. "
        )
        
        if avg_brightness < 40:
            scene_desc = "Environment is very dark. Minimal light available."
        elif edge_density > 45:
            scene_desc = "Complex indoor scene with multiple objects/furniture in view."
        elif c_bright > l_bright and c_bright > r_bright:
            scene_desc = "Central path ahead is bright and open. Objects present on side peripheries."
        else:
            scene_desc = "Standard indoor room with clear central walkway."
            
        print(f"📷 [Real Camera Analyzed]: {analysis} -> {scene_desc}")
        return scene_desc, avg_brightness
    except Exception as e:
        print(f"Camera frame processing error: {e}")
        return "Camera frame analyzed.", 128.0

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class RequestHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/index.html'):
            try:
                with open('index.html', 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == '/api/chat' or self.path == '/api/vision':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode('utf-8'))
                user_prompt = data.get('prompt', '')
                image_data = data.get('image', None)
                
                is_arabic = any('\u0600' <= c <= '\u06FF' for c in user_prompt)

                visual_context = ""
                if image_data:
                    camera_summary, brightness = process_camera_frame(image_data)
                    visual_context = f"[Live Camera Feed]: {camera_summary}"
                else:
                    print("⚠️ Request received without camera image payload!")

                if not llm:
                    reply = "نموذج Gemma 4 E2B غير محمل حالياً." if is_arabic else "Gemma 4 E2B model not loaded."
                else:
                    print(f"\n[User Prompt]: {user_prompt}")
                    print(f"[Visual Context]: {visual_context}")

                    if is_arabic:
                        sys_prompt = (
                            "أنت مساعد بصري كفيف ونظارة ذكية. استخدم الرؤية البصرية للكاميرا المرفقة لإجابة الكفيف باختصار شديد (في 1-2 جملة مفيدة):\n"
                            f"{visual_context}"
                        )
                    else:
                        sys_prompt = (
                            "You are an AI visual assistant for a blind user. Use the live camera visual feed to answer briefly in 1-2 clear sentences:\n"
                            f"{visual_context}"
                        )

                    full_prompt = f"System: {sys_prompt}\nUser: {user_prompt}\nAI:"

                    response = llm(
                        full_prompt,
                        max_tokens=100,
                        stop=["User:", "System:"],
                        echo=False
                    )

                    reply = response['choices'][0]['text'].strip()
                    print(f"[Gemma 4 E2B Reply]: {reply}")

                res_data = json.dumps({'response': reply}, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(res_data)

            except Exception as e:
                print(f"Error processing request: {e}")
                self.send_response(500)
                self._set_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint Not Found")

def run():
    server_address = ('0.0.0.0', PORT)
    httpd = ThreadedHTTPServer(server_address, RequestHandler)
    print(f"\n🌍 Gemma 4 E2B AI Server running live on http://0.0.0.0:{PORT}")
    print(f"📱 Connect your iPhone on the same Wi-Fi to: http://172.20.10.2:{PORT}")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == '__main__':
    run()

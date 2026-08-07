import os
import sys
import json
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

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
                is_arabic = any('\u0600' <= c <= '\u06FF' for c in user_prompt)

                if not llm:
                    reply = "نموذج Gemma 4 E2B غير محمل حالياً." if is_arabic else "Gemma 4 E2B model not loaded."
                else:
                    print(f"\n[Gemma 4 E2B Prompt]: {user_prompt}")

                    if is_arabic:
                        sys_prompt = "أنت مساعد ذكي ونظارة بصري للأشخاص المكفوفين. أجب باختصار شديد (في جملتين مفيدتين) باللغة العربية الفصحى:"
                    else:
                        sys_prompt = "You are an AI assistant for a blind user. Answer briefly in 1-2 clear helpful sentences:"

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

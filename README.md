# 🕶️ AI Glasses — Multimodal Local AI for Smart Glasses (iOS)

> **Academic Project & Technical Documentation**  
> **Developer**: Wajd Moussi  
> **Platform**: Native iOS Application (Built with Python, BeeWare Toga, and Gemma 4 E2B)

---

## 📌 1. Project Overview & Objectives

**AI Glasses** is an innovative edge-computing application designed for smart glasses and mobile devices. It runs a **multimodal local Artificial Intelligence model** directly on the user's device without requiring active internet connectivity or cloud servers.

### Key Objectives:
1. **Privacy & Offline First**: Zero cloud dependency — all text, vision, and audio processing remain 100% local on-device.
2. **Multimodal Capability**: Seamless processing of **Text**, **Vision (Camera)**, and **Voice (Microphone)** input streams.
3. **Cross-Platform Python Architecture**: Developed using **BeeWare Toga**, compiled directly into native iOS Objective-C / Swift runtime via Xcode build tools.

---

## 🏗️ 2. System Architecture

```
┌────────────────────────────────────────────────────────┐
│                     USER INTERFACE                     │
│           (Native iOS Toga UI / Dynamic Layout)        │
└───────────┬──────────────────┬──────────────────┬──────┘
            │                  │                  │
   📷 Camera Feed       🎤 Audio Input      💬 Text Input
            │                  │                  │
┌───────────▼──────────────────▼──────────────────▼──────┐
│                  CONTROLLER / LOGIC                    │
│                (src/ai_glasses/app.py)                 │
└──────────────────────────┬─────────────────────────────┘
                           │ Async Handler (asyncio)
┌──────────────────────────▼─────────────────────────────┐
│                 MULTIMODAL AI ENGINE                   │
│            (src/ai_glasses/model_handler.py)           │
│                                                        │
│        🧠 Gemma 4 E2B Model (Quantized GGUF)           │
│           Core Engine: llama-cpp-python                │
└────────────────────────────────────────────────────────┘
```

---

## 💻 3. Codebase Components & Explanation

### 📄 `pyproject.toml`
Defines project metadata, dependencies, custom icon specifications, and **iOS native permissions** (`NSCameraUsageDescription` and `NSMicrophoneUsageDescription`).

### 📄 `src/ai_glasses/app.py`
The primary User Interface (UI) built with Toga.
- Uses asynchronous event handling (`asyncio.to_thread`) to execute heavy GGUF inference in worker threads without freezing the main UI thread.
- Includes defensive error boundaries (`try/except`) to ensure zero-crash startup on physical iOS devices.

### 📄 `src/ai_glasses/model_handler.py`
Interfaces with the `llama-cpp-python` engine and manages the `Gemma-4-E2B.gguf` multimodal model lifecycle (loading, vision analysis, speech processing, and text generation).

### 📄 `src/ai_glasses/resources/ai_glasses.png`
Custom high-resolution (1024x1024) PNG application icon depicting futuristic glowing AI smart glasses.

---

## ⚙️ 4. CI/CD & Automated iOS Cloud Build

Due to iOS development requiring macOS and Xcode, the project uses an automated **GitHub Actions CI/CD pipeline** (`.github/workflows/build_ios.yml`):

1. **Linux Syntax Validation**: Fast syntax verification step running on Ubuntu runners.
2. **macOS Apple Silicon Runner (`macos-14`)**: Installs Python 3.11, Briefcase, Toga, and Pillow.
3. **AppIcon Generation**: Pillow resizes the custom PNG logo into native Apple `AppIcon.appiconset`.
4. **Physical Device Build**: Executes `briefcase build iOS -d` targeting physical ARM64 iPhone devices (`iphoneos` SDK).
5. **Artifact Packaging**: Exports the resulting binary package ready for sideloading.

---

## 📲 5. Device Deployment (Windows to iPhone)

Since the build is compiled for physical ARM64 iPhones, it can be deployed from Windows without a Mac:

1. Download **`AI-Glasses-iOS-App.zip`** from GitHub Actions Artifacts.
2. Extract the archive and place the app folder inside a directory named **`Payload`**.
3. Compress the `Payload` directory into a `.zip` archive and rename its extension to **`.ipa`** (`AI Glasses.ipa`).
4. Open **3uTools** (or **Sideloadly**), go to **Toolbox → IPA Signature**, sign with your Apple ID, and install it to the iPhone.
5. On the iPhone: Go to **Settings → General → VPN & Device Management** and tap **Trust**.
6. Ensure **Developer Mode** is enabled on iOS (`Settings → Privacy & Security → Developer Mode`).

---

## 🎓 6. Technologies & Credits

- **UI Framework**: [BeeWare Toga](https://beeware.org/)
- **AI Inference Engine**: [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- **Model Family**: Google Gemma 4 E2B Multimodal GGUF
- **CI/CD Pipeline**: GitHub Actions (macOS 14 ARM64)

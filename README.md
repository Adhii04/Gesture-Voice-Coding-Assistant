
# 🖐️🎤 Gesture-Voice-Coding-Assistant

A gesture-controlled mouse and voice-driven typing system that enables hands-free cursor control and text input using computer vision and speech recognition.  
Designed for touchless interaction, accessibility, and keyboard-free coding.

---

## 🚀 Features

- 🖱️ Gesture-controlled mouse movement using index finger  
- 👆 Click action using index + thumb pinch  
- 🎤 Voice-controlled typing activated via index + pinky gesture  
- ⌨️ Command-aware continuous voice dictation  
- 🧠 State-based control to prevent gesture–voice conflicts  

---

## 🧩 How It Works

1. Webcam captures real-time hand movements  
2. MediaPipe detects and tracks hand landmarks  
3. Gestures control cursor movement and clicks  
4. A voice assistant is triggered using a gesture  
5. Speech is converted to text and typed into the active input field  

---

## 🛠️ Tech Stack

- Python 3.11  
- OpenCV  
- MediaPipe  
- PyAutoGUI  
- SpeechRecognition  
- PyAudio  
- pyttsx3  

---

## 📦 Installation

### Clone the repository
```bash
git clone https://github.com/your-username/hands-free-coding-assistant.git
cd hands-free-coding-assistant
```
### Create and activate virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate
```
### Install dependencies
```bash
pip install opencv-python mediapipe pyautogui SpeechRecognition pyttsx3
pip install pipwin
pipwin install pyaudio
```
## ▶️ Usage

1. Run the program:
```bash
python GestureControl.py
```

2. Move cursor using your index finger  
3. Click using index + thumb pinch  
4. Start voice assistant using index + pinky gesture  
5. Assistant says:    
    “Yes, tell me. What should I type for you?”  
6. Speak commands like:  
```bash
type hello world
space
full stop
```
7.Say end or stop assistant to stop voice mode  

## 🎯 Use Cases  
- Hands-free coding and text entry  
- Accessibility for users with limited motor control  
- Touchless computer interaction  
- Human–Computer Interaction (HCI) research demos  

## 📌 Future Enhancements  
- Code-specific commands (indent, new line, tab)  
- Visual on-screen status indicator  
- Offline speech recognition  
- Multi-language voice support  

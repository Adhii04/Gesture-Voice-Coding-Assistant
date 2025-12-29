import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import pyttsx3
import math
import time

pyautogui.FAILSAFE = False

# -------------------- TEXT TO SPEECH -------------------
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# -------------------- COMMAND MAP ----------------paper ----
COMMANDS = {
    "space": lambda: pyautogui.press("space"),
    "space bar": lambda: pyautogui.press("space"),
    "enter": lambda: pyautogui.press("enter"),

    "backspace": lambda: pyautogui.press("backspace"),
    "back space": lambda: pyautogui.press("backspace"),

    "full stop": lambda: pyautogui.write("."),
    "semicolon": lambda: pyautogui.write(";"),
    "colon": lambda: pyautogui.write(":"),
    "comma": lambda: pyautogui.write(","),

    "parenthesis open": lambda: pyautogui.write("("),
    "parenthesis close": lambda: pyautogui.write(")"),

    "equal to": lambda: pyautogui.write("="),
    "plus": lambda: pyautogui.write("+"),
    "minus": lambda: pyautogui.write("-"),
    "slash": lambda: pyautogui.write("/"),

    # 🔹 Quotes
    "double quote": lambda: pyautogui.write('"'),
    "double quotation": lambda: pyautogui.write('"'),
    "single quote": lambda: pyautogui.write("'"),
    "single quotation": lambda: pyautogui.write("'"),
}


# -------------------- PROCESS VOICE INPUT --------------------
def process_voice(text):
    global typing_mode

    text = text.lower().strip()

    # STOP assistant
    if text == "stop assistant" or text == "end":
        return "STOP"

    # CASE 1: "type something"  ← THIS WAS MISSING
    if text.startswith("type "):
        typing_mode = True
        to_type = text.replace("type ", "", 1)
        pyautogui.write(to_type + " ", interval=0.05)
        return "TYPED"

    # CASE 2: "type" alone
    if text == "type":
        typing_mode = True
        print("Typing mode ON")
        return "TYPE_MODE"

    executed = False
    used = set()

    # Execute command words (longest first)
    for command in sorted(COMMANDS, key=len, reverse=True):
        if command in text and command not in used:
            COMMANDS[command]()
            used.add(command)
            executed = True

    # If typing mode is ON, type whatever is spoken
    if typing_mode and not executed:
        pyautogui.write(text + " ", interval=0.05)
        return "TYPED"

    if executed:
        return "COMMAND"

    print("Ignored:", text)
    return "IGNORED"

# -------------------- VOICE TYPING MODE --------------------
def voice_typing_mode():
    global assistant_active, typing_mode

    r = sr.Recognizer()
    speak("Yes, tell me. What should I type for you?")

    typing_mode = False   # reset on entry

    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("Heard:", text)

            if process_voice(text) == "STOP":
                speak("Stopping assistant")
                break

        except:
            speak("Please say again")

    typing_mode = False
    assistant_active = False

# -------------------- GESTURE DETECTION --------------------
def index_pinky_up(hand):
    index_up = hand.landmark[8].y < hand.landmark[6].y
    pinky_up = hand.landmark[20].y < hand.landmark[18].y

    middle_down = hand.landmark[12].y > hand.landmark[10].y
    ring_down = hand.landmark[16].y > hand.landmark[14].y

    return index_up and pinky_up and middle_down and ring_down

# -------------------- INITIALIZE --------------------
cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

PINCH_THRESHOLD = 0.03
last_click = 0
assistant_active = False

# -------------------- MAIN LOOP --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            index_tip = hand.landmark[8]
            thumb_tip = hand.landmark[4]

            # Move cursor
            pyautogui.moveTo(
                int(index_tip.x * screen_w),
                int(index_tip.y * screen_h)
            )

            # Pinch click
            distance = math.hypot(
                index_tip.x - thumb_tip.x,
                index_tip.y - thumb_tip.y
            )

            if distance < PINCH_THRESHOLD and time.time() - last_click > 0.7:
                pyautogui.click()
                last_click = time.time()

            # Voice assistant gesture
            if index_pinky_up(hand) and not assistant_active:
                assistant_active = True
                voice_typing_mode()
                assistant_active = False

    cv2.imshow("Gesture Mouse + Voice Assistant", frame)

    if cv2.waitKey(1) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()

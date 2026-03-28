import os
import time
import cv2
import mediapipe as mp
import pyttsx3
import json
import math

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# -------------------- TTS --------------------
engine = pyttsx3.init()
def speak(text):
    if text:
        engine.say(text)
        engine.runAndWait()

# -------------------- Load dictionary --------------------
with open("dictionary.json", "r") as f:
    words = json.load(f)

def predict_word(current_string):
    suggestions = [w for w in words if w.startswith(current_string.lower())]
    return suggestions[0] if suggestions else current_string

# -------------------- Letters --------------------
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
letter_positions = {}
start_x, start_y = 20, 20
box_size = 60        # smaller box
letters_per_row = 7

for i, letter in enumerate(letters):
    x1 = start_x + (i % letters_per_row) * box_size
    y1 = start_y + (i // letters_per_row) * box_size
    x2, y2 = x1 + box_size, y1 + box_size
    letter_positions[letter] = (x1, y1, x2, y2)

# -------------------- Buttons --------------------
rows = (len(letters) - 1) // letters_per_row + 1
button_y_start = start_y + rows * box_size + 50   # move buttons further down
buttons = {
    "CLEAR": (20, button_y_start, 160, button_y_start + 50),
    "FINISH": (200, button_y_start, 360, button_y_start + 50),
    "EXIT": (400, button_y_start, 560, button_y_start + 50)
}

# -------------------- MediaPipe Hands --------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, model_complexity=0)
mp_draw = mp.solutions.drawing_utils

# -------------------- Camera --------------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cv2.namedWindow("Sign Language Predictor", cv2.WINDOW_NORMAL)

# -------------------- State --------------------
current_string = ""
predicted_word = ""
last_tap_time = 0
tap_cooldown = 0.5
hover_box = None
hover_start_time = 0

# -------------------- Helper functions --------------------
def is_pointing_index(handLms):
    index_up = handLms.landmark[8].y < handLms.landmark[6].y
    others_down = (
        handLms.landmark[12].y > handLms.landmark[10].y and
        handLms.landmark[16].y > handLms.landmark[14].y and
        handLms.landmark[20].y > handLms.landmark[18].y
    )
    return index_up and others_down

def is_tap(handLms, h, w):
    ix, iy = int(handLms.landmark[8].x * w), int(handLms.landmark[8].y * h)
    tx, ty = int(handLms.landmark[4].x * w), int(handLms.landmark[4].y * h)
    dist = math.hypot(ix - tx, iy - ty)
    return dist < 30, ix, iy

# -------------------- Main Loop --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    # Draw letters
    for letter, (x1, y1, x2, y2) in letter_positions.items():
        color = (0, 255, 0)
        if hover_box == letter:
            color = (0, 255, 255)  # highlight
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, letter, (x1 + 12, y1 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2)

    # Draw buttons
    for btn, (x1, y1, x2, y2) in buttons.items():
        color = (0, 0, 255)
        if hover_box == btn:
            color = (0, 255, 255)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, -1)
        cv2.putText(frame, btn, (x1 + 10, y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

    # Hand detection & tap
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            tap, x_tip, y_tip = is_tap(handLms, h, w)
            cv2.circle(frame, (x_tip, y_tip), 6, (255, 0, 0), -1)

            current_box = None
            # Check buttons first
            for btn, (x1, y1, x2, y2) in buttons.items():
                if x1 < x_tip < x2 and y1 < y_tip < y2:
                    current_box = btn
                    break
            # Check letters if no button hovered
            if not current_box:
                for letter, (x1, y1, x2, y2) in letter_positions.items():
                    if x1 < x_tip < x2 and y1 < y_tip < y2:
                        current_box = letter
                        break

            # Hover highlight
            if current_box != hover_box:
                hover_box = current_box
                hover_start_time = time.time()

            # Tap selection
            if current_box and tap:
                now = time.time()
                if now - last_tap_time > tap_cooldown:
                    # Letters require pointing
                    if current_box in letters and is_pointing_index(handLms):
                        current_string += current_box
                        predicted_word = predict_word(current_string)
                    # Buttons do not require pointing
                    elif current_box == "CLEAR":
                        if current_string:
                            current_string = current_string[:-1]
                            predicted_word = predict_word(current_string)
                    elif current_box == "FINISH":
                        predicted_word = predict_word(current_string)
                        speak(predicted_word)
                    elif current_box == "EXIT":
                        cap.release()
                        cv2.destroyAllWindows()
                        exit()
                    last_tap_time = now

    # Display typed & predicted words
    cv2.putText(frame, f"Typed: {current_string}", (20, button_y_start + 90),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
    cv2.putText(frame, f"Prediction: {predicted_word}", (20, button_y_start + 140),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)

    cv2.imshow("Sign Language Predictor", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

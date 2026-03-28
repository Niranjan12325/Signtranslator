## Sign Language Predictor (Hand Gesture Typing System)
## Overview

This project is a real-time Sign Language Predictor that allows users to type letters using hand gestures and convert them into meaningful words with text-to-speech output.

It uses computer vision and hand tracking to detect finger movements and simulate a virtual keyboard.

## Features
- Hand gesture-based typing using webcam
- Virtual keyboard (A–Z letters)
- Word prediction using dictionary
- Text-to-Speech output
- Clear last character option
- Finish & speak full word
- Exit functionality
- Tap detection using finger distance

## Technologies Used
- Python
- OpenCV
- MediaPipe
- pyttsx3
📂 Project Structure
   SignLanguagePredictor/
    │
    ├── main.py                # Main application file
    ├── dictionary.json       # Word dictionary for prediction
    ├── README.md             # Project documentation
## Installation
1️. Clone the Repository
git clone https://github.com/your-username/sign-language-predictor.git
cd sign-language-predictor
2️. Install Dependencies
pip install opencv-python mediapipe pyttsx3
3. How to Run
python main.py
4. How It Works
- 📷 Webcam captures your hand
- 🧠 MediaPipe detects hand landmarks
- 👆 Index finger acts as pointer
- 🤏 Thumb + index finger = TAP action
- ⌨️ Tap on virtual keyboard to type
- 🔮 System predicts word using dictionary
- 🔊 Press FINISH to speak output
- 🧠 Gesture Controls
Gesture	Action
- 👆 Pointing Index Finger	Select letters
- 🤏 Thumb + Index Close	Tap
- 🧹 CLEAR Button	Delete last letter
- ✅ FINISH Button	Speak predicted word
- ❌ EXIT Button	Close application

## Output Example
- Typed: HEL
- Prediction: HELLO
- Speech Output:  "Hello"

## Future Improvements
- Add full sign language recognition (not just virtual keyboard)
- Improve prediction using NLP models
- Add sentence formation
- Deploy as web app using Django/Flask
- Mobile app version
 
## Acknowledgements
- Google for MediaPipe
- Open-source computer vision community

## Author
Niranjan E

⭐ If you like this project
Give it a ⭐ on GitHub and share!

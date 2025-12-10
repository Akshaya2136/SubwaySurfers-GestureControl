🎮 Hand Gesture Controlled Subway Surfers

Control Subway Surfers using your hand gestures through your webcam!
This project uses MediaPipe + OpenCV + Python + Pynput to detect your hand movements and trigger game actions like left, right, jump, and duck.

🚀 Features

 🖐️ Real-time hand tracking

 🎯 Detects gestures for:

   Move Left

   Move Right

   Jump

   Duck

 🎮 Controls Subway Surfers through keyboard emulation

 📷 Simple webcam-based interface

 ⚡ Lightweight and fast (runs on CPU)
 
 🛠️ Technologies Used

Python

OpenCV

MediaPipe

Pynput

TensorFlow Lite (MediaPipe backend)

▶️ How to Run

1️⃣ Create and activate environment

conda create -n subway python=3.10 -y

conda activate subway

2️⃣ Install requirements

pip install opencv-python mediapipe pynput

3️⃣ Run the program

python gesture_subway.py

Your webcam will open → show your hand → start controlling the game.


🕹️ Gestures & Actions
| Gesture                             | Action     |
| ----------------------------------- | ---------- |
| Hand moves left                     | Move Left  |
| Hand moves right                    | Move Right |
| Full open palm                      | Jump       |
| pinky extended (hang loose)         | Duck       |

🧠 How It Works

MediaPipe Hands detects 21 landmarks on your hand

Landmark positions determine:

Horizontal movement → lane switching

Finger extension → jump & duck

Pynput simulates keyboard presses

Your gestures control the Subway Surfers player in real time

🧧 Future Enhancements

Add swipe-like gestures

Add calibration mode

Improve gesture accuracy

Add support for other games

🤝 Contributions

Pull requests are welcome!

If you'd like to add custom gestures or improve accuracy, feel free to contribute.

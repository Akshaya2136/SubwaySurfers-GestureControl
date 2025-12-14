# 🎮 Hand Gesture Controlled Subway Surfers

Control Subway Surfers using your hand gestures through a webcam.
This project uses MediaPipe, OpenCV, Python, and Pynput to detect hand movements and convert them into in-game actions such as left, right, jump, and duck.

---

## 🚀 Features

- 🖐️ Real-time hand tracking
- 🎯 Gesture detection for:
  - Move Left
  - Move Right
  - Jump
  - Duck
- 🎮 Controls the game using keyboard emulation
- 📷 Webcam-based interface (no extra hardware needed)
- ⚡ Lightweight and fast (CPU only)

---

## 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- Pynput
- TensorFlow Lite (MediaPipe backend)

---

## ▶️ How to Run

### Clone or download the repository
```bash
git clone https://github.com/Akshaya2136/SubwaySurfers-GestureControl.git
```
then
```bash
cd SubwaySurfers-GestureControl
```

### Create and activate a virtual environment:
```bash
conda create -n subway python=3.10 -y
conda activate subway
```
### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the program:
```bash
python gesture_subway.py
```

Your webcam will open. Show your hand to start controlling the game.

## 🕹️ Gestures & Actions

| Gesture                     | Action     |
|-----------------------------|------------|
| Hand moves left             | Move Left  |
| Hand moves right            | Move Right |
| Fully open palm             | Jump       |
| Pinky extended (hang loose) | Duck       |

---

## 🧠 How It Works

- MediaPipe Hands detects **21 hand landmarks**
- Landmark positions are analyzed to determine:
  - Horizontal hand movement → lane switching
  - Finger extension → jump and duck
- Pynput simulates keyboard key presses
- Gestures are mapped to in-game actions in real time

---

## 🧧 Future Enhancements

- Swipe-based gesture support
- Calibration mode for different hand sizes
- Improved gesture accuracy
- Support for other games

---

## 🤝 Contributions

Pull requests are welcome.  
If you'd like to add new gestures, improve accuracy, or extend support to other games, feel free to contribute.

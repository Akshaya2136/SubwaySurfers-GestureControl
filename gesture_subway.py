# -------------------------------------------
# IMPORT REQUIRED LIBRARIES
# -------------------------------------------

import cv2                             # For webcam video processing
import mediapipe as mp                 # For detecting hand & finger landmarks
from pynput.keyboard import Key, Controller   # For simulating keyboard presses
import time
import math

# -------------------------------------------
# INITIAL SETUP
# -------------------------------------------

keyboard = Controller()                # Allows sending keyboard key presses

mp_drawing = mp.solutions.drawing_utils    # For drawing hand landmarks on screen
mp_hands = mp.solutions.hands             # Hand-tracking model

# Initialize the hand detection model
hands = mp_hands.Hands(
    static_image_mode=False,              # Video mode → continuous tracking
    max_num_hands=1,                      # Only track 1 hand
    min_detection_confidence=0.3,
    min_tracking_confidence=0.3
)

# Start webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

pTime = 0                             # For FPS calculation
active_action = "Idle"                # What action is currently happening?

# -------------------------------------------
# GESTURE STATE MEMORY  
# (Prevents repeating key presses too fast)
# -------------------------------------------

gesture_state = {
    'move_left': False,
    'move_right': False,
    'jump': False,
    'duck': False
}

# Lane detection X-axis boundaries  
LEFT_LANE_BOUND = 0.33
RIGHT_LANE_BOUND = 0.63

# Landmark indices for finger tips
FINGER_TIPS = [
    mp_hands.HandLandmark.THUMB_TIP,
    mp_hands.HandLandmark.INDEX_FINGER_TIP,
    mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
    mp_hands.HandLandmark.RING_FINGER_TIP,
    mp_hands.HandLandmark.PINKY_TIP
]

# -------------------------------------------
# FUNCTION: Press and release a keyboard key
# -------------------------------------------

def press_and_release(key_code):
    """Sends a quick keyboard press (like tapping a key)."""
    keyboard.press(key_code)
    keyboard.release(key_code)

# -------------------------------------------
# FUNCTION: Count which fingers are extended
# -------------------------------------------

def count_extended_fingers(landmarks):
    """
    Returns a list of 5 booleans indicating which fingers are extended.
    Order: [Thumb, Index, Middle, Ring, Pinky]
    """
    extended_fingers = [False] * 5

    # Thumb check (compare tip and MCP positions)
    if landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y < \
       landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y:
        extended_fingers[0] = True

    # Check other four fingers
    for i in range(1, 5):
        tip_id = FINGER_TIPS[i].value
        pip_id = tip_id - 2             # PIP joint is always 2 positions before tip

        if landmarks.landmark[tip_id].y < landmarks.landmark[pip_id].y:
            extended_fingers[i] = True

    return extended_fingers

# -------------------------------------------
# MAIN LOOP – Read webcam frame-by-frame
# -------------------------------------------

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    image = cv2.flip(image, 1)       # Mirror the video (more natural control)

    h, w, c = image.shape
    image.flags.writeable = False    # Speed optimization for mediapipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    image.flags.writeable = True

    # Reset current action every frame
    current_action = {
        'move_left': False,
        'move_right': False,
        'jump': False,
        'duck': False
    }

    # -------------------------------------------
    # HAND DETECTION & GESTURE LOGIC
    # -------------------------------------------

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]

        # Get thumb tip & index tip coordinates
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Calculate horizontal center between thumb & index
        center_x = (thumb_tip.x + index_tip.x) / 2

        # Determine which fingers are extended
        extended = count_extended_fingers(hand_landmarks)

        # Draw hand skeleton
        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # -------------------------------------------
        # MOVEMENT LEFT / RIGHT BASED ON X POSITION
        # -------------------------------------------

        if center_x > RIGHT_LANE_BOUND:
            current_action['move_right'] = True

        elif center_x < LEFT_LANE_BOUND:
            current_action['move_left'] = True

        # -------------------------------------------
        # JUMP (open palm = all fingers extended)
        # -------------------------------------------

        if all(extended):
            current_action['jump'] = True

        # -------------------------------------------
        # DUCK (Hang Loose Sign: thumb + pinky only)
        # -------------------------------------------

        elif extended[0] and extended[4] and not extended[1] and not extended[2] and not extended[3]:
            current_action['duck'] = True

    # -------------------------------------------
    # EXECUTE ACTIONS BASED ON GESTURE
    # -------------------------------------------

    # MOVE RIGHT
    if current_action['move_right'] and not gesture_state['move_right']:
        press_and_release(Key.right)
        gesture_state['move_right'] = True
        active_action = "Move RIGHT (Press)"

    elif not current_action['move_right'] and gesture_state['move_right']:
        gesture_state['move_right'] = False

    # MOVE LEFT
    elif current_action['move_left'] and not gesture_state['move_left']:
        press_and_release(Key.left)
        gesture_state['move_left'] = True
        active_action = "Move LEFT (Press)"

    elif not current_action['move_left'] and gesture_state['move_left']:
        gesture_state['move_left'] = False

    # JUMP
    elif current_action['jump'] and not gesture_state['jump']:
        press_and_release(Key.up)
        gesture_state['jump'] = True
        active_action = "JUMP (Press)"

    elif not current_action['jump'] and gesture_state['jump']:
        gesture_state['jump'] = False

    # DUCK
    elif current_action['duck'] and not gesture_state['duck']:
        press_and_release(Key.down)
        gesture_state['duck'] = True
        active_action = "DUCK (Press)"

    elif not current_action['duck'] and gesture_state['duck']:
        gesture_state['duck'] = False

    # If any action is being held
    elif any(gesture_state.values()):
        for action, is_active in gesture_state.items():
            if is_active:
                active_action = f"{action.upper().replace('_', ' ')} (Held)"
                break
    else:
        active_action = "Idle (Middle Lane)"

    # -------------------------------------------
    # DISPLAY FPS & CURRENT ACTION ON SCREEN
    # -------------------------------------------

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(image, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.putText(image, f'Action: {active_action}', (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show final output window
    cv2.imshow('Subway Surfers Gesture Control', image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# -------------------------------------------
# CLEANUP
# -------------------------------------------

cap.release()
cv2.destroyAllWindows()

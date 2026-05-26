# Modules needed 
# (use pip install opencv-python mediapipe to install modules)

import cv2, math
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode

# Variables and lists needed (HAND_CONNECTIONS is necessary for Mediapipe's Tasks API)

X_COR = 100
Y_COR = 100
X_INCREMENT = 7
Y_INCREMENT = 7
DECAY = 0.0005
BALL_R = 50

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17),
]

# Functions for collision logic

def bounce(v):
    return -math.copysign(max(abs(v) - DECAY, 0), v)

def decay(v):
    return math.copysign(max(abs(v) - DECAY, 0), v)

def closest_point_on_segment(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return ax, ay
    t = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return ax + t * dx, ay + t * dy

# Setting up the hand landmarks. 
# Keep in mind that mediapipe.solutions is now deprecated, 
# so you must use mediapipe.tasks for hand landmarks

landmarker = HandLandmarker.create_from_options(HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="hand_landmarker.task"),
    running_mode=RunningMode.VIDEO,
    num_hands=2,
))

# Setting up the camera and frame

cam = cv2.VideoCapture(0)
if not cam: print("Error: couldn't connect camera...")

frame_idx = 0
while True:
    ret, frame = cam.read()
    if not ret:
        print("Error: frame not read. Exiting loop.")
        break

    # Creating ball, movement, x+y coordinate limits
    # and collision logic

    cv2.circle(frame, (int(X_COR), int(Y_COR)), BALL_R, (255, 0, 0), -1)
    X_COR += X_INCREMENT
    Y_COR += Y_INCREMENT

    if Y_COR >= 450 or Y_COR <= 50:
        Y_INCREMENT = bounce(Y_INCREMENT)

    if X_COR >= 600 and X_INCREMENT > 0 or X_COR <= 40 and X_INCREMENT < 0:
        X_INCREMENT = bounce(X_INCREMENT)

    # Displaying of landmarks and collision detection with them. 
    # Mediapipe expects an RGB image to work, so color conversion is a MUST

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    results = landmarker.detect_for_video(mp_image, frame_idx)
    frame_idx += 1

    h, w = frame.shape[:2]
    nearest_d = float("inf")
    nearest_cx = nearest_cy = 0.0
    for hand_lms in results.hand_landmarks:
        pts = [(int(lm.x * w), int(lm.y * h)) for lm in hand_lms]
        for a, b in HAND_CONNECTIONS:
            cv2.line(frame, pts[a], pts[b], (0, 255, 0), 2)
            cx, cy = closest_point_on_segment(X_COR, Y_COR, pts[a][0], pts[a][1], pts[b][0], pts[b][1])
            d = math.hypot(X_COR - cx, Y_COR - cy)
            if d < nearest_d:
                nearest_d, nearest_cx, nearest_cy = d, cx, cy
        for p in pts:
            cv2.circle(frame, p, 4, (0, 0, 255), -1)

    # Collision detection logic - looks for the 
    # closest landmark to the blue ball

    if nearest_d <= BALL_R:
        nx, ny = X_COR - nearest_cx, Y_COR - nearest_cy
        n_len = nearest_d if nearest_d > 1e-6 else 1.0
        nx, ny = nx / n_len, ny / n_len
        v_dot_n = X_INCREMENT * nx + Y_INCREMENT * ny
        if v_dot_n < 0:
            X_INCREMENT -= 2 * v_dot_n * nx
            Y_INCREMENT -= 2 * v_dot_n * ny
            X_INCREMENT = decay(X_INCREMENT)
            Y_INCREMENT = decay(Y_INCREMENT)
        overlap = BALL_R - nearest_d
        if overlap > 0:
            X_COR += nx * overlap
            Y_COR += ny * overlap

    # Displaying the webcam frames
    
    cv2.imshow("Annoying circle", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

import cv2 as cv
import numpy as np
import time

def create_background(cap, num_frames=30):
    print("Capturing background. Please move out of frame.")
    time.sleep(5)  # Give user time to move out of frame
    backgrounds = []
    for i in range(num_frames):
        ret, frame = cap.read()
        if ret:
            backgrounds.append(frame)
        else:
            print(f"Could not read the frame {i+1}/{num_frames}")
        time.sleep(0.1)
    if backgrounds:
        median_background = np.median(backgrounds, axis=0).astype(np.uint8)
        return median_background
    else:
        raise ValueError("Could not capture any frames for background")

def create_mask(frame, lower_color, upper_color):
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_color, upper_color)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask = cv.morphologyEx(mask, cv.MORPH_DILATE, np.ones((3,3), np.uint8))
    return mask

def apply_cloak_effect(frame, mask, background):
    mask_inv = cv.bitwise_not(mask)
    fg = cv.bitwise_and(frame, frame, mask=mask_inv)
    bg = cv.bitwise_and(background, background, mask=mask)
    return cv.add(fg, bg)

def main():
    print("OpenCV version:", cv.__version__)
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Error opening the camera.")
        return

    try:
        background = create_background(cap)
    except Exception as e:
        print(f"Error loading the background: {e}")
        cap.release()
        return

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    print("Starting main loop. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            time.sleep(1)
            continue

        frame = cv.flip(frame, 1) 

        mask = create_mask(frame, lower_blue, upper_blue)
        result = apply_cloak_effect(frame, mask, background)

        cv.imshow("Invisibility Cloak", result)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()

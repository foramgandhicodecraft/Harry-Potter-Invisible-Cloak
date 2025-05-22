How It Works
Background Capture: The script first captures the background for a few seconds while the user is out of the frame.

Color Detection: It detects a specific cloak color (default: blue) using HSV color segmentation.

Masking and Replacement: The cloak area is masked and replaced with the pre-captured background, giving the illusion of invisibility.

 Tech Stack
Python

OpenCV

NumPy

Customization
If you're using a different colored cloak (e.g., red or green), adjust the lower_color and upper_color HSV ranges in the code:
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([130, 255, 255])


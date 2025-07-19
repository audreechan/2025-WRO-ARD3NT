import cv2
import numpy as np

def nothing(x):
    pass

# Load image
image_path = "test_mask4.png"  # Replace with your actual image path
image = cv2.imread(image_path)
if image is None:
    print("Image not found.")
    exit()

# Resize for consistency
image = cv2.resize(image, (640, 480))
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create window
cv2.namedWindow("Dark Blue/Black Mask Tuner")

# Trackbars for HSV bounds
cv2.createTrackbar("Low H", "Dark Blue/Black Mask Tuner", 100, 180, nothing)
cv2.createTrackbar("High H", "Dark Blue/Black Mask Tuner", 130, 180, nothing)
cv2.createTrackbar("Low S", "Dark Blue/Black Mask Tuner", 50, 255, nothing)
cv2.createTrackbar("High S", "Dark Blue/Black Mask Tuner", 255, 255, nothing)
cv2.createTrackbar("Low V", "Dark Blue/Black Mask Tuner", 0, 255, nothing)
cv2.createTrackbar("High V", "Dark Blue/Black Mask Tuner", 100, 255, nothing)

while True:
    # Get trackbar positions
    lh = cv2.getTrackbarPos("Low H", "Dark Blue/Black Mask Tuner")
    hh = cv2.getTrackbarPos("High H", "Dark Blue/Black Mask Tuner")
    ls = cv2.getTrackbarPos("Low S", "Dark Blue/Black Mask Tuner")
    hs = cv2.getTrackbarPos("High S", "Dark Blue/Black Mask Tuner")
    lv = cv2.getTrackbarPos("Low V", "Dark Blue/Black Mask Tuner")
    hv = cv2.getTrackbarPos("High V", "Dark Blue/Black Mask Tuner")

    # Mask creation
    lower = np.array([lh, ls, lv])
    upper = np.array([hh, hs, hv])
    mask = cv2.inRange(hsv, lower, upper)

    # Create white background
    white_bg = np.ones_like(image, dtype=np.uint8) * 255

    # Blend the image with white background based on mask
    result = np.where(mask[:, :, None] == 255, image, white_bg)

    # Show side by side
    stacked = np.hstack((image, result))

    cv2.imshow("Dark Blue/Black Mask Tuner", stacked)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to quit
        break

cv2.destroyAllWindows()
print(f"lower_red1 = {lower}, upper_red1 = {upper}")
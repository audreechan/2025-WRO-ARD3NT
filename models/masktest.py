import cv2
import numpy as np

def nothing(x):
    pass

# Load image
image_path = "test_mask2.png"  # Replace with your image filename
image = cv2.imread(image_path)
if image is None:
    print("Image not found.")
    exit()

# Resize for visibility (optional)
image = cv2.resize(image, (640, 480))

# Convert to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create window
cv2.namedWindow("Red Mask Tuner")

# Create trackbars for HSV bounds
cv2.createTrackbar("Low H1", "Red Mask Tuner", 0, 180, nothing)
cv2.createTrackbar("High H1", "Red Mask Tuner", 10, 180, nothing)
cv2.createTrackbar("Low H2", "Red Mask Tuner", 160, 180, nothing)
cv2.createTrackbar("High H2", "Red Mask Tuner", 180, 180, nothing)
cv2.createTrackbar("Low S", "Red Mask Tuner", 100, 255, nothing)
cv2.createTrackbar("High S", "Red Mask Tuner", 255, 255, nothing)
cv2.createTrackbar("Low V", "Red Mask Tuner", 100, 255, nothing)
cv2.createTrackbar("High V", "Red Mask Tuner", 255, 255, nothing)

while True:
    # Get current positions
    lh1 = cv2.getTrackbarPos("Low H1", "Red Mask Tuner")
    hh1 = cv2.getTrackbarPos("High H1", "Red Mask Tuner")
    lh2 = cv2.getTrackbarPos("Low H2", "Red Mask Tuner")
    hh2 = cv2.getTrackbarPos("High H2", "Red Mask Tuner")
    ls = cv2.getTrackbarPos("Low S", "Red Mask Tuner")
    hs = cv2.getTrackbarPos("High S", "Red Mask Tuner")
    lv = cv2.getTrackbarPos("Low V", "Red Mask Tuner")
    hv = cv2.getTrackbarPos("High V", "Red Mask Tuner")

    # Create red masks (two ranges for wraparound)
    lower_red1 = np.array([lh1, ls, lv])
    upper_red1 = np.array([hh1, hs, hv])
    lower_red2 = np.array([lh2, ls, lv])
    upper_red2 = np.array([hh2, hs, hv])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Apply mask to original image
    result = cv2.bitwise_and(image, image, mask=mask)

    # Stack original and result for comparison
    stacked = np.hstack((image, result))

    # Show
    cv2.imshow("Red Mask Tuner", stacked)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to exit
        break

cv2.destroyAllWindows()
print(f"lower_red1 = {lower_red1}, upper_red1 = {upper_red1}")
print(f"lower_red2 = {lower_red2}, upper_red2 = {upper_red2}")

import time
from piracer.vehicles import PiRacerPro
from ultralytics import YOLO
import cv2
import numpy as np
from picamera2 import Picamera2

#Change to use piracer camera later
def prendre_image(camera):
    if camera is not None:
        image = camera.capture_array()
        if image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

        # Convert RGB to BGR for OpenCV processing
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Optionally flip the image vertically
        image = cv2.flip(image, 0)
        return image
    # Load the image
    image_path = "test.png"
    image = cv2.imread(image_path)
    return image
#Detects far away objects so that the car can adjust to face them
def trouver(image):
    image_height, image_width = image.shape[:2]
    image_center_x = image_width // 2

    # Focus on bottom 60% of the image
    start_y = int(image_height * 0.4)
    end_y = int(image_height * 0.55)
    roi = image[start_y:end_y, :]

    # Draw a rectangle around ROI
    cv2.rectangle(image, (0, start_y), (image_width - 1, end_y - 1), (255, 0, 0), 3)

    # Convert ROI to HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Red mask
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    red_mask = cv2.bitwise_or(
        cv2.inRange(hsv, lower_red1, upper_red1),
        cv2.inRange(hsv, lower_red2, upper_red2)
    )

    # Green mask
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours for both colors
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find largest red or green contour
    largest_contour = None
    largest_area = 0
    color = "none"
    centroid_x = -1

    for cnt, col in [(red_contours, "red"), (green_contours, "green")]:
        if cnt:
            biggest = max(cnt, key=cv2.contourArea)
            area = cv2.contourArea(biggest)
            if area > largest_area:
                largest_area = area
                largest_contour = (biggest, col)

    # Draw and compute centroid
    if largest_contour:
        cnt, color = largest_contour
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"]) + start_y  # offset to image coords
            centroid_x = cx

            # Draw centroid
            cv2.circle(image, (cx, cy), 5, (0, 255, 255), -1)
            cv2.putText(image, f"{color} center", (cx + 5, cy - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            print(f"{color.title()} centroid at: ({cx}, {cy})")
        else:
            print(f"{color.title()} blob found but area was zero")
    else:
        print("No red or green blobs detected")

    # Save debug image
    output_path = "high_mask.jpg"
    cv2.imwrite(output_path, image)
    print(f"Saved image with centroid to '{output_path}'")
    return {
        "size": largest_area,
        "color": color,
        "position": max(-1.0, min(1.0, (centroid_x - image_center_x) / (image_width / 2))) if centroid_x != -1 else "none"  # this is the x-coordinate or "none"
    }
#Detects closer objects so that the car can pass them correctly
def gauche_ou_droit_alt(image):
    image_height, image_width = image.shape[:2]
    image_center_x = image_width // 2

    # Focus on bottom 60% of the image
    start_y = int(image_height * 0.55)
    start_x = int(image_width * 0.1)
    end_x = int(image_width * 0.9)
    roi = image[start_y:, start_x:end_x]

    # Draw a rectangle around ROI
    cv2.rectangle(image, (start_x, start_y), (end_x - 1, image_height - 1), (255, 0, 0), 3)

    # Convert ROI to HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Red mask
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    red_mask = cv2.bitwise_or(
        cv2.inRange(hsv, lower_red1, upper_red1),
        cv2.inRange(hsv, lower_red2, upper_red2)
    )

    # Green mask
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours for both colors
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find largest red or green contour
    largest_contour = None
    largest_area = 0
    color = "none"
    centroid_x = -1

    for cnt, col in [(red_contours, "red"), (green_contours, "green")]:
        if cnt:
            biggest = max(cnt, key=cv2.contourArea)
            area = cv2.contourArea(biggest)
            if area > largest_area:
                largest_area = area
                largest_contour = (biggest, col)

    # Draw and compute centroid
    if largest_contour:
        cnt, color = largest_contour
        M = cv2.moments(cnt)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"]) + start_y  # offset to image coords
            centroid_x = cx

            # Draw centroid
            cv2.circle(image, (cx, cy), 5, (0, 255, 255), -1)
            cv2.putText(image, f"{color} center", (cx + 5, cy - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            print(f"{color.title()} centroid at: ({cx}, {cy})")
        else:
            print(f"{color.title()} blob found but area was zero")
    else:
        print("No red or green blobs detected")

    # Save debug image
    output_path = "low_mask.jpg"
    cv2.imwrite(output_path, image)
    print(f"Saved image with centroid to '{output_path}'")

    return {
        "size": largest_area,
        "color": color,
        "position": max(-1.0, min(1.0, (centroid_x - image_center_x) / (image_width / 2))) if centroid_x != -1 else "none"  # this is the x-coordinate or "none"
    }
#Tell if obstacle is on the left or right, and if it is red or green, and its size
def gauche_ou_droit(model, image):
    image_height, image_width = image.shape[:2]
    image_center_x = image_width // 2

    # Run inference
    results = model(image)[0]

    # COCO class ID for "car" is 2, bowl is 51
    car_class_id = 41

    largest_box = None
    largest_area = 0

    # Iterate over detections
    for box in results.boxes:
        cls = int(box.cls[0])
        if cls == car_class_id:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box
            conf = float(box.conf[0])              # Confidence
            print(f"Car detected: ({x1}, {y1}) to ({x2}, {y2}) | Confidence: {conf:.2f}")
            # Compute center of bounding box
            box_center_x = (x1 + x2) // 2

            # Choose color based on box position relative to image center
            if box_center_x > image_center_x:
                color = (0, 0, 255)  # Red (Right of center)
            else:
                color = (0, 255, 0)  # Green (Left of center)

            # Draw bounding box and label
            cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            label = f"Cup {conf:.2f}"
            cv2.putText(image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            area = (x2 - x1) * (y2 - y1)
            if area > largest_area:
                largest_area = area
                largest_box = (x1, y1, x2, y2)
    if largest_box:
        x1, y1, x2, y2 = largest_box
        # Draw a blue rectangle over the largest box
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
        crop = image[y1:y2, x1:x2]

        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

        # Define blue mask
        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])

        # Define orange mask
        lower_orange = np.array([10, 100, 100])
        upper_orange = np.array([25, 255, 255])

        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)

        blue_pixels = cv2.countNonZero(blue_mask)
        orange_pixels = cv2.countNonZero(orange_mask)

        # Define red mask (two ranges due to HSV wraparound)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        # Define green mask
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])

        red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        green_mask = cv2.inRange(hsv, lower_green, upper_green)

        red_pixels = cv2.countNonZero(red_mask)
        green_pixels = cv2.countNonZero(green_mask)

        if red_pixels > green_pixels:
            print("The largest car bounding box contains mostly RED.")
        elif green_pixels > red_pixels:
            print("The largest car bounding box contains mostly GREEN.")
        else:
            print("The largest car bounding box contains neither color predominantly.")
        color = "red" if red_pixels > green_pixels else "green" if green_pixels > red_pixels else "none"
    else:
        print("No car detected.")
    # Save the output image
    output_path = "cars_detected.jpg"
    #TODO
    cv2.imwrite(output_path, image)
    print(f"Saved image with car detections to '{output_path}'")
    print("largest_area:", largest_area)
    res = {
        "size": largest_area,
        "color": color if 'color' in locals() else "?",
        "position": ("right" if box_center_x > image_center_x else "left") if 'box_center_x' in locals() and 'image_center_x' in locals() else "none"
    }
    print(res["position"])
    return res

if __name__ == '__main__':
    straight = -0.225
    left = -1
    right = 1
    forward = 0.25
    backward = -0.25
    stop = 0
    back_up_size_threshold = 50000
    piracer = PiRacerPro()
    picam2 = Picamera2()
    picam2.start()
    time.sleep(2)  # let camera warm up
    not_done = True
    #model = YOLO("yolov8n.pt")  # COCO-trained model
    #start main loop
    while not_done:
        direction = "straight"
        speed = "forward"
        #Get image from camera

        #Identify obstacles
        image = prendre_image(picam2)
        ob_res = gauche_ou_droit_alt(image)
        magnitude = 1
        #If obstacle is large, stop and back up until it is small enough(farther)
        if ob_res["size"] > back_up_size_threshold:
            speed = "back"

        #If obstacle is red, turn right
        if ob_res["color"] == "red":
            direction = "right"

        #If obstacle is green, turn left
        elif ob_res["color"] == "green":
            direction = "left"
        #If no obstacles were detected, identify obstacles in the bottom 45%-60% of the image
        else:
            speed = "forward"
            pk_res = trouver(image)
            if pk_res["color"]!= "none":
                direction = "left"
                magnitude = pk_res["position"]*2
                if magnitude > right:
                    magnitude = right
                elif magnitude < left:
                    magnitude = left
            else:
                #If no obstacles were detected, identify lines
                direction = "straight"

        #Identify lines

        #If line is tilting right, turn right
        #If line is tilting left, turn left
        #Note: keep adjusting steering with the lines
        #Try to keep the lines close enough, so the car does not hit the walls


        #Execute the movement
        if speed == "forward":
            piracer.set_throttle_percent(forward)
            if direction == "straight":
                piracer.set_steering_percent(straight)
                pass
            elif direction == "left":
                piracer.set_steering_percent(left*magnitude)
                pass
            elif direction == "right":
                piracer.set_steering_percent(right*magnitude)
                pass
        elif speed == "back":
            piracer.set_throttle_percent(backward)
            if direction == "straight":
                piracer.set_steering_percent(straight)
                pass
            # FLIP
            elif direction == "left":
                piracer.set_steering_percent(right*magnitude)
                pass
            elif direction == "right":
                piracer.set_steering_percent(left*magnitude)
                pass
        else:
            piracer.set_throttle_percent(stop)
            pass
        time.sleep(0.05)
        #not_done = False
"""
Main Loop:
1. Capture image from camera.
2. Detect obstacles in the bottom 45% of the image, squeezed to the middle.
    - If the obstacle is large(closer), back up.
    - If the obstacle is red, turn right.
    - If the obstacle is green, turn left.
3. If no obstacles were in the bottom 45% of image, identify obstacles in the bottom 45%-60% of the image.
    - Align so that the car faces the obstacle.
6. If no obstacles were detected, detect lines and adjust steering accordingly.
7. Execute movement based on detected obstacles and lines.
8. Repeat until 3 turns.
"""

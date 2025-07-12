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

#Tell if obstacle is on the left or right, and if it is red or green, and its size
def gauche_ou_droit(model, image):
    image_height, image_width = image.shape[:2]
    image_center_x = image_width // 2

    # Run inference
    results = model(image)[0]

    # COCO class ID for "car" is 2
    car_class_id = 2

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
            label = f"Car {conf:.2f}"
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
    res = {
        "size": largest_area,
        "color": color if color else "?",
        "position": "right" if box_center_x > image_center_x else "left"
    }
    return res

if __name__ == '__main__':
    straight = -0.225
    left = -1
    right = 1
    forward = 0.3
    backward = -0.3
    stop = 0
    back_up_size_threshold = 1000
    piracer = PiRacerPro()
    picam2 = Picamera2()
    picam2.start()
    time.sleep(2)  # let camera warm up
    not_done = True
    model = YOLO("yolov8n.pt")  # COCO-trained model
    #start main loop
    while not_done:
        direction = "straight"
        speed = "forward"
        #Get image from camera

        #Identify obstacles
        ob_res = gauche_ou_droit(model, prendre_image(picam2))

        #If obstacle is large, stop and back up until it is small enough(farther)
        if ob_res["size"] > back_up_size_threshold:
            speed = "back"

        #If obstacle is red, turn right
        if ob_res["color"] == "red":
            direction = "right"

        #If obstacle is green, turn left
        elif ob_res["color"] == "green":
            direction = "left"

        #Identify lines

        #If line is tilting right, turn right
        #If line is tilting left, turn left
        #Note: keep adjusting steering with the lines
        #Try to keep the lines close enough, so the car does not hit the walls


        #Execute the movement
        if speed == "forward":
            ##piracer.set_throttle_percent(forward)
            if direction == "straight":
                ##piracer.set_steering_percent(straight)
                pass
            elif direction == "left":
                ##piracer.set_steering_percent(left)
                pass
            elif direction == "right":
                ##piracer.set_steering_percent(right)
                pass
        elif speed == "back":
            ##piracer.set_throttle_percent(backward)
            if direction == "straight":
                ##piracer.set_steering_percent(straight)
                pass
            # FLIP
            elif direction == "left":
                ##piracer.set_steering_percent(right)
                pass
            elif direction == "right":
                ##piracer.set_steering_percent(left)
                pass
        else:
            ##piracer.set_throttle_percent(stop)
            pass
        time.sleep(0.2)
        #not_done = False
"""
Main Loop:
1. Capture image from camera.
2. Detect obstacles using YOLO model.
3. If the obstacle is large(closer), back up.
4. If the obstacle is red, turn right.
5. If the obstacle is green, turn left.
6. Detect lines and adjust steering accordingly.
7. Execute movement based on detected obstacles and lines.
8. Repeat until 3 turns.
"""

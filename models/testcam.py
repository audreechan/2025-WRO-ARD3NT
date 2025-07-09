from picamera2 import Picamera2
import time

picam2 = Picamera2()
#config = picam2.create_video_configuration(main={"size":(640,480)}, transform=Transform(vflip = True))
#picam2.configure(config)
picam2.start()
time.sleep(2)  # let camera warm up
image = picam2.capture_array()
print(image)
# Save or display the image
from PIL import Image
Image.fromarray(image).save("output.png")

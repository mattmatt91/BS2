import datetime
from fastapi.responses import StreamingResponse
from io import BytesIO
from os.path import join
import cv2
import os
from time import sleep
import time
import numpy as np
from PIL import Image

class ImageCapturer:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        sleep(2)

    def capture(self):
        # Capture an image using picamera2
        ret, frame = self.camera.read()
        if not ret:
            raise Exception("Cam not found")
        if ret:
            return frame
        else:
            return None
        

    def save_image(self, frame):
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        path = join("data/", filename)
        print("Current working directory:", os.getcwd())
        # Save the image using PIL
        try:
            cv2.imwrite(path, frame)
            print(f"taking image to {path}")
        except Exception as e:
            print(f"unable to save image: {e}")
        return filename

    def format_for_serving(self, image):
        # Convert the image to PNG using PIL and serve
        img = Image.fromarray(image)
        buf = BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")

    def close(self):
        self.camera.release()

if __name__ == "__main__":
    # Example usage
    capturer = ImageCapturer()
    try:
        image, ret = capturer.capture()
        # Save the image
        filename = capturer.save_image(image, ret)
        # Serve the image via FastAPI
        image_response = capturer.format_for_serving(image)
    finally:
        capturer.close()

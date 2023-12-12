import cv2
import datetime
import numpy as np
from fastapi.responses import StreamingResponse
from io import BytesIO
from os.path import join
class ImageCapturer:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise ValueError("Could not open the camera")

    def capture(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture image")
        return frame

    def save_image(self, image):
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        path = join("/app/data/", filename)
        cv2.imwrite(filename, image)
        return filename

    def format_for_serving(self, image):
        _, encoded_image = cv2.imencode('.png', image)
        return StreamingResponse(BytesIO(encoded_image.tobytes()), media_type="image/png")

    def close(self):
        self.cap.release()

if __name__ == "__main__":
    # Example usage
    capturer = ImageCapturer()
    try:
        image = capturer.capture()
        # Save the image
        filename = capturer.save_image(image)
        # Serve the image via FastAPI
        image_response = capturer.format_for_serving(image)
    finally:
        capturer.close()

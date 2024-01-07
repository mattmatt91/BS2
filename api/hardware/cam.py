import datetime
from fastapi.responses import StreamingResponse
from io import BytesIO
from os.path import join
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import numpy as np

class ImageCapturer:
    def __init__(self):
        # Initialize the camera
        self.camera = PiCamera()
        self.stream = PiRGBArray(self.camera)
        # Camera warm-up time
        time.sleep(2)

    def capture(self):
        # Capture an image to a NumPy array
        self.camera.capture(self.stream, format='bgr')
        # Extract the frame
        frame = self.stream.array
        # Clear the stream for the next frame
        self.stream.truncate(0)
        self.stream.seek(0)
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
        self.camera.close()

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

import datetime
from fastapi.responses import StreamingResponse
from io import BytesIO
from os.path import join
import cv2
import os
from PIL import Image


class ImageCapturer:
    def __init__(self):
        pass

    def capture(self):
        # Attempt to capture an image using the specified camera index
        self.camera = cv2.VideoCapture(-1)
        ret, frame = None, None
        for i in range(
            10
        ):  # Attempt to read a few frames to allow the camera to adjust
            ret, frame = self.camera.read()
        self.camera.release()

        if not ret:
            raise Exception("Cam not found")
        return frame  # Return the captured frame directly

    def save_image(self, frame):
        # Save the captured frame to a PNG file
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        path = join("data/", filename)
        try:
            cv2.imwrite(path, frame)
            print(f"Image saved to {path}")
        except Exception as e:
            print(f"Unable to save image: {e}")
        return filename

    def format_for_serving(self, image):
        # Convert the image from BGR (OpenCV format) to RGB for serving
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image_rgb)
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return StreamingResponse(buf, media_type="image/png")

    def close(self):
        pass


if __name__ == "__main__":
    # Example usage
    capturer = ImageCapturer()
    try:
        # Capture the image
        image = capturer.capture()
        if image is not None:
            # Save the image
            filename = capturer.save_image(image)
            # Prepare the image for serving
            image_response = capturer.format_for_serving(image)
        else:
            print("No image captured.")
    finally:
        capturer.close()

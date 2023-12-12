import cv2
import datetime
from fastapi.responses import StreamingResponse
from io import BytesIO
import numpy as np
from os.path import join

class MockImageCapturer:
    def __init__(self, image_path='./hardware/test_img.png'):
        # Load a static image to mock camera capture
        self.static_image = cv2.imread(image_path)
        if self.static_image is None:
            raise ValueError("Static image not found or unable to load.")

    def capture(self):
        # Create a copy of the image to add text
        image_with_text = self.static_image.copy()

        # Get current date and time
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add date and time to the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image_with_text, current_datetime, (10, 30), font, 1, (0, 0, 255), 2, cv2.LINE_AA)

        return image_with_text

    def save_image(self, image):
        filename = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
        path = join("/app/data", filename)
        cv2.imwrite(filename, image)
        return filename

    def format_for_serving(self, image):
        _, encoded_image = cv2.imencode('.png', image)
        return StreamingResponse(BytesIO(encoded_image.tobytes()), media_type="image/png")

    def close(self):
        pass  # Nothing to close in the mock class



if __name__ == "__main__":
    # Example usage
    mock_capturer = MockImageCapturer()
    try:
        image = mock_capturer.capture()
        print(image)
        
        # Save the image
        filename = mock_capturer.save_image(image)
        # Serve the image via FastAPI
        image_response = mock_capturer.format_for_serving(image)
        print(image_response)
    finally:
        mock_capturer.close()

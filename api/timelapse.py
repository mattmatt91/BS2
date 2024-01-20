import cv2
import os
import numpy as np
from datetime import datetime


class Timelapse:
    text_color = (0, 0, 255)
    text_size = 1
    text_position = (80, 80)
    frame_size = (640, 480)
    frame_rate = 1
    directory = "data/"
    brightness_threshold = 30  # Adjust this threshold as needed

    @classmethod
    def extract_timestamp(cls, file_path):
        try:
            filename = os.path.basename(file_path)
            time_str = os.path.splitext(filename)[0]
            datetime_obj = datetime.strptime(time_str, "%Y%m%d_%H%M%S")
            return datetime_obj
        except ValueError:
            return None

    @classmethod
    def list_new_images(cls, directory):
        image_files = []
        for f in os.listdir(directory):
            if f.endswith(".png") and "_read" not in f:
                full_path = os.path.join(directory, f)
                timestamp = cls.extract_timestamp(full_path)
                if timestamp:
                    image_files.append((timestamp, full_path))

        # Sort the files based on timestamp
        image_files.sort()
        return [file_path for _, file_path in image_files]

    @classmethod
    def is_dark_image(cls, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return True  # Consider it dark if the image can't be read

        avg_brightness = np.mean(img)
        return avg_brightness < cls.brightness_threshold

    @classmethod
    def create_video(cls, image_paths, video_path):
        video = cv2.VideoWriter(
            video_path, cv2.VideoWriter_fourcc(*"mp4v"), cls.frame_rate, cls.frame_size
        )

        for image_path in image_paths:
            if cls.is_dark_image(image_path):
                print(f"Skipping dark image: {image_path}")
                cls.mark_image_as_processed(image_path)
                continue

            img = cv2.imread(image_path)
            img = cv2.resize(img, cls.frame_size)
            timestamp_str = os.path.splitext(os.path.basename(image_path))[0]
            datetime_obj = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            formatted_time = datetime_obj.strftime("%d.%m.%Y %H:%M:%S")
            cv2.putText(
                img,
                formatted_time,
                cls.text_position,
                cv2.FONT_HERSHEY_SIMPLEX,
                cls.text_size,
                cls.text_color,
                2,
            )
            video.write(img)
            cls.mark_image_as_processed(image_path)

        video.release()

    @classmethod
    def mark_image_as_processed(cls, image_path):
        pass
        # new_name = f"{image_path}_read.png"
        # new_name = os.path.join(cls.directory, f"{image_path.split("/")[-1].split(".")[0]}_read.png")
        # os.rename(image_path, new_name)

    @classmethod
    def create_timelapse(cls, video_path):
        new_images = cls.list_new_images(cls.directory)
        if new_images:
            cls.create_video(new_images, video_path)

    @classmethod
    def download_video(cls, video_path):
        cls.create_timelapse(video_path)
        return video_path


if __name__ == "__main__":
    video_path = "timelapse_video.mp4"  # Specify your desired output path here
    Timelapse.create_timelapse(video_path)
    print(f"Video saved to {video_path}")

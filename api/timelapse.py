import io
import cv2
import os
from datetime import datetime
import tempfile
import shutil


class Timelapse:
    text_color = (0, 0, 255)
    text_size = 1
    text_position = (80, 80)
    frame_size = (640, 480)
    duration_per_image = 0.1
    frame_rate = 60 / duration_per_image
    directory = "../data/images/images"

    @classmethod
    def create_video(cls, image_paths, output_path):
        # Create video and write to specified file
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video = cv2.VideoWriter(output_path, fourcc, cls.frame_rate, cls.frame_size)
        for image_path in image_paths:
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
            for _ in range(int(cls.frame_rate * cls.duration_per_image)):
                video.write(img)
        video.release()

    @classmethod
    def list_png_files(cls, directory):
        png_files = {}
        print(directory)
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path) and entry.lower().endswith(".png"):
                png_files[cls.get_timestamp(entry)] = full_path
        return png_files

    @classmethod
    def get_timestamp(cls, file):
        time_string = file.split(".")[0]
        datetime_obj = datetime.strptime(time_string, "%Y%m%d_%H%M%S")
        return datetime_obj

    @classmethod
    def save_video_to_file(cls, output_path):
        png_files = cls.list_png_files(cls.directory)
        print(png_files)
        sorted_file_paths = [png_files[key] for key in sorted(png_files)]
        cls.create_video(sorted_file_paths, output_path)


if __name__ == "__main__":
    timelapse = Timelapse()
    output_path = "timelapse_video.mp4"  # Specify your desired output path here
    timelapse.save_video_to_file(output_path)
    print(f"Video saved to {output_path}")

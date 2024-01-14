import io
import cv2
import os
from datetime import datetime
import tempfile
import shutil

class Timelapse():
    text_color = (0, 0, 255)  # Red color in BGR format
    text_size = 1             # Font size
    text_position = (80, 80)
    frame_size = (640, 480)
    duration_per_image = 1
    frame_rate = 60 / duration_per_image
    directory = "data/"
    output_video = 'timelapse.mp4'

    @classmethod
    def create_video(cls, image_paths, output_video):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(output_video, fourcc,
                                cls.frame_rate, cls.frame_size)
        for image_path in image_paths:
            img = cv2.imread(image_path)
            img = cv2.resize(img, cls.frame_size)
            timestamp_str = os.path.splitext(os.path.basename(image_path))[0]
            datetime_obj = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            formatted_time = datetime_obj.strftime('%d.%m.%Y %H:%M:%S')
            cv2.putText(img, formatted_time, cls.text_position,
                        cv2.FONT_HERSHEY_SIMPLEX, cls.text_size, cls.text_color, 2)
            for _ in range(int(cls.frame_rate * cls.duration_per_image)):
                video.write(img)
        video.release()

    @classmethod
    def create_video_buffer(cls, image_paths):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
            # Create video and write to temporary file
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(temp_video_file.name, fourcc, cls.frame_rate, cls.frame_size)

        for image_path in image_paths:
            img = cv2.imread(image_path)
            img = cv2.resize(img, cls.frame_size)
            timestamp_str = os.path.splitext(os.path.basename(image_path))[0]
            datetime_obj = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
            formatted_time = datetime_obj.strftime('%d.%m.%Y %H:%M:%S')
            cv2.putText(img, formatted_time, cls.text_position,
                        cv2.FONT_HERSHEY_SIMPLEX, cls.text_size, cls.text_color, 2)
            for _ in range(int(cls.frame_rate * cls.duration_per_image)):
                video.write(img)
        video.release()
        with open(temp_video_file.name, 'rb') as file:
                video_data = file.read()

        # Optionally delete the temporary file
        os.remove(temp_video_file.name)

        return video_data

    @classmethod
    def list_png_files(cls, directory):
        png_files = {}
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path) and entry.lower().endswith('.png'):
                png_files[cls.get_timestamp(entry)] = full_path
        return png_files

    @classmethod
    def get_timestamp(cls, file):
        time_string = file.split(".")[0]
        datetime_obj = datetime.strptime(time_string, '%Y%m%d_%H%M%S')
        return datetime_obj

    @classmethod
    def download_video(cls):
        png_files = cls.list_png_files(cls.directory)
        sorted_file_paths = [png_files[key] for key in sorted(png_files)]
        cls.create_video_buffer(sorted_file_paths)


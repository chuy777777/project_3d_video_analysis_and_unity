import os
import cv2

from components.video_recording import VideoRecording

class VideoCameras():
    def __init__(self):
        self.cap_camera_1=None
        self.cap_camera_2=None
        self.full_path_video_camera_1=""
        self.full_path_video_camera_2=""
        self.duration_ms_camera_1=0 
        self.duration_ms_camera_2=0 
        self.frame_count_camera_1=0
        self.frame_count_camera_2=0

    def init_cap_cameras(self):
        if self.cap_camera_1 is not None:
            self.cap_camera_1.release()
        if self.cap_camera_2 is not None:
            self.cap_camera_2.release()
        self.cap_camera_1=None
        self.cap_camera_2=None

    def set_cap_cameras(self, folder_name_video_recording, camera_name_1, camera_name_2):
        self.full_path_video_camera_1=os.path.join(folder_name_video_recording, *["{}.{}".format(camera_name_1, VideoRecording.video_format)])
        self.full_path_video_camera_2=os.path.join(folder_name_video_recording, *["{}.{}".format(camera_name_2, VideoRecording.video_format)])
        self.cap_camera_1=cv2.VideoCapture(self.full_path_video_camera_1)
        self.cap_camera_2=cv2.VideoCapture(self.full_path_video_camera_2)
        if self.cap_camera_1.isOpened() and self.cap_camera_2.isOpened():
            self.frame_count_camera_1=self.cap_camera_1.get(cv2.CAP_PROP_FRAME_COUNT)
            self.duration_ms_camera_1=(self.frame_count_camera_1 * (1 / self.cap_camera_1.get(cv2.CAP_PROP_FPS))) * 1000
            self.frame_count_camera_2=self.cap_camera_2.get(cv2.CAP_PROP_FRAME_COUNT)
            self.duration_ms_camera_2=(self.frame_count_camera_2 * (1 / self.cap_camera_2.get(cv2.CAP_PROP_FPS))) * 1000
        else:
            self.init_cap_cameras()

    def cap_cameras_is_ok(self):
        return self.cap_camera_1 is not None and self.cap_camera_2 is not None
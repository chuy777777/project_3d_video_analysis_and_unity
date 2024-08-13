import cv2
from threading import Timer

class VideoRecording():
    video_format="mp4"

    def __init__(self):
        self.out=None
        self.timer=None
        self.is_recording=False

    def init_video_recording(self, full_path, fps, frame_size, max_seconds):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
        self.out = cv2.VideoWriter(full_path, fourcc, fps, frame_size) # 'VideoWriter' expects stable FPS (https://github.com/opencv/opencv/issues/23403)
        self.timer = Timer(max_seconds, self.save)
        self.timer.start()
        self.is_recording=True

    def stop_video_recording(self):
        if self.is_recording:
            self.timer.cancel()
            self.save()

    def save(self):
        try:
            if self.is_recording:
                self.is_recording=False
                self.out.release()
                self.out=None 
                self.timer=None
        except cv2.error as error:
            print("cv2.error: {}".format(error))
        except:
            print("Save video except")
            
    def write(self, frame_bgr):
        if self.is_recording:
            self.out.write(frame_bgr)
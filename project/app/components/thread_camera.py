import cv2
import time
import os
from threading import Thread

from components.template_thread import TemplateThread
from components.video_recording import VideoRecording
from pinhole_camera_model.camera_device import CameraDevice

class ThreadCameraFrameListener():
    def __init__(self):
        pass 

    # Sobreescribir este metodo
    def thread_camera_frame_listener_notification(self):
        pass

class ThreadCamera(Thread, TemplateThread, VideoRecording):
    def __init__(self, root_name, folder_name_optimal_parameters):
        Thread.__init__(self, daemon=True)
        TemplateThread.__init__(self)
        VideoRecording.__init__(self)
        self.root_name=root_name
        self.folder_name_optimal_parameters=folder_name_optimal_parameters
        self.camera_device=CameraDevice()
        self.cap=None
        self.frame_bgr=None
        self.frame_bgr_shape=None
        self.frame_listener_list=[]

    def run(self):
        self.init_cap()
        self.view_camera()       
        print("End ThreadCamera from '{}'".format(self.camera_device.camera_name))    

    def init_cap(self, camera_name="", camera_path=""):
        self.release_cap()
        if camera_name == "":
            self.camera_device.init_device()
        else:
            self.set_device_and_load_saved_calibration_information(camera_name=camera_name, camera_path=camera_path)
        if camera_path == "":
            self.cap=cv2.VideoCapture() 
        else:
            self.cap=cv2.VideoCapture(camera_path)
        self.notify_frame_listeners()
        
    def release_cap(self):
        if self.cap is not None:
            self.cap.release()

    def view_camera(self):
        while not self.event_kill_thread.is_set():
            try:
                if self.cap is not None:
                    if self.cap.isOpened():
                        ret, frame_bgr=self.cap.read()
                        if ret:
                            self.frame_bgr=frame_bgr
                            self.frame_bgr_shape=frame_bgr.shape
                            self.write(frame_bgr=frame_bgr)
                        else:
                            """
                            Una vez que esta funcionando, si la camara se desconecta entra aqui.
                            Si se vuelve a conectar por USB no se reconecta por si sola.
                            """
                            self.frame_bgr=None
                            self.frame_bgr_shape=None
                    else:
                        """
                        Si la camara no esta conectada por USB desde un inicio entra aqui.
                        Si se vuelve a conectar por USB no se reconecta por si sola.
                        """
                        self.frame_bgr=None
                        self.frame_bgr_shape=None
                else:
                    self.frame_bgr=None
                    self.frame_bgr_shape=None
            except cv2.error as e:
                print("(cv2.error): {}".format(e))
                self.frame_bgr=None
                self.frame_bgr_shape=None

            time.sleep(0.001)
        self.release_cap()

    def start_video_recording(self, folder_name_video_recording, fps=20.0, max_seconds=60):
        if self.frame_bgr_shape is not None:
            file_name="{}.{}".format(self.camera_device.camera_name, VideoRecording.video_format)
            h,w,d=self.frame_bgr_shape
            frame_size=(w,h)
            full_path=os.path.join(folder_name_video_recording, *[file_name])
            self.init_video_recording(full_path=full_path, fps=fps, frame_size=frame_size, max_seconds=max_seconds)
            return True
        else:
            return False
        
    def set_device_and_load_saved_calibration_information(self, camera_name, camera_path):
        self.camera_device.set_device(camera_name=camera_name, camera_path=camera_path)
        self.camera_device.load_saved_calibration_information(folder_name=self.folder_name_optimal_parameters)
    
    def load_new_calibration_information(self, K, K_inv, q, Qs, lambdas, history_L, history_norm_grad, calibration_parameters, optimization_parameters):
        self.camera_device.load_new_calibration_information(K=K, K_inv=K_inv, q=q, Qs=Qs, lambdas=lambdas, history_L=history_L, history_norm_grad=history_norm_grad, calibration_parameters=calibration_parameters, optimization_parameters=optimization_parameters)
        self.notify_frame_listeners()
        
    def save_calibration_information(self):
        self.camera_device.save_calibration_information(folder_name=self.folder_name_optimal_parameters)
    
    def add_frame_listener(self, frame_listener):
        frame_listener_name_list=list(map(lambda elem: elem.name, self.frame_listener_list))
        if frame_listener.name not in frame_listener_name_list:
            self.frame_listener_list.append(frame_listener)

    def delete_frame_listener(self, frame_listener_name):
        self.frame_listener_list=list(filter(lambda elem: elem.name != frame_listener_name,self.frame_listener_list))

    def notify_frame_listeners(self):
        for frame_listener in self.frame_listener_list:
            frame_listener.thread_camera_frame_listener_notification()
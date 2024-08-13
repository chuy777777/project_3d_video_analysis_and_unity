import customtkinter  as ctk
import tkinter as tk
import numpy as np

from components.create_frame import CreateFrame
from components.grid_frame import GridFrame
from components.frame_camera_display import FrameCameraDisplay
from components.text_validator import TextValidator

class FrameVideoRecording(CreateFrame):
    def __init__(self, master, name, callback=None, **kwargs):
        CreateFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(1,1), arr=None), **kwargs)
        self.app=self.get_frame(frame_name="FrameApplication") 
        self.thread_camera_1=self.app.thread_camera_1
        self.thread_camera_2=self.app.thread_camera_2
        self.callback=callback
        self.folder_name_video_recording=self.app.folder_name_video_recording
        self.rate_ms=50
        self.fps=20.0

        frame_camera_displays=CreateFrame(master=self, grid_frame=GridFrame(dim=(1,3), arr=None))
        self.frame_camera_display_camera_1=FrameCameraDisplay(master=frame_camera_displays, name="FrameCameraDisplay1", thread_camera=self.thread_camera_1, rate_ms=self.rate_ms, scale_percent=70, editable=False)
        self.frame_camera_display_camera_2=FrameCameraDisplay(master=frame_camera_displays, name="FrameCameraDisplay2", thread_camera=self.thread_camera_2, rate_ms=self.rate_ms, scale_percent=70, editable=False)
        frame_container=CreateFrame(master=frame_camera_displays, grid_frame=GridFrame(dim=(4,2), arr=np.array([["0,0","0,0"],["1,0","1,0"],["2,0","2,1"],["3,0","3,1"]])))
        label_max_seconds=ctk.CTkLabel(master=frame_container, text="Maxima duracion (s)")
        self.var_max_seconds=ctk.StringVar(value="60")
        entry_max_seconds=ctk.CTkEntry(master=frame_container, textvariable=self.var_max_seconds, width=100)
        button_start_video_recording=ctk.CTkButton(master=frame_container, text="Comenzar", fg_color="green2", hover_color="green3", command=self.start_video_recording)
        button_stop_video_recording=ctk.CTkButton(master=frame_container, text="Detener", fg_color="red2", hover_color="red3", command=self.stop_video_recording)
        self.label_video_recording_camera_1=ctk.CTkLabel(master=frame_container, text="", width=100, height=100)
        self.label_video_recording_camera_2=ctk.CTkLabel(master=frame_container, text="", width=100, height=100)
        frame_container.insert_element(cad_pos="0,0", element=label_max_seconds, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="1,0", element=entry_max_seconds, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="2,0", element=button_start_video_recording, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="2,1", element=button_stop_video_recording, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="3,0", element=self.label_video_recording_camera_1, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="3,1", element=self.label_video_recording_camera_2, padx=5, pady=5, sticky="")
        frame_camera_displays.insert_element(cad_pos="0,0", element=self.frame_camera_display_camera_1, padx=5, pady=5, sticky="")
        frame_camera_displays.insert_element(cad_pos="0,1", element=frame_container, padx=5, pady=5, sticky="")
        frame_camera_displays.insert_element(cad_pos="0,2", element=self.frame_camera_display_camera_2, padx=5, pady=5, sticky="")
        
        self.insert_element(cad_pos="0,0", element=frame_camera_displays, padx=5, pady=5, sticky="ew")

    def start_video_recording(self):
        if not self.thread_camera_1.is_recording and not self.thread_camera_2.is_recording:
            max_seconds=TextValidator.validate_number(text=self.var_max_seconds.get())
            if max_seconds is not None and max_seconds > 0:
                self.label_video_recording_camera_1.configure(bg_color="green" if self.thread_camera_1.start_video_recording(self.folder_name_video_recording, fps=self.fps, max_seconds=max_seconds) else "red")
                self.label_video_recording_camera_2.configure(bg_color="green" if self.thread_camera_2.start_video_recording(self.folder_name_video_recording, fps=self.fps, max_seconds=max_seconds) else "red")
                self.waiting_for_video_recording()
            else:
                tk.messagebox.showinfo(title="Grabacion de video", message="El campo de duracion maxima del video no es correcto.")

    def stop_video_recording(self):
        self.thread_camera_1.stop_video_recording()
        self.thread_camera_2.stop_video_recording()
        self.waiting_for_video_recording()

    def waiting_for_video_recording(self):
        if self.thread_camera_1.is_recording or self.thread_camera_2.is_recording:
            self.after(self.rate_ms, self.waiting_for_video_recording)
        else:
            self.label_video_recording_camera_1.configure(bg_color="transparent")
            self.label_video_recording_camera_2.configure(bg_color="transparent")
            if self.callback is not None:
                self.callback()
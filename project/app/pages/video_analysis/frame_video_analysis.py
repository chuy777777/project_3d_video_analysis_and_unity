import customtkinter  as ctk
import tkinter as tk
import numpy as np
import os
import cv2

from components.create_frame import CreateFrame
from components.create_scrollable_frame import CreateScrollableFrame
from components.grid_frame import GridFrame
import components.utils as utils
from pages.estimation.frame_estimation_graphic_3D_with_options import FrameEstimationGraphic3DWithOptions
from pages.estimation.frame_calculate_extrinsic_matrices import FrameCalculateExtrinsicMatrices
from pages.estimation.frame_select_algorithms import FrameSelectAlgorithms
from pages.video_analysis.frame_video_recording import FrameVideoRecording
from pages.video_analysis.video_cameras import VideoCameras
from pages.video_analysis.frame_select_angles import FrameSelectAngles

class FrameVideoAnalysis(CreateScrollableFrame):
    def __init__(self, master, name, **kwargs):
        CreateScrollableFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(5,1), arr=None), **kwargs)
        self.app=self.get_frame(frame_name="FrameApplication") 
        self.thread_camera_1=self.app.thread_camera_1
        self.thread_camera_2=self.app.thread_camera_2
        self.folder_name_video_recording=self.app.folder_name_video_recording
        self.label_frame_scale_percent=80
        self.video_cameras=VideoCameras()

        frame_video_recording=FrameVideoRecording(master=self, name="FrameVideoRecording", callback=self.load_videos)

        self.frame_calculate_extrinsic_matrices=FrameCalculateExtrinsicMatrices(master=self, name="FrameCalculateExtrinsicMatrices", callback=self.update_frames)

        self.frame_select_algorithms=FrameSelectAlgorithms(master=self, name="FrameSelectAlgorithms", callback=self.callback_select_algorithms)

        frame_container=CreateFrame(master=self, grid_frame=GridFrame(dim=(4,4), arr=np.array([["0,0","0,0","0,0","0,0"],["1,0","1,1","1,1","1,3"],["2,0","2,0","2,2","2,2"],["3,0","3,1","3,1","3,3"]])))
        button_load_videos=ctk.CTkButton(master=frame_container, text="Cargar videos de las correspondientes camaras", fg_color="orange2", hover_color="orange3", command=self.load_videos)
        self.var_label_camera_1=ctk.StringVar(value="")
        label_camera_1=ctk.CTkLabel(master=frame_container, textvariable=self.var_label_camera_1)
        self.var_label_camera_2=ctk.StringVar(value="")
        label_camera_2=ctk.CTkLabel(master=frame_container, textvariable=self.var_label_camera_2)
        button_delete_videos=ctk.CTkButton(master=frame_container, text="Eliminar videos", fg_color="red2", hover_color="red3", command=self.delete_videos)
        self.label_frame_camera_1=ctk.CTkLabel(master=frame_container, text="")
        self.label_frame_camera_2=ctk.CTkLabel(master=frame_container, text="")
        button_slider_video_left=ctk.CTkButton(master=frame_container, text="Ir a la izquierda", command=self.go_to_left)
        self.var_slider_video=ctk.IntVar(value=0)
        self.var_slider_video.trace_add("write", self.trace_var_slider_video)
        self.slider_video=ctk.CTkSlider(master=frame_container, variable=self.var_slider_video, from_=0, to=1, number_of_steps=1)
        button_slider_video_right=ctk.CTkButton(master=frame_container, text="Ir a la Derecha", command=self.go_to_right)
        frame_container.insert_element(cad_pos="0,0", element=button_load_videos, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="1,0", element=label_camera_1, padx=5, pady=5, sticky="ew")
        frame_container.insert_element(cad_pos="1,1", element=button_delete_videos, padx=5, pady=5, sticky="")
        frame_container.insert_element(cad_pos="1,3", element=label_camera_2, padx=5, pady=5, sticky="ew")
        frame_container.insert_element(cad_pos="2,0", element=self.label_frame_camera_1, padx=5, pady=5, sticky="ew")
        frame_container.insert_element(cad_pos="2,2", element=self.label_frame_camera_2, padx=5, pady=5, sticky="ew")
        frame_container.insert_element(cad_pos="3,0", element=button_slider_video_left, padx=5, pady=5, sticky="ew")
        frame_container.insert_element(cad_pos="3,1", element=self.slider_video, padx=5, pady=5, sticky="ew")
        frame_container.insert_element(cad_pos="3,3", element=button_slider_video_right, padx=5, pady=5, sticky="ew")

        frame_container_graphic_3D=CreateFrame(master=self, grid_frame=GridFrame(dim=(1,2), arr=None))
        self.frame_estimation_graphic_3D_with_options=FrameEstimationGraphic3DWithOptions(master=frame_container_graphic_3D, name="FrameEstimationGraphic3DWithOptions", callback=self.update_frames, square_size=1, width=700, height=700)
        self.frame_container_select_angles=CreateScrollableFrame(master=frame_container_graphic_3D, grid_frame=GridFrame(dim=(len(self.frame_select_algorithms.algorithm_class_list),1), arr=None), orientation="vertical")
        frame_container_graphic_3D.insert_element(cad_pos="0,0", element=self.frame_estimation_graphic_3D_with_options, padx=5, pady=5, sticky="")
        frame_container_graphic_3D.insert_element(cad_pos="0,1", element=self.frame_container_select_angles, padx=5, pady=5, sticky="nsew")
        
        self.insert_element(cad_pos="0,0", element=frame_video_recording, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="1,0", element=self.frame_calculate_extrinsic_matrices, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="2,0", element=self.frame_select_algorithms, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="3,0", element=frame_container, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="4,0", element=frame_container_graphic_3D, padx=5, pady=5, sticky="ew")

    def destroy(self):
       self.video_cameras.init_cap_cameras()
       CreateScrollableFrame.destroy(self)

    def load_videos(self):
        self.video_cameras.init_cap_cameras()
        self.video_cameras.set_cap_cameras(folder_name_video_recording=self.folder_name_video_recording, camera_name_1=self.thread_camera_1.camera_device.camera_name, camera_name_2=self.thread_camera_2.camera_device.camera_name)
        self.set_slider()
        self.update_frames()
        self.var_label_camera_1.set(value=self.thread_camera_1.camera_device.camera_name)
        self.var_label_camera_2.set(value=self.thread_camera_2.camera_device.camera_name)

    def delete_videos(self):
        if tk.messagebox.askyesnocancel(title="Eliminar videos", message="¿Esta seguro de eliminar los videos?"):
            for file_name in os.listdir(self.folder_name_video_recording):
                full_path=os.path.join(self.folder_name_video_recording, *[file_name])
                os.remove(full_path)
            self.video_cameras.init_cap_cameras()
            self.set_slider()
            self.update_frames()
            self.var_label_camera_1.set(value="")
            self.var_label_camera_2.set(value="")
            
    def callback_select_algorithms(self):
        self.update_frame_container_select_angles()
        self.update_frames()

    def update_frame_container_select_angles(self):
        current_algorithm_name_list=self.frame_select_algorithms.current_algorithm_names()
        algorithm_class_list=self.frame_select_algorithms.algorithm_class_list
        n=len(algorithm_class_list)
        all_algorithm_name_list=list(map(lambda elem: elem.algorithm_name, algorithm_class_list))
        for i in range(n):
            algorithm_name=all_algorithm_name_list[i]
            if algorithm_name in current_algorithm_name_list and not self.frame_container_select_angles.element_exists(cad_pos="{},0".format(i)):
                # Crear nuevo
                frame_select_angles=FrameSelectAngles(master=self.frame_container_select_angles, name="FrameSelectAngles", algorithm_name=algorithm_class_list[i].algorithm_name, number_points=algorithm_class_list[i].number_points, callback=self.update_frames)
                self.frame_container_select_angles.insert_element(cad_pos="{},0".format(i), element=frame_select_angles, padx=5, pady=5, sticky="ew")
            if algorithm_name not in current_algorithm_name_list and self.frame_container_select_angles.element_exists(cad_pos="{},0".format(i)):
                # Eliminar existente
                self.frame_container_select_angles.destroy_element(cad_pos="{},0".format(i))

    def set_slider(self):
        self.var_slider_video.set(value=0)
        if self.video_cameras.cap_cameras_is_ok():
            mean_frames=int((self.video_cameras.frame_count_camera_1 + self.video_cameras.frame_count_camera_2) / 2)
            self.slider_video.configure(from_=0, to=mean_frames, number_of_steps=mean_frames)
        else:
            self.slider_video.configure(from_=0, to=1, number_of_steps=1)

    def trace_var_slider_video(self,  var, index, mode):  
        if self.video_cameras.cap_cameras_is_ok():
            n=int(self.slider_video.cget(attribute_name="number_of_steps"))
            p=self.var_slider_video.get()
            d1=self.video_cameras.duration_ms_camera_1
            d2=self.video_cameras.duration_ms_camera_2
            p1=p * (d1 / n)
            p2=p * (d2 / n)
            self.video_cameras.cap_camera_1.set(cv2.CAP_PROP_POS_MSEC, p1)
            self.video_cameras.cap_camera_2.set(cv2.CAP_PROP_POS_MSEC, p2)
            self.update_frames()

    def go_to_left(self):
        p=self.var_slider_video.get()
        if p - 1 >= 0:
            self.var_slider_video.set(value=p - 1)

    def go_to_right(self):
        n=int(self.slider_video.cget(attribute_name="number_of_steps"))
        p=self.var_slider_video.get()
        if p + 1 <= n:
            self.var_slider_video.set(value=p + 1)

    def set_label_frame(self, label, frame_bgr):
        img=utils.frame_bgr_to_ctk_img(frame_bgr=frame_bgr)
        label.configure(image=img)
        label.image=img

    def update_frames(self):
        # Limpiamos el grafico en cada instante
        self.frame_estimation_graphic_3D_with_options.frame_graphic_3D.clear()
        if self.video_cameras.cap_cameras_is_ok():
            ret1,frame_bgr_1=self.video_cameras.cap_camera_1.read()
            ret2,frame_bgr_2=self.video_cameras.cap_camera_2.read()
            if ret1 and ret2:
                frame_bgr_1=utils.resize_frame_bgr(scale_percent=self.label_frame_scale_percent, frame_bgr=frame_bgr_1)
                frame_bgr_2=utils.resize_frame_bgr(scale_percent=self.label_frame_scale_percent, frame_bgr=frame_bgr_2)
                Q1=self.frame_calculate_extrinsic_matrices.dict_extrinsic_matrices["Q1"]
                Q2=self.frame_calculate_extrinsic_matrices.dict_extrinsic_matrices["Q2"]
                frame_bgr_1,frame_bgr_2=self.frame_select_algorithms.set_estimation_data_from_algorithms(Q1=Q1, Q2=Q2, frame_bgr_1=frame_bgr_1, frame_bgr_2=frame_bgr_2, draw=True)
                self.set_label_frame(label=self.label_frame_camera_1, frame_bgr=frame_bgr_1)
                self.set_label_frame(label=self.label_frame_camera_2, frame_bgr=frame_bgr_2)
                self.frame_estimation_graphic_3D_with_options.draw_estimation(algorithm_list=self.frame_select_algorithms.algorithm_list)
                self.draw_angles()
            else:
                self.set_label_frame(label=self.label_frame_camera_1, frame_bgr=None)
                self.set_label_frame(label=self.label_frame_camera_2, frame_bgr=None)
        else:
            self.set_label_frame(label=self.label_frame_camera_1, frame_bgr=None)
            self.set_label_frame(label=self.label_frame_camera_2, frame_bgr=None)

    def draw_angles(self):
        algorithm_list=self.frame_select_algorithms.algorithm_list
        all_algorithm_name_list=list(map(lambda elem: elem.algorithm_name, self.frame_select_algorithms.algorithm_class_list))
        for algorithm in algorithm_list:
            index=all_algorithm_name_list.index(algorithm.algorithm_name)
            frame_select_angles: FrameSelectAngles=self.frame_container_select_angles.get_element(cad_pos="{},0".format(index))
            if algorithm.is_double_estimate:
                for key in algorithm.dict_points_3D.keys():
                    points_3D=algorithm.dict_points_3D[key]
                    for triplet in frame_select_angles.triplet_list:
                        p1,pm,p2=points_3D[triplet[0]],points_3D[triplet[1]],points_3D[triplet[2]]
                        self.frame_estimation_graphic_3D_with_options.frame_graphic_3D.plot_angle(pm=pm, p1=p1, p2=p2, show_degree=True, color_rgb_polygon_facecolors=(0,255,0), color_rgb_polygon_edgecolors=(0,0,0), alpha_polygon=0.2, color_rgb_text=(0,0,0), fontsize_text="medium", fontweight_text="bold")
            else:
                if algorithm.points_3D is not None:
                    for triplet in frame_select_angles.triplet_list:
                        p1,pm,p2=algorithm.points_3D[triplet[0]],algorithm.points_3D[triplet[1]],algorithm.points_3D[triplet[2]]
                        self.frame_estimation_graphic_3D_with_options.frame_graphic_3D.plot_angle(pm=pm, p1=p1, p2=p2, show_degree=True, color_rgb_polygon_facecolors=(0,255,0), color_rgb_polygon_edgecolors=(0,0,0), alpha_polygon=0.2, color_rgb_text=(0,0,0), fontsize_text="medium", fontweight_text="bold")
        self.frame_estimation_graphic_3D_with_options.frame_graphic_3D.draw()

    

    

    

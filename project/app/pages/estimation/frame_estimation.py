import customtkinter  as ctk
import tkinter as tk
import numpy as np

from components.create_frame import CreateFrame
from components.create_scrollable_frame import CreateScrollableFrame
from components.grid_frame import GridFrame
from components.frame_camera_display import FrameCameraDisplay
from pages.parameter_checking.frame_calibration_information import FrameCalibrationInformation
from pages.estimation.frame_estimation_graphic_3D_with_options import FrameEstimationGraphic3DWithOptions
from pages.estimation.frame_calculate_extrinsic_matrices import FrameCalculateExtrinsicMatrices
from pages.estimation.frame_select_algorithms import FrameSelectAlgorithms

class FrameEstimation(CreateScrollableFrame):
    def __init__(self, master, name, callback_estimation_data, **kwargs):
        CreateScrollableFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(6,1), arr=None), **kwargs)
        self.app=self.get_frame(frame_name="FrameApplication") 
        self.thread_camera_1=self.app.thread_camera_1
        self.thread_camera_2=self.app.thread_camera_2
        self.callback_estimation_data=callback_estimation_data
        self.rate_ms=50

        self.frame_select_algorithms=FrameSelectAlgorithms(master=self, name="FrameSelectAlgorithms")

        frame_calibration_informations=CreateFrame(master=self, grid_frame=GridFrame(dim=(1,2), arr=None))
        frame_calibration_information_camera_1=FrameCalibrationInformation(master=frame_calibration_informations, name="FrameCalibrationInformation1", thread_camera=self.thread_camera_1, only_camera_parameters=True)
        frame_calibration_information_camera_2=FrameCalibrationInformation(master=frame_calibration_informations, name="FrameCalibrationInformation2", thread_camera=self.thread_camera_2, only_camera_parameters=True)
        frame_calibration_informations.insert_element(cad_pos="0,0", element=frame_calibration_information_camera_1, padx=5, pady=5, sticky="")
        frame_calibration_informations.insert_element(cad_pos="0,1", element=frame_calibration_information_camera_2, padx=5, pady=5, sticky="")

        frame_camera_displays=CreateFrame(master=self, grid_frame=GridFrame(dim=(2,3), arr=np.array([["0,0","0,0","0,0"],["1,0","1,1","1,2"]])))
        self.var_draw_algorithms=ctk.IntVar(value=1)
        check_box_draw_algorithms=ctk.CTkCheckBox(master=frame_camera_displays, text="Mostrar algoritmos en imagen", variable=self.var_draw_algorithms, onvalue=1, offvalue=0)
        self.frame_camera_display_camera_1=FrameCameraDisplay(master=frame_camera_displays, name="FrameCameraDisplay1", thread_camera=self.thread_camera_1, rate_ms=self.rate_ms, scale_percent=70, editable=True)
        self.frame_camera_display_camera_2=FrameCameraDisplay(master=frame_camera_displays, name="FrameCameraDisplay2", thread_camera=self.thread_camera_2, rate_ms=self.rate_ms, scale_percent=70, editable=True)
        self.frame_estimation_graphic_3D_with_options=FrameEstimationGraphic3DWithOptions(master=frame_camera_displays, name="FrameEstimationGraphic3DWithOptions", square_size=1, width=400, height=400)
        frame_camera_displays.insert_element(cad_pos="0,0", element=check_box_draw_algorithms, padx=5, pady=5, sticky="")
        frame_camera_displays.insert_element(cad_pos="1,0", element=self.frame_camera_display_camera_1, padx=5, pady=5, sticky="")
        frame_camera_displays.insert_element(cad_pos="1,1", element=self.frame_estimation_graphic_3D_with_options, padx=5, pady=5, sticky="")
        frame_camera_displays.insert_element(cad_pos="1,2", element=self.frame_camera_display_camera_2, padx=5, pady=5, sticky="")
        
        self.frame_calculate_extrinsic_matrices=FrameCalculateExtrinsicMatrices(master=self, name="FrameCalculateExtrinsicMatrices")

        self.insert_element(cad_pos="0,0", element=self.frame_select_algorithms, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="1,0", element=frame_calibration_informations, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="2,0", element=frame_camera_displays, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="3,0", element=self.frame_calculate_extrinsic_matrices, padx=5, pady=5, sticky="new")

        self.start_process()

    def start_process(self):
        Q1=self.frame_calculate_extrinsic_matrices.dict_extrinsic_matrices["Q1"]
        Q2=self.frame_calculate_extrinsic_matrices.dict_extrinsic_matrices["Q2"]
        
        frame_bgr_1,frame_bgr_2=self.frame_select_algorithms.set_estimation_data_from_algorithms(Q1=Q1, Q2=Q2, draw=self.var_draw_algorithms.get())

        self.frame_camera_display_camera_1.update_label_camera(frame_bgr=frame_bgr_1)
        self.frame_camera_display_camera_2.update_label_camera(frame_bgr=frame_bgr_2)

        self.frame_estimation_graphic_3D_with_options.draw_estimation(algorithm_list=self.frame_select_algorithms.algorithm_list)

        # Notificamos de los datos de estimacion
        self.callback_estimation_data(algorithm_list=self.frame_select_algorithms.algorithm_list)

        self.after(self.rate_ms, self.start_process)
        
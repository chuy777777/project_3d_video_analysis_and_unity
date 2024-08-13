import numpy as np
import customtkinter  as ctk

from components.create_frame import CreateFrame
from components.grid_frame import GridFrame

class FramePageButtons(CreateFrame):
    def __init__(self, master, name, **kwargs):
        CreateFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(3,2), arr=np.array([["0,0","0,0"],["1,0","1,1"],["2,0","2,0"]])), **kwargs)
        self.app=self.get_frame(frame_name="FrameApplication") 

        button_parameter_checking_page=ctk.CTkButton(master=self, text="Comprobacion de parametros", command=lambda: self.set_page(page_name="parameter_checking"))
        button_calibration_page=ctk.CTkButton(master=self, text="Calibracion", command=lambda: self.set_page(page_name="calibration"))
        button_estimation_page=ctk.CTkButton(master=self, text="Estimaciones", command=lambda: self.set_page(page_name="estimation"))
        button_video_analysis_page=ctk.CTkButton(master=self, text="Analisis de video", command=lambda: self.set_page(page_name="video_analysis"))

        self.insert_element(cad_pos="0,0", element=button_parameter_checking_page, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="1,0", element=button_calibration_page, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="1,1", element=button_estimation_page, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="2,0", element=button_video_analysis_page, padx=5, pady=5, sticky="ew")

    def set_page(self, page_name):
        self.get_element(cad_pos="0,0").configure(fg_color=("gray40", "gray25") if page_name == "parameter_checking" else "gray70")
        self.get_element(cad_pos="1,0").configure(fg_color=("gray40", "gray25") if page_name == "calibration" else "gray70")
        self.get_element(cad_pos="1,1").configure(fg_color=("gray40", "gray25") if page_name == "estimation" else "gray70") 
        self.get_element(cad_pos="2,0").configure(fg_color=("gray40", "gray25") if page_name == "video_analysis" else "gray70") 
        self.app.set_page(page_name=page_name)
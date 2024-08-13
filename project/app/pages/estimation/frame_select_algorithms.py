import customtkinter  as ctk

from components.create_frame import CreateFrame
from components.grid_frame import GridFrame
from components.coordinate_converter import CoordinateConverter
from pinhole_camera_model.estimate_points_3D import EstimatePoints3D
from pinhole_camera_model.draw_image import DrawImage

# ALGORITMOS
from pinhole_camera_model.algorithms.algorithm_mediapipe_hands import AlgorithmMediaPipeHands
from pinhole_camera_model.algorithms.algorithm_mediapipe_pose import AlgorithmMediaPipePose

class FrameSelectAlgorithms(CreateFrame):
    def __init__(self, master, name, callback=None, **kwargs):
        CreateFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(2,1), arr=None), **kwargs)
        self.app=self.get_frame(frame_name="FrameApplication") 
        self.thread_camera_1=self.app.thread_camera_1
        self.thread_camera_2=self.app.thread_camera_2
        self.callback=callback
        self.band_changed_algorithms=False
        self.algorithm_list=[]
        self.factor_mm_to_mt=1 / 1000

        label_algorithms=ctk.CTkLabel(master=self, text="Seleccion de algoritmos")

        self.algorithm_class_list=[
            AlgorithmMediaPipeHands,
            AlgorithmMediaPipePose
        ]
        self.var_selected_algorithm_list=[]
        n=len(self.algorithm_class_list)
        frame_container=CreateFrame(master=self, grid_frame=GridFrame(dim=(n,1), arr=None))
        for i in range(n):
            var_selected_algorithm=ctk.IntVar(value=0)
            var_selected_algorithm.trace_add("write", self.changed_algorithms)
            self.var_selected_algorithm_list.append(var_selected_algorithm)
            check_box_algorithm=ctk.CTkCheckBox(master=frame_container, text=self.algorithm_class_list[i].algorithm_name, variable=var_selected_algorithm, onvalue=1, offvalue=0)
            frame_container.insert_element(cad_pos="{},0".format(i), element=check_box_algorithm, padx=5, pady=5, sticky="")

        self.insert_element(cad_pos="0,0", element=label_algorithms, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="1,0", element=frame_container, padx=5, pady=5, sticky="new")

    def changed_algorithms(self, var, index, mode):
        self.band_changed_algorithms=True
        if self.callback is not None:
            self.callback()

    def current_algorithm_names(self):
        current_algorithm_name_list=[]
        for i in range(len(self.var_selected_algorithm_list)):
            if self.var_selected_algorithm_list[i].get():
                current_algorithm_name_list.append(self.algorithm_class_list[i].algorithm_name)
        return current_algorithm_name_list
    
    def apply_selection(self):
        if self.band_changed_algorithms:
            for i in range(len(self.algorithm_list)):
                algorithm=self.algorithm_list[i]
                del algorithm
            self.algorithm_list=[]
            for i in range(len(self.var_selected_algorithm_list)):
                if self.var_selected_algorithm_list[i].get():
                    self.algorithm_list.append(self.algorithm_class_list[i]())
            self.band_changed_algorithms=False 

    """
    Con respecto a los puntos 3D calculados por el modelo de camara Pinhole:
        - Se asume que el sistema de coordenadas del mundo queda de tal manera que el tablero
            esta apuntando de frente a las camaras
        - Los puntos 3D se pasan al systema de coordenadas de matplotlib (tradicional)
        - Los puntos se convierten de mm a mt
    """
    def set_estimation_data_from_algorithms(self, Q1, Q2, frame_bgr_1=None, frame_bgr_2=None, draw=True):
        self.apply_selection()

        frame_bgr_1=self.thread_camera_1.frame_bgr if frame_bgr_1 is None else frame_bgr_1
        frame_bgr_2=self.thread_camera_2.frame_bgr if frame_bgr_2 is None else frame_bgr_2
        camera_device_1=self.thread_camera_1.camera_device if self.thread_camera_1.camera_device.calibration_information_is_loaded else None
        camera_device_2=self.thread_camera_2.camera_device if self.thread_camera_2.camera_device.calibration_information_is_loaded else None
        for i in range(len(self.algorithm_list)):
            algorithm=self.algorithm_list[i]
            if algorithm.is_double_estimate:
                dict_v3pds1,is_ok1=algorithm.get_points_2D(frame_bgr=frame_bgr_1)
                dict_v3pds2,is_ok2=algorithm.get_points_2D(frame_bgr=frame_bgr_2)
                if draw:
                    if is_ok1:
                        for key in dict_v3pds1.keys():
                            frame_bgr_1=DrawImage.draw_conenctions(frame_bgr=frame_bgr_1, points=dict_v3pds1[key], connection_list=algorithm.connection_list)
                    if is_ok2:
                        for key in dict_v3pds2.keys():
                            frame_bgr_2=DrawImage.draw_conenctions(frame_bgr=frame_bgr_2, points=dict_v3pds2[key], connection_list=algorithm.connection_list)
                if is_ok1 and is_ok2 and Q1 is not None and Q2 is not None and camera_device_1 is not None and camera_device_2 is not None:
                    dict_points_3D={}
                    for key in ["Left", "Right"]:
                        if key in dict_v3pds1 and key in dict_v3pds2:
                            vws=EstimatePoints3D.estimate_points_3D(K1=camera_device_1.K, K1_inv=camera_device_1.K_inv, Q1=Q1, q1=camera_device_1.q, K2=camera_device_2.K, K2_inv=camera_device_2.K_inv, Q2=Q2, q2=camera_device_2.q, v3pds1=dict_v3pds1[key], v3pds2=dict_v3pds2[key])
                            vms=CoordinateConverter.system_w_to_system_m(vws=vws) * self.factor_mm_to_mt
                            dict_points_3D[key]=vms
                    algorithm.set_data(dict_points_3D=dict_points_3D)
                else:
                    algorithm.set_data(dict_points_3D={})
            else:
                v3pds1,is_ok1=algorithm.get_points_2D(frame_bgr=frame_bgr_1)
                v3pds2,is_ok2=algorithm.get_points_2D(frame_bgr=frame_bgr_2)
                if draw:
                    if is_ok1:
                        frame_bgr_1=DrawImage.draw_conenctions(frame_bgr=frame_bgr_1, points=v3pds1, connection_list=algorithm.connection_list)
                    if is_ok2:
                        frame_bgr_2=DrawImage.draw_conenctions(frame_bgr=frame_bgr_2, points=v3pds2, connection_list=algorithm.connection_list)
                if is_ok1 and is_ok2 and Q1 is not None and Q2 is not None and camera_device_1 is not None and camera_device_2 is not None:
                    vws=EstimatePoints3D.estimate_points_3D(K1=camera_device_1.K, K1_inv=camera_device_1.K_inv, Q1=Q1, q1=camera_device_1.q, K2=camera_device_2.K, K2_inv=camera_device_2.K_inv, Q2=Q2, q2=camera_device_2.q, v3pds1=v3pds1, v3pds2=v3pds2)
                    vms=CoordinateConverter.system_w_to_system_m(vws=vws) * self.factor_mm_to_mt
                    algorithm.set_data(points_3D=vms)
                else:
                    algorithm.set_data(points_3D=None)
                    
        return frame_bgr_1,frame_bgr_2
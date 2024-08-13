import numpy as np
import customtkinter  as ctk

from components.create_frame import CreateFrame
from components.grid_frame import GridFrame
from components.thread_camera import ThreadCameraFrameListener
from components.frame_graphic_2D import FrameGraphic2D
from components.frame_graphic_3D import FrameGraphic3D

class FrameCalibrationInformation(CreateFrame, ThreadCameraFrameListener):
    def __init__(self, master, name, thread_camera, only_camera_parameters=False, **kwargs):
        CreateFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(3,1), arr=None), **kwargs)
        ThreadCameraFrameListener.__init__(self)
        self.thread_camera=thread_camera
        self.thread_camera.add_frame_listener(frame_listener=self)
        self.only_camera_parameters=only_camera_parameters

    def destroy(self):
        self.thread_camera.delete_frame_listener(frame_listener_name=self.name)
        CreateFrame.destroy(self)

    def thread_camera_frame_listener_notification(self):
        self.destroy_all()
        if self.thread_camera.camera_device.calibration_information_is_loaded:
            self.show_calibration_information()
        else:
            self.show_not_calibration_information()

    def show_calibration_information(self):
        camera_device=self.thread_camera.camera_device

        if self.only_camera_parameters:
            label_camera_parameters=ctk.CTkLabel(master=self, text=camera_device.__str__())
            self.insert_element(cad_pos="0,0", element=label_camera_parameters, padx=5, pady=5, sticky="ew")
        else:
            label_camera_parameters=ctk.CTkLabel(master=self, text=camera_device.__str__())
            frame_graphic_2D=FrameGraphic2D(master=self, name="FrameGraphic2D_{}".format(camera_device.camera_name), width=400, height=400)
            ps=np.concatenate([np.arange(1,camera_device.history_L.size + 1)[:,None], camera_device.history_L[:,None]], axis=1)
            frame_graphic_2D.plot_lines(ps=ps, color_rgb=(0,0,255))
            frame_graphic_2D.graphic_configuration(xlabel="Iteraciones", ylabel="L", title="Historial de perdida")
            frame_graphic_2D.draw()
            frame_graphic_3D=FrameGraphic3D(master=self, name="FrameGraphic3D_{}".format(camera_device.camera_name), square_size=0.7, width=500, height=500)
            tcm,Tcm=np.array([[0],[-0.5],[0]]),np.array([[1,0,0],[0,0,1],[0,-1,0]])
            frame_graphic_3D.plot_coordinate_system(t_list=[tcm], T_list=[Tcm], length=0.5)
            factor_mm_to_mt=1 / 1000
            for i in range(camera_device.Qs.shape[0]):
                Q=camera_device.Qs[i]
                twc,Twc=Q[:,[3]],Q[:,[0,1,2]]
                H=frame_graphic_3D.plot_coordinate_system(t_list=[tcm,twc * factor_mm_to_mt], T_list=[Tcm,Twc], length=0.5)
                length=0.5
                vm_=H @ np.array([[0,0,0,1],[length,0,0,1],[length,length,0,1],[0,length,0,1]]).T
                # Puntos en forma de vector fila
                vm=vm_[0:3,:].T
                frame_graphic_3D.plot_polygon(verts=vm, alpha=0.8, facecolors="orange", edgecolors="black")
            frame_graphic_3D.set_title(title="Matrices extrinsecas Q's ({})\nEjes: X (rojo) Y (verde) Z (azul)".format(camera_device.Qs.shape[0]))
            frame_graphic_3D.draw()

            self.insert_element(cad_pos="0,0", element=label_camera_parameters, padx=5, pady=5, sticky="ew")
            self.insert_element(cad_pos="1,0", element=frame_graphic_2D, padx=5, pady=5, sticky="")
            self.insert_element(cad_pos="2,0", element=frame_graphic_3D, padx=5, pady=5, sticky="")

    def show_not_calibration_information(self):
        label_not_camera_parameters=ctk.CTkLabel(master=self, text=" --- CAMARA NO CALIBRADA ---")

        self.insert_element(cad_pos="0,0", element=label_not_camera_parameters, padx=5, pady=5, sticky="ew")

import customtkinter  as ctk

from components.create_frame import CreateFrame
from components.grid_frame import GridFrame
from components.frame_graphic_3D import FrameGraphic3D

class FrameEstimationGraphic3DWithOptions(CreateFrame):
    def __init__(self, master, name, callback=None, square_size=1, width=400, height=400, **kwargs):
        CreateFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(3,1), arr=None), **kwargs)
        self.callback=callback

        self.var_points=ctk.IntVar(value=1)
        self.var_points.trace_add("write", self.trace_vars)
        self.var_lines=ctk.IntVar(value=1)
        self.var_lines.trace_add("write", self.trace_vars)
        self.var_coordinate_systems=ctk.IntVar(value=0)
        self.var_coordinate_systems.trace_add("write", self.trace_vars)
        frame_options=CreateFrame(master=self, grid_frame=GridFrame(dim=(3,1), arr=None))
        check_box_points=ctk.CTkCheckBox(master=frame_options, text="Puntos", variable=self.var_points, onvalue=1, offvalue=0)
        check_box_lines=ctk.CTkCheckBox(master=frame_options, text="Lineas", variable=self.var_lines, onvalue=1, offvalue=0)
        check_box_coordinate_systems=ctk.CTkCheckBox(master=frame_options, text="Sistemas de coordenadas", variable=self.var_coordinate_systems, onvalue=1, offvalue=0)
        frame_options.insert_element(cad_pos="0,0", element=check_box_points, padx=5, pady=5, sticky="")
        frame_options.insert_element(cad_pos="1,0", element=check_box_lines, padx=5, pady=5, sticky="")
        frame_options.insert_element(cad_pos="2,0", element=check_box_coordinate_systems, padx=5, pady=5, sticky="")

        self.frame_graphic_3D=FrameGraphic3D(master=self, name="FrameGraphic3DWithOptions", square_size=square_size, width=width, height=height)
        
        slider_graphic_3D=ctk.CTkSlider(master=self, from_=0.1, to=2.0, number_of_steps=100, command=self.slider_callback)

        self.insert_element(cad_pos="0,0", element=frame_options, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="1,0", element=self.frame_graphic_3D, padx=5, pady=5, sticky="ew")
        self.insert_element(cad_pos="2,0", element=slider_graphic_3D, padx=5, pady=5, sticky="ew")

    def trace_vars(self, var, index, mode):
        if self.callback is not None:
            self.callback()

    def slider_callback(self, value):
        self.frame_graphic_3D.graphic_configuration(xlabel="X", ylabel="Y", zlabel="Z", xlim=[-value,value], ylim=[-value,value], zlim=[-value,value])
        self.frame_graphic_3D.draw()
        
    def draw_estimation(self, algorithm_list):
        self.frame_graphic_3D.clear()
        for algorithm in algorithm_list:
            if algorithm.is_double_estimate:
                for key in algorithm.dict_points_3D.keys():
                    if self.var_points.get():
                        self.frame_graphic_3D.plot_points(ps=algorithm.dict_points_3D[key], color_rgb=(255,0,0), alpha=0.8, marker=".", s=70)
                    if self.var_lines.get():
                        self.frame_graphic_3D.plot_lines(ps=algorithm.dict_points_3D[key], connection_list=algorithm.connection_list, color_rgb=(0,255,0))
                    if self.var_coordinate_systems.get():
                        points_3D=algorithm.dict_points_3D[key]
                        coordinate_system_list=algorithm.dict_coordinate_system_list[key]
                        for i in range(len(coordinate_system_list)):
                            self.frame_graphic_3D.plot_coordinate_system(t_list=[points_3D[[i],:].T], T_list=[coordinate_system_list[i]], length=0.03)
            else:
                if algorithm.points_3D is not None:
                    if self.var_points.get():
                        self.frame_graphic_3D.plot_points(ps=algorithm.points_3D, color_rgb=(255,0,0), alpha=0.8, marker=".", s=70)
                    if self.var_lines.get():
                            self.frame_graphic_3D.plot_lines(ps=algorithm.points_3D, connection_list=algorithm.connection_list, color_rgb=(0,255,0))
                    if self.var_coordinate_systems.get():
                        for i in range(len(algorithm.coordinate_system_list)):
                            self.frame_graphic_3D.plot_coordinate_system(t_list=[algorithm.points_3D[[i],:].T], T_list=[algorithm.coordinate_system_list[i]], length=0.03)
        self.frame_graphic_3D.draw()
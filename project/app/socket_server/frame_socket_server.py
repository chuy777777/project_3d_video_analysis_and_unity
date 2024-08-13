import customtkinter  as ctk
import numpy as np
import copy

from components.create_frame import CreateFrame
from components.grid_frame import GridFrame
from components.text_validator import TextValidator
from socket_server.thread_server_socket import ThreadServerSocket

from decouple import config

class FrameSocketServer(CreateFrame):
    def __init__(self, master, name, **kwargs):
        CreateFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(3,3), arr=np.array([["0,0","0,0","0,0"],["1,0","1,1","1,2"],["2,0","2,0","2,2"]])), **kwargs)
        self.thread_server_socket=None 

        APP_HOST=config("APP_HOST")
        APP_PORT=config("APP_PORT")

        label_server=ctk.CTkLabel(master=self, text="Servidor")
        self.var_host=ctk.StringVar(value=APP_HOST)
        entry_host=ctk.CTkEntry(master=self, width=140, textvariable=self.var_host)
        self.var_port=ctk.StringVar(value=APP_PORT)
        entry_port=ctk.CTkEntry(master=self, width=140, textvariable=self.var_port)
        button_start_server=ctk.CTkButton(master=self, text="Iniciar servidor", fg_color="green2", hover_color="green3", command=self.start_server)
        self.var_label_message=ctk.StringVar(value="")
        label_message=ctk.CTkLabel(master=self, textvariable=self.var_label_message, wraplength=400)
        self.label_status=ctk.CTkLabel(master=self, text="", width=50, height=50)

        self.insert_element(cad_pos="0,0", element=label_server, padx=5, pady=5, sticky="")
        self.insert_element(cad_pos="1,0", element=entry_host, padx=5, pady=5, sticky="")
        self.insert_element(cad_pos="1,1", element=entry_port, padx=5, pady=5, sticky="")
        self.insert_element(cad_pos="1,2", element=button_start_server, padx=5, pady=5, sticky="")
        self.insert_element(cad_pos="2,0", element=label_message, padx=5, pady=5, sticky="")
        self.insert_element(cad_pos="2,2", element=self.label_status, padx=5, pady=5, sticky="")
    
    def start_server(self):
        if self.thread_server_socket is None or not self.thread_server_socket.is_alive():
            host=self.var_host.get()
            port=TextValidator.validate_number(text=self.var_port.get())
            if port is not None:
                self.thread_server_socket=ThreadServerSocket(name="Thread Server Socket", host=host, port=int(port), callback_set_state=self.set_state, daemon=True)
                self.thread_server_socket.start()
            else:
                self.set_state(message="El puerto no esta bien escrito", status_color="red")

    def set_state(self, message, status_color):
        self.var_label_message.set(value=message)
        self.label_status.configure(bg_color=status_color)

    def estimation_data(self, algorithm_list):
        if self.thread_server_socket is not None and self.thread_server_socket.is_alive():
            dict_algorithm_data_list=[]
            for algorithm in algorithm_list:
                # Es importante crear una copia (ya que se puede estar modificando en otra parte)
                dict_algorithm_data=copy.deepcopy(algorithm.get_dict_algorithm_data())
                dict_algorithm_data_list.append(dict_algorithm_data)
            self.thread_server_socket.set_dict_algorithm_data_list(dict_algorithm_data_list=dict_algorithm_data_list)

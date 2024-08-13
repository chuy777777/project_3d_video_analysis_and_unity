import socket
from threading import Thread

from pinhole_camera_model.algorithms.bytes_algorithms import BytesAlgorithms

class ThreadServerSocket(Thread):
    def __init__(self, name, host, port, callback_set_state, daemon=True):
        Thread.__init__(self, name=name, daemon=daemon)
        self.name=name
        self.host=host
        self.port=port
        self.callback_set_state=callback_set_state
        self.dict_algorithm_data_list=[]

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                self.callback_set_state(message="Servidor escuchando en {}:{}".format(self.host, self.port), status_color="green")
                s.bind((self.host, self.port))
                s.listen()
                while True:
                    self.callback_set_state(message="Esperando por conexion...", status_color="green")
                    conn, addr = s.accept()
                    with conn:
                        self.callback_set_state(message="Conectado por '{}'".format(addr), status_color="green")
                        while True:
                            data=conn.recv(4)
                            if not data:
                                # El cliente ha cerrado la conexion
                                self.callback_set_state(message="Cliente desconectado", status_color="red")
                                break
                            else:
                                value=int.from_bytes(data, "little")
                                if value == 1:
                                    bytes_to_unity=BytesAlgorithms.get_bytes_to_unity(dict_algorithm_data_list=self.dict_algorithm_data_list)
                                    conn.send(bytes_to_unity)
        except Exception as e:
            self.callback_set_state(message="Ha ocurrido una excepcion: {}".format(e), status_color="red")

    def set_dict_algorithm_data_list(self, dict_algorithm_data_list):
        self.dict_algorithm_data_list=dict_algorithm_data_list
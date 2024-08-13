from components.create_frame import CreateFrame
from components.grid_frame import GridFrame
from components.frame_page_buttons import FramePageButtons
from components.frame_select_camera import FrameSelectCamera
from socket_server.frame_socket_server import FrameSocketServer

class FrameNavbar(CreateFrame):
    def __init__(self, master, name, **kwargs):
        CreateFrame.__init__(self, master=master, name=name, grid_frame=GridFrame(dim=(1,3), arr=None), **kwargs)

        frame_button_pages=FramePageButtons(self, name="FramePageButtons")
        frame_select_camera=FrameSelectCamera(self, name="FrameSelectCamera")
        self.frame_socket_server=FrameSocketServer(self, name="FrameSocketServer")

        self.insert_element(cad_pos="0,0", element=frame_button_pages, padx=5, pady=5, sticky="")
        self.insert_element(cad_pos="0,1", element=frame_select_camera, padx=5, pady=5, sticky="")
        self.insert_element(cad_pos="0,2", element=self.frame_socket_server, padx=5, pady=5, sticky="ew")
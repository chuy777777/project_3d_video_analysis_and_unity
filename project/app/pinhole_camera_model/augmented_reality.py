import numpy as np
from pinhole_camera_model.image_points_2D_3D import ImagePoints2D3D
from pinhole_camera_model.camera_calibration import CameraCalibration
from pinhole_camera_model.draw_image import DrawImage

class AugmentedReality():
    def __init__(self):
        pass

    @staticmethod
    def draw_cube_on_chessboard(frame_bgr, chessboard_dimensions, square_size, K, K_inv, q, fast):
        if frame_bgr is None:
            return None 
        else:
            frame_bgr_copy=np.copy(frame_bgr)
            v3pds,vws,is_ok=ImagePoints2D3D.point_pairs_2D_and_3D_chessboard(frame_bgr=frame_bgr_copy, chessboard_dimensions=chessboard_dimensions, square_size=square_size, fast=fast)
            if is_ok:
                wb,hb=chessboard_dimensions
                indexes_corners=[0,wb - 1,wb * (hb - 1),wb * hb - 1]
                v3pds=v3pds[indexes_corners]
                vws=vws[indexes_corners]
                Q=CameraCalibration.get_Q(v3pds=v3pds, vws=vws, K=K, K_inv=K_inv, q=q)

                cube_height=80 # mm
                vws_bottom=np.copy(vws)
                vws_top=np.copy(vws)
                vws_top[:,2]=cube_height
                vws=np.concatenate([vws_bottom, vws_top], axis=0)
                connections=[(0,1),(1,3),(3,2),(2,0),(4,5),(5,7),(7,6),(6,4),(0,4),(1,5),(3,7),(2,6)]
                v3pds=CameraCalibration.get_v3pds(vws=vws, K=K, Q=Q, q=q)
                points1=np.zeros((len(connections),2))
                points2=np.zeros((len(connections),2))
                for i in range(len(connections)):
                    p1,p2=connections[i]
                    points1[i]=v3pds[p1]
                    points2[i]=v3pds[p2]
                frame_bgr_copy=DrawImage.draw_points(frame_bgr=frame_bgr_copy, points=v3pds, size=5, color_bgr=(0,255,0))
                frame_bgr_copy=DrawImage.draw_lines(frame_bgr=frame_bgr_copy, lines=(points1,points2), color_bgr=(0,0,255), weight=2)
                                                        
            return frame_bgr_copy










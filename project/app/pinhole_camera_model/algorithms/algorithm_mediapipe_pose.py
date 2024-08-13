import numpy as np
import cv2 
import mediapipe as mp
mp_pose=mp.solutions.pose

from pinhole_camera_model.algorithms.utils_algorithm import UtilsAlgorithm
 
"""
Algoritmo de deep learning para la estimacion de puntos caracteristicos del cuerpo humano.
"""
class AlgorithmMediaPipePose(UtilsAlgorithm):
    algorithm_name="MediaPipe Pose"
    number_points=33
    is_double_estimate=False
    connection_list=[(0,1),(1,2),(2,3),(3,7),(0,4),(4,5),(5,6),(6,8),(9,10),(11,13),(13,15),(15,21),(15,19),(19,17),(17,15),(12,14),(14,16),(16,22),(16,20),(20,18),(18,16),(11,23),(23,24),(24,12),(12,11),(23,25),(25,27),(27,31),(31,29),(29,27),(24,26),(26,28),(28,32),(32,30),(30,28)]
    creation_coordinate_system_list=[(0,9,0,10),(0,9,0,10),(0,9,0,10),(0,9,0,10),(0,9,0,10),(0,9,0,10),(0,9,0,10),(0,9,0,10),(0,9,0,10),(0,9,0,10),(0,9,0,10),(11,13,11,23),(12,14,12,24),(13,15,13,24),(14,16,14,23),(15,19,15,17),(16,20,16,18),(17,15,17,19),(18,16,18,20),(19,17,19,15),(20,18,20,16),(21,15,21,17),(22,16,22,18),(23,25,23,24),(24,26,24,23),(25,27,25,26),(26,28,26,25),(27,31,27,29),(28,32,28,30),(29,31,29,27),(30,32,30,28),(31,29,31,27),(32,30,32,28)]
        
    def __init__(self):
        UtilsAlgorithm.__init__(self)
        self.pose=mp_pose.Pose(
            static_image_mode=True,
            model_complexity=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.init_data()

    def init_data(self):
        self.points_3D=None 
        self.euler_angles=None
        self.coordinate_system_list=None

    def set_data(self, points_3D):
        self.init_data()
        self.points_3D=points_3D
        if self.points_3D is not None:
            euler_angles,coordinate_system_list=self.get_data_from_points_3D(points_3D=points_3D, creation_coordinate_system_list=AlgorithmMediaPipePose.creation_coordinate_system_list)
            self.euler_angles=euler_angles
            self.coordinate_system_list=coordinate_system_list
        else:
            self.euler_angles=None
            self.coordinate_system_list=None

    # Devuelve: (N,2)
    def get_points_2D(self, frame_bgr):
        if frame_bgr is not None:
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

            frame_rgb.flags.writeable = False
            results = self.pose.process(frame_rgb)
            frame_rgb.flags.writeable = True

            if results.pose_landmarks is not None:
                N=len(results.pose_landmarks.landmark)
                points=np.zeros((N, 2))
                for n in range(N):
                    x=results.pose_landmarks.landmark[n].x*frame_rgb.shape[1]
                    y=results.pose_landmarks.landmark[n].y*frame_rgb.shape[0]
                    points[n]=np.array([x,y])
                return points,True

        return None,False
    
    def get_dict_algorithm_data(self):
        return {
            "algorithm_name": self.algorithm_name,
            "number_points": self.number_points,
            "is_double_estimate": self.is_double_estimate,
            "data": {
                "points_3D": self.points_3D, 
                "euler_angles": self.euler_angles,
                "coordinate_system_list": self.coordinate_system_list
            }
        }
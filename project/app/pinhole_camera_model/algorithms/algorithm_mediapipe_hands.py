import numpy as np
import cv2 
import mediapipe as mp
mp_hands=mp.solutions.hands

from pinhole_camera_model.algorithms.utils_algorithm import UtilsAlgorithm

"""
Algoritmo de deep learning para la estimacion de puntos caracteristicos de la mano.
"""
class AlgorithmMediaPipeHands(UtilsAlgorithm):
    algorithm_name="MediaPipe Hands"
    number_points=21
    is_double_estimate=True
    connection_list=[(0,1),(1,2),(2,3),(3,4),(0,5),(5,6),(6,7),(7,8),(5,9),(9,10),(10,11),(11,12),(9,13),(13,14),(14,15),(15,16),(13,17),(17,18),(18,19),(19,20),(0,17)]
    creation_coordinate_system_list=[(0,9,0,17),(1,2,0,17),(2,3,0,17),(3,4,0,17),(3,4,0,17),(5,6,5,9),(6,7,5,9),(7,8,5,9),(7,8,5,9),(9,10,5,9),(10,11,5,9),(11,12,5,9),(11,12,5,9),(13,14,5,9),(14,15,5,9),(15,16,5,9),(15,16,5,9),(17,18,5,9),(18,19,5,9),(19,20,5,9),(19,20,5,9)]
    
    def __init__(self):
        UtilsAlgorithm.__init__(self)
        self.hands=mp_hands.Hands(
            static_image_mode=True, 
            model_complexity=1, 
            max_num_hands=2, 
            min_detection_confidence=0.5, 
            min_tracking_confidence=0.5
        )
        self.init_data()

    def init_data(self):
        self.dict_points_3D={}
        self.dict_euler_angles={}
        self.dict_coordinate_system_list={}

    def set_data(self, dict_points_3D):
        self.init_data()
        for key in dict_points_3D.keys():
            points_3D=dict_points_3D[key]
            euler_angles,coordinate_system_list=self.get_data_from_points_3D(points_3D=points_3D, creation_coordinate_system_list=AlgorithmMediaPipeHands.creation_coordinate_system_list)
            self.dict_points_3D[key]=points_3D
            self.dict_euler_angles[key]=euler_angles
            self.dict_coordinate_system_list[key]=coordinate_system_list

    # Devuelve: {"Left": (N,2), "Right": (N,2)}
    def get_points_2D(self, frame_bgr):
        if frame_bgr is not None:
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

            frame_rgb.flags.writeable = False
            results = self.hands.process(frame_rgb)
            frame_rgb.flags.writeable = True

            if results.multi_hand_landmarks is not None:

                l=["Left", "Right"]
                d=dict()
                hands_positions=[]
                for hand in results.multi_handedness:
                    hands_positions.append(list(set(l).difference(set([hand.classification[0].label])))[0])
                for i in range(len(results.multi_hand_landmarks)):
                    hand_landmarks=results.multi_hand_landmarks[i]
                    if hands_positions[i]=="Left": 
                        d['Left']=hand_landmarks
                    elif hands_positions[i]=="Right": 
                        d['Right']=hand_landmarks

                N=len(d[list(d.keys())[0]].landmark)
                dict_points=dict()
                for k in list(d.keys()):
                    hand_landmarks=d[k]
                    points=np.zeros((N, 2))
                    for n in range(N):
                        x=hand_landmarks.landmark[n].x*frame_rgb.shape[1]
                        y=hand_landmarks.landmark[n].y*frame_rgb.shape[0]
                        points[n]=np.array([x,y])
                    dict_points[k]=points
                return dict_points,True

        return None,False
    
    def get_dict_algorithm_data(self):
        return {
            "algorithm_name": self.algorithm_name,
            "number_points": self.number_points,
            "is_double_estimate": self.is_double_estimate,
            "data": {
                "dict_points_3D": self.dict_points_3D, 
                "dict_euler_angles": self.dict_euler_angles,
                "dict_coordinate_system_list": self.dict_coordinate_system_list
            }
        }
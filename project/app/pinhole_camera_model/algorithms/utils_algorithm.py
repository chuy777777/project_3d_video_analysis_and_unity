import numpy as np

import components.utils as utils

class UtilsAlgorithm():
    def __init__(self):
        pass 

    def get_coordinate_system_list(self, points_3D, creation_coordinate_system_list):
        # Este es el enfoque que se utiliza para crear los sistemas de coordenadas
        # Los puntos 3D estan en el sistema de coordenadas matplotlib (N,3)
        coordinate_system_list=[]
        number_points=points_3D.shape[0]
        for i in range(number_points):
            m,n,p,q=creation_coordinate_system_list[i]
            vz_mn=points_3D[n] - points_3D[m]
            v_pq=points_3D[q] - points_3D[p]
            vy=np.cross(v_pq, vz_mn)
            uy=utils.normalize_vector(vy)
            uz_mn=utils.normalize_vector(vz_mn)
            ux=np.cross(uy, uz_mn)
            R=np.concatenate([ux[:,None],uy[:,None],uz_mn[:,None]], axis=1)
            coordinate_system_list.append(R)

        return coordinate_system_list
    
    def get_euler_angles(self, coordinate_system_list):
        N=len(coordinate_system_list)
        euler_angles=np.zeros((N,3))
        for n in range(N):
            euler_angles[n]=utils.euler_angles_from_to_rotation_matrix(R=coordinate_system_list[n])
        return euler_angles
    
    def get_data_from_points_3D(self, points_3D, creation_coordinate_system_list):
        coordinate_system_list=self.get_coordinate_system_list(points_3D=points_3D, creation_coordinate_system_list=creation_coordinate_system_list)
        euler_angles=self.get_euler_angles(coordinate_system_list=coordinate_system_list)
        return euler_angles,coordinate_system_list
    
    
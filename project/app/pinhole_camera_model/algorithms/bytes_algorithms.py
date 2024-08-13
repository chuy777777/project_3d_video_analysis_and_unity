import numpy as np

from components.data_to_bytes import DataToBytes
from components.coordinate_converter import CoordinateConverter

class BytesAlgorithms():
    bytes_by_str=20
    bytes_by_number=4
    factor_radians_to_degrees=180 / np.pi

    def __init__(self):
        pass

    """
        - Los puntos estan en unidades de metros 
        - Los puntos se transforman del sistema de matplotlib al sistema de Unity
        - Los angulos de euler se pasan de radianes a grados (ya que unity trabaja con grados)
    """
    @staticmethod
    def get_bytes_algorithm(dict_algorithm_data):
        bytes_algorithm=bytes()

        bytes_algorithm_name=DataToBytes.str_to_bytes(cad=dict_algorithm_data["algorithm_name"], n=BytesAlgorithms.bytes_by_str)
        bytes_number_points=DataToBytes.int_to_bytes(number=dict_algorithm_data["number_points"], n=BytesAlgorithms.bytes_by_number)
        if dict_algorithm_data["is_double_estimate"]:
            dict_points_3D=dict_algorithm_data["data"]["dict_points_3D"]
            dict_euler_angles=dict_algorithm_data["data"]["dict_euler_angles"]
            if len(dict_algorithm_data["data"]["dict_points_3D"].keys()) == 0: 
                return None
            number_parts=len(dict_points_3D.keys())
            bytes_number_parts=DataToBytes.int_to_bytes(number=number_parts, n=BytesAlgorithms.bytes_by_number)
            bytes_algorithm=bytes_algorithm_name + bytes_number_points + bytes_number_parts
            for key in dict_points_3D.keys():
                points_3D=dict_points_3D[key]
                euler_angles=dict_euler_angles[key]
                bytes_part_name=DataToBytes.str_to_bytes(cad=key, n=BytesAlgorithms.bytes_by_str)
                bytes_points_3D=DataToBytes.numpy_array_to_bytes(arr=CoordinateConverter.system_m_to_system_u(vms=points_3D).T)
                bytes_euler_angles=DataToBytes.numpy_array_to_bytes(arr=euler_angles.T * BytesAlgorithms.factor_radians_to_degrees)
                bytes_algorithm+=bytes_part_name + bytes_points_3D + bytes_euler_angles
        else:
            points_3D=dict_algorithm_data["data"]["points_3D"]
            euler_angles=dict_algorithm_data["data"]["euler_angles"]
            if points_3D is None:
                return None
            number_parts=1 
            bytes_number_parts=DataToBytes.int_to_bytes(number=number_parts, n=BytesAlgorithms.bytes_by_number)
            bytes_part_name=DataToBytes.str_to_bytes(cad="All", n=BytesAlgorithms.bytes_by_str)
            bytes_points_3D=DataToBytes.numpy_array_to_bytes(arr=CoordinateConverter.system_m_to_system_u(vms=points_3D).T)
            bytes_euler_angles=DataToBytes.numpy_array_to_bytes(arr=euler_angles.T * BytesAlgorithms.factor_radians_to_degrees)
            bytes_algorithm=bytes_algorithm_name + bytes_number_points + bytes_number_parts + bytes_part_name + bytes_points_3D + bytes_euler_angles

        return bytes_algorithm     

    @staticmethod
    def get_bytes_to_unity(dict_algorithm_data_list):
        bytes_to_unity=bytes()
        bytes_temp=bytes()
        count=0
        for dict_algorithm_data in dict_algorithm_data_list:
            bytes_algorithm=BytesAlgorithms.get_bytes_algorithm(dict_algorithm_data=dict_algorithm_data)
            if bytes_algorithm is not None:
                bytes_temp+=bytes_algorithm
                count+=1
        if count > 0:
            bytes_exists_data=DataToBytes.int_to_bytes(number=1, n=BytesAlgorithms.bytes_by_number)
            bytes_number_algorithms=DataToBytes.int_to_bytes(number=count, n=BytesAlgorithms.bytes_by_number)
            bytes_to_unity=bytes_exists_data + bytes_number_algorithms + bytes_temp
            return bytes_to_unity
        else:
            bytes_exists_data=DataToBytes.int_to_bytes(number=0, n=BytesAlgorithms.bytes_by_number)
            bytes_to_unity=bytes_exists_data
            return bytes_to_unity

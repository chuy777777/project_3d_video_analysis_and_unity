class DataToBytes():
    def __init__(self):
        pass

    @staticmethod
    def concatenate_bytes(bytes_list):
        data=bytes()
        for b in bytes_list:
            data+=b 
        return data

    @staticmethod
    def str_to_bytes(cad, n):
        return bytes(cad.ljust(n, " "), 'ascii')

    @staticmethod
    def int_to_bytes(number, n):
        return int(number).to_bytes(n, 'little')
    
    @staticmethod
    def bool_to_bytes(band):
        return bool(band).to_bytes(1, 'little')

    # Se devuelven en su forma vectorizada
    @staticmethod
    def numpy_array_to_bytes(arr):
        arr=arr.astype('float32')               # 4 bytes por valor
        arr=arr.flatten(order='F')              # Equivale a vec(arr) 
        return arr.tobytes(order='c')
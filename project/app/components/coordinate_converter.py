import numpy as np

class CoordinateConverter():
    def __init__(self):
        pass

    # Para un tablero que apunta de frente a la computadora 
    @staticmethod
    def system_w_to_system_m(vws):
        twm=np.zeros((3,1))
        Twm=np.array([[0,0,-1],[-1,0,0],[0,-1,0]])
        H=np.concatenate([np.concatenate([Twm,np.zeros((1,3))], axis=0), np.concatenate([twm,np.ones((1,1))], axis=0)], axis=1)
        vws_=np.concatenate([vws, np.ones((vws.shape[0],1))], axis=1).T
        vms_=H @ vws_
        # Puntos en forma de vector fila
        vms=vms_[0:3,:].T
        return vms
    
    @staticmethod
    def system_m_to_system_u(vms):
        tmu=np.zeros((3,1))
        Tmu=np.array([[1,0,0],[0,0,1],[0,1,0]])
        H=np.concatenate([np.concatenate([Tmu,np.zeros((1,3))], axis=0), np.concatenate([tmu,np.ones((1,1))], axis=0)], axis=1)
        vms_=np.concatenate([vms, np.ones((vms.shape[0],1))], axis=1).T
        vus_=H @ vms_
        # Puntos en forma de vector fila
        vus=vus_[0:3,:].T
        return vus
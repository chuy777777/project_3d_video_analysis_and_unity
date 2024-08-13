from typing import Literal
import numpy as np

"""
OPTIMIZADORES
    Varios optimizadores hacen uso de la media movil exponencial (EMA)

    - Minibatch Gradient Descent
        - Momentum 
        - Nesterov 
    - RMSProp
    - AdaGrad
    - AdaDelta 
    - Adam
"""

class MBGDOptimizer():
    def __init__(self, with_: Literal["none", "momentum", "nesterov"]):
        self.with_=with_
        self.clear()
        
    def clear(self):
        self.it=0
        self.vg=None
        
    def iterate(self, grad, x, lr, beta=0.9):
        self.it+=1
        params=x
        
        new_params=None
        if self.with_ == "none":
            new_params=params - (lr * grad)
        elif self.with_ == "momentum":
            vg_previous=np.zeros((grad.size)) if self.it == 1 else self.vg
            self.vg=beta * vg_previous + (1 - beta) * grad
            new_params=params - (lr * self.vg)
        elif self.with_ == "nesterov":
            pass
        
        return new_params
        
class RMSPropOptimizer():
    def __init__(self):
        self.clear()
        
    def clear(self):
        self.it=0
        self.eps=1e-5
        self.vgs=None
        
    def iterate(self, grad, x, lr, beta=0.9):
        self.it+=1
        params=x
        
        vgs_previous=np.zeros((grad.size)) if self.it == 1 else self.vgs
        self.vgs=beta * vgs_previous + (1 - beta) * (grad ** 2)
        new_params=params - (lr * (1 / np.sqrt(self.vgs + self.eps)) * grad)
        
        return new_params
        
class AdaGradOptimizer():
    def __init__(self):
        self.clear()
        
    def clear(self):
        self.it=0
        self.eps=1e-5
        self.sum_gs=None
        
    def iterate(self, grad, x, lr, beta=0.9):
        self.it+=1
        params=x
        
        self.sum_gs=(grad ** 2) if self.it == 1 else self.sum_gs + (grad ** 2)
        new_params=params - (lr * (1 / np.sqrt(self.sum_gs + self.eps)) * grad)
        
        return new_params

class AdaDeltaOptimizer():
    def __init__(self):
        self.clear()
        
    def clear(self):
        self.it=0
        self.eps=1e-5
        self.vgs=None
        self.vdps=None
        self.delta_params=None
        
    def iterate(self, grad, x, beta=0.9):
        self.it+=1
        params=x
        
        self.delta_params=np.zeros((params.size)) if self.it == 1 else self.delta_params
        vdps_previous=np.zeros((params.size)) if self.it == 1 else self.vdps
        self.vdps=beta * vdps_previous + (1 - beta) * (self.delta_params ** 2)
        vgs_previous=np.zeros((grad.size)) if self.it == 1 else self.vgs
        self.vgs=beta * vgs_previous + (1 - beta) * (grad ** 2)
        self.delta_params=-(np.sqrt(self.vdps + self.eps) * (1 / np.sqrt(self.vgs + self.eps)) * grad)
        new_params=params + self.delta_params
        
        return new_params
        
class AdamOptimizer():
    def __init__(self):
        self.clear()
        
    def clear(self):
        self.it=0
        self.eps=1e-5
        self.vg=None
        self.vgs=None
        
    def iterate(self, grad, x, lr, beta_1=0.9, beta_2=0.999):
        self.it+=1
        params=x
        
        vg_previous=np.zeros((grad.size)) if self.it == 1 else self.vg
        self.vg=beta_1 * vg_previous + (1 - beta_1) * grad
        vgs_previous=np.zeros((grad.size)) if self.it == 1 else self.vgs
        self.vgs=beta_2 * vgs_previous + (1 - beta_2) * (grad ** 2)
        vg_=self.vg / (1 - beta_1 ** self.it)
        vgs_=self.vgs / (1 - beta_2 ** self.it)
        new_params=params - (lr * (1 / np.sqrt(vgs_ + self.eps)) * vg_)
        
        return new_params
      












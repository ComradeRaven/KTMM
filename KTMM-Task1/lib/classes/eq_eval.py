###########
# IMPORTS #
###########


# Math
import math
# Handy arrays
import numpy as np
# Custom modules
from lib.classes.mesh import Mesh
from lib.classes.config import Config

# For annotations
from numpy import ndarray


######################
# Equation Evaluator #
######################


class EquationEvaluator:
    """Holds equation parts and can evaluate it in given point t with given vector y.
    """
    
    def __init__(self, mesh: Mesh, config: Config, iters: int) -> None:
        # K_ij
        self.k = - mesh.intercestions_surfaces * config.therm_cond_coefs
        # Surfaces heat loss
        self.heat_loss = - 5.67 * config.eps * mesh.surfaces
        # Q_R
        self.q_r = config.q_r
        # Vector c
        self.c = config.c
        
        self.iters = iters
    
    
    def eval_equation(self, y, t) -> ndarray:
        """Evaluates task equation.

        Args:
            y (_type_): y vector.
            t (_type_): time point.
            mesh (Mesh): model.
            config (Config): config.

        Returns:
            dy.
        """
        
        # Q_TC
        q_tc = np.empty(self.k.shape)
        for i in range(q_tc.shape[0]):
            for j in range(q_tc.shape[1]):
                q_tc[i, j] = y[i] - y[j]
        q_tc *= self.k
        
        # Q_E
        q_e = self.heat_loss * (y/100)**4
        
        # Q_R
        q_r = eval(self.q_r, globals(), locals())
        
        if self.iters > 0:
            print(np.sum(q_tc, axis=1))
            print((np.sum(q_tc, axis=1) + q_e + q_r) / self.c)
            self.iters -= 1
        
        # Formula from docs
        return (np.sum(q_tc, axis=1) + q_e + q_r) / self.c
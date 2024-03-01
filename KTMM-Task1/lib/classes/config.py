###########
# IMPORTS #
###########


# Handy arrays
import numpy as np


########################
# Container for config #
########################


class Config:
    """Holds program config.
    """
    
    def __init__(self, eps: list, c: list, therm_cond_coefs: list, q_r: list):
        self.eps = np.array(eps)
        self.c = np.array(c)
        self.therm_cond_coefs = np.array(therm_cond_coefs)
        self.q_r = q_r
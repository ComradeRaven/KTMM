###########
# IMPORTS #
###########


# Handy arrays
import numpy as np


########################
# Container for config #
########################


class Config:
    """Holds program config."""
    
    def __init__(self, eps: list, c: list) -> None:
        self.eps = np.array(eps)
        self.c = np.array(c)
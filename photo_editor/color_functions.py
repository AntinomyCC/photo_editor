import numpy as np

def saturation_tuner(s_channel, t):
    return s_channel**np.exp(-t)
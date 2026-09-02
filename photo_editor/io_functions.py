import tkinter as tk
from tkinter import filedialog
import skimage as ski
import warnings
import numpy as np

def photo_path():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename() 
    return path

def photo_read(path):
    photo_rgb = ski.io.imread(path)
    if photo_rgb.ndim == 3 and photo_rgb.shape[2] == 4: # For .png format, discard the alpha dimension.
        photo_rgb_3D = photo_rgb[:,:,:3]
        photo_rgb = photo_rgb_3D #alpha dimension discarded, since the target of this software is photo. If someday it is needed, we can keep it instead.
        warnings.warn("Tested and removed alpha channel, only RGB channels remained.")
    elif photo_rgb.ndim == 3 and photo_rgb.shape[2] == 3: pass # For .jepg format.
    else: raise ValueError(f"Image type currently not supported")
    if photo_rgb.dtype != np.uint8: #If the photo is not a standard 8 bit rgb photo:
        raise ValueError(f"Data type {photo_rgb.dtype} not supported. Currently only support 8 bit rgb photo.")
    return photo_rgb

def photo_read_HEIC():
    pass

import numpy as np
from matplotlib import pyplot as plt
from photo_editor.color_functions import rgb_to_hsl, hsl_to_rgb, saturation_tuner,contrast_tuner
from photo_editor.io_functions import photo_path,photo_read,photo_read_HEIC 


class Photo:

    def __init__(self):
        self.path = None
        self.photo_rgb = None
        self.photo_hsl = None
        self.photo_rgb_output = None
        self.photo_adjusted = None
        self.params = {"saturation":0,
                       "contrast":1}

    def photo_read(self):
        self.path = photo_path()
        self.photo_rgb = photo_read(self.path)
    
    def photo_read_HEIC(self):
        pass

    def rgb_to_hsl(self):
        self.photo_hsl = rgb_to_hsl(self.photo_rgb)
        self.photo_adjusted = self.photo_hsl.copy()

    def hsl_to_rgb(self,photo_hsl):
        if photo_hsl is None:
            raise RuntimeError("No photo is loaded")
        return hsl_to_rgb(photo_hsl) # In order to avoid the adjusted rgb output cover the original rgb output. One can adjust it when it is used.

    def saturation(self,t):
        self.params["saturation"] = t
        self._recompute()

    def contrast(self,t):
        self.params["contrast"] = t
        self._recompute()

    def _recompute(self):
        if self.photo_hsl is None:
            raise RuntimeError("No photo is currently loaded")
        self.photo_adjusted[:,:,1] = saturation_tuner(self.photo_hsl[:,:,1],self.params["saturation"])
        self.photo_adjusted[:,:,2] = contrast_tuner(self.photo_hsl[:,:,2],self.params["contrast"])

def main():
    photo = Photo()
    photo.photo_read()
    photo.rgb_to_hsl()
    photo.saturation(-50)
    photo.contrast(20)
    adjusted_photo = photo.hsl_to_rgb(photo.photo_adjusted)

    plt.imshow(adjusted_photo)
    plt.show()

if __name__ == "__main__":
    main()  
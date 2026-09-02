import numpy as np
from matplotlib import pyplot as plt
from photo_editor.color_functions import rgb_to_hsl, hsl_to_rgb, saturation_tuner
from photo_editor.io_functions import photo_path,photo_read,photo_read_HEIC 


class Photo:

    def __init__(self):
        self.path = None
        self.photo_rgb = None
        self.photo_hsl = None
        self.photo_rgb_output = None
        self.photo_s_adjusted = None

    def photo_read(self):
        self.path = photo_path()
        self.photo_rgb = photo_read(self.path)
    
    def photo_read_HEIC(self):
        pass

    def rgb_to_hsl(self):
        #if self.photo_rgb is None:
        #   self.photo_read()
        self.photo_hsl = rgb_to_hsl(self.photo_rgb)

    def hsl_to_rgb(self,photo_hsl):
        if photo_hsl is None:
            raise RuntimeError("No photo is loaded")
        return hsl_to_rgb(photo_hsl) # In order to avoid the adjusted rgb output cover the original rgb output. One can adjust it when it is used.

    def saturation(self,t):
        if self.photo_hsl is None:
            raise RuntimeError("No photo is currently loaded as hsl format")
        self.photo_s_adjusted = self.photo_hsl.copy()
        self.photo_s_adjusted[:,:,1] = saturation_tuner(self.photo_hsl[:,:,1],t)

def main():
    photo = Photo()
    photo.photo_read()
    photo.rgb_to_hsl()
    photo.saturation(0.5)
    output_photo = photo.hsl_to_rgb(photo.photo_hsl)
    adjusted_photo = photo.hsl_to_rgb(photo.photo_s_adjusted)
   # photo_MSE = np.square(photo.photo_rgb - photo.photo_rgb_output)
    #print(photo.photo_rgb.dtype, photo.photo_rgb_output.dtype)
    diff = photo.photo_rgb.astype(float) - output_photo.astype(float)
    print(diff.min(), diff.max())  
    print(np.mean(diff**2))  
    print(id(photo.photo_rgb), id(output_photo))
    print(np.sum(diff != 0)) 
    print(np.unique(diff))    
    plt.imshow(adjusted_photo)
    plt.show()

if __name__ == "__main__":
    main()  
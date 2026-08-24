import numpy as np
import skimage as ski
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt
import warnings

def photo_path():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename() 
    return path

class Photo:

    def __init__(self, path):
        self.path = path
        self.photo_rgb = None
        self.photo_hsl = None
        self.photo_rgb_output = None

    def photo_read(self): # Use ski.io.imread to read the photo as np.ndarray, and store it as rgb photo.
        self.photo_rgb = ski.io.imread(self.path)
        if self.photo_rgb.ndim == 3 and self.photo_rgb.shape[2] == 4:
            photo_rgb_3D = self.photo_rgb[:,:,:3]
            self.photo_rgb = photo_rgb_3D
            warnings.warn("Tested and removed alpha channel, only RGB channels remained.")
        elif self.photo_rgb.ndim == 3 and self.photo_rgb.shape[2] == 3: pass
        else: raise ValueError(f"Image type currently not supported")
        if self.photo_rgb.dtype != np.uint8:
            raise ValueError(f"Data type {self.photo_rgb.dtype} not supported. Currently only support 8 bit rgb photo.")

            
    
    def photo_read_HEIC(self):
        pass

    def rgb_to_hsl(self): #convert the RGB format to HSL format, for following opreations.
        if self.photo_rgb is None:
            self.photo_read()          
        photo_rgb = self.photo_rgb

        photo_rgb_normalized = photo_rgb/255.0
        photo_hsl = np.zeros(photo_rgb.shape)

        min_rgb_normalized = np.min(photo_rgb_normalized, axis=2)
        max_rgb_normalized = np.max(photo_rgb_normalized, axis=2)
        idxmax_rgb_normalized = np.argmax(photo_rgb_normalized, axis=2)
        delta_rgb_normalized = max_rgb_normalized - min_rgb_normalized
        photo_hsl[:,:,2] = (min_rgb_normalized+max_rgb_normalized)/2
       # photo_hsl[:,:,2] = (min_rgb_normalized+max_rgb_normalized)/2 +0.01 #Final error test
        
        photo_hsl[:,:,0] = np.select([delta_rgb_normalized == 0, 
                   idxmax_rgb_normalized == 0, 
                   idxmax_rgb_normalized == 1, 
                   idxmax_rgb_normalized == 2
                   ],
                   [0.0,
                    60*(((photo_rgb_normalized[:,:,1]-photo_rgb_normalized[:,:,2])/delta_rgb_normalized)%6),
                    60*(((photo_rgb_normalized[:,:,2]-photo_rgb_normalized[:,:,0])/delta_rgb_normalized)+2),
                    60*(((photo_rgb_normalized[:,:,0]-photo_rgb_normalized[:,:,1])/delta_rgb_normalized)+4)
                    ])
        photo_hsl[:,:,1] = np.select([delta_rgb_normalized==0,
                                      photo_hsl[:,:,2] <= 0.5,
                                      photo_hsl[:,:,2] >0.5
                                      ],
                                      [0,
                                       delta_rgb_normalized/(max_rgb_normalized + min_rgb_normalized),
                                       delta_rgb_normalized/(2.0 - max_rgb_normalized - min_rgb_normalized)])
        self.photo_hsl = photo_hsl

    def hsl_to_rgb(self):
        photo_hsl = self.photo_hsl
        photo_rgb_output = np.zeros(photo_hsl.shape)

        c_hsl = (1.0 - np.abs(2.0 * photo_hsl[:,:,2] - 1.0)) * photo_hsl[:,:,1]
        x_hsl = c_hsl * (1 - np.abs((photo_hsl[:,:,0] / 60.0) % 2 - 1))
        m_hsl = photo_hsl[:,:,2] - c_hsl/2.0
        zeros_2d = np.zeros(m_hsl.shape)
        h_hsl_3d = np.stack((photo_hsl[:,:,0],photo_hsl[:,:,0],photo_hsl[:,:,0]),axis=2)
        photo_rgb_output = np.select([((h_hsl_3d >=0) & (h_hsl_3d < 60)),
                                      ((h_hsl_3d >=60) & (h_hsl_3d < 120)), 
                                      (h_hsl_3d >=120) & ((h_hsl_3d < 180)), 
                                      ((h_hsl_3d >=180) & (h_hsl_3d < 240)), 
                                      ((h_hsl_3d >=240) & (h_hsl_3d < 300)), 
                                      ((h_hsl_3d >=300) & (h_hsl_3d <= 360))

        ],
        [
            np.stack((c_hsl,x_hsl,zeros_2d),axis=2),
            np.stack((x_hsl,c_hsl,zeros_2d),axis=2),
            np.stack((zeros_2d,c_hsl,x_hsl),axis=2),
            np.stack((zeros_2d,x_hsl,c_hsl),axis=2),
            np.stack((x_hsl,zeros_2d,c_hsl),axis=2),
            np.stack((c_hsl,zeros_2d,x_hsl),axis=2)
        ])

        for i in [0,1,2]:
            photo_rgb_output[:,:,i] = np.round((photo_rgb_output[:,:,i] + m_hsl) * 255)
        photo_rgb_output = photo_rgb_output.astype(int)
        self.photo_rgb_output = photo_rgb_output

    def saturation_tuner(self):
        pass

class widgets:
    pass



def main():
    path = photo_path()
    photo = Photo(path)
    photo.rgb_to_hsl()
    photo.hsl_to_rgb()
   # photo_MSE = np.square(photo.photo_rgb - photo.photo_rgb_output)
    print(photo.photo_rgb.dtype, photo.photo_rgb_output.dtype)
    diff = photo.photo_rgb.astype(float) - photo.photo_rgb_output.astype(float)
    print(diff.min(), diff.max())  
    print(np.mean(diff**2))  
    print(id(photo.photo_rgb), id(photo.photo_rgb_output))
    print(np.sum(diff != 0)) 
    print(np.unique(diff))    
if __name__ == "__main__":
    main()  
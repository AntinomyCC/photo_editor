import numpy as np
import skimage as ski
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt

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

    def photo_read(self):
        photo_rgb = ski.io.imread(self.path)
        self.photo_rgb = photo_rgb
    
    def photo_read_HEIC(self):
        pass

    def convert_photo_to_hsl(self):
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
        
        photo_hsl[:,:,0] = np.select([delta_rgb_normalized == 0, 
                   idxmax_rgb_normalized == 0, 
                   idxmax_rgb_normalized == 1, 
                   idxmax_rgb_normalized == 2
                   ],
                   [0.0,
                    60*((photo_rgb_normalized[:,:,1]-photo_rgb_normalized[:,:,2])/delta_rgb_normalized)%6,
                    60*((photo_rgb_normalized[:,:,2]-photo_rgb_normalized[:,:,0])/delta_rgb_normalized)+2,
                    60*((photo_rgb_normalized[:,:,0]-photo_rgb_normalized[:,:,1])/delta_rgb_normalized)+4
                    ])
        photo_hsl[:,:,1] = np.select([delta_rgb_normalized==0,
                                      photo_hsl[:,:,2] <= 0.5,
                                      photo_hsl[:,:,2] >0.5
                                      ],
                                      [0,
                                       delta_rgb_normalized/(max_rgb_normalized + min_rgb_normalized),
                                       delta_rgb_normalized/(2.0 - max_rgb_normalized - min_rgb_normalized)])
        self.photo_hsl = photo_hsl
            
    def saturation_tuner(self):
        pass

class widgets:
    pass



def main():
    path = photo_path()
    photo = Photo(path)
    photo.photo_read()
    photo.convert_photo_to_hsl()
    plt.imshow(photo.photo_rgb  )
    plt.show()

if __name__ == "__main__":
    main()  
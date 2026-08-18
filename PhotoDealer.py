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
        red_channel = photo_rgb[:,:,0].astype(float)/255
        green_channel =photo_rgb[:,:,1].astype(float)/255
        blue_channel = photo_rgb[:,:,2].astype(float)/255 

        (pixels_vertical, pixels_horizontal)= red_channel.shape
        photo_hsl = np.zeros((pixels_vertical,pixels_horizontal,3)) # allocate the room for the converted photo. 

        for i in range(0,pixels_vertical):
            for j in range(0,pixels_horizontal):
                min = np.min([red_channel[i,j],green_channel[i,j],blue_channel[i,j]])
                max = np.max([red_channel[i,j],green_channel[i,j],blue_channel[i,j]])
                idxmax = np.argmax([red_channel[i,j],green_channel[i,j],blue_channel[i,j]])

                delta = max - min
                L = (min + max) /2
                photo_hsl[i,j,2] = L
                if delta == 0:
                    H = 0
                elif idxmax == 0:
                    H = 60 * (((green_channel[i,j] - blue_channel[i,j])/delta) % 6)
                elif idxmax == 1:
                    H = 60 * ((blue_channel[i,j] - red_channel[i,j]) / delta + 2)
                elif idxmax == 2:
                    H = 60 * ((red_channel[i,j] - green_channel[i,j]) / delta + 4)

                photo_hsl[i,j,0] = H 

                if delta == 0:
                    S = 0
                elif L <= 0.5:
                    S = delta/(max + min)
                else:
                    S = delta/(2 - max - min)

                photo_hsl[i,j,1] = S
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
    plt.imshow(photo.photo_hsl)
    plt.show()

if __name__ == "__main__":
    main()  
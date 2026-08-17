import numpy as np
import skimage as ski
import tkinter as tk
from tkinter import filedialog

class data_function:

    def photo_path(): # read the path of the photo
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename()
        return path

    def format_converter(path): # convert the format form HEIC to PNG(if need)
        pass

    def photo_array_convert(path): # convert png/jepg photos to numpy array
        photo = ski.io.imread(path)
        return photo #return photo as an arraylist


class analysis_function:

    def RGB_to_HSL(photo):
        red_channel = photo[:,:,0].astype(float)/255
        green_channel =photo[:,:,1].astype(float)/255
        blue_channel = photo[:,:,2].astype(float)/255

        (pixels_vertical, pixels_horizontal)= red_channel.shape
        photo_HSL = np.zeros((pixels_vertical,pixels_horizontal,3)) # allocate the room for the converted photo.

        for i in range(0,pixels_vertical):
            for j in range(0,pixels_horizontal):
                min = np.min([red_channel[i,j],green_channel[i,j],blue_channel[i,j]])
                max = np.max([red_channel[i,j],green_channel[i,j],blue_channel[i,j]])
                idxmax = np.argmax([red_channel[i,j],green_channel[i,j],blue_channel[i,j]])

                delta = max - min
                L = (min + max) /2
                photo_HSL[i,j,2] = L
                if delta == 0:
                    H = 0
                elif idxmax == 0:
                    H = 60 * (((green_channel[i,j] - blue_channel[i,j])/delta) % 6)
                elif idxmax == 1:
                    H = 60 * ((blue_channel[i,j] - red_channel[i,j]) / delta + 2)
                elif idxmax == 2:
                    H = 60 * ((red_channel[i,j] - green_channel[i,j]) / delta + 4)

                photo_HSL[i,j,0] = H 

                if delta == 0:
                    S = 0
                elif L <= 0.5:
                    S = delta/(max + min)
                else:
                    S = delta/(2 - max - min)

                photo_HSL[i,j,1] = S

        return photo_HSL

    def saturation_tuner(photo_HSL):
        pass

class widgets:
    pass



def main():

    photo = data_function.photo_path()
    photo_array = data_function.photo_array_convert(photo)
    photo_HSL = analysis_function.RGB_to_HSL(photo_array)
    #print(photo_HSL)
    photo_saturation_adjusted = analysis_function.saturation_tuner(photo_HSL)
    
main()
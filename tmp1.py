import numpy as np
'''
photo_rgb = np.array([[[255,0,0],[0,0,0]],
                        [[0,0,0],[255,0,0]]])
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
print(photo_hsl[:,:,0]    

test_image = np.array([
[1.0,0.0,0.0],
[1.0,0.0,0.0],
[1.0,1.0,0.0],
[1.0,1.0,0.0],
[1.0,0.5,0.0],
[1.0,0.99,0.0],
[1.0,0.99,0.0]])

'''
print(np.exp(-1e5))
print(np.exp(1e5))
print(0.99 ** np.exp(-1e5))
print(0.99 ** np.exp(1e5))

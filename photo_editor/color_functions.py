import numpy as np

def saturation_tuner(s_channel, t): 
    # Use the exponential function y = x^(exp(-t)) to create a projection for S from [0,1] to [0,1].
    # Use -t to align the direction of t slide and saturation change.
    return s_channel**np.exp(-t)

def contrast_tuner(l_channel, t):
    return np.clip((t*(l_channel-0.5)+0.5),0.0,1.0)

def hsl_to_rgb(photo_hsl):
    # Switch a hsl photo stored in 3d np array to rgb photo.
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
    return photo_rgb_output

def rgb_to_hsl(photo_rgb):
    # Switch a hsl photo stored in 3d np array to rgb photo.
    photo_rgb_normalized = photo_rgb/255.0
    photo_hsl = np.zeros(photo_rgb.shape)

    min_rgb_normalized = np.min(photo_rgb_normalized, axis=2)
    max_rgb_normalized = np.max(photo_rgb_normalized, axis=2)
    idxmax_rgb_normalized = np.argmax(photo_rgb_normalized, axis=2)
    delta_rgb_normalized = max_rgb_normalized - min_rgb_normalized
    photo_hsl[:,:,2] = (min_rgb_normalized+max_rgb_normalized)/2
    # photo_hsl[:,:,2] = (min_rgb_normalized+max_rgb_normalized)/2 +0.01 #Final error test
    with np.errstate(invalid='ignore'):
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
    return photo_hsl
from PhotoDealer import Photo
import pytest
import numpy as np

def test_RBG_to_HSL_red_and_black():
    #test RGB_to_HSL
    test_image = np.array([[[255,0,0],[0,0,0]],
                        [[0,0,0],[255,0,0]]])
    photo = Photo("fake path")
    photo.photo_rgb = test_image
    photo.convert_photo_to_hsl()

    #test the transform of red(255,0,0) pixel
    np.testing.assert_almost_equal(photo.photo_hsl[0,0,:],np.array([0.0,1.0,0.5]))
    #test the transform of black(0,0,0) pixel
    np.testing.assert_almost_equal(photo.photo_hsl[0,1,:],np.array([0.0,0.0,0.0]))

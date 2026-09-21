import numpy as np
from photo_editor.color_functions import contrast_tuner
import pytest

def test_contrast():
    #test 1: l = 0.5, regardless t it will give 0.5.
    #test 2: t = 1, the result will keep unchange.
    #test 3: when the result is over 1 it will be cliped to 1.(also smaller than 0 it will be clipped to 0)
    test_image = np.array([0.5,0.8,0.9])
    test_t_value = np.array([123, 1.0, 3.0])
    result = contrast_tuner(test_image,test_t_value)
    test_answer = np.array([0.5,0.8,1.0])
    np.testing.assert_array_equal(result,test_answer)

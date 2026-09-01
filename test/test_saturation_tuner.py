import numpy as np
from PhotoDealer import saturation_tuner
import pytest

def test_saturation_exact():

    test_image_exact = np.array([0.0,0.0,1.0,1.0,0.5])
    test_t_values_exact = np.array([0.0,0.5,0.0,0.5,0.0])
    expected_image_exact = np.array([0.0,0.0,1.0,1.0,0.5])
    result_exact = saturation_tuner(test_image_exact, test_t_values_exact)

   
    np.testing.assert_array_equal(result_exact,expected_image_exact)

def test_saturation_approx():
    large_number = 100.0

    test_image_approx = np.array([0.99,0.99])
    test_t_values_approx =np.array([large_number,-large_number])
    expected_image_approx = np.array([1.0,0.0])
    result_approx = saturation_tuner(test_image_approx,test_t_values_approx)

    np.testing.assert_almost_equal(result_approx,expected_image_approx)

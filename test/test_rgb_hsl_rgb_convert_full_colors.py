from photo_editor.photo import Photo
import numpy as np
import pytest
def test_rgb_hsl_rgb_convert():
    r, g, b = np.meshgrid(
    np.arange(256, dtype=np.uint8),
    np.arange(256, dtype=np.uint8),
    np.arange(256, dtype=np.uint8),
    indexing='ij'
    )

    all_rgb_array = np.stack([r, g, b], axis=-1).reshape(4096, 4096, 3)

    photo = Photo.photo_read()
    photo.photo_rgb = all_rgb_array
    photo.rgb_to_hsl()
    photo.hsl_to_rgb()

    diff = photo.photo_rgb.astype(float) - photo.photo_rgb_output.astype(float)
    zero = np.zeros_like(diff)
    np.testing.assert_array_equal(diff,zero)
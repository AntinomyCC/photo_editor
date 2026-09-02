from PhotoDealer import Photo, photo_path
from PIL import Image
import numpy as np

def main():

    r, g, b = np.meshgrid(
    np.arange(256, dtype=np.uint8),
    np.arange(256, dtype=np.uint8),
    np.arange(256, dtype=np.uint8),
    indexing='ij'
)

# 2. 堆叠并重构形状为 (4096, 4096, 3) 的图像矩阵
    all_rgb_array = np.stack([r, g, b], axis=-1).reshape(4096, 4096, 3)

# 3. 转换为 PIL Image 对象（如果你的代码接受 PIL Image 作为输入）
    #all_rgb_image = Image.fromarray(all_rgb_array)

    path = "test path"
    photo = Photo(path)
    photo.photo_rgb = all_rgb_array
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
# https://github.com/scikit-image/scikit-image/issues/4509
# https://github.com/scikit-image/scikit-image/issues/3819

from skimage import img_as_ubyte
from skimage.io import imsave, imread
from skimage.transform import resize

original_image_path = './src/scripts/data/bridge.jpeg'
otuput_renamed_image_path = './src/scripts/data/bridge-new.jpeg'
otuput_resized_image_path = './src/scripts/data/bridge-100x100.jpeg'
otuput_converted_image_path = './src/scripts/data/bridge.png'

# read original image
original = imread(original_image_path)
print(original[0, 0], "Original loaded image", original.dtype)

# copy original image
ubyte_original = img_as_ubyte(original)
imsave(otuput_renamed_image_path, ubyte_original)
print(ubyte_original[0, 0], "Renamed image ubyte", ubyte_original.dtype)
renamed_image = imread(otuput_renamed_image_path)
print(renamed_image[0, 0], "Reloaded renamed image", renamed_image.dtype)

# resize image to 100x100px
resized = resize(original, (100, 100, 3))
print(resized[0, 0], "Resized image", resized.dtype)
ubyte_resized_image = img_as_ubyte(resized)
imsave(otuput_resized_image_path, ubyte_resized_image)
print(ubyte_resized_image[0, 0], "Resized image as ubyte", ubyte_resized_image.dtype)

# reload resized image
resized_reloaded = imread(otuput_resized_image_path)
print(resized_reloaded[0, 0], "Reloaded resized image", resized_reloaded.dtype)

# convert image to PNG
imsave(otuput_converted_image_path, ubyte_original)

# reload converted image
converted_reloaded = imread(otuput_converted_image_path)
print(converted_reloaded[0, 0], "Reloaded converted image", converted_reloaded.dtype)


""" Output
[14  7  0] Original loaded image uint8
[14  7  0] Renamed image ubyte uint8
[15  7  0] Reloaded renamed image uint8
[0.13098039 0.13788235 0.07843137] Resized image float64
[33 35 20] Resized image as ubyte uint8
[41 46 14] Reloaded resized image uint8
[14  7  0] Reloaded converted image uint8
"""
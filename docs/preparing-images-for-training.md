## Preparing images for training

The model is not trained directly with raw images.

Raw images have different sizes. This is a sample raw image of 240x160px.

![Raw golf ball iamge](images/raw-golf-ball-image.jpeg)

In the train.py all images are resized to 100x100px and them reshaped.

The resized version of the previous image is:

![Raw golf ball iamge](images/raw-golf-ball-image-resized.png)

100x100px.

To train the model, we need to process the raw images. There are two steps for image normalization. First, we resize them to 100x100px and then we reshape them. The code to do that is:

```
def resize_and_reshape(image):
    return im_reshape(im_resize(image))

def im_resize(image):
    # resize doc: https://scikit-image.org/docs/stable/api/skimage.transform.html?highlight=resize#resize
    return resize(image, (100, 100, 3))

def im_reshape(image):
    # reshaped doc: https://numpy.org/doc/stable/reference/generated/numpy.reshape.html#numpy-reshape
    return image.reshape((1, 30000))
```

The images are previously loaded using skimage.[imread](https://scikit-image.org/docs/dev/api/skimage.io.html#skimage.io.imread) method.

We wanted to cache the resized images. The idea was simple: save the images after resize them and use them later for the training so that you do not need to resize them again and again. The script to resize images is `src/prepare_images.py`. We are not going to explain it because it's small. We only get the raw image, we calculate the new path for the resized image and save it. That part was easy, but when we tried to train the model with the newly resized images, it did not work at all!. We created an issue and spent a lot of time trying to find out why.

This is the issue: [The model is not working using pre-resized images](https://github.com/josecelano/data-version-control/issues/2)

We were trying to find out why the model did not work. We find out that after resizing the image, the internal image format changed.

Skimage uses `numpy` arrays with different data types and ranges: [Skimage image data types](https://scikit-image.org/docs/dev/user_guide/data_types.html#image-data-types-and-what-they-mean)

After resizing the image, its internal data type changes from `uint8` to `float64`. That was the first surprise. It seems skimage automatically changes the internal data type after applying some transformations. You can read it in their documentation:

>"Functions in skimage are designed so that they accept any of these `dtypes` but for efficiency, may return an image of a different `dtype` (see Output types)."

Anyway, we thought that could not be the problem. We tried saving and reloading a single image, and the second surprise was we did not get back the same data. We were also using JPEG format for the resized image.

In the beginning, we thought the problem was we were losing precision, saving the image as JPEG. So we decided to use PNG, but that did not fix the problem. The resized image uses `float64`, and the saved image in JPEG uses `uint8`. The idea came up after reading some complaints like [this](https://stackoverflow.com/questions/47361966/scikit-image-write-a-ndarray-to-image-with-imsave-read-back-with-imread-data)). There are some issues on different repositories because people do not expect an image to change if you only save it and reload it.

We continued trying other approaches. We tried to save the image using the `float64` after reading this page ["Save numpy array as image with high precision (16 bits) with scikit-image"](https://www.py4u.net/discuss/142943). We discarded this option. Instead of trying to find a quick fix, we decided to run some small examples to understand better how skimage handles the images internally. We created this script `src/scripts/resize_image_and_convert_to_png.py` to run some tests. That script only loads and saves an original JPEG image with different sizes and formats. We found out that even only renaming and saving the file it produces a different numpy array when we reload the image. Surprisingly, if we save the image as PNG and we reload it, we do get the same exact numpy array (at list the first value).

This way, we confirmed that we were reloading the right image (even if the numpy array was not exactly the same). So the problem should be somewhere else.

After thinking for a while we decided to make a small test: resize again the already resized image to the same size(100x100px) and it surprisingly worked!!.

It seems that the model is expecting a `float64` value. We have not confirmed it yet, but at least we get again back the initial accuracy (0.8124207858048162) for the model but using the resized images instead of raw images.

We also added the resized images to DVC.

According to GitHub Action times, the training time has decreased from 36s to 23s.

The goal was not to improve the performance. We want to use this task (generate cache for resized images) as a sample task to create a GitHub Action. Although we will probably need some refactors to the script. 
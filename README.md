[![Build the model](https://github.com/josecelano/data-version-control/actions/workflows/main.yml/badge.svg)](https://github.com/josecelano/data-version-control/actions/workflows/main.yml)

[![Resize image using conda](https://github.com/josecelano/data-version-control/actions/workflows/resize-image-conda.yml/badge.svg)](https://github.com/josecelano/data-version-control/actions/workflows/resize-image-conda.yml)

[![Resize image using GitHub Action](https://github.com/josecelano/data-version-control/actions/workflows/resize-image-with-action.yml/badge.svg)](https://github.com/josecelano/data-version-control/actions/workflows/resize-image-with-action.yml)

# Data Version Control Tutorial

Example repository for the [Data Version Control With Python and DVC](https://realpython.com/python-data-version-control/) article on [Real Python](https://realpython.com/).

To use this repo as part of the tutorial, you first need to get your own copy. Click the _Fork_ button in the top-right corner of the screen, and select your private account in the window that pops up. GitHub will create a forked copy of the repository under your account.

Clone the forked repository to your computer with the `git clone` command

```console
git clone git@github.com:YourUsername/data-version-control.git
```

Make sure to replace `YourUsername` in the above command with your actual GitHub username.

Happy coding!

# Custom features for this fork

This is a fork from a tutorial example repo. I'm adding some new features like an script to classify images using the generated model.
For more details read the original tutorial.

* Tutorial: https://realpython.com/python-data-version-control/
* Original repo: https://github.com/realpython/data-version-control

## Install

```
git clone git@github.com:josecelano/data-version-control.git
cd data-version-control
conda create --name dvc python=3.8.2 -y
conda config --add channels conda-forge
conda install dvc scikit-learn scikit-image pandas numpy
```

Alternatively you can create the conda environment with:

```
conda env create --file environment.yml
```

## Run

```
conda activate dvc
```

Generate csv files:
```
python3 src/prepare.py
```

Resize images to 100x100 and convert them to PNG format:
```
python3 src/prepare_images.py
```
The model can be trained with raw images or pre-processed images and use them. For the time being both options are hardcoded in train.py file.
The default option is from pre-resized images.

Train the model:
```
python3 src/train.py
```

Evaluate the model with the test set:
```
python3 src/evaluate.py && cat metrics/accuracy.json 
```

User the model to classify the image:
```
python3 src/predict.py
```

Sample output for predict.py script:
```
(dvc) josecelano@josecelano:~/Documents/github/josecelano/data-version-control$ python src/predict.py -i /home/josecelano/Documents/github/josecelano/data-version-control/data/raw/train/n03888257/n03888257_24024.JPEG
Predicting for image: " /home/josecelano/Documents/github/josecelano/data-version-control/data/raw/train/n03888257/n03888257_24024.JPEG "
['parachute']
```

This could be a golden test if you change something:
```
python src/train.py && python src/evaluate.py && cat metrics/accuracy.json
```
Accuracy should be almost the same. The trainning process is not deterministic.

## Run workflow locally

We are using [act](https://github.com/nektos/act) to run GitHub Actions locally.

`act` usage:
```
act -h
```

Run workflow locally:
```
act -j build --secret-file .env
```
With the `j` you can run only a single job.

Don't forget to add your Azure Blog Storage credentials to pull images from remote DVC storage. Otherwise you will get this error:

```
| ERROR: failed to pull data from the cloud - Authentication to Azure Blob Storage requires either account_name or connection_string.
| Learn more about configuration settings at <https://man.dvc.org/remote/modify>
[Build the model/build]   ❌  Failure - Pull dataset from remote
```

## Run workflow on GitHub

You need to add the secrets in `.env.ci` file:

```
AZURE_STORAGE_ACCOUNT='YOUR_STORAGE_ACCOUNT_NAME'
AZURE_STORAGE_KEY='YOUR_STORAGE_KEY'
```

## New content

* [Add remote storage using Azure Blog Storage](docs/azure-blob-storage.md).
* [Basic workflow: pull dataset, train the model, evaluate the model and make some predictions](docs/basic-workflow-with-dvc.md)
* [Preparing images for training](docs/preparing-images-for-training.md)
* [GitHub Action: skimage-resizer](docs/github-action-skimage-resizer.md)

## Links

* [Random forest Algorithm](https://inblog.in/Random-forest-r7gFle7V8L)

## Troubleshooting

* [Troubleshooting](docs/troubleshooting.md)

## TODO

* Cache for DVC cache? We have to pull the whole dataset on every pipeline.
* Consider docker instead of `conda` setup? maybe faster?.
* Refactor `prepare_images.py` script. How could be easily converted to GitHub Action in the future?
* Use GitHub cache for DVC local cache `.dvc\cache`?
* It seems `conda` cache it's not working. See issue [#1](https://github.com/josecelano/data-version-control/issues/1).
* Make the pipeline fail if the accuracy of the model decreases.
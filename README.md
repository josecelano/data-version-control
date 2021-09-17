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

Train the model:
```
python3 src/train.py
```

Evaluate the model with the test set:
```
python3 src/evaluate.py
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

## Run workflow locally

We are using [act](https://github.com/nektos/act) to run GitHub Actions locally.

```
act -j build --secret-file .env
```

Don't forget to add your Azure Blog Storage credentials to pull images from remote DVC storage.

## Run workflow on GitHub

You need to add the secrets in `.env.ci` file:

```
AZURE_STORAGE_ACCOUNT='YOUR_STORAGE_ACCOUNT_NAME'
AZURE_STORAGE_KEY='YOUR_STORAGE_KEY'
```

## New content

* [Add remote storage using Azure Blog Storage](docs/azure-blob-storage.md)
* Basic workflow: pull dataset, train the model, evaluate the model¡ and make some predictions.

## TODO

* Write article for basic workflow.
* Cache for DVC cache? We have to pull the whole dataset on every pipeline.
* Consider docker insted of conda setup? maybe faster?
* Update README to use conda environment.yml for installation
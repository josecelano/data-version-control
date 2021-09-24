# Skimage Resizer

Image resizer using [scikit-image](https://scikit-image.org/). A Python image processing library.

## Usage

Describe how to use your action here.

### Example workflow

```yaml
name: My Workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - name: Run action
      uses: ./.github/actions/skimage-resizer

```



### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myInput`  | An example mandatory input    |
| `anotherInput` _(optional)_  | An example optional input    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `myOutput`  | An example output (returns 'Hello world')    |

### Development

Build docker image:
```
docker build -t skimage-resizer .
```

Run locally with docker:
```
docker run -it \
  --env INPUT_SOURCE_IMAGE_PATH=/github/workspace/src/scripts/data/bridge.jpeg \
  --env INPUT_RESIZED_IMAGE_PATH=/github/workspace/src/scripts/data/bridge-100x100.jpeg \
  --env INPUT_ROWS=100 \
  --env INPUT_COLS=100 \
  --env INPUT_DIM=3 \
  --volume $(pwd):/github/workspace \
  skimage-resizer
```
See: https://docs.github.com/en/actions/creating-actions/dockerfile-support-for-github-actions#workdir

Sample usage without docker:
```
INPUT_SOURCE_IMAGE_PATH=src/scripts/data/bridge.jpeg \
INPUT_RESIZED_IMAGE_PATH=src/scripts/data/bridge-100x100.jpeg \
INPUT_ROWS=100 \
INPUT_COLS=100 \
INPUT_DIM=3 \
python .github/actions/skimage-resizer/main.py
```

Run action using `act`:
```
act -j resize_with_github_action
```

Delete previous built docker image when `act` is used (the container iamge is cached):
```
docker image rm act-github-actions-skimage-resizer
```
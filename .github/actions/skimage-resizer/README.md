# Skimage Resizer

Image resizer using [scikit-image](https://scikit-image.org/). A Python image processing library.

## Usage

You just need to add the action in your workflow:

```yaml
- name: Run action
  uses: ./.github/actions/skimage-resizer
  with:
    source_image_path: ${{ github.workspace }}/src/scripts/data/bridge.jpeg
    resized_image_path: ${{ github.workspace }}/src/scripts/data/bridge-100x100.jpeg
    rows: 100
    cols: 100
    dim: 3
```

The action is only a wrapper of the [skimage.resize()](https://scikit-image.org/docs/dev/api/skimage.transform.html#skimage.transform.resize) function. We only use the `output_shape` parameter.

> Size of the generated output image (rows, cols[, …][, dim]). If dim is not provided, the number of channels is preserved. In case the number of input channels does not equal the number of output channels a n-dimensional interpolation is applied.

### Inputs

| Input                | Description                          |
|----------------------|--------------------------------------|
| `source_image_path`  | Source image path                    |
| `resized_image_path` | Resized image path                   |
| `rows`               | Width                                |
| `cols`               | Heigth                               |
| `dim`                | Dim parameter in output_shape tuple  |

### Outputs

No outputs.

### Development

Build docker image:
```
docker build -t skimage-resizer .
```

Run it locally with docker:
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

Run it locally without docker:
```
INPUT_SOURCE_IMAGE_PATH=src/scripts/data/bridge.jpeg \
INPUT_RESIZED_IMAGE_PATH=src/scripts/data/bridge-100x100.jpeg \
INPUT_ROWS=100 \
INPUT_COLS=100 \
INPUT_DIM=3 \
python .github/actions/skimage-resizer/main.py
```
You can use your pre-activated conda environment to run the script if the dependencies are the same.

Run action using `act`:
```
act -j resize_with_github_action
```
If you run the GitHub action locally the image will be resized but you will not see the output image in you disk. See [Troubleshooting Section](#Troubleshooting).

If you run the GitHub action locally with `act`, the docker image is built only once. If you change something in the action you need to re-build the docker image and delete the old one:
```
docker image rm act-github-actions-skimage-resizer && docker build -t skimage-resizer .
```

### Notes

* We use `root` user in `Dockerfile` because GitHub recommends doing it: https://docs.github.com/en/actions/creating-actions/dockerfile-support-for-github-actions#user

### Troubleshooting

#### Output image not generated using `act` locally

When you run the action locally using `act` you can't see the output image. There is no problem creating the image but the image is not copied to the docker host folder. Probably that's because `act` is not mounting a volumne when it runs the docker action in the nested docker image. The action works on GitHub, the image is generated on the runner and we even generate an artifact that you can download.

These are the commands runned by GitHub on the runner:

Docker build:
```
/usr/bin/docker build -t e1cc51:b909f635dcb454fc4cb2897fad8eb2b9 -f "/home/runner/work/data-version-control/data-version-control/./.github/actions/skimage-resizer/Dockerfile" "/home/runner/work/data-version-control/data-version-control/.github/actions/skimage-resizer"
```

Docker run:
```
/usr/bin/docker run --name e1cc51b909f635dcb454fc4cb2897fad8eb2b9_6d9360 \
 --label e1cc51 \
 --workdir /github/workspace \
 --rm
 -e INPUT_SOURCE_IMAGE_PATH
 -e INPUT_RESIZED_IMAGE_PATH
 -e INPUT_ROWS
 -e INPUT_COLS
 -e INPUT_DIM
 -e HOME
 -e GITHUB_JOB
 -e GITHUB_REF
 -e GITHUB_SHA
 -e GITHUB_REPOSITORY
 -e GITHUB_REPOSITORY_OWNER
 -e GITHUB_RUN_ID
 -e GITHUB_RUN_NUMBER
 -e GITHUB_RETENTION_DAYS
 -e GITHUB_RUN_ATTEMPT
 -e GITHUB_ACTOR
 -e GITHUB_WORKFLOW
 -e GITHUB_HEAD_REF
 -e GITHUB_BASE_REF
 -e GITHUB_EVENT_NAME
 -e GITHUB_SERVER_URL
 -e GITHUB_API_URL
 -e GITHUB_GRAPHQL_URL
 -e GITHUB_WORKSPACE
 -e GITHUB_ACTION
 -e GITHUB_EVENT_PATH
 -e GITHUB_ACTION_REPOSITORY
 -e GITHUB_ACTION_REF
 -e GITHUB_PATH
 -e GITHUB_ENV
 -e RUNNER_OS
 -e RUNNER_NAME
 -e RUNNER_TOOL_CACHE
 -e RUNNER_TEMP
 -e RUNNER_WORKSPACE
 -e ACTIONS_RUNTIME_URL
 -e ACTIONS_RUNTIME_TOKEN
 -e ACTIONS_CACHE_URL
 -e GITHUB_ACTIONS=true
 -e CI=true
 -v "/var/run/docker.sock":"/var/run/docker.sock"
 -v "/home/runner/work/_temp/_github_home":"/github/home"
 -v "/home/runner/work/_temp/_github_workflow":"/github/workflow"
 -v "/home/runner/work/_temp/_runner_file_commands":"/github/file_commands"
 -v "/home/runner/work/data-version-control/data-version-control":"/github/workspace" e1cc51:b909f635dcb454fc4cb2897fad8eb2b9
```

As you can see the runner mounts the source code as a volume inside the docker action container:

```
-v "/home/runner/work/data-version-control/data-version-control":"/github/workspace" 
``` 
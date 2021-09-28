## GitHub ACtion: skimage-resizer

In a previous article, we created a workflow task to resize a single image using the image processing library [scikit-image](https://scikit-image.org/).

And this is how you you can use the script in a workflow:
```yml
- name: Setup Conda
  uses: conda-incubator/setup-miniconda@v2
  with:
    miniconda-version: "latest"
    auto-update-conda: false
    python-version: '3.8'
    activate-environment: resize-image-action
    environment-file: src/actions/resize_image/environment.yml

...

- name: Resize sample image
  run: python src/actions/resize_image/resize_image.py -i src/scripts/data/bridge.jpeg -o src/scripts/data/bridge-100x100.jpeg -r 100 -c 100 -d 3
```

As you can see, we need to set up the Python virtual environment berofe calling the script. This approach has some pros and cons.

Pros:

* You don't need to use docker. That means you can avoid double virtualization. That could be slower.
* If all your actions use the same Python environment, you only need to set up the environment once and save a lot of time.

Cons:

* If all your actions have different dependencies, you might end up needing a different environment for each action. If you only use one environemnt, you could end up having a dependency mess. That means you can end up not knowing which action is using a given dependency. Of course, you could find a way to store that information, but extracting and reusing one action is probably going to be very hard.
* When you use the action, you always have to set up the environment before using the actual action. That could be pretty annoying or slow if you are constantly switching between different environments.
* Even if it takes time to build docker images, it also takes time to create virtual Python environments with [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-environments) or [venv](https://docs.python.org/3/library/venv.html#module-venv).

Conclusion:

This approach could be convenient if you have a lot of actions that have the same dependencies and are not going to be reused outside of the repository.

In this article, we are going to explain the alternative approach: GitHub Action with docker. GitHub Action only supports `nodejs` actions natively. If you want to use a different language, you need to use docker. We are going to explain how we created the same action to resize an image but using a GitHub Action. In the end, we will use it in a workflow like this:

```yml
- name: Run action
  uses: ./.github/actions/skimage-resizer
  with:
    source_image_path: ${{ github.workspace }}/src/scripts/data/bridge.jpeg
    resized_image_path: ${{ github.workspace }}/src/scripts/data/bridge-100x100.jpeg
    rows: 100
    cols: 100
    dim: 3
```          

GitHub allows you to embed actions in the same repo where you use them. You do not need to publish them in the marketplace or even create an independent repo. You can add your action in the `.github/actions/` and `use` them as a step in a workflow (with the relative path).

What GitHub and `act` do is building the docker image and then run it.

To create your custom action, you need two things: the action configuration file (`action.yml`) and your docker image (`Dockerfile` and your action code).

### action.yml

Our action file is very simple:

```
name: "Skimage Resizer"
description: "Image resizer using Python package scikit-image"
author: "Jose Celano"
inputs:
  source_image_path:
    description: "Source image path"
    required: true
  resized_image_path:
    description: "Resized image path"
    required: true
  rows:
    description: "Rows"
    required: true
  cols:
    description: "Cols"
    required: true
  dim:
    description: "Dim"
    required: true
runs:
  using: "docker"
  image: "Dockerfile"
```

We declare the inputs and we tell GitHub we are going to use a docker action.

We have the same arguments that we were using in the previous "inline" action sample using `conda`.

### Dockerfile

Since the sample it's very simple, our `Dockerfile` it's also very simple:

```dockerfile
FROM python:3-slim AS builder
ADD ./src /src
WORKDIR /src
# We are installing a dependency here directly into our app source dir
RUN pip install --target=/src scikit-image

FROM python:3-slim
COPY --from=builder /src /src
WORKDIR /src
ENV PYTHONPATH /src
CMD ["python", "/src/app/gh-action/main.py"]
```

We started using this template repo to build the action: https://github.com/jacobtomlinson/python-container-action/blob/master/Dockerfile, but we had problems to install `skimage` package on the source docker image: [gcr.io/distroless/python3-debian10](https://github.com/GoogleContainerTools/distroless)

These are some templates to build GitHub Action with Python:

* https://github.com/cicirello/python-github-action-template
* https://github.com/jacobtomlinson/python-container-action

Once we have the dependencies and the `action.yml` file, we only need to write the action code.

### Writing Python code for the action

Before writing the action we defined some requirements:

* Even if we are planning to use GitHub Actions we wanted the core action code to be decouple from GitHub Actions so that we could reuse the same code in another CI platform like for example GitLab in the future. That means we have to decouple the code to extract arguments from the core action code to resize the image.
* We also wanted to execute the action directly as a console application. This way we can easily run it locally on development environment with any external dependency or even use it with other CI systems. GitHub uses env variables in order to pass arguments to the action. That makes sense but sometimes using the script passing arguments could be a better option.
* Of course, the action should be executed locally using `act` but that's something you have by default if you implement an standard GitHub Action. But surprisinly we find out that the action we built works perfectly on the GitHub runner, but it does not work perfectly with `act`. If you run it with `act` the output image is not copied to you hard disk from inside the container. It seems the `act` docker image we are using does not mount any volume on the nested docker image.

The final action folder strcuture was:

```shell
.
├── action.yml
├── Dockerfile
├── LICENSE
├── README.md
└── src
    ├── app
    │   ├── console
    │   │   └── main.py
    │   └── gh-action
    │       └── main.py
    ├── shared
    │   └── resize_image_handler.py
    └── tests
        └── fixtures
            └── bridge.jpeg
```

On the top layer we have two applications (UI layer). One application is the consle app and the other application is the GitHub Action. Both of them share the same login to resize the image `resize_image_handler`. The rules for the designa are:

* `resize_image_handler` should not know any detail about who is calling it and from where (console, GitHub runner).
* Each application should not know the ohter application implementation.

The code for the console app is very simple. We used argparse to extract the arguments from the command line:

```python
import argparse

from shared.resize_image_handler import resize_image_handler


def init_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True,
                        help="source image path")
    parser.add_argument('-o', '--output', required=True,
                        help="resized image path")
    parser.add_argument('-r', '--rows', required=True,
                        type=int, help="resized image width")
    parser.add_argument('-c', '--cols', required=True,
                        type=int, help="resized image heigth")
    parser.add_argument('-d', '--dim', required=True, type=int)
    return parser


def main():
    parser = init_argparse()
    args = parser.parse_args()

    resize_image_handler(args.input, args.output,
                         (args.rows, args.cols, args.dim))


if __name__ == "__main__":
    main()
```

You can use the app like this:

```shell
  python /src/app/console/main.py \
    --input ./tests/fixtures/bridge.jpeg \
    --output ./tests/fixtures/bridge-100x100.jpeg \
    -r 100 \
    -c 100 \
    -d 3
```

The GitHub is also pretty straightforward:

```python
import os
import sys

from shared.resize_image_handler import resize_image_handler


def parse_output_shape():
    rows = int(os.environ["INPUT_ROWS"])
    cols = int(os.environ["INPUT_COLS"])
    dim = int(os.environ["INPUT_DIM"])
    return (rows, cols, dim)


def main():
    source_image_path = os.environ["INPUT_SOURCE_IMAGE_PATH"]
    resized_image_path = os.environ["INPUT_RESIZED_IMAGE_PATH"]
    output_shape = parse_output_shape()

    resize_image_handler(source_image_path, resized_image_path, output_shape)

    output = f"Resized image {resized_image_path}"
    print(output)


if __name__ == "__main__":
    main()
```

You could also use it from console:

```shell
export INPUT_SOURCE_IMAGE_PATH=./tests/fixtures/bridge.jpeg && \
export INPUT_RESIZED_IMAGE_PATH=./tests/fixtures/bridge-100x100.jpeg && \
export INPUT_ROWS=100 && \
export INPUT_COLS=100 && \
export INPUT_DIM=3 && \
python /src/app/gh-action/main.py
```

## Performance

We implemented the same action with two defirrent approaches:

1. [Using conda to install our Python version and our actions dependencies](https://github.com/josecelano/data-version-control/actions/workflows/resize-image-with-action.yml)
2. [This example using a docker image](https://github.com/josecelano/data-version-control/actions/workflows/resize-image-conda.yml)

Surprisingly it takes the same time for both workflows to fisnish: 1m 19s (conda), 1m 2s (GH action).

* Setup conda and resize the image: 61s
* Build the docker image and resize the image: 44s

The docker version is a litle bit faster. We are not considering cache, neither for conda ([which seems not to work properly yet](https://github.com/josecelano/data-version-control/issues/1)) nor docker.

It is supposed you should be able to use cache is both cases. See links at the end of this article.

### Alternatives to docker with Python

[Peter Evans](https://github.com/peter-evans) has developed a [JavaScript wrapper for Python actions](https://github.com/peter-evans/python-action). Basically the approach is similar to the `conda` approach becuase you have to install the Python version and dependencies you need. He saids this approach has some advantages in comparison with using docker:

1. Currently container actions are not multi-platform. You can only run them on linux virtual machines.
2. Container actions using image: 'Dockerfile' are slow because they need to build the image from scratch every time the workflow runs.
3. Container actions using image: 'docker://my-namespace/my-image:1.0.0' cannot be forked easily because the reference to the public Docker image remains. Being able to fork GitHub actions is important for security conscious users.

Regarding point 1 that depends on your project needs.
Regarding point 2, as we have seen it probably depends on how you set up the cache.
And finally regarding point 3, I suppose he means you can use a [public the docker image in the task](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions#example-using-public-docker-registry-container):

```
runs:
  using: 'docker'
  image: 'docker://debian:stretch-slim'
```

In that case, you do not need to build the image. I don not understand why he saids you cannot fork the action. I suppose that could only happen if you create an action with a dockerfile, you publish the image and you use it that way. In that case you could not have access to the original repo if it's not public, but I do not thing it a docker problem but the wey you implemnt the action with docker.

### Conclusions

We have implemented 2 different ways to resize an image:

1. [Stardard Python with conda](https://github.com/josecelano/data-version-control/blob/master/.github/workflows/resize-image-conda.yml)
2. [Docker GitHub Action](https://github.com/josecelano/data-version-control/blob/master/.github/workflows/resize-image-with-action.yml)

Which one is the best approach depends on the concrete actions you are going to implement. Maybe it makes snese to apply the first approach if you consider the action as an small part of a CI application which is tiggly couple to the repo logic. That means you probably will not use that piece of code in another repository. An example for that case could be sending a notification when something happens in the repo. For exmple: we could email the repo owner every time we resize an image with an email template. If you have a lot of these kind of action, it could make sense to consider all of them as small command belonging to the whole CI application, like a console application.

The second approach seems to be more useful when you are building totally independent funtionalities. For example, extracting the list of changed files in a pull request. In our example, we could need to get the list of new iamges in a pull request in order to resize all of them. The sample action (image resizer) is also a good candidate for a GitHub Actions.

### Links

* The official documentation for the [action metadata file](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions).
* [Build images on GitHub Actions with Docker layer caching](https://evilmartians.com/chronicles/build-images-on-github-actions-with-docker-layer-caching)
* [Docker Layer Caching in GitHub Actions](https://github.com/marketplace/actions/docker-layer-caching)
* [Caching Docker builds in GitHub Actions: Which approach is the fastest? 🤔 A research](https://dev.to/dtinth/caching-docker-builds-in-github-actions-which-approach-is-the-fastest-a-research-18ei)
* https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions#jobsjob_idcontainerimage
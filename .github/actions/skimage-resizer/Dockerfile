FROM python:3-slim AS builder
ADD ./src /src
WORKDIR /src
# We are installing a dependency here directly into our app source dir
RUN pip install --target=/src scikit-image geometry

FROM python:3-slim
COPY --from=builder /src /src
WORKDIR /src
ENV PYTHONPATH /src
CMD ["python", "/src/app/gh-action/main.py"]
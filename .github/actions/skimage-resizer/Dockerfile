FROM python:3-slim AS builder
ADD ./src /app
WORKDIR /app
# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app scikit-image geometry

FROM python:3-slim
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["python", "/app/main.py"]
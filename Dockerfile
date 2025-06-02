FROM python:3.11-slim as builder

LABEL org.opencontainers.image.authors="Patryk Kaniosz"

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip uninstall -y setuptools && \
    pip install setuptools==78.1.1 && \
    pip install --prefix=/install -r requirements.txt

FROM python:3.11-alpine

COPY --from=builder /install /usr/local
COPY app /app

WORKDIR /app
EXPOSE 8080

ENV APP_PORT=8080

HEALTHCHECK --interval=30s --timeout=5s CMD wget --spider -q http://localhost:8080/ || exit 1

CMD ["python", "main.py"]

FROM python:3.11-slim as builder

LABEL org.opencontainers.image.authors="Patryk Kaniosz"

WORKDIR /app
COPY requirements.txt .

# Instalacja najnowszego pip, bezpiecznej wersji setuptools i wszystkich zależności
RUN pip install --upgrade pip && \
    pip uninstall -y setuptools && \
    pip install setuptools==78.1.1 && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.11-alpine

# Instalujemy tylko potrzebne pakiety, w tym bezpieczną wersję setuptools
COPY --from=builder /install /usr/local

# Upewniamy się, że tylko jedna wersja setuptools istnieje
RUN pip install --upgrade pip && \
    pip uninstall -y setuptools && \
    pip install setuptools==78.1.1 && \
    find /usr -type d -name 'setuptools*' -exec rm -rf {} + && \
    find /usr -type f -name 'setuptools*' -exec rm -f {} + && \
    pip cache purge

COPY app /app

WORKDIR /app
EXPOSE 8080

ENV APP_PORT=8080

HEALTHCHECK --interval=30s --timeout=5s CMD wget --spider -q http://localhost:8080/ || exit 1

CMD ["python", "main.py"]

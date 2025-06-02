# Zadanie 1 – 🌦️ Pogoda App

Aplikacja webowa w FastAPI, działająca w kontenerze Docker, umożliwiająca sprawdzenie aktualnej pogody dla wybranego miasta i kraju.

---

## 📦 Funkcjonalność

- Dynamiczne wybieranie kraju i miasta (zależne listy rozwijane)
- Pobieranie i wyświetlanie aktualnych danych pogodowych z OpenWeatherMap
- Stylizowany formularz HTML z prostym interfejsem
- Logowanie daty uruchomienia, autora i portu do logów kontenera

---

## 🚀 Uruchomienie

### 1. Skonfiguruj klucz API
Zarejestruj się na [https://openweathermap.org/api](https://openweathermap.org/api) i wstaw swój klucz API do pliku `app/main.py`:

```python
api_key = "tu_wstaw_swoj_klucz_api"
```
### 2. Uruchamianie w cmd
```bash 
docker build -t pogoda-app:latest .
docker run -d -p 8080:8080 --name pogoda pogoda-app:latest
docker logs pogoda
docker image ls pogoda-app
```

http://localhost:8080

# Zadanie 2 – Aplikacja FastAPI + Docker + GitHub Actions + Trivy

## 📦 Zawartość repozytorium

- `Dockerfile` – buduje aplikację FastAPI jako wieloarchitekturny obraz Docker.
- `app/` – folder z kodem aplikacji FastAPI.
- `requirements.txt` – zależności Pythona.
- `.github/workflows/build.yml` – definicja GitHub Actions do budowy, skanowania i publikacji obrazu.
- `README.md` – opis konfiguracji projektu.

---

## ⚙️ Etapy konfiguracji

### 1. **Dockerfile (build multiarch + minimalny obraz)**

Aplikacja budowana jest w dwóch etapach:
- **builder** oparty o `python:3.11-slim`, instaluje zależności w `/install`
- **finalny obraz** oparty o `python:3.11-alpine`, kopiuje tylko gotowe biblioteki i kod

Zaletą tego podejścia jest mniejszy finalny obraz i szybsze uruchamianie.

---

### 2. **GitHub Actions – automatyzacja**

Workflow `build.yml` zawiera:
- Checkout repozytorium
- Logowanie do GitHub Container Registry (`ghcr.io`)
- Budowa obrazu tylko dla `linux/amd64` do skanowania Trivy
- Skan bezpieczeństwa (CVE) za pomocą `trivy`
- W razie braku błędów typu CRITICAL/HIGH – publikacja multiarch obrazu do `ghcr.io`
- Cache budowania trzymany na DockerHub

---

### 3. **Skanowanie Trivy (bezpieczeństwo)**

Każdy obraz jest analizowany pod kątem podatności (CVEs) przed publikacją.
Jeśli zostaną wykryte podatności CRITICAL lub HIGH – workflow się przerywa.

---

## 🔐 Sekrety

W repozytorium GitHub ustawiono:

- `DOCKERHUB_USERNAME` – login do DockerHub (np. `patrykkan`)
- `DOCKERHUB_TOKEN` – token (wygenerowany na https://hub.docker.com)
  
Oba potrzebne są do cache'owania budowy obrazu.

---

## ☁️ Publikacja obrazu

Obraz publikowany jest do:


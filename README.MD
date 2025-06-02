# 🌦️ Pogoda App

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
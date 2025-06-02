from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import httpx
import datetime
import os
from contextlib import asynccontextmanager

AUTHOR = "Patryk Kaniosz"
PORT = int(os.environ.get("APP_PORT", 8080))

@asynccontextmanager
async def lifespan(app: FastAPI):
    now = datetime.datetime.now().isoformat()
    print(f"[INFO] Aplikacja uruchomiona {now} | Autor: {AUTHOR} | Nasłuch na porcie: {PORT}")
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/", response_class=HTMLResponse)
async def form():
    return """
    <html>
    <head>
        <title>Pogoda</title>
        <style>
    body {
        font-family: Arial;
        padding: 30px;
        background: #f0f0f0;
        margin: 0;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    form {
        background: white;
        padding: 20px;
        border-radius: 8px;
        width: 300px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    label, select, input {
        display: block;
        margin-bottom: 10px;
        width: 100%;
    }
    h2 {
        margin-bottom: 20px;
    }
</style>

        <script>
            function updateCities() {
                const countryCityMap = {
                    'PL': ['Warsaw', 'Krakow', 'Gdansk'],
                    'DE': ['Berlin', 'Munich', 'Hamburg'],
                    'GB': ['London', 'Manchester', 'Liverpool']
                };
                const country = document.getElementById('country').value;
                const citySelect = document.getElementById('city');
                citySelect.innerHTML = '';
                countryCityMap[country].forEach(function(city) {
                    const opt = document.createElement('option');
                    opt.value = city;
                    opt.innerHTML = city;
                    citySelect.appendChild(opt);
                });
            }
        </script>
    </head>
    <body>
        <form method='post'>
            <h2>Sprawdź pogodę</h2>
            <label for='country'>Wybierz kraj:</label>
            <select id='country' name='country' onchange='updateCities()'>
                <option value='PL'>Polska</option>
                <option value='DE'>Niemcy</option>
                <option value='GB'>Wielka Brytania</option>
            </select>

            <label for='city'>Wybierz miasto:</label>
            <select id='city' name='city'>
                <option value='Warsaw'>Warsaw</option>
                <option value='Krakow'>Krakow</option>
                <option value='Gdansk'>Gdansk</option>
            </select>

            <input type='submit' value='Pokaż pogodę'>
        </form>
    </body>
    </html>
    """

@app.post("/", response_class=HTMLResponse)
async def get_weather(country: str = Form(...), city: str = Form(...)):
    api_key = "6e5ebfb6b4dab560b7a7794d0ac6c865"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={api_key}&units=metric&lang=pl"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            data = r.json()
            desc = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"""
                <html>
                    <body style="font-family:Arial; margin:0; height:100vh; background:#f0f0f0; display:flex; justify-content:center; align-items:center;">
                        <div style="background:white; padding:20px; border-radius:8px; width:300px; box-shadow:0 4px 10px rgba(0,0,0,0.1); text-align:center;">
                            <h3>Pogoda w {city}, {country}</h3>
                            <p><strong>Opis:</strong> {desc}</p>
                            <p><strong>Temperatura:</strong> {temp} &deg;C</p>
                            <a href="/">⟵ Powrót</a>
                        </div>
                    </body>
                </html>
            """
        else:
            return f"Błąd pobierania pogody dla {city}, {country}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)

import requests
import csv


url = "https://meteostat.p.rapidapi.com/stations/daily"

headers = {
    "X-RapidAPI-Key": "db1142695cmsh339e81a9ce14c6ep1e86f8jsn81be2765aee5", 
    "X-RapidAPI-Host": "meteostat.p.rapidapi.com"
}

params = {
    "station": "08222",     # Retiro, Madrid
    "start": "2024-01-01",
    "end": "2025-12-31"
}


# PETICIÓN A LA API

print("Consultando la API de Meteostat…")
response = requests.get(url, headers=headers, params=params)

if response.status_code != 200:
    print("Error al consultar la API:", response.status_code)
    print(response.text)
    exit()

data = response.json()["data"]  # lista de días

if not data:
    print("No se obtuvieron datos")
    exit()


# ESCRIBIR CSV

print(f"Generando CSV: datos_clima_madrid_2025.csv")
with open("datos_clima_madrid_2025.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # Cabecera
    writer.writerow(["fecha", "temp_max", "temp_min", "precipitacion"])

    # Filas
    for d in data:
        writer.writerow([
            d.get("date", "").split(" ")[0],  # solo fecha, sin hora
            d.get("tmax", ""),
            d.get("tmin", ""),
            d.get("prcp", "")
        ])

print(f"CSV generado correctamente con {len(data)} filas")

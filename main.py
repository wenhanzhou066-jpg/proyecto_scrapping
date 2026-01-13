import requests
import pandas as pd

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

# CREAR CSV CON PANDAS

print("Generando CSV: datos_clima_madrid_2025.csv")

# Crear DataFrame desde la lista de dicts
df = pd.DataFrame(data)

# Renombrar columnas
df = df.rename(columns={
    "date": "fecha",
    "tmax": "temp_max",
    "tmin": "temp_min",
    "prcp": "precipitacion"
})

# Quedarnos solo con las columnas necesarias
df = df[["fecha", "temp_max", "temp_min", "precipitacion"]]

# Eliminar la hora de la fecha
df["fecha"] = df["fecha"].str.split(" ").str[0]

# Guardar CSV
df.to_csv(
    "datos_clima_madrid_2025.csv",
    index=False,
    encoding="utf-8"
)

print(f"CSV generado correctamente con {len(df)} filas")

from meteostat import daily
from datetime import datetime
import pandas as pd

# ID de la estación de Madrid (Retiro / AEMET)
station_id = "08222"

# Fechas: 1 enero 2024 - 31 diciembre 2024
inicio = datetime(2024, 1, 1)
fin = datetime(2024, 12, 31)

# Obtener datos diarios
datos = daily(station_id, start=inicio, end=fin)
df = datos.fetch()

if df is None or df.empty:
    raise ValueError(f"No se encontraron datos para la estación {station_id}")
else:
    # Seleccionar columnas importantes
    df = df[['tmax', 'tmin', 'prcp']].reset_index()
    df.columns = ['fecha', 'temp_max', 'temp_min', 'precipitacion']

    # Guardar CSV
    df.to_csv("datos_clima_madrid_2024.csv", index=False)
    print("Datos guardados correctamente en 'datos_clima_madrid_2024.csv'")
    print(df.head())

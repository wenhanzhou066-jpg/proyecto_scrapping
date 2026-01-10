import pandas as panda
import numpy as nump


dataf = panda.read_csv("datos_clima_madrid_2024.csv")

# Convertimos la columna fecha a formato datetime
dataf["fecha"] = panda.to_datetime(dataf["fecha"])

# Creamos nuevas columnas a partir de la fecha
dataf["dia"] = dataf["fecha"].dt.day
dataf["mes"] = dataf["fecha"].dt.month
dataf["anio"] = dataf["fecha"].dt.year
dataf["dia_del_anyo"] = dataf["fecha"].dt.dayofyear

# Rellenamos valores nulos con la media
dataf["temp_max"] = dataf["temp_max"].fillna(dataf["temp_max"].mean())
dataf["temp_min"] = dataf["temp_min"].fillna(dataf["temp_min"].mean())
dataf["precipitacion"] = dataf["precipitacion"].fillna(0)

# Eliminamos filas duplicadas si las hubiera
dataf = dataf.drop_duplicates()

# Temperatura media diaria
dataf["temp_media"] = ((dataf["temp_max"] + dataf["temp_min"]) / 2).round(1)


# Dia lluvioso 
dataf["lluvia"] = nump.where(dataf["precipitacion"] > 0, 1, 0)


def clasificar_dia(temp):
    if temp < 10:
        return "frio"
    elif temp < 20:
        return "templado"
    else:
        return "calor"

dataf["tipo_dia"] = dataf["temp_media"].apply(clasificar_dia)

dataf_final = dataf[
    [
        "fecha",
        "dia_del_anyo",
        "temp_max",
        "temp_min",
        "temp_media",
        "precipitacion",
        "lluvia",
        "tipo_dia"
    ]
]

dataf_final.to_csv("clima_procesado.csv", index=False)


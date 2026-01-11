import pandas as panda
import numpy as nump

#Libreria pandas sirve basicamente para procesar datos ,crear tablas ,etc
#Libreria numpy sirve para calculos , estadisticas, cuentas , etc

# Lee el CSV
dataf = panda.read_csv("datos_clima_madrid_2025.csv")

# Convertimos la columna fecha a formato datetime
dataf["fecha"] = panda.to_datetime(dataf["fecha"])

# Creamos nuevas columnas a partir de la fecha
# El dataframe es basicamente una herramienta para hacer tablas y con el .day y eso dividimos la fecha
dataf["dia"] = dataf["fecha"].dt.day
dataf["mes"] = dataf["fecha"].dt.month
dataf["anyo"] = dataf["fecha"].dt.year
dataf["dia_del_anyo"] = dataf["fecha"].dt.dayofyear

# Rellenamos valores nulos con la media
# Fillna sirve basicamente para si hay valores nulos rellenarlos con el valor que haya entre parentesis,concretamente en esta la temperatura maxima media que hace con el .mean
dataf["temp_max"] = dataf["temp_max"].fillna(dataf["temp_max"].mean()) 
dataf["temp_min"] = dataf["temp_min"].fillna(dataf["temp_min"].mean())
dataf["precipitacion"] = dataf["precipitacion"].fillna(0)

# Elimino filas duplicadas 
dataf = dataf.drop_duplicates()

# Temperatura media diaria
# Sacamos la temp media y ademas con el round redondeamos a un decimal solo
dataf["temp_media"] = ((dataf["temp_max"] + dataf["temp_min"]) / 2).round(1)


# Llueve o no
# El where actua como un condicional si la precipitacion es mayor que 0 el valor de la lluvia sera 1 (binario) y si es igual a 0 no llueve
dataf["lluvia"] = nump.where(dataf["precipitacion"] > 0, 1, 0)


#Esta es la estructura de la tabla 
dataf_final = dataf[
    [
        "fecha",
        "dia_del_anyo",
        "temp_max",
        "temp_min",
        "temp_media",
        "precipitacion",
        "lluvia",
    ]
]
#Convierte a csv 
dataf_final.to_csv("clima_procesado.csv", index=False)


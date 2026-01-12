import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Con el pandas leemos los csv y pasamos las fechas a datetime
df_real = pd.read_csv("clima_procesado.csv")
df_real["fecha"] = pd.to_datetime(df_real["fecha"])

df_pred = pd.read_csv("predicciones_ml.csv")
df_pred["fecha"] = pd.to_datetime(df_pred["fecha"])

#Con el merge filtra y une los datos que quiere usar para hacer el grafico y se quita los demas que no sirve ni coinciden entre los dos csv
df = pd.merge(
    df_real[["fecha", "temp_max", "precipitacion"]],#Selecciona los datos que quiere de cada csv
    df_pred[["fecha", "temp_max_predicha"]],
    on="fecha",#Hace que la comparacion sea a traves de la fecha 
    how="inner"#Omite los datos que no esten en ambos csv
)

# Calcula el error de predicción para cada día
error = df["temp_max"] - df["temp_max_predicha"]

# Mide cuanto se dispersan los errores respecto a su media
std_error = np.std(error)

# Límites superior e inferior
limite_superior = df["temp_max_predicha"] + std_error
limite_inferior = df["temp_max_predicha"] - std_error

#Crea el grafico en blanco
plt.figure(figsize=(10, 5))

plt.plot(df["fecha"], df["temp_max"], label="Temp. máxima real")#Dibuja la tem_real en el grafico
plt.plot(#Dibuja la temperatura que hemos predicho
    df["fecha"],
    df["temp_max_predicha"],
    label="Temp. máxima predicha",
    linestyle="--"#Dibuja la linea discontinua para diferenciar
)

# Intervalo de confianza
plt.fill_between(#Rellena el area de error que existe entre ambas lineas
    df["fecha"],
    limite_inferior,
    limite_superior,
    alpha=0.3,#Le añade transparencia para que se vean las lineas 
    label="Intervalo de confianza (±1 std)"
)

plt.title("Temperatura máxima real vs predicha")#Titulo
plt.xlabel("Fecha")#Etiquetas
plt.ylabel("Temperatura máxima (°C)")#Etiquetas
plt.legend()#Añade leyenda
plt.grid(True)#Añade cuadricula
plt.tight_layout()#Ajusta los margenes automaticamente
plt.savefig("temp_max_real_vs_predicha_con_intervalo.png")#Guarda el grafico en un .png
plt.close()#Cierra el grafico

plt.figure(figsize=(6, 4))
plt.scatter(df["precipitacion"], df["temp_max"])#Crea un grafico de dispersion en el que el EJEX es la precipitacion y el Y la temp_max
plt.title("Precipitación vs Temperatura máxima")#Añade titulo
plt.xlabel("Precipitación (mm)")#Etiquetas
plt.ylabel("Temperatura máxima (°C)")#Etiquetas
plt.tight_layout()#Ajusta los margenes automaticamente
plt.savefig("scatter_precipitacion_vs_temp_max.png")#Guarda el grafico en un .png
plt.close()#Cierra el grafico

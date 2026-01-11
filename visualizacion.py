import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_real = pd.read_csv("clima_procesado.csv")
df_real["fecha"] = pd.to_datetime(df_real["fecha"])

df_pred = pd.read_csv("predicciones_ml.csv")
df_pred["fecha"] = pd.to_datetime(df_pred["fecha"])

df = pd.merge(
    df_real[["fecha", "temp_max", "precipitacion"]],
    df_pred[["fecha", "temp_max_predicha"]],
    on="fecha",
    how="inner"
)

# Error entre real y predicho
error = df["temp_max"] - df["temp_max_predicha"]

# Desviación estándar del error
std_error = np.std(error)

# Límites superior e inferior
limite_superior = df["temp_max_predicha"] + std_error
limite_inferior = df["temp_max_predicha"] - std_error

plt.figure(figsize=(10, 5))

plt.plot(df["fecha"], df["temp_max"], label="Temp. máxima real")
plt.plot(
    df["fecha"],
    df["temp_max_predicha"],
    label="Temp. máxima predicha",
    linestyle="--"
)

# Intervalo de confianza
plt.fill_between(
    df["fecha"],
    limite_inferior,
    limite_superior,
    alpha=0.3,
    label="Intervalo de confianza (±1 std)"
)

plt.title("Temperatura máxima real vs predicha")
plt.xlabel("Fecha")
plt.ylabel("Temperatura máxima (°C)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("temp_max_real_vs_predicha_con_intervalo.png")
plt.close()

plt.figure(figsize=(6, 4))
plt.scatter(df["precipitacion"], df["temp_max"])
plt.title("Precipitación vs Temperatura máxima")
plt.xlabel("Precipitación (mm)")
plt.ylabel("Temperatura máxima (°C)")
plt.tight_layout()
plt.savefig("scatter_precipitacion_vs_temp_max.png")
plt.close()

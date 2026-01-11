import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from machine_learning import y_test, y_pred   

# Cargar los datos reales
df = pd.read_csv("clima_procesado.csv", parse_dates=["fecha"])
df = df.sort_values("fecha")

# Reconstruir el conjunto test (80% train, 20% test cronológico)
split = int(len(df) * 0.8)
test_df = df.iloc[split:]

test_dates = test_df["fecha"]
y_test = test_df["temp_max"]


error = y_test - y_pred
std = np.std(error)

plt.figure(figsize=(12,6))

plt.plot(test_dates, y_test, label="Temperatura real", linewidth=2)
plt.plot(test_dates, y_pred, "--", label="Predicción")

# Intervalo de confianza
plt.fill_between(
    test_dates,
    y_pred - std,
    y_pred + std,
    alpha=0.25,
    label="Intervalo ±1σ"
)

plt.title("Temperatura máxima real vs predicha (Madrid 2024)")
plt.xlabel("Fecha")
plt.ylabel("Temperatura (°C)")
plt.legend()
plt.grid(True)

plt.savefig("temperatura_real_vs_predicha.png")
plt.show()

plt.figure(figsize=(8,6))

plt.scatter(df["precip"], df["temp_max"], alpha=0.6)

plt.title("Relación entre precipitación y temperatura máxima")
plt.xlabel("Precipitación (mm)")
plt.ylabel("Temperatura máxima (°C)")
plt.grid(True)

plt.savefig("precipitacion_vs_temperatura.png")
plt.show()

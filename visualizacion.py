import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from machine_learning import y_pred   # solo necesitamos y_pred

df = pd.read_csv("clima_procesado.csv", parse_dates=["date"])
df = df.sort_values("date")

split = int(len(df) * 0.8)
test_df = df.iloc[split:]

test_dates = test_df["date"]
y_real = test_df["temp_max"]

# Convertimos a numpy arrays
x = test_dates.values
y_real_np = y_real.values
y_pred_np = np.array(y_pred)

error = y_real_np - y_pred_np
std = np.std(error)

plt.figure(figsize=(12,6))

plt.plot(x, y_real_np, label="Temperatura real", linewidth=2)
plt.plot(x, y_pred_np, "--", label="Predicción")

plt.fill_between(
    x,
    y_pred_np - std,
    y_pred_np + std,
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

# Scatter precipitación vs temperatura
plt.figure(figsize=(8,6))
plt.scatter(df["precip"], df["temp_max"], alpha=0.6)
plt.title("Relación entre precipitación y temperatura máxima")
plt.xlabel("Precipitación (mm)")
plt.ylabel("Temperatura máxima (°C)")
plt.grid(True)
plt.savefig("precipitacion_vs_temperatura.png")
plt.show()

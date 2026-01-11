import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("clima_procesado.csv")
df["fecha"] = pd.to_datetime(df["fecha"])

plt.figure(figsize=(10, 5))
plt.plot(df["fecha"], df["temp_media"])
plt.title("Evolucion de la temperatura media")
plt.xlabel("Fecha")
plt.ylabel("Temperatura media (°C)")
plt.grid(True)
plt.tight_layout()
plt.savefig("grafico_temperatura_media.png")
plt.close()

temp_por_tipo = df.groupby("tipo_dia")["temp_media"].mean()

plt.figure(figsize=(6, 4))
temp_por_tipo.plot(kind="bar")
plt.title("Temperatura media por tipo de día")
plt.xlabel("Tipo de día")
plt.ylabel("Temperatura media (°C)")
plt.tight_layout()
plt.savefig("grafico_tipo_dia.png")
plt.close()

temp_media_mensual = df.groupby(df["fecha"].dt.month)["temp_media"].mean()

plt.figure(figsize=(8, 5))
plt.bar(temp_media_mensual.index, temp_media_mensual.values)
plt.title("Temperatura media mensual")
plt.xlabel("Mes")
plt.ylabel("Temperatura media (°C)")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.savefig("temperatura_media_mensual.png")
plt.close()

plt.figure(figsize=(6, 4))
plt.hist(df["temp_media"], bins=15)
plt.title("Distribucion de la temperatura media")
plt.xlabel("Temperatura media (°C)")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("histograma_temp_media.png")
plt.close()

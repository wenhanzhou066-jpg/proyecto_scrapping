import pandas as pd #pandas: para manipulación y análisis de datos (lectura de CSV, filtrado, selección de columnas, etc.).
import matplotlib.pyplot as plt #matplotlib.pyplot: para crear gráficos y visualizaciones.
import numpy as np #numpy: para operaciones numéricas eficientes (arrays, cálculos de desviación estándar, etc.).

from machine_learning import y_pred #y_pred: vector de predicciones generado por un modelo de machine learning (ya entrenado)

df = pd.read_csv("clima_procesado.csv", parse_dates=["date"]) #pd.read_csv(): lee el archivo CSV que contiene los datos de clima/parse_dates=["date"]: convierte la columna "date" en objetos de tipo fecha (datetime).
df = df.sort_values("date") #sort_values("date"): asegura que los datos estén ordenados cronológicamente. Esto es importante para que las gráficas de series temporales se vean correctamente.

split = int(len(df) * 0.8) #Calcula el 80% de los datos para entrenamiento y toma el 20% final para pruebas.
test_df = df.iloc[split:] #df.iloc[split:]: selecciona las filas restantes para el conjunto de prueba (test_df).

#Propósito: comparar las predicciones con datos que no fueron usados para entrenar el modelo.

test_dates = test_df["date"] #test_dates → eje x de la gráfica (fechas).
y_real = test_df["temp_max"] #y_real → eje y (temperatura máxima real).

# Convertimos a numpy arrays
x = test_dates.values
y_real_np = y_real.values
y_pred_np = np.array(y_pred)

error = y_real_np - y_pred_np #error: diferencia entre temperatura real y predicha
std = np.std(error) #std: desviación estándar de los errores.

#Propósito: mostrar incertidumbre o rango de ±1σ alrededor de la predicción en la gráfica.

plt.figure(figsize=(12,6)) #plt.figure(figsize=(12,6)): define tamaño del gráfico.

plt.plot(x, y_real_np, label="Temperatura real", linewidth=2) #plt.plot(): dibuja la curva de temperatura real y predich
plt.plot(x, y_pred_np, "--", label="Predicción")

plt.fill_between( #plt.fill_between(): crea una banda sombreada entre
    x,
    y_pred_np - std, #y_pred ± std para mostrar la desviación.
    y_pred_np + std, 
    alpha=0.25, #alpha=0.25: hace la banda semitransparente
    label="Intervalo ±1σ"
)


# Titulos y estiquetas
plt.title("Temperatura máxima real vs predicha (Madrid 2024)")
plt.xlabel("Fecha")
plt.ylabel("Temperatura (°C)")
plt.legend() #plt.legend(): muestra la leyenda con los nombres de las líneas.
plt.grid(True) #plt.grid(True): añade cuadrícula para mejor lectura.

plt.savefig("temperatura_real_vs_predicha.png") #plt.savefig(): guarda la imagen en un archivo.
plt.show() #plt.show(): muestra la gráfica en pantalla.

# Scatter precipitación vs temperatura
plt.figure(figsize=(8,6))
plt.scatter(df["precip"], df["temp_max"], alpha=0.6)
plt.title("Relación entre precipitación y temperatura máxima")
plt.xlabel("Precipitación (mm)")
plt.ylabel("Temperatura máxima (°C)")
plt.grid(True)
plt.savefig("precipitacion_vs_temperatura.png")
plt.show()

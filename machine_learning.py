from sklearn.ensemble import RandomForestRegressor # type: ignore
from sklearn.metrics import mean_absolute_error, root_mean_squared_error # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
import pandas as pd # type: ignore

# Cargamos el dataset en un dataframe
df = pd.read_csv('clima_procesado.csv')

# Convertimos la columna 'date' en formato datetime
df["fecha"] = pd.to_datetime(df["fecha"])

# Convertimos fecha en número ordinal
df["fecha_ordinal"] = df["fecha"].astype("int64") / 10**9 # con astype pasamos la fecha a nanosegundos y dividimos por 10**9  (1.000.000.000) para pasarlo a segundos 

X = df[["fecha_ordinal" , "precipitacion", "temp_min", "temp_media","dia_del_anyo","lluvia"]].values # El valor de X son las variables de entrada, lo que vamos a usar para predecir
y = df["temp_max"].values # y es la variable objetivo, lo que queremos predecir   .values convirte el dataframe en un array de Numpy para poder procesarlo

# Dividimos los datos en entrenamiento y test , ponemos shuffle= False para que no mezcle los datos y asi seguir orden cronológico, 20% datos son para test (test_size)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, shuffle= False)

# Creamos la maquina y la entrenamos
machine = RandomForestRegressor(n_estimators= 200, random_state=42) # randomforest crea varios arboles de decision, n_estimators es el nùmero de arboles que tiene el ''bosque'' , random_state es una semilla aleatoria para que siempre nos de la misma predicción y no varie 
machine.fit(X_train, y_train)

# Predecimos la temperatura_maxima
y_pred = machine.predict(X_test)

MAE = mean_absolute_error(y_test, y_pred) # Error absoluto promedio, promedio de equivocaciones en cada predicción
RMSE = root_mean_squared_error(y_test, y_pred) # Igual que el MAE pero dando mas importancia a errores grandes

print(f"MAE: {MAE:.2f}ºC")
print(f"RMSE: {RMSE:.2f}ºC")


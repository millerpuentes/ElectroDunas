import pandas as pd
import numpy as np
import os
from sklearn.ensemble import IsolationForest

# Obtén la ruta absoluta de la carpeta actual del script
current_folder_path = os.path.dirname(os.path.abspath(__file__))
# Define la ruta relativa a la carpeta "Entrada" desde la carpeta actual del script
folder_path = os.path.join(current_folder_path, '..', '..', 'Entrada')

# Lista todos los archivos CSV en la carpeta especificada
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Crea un DataFrame vacío para almacenar todos los datos
all_data = pd.DataFrame()

# Itera sobre los archivos y los concatena en el DataFrame all_data
for file in files:
    try:
        # Extrae el ID del cliente del nombre del archivo
        cliente_id_str = file.replace('DATOSCLIENTE', '').replace('.csv', '')
        cliente_id = int(cliente_id_str)  # Convierte a entero

        # Lee el archivo CSV y agrega una columna con el ID del cliente
        file_path = os.path.join(folder_path, file)
        data = pd.read_csv(file_path)
        data['Cliente_ID'] = cliente_id
        all_data = pd.concat([all_data, data], ignore_index=True)
    except ValueError:
        # Muestra una advertencia si el archivo no contiene un ID de cliente válido
        print(f"Advertencia: El archivo {file} no contiene un ID de cliente válido y será omitido.")


# Obtén la ruta absoluta de la carpeta actual del script
current_folder_path = os.path.dirname(os.path.abspath(__file__))
# Define la ruta relativa al archivo "sector_economico_clientes.xlsx" desde la carpeta actual del script
file_path = os.path.join(current_folder_path, '..', '..', 'Entrada', 'sector_economico_clientes.xlsx')

sector_economico_clientes = pd.read_excel(file_path)

# Extrae el ID del cliente del nombre y lo agrega como una nueva columna
sector_economico_clientes['Cliente_ID'] = (
    sector_economico_clientes['Cliente:']
    .str.extract('(\d+)')  # Extrae el número del nombre del cliente
    .astype(int)           # Convierte el resultado en entero
)

# Fusiona los datos de los clientes con la información del sector económico
data_merged = pd.merge(all_data, sector_economico_clientes, on='Cliente_ID', how='left')

# Filtra los valores negativos en la columna de energía activa
data_filtered_neg = data_merged.copy()
data_filtered_neg['Active_energy'] = data_filtered_neg['Active_energy'].clip(lower=0)

# Ordena los datos por Cliente_ID y Fecha
data_filtered_neg_sorted = data_filtered_neg.sort_values(by=['Cliente_ID', 'Fecha'])
data_filtered_neg_sorted['Fecha'] = pd.to_datetime(data_filtered_neg_sorted['Fecha'])

# Función para detectar anomalías en la relación energía reactiva/energía activa
def anomalias_ER_EA(data_filtered_neg, num_cliente):
    """
    Detecta anomalías en la relación entre energía reactiva y energía activa para un cliente específico.

    Args:
    data_filtered_neg (DataFrame): DataFrame con los datos filtrados.
    num_cliente (int): ID del cliente.

    Returns:
    DataFrame: DataFrame con las anomalías detectadas para el cliente.
    """
    df = data_filtered_neg[data_filtered_neg['Cliente_ID'] == num_cliente]
    df = df[['Fecha', 'Active_energy', 'Reactive_energy']]
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    df.set_index('Fecha', inplace=True)
    df_resumen = df.resample('M').sum()
    df_resumen['Cliente_ID'] = num_cliente
    df_resumen['Reactive_to_Active_ratio'] = (df_resumen['Reactive_energy'] / df_resumen['Active_energy']) * 100
    df_resumen['Anomalía'] = 0
    df_resumen.loc[df_resumen['Reactive_to_Active_ratio'] > 30, 'Anomalía'] = 1
    df_resumen.reset_index(inplace=True)
    return df_resumen

# Función para evaluar todos los clientes
def evaluar_todos_los_clientes(data_filtered_neg):
    """
    Evalúa la relación entre energía reactiva y energía activa para todos los clientes y detecta anomalías.

    Args:
    data_filtered_neg (DataFrame): DataFrame con los datos filtrados.

    Returns:
    DataFrame: DataFrame con las anomalías detectadas para todos los clientes.
    """
    resultados = []
    clientes_unicos = data_filtered_neg['Cliente_ID'].unique()
    for num_cliente in clientes_unicos:
        resultado_cliente = anomalias_ER_EA(data_filtered_neg, num_cliente)
        resultados.append(resultado_cliente)
    df_resultados = pd.concat(resultados, ignore_index=True)
    return df_resultados

# Detecta anomalías en la relación energía reactiva/energía activa para todos los clientes
df_anomalias_ER_EA = evaluar_todos_los_clientes(data_filtered_neg_sorted)


# Obtén la ruta absoluta de la carpeta actual del script
current_folder_path = os.path.dirname(os.path.abspath(__file__))
# Define la ruta relativa al archivo "df_anomalias_ER_EA.csv" desde la carpeta actual del script
ruta_csv = os.path.join(current_folder_path, '..', '..', 'Salida', 'df_anomalias_ER_EA.csv')
# Guarda los resultados en un archivo CSV
df_anomalias_ER_EA.to_csv(ruta_csv, index=False)


print("El script de las anomalías Contractuales se ha ejecutado correctamente!")

# Diccionario con los mejores hiperparámetros para el modelo Isolation Forest por cliente
best_params_dict = {
    1: {'contamination': 0.02, 'n_estimators': 50},
    2: {'contamination': 0.02, 'n_estimators': 50},
    3: {'contamination': 0.02, 'n_estimators': 50},
    4: {'contamination': 0.02, 'n_estimators': 50},
    5: {'contamination': 0.02, 'n_estimators': 50},
    6: {'contamination': 0.02, 'n_estimators': 150},
    7: {'contamination': 0.02, 'n_estimators': 200},
    8: {'contamination': 0.02, 'n_estimators': 50},
    9: {'contamination': 0.02, 'n_estimators': 50},
    10: {'contamination': 0.01, 'n_estimators': 100},
    11: {'contamination': 0.03, 'n_estimators': 50},
    12: {'contamination': 0.03, 'n_estimators': 50},
    13: {'contamination': 0.03, 'n_estimators': 150},
    14: {'contamination': 0.03, 'n_estimators': 50},
    15: {'contamination': 0.03, 'n_estimators': 50},
    16: {'contamination': 0.03, 'n_estimators': 200},
    17: {'contamination': 0.03, 'n_estimators': 50},
    18: {'contamination': 0.03, 'n_estimators': 50},
    19: {'contamination': 0.03, 'n_estimators': 50},
    20: {'contamination': 0.03, 'n_estimators': 150},
    21: {'contamination': 0.03, 'n_estimators': 50},
    22: {'contamination': 0.03, 'n_estimators': 100},
    23: {'contamination': 0.03, 'n_estimators': 50},
    24: {'contamination': 0.03, 'n_estimators': 50},
    25: {'contamination': 0.03, 'n_estimators': 50},
    26: {'contamination': 0.03, 'n_estimators': 100},
    27: {'contamination': 0.03, 'n_estimators': 50},
    28: {'contamination': 0.03, 'n_estimators': 150},
    29: {'contamination': 0.03, 'n_estimators': 150},
    30: {'contamination': 0.03, 'n_estimators': 150}
}

# Función para aplicar Isolation Forest y detectar anomalías
def apply_isolation_forest(client_id, data):
    """
    Aplica el modelo Isolation Forest a los datos de energía activa de un cliente específico,
    utilizando parámetros predefinidos para detectar anomalías.

    Args:
    client_id (int): ID del cliente.
    data (DataFrame): DataFrame que contiene los datos de los clientes.

    Returns:
    DataFrame: Datos del cliente con columnas adicionales de anomalías y puntuaciones de anomalías.
    """
    client_data = data[data['Cliente_ID'] == client_id].copy()
    client_data['Active_energy'] = client_data['Active_energy'].astype(np.float64)
    client_data['Fecha'] = pd.to_datetime(client_data['Fecha'])
    client_data['Mes'] = client_data['Fecha'].dt.month
    client_data['Dia_de_Semana'] = client_data['Fecha'].dt.dayofweek
    client_data['Franja_Horaria'] = client_data['Fecha'].dt.hour.apply(
        lambda h: '12am-6am' if 0 <= h < 6 else '6am-12pm' if 6 <= h < 12 else '12pm-6pm' if 12 <= h < 18 else '6pm-12am'
    )

    # Establecer valores por defecto
    default_params = {'contamination': 0.03, 'n_estimators': 50}
    
    # Obtener parámetros del cliente o usar valores por defecto
    if client_id in best_params_dict:
        params = best_params_dict[client_id]
    else:
        params = default_params
    
    model = IsolationForest(n_estimators=params['n_estimators'], contamination=params['contamination'], random_state=123)
    anomalies = model.fit_predict(client_data[['Active_energy']])
    client_data['Anomaly_IF'] = (anomalies == -1).astype(int)
    client_data['Anomaly_Score_IF'] = model.decision_function(client_data[['Active_energy']])
    
    return client_data

# Función para detectar la criticidad de las anomalías
def detect_anomalies_criticidad(client_data):
    """
    Evalúa la criticidad de las anomalías detectadas en los datos de energía activa del cliente.

    Args:
    client_data (DataFrame): DataFrame que contiene datos y resultados de anomalías del cliente.

    Returns:
    DataFrame: DataFrame actualizado con una columna de criticidad para cada anomalía detectada.
    """
    # Asignar "No anomalía" a todas las filas donde Anomaly_IF es 0
    client_data['criticidad'] = 'No anomalía'

    if 'Anomaly_IF' in client_data.columns and (client_data['Anomaly_IF'] == 1).any():
        # Calcular la mediana y desviación estándar para toda la columna Active_energy
        median = client_data['Active_energy'].median()
        std_dev = client_data['Active_energy'].std()

        # Calcular el Z-Score para toda la columna Active_energy
        client_data['Z_Score'] = (client_data['Active_energy'] - median) / std_dev

        # Asignar criticidad basada en el Z-Score para las filas donde Anomaly_IF es 1
        client_data.loc[client_data['Anomaly_IF'] == 1, 'criticidad'] = pd.cut(client_data.loc[client_data['Anomaly_IF'] == 1, 'Z_Score'],
                                                                              bins=[-np.inf, -2.5, -1.25, 1.25, 2.25, 2.5, np.inf],
                                                                              labels=['crítica', 'moderada', 'leve', 'leve', 'moderada', 'crítica'],
                                                                              right=False,
                                                                              ordered=False)
    else:
        print("No se encontraron anomalías en los datos del cliente.")
    return client_data

# Aplica el modelo Isolation Forest y detecta anomalías para todos los clientes
unique_clients = data_filtered_neg_sorted['Cliente_ID'].unique()
all_results = []

for client_id in unique_clients:
    client_results = apply_isolation_forest(client_id, data_filtered_neg_sorted)
    if client_results is not None:
        client_results = detect_anomalies_criticidad(client_results)
        all_results.append(client_results)

# Concatenar todos los resultados en un DataFrame final.
df_anomalias_IF = pd.concat(all_results)
df_anomalias_IF = df_anomalias_IF[['Fecha', 'Cliente_ID', 'Sector Económico:', 'Mes', 'Dia_de_Semana', 'Franja_Horaria', 'Active_energy', 'Anomaly_IF', 'Anomaly_Score_IF', 'criticidad']]


# Obtén la ruta absoluta de la carpeta actual del script
current_folder_path = os.path.dirname(os.path.abspath(__file__))
# Define la ruta relativa al archivo "df_anomalias_IF.csv" desde la carpeta actual del script
ruta_csv = os.path.join(current_folder_path, '..', '..', 'Salida', 'df_anomalias_IF.csv')
# Guarda los resultados en un archivo CSV
df_anomalias_IF.to_csv(ruta_csv, index=False)



print("El script de las anomalías por tendencia se ha ejecutado correctamente!")

# Elimina los DataFrames temporales para liberar memoria
del data_merged, all_data, sector_economico_clientes, df_anomalias_IF, df_anomalias_ER_EA

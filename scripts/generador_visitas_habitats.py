import os
import pandas as pd
import numpy as np

habitat_ids = [
    "H001", "H002", "H003", "H004", "H005", "H006", "H007", "H008",
    "H009", "H010", "H011", "H012", "H013", "H014", "H015", "H016",
    "H017", "H018"
]

habitat_probabilities = [
    0.05, 0.12, 0.08, 0.03, 0.06, 0.04, 0.05, 0.04,
    0.03, 0.02, 0.07, 0.03, 0.02, 0.10, 0.03, 0.04,
    0.04, 0.15
]

if not np.isclose(sum(habitat_probabilities), 1.0):
    raise ValueError(f"La suma de las probabilidades de los hábitats debe ser 1.0. Suma actual: {sum(habitat_probabilities)}")
if len(habitat_ids) != len(habitat_probabilities):
    raise ValueError("La cantidad de IDs de hábitat debe coincidir con la cantidad de probabilidades.")

total_visitas_registros = 250

min_id_entrada = 1
max_id_entrada = 80

porcentaje_nulos_general = 0.07


# --- Función para introducir nulos ---
def introducir_nulos(data_array, porcentaje_nulos):
    """
    Introduce un porcentaje de valores NaN (Not a Number, un tipo de nulo)
    en una copia del array o estructura similar a un array que se le pase.

    Parámetros:
    data_array (array-like): La estructura de datos (lista, array de NumPy, Serie de Pandas)
                             a la que se le añadirán nulos.
    porcentaje_nulos (float): El porcentaje de nulos a introducir, expresado como decimal
                              (ej. 0.05 para 5%).

    Retorna:
    numpy.ndarray: Un nuevo array de NumPy con los nulos introducidos.
    """
    if pd.api.types.is_integer_dtype(data_array) and not pd.api.types.is_bool_dtype(data_array):  # No convertir booleanos a float
        data_array_con_nulos = data_array.astype(float)
    else:
        data_array_con_nulos = np.array(data_array, dtype=object)

    num_nulos = int(len(data_array_con_nulos) * porcentaje_nulos)
    if num_nulos > 0:  # Solo si hay nulos que introducir
        indices_nulos = np.random.choice(len(data_array_con_nulos), size=num_nulos, replace=False)
        data_array_con_nulos[indices_nulos] = np.nan
    return data_array_con_nulos


# --- Generación de Datos ---

id_habitat_lista_original = np.random.choice(
    habitat_ids,
    size=total_visitas_registros,
    p=habitat_probabilities
)

# Generar ID_entrada
id_entrada_lista_original = np.random.randint(min_id_entrada, max_id_entrada + 1, size=total_visitas_registros)

# Generar 'satisfaccion' (escala 1-5)
satisfaccion_lista_original = np.random.randint(1, 6, size=total_visitas_registros)
satisfaccion_con_nulos = introducir_nulos(satisfaccion_lista_original, porcentaje_nulos_general)


# --- Crear DataFrame de Pandas ---
df_visitas_habitats = pd.DataFrame({
    'ID_entrada': id_entrada_lista_original,
    'ID_habitat': id_habitat_lista_original,
    'satisfaccion': satisfaccion_con_nulos
})

# Ordenar por ID_entrada (Pandas por defecto pone los NULL al final al ordenar)
df_visitas_habitats = df_visitas_habitats.sort_values(by='ID_entrada').reset_index(drop=True)

# --- Guardar a CSV ---
carpeta_destino = 'zoo_dataset'
nombre_archivo_csv = 'visitas_habitats_sucio.csv'

if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

nombre_archivo_csv = os.path.join(carpeta_destino, nombre_archivo_csv)

df_visitas_habitats.to_csv(nombre_archivo_csv, index=False, na_rep='NULL')

print(f"Archivo '{nombre_archivo_csv}' generado con {len(df_visitas_habitats)} registros.")
print("\nPrimeras 10 filas del DataFrame generado:")
print(df_visitas_habitats.head(10))

print("\nPorcentaje de valores nulos por columna:")
print(df_visitas_habitats.isnull().mean().apply(lambda x: f"{x:.2%}"))

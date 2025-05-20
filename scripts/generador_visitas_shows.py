import os
import pandas as pd
import numpy as np

shows_ids = [
    "S001", "S002", "S003", "S004", "S005", "S006", "S007", "S008",
    "S009", "S010", "S011", "S012", "S013", "S014", "S015", "S016",
    "S017", "S018"
]


total_visitas_registros = 400

min_id_entrada = 0
max_id_entrada = 199

porcentaje_nulos_general = 0.07

# --- Función para introducir nulos ---
def introducir_nulos(data_array, porcentaje_nulos):
    """Introduce un porcentaje de valores NaN en una copia del array."""
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

id_shows_lista_original = np.random.choice(
    shows_ids,
    size=total_visitas_registros,
)
id_shows_con_nulos = introducir_nulos(id_shows_lista_original, porcentaje_nulos_general)

# Generar ID_entrada
id_entrada_lista_original = np.random.randint(min_id_entrada, max_id_entrada + 1, size=total_visitas_registros)
id_entrada_con_nulos = introducir_nulos(id_entrada_lista_original, porcentaje_nulos_general)

# Generar 'satisfaccion' (escala 1-5)
satisfaccion_lista_original = np.random.randint(1, 6, size=total_visitas_registros)
satisfaccion_con_nulos = introducir_nulos(satisfaccion_lista_original, porcentaje_nulos_general)


# --- Crear DataFrame de Pandas ---
df_visitas_shows = pd.DataFrame({
    'ID_entrada': id_entrada_con_nulos,
    'ID_show': id_shows_con_nulos,
    'satisfaccion': satisfaccion_con_nulos
})

# Ordenar por ID_entrada (Pandas por defecto pone los NULL al final al ordenar)
df_visitas_shows = df_visitas_shows.sort_values(by='ID_entrada').reset_index(drop=True)

# --- Guardar a CSV ---
carpeta_destino = 'zoo_dataset'
nombre_archivo_csv = 'visitas_shows_sucio_generado.csv'

if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

nombre_archivo_csv = os.path.join(carpeta_destino, nombre_archivo_csv)

df_visitas_shows.to_csv(nombre_archivo_csv, index=False, na_rep='NULL')

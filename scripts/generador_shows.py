import os
import pandas as pd
import numpy as np

porcentaje_nulos_general = 0.07
total_shows = 18


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


shows_ids = [
    "S001", "S002", "S003", "S004", "S005", "S006", "S007", "S008",
    "S009", "S010", "S011", "S012", "S013", "S014", "S015", "S016",
    "S017", "S018"
]

nombres_shows = [
    "Aventuras Salvajes",
    "El Rugido de la Selva",
    "Vuelo Majestuoso",
    "Guardianes del Reino Animal",
    "Entre Garras y Plumas",
    "Reptiles al Descubierto",
    "Safari Sonoro",
    "Zooluminación Nocturna",
    "Amigos del Pantano",
    "Gigantes de la Sabana",
    "Baile de las Aves",
    "Pequeños Exploradores",
    "Magia Marina",
    "Caminata con Canguros",
    "El Misterio del Amazonas",
    "Bestias del Crepúsculo",
    "Manada en Movimiento",
    "Historias del Zoo"
]

cupos_totales = np.random.randint(30, 51, size=total_shows)

cupos_ocupados = np.array([np.random.randint(0, total + 1) for total in cupos_totales])

tipos_ambientes = [
    "Cerrado", "Abierto", "Mixto"
]

ambientes = np.random.choice(tipos_ambientes, size=total_shows)

duracion = np.random.randint(30, 121, size=total_shows)

nombres_shows_con_nulos = introducir_nulos(nombres_shows, porcentaje_nulos_general)
cupos_totales_con_nulos = introducir_nulos(cupos_totales, porcentaje_nulos_general)
cupos_ocupados_con_nulos = introducir_nulos(cupos_ocupados, porcentaje_nulos_general)
ambientes_con_nulos = introducir_nulos(ambientes, porcentaje_nulos_general)
duracion_con_nulos = introducir_nulos(duracion, porcentaje_nulos_general)

shows = pd.DataFrame({
    'ID_show': shows_ids,
    'nombre_show': nombres_shows_con_nulos,
    'cupos_totales': cupos_totales_con_nulos,
    'cupos_ocupados': cupos_ocupados_con_nulos,
    'tipo_ambiente': ambientes_con_nulos,
    'duracion': duracion_con_nulos
})

shows = shows.sort_values(by='ID_show').reset_index(drop=True)

# --- Guardar a CSV ---
carpeta_destino = 'zoo_dataset'
nombre_archivo_csv = 'shows_sucio_generado.csv'

if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

nombre_archivo_csv = os.path.join(carpeta_destino, nombre_archivo_csv)

shows.to_csv(nombre_archivo_csv, index=False, na_rep='NULL')

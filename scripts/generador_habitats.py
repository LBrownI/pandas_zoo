import os
import pandas as pd
import numpy as np

porcentaje_nulos_general = 0.07
total_habitats = 18


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


habitat_ids = [
    "H001", "H002", "H003", "H004", "H005", "H006", "H007", "H008",
    "H009", "H010", "H011", "H012", "H013", "H014", "H015", "H016",
    "H017", "H018"
]

nombres_habitats = [
    "Selva Tropical",
    "Sabana Dorada",
    "Caverna de los Murciélagos",
    "Pantano Misterioso",
    "Bosque Templado",
    "Rincón de los Reptiles",
    "Altas Cumbres",
    "Mares Profundos",
    "Isla de los Primates",
    "Valle del Tigre",
    "Estepa Salvaje",
    "Refugio del Panda",
    "Jardín de las Mariposas",
    "Desierto Rojo",
    "Granja Interactiva",
    "La Antártida Viva",
    "Bosque de Koalas",
    "Zona Nocturna"
]


cantidad_especies = np.random.randint(1, 5, size=total_habitats)

tipos_ambientes = [
    "Cerrado", "Abierto", "Mixto"
]

ambientes = np.random.choice(tipos_ambientes, size=total_habitats)

permite_alimentos = np.random.choice([True, False], size=total_habitats)

comercio = np.random.choice([True, False], size=total_habitats)

aforo = np.random.randint(30, 50, size=total_habitats)

nombres_habitats_con_nulos = introducir_nulos(nombres_habitats, porcentaje_nulos_general)
cantidad_especies_con_nulos = introducir_nulos(cantidad_especies, porcentaje_nulos_general)
tipo_ambiente_con_nulos = introducir_nulos(ambientes, porcentaje_nulos_general)
permite_alimentos_con_nulos = introducir_nulos(permite_alimentos, porcentaje_nulos_general)
comercio_con_nulos = introducir_nulos(comercio, porcentaje_nulos_general)
aforo_con_nulos = introducir_nulos(aforo, porcentaje_nulos_general)


habitats = pd.DataFrame({
    'ID_show': habitat_ids,
    'nombre_habitat': nombres_habitats_con_nulos,
    'cantidad_especies': cantidad_especies_con_nulos,
    'tipo_ambiente': tipo_ambiente_con_nulos,
    'permite_alimentos': permite_alimentos_con_nulos,
    'comercio': comercio_con_nulos,
    'aforo': aforo_con_nulos
})

habitats = habitats.sort_values(by='ID_show').reset_index(drop=True)

# --- Guardar a CSV ---
carpeta_destino = 'zoo_dataset'
nombre_archivo_csv = 'habitats_sucio_generado.csv'

if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

nombre_archivo_csv = os.path.join(carpeta_destino, nombre_archivo_csv)

habitats.to_csv(nombre_archivo_csv, index=False, na_rep='NULL')

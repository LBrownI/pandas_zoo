import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from datetime import datetime

entradas = pd.read_csv("../zoo_dataset/entradas_zoo_limpio.csv", encoding="utf-8")
habitats = pd.read_csv("../zoo_dataset/habitats_generado.csv", encoding="utf-8")
entradas_habitats = pd.read_csv("../zoo_dataset/visitas_habitats_limpio.csv", encoding="utf-8")
entradas_shows = pd.read_csv("../zoo_dataset/visitas_shows_limpio.csv", encoding="utf-8")
shows = pd.read_csv("../zoo_dataset/shows_generado.csv", encoding="utf-8")


# Responder pregunta 1: ¿Qué días de la semana hay una mayor frecuencia de visitantes según cada rango etario?
def generar_grafico_1(dataframe, rango_etario_arg):
    entradas_filtradas = dataframe[dataframe["rango_etario"] == rango_etario_arg]
    entradas_dias = entradas_filtradas["día_semana"].value_counts().reset_index()

    plt.figure()
    sb.barplot(x="día_semana", y="count", data=entradas_dias)
    plt.title(f"Frecuencia de entradas de {rango_etario_arg} por día de la semana")
    plt.xlabel("Día de la semana")
    plt.ylabel("Cantidad")


rango_etarios = ["Adulto", "Niño", "Adulto Mayor"]
for edad in rango_etarios:
    generar_grafico_1(entradas, edad)


# Pregunta 2: ¿En qué meses hay una mayor frecuencia de visitantes?
entradas_fecha = entradas["fecha"].str.split("/", expand=True)
entradas_fecha.columns = ["día", "mes", "año"]
conteo_mes = entradas_fecha["mes"].value_counts().reset_index()

meses_orden = {
    "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril",
    "05": "Mayo", "06": "Junio", "07": "Julio", "08": "Agosto",
    "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
}

conteo_mes["mes_nombre"] = conteo_mes["mes"].map(meses_orden)
conteo_mes["mes_num"] = conteo_mes["mes"].astype(int)
conteo_mes = conteo_mes.sort_values("mes_num")

plt.figure()
sb.lineplot(x="mes_nombre", y="count", data=conteo_mes, marker="o")
plt.title("Visitas por mes")
plt.xlabel("Mes")
plt.ylabel("N° de Visitantes")

# Pregunta 3: ¿Existe alguna relación entre el tipo de ambiente de cada hábitat y la frecuencia de visitas?
left_join_entradas_habitats = pd.merge(entradas_habitats, habitats, how="left", on="ID_habitat")

print(habitats[["nombre_habitat", "tipo_ambiente"]])  # Cambiar a display en notebook

tipo_habitats = habitats[["nombre_habitat", "tipo_ambiente"]]

conteo_tipo_habitats = tipo_habitats["tipo_ambiente"].value_counts().reset_index()

print(conteo_tipo_habitats)

plt.figure()
plt.pie(conteo_tipo_habitats["count"], labels=conteo_tipo_habitats["tipo_ambiente"], autopct='%.0f%%')
plt.title("Distribución porcentual según tipo de hábitat")

conteo_tipo_habitats_entradas = left_join_entradas_habitats["nombre_habitat"].value_counts().reset_index()
plt.figure()
sb.barplot(x="count", y="nombre_habitat", data=conteo_tipo_habitats_entradas)
plt.title("N° de visitas en cada hábitat")
plt.xlabel("N° de visitantes")
plt.ylabel("Nombre hábitats")
plt.tight_layout()

conteo_entradas = left_join_entradas_habitats["tipo_ambiente"].value_counts().reset_index()

print(left_join_entradas_habitats)

print(left_join_entradas_habitats["tipo_ambiente"].value_counts().reset_index())

plt.figure()
sb.barplot(x="tipo_ambiente", y="count", data=conteo_entradas)
plt.title("Número de visitante por tipo de ambiente")
plt.xlabel("Tipo de ambiente")
plt.ylabel("N° de visitantes según tipo de ambiente")

# Pregunta 4: ¿La duración de los shows afecta la preferencia de los diferentes rangos etarios?
left_join_entradas_shows = pd.merge(entradas_shows, shows, how="left", on="ID_show")

left_join_entradas_shows_rango_etario = pd.merge(left_join_entradas_shows, entradas[["ID_entrada", "rango_etario"]], how="left", on="ID_entrada")

print(left_join_entradas_shows_rango_etario["rango_etario"].unique())

for rango in left_join_entradas_shows_rango_etario["rango_etario"].unique():
    filtro_edad_actual = left_join_entradas_shows_rango_etario[left_join_entradas_shows_rango_etario["rango_etario"] == rango]
    asistencia_segun_duracion = filtro_edad_actual["duracion"].value_counts().reset_index().sort_values(by="duracion")
    plt.figure()
    sb.barplot(x="duracion", y="count", data=asistencia_segun_duracion)
    plt.title(f"Frecuencia de asistencia a shows de {rango} según su duración")
    plt.xlabel("Duración del show (minutos)")
    plt.ylabel(f"N° de asistentes {rango}")
    plt.tight_layout()


# Pregunta 5: ¿En qué horario se concentra la mayor cantidad de visitas?
def hora_a_minutos(hora_str):
    try:
        t = datetime.strptime(hora_str, "%H:%M")
        return t.hour + t.minute / 60
    except:
        return None


entradas["hora_decimal"] = entradas["hora_ingreso"].apply(hora_a_minutos)

plt.figure()
sb.histplot(data=entradas, x="hora_decimal", bins=16, kde=False)
plt.title("Distribución de visitas por horario")
plt.xlabel("Hora del día (en formato decimal)")
plt.ylabel("Cantidad de visitas")
plt.xticks(ticks=range(9, 18), labels=[f"{h}:00" for h in range(9, 18)])
plt.tight_layout()

# Pregunta 6: ¿La presencia de comercios en los hábitats afecta la satisfacción de los visitantes?
for comercio in left_join_entradas_habitats["comercio"].unique():
    filtro_comercio = left_join_entradas_habitats[left_join_entradas_habitats["comercio"] == comercio].copy()
    filtro_comercio["satisfaccion"] = filtro_comercio["satisfaccion"].fillna("No responde")
    conteo_satisfaccion = filtro_comercio["satisfaccion"].value_counts().reset_index()
    plt.figure()
    plt.pie(conteo_satisfaccion["count"], labels=conteo_satisfaccion["satisfaccion"], autopct='%.0f%%')
    titulo_comercio = "SI" if comercio else "NO"
    plt.title(f"Satisfacción (1 a 5) de visitantes cuando {titulo_comercio} hay comercio")

# Pregunta 7: ¿La posibilidad de consumir alimentos dentro de los hábitats influye en la cantidad de visitas?
print("\n--- Pregunta 7 ---")
left_join_entradas_habitats['permite_alimentos_str'] = left_join_entradas_habitats['permite_alimentos'].astype(str)

visitas_por_permiso_alimentos = left_join_entradas_habitats.groupby("permite_alimentos_str")["ID_entrada"].count().reset_index()
visitas_por_permiso_alimentos.columns = ["permite_alimentos", "cantidad_visitas"]

visitas_por_permiso_alimentos["permite_alimentos_label"] = visitas_por_permiso_alimentos["permite_alimentos"].map({
    'True': 'Sí Permite Alimentos',
    'False': 'No Permite Alimentos',
    'nan': 'No Especificado',
    'true': 'Sí Permite Alimentos',
    'false': 'No Permite Alimentos'
})


plt.figure()
sb.barplot(x="permite_alimentos_label", y="cantidad_visitas", data=visitas_por_permiso_alimentos)
plt.title("Cantidad de visitas según si el hábitat permite alimentos")
plt.xlabel("¿Permite consumir alimentos en el hábitat?")
plt.ylabel("Cantidad de Visitas")
plt.tight_layout()
print(visitas_por_permiso_alimentos[["permite_alimentos_label", "cantidad_visitas"]])

# Pregunta 8: ¿Existe una correlación entre el porcentaje de cupos ocupados en los shows y el nivel de satisfacción de los visitantes?
print("\n--- Pregunta 8 ---")
merged_shows_satisfaccion = pd.merge(entradas_shows, shows, on="ID_show", how="left")

# Calcular porcentaje de ocupación (with NumPy np.where)
merged_shows_satisfaccion["porcentaje_ocupacion"] = np.where(
    merged_shows_satisfaccion["cupos_totales"] > 0,  # Condición
    (merged_shows_satisfaccion["cupos_ocupados"] / merged_shows_satisfaccion["cupos_totales"]) * 100,  # Valor si True
    0.0  # Valor si False (o si cupos_totales es 0 o NaN, ya que la condición sera False)
)

data_q8 = merged_shows_satisfaccion.dropna(subset=['satisfaccion', 'porcentaje_ocupacion'])

plt.figure()
sb.scatterplot(x="porcentaje_ocupacion", y="satisfaccion", data=data_q8, alpha=0.5)
plt.title("Correlación: % Ocupación Show vs Satisfacción del Visitante")
plt.xlabel("Porcentaje de Ocupación del Show (%)")
plt.ylabel("Nivel de Satisfacción (1-5)")
plt.tight_layout()

correlation_q8 = data_q8["porcentaje_ocupacion"].corr(data_q8["satisfaccion"])
print(f"Correlación entre porcentaje de ocupación y satisfacción: {correlation_q8:.2f}")


# Pregunta 9: ¿Existe una correlación entre el tipo de entrada (VIP) y el nivel de satisfacción de los visitantes?
print("\n--- Pregunta 9 ---")
merged_vip_satisfaccion_habitat = pd.merge(entradas_habitats, entradas[['ID_entrada', 'VIP']], on="ID_entrada", how="left")

# Convertir VIP a numérico para correlación (ej: True/1, False/0)
# Esto maneja booleanos, strings 'Si'/'No', 'True'/'False', y numéricos 0/1
if merged_vip_satisfaccion_habitat['VIP'].dtype == 'bool':
    merged_vip_satisfaccion_habitat['VIP_numeric'] = merged_vip_satisfaccion_habitat['VIP'].astype(int)
else:  # Si no es booleano, convierte a string para mapeo consistente
    merged_vip_satisfaccion_habitat['VIP_str'] = merged_vip_satisfaccion_habitat['VIP'].astype(str).str.lower()
    vip_map = {'true': 1, 'false': 0, 'si': 1, 'no': 0, '1': 1, '0': 0, '1.0': 1, '0.0': 0}
    merged_vip_satisfaccion_habitat['VIP_numeric'] = merged_vip_satisfaccion_habitat['VIP_str'].map(vip_map)

data_q9 = merged_vip_satisfaccion_habitat.dropna(subset=['satisfaccion', 'VIP_numeric'])

plt.figure()
sb.boxplot(x="VIP", y="satisfaccion", data=data_q9)  # Usa la columna VIP original para etiquetas del boxplot
plt.title("Nivel de Satisfacción en Hábitats según Tipo de Entrada (VIP)")
plt.xlabel("Tipo de Entrada VIP")
plt.ylabel("Nivel de Satisfacción (1-5)")
plt.tight_layout()

correlation_q9 = data_q9["VIP_numeric"].corr(data_q9["satisfaccion"])
print(f"Correlación (punto biserial) entre entrada VIP y satisfacción en hábitats: {correlation_q9:.2f}")


# Pregunta 10: ¿La adquisición de entradas VIP se relaciona con la asistencia a shows?
print("\n--- Pregunta 10 ---")
ids_asistieron_shows = entradas_shows["ID_entrada"].unique()
entradas_con_asistencia = entradas.copy()  # Trabaja sobre una copia
entradas_con_asistencia["asistio_show"] = entradas_con_asistencia["ID_entrada"].isin(ids_asistieron_shows)

contingency_table_q10 = pd.crosstab(entradas_con_asistencia["VIP"], entradas_con_asistencia["asistio_show"])
print("Tabla de contingencia VIP vs Asistencia a Shows:")
print(contingency_table_q10)

contingency_table_q10.plot(kind='bar', stacked=False)
plt.title("Relación entre Entrada VIP y Asistencia a Shows")
plt.xlabel("Tipo de Entrada VIP")
plt.ylabel("Cantidad de Entradas")
plt.xticks(rotation=0)
plt.legend(title="Asistió a Show", labels=["No Asistió", "Sí Asistió"])
plt.tight_layout()


# Pregunta 11: ¿Existe una correlación entre la cantidad de especies en un hábitat y el número de visitas anuales?
print("\n--- Pregunta 11 ---")
visitas_por_habitat = entradas_habitats.groupby("ID_habitat")["ID_entrada"].count().reset_index()
visitas_por_habitat.rename(columns={"ID_entrada": "numero_visitas"}, inplace=True)

merged_especies_visitas = pd.merge(visitas_por_habitat, habitats[["ID_habitat", "cantidad_especies", "nombre_habitat"]], on="ID_habitat", how="left")

data_q11 = merged_especies_visitas.dropna(subset=['numero_visitas', 'cantidad_especies'])

plt.figure()
sb.scatterplot(x="cantidad_especies", y="numero_visitas", data=data_q11, hue="nombre_habitat", legend=False, alpha=0.7)
plt.title("Correlación: Cantidad de Especies en Hábitat vs. Número de Visitas")
plt.xlabel("Cantidad de Especies")
plt.ylabel("Número de Visitas Anuales al Hábitat")
plt.tight_layout()

correlation_q11 = data_q11["cantidad_especies"].corr(data_q11["numero_visitas"])
print(f"Correlación entre cantidad de especies y número de visitas: {correlation_q11:.2f}")
print("\nDatos usados para el gráfico de Q11 (especies vs visitas):")
print(data_q11[["nombre_habitat", "cantidad_especies", "numero_visitas"]])

plt.show()

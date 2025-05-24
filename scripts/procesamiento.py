import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from datetime import datetime

entradas = pd.read_csv("../zoo_dataset/entradas_zoo_limpio.csv", encoding="utf-8")
habitats = pd.read_csv("../zoo_dataset/habitats_generado.csv", encoding="utf-8")
entradas_habitats = pd.read_csv("../zoo_dataset/visitas_habitats_limpio.csv", encoding="utf-8")
entradas_shows = pd.read_csv("../zoo_dataset/visitas_shows_limpio.csv", encoding="utf-8")
shows = pd.read_csv("../zoo_dataset/shows_generado.csv", encoding="utf-8")

# Responder pregunta 1:


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


# Responde pregunta 2:
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

# Responde pregunta 3:

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

# Responde pregunta 4:

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

# Responde pregunta 5


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

# Responde pregunta 6

for comercio in left_join_entradas_habitats["comercio"].unique():
    filtro_comercio = left_join_entradas_habitats[left_join_entradas_habitats["comercio"] == comercio]
    conteo_satisfaccion = filtro_comercio["satisfaccion"].value_counts().reset_index()
    plt.figure()
    plt.pie(conteo_satisfaccion["count"], labels=conteo_satisfaccion["satisfaccion"], autopct='%.0f%%')
    titulo_comercio = "hay comercio" if comercio else "NO hay comercio"
    plt.title(f"Satisfacción (1 a 5) de visitantes cuando {titulo_comercio} hay comercio")

plt.show()

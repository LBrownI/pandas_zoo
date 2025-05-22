import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

entradas = pd.read_csv("../zoo_dataset/entradas_zoo_sucio_generado.csv", encoding="utf-8", na_values=["NULL"])

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


plt.show()

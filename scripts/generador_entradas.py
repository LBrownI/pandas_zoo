import random
import os
import pandas as pd
import time
from datetime import datetime, timedelta

carpeta_destino = '../zoo_dataset'
nombre_archivo_csv = 'entradas_zoo_sucio_generado.csv'


def fecha_random(inicio, fin, formato, prop):
    tiempo_i = time.mktime(time.strptime(inicio, formato))
    tiempo_f = time.mktime(time.strptime(fin, formato))

    tiempo_p = tiempo_i + prop * (tiempo_i - tiempo_f)

    return time.strftime(formato, time.localtime(tiempo_p))


def hora_random():
    hora_inicio = datetime.strptime("09:30", "%H:%M")
    hora_fin = datetime.strptime("17:30", "%H:%M")
    delta = hora_fin - hora_inicio
    segundos_random = random.random() * delta.total_seconds()
    hora_generada = hora_inicio + timedelta(seconds=segundos_random)
    return hora_generada


def dia_semana(fecha):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    fecha_dt = datetime.strptime(fecha, "%d/%m/%Y")
    return dias[fecha_dt.weekday()]


diccionario_ventas = {"VIP": [], "rango_etario": [], "fecha": [], "día_semana": [], "hora_ingreso": []}

for _ in range(500):
    definir_nulo = random.randint(1, 400)
    fecha = ""
    if definir_nulo in range(1, 41):
        diccionario_ventas["VIP"].append(None)
    else:
        diccionario_ventas["VIP"].append(random.choice(["Si", "No"]))
    if definir_nulo in range(41, 81):
        diccionario_ventas["rango_etario"].append(None)
    else:
        diccionario_ventas["rango_etario"].append(random.choice(["Niño", "Adulto", "Adulto Mayor"]))
    if definir_nulo in range(81, 121):
        diccionario_ventas["fecha"].append(None)
    else:
        fecha = fecha_random("01/01/2025", "20/05/2025", "%d/%m/%Y", random.random())
        diccionario_ventas["fecha"].append(fecha)
    if definir_nulo in range(121, 161) or fecha == "":
        diccionario_ventas["día_semana"].append(None)
    else:
        diccionario_ventas["día_semana"].append(dia_semana(fecha))
    if definir_nulo in range(161, 201):
        diccionario_ventas["hora_ingreso"].append(None)
    else:
        diccionario_ventas["hora_ingreso"].append(hora_random().strftime("%H:%M"))

frame = pd.DataFrame(diccionario_ventas, columns=diccionario_ventas.keys())
frame.index.name = "ID_entrada"
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

nombre_archivo_csv = os.path.join(carpeta_destino, nombre_archivo_csv)

frame.to_csv(nombre_archivo_csv, na_rep='NULL')

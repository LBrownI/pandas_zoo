import random
from datetime import datetime, timedelta, time

VIP = [True, False]
rango_etario = ['Niños', 'Adultos', 'Adultos Mayores']
dia_semana = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def generar_fecha():
    # Rango de fechas: 1 de enero a 31 de diciembre de 2025
    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)

    # Número total de días entre fechas
    delta = end_date - start_date

    # Generar un número aleatorio de días desde la fecha inicial
    random_days = random.randint(0, delta.days)

    # Sumarlo a la fecha inicial
    random_date = start_date + timedelta(days=random_days)

    return random_date.date()  # solo fecha


def generar_hora():
    # Convertir el rango a minutos desde medianoche
    start_time = 9 * 60 + 30   # 9:30 = 570 minutos
    end_time = 17 * 60 + 30  # 17:30 = 1050 minutos

    # Elegir minutos aleatorios dentro del rango
    random_min = random.randint(start_time, end_time)

    # Convertir de vuelta a hora, minuto
    hora = random_min // 60
    minuto = random_min % 60

    # Segundo aleatorio
    segundo = random.randint(0, 59)

    return time(hora, minuto, segundo)


# Ejemplo
print(generar_fecha())
print(generar_hora())

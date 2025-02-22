# -*- coding: utf-8 -*-

import os
import pickle
import datetime

# Diccionario temporal que aloja los datos del archivo dat
datos_temporales = {
    "servicios": {},
    "estadistica": {},
    "stock": {}
}

# Limpia la pantalla
def cleaning():
    os.system("clear" if os.name == "posix" else "cls")

# Función para validar la existencia del archivo
def validating_existence_file(file_name):
    try:
        with open(file_name, "r+"):
            pass
    except IOError:
        with open(file_name, "w+"):
            pass

# En caso de que no exista un archivo dat, esta función asigna valores iniciales de productos.
def actualizar_stock_inicial(stock):
    """Inicializa el stock con una cantidad predeterminada de 10 por producto."""
    for categoria, productos in stock.items():
        for producto in productos:
            producto[2] = 10

# Levanta datos del archivo dat al programa en ejecución
def cargar_en_memoria(servicios, estadistica, stock):
    """Carga los datos en el diccionario temporal."""
    global datos_temporales
    datos_temporales["servicios"] = servicios
    datos_temporales["estadistica"] = estadistica
    datos_temporales["stock"] = stock

# Devuelve los datos almacenados en memoria
def obtener_datos():
    return datos_temporales["servicios"], datos_temporales["estadistica"], datos_temporales["stock"]

# Carga los datos del archivo dat
def cargar_datos(nombre_archivo='archivo.dat'):
    """Carga los datos desde un archivo o inicializa valores si no existe."""
    try:
        with open(nombre_archivo, 'rb') as archivo:
            servicios = pickle.load(archivo)
            estadistica = pickle.load(archivo)
            stock = pickle.load(archivo)
        print(f"\nDatos cargados desde {nombre_archivo} correctamente.")
    except (IOError, EOFError):
        print(f"\nNo se encontró {nombre_archivo} o está vacío. Creando nuevos diccionarios.")
        servicios = {}
        estadistica = {
            'total_servicios': 0,
            'cremaciones': 0,
            'cementerio': 0,
            'urnas': {i: 0 for i in range(1, 7)},
            'catering': {i: 0 for i in (10, 20, 30)},
            'autos': {i: 0 for i in (1, 2, 3)},
            'feretros': {i: 0 for i in range(1, 5)}
        }
        stock = {
            "feretros": [
                [1, "Básico", 0, 225000.0],
                [2, "Intermedio", 0, 305000.0],
                [3, "Superior", 0, 398000.0],
                [4, "Presidencial", 0, 785900.0]
            ],
            "urnas": [
                [1, "Madera", 0, 150000.0],
                [2, "Fibra de vidrio", 0, 160000.0],
                [3, "Cristal/Cerámica", 0, 198000.0],
                [4, "Mármol", 0, 233000.0],
                [5, "Acero", 0, 259000.0],
                [6, "Bronce/Cobre", 0, 310000.0]
            ],
            "autos": [
                [1, "2 autos", 0, 70000.0],
                [2, "3 autos", 0, 90000.0],
                [3, "5 autos", 0, 175000.0]
            ],
            "catering": [
                [10, "Normal (básico incluido)", 0, 80000.0],
                [20, "Intermedio", 0, 160000.0],
                [30, "Superior", 0, 195000.0]
            ]
        }
        actualizar_stock_inicial(stock)
        guardar_datos(nombre_archivo, servicios, estadistica, stock)
    return servicios, estadistica, stock

# Guarda las actualizaciones de los datos que se manipulan en el sistema
def guardar_datos(file_name, servicios, estadistica, stock, mostrar_dat=False):
    """Guarda los datos en un archivo."""
    with open(file_name, 'wb') as archivo:
        pickle.dump(servicios, archivo)
        pickle.dump(estadistica, archivo)
        pickle.dump(stock, archivo)
    if mostrar_dat:
        print(f"\nDatos guardados correctamente en {file_name}.")

# Verifica y actualiza las claves en estadística
def verificar_y_actualizar_claves(estadistica, tipo, codigo):
    estadistica.setdefault(tipo, {})
    estadistica[tipo].setdefault(codigo, 0)
    estadistica[tipo][codigo] += 1

# Actualiza e informa disponibilidad del inventario
def actualizar_inventario(stock, tipo, codigo, cantidad):
    for item in stock.get(tipo, []):
        if item[0] == codigo:
            if item[2] >= cantidad:
                item[2] -= cantidad
                return True
            print("\nNo hay suficiente cantidad de producto para completar el servicio.")
            return False
    print("\nCódigo no encontrado en el stock.")
    return False

# Función para calcular la facturación de un intervalo ingresado por teclado
def calcular_intervalo(intervalo):
    hoy = datetime.datetime.now()
    if intervalo == 1:
        return hoy.replace(hour=0, minute=0, second=0, microsecond=0), hoy
    elif intervalo == 2:
        fecha_inicio = hoy - datetime.timedelta(days=hoy.weekday())
        return fecha_inicio, fecha_inicio + datetime.timedelta(days=6)
    elif intervalo == 3:
        dia_inicio = 1 if hoy.day <= 15 else 16
        dia_fin = 15 if hoy.day <= 15 else (hoy.replace(day=28) + datetime.timedelta(days=4)).day
        return hoy.replace(day=dia_inicio, hour=0, minute=0, second=0, microsecond=0), hoy.replace(day=dia_fin, hour=23, minute=59, second=59, microsecond=999999)
    elif intervalo == 4:
        return hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0), (hoy.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
    else:
        raise ValueError("Intervalo no válido.")

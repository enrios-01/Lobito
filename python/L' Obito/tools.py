# -*- coding: utf-8 -*-


import pickle
from utils import validating_existence_file

datos_temporales = {
    "servicios": {},
    "estadistica": {},
    "stock": {}
}

def cargar_en_memoria(servicios, estadistica, stock):
    """Carga los datos en el diccionario temporal."""
    global datos_temporales
    datos_temporales["servicios"] = servicios
    datos_temporales["estadistica"] = estadistica
    datos_temporales["stock"] = stock

def obtener_datos():
    """Devuelve los datos almacenados en memoria."""
    return datos_temporales["servicios"], datos_temporales["estadistica"], datos_temporales["stock"]

def forzar_actualizacion(nombre_archivo='archivo.dat', mostrar_dat=False):
    """Fuerza la actualización del archivo .dat asegurando que los datos sean correctos."""
    
    # Cargar los datos actuales
    servicios, estadistica, stock = cargar_datos(nombre_archivo)
    
    # Verificar si 'autos' y otras claves importantes están en estadistica
    claves_requeridas = ['total_servicios', 'cremaciones', 'cementerio', 'urnas', 'catering', 'autos', 'feretros']
    for clave in claves_requeridas:
        if clave not in estadistica:
            estadistica[clave] = {}  # Se inicializa la clave si falta
    
    # Forzar el guardado correcto de los datos
    guardar_datos(nombre_archivo, servicios, estadistica, stock, mostrar_dat=mostrar_dat)
    if mostrar_dat:
        print("\n Archivo '{}' actualizado correctamente.".format(nombre_archivo))

def cargar_datos(nombre_archivo='archivo.dat'):
    """Carga los datos desde un archivo."""
    try:
        with open(nombre_archivo, 'rb') as archivo:
            servicios = pickle.load(archivo)
            estadistica = pickle.load(archivo)
            stock = pickle.load(archivo)
            print("\nDatos cargados desde {} correctamente.".format(nombre_archivo))
            return servicios, estadistica, stock
    except (IOError, EOFError):
        print("\nNo se encontró {} o está vacío. Creando nuevos diccionarios.".format(nombre_archivo))
        servicios = {}
        estadistica = {
            'total_servicios': 0,
            'cremaciones': 0,
            'cementerio': 0,
            'urnas': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0},
            'catering': {10: 0, 20: 0, 30: 0},
            'autos': {1: 0, 2: 0, 3: 0},
            'feretros': {1: 0, 2: 0, 3: 0, 4: 0}
        }
        stock = {
            "feretros": [
                [1, "Básico", 10, 225000.0],
                [2, "Intermedio", 8, 305000.0],
                [3, "Superior", 10, 398000.0],
                [4, "Presidencial", 10, 785900.0]
            ],
            "urnas": [
                [1, "Madera", 10, 150000.0],
                [2, "Fibra de vidrio", 8, 160000.0],
                [3, "Cristal/Cerámica", 6, 198000.0],
                [4, "Mármol", 5, 233000.0],
                [5, "Acero", 4, 259000.0],
                [6, "Bronce/Cobre", 4, 310000.0]
            ],
            "autos": [
                [1, "2 autos", 5, 70000.0],
                [2, "3 autos", 2, 90000.0],
                [3, "5 autos", 1, 175000.0]
            ],
            "catering": [
                [10, "Normal (básico incluido)", 8, 80000.0],
                [20, "Intermedio", 9, 160000.0],
                [30, "Superior", 8, 195000.0]
            ]
        }
        guardar_datos(nombre_archivo, servicios, estadistica, stock)
        return servicios, estadistica, stock

def guardar_datos(file_name, servicios, estadistica, stock, mostrar_dat=False):
    """Guarda los datos en un archivo."""
    with open(file_name, 'wb') as archivo:
        pickle.dump(servicios, archivo)
        pickle.dump(estadistica, archivo)
        pickle.dump(stock, archivo)
        if mostrar_dat:
            print("\nDatos guardados correctamente en {}.".format(file_name))

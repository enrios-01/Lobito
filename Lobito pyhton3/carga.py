# -*- coding: utf-8 -*-


import sys
from datetime import datetime
from stock import obtener_precio
from tools import (
    cargar_en_memoria, 
    guardar_datos, 
    cleaning, 
    actualizar_inventario, 
    verificar_y_actualizar_claves
)

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

# Valida formato de fecha y mantiene la coherencia de las fechas de nacimiento, defunción y servicio.
def validar_fecha(mensaje, fecha_maxima=None, fecha_minima=None):
    while True:
        fecha = input(mensaje)
        fecha = fecha.replace("/", "").replace("-", "") # Elimina separadores previos
        if len(fecha) == 8 and fecha.isdigit():
            dia = int(fecha[:2])
            mes = int(fecha[2:4])
            anio = int(fecha[4:])
            try:
                fecha_formateada = datetime(anio, mes, dia)
                if fecha_maxima and fecha_formateada > fecha_maxima:
                    print("\n\tLa fecha no puede ser posterior a la fecha permitida.")
                elif fecha_minima and fecha_formateada < fecha_minima:
                    print("\n\tLa fecha no puede ser anterior a la fecha mínima permitida.")
                else:
                    return fecha_formateada
            except ValueError:
                print("\n\tFecha invalida. Verifique el día, mes y año ingresados.")
        else:
            print("\n\tFormato invalido. Use DD-MM-YYYY o ingrese solo numeros para ser formateado automaticamente.")

# Calcula la edad del difunto
def calcular_edad(fecha_nacimiento, fecha_fallecimiento):
    edad = fecha_fallecimiento.year - fecha_nacimiento.year - ((fecha_fallecimiento.month, fecha_fallecimiento.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

# Funcion principal del programa, carga los servicios funerarios
def carga_servicios(servicios, estadistica, stock):
    ficha = {}
    while True:
        dni = input("\n\t\t\t\tIngrese el DNI del difunto: ")
        try:
            dni = int(dni)
            break
        except ValueError:
            print("\n\t\t\t\tDNI inválido. Ingrese solo números.")
    
    ape_nom = input("\n\t\t\t\tIngrese el nombre del difunto: ")
    fecha_nac = validar_fecha("\n\t\t\t\tIngrese la fecha de nacimiento (DD/MM/YYYY o DD-MM-YYYY): ", fecha_maxima=datetime.now())
    
    while True:
        fecha_def = validar_fecha("\n\t\t\t\tIngrese la fecha de fallecimiento (DD/MM/YYYY o DD-MM-YYYY): ", fecha_maxima=datetime.now(), fecha_minima=fecha_nac)
        if fecha_def >= fecha_nac:
            break
        print("\n\t\t\t\tError: La fecha de fallecimiento no puede ser anterior a la de nacimiento.")
    
    try:
        edad = calcular_edad(fecha_nac, fecha_def)
        print("\n\t\t\t\tEdad calculada del difunto: {} años".format(edad))
    except ValueError:
        print("\n\t\t\t\tError al calcular la edad. Verifique las fechas ingresadas.")
        edad = "Desconocida"
    
    while True:
        fecha_servicio = validar_fecha("\n\t\t\t\tIngrese la fecha del servicio (DD/MM/YYYY o DD-MM-YYYY): ")
        
        if fecha_servicio >= fecha_def:
            break # Si la fecha es válida, salimos del bucle
        
        print("\n\t\t\t\tError: La fecha del servicio no puede ser anterior a la fecha de fallecimiento.")
    
    ficha_1001 = []
    ficha_1002 = []
    while True:
        funeral = input("\n\t\t\t\tIngrese el código del funeral (1001 = cremación, 1002 = entierro): ")
        try:
            funeral = int(funeral)
            if funeral in [1001, 1002]:
                break
            else:
                print("\n\t\t\t\tCódigo de funeral inválido. Ingrese 1001 o 1002.")
        except ValueError:
            print("\n\t\t\t\tCódigo de funeral inválido. Ingrese solo números.")
    
    estadistica['total_servicios'] += 1
    
    if funeral == 1001: # CREMACIÓN
        estadistica['cremaciones'] += 1
        
        # Selección de urna
        while True:
            print("\n\t\t\t\tElija el tipo de urna:")
            print("\n\t\t\t\t1: Madera, 2: Fibra de vidrio, 3: Cristal/Cerámica, 4: Mármol, 5: Acero, 6: Bronce/Cobre")
            urna = input("\n\t\t\t\tIngrese el código de urna: ")
            try:
                urna = int(urna)
                if actualizar_inventario(stock, 'urnas', urna, 1):
                    verificar_y_actualizar_claves(estadistica, 'urnas', urna)
                    break
            except ValueError:
                print("\n\t\t\t\tCódigo de urna inválido. Ingrese solo números.")
        
        # Selección de catering
        while True:
            print("\n\t\t\t\tTipo de catering solicitado:") 
            print("\n\t\t\t\t010 = Normal (incluido en el servicio) - 020 = Intermedio - 030 = Superior")
            catering = input("\n\t\t\t\tIngrese el tipo de catering a contratar: ")
            
            try:
                catering = int(catering)
                if actualizar_inventario(stock, 'catering', catering, 1):
                    verificar_y_actualizar_claves(estadistica, 'catering', catering)
                    break
            except ValueError:
                print("\n\t\t\t\tCódigo de catering inválido. Ingrese solo números.")
        
        # Cálculo de costos
        costo = obtener_precio("urnas", urna) + obtener_precio("catering", catering)
        iva = costo * 0.21
        total = costo + iva
        ficha_1001.extend([urna, catering, costo, iva, total])
        ficha['funeral'] = funeral
        ficha['detalles'] = ficha_1001
    
    elif funeral == 1002: # CEMENTERIO
        estadistica['cementerio'] += 1
        
        # Selección de féretro
        while True:
            print("\n\t\t\t\tElija el tipo de féretro:")
            print("\n\t\t\t\t1: Básico, 2: Intermedio, 3: Superior, 4: Presidencial")
            feretro = input("\n\t\t\t\tIndique el código de féretro solicitado: ")
            try:
                feretro = int(feretro)
                if actualizar_inventario(stock, 'feretros', feretro, 1):
                    verificar_y_actualizar_claves(estadistica, 'feretros', feretro)
                    break
            except ValueError:
                print("\n\t\t\t\tCódigo de féretro inválido. Ingrese solo números.")
        
        # Selección de caravana
        while True:
            print("\n\t\t\t\tSeleccione el tipo de caravana:")
            print("\n\t\t\t\t1 = 2 autos - 2 = 3 autos - 3 = 5 autos")
            codigo_caravana = input("\n\t\t\t\tIngrese el código de caravana: ")
            try:
                codigo_caravana = int(codigo_caravana)
                if actualizar_inventario(stock, "autos", codigo_caravana, 1):
                    verificar_y_actualizar_claves(estadistica, 'autos', codigo_caravana)
                    break
            except ValueError:
                print("\n\t\t\t\tCódigo inválido. Ingrese solo números.")
        
        # Selección de catering
        while True:
            print("\n\t\t\t\tTipo de catering solicitado:")
            print("\n\t\t\t\t010 = Normal (incluido en el servicio) - 020 = Intermedio - 030 = Superior")
            catering = input("\n\t\t\t\tIngrese el tipo de catering a contratar: ")
            try:
                catering = int(catering)
                if actualizar_inventario(stock, 'catering', catering, 1):
                    verificar_y_actualizar_claves(estadistica, 'catering', catering)
                    break
            except ValueError:
                print("\n\t\t\t\tCódigo de catering inválido. Ingrese solo números.")
        
        # Ingreso del destino del féretro
        while True:
            destino = input("\n\t\t\t\tIngrese el destino del féretro (nombre del cementerio): ")
            if destino.strip():
                break
            else:
                print("\n\t\t\t\tEl destino no puede estar vacío.")
        
        # Cálculo de costos
        costo = obtener_precio("feretros", feretro) + obtener_precio("catering", catering) + obtener_precio("autos", codigo_caravana)
        iva = costo * 0.21
        total = costo + iva
        ficha_1002.extend([feretro, codigo_caravana, catering, destino, costo, iva, total])
        ficha['funeral'] = funeral
        ficha['detalles'] = ficha_1002

        # Actualización de la ficha
        ficha.update({
            'dni': dni,
            'nombre': ape_nom,
            'fecha_nacimiento': fecha_nac,
            'fecha_defuncion': fecha_def,
            'edad': edad,
            'fecha_servicio': fecha_servicio,
            'estado': True,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        # Registro del servicio
        servicios[dni] = ficha
        cargar_en_memoria(servicios, estadistica, stock)
        guardar_datos('archivo.dat', servicios, estadistica, stock)

        cleaning()
        print("\n\t\t\t\tServicio cargado exitosamente.")
        print("\n\t\t\t\t===== RESUMEN DEL SERVICIO =====")

        for clave, valor in ficha.items():
            print("\n\t\t\t\t{}: {}".format(clave.capitalize().replace("_", " "), valor))
        print("\n\t\t\t\t================*================")
        input("\n\t\t\t\tPresione ENTER para continuar...")

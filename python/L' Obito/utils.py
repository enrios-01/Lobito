# -*- coding: utf-8 -*-


import os
import pickle
import datetime

#Controla que existan los codigos de productos y cantidad disponible
def validate_stock(stock, tipo, codigo, estadistica):
    validacion = (10, 20, 30, 1, 2, 3, 4, 5, 6)  # Lista de códigos válidos
    if codigo not in validacion:  # Valida el código
        print "\n\tCódigo inválido. Ingrese un número válido."
        return False

    if not stock.has_key(tipo):  # Verifica que 'tipo' exista en stock
        print "\n\tError: '{}' no está en el stock.".format(tipo)
        return False

    for item in stock[tipo]:  # Verifica disponibilidad en el stock
        if item[0] == codigo:
            cantidad = item[2]
            if cantidad > 0:
                item[2] -= 1  # Reduce stock
                
                # **Nueva validación para evitar KeyError en estadistica**
                if not estadistica.has_key(tipo):
                    estadistica[tipo] = {}  # Se inicializa si no existe
                if not estadistica[tipo].has_key(codigo):
                    estadistica[tipo][codigo] = 0  # Se inicializa si no existe
                estadistica[tipo][codigo] += 1  # Se actualiza la estadística
                
                return True
            else:
                print "\n\tProducto no disponible. Elija otro."
                return False

    print "\n\tCódigo no encontrado en el stock."  # Si el código no se encuentra en el stock
    return False

# Función para validar la existencia del archivo
def validating_existence_file(file_name):
    try:
        object_type_file = open(file_name, "r+")
    except IOError:
        object_type_file = open(file_name, "w+")
    object_type_file.close()

#Limpia la pantalla
def cleaning():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")
        
# Función para registrar un servicio y actualizar el inventario
def registrar_servicio(servicio, cantidad, productos, servicios_vendidos):
    """Registra un servicio vendido y actualiza el inventario."""
    if servicio in productos and productos[servicio][0] >= cantidad:  # Verifica si hay suficiente cantidad
        productos[servicio][0] -= cantidad  # Resta del inventario
        # Registra el servicio vendido
        servicios_vendidos.append({'servicio': servicio, 'cantidad': cantidad, 'fecha': datetime.datetime.now()})
        print "\n\tServicio registrado con éxito."
    else:
        print "\n\tNo hay suficiente cantidad de producto para completar el servicio."

# Función para calcular la facturación de un intervalo ingresado por teclado
def calcular_intervalo(intervalo):
    hoy = datetime.datetime.now()

    if intervalo == 1:  # Diario
        fecha_inicio = hoy.replace(hour=0, minute=0, second=0, microsecond=0)
        fecha_final = hoy
    elif intervalo == 2:  # Semanal
        fecha_inicio = hoy - datetime.timedelta(days=hoy.weekday())
        fecha_final = fecha_inicio + datetime.timedelta(days=6)
    elif intervalo == 3:  # Quincenal
        if hoy.day <= 15:
            fecha_inicio = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            fecha_final = hoy.replace(day=15, hour=23, minute=59, second=59, microsecond=999999)
        else:
            fecha_inicio = hoy.replace(day=16, hour=0, minute=0, second=0, microsecond=0)
            fecha_final = (hoy + datetime.timedelta(days=(31 - hoy.day))).replace(day=1) - datetime.timedelta(days=1)
    elif intervalo == 4:  # Mensual
        fecha_inicio = hoy.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        fecha_final = (hoy + datetime.timedelta(days=(31 - hoy.day))).replace(day=1) - datetime.timedelta(days=1)
    elif intervalo == 5:  # Trimestral
        mes_inicio = ((hoy.month - 1) // 3) * 3 + 1
        fecha_inicio = hoy.replace(month=mes_inicio, day=1, hour=0, minute=0, second=0, microsecond=0)
        fecha_final = (fecha_inicio + datetime.timedelta(days=92)).replace(day=1) - datetime.timedelta(days=1)
    elif intervalo == 6:  # Semestral
        mes_inicio = 1 if hoy.month <= 6 else 7
        fecha_inicio = hoy.replace(month=mes_inicio, day=1, hour=0, minute=0, second=0, microsecond=0)
        fecha_final = (fecha_inicio + datetime.timedelta(days=183)).replace(day=1) - datetime.timedelta(days=1)
    elif intervalo == 7:  # Anual
        fecha_inicio = hoy.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        fecha_final = hoy.replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
    else:
        raise ValueError("Intervalo no válido.")

    return fecha_inicio, fecha_final

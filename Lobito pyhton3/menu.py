# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from tools import cargar_en_memoria, obtener_datos, cargar_datos, validating_existence_file, cleaning
from carga import carga_servicios, servicios
from stock import menu_stock
from consultas import modificar_servicio, eliminar_servicio, menu_gestion_servicios

def verificar_usuario(usuarios, claves):
    print("\n\t\t\t\t")
    print("\t\t\t\t=============================")
    print("\t\t\t\tL'Obito  Servicios exequiales")
    print("\t\t\t\t=============================")
    print(" \n\t\t\t\tInicio de sesion")
    
    ingreso = input("\n\t\t\t\tUSUARIO: ")
    encontrado = False
    for i in range(len(usuarios)):
        if usuarios[i] == ingreso:
            encontrado = True
            while True:
                clave = input("\n\t\t\t\tCLAVE: ")
                if claves[i] == clave:
                    print("\n\t\t\t\tBienvenido al sistema")
                    return True
                else:
                    print("\n\t\t\t\tClave incorrecta. Intente de nuevo.")
            break
    
    if not encontrado:
        print("\n\t\t\t\tUsuario no encontrado.")
    return False

usuarios = ("enrios", "gcafferata", "slachin", "mcanda")
claves = ("rios2025", "cafferata2025", "lachin2025", "canda2025")

if not verificar_usuario(usuarios, claves):
    print("\n\t\t\t\tAcceso denegado.")
    exit()

menu_opciones = (
    "\n\n\n\n\ ",
    "\n\t\t\t\t---- Menú de Gestión L'Obito ----",
    "\n\t\t\t\t1. Servicios",
    "\n\t\t\t\t2. Facturacion",
    "\n\t\t\t\t3. Gestión de Stock",
    "\n\t\t\t\t4. Salir"
)

def mostrar_menu(menu_opciones):
    for opcion in menu_opciones:
        print(opcion)
    while True:
        try:
            opcion = int(input("\n\t\t\t\tSeleccione una opci\u00f3n: "))
            if 1 <= opcion <= len(menu_opciones):
                return opcion
            else:
                print("\n\t\t\t\tOpci\u00f3n inv\u00e1lida. Por favor, ingrese un n\u00famero v\u00e1lido.")
        except ValueError:
            print("\n\t\t\t\tEntrada inv\u00e1lida. Debe ingresar un n\u00famero entero.")

sub_menu_carga = (
    "\n\t\t\t\t1. Cargar servicios",
    "\n\t\t\t\t2. Modificar Servicio",
    "\n\t\t\t\t3. Eliminar Servicios",
    "\n\t\t\t\t4. SALIR"
)

validating_existence_file("archivo.dat")
servicios, estadistica, stock = cargar_datos()
cargar_en_memoria(servicios, estadistica, stock)

while True:
    cleaning()
    opcion = mostrar_menu(menu_opciones)
    
    if opcion == 1:
        while True:
            cleaning()
            sub_opcion = mostrar_menu(sub_menu_carga)
            
            if sub_opcion == 1:
                carga_servicios(servicios, estadistica, stock)
            elif sub_opcion == 2:
                modificar_servicio()
            elif sub_opcion == 3:
                eliminar_servicio('archivo.dat')
            elif sub_opcion == 4:
                break

        cargar_en_memoria(servicios, estadistica, stock)
    
    elif opcion == 2:
        cleaning()
        menu_gestion_servicios()
    elif opcion == 3:
        cleaning()
        menu_stock(stock)
    elif opcion == 4:
        cleaning()
        print("\n\t\t\t\tSaliendo del programa...")
        cargar_en_memoria(servicios, estadistica, stock)
        break

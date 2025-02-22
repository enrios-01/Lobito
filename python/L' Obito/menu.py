# -*- coding: utf-8 -*-


from utils import validating_existence_file, cleaning
from tools import cargar_en_memoria, obtener_datos, cargar_datos
from carga import carga_servicios
from stock import menu_stock
from consultas import menu_consultas
from reportes import generar_reportes

# Función de verificación de usuario
def verificar_usuario(usuarios, claves):
    """Función que verifica el nombre de usuario y la clave ingresados. Si el usuario existe y la clave es correcta, muestra un mensaje de bienvenida. 
    Si el usuario no existe o la clave es incorrecta, muestra un mensaje de error."""
    print "\n\t\t\t\t"
    print "\t\t\t\t============================="
    print "\t\t\t\tL'Obito  Servicios exequiales"
    print "\t\t\t\t============================="
    print " \n\t\t\t\tInicio de sesion"
    ingreso = raw_input("\n\t\t\t\tUSUARIO: ")

    while ingreso in usuarios:
        clave = raw_input("\n\t\t\t\tCLAVE: ")
        indice = usuarios.index(ingreso)
        if clave == claves[indice]:
            print("\n\t\t\t\t¡Bienvenido al sistema, {}!".format(ingreso))    
            return True
        else:
            print "\n\t\t\t\tClave incorrecta. Intenta nuevamente."
    else:
        print "\n\t\t\t\tUsuario no encontrado."
        return False

# Usuarios y claves autorizados
usuarios = ('enrios', 'gacafferata', 'selachin', 'macanda')
claves = ('rios2025', 'cafferata2025', 'lachin2025', 'canda2025')

# Verificar usuario antes de mostrar el menú
if not verificar_usuario(usuarios, claves):
    print "\n\t\t\t\t\t\tAcceso denegado."
    exit()

menu_opciones = ( "\n\n\n\n\ ", 

    "\n\t\t\t\t\t\t---- Menú de Gestión L'Obito ----",
    "\n\t\t\t\t\t\t1. Registrar nuevo servicio",
    "\n\t\t\t\t\t\t2. Gestión de Servicios",
    "\n\t\t\t\t\t\t3. Gestión de Stock",
    "\n\t\t\t\t\t\t4. Gestion de Facturación",
    "\n\t\t\t\t\t\t5. Salir"
)

def mostrar_menu(menu_opciones):
    for opcion in menu_opciones:
        print(opcion)
    while True:
        try:
            opcion = raw_input("\n\t\t\t\t\t\tSeleccione una opción: ")
            opcion = int(opcion)
            if 1 <= opcion <= 5:
                return opcion
            else:
                print "\n\t\t\t\t\t\tOpción inválida. Por favor, ingrese un número del 1 al 5."
        except ValueError:
            print "\n\t\t\t\t\t\tEntrada inválida. Debe ingresar un número entero."
            
validating_existence_file("archivo.dat")
servicios, estadistica, stock = cargar_datos()
cargar_en_memoria(servicios, estadistica, stock)

while True:
    cleaning()
    opcion = mostrar_menu(menu_opciones)
    if opcion == 1:
        cleaning()
        servicios, estadistica, stock = obtener_datos()  # 1. Cargar los datos antes de operar
        carga_servicios(servicios, estadistica, stock)  # 2. Trabajar con los datos cargados
        cargar_en_memoria(servicios, estadistica, stock) # 3. Guardar los datos al salir de la opción
    elif opcion == 2:
        cleaning()
        menu_consultas(servicios)
    elif opcion == 3:
        cleaning()
        menu_stock(stock)
    elif opcion == 4:
        cleaning()
        generar_reportes()
    elif opcion == 5:
        cleaning()
        print "\n\t\t\t\tSaliendo del programa..."
        cargar_en_memoria(servicios, estadistica, stock)
        break

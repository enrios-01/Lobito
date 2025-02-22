# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from carga import servicios
from utils import cleaning
from tools import obtener_datos, cargar_en_memoria, guardar_datos

def actualizar_estado_servicios(servicios):
    fecha_actual = datetime.now()
    for servicio in servicios.values():
        fecha_servicio = servicio["fecha_servicio"]
        if not isinstance(fecha_servicio, datetime):
            try:
                # Intentar convertir la fecha al formato datetime
                fecha_servicio = datetime.strptime(fecha_servicio, "%d-%m-%Y")
                servicio["fecha_servicio"] = fecha_servicio
            except ValueError:
                print "\n\tFormato de fecha inválido en el servicio con DNI: {}".format(servicio["dni"])
                continue
        if fecha_actual > fecha_servicio + timedelta(days=1):
            servicio["estado"] = False
            
def mostrar_servicios_pendientes(servicios):
    actualizar_estado_servicios(servicios)  # Pasa el diccionario `servicios`
    print "\n\t--- Servicios Pendientes ---"
    for servicio in servicios.values():
        if servicio["estado"]:  # Filtra servicios pendientes
            print("\n\tDNI: {}, Nombre: {}, Fecha Servicio: {}".format(
                servicio["dni"], servicio["nombre"], servicio["fecha_servicio"]
            ))
    print "\n\t--- Fin de Servicios Pendientes ---"

def mostrar_servicios_realizados(servicios):
    if not servicios:
        print "\n\tNo hay servicios registrados."
        return
    print "\n\t---- Lista de servicios realizados ----"
    # Encabezado
    encabezado = "{:<10} {:<20} {:<15} {:<15} {:<10} {:<15}".format(
        "ID", "Nombre", "Nacimiento", "Defunción", "Edad", "Fecha Servicio"
    )
    print(encabezado)
    print("-" * len(encabezado))  # Línea separadora
    # Fecha actual
    fecha_actual = datetime.now()
    # Filtrar y mostrar servicios realizados
    servicios_realizados = False  # Bandera para verificar si hay servicios realizados
    for id_servicio, detalles in servicios.items():
        fecha_servicio = detalles.get("fecha_servicio", "")
        if isinstance(fecha_servicio, datetime):
            # Determinar si el servicio es realizado
            if (fecha_actual - fecha_servicio).days >= 1 or not detalles.get("estado", True):
                servicios_realizados = True
                print("{:<10} {:<20} {:<15} {:<15} {:<10} {:<15}".format(
                    id_servicio,
                    detalles.get("nombre", ""),
                    detalles.get("fecha_nacimiento", "").strftime("%d/%m/%Y") if isinstance(detalles.get("fecha_nacimiento", ""), datetime) else detalles.get("fecha_nacimiento", ""),
                    detalles.get("fecha_defuncion", "").strftime("%d/%m/%Y") if isinstance(detalles.get("fecha_defuncion", ""), datetime) else detalles.get("fecha_defuncion", ""),
                    detalles.get("edad", ""),
                    fecha_servicio.strftime("%d/%m/%Y")
                ))
    if not servicios_realizados:
        print "\n\tNo hay servicios realizados en este momento."
    print "\n\t-- Fin de los Servicios Realizados --"

def listar_todos_los_servicios(servicios):
    if not servicios:
        print "\n\tNo hay servicios registrados."
        return
    print "\n\t---- Lista de todos los servicios ----"
    # Encabezado
    encabezado = "\n\t{:<10} {:<20} {:<15} {:<15} {:<10} {:<15} {:<10}".format(
        "ID", "Nombre", "Nacimiento", "Defunción", "Edad", "Fecha Servicio", "Estado"
    )
    print(encabezado)
    print("-" * len(encabezado))  # Línea separadora
    # Fecha actual
    fecha_actual = datetime.now()
    # Detalles de los servicios
    for id_servicio, detalles in servicios.items():
        fecha_servicio = detalles.get("fecha_servicio", "")
        if isinstance(fecha_servicio, datetime):
            # Calcular si el estado es Pendiente o Realizado
            estado = "Pendiente" if detalles.get("estado", True) and (fecha_actual - fecha_servicio).days < 1 else "Realizado"
            print("{:<10} {:<20} {:<15} {:<15} {:<10} {:<15} {:<10}".format(
                id_servicio,
                detalles.get("nombre", ""),
                detalles.get("fecha_nacimiento", "").strftime("%d/%m/%Y") if isinstance(detalles.get("fecha_nacimiento", ""), datetime) else detalles.get("fecha_nacimiento", ""),
                detalles.get("fecha_defuncion", "").strftime("%d/%m/%Y") if isinstance(detalles.get("fecha_defuncion", ""), datetime) else detalles.get("fecha_defuncion", ""),
                detalles.get("edad", ""),
                fecha_servicio.strftime("%d/%m/%Y"),
                estado
            ))
    print "\n\t-- Fin de los Servicios --"

def eliminar_servicio(archivo='archivo.dat'):
    servicios, estadistica, stock = obtener_datos()
    cargar_en_memoria(servicios, estadistica, stock)

    print("\nINFORME - Contenido de servicios cargados:")
    print(servicios)  # Ver qué datos están en el archivo

    cleaning()
    print "\nEliminar SERVICIO.\n\n"
    id_servicio = raw_input("\n\t\tIngrese el DNI del difunto cuyo servicio desea eliminar: ")
    
    try:
        id_servicio = int(id_servicio)  # Convertir a entero
    except ValueError:
        print "\nERROR - El DNI ingresado no es un número válido.\n"
        raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
        return

    cleaning()
    
    if id_servicio in servicios.keys():
        del servicios[id_servicio]
        print "\nAVISO - Se ELIMINO el servicio:"
        print(servicios)  # Verificar que el servicio se eliminó
        guardar_datos(archivo, servicios, estadistica, stock)
        cleaning()
        print "\n\t\tEl SERVICIO ha sido eliminado del SISTEMA exitosamente."
    else:
        print "\nEl SERVICIO con DNI N°", id_servicio, "que desea eliminar, NO ESTÁ REGISTRADO.\n"
    
    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")

def modificar_servicio(archivo='archivo.dat'):
    servicios, estadistica, stock = obtener_datos()
    cleaning()
    print "\nModificar SERVICIO.\n\n"
    
    id_servicio = raw_input("\n\t\tIngrese el DNI del difunto cuyo servicio desea modificar: ")
    
    try:
        id_servicio = int(id_servicio)  # Convertir a entero
    except ValueError:
        print "\nERROR - El DNI ingresado no es un número válido.\n" 
        raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
        return

    cleaning()

    if id_servicio in servicios.keys():
        temporal = servicios[id_servicio]
        print "\nLos datos del SERVICIO con DNI N°", id_servicio, "a modificar son:\n"
        print "\n\t\t1. Nombre:", temporal['nombre']
        print "\n\t\t2. Fecha de nacimiento:", temporal['fecha_nacimiento']
        print "\n\t\t3. Fecha de defunción:", temporal['fecha_defuncion']
        print "\n\t\t4. Edad:", temporal['edad']
        print "\n\t\t5. Fecha del servicio:", temporal['fecha_servicio']
        print "\n\t\t6. Tipo de servicio:", "Cremación" if temporal['funeral'] == 1001 else "Entierro"
        print "\n\t\t7. Detalles del servicio:", temporal['detalles']
        print "\n\n\n\t\t8. Salir SIN MODIFICAR DATOS del SERVICIO."
        
        atributo = raw_input("\n\n\t\tIngrese una opción: ")
        
        try:
            atributo = int(atributo)
        except ValueError:
            print "\nERROR - Opción inválida.\n" 
            raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
            return

        cleaning()

        if atributo != 8:
            msje = "Ingrese "
            etiquetas = {
                1: "Nombre",
                2: "Fecha de nacimiento (DD/MM/YYYY)",
                3: "Fecha de defunción (DD/MM/YYYY)",
                4: "Edad",
                5: "Fecha del servicio (DD/MM/YYYY)",
                6: "Tipo de servicio (1001 = cremación, 1002 = entierro)",
                7: "Detalles del servicio"
            }

            if atributo not in etiquetas:
                print "\nERROR - Opción inválida.\n"
                raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
                return

            msje += etiquetas[atributo] + ": "
            dato = raw_input(msje)

            # Diccionario correcto para mapear la opción del usuario con la clave real del diccionario
            atributos_dict = {
                1: "nombre",
                2: "fecha_nacimiento",
                3: "fecha_defuncion",
                4: "edad",
                5: "fecha_servicio",
                6: "funeral",
                7: "detalles"
            }
            
            clave_atributo = atributos_dict.get(atributo)

            if clave_atributo:
                temporal[clave_atributo] = dato
                servicios[id_servicio] = temporal  # Asegurar que se actualiza correctamente en el diccionario
                
                guardar_datos(archivo, servicios, estadistica, stock)  # Guardar cambios
                cleaning()
                print "\n\t\tEl SERVICIO ha sido modificado en el SISTEMA exitosamente."
            else:
                print "\n\t\tERROR - Opción inválida."
        else:
            print "\n\t\tNO ha sido modificado ningún atributo del SERVICIO en el SISTEMA."
    else:
        print "\nEl SERVICIO con DNI N°", id_servicio, "que desea modificar, NO ESTÁ REGISTRADO.\n"

    raw_input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")

validacion = (1, 2, 3, 4, 5, 6)  # Opciones válidas del menú

sub_menu = ("\n\t\t\t\t---- Menú de Consultas de Servicios ----",
            "\n\t\t\t\t1. Mostrar servicios pendientes",
            "\n\t\t\t\t2. Mostrar servicios realizados",
            "\n\t\t\t\t3. Listar todos los servicios",
            "\n\t\t\t\t4. Modificar servicio agendado",
            "\n\t\t\t\t5. Eliminar servicio agendado",
            "\n\t\t\t\t6. Volver al menú principal")

def menu_consultas(servicios):
    while True:
        for linea in sub_menu:
            print(linea)

        opcion = raw_input("\n\t\t\t\tSeleccione una opción: ")
        opcion = int(opcion)

        if opcion == 1:
            cleaning()
            mostrar_servicios_pendientes(servicios)
        elif opcion == 2:
            cleaning()
            mostrar_servicios_realizados(servicios)
        elif opcion == 3:
            cleaning()
            listar_todos_los_servicios(servicios)
        elif opcion == 4:
            cleaning()
            modificar_servicio()
        elif opcion == 5:
            cleaning()
            eliminar_servicio('archivo.dat')
        elif opcion == 6:
            break
        else:
            print "\n\t\t\t\tOpción inválida. Por favor, intente nuevamente."

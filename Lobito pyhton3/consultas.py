# -*- coding: utf-8 -*-


from stock import stock
from datetime import datetime, timedelta
from carga import servicios, carga_servicios, estadistica
from tools import obtener_datos, cargar_en_memoria, guardar_datos, cleaning, calcular_intervalo

def actualizar_estado_servicios(servicios):
    fecha_actual = datetime.now()
    for servicio in servicios.values():
        fecha_servicio = servicio["fecha_servicio"]
        if not isinstance(fecha_servicio, datetime):
            try:
                fecha_servicio = datetime.strptime(fecha_servicio, "%d-%m-%Y")
                servicio["fecha_servicio"] = fecha_servicio
            except ValueError:
                print("\n\tFormato de fecha inválido en el servicio con DNI: {}".format(servicio["dni"]))
                continue
        if fecha_actual > fecha_servicio + timedelta(days=1):
            servicio["estado"] = False

def mostrar_servicios_pendientes(servicios):
    actualizar_estado_servicios(servicios)
    print("\n\t--- Servicios Pendientes ---")
    for servicio in servicios.values():
        if servicio["estado"]:
            print("\n\tDNI: {}, Nombre: {}, Fecha Servicio: {}".format(
                servicio["dni"], servicio["nombre"], servicio["fecha_servicio"].strftime("%d/%m/%Y")
            ))
    print("\n\t--- Fin de Servicios Pendientes ---")

def mostrar_servicios_realizados(servicios):
    if not servicios:
        print("\n\tNo hay servicios registrados.")
        return
    print("\n\t---- Lista de servicios realizados ----")
    encabezado = "{:<10} {:<20} {:<15} {:<15} {:<10} {:<15}".format(
        "ID", "Nombre", "Nacimiento", "Defunción", "Edad", "Fecha Servicio"
    )
    print(encabezado)
    print("-" * len(encabezado))
    
    fecha_actual = datetime.now()
    servicios_realizados = False

    for id_servicio, detalles in servicios.items():
        fecha_servicio = detalles.get("fecha_servicio", "")
        try:
            fecha_str = fecha_servicio.strftime("%d/%m/%Y")
            diferencia_dias = (fecha_actual - fecha_servicio).days
        except AttributeError:
            fecha_str = fecha_servicio
            diferencia_dias = 0

        if diferencia_dias >= 1 or not detalles.get("estado", True):
            servicios_realizados = True
            fecha_nacimiento = detalles.get("fecha_nacimiento", "")
            fecha_defuncion = detalles.get("fecha_defuncion", "")

            print("{:<10} {:<20} {:<15} {:<15} {:<10} {:<15}".format(
                id_servicio,
                detalles.get("nombre", ""),
                fecha_nacimiento,
                fecha_defuncion,
                detalles.get("edad", ""),
                fecha_str
            ))
    
    if not servicios_realizados:
        print("\n\t\t\tNo hay servicios realizados en este momento.")
    print("\n\t\t\t-- Fin de los Servicios Realizados --")

def listar_todos_los_servicios(servicios):
    if not servicios:
        print("\n\t\t\tNo hay servicios registrados.")
        return
    print("\n\t\t\t---- Lista de todos los servicios ----")
    encabezado = "{:<10} {:<20} {:<15} {:<15} {:<10} {:<15} {:<10}".format(
        "ID", "Nombre", "Nacimiento", "Defunción", "Edad", "Fecha Servicio", "Estado"
    )
    print(encabezado)
    print("-" * len(encabezado))
    
    fecha_actual = datetime.now()
    for id_servicio, detalles in servicios.items():
        fecha_servicio = detalles.get("fecha_servicio", "")
        try:
            fecha_str = fecha_servicio.strftime("%d/%m/%Y")
            diferencia_dias = (fecha_actual - fecha_servicio).days
        except AttributeError:
            fecha_str = fecha_servicio
            diferencia_dias = 0
        estado = "Pendiente" if detalles.get("estado", True) and diferencia_dias < 1 else "Realizado"
        fecha_nacimiento = detalles.get("fecha_nacimiento", "")
        fecha_defuncion = detalles.get("fecha_defuncion", "")

        print("{:<10} {:<20} {:<15} {:<15} {:<10} {:<15} {:<10}".format(
            id_servicio,
            detalles.get("nombre", ""),
            fecha_nacimiento,
            fecha_defuncion,
            detalles.get("edad", ""),
            fecha_str,
            estado
        ))
    print("\n\t-- Fin de los Servicios --")

def eliminar_servicio(archivo='archivo.dat'):
    servicios, estadistica, stock = obtener_datos()
    cargar_en_memoria(servicios, estadistica, stock)
    print("\nINFORME - Contenido de servicios cargados:")
    print(servicios)
    cleaning()
    print("\nEliminar SERVICIO.\n\n")
    id_servicio = input("\n\t\tIngrese el DNI del difunto cuyo servicio desea eliminar: ")
    try:
        id_servicio = int(id_servicio)
    except ValueError:
        print("\nERROR - El DNI ingresado no es un número válido.\n")
        input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
        return
    cleaning()
    if id_servicio in servicios.keys():
        del servicios[id_servicio]
        print("\nAVISO - Se ELIMINÓ el servicio:")
        print(servicios)
        guardar_datos(archivo, servicios, estadistica, stock)
        cleaning()
        print("\n\t\tEl SERVICIO ha sido eliminado del SISTEMA exitosamente.")
    else:
        print("\nEl SERVICIO con DNI N°", id_servicio, "que desea eliminar, NO ESTÁ REGISTRADO.\n")
    input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
    
#Funcion que modifica los servicios cargados y alojados en el archivo dat
def modificar_servicio(archivo='archivo.dat'):
    servicios, estadistica, stock = obtener_datos()
    cleaning()
    print("\nModificar SERVICIO.\n\n")

    id_servicio = input("\n\t\tIngrese el DNI del difunto cuyo servicio desea modificar: ")

    try:
        id_servicio = int(id_servicio)  # Convertir a entero
    except ValueError:
        print("\nERROR - El DNI ingresado no es un número válido.\n")
        input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
        return

    cleaning()

    if id_servicio in servicios.keys():
        temporal = servicios[id_servicio]
        print("\nLos datos del SERVICIO con DNI N°", id_servicio, "a modificar son:\n")
        print("\n\t\t1. Nombre:", temporal['nombre'])
        print("\n\t\t2. Fecha de nacimiento:", temporal['fecha_nacimiento'])
        print("\n\t\t3. Fecha de defunción:", temporal['fecha_defuncion'])
        print("\n\t\t4. Edad:", temporal['edad'])
        print("\n\t\t5. Fecha del servicio:", temporal['fecha_servicio'])
        print("\n\t\t6. Tipo de servicio:", "Cremación" if temporal['funeral'] == 1001 else "Entierro")
        print("\n\t\t7. Detalles del servicio:", temporal['detalles'])
        print("\n\n\n\t\t8. Salir SIN MODIFICAR DATOS del SERVICIO.")

        atributo = input("\n\n\t\tIngrese una opción: ")

        try:
            atributo = int(atributo)
        except ValueError:
            print("\nERROR - Opción inválida.\n")
            input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
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
                print("\nERROR - Opción inválida.\n")
                input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")
                return

            msje += etiquetas[atributo] + ": "
            dato = input(msje)

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
                print("\n\t\tEl SERVICIO ha sido modificado en el SISTEMA exitosamente.")
            else:
                print("\n\t\tERROR - Opción inválida.")
        else:
            print("\n\t\tNO ha sido modificado ningún atributo del SERVICIO en el SISTEMA.")
    else:
        print("\nEl SERVICIO con DNI N°", id_servicio, "que desea modificar, NO ESTÁ REGISTRADO.\n")

    input("\n\n\t\t\t\tPresione la tecla ENTER para continuar.")

def servicios_mas_contratados(estadistica):
    informe = (
        estadistica['cementerio'], estadistica['cremaciones'],
        estadistica['urnas'].get(1, 0), estadistica['urnas'].get(2, 0), estadistica['urnas'].get(3, 0), estadistica['urnas'].get(4, 0),
        estadistica['urnas'].get(5, 0), estadistica['urnas'].get(6, 0),
        estadistica['catering'].get(10, 0), estadistica['catering'].get(20, 0), estadistica['catering'].get(30, 0),
        estadistica['autos'].get(1, 0), estadistica['autos'].get(2, 0), estadistica['autos'].get(3, 0),
        estadistica['feretros'].get(1, 0), estadistica['feretros'].get(2, 0), estadistica['feretros'].get(3, 0), estadistica['feretros'].get(4, 0)
    )
    total_caravana = sum(estadistica['autos'].values())
    total_catering = sum(estadistica['catering'].values())
    total_servicios_realizados = estadistica['cementerio'] + estadistica['cremaciones']

    print("\t\t\t*Reporte de Servicios Contratados*")
    print("\t\t\tTotal de servicios realizados: ", total_servicios_realizados)
    print("\t\t\t* Cremación: *                 ", informe[1])
    print("\t\t\t Urnas:")
    print("\t\t\t Madera - Código 1:            ", informe[2])
    print("\t\t\t Fibra de vidrio - Código 2:   ", informe[3])
    print("\t\t\t Cristal/ Ceramica - Código 3: ", informe[4])
    print("\t\t\t Marmol - Código 4:            ", informe[5])
    print("\t\t\t Acero - Código 5:             ", informe[6])
    print("\t\t\t Bronce/ Cobre - Código 6:     ", informe[7])
    print("\n\t\t\t==================================")
    print("\n\t\t\t* Cementerio: *                ", informe[0])
    print("\t\t\t Caravanas:                    ", total_caravana)
    print("\t\t\t Autos Código 100:             ", informe[11])
    print("\t\t\t Autos Código 200:             ", informe[12])
    print("\t\t\t Autos Código 300:             ", informe[13])
    print("\t\t\t Féretros:")
    print("\t\t\t Básico - Código 1:            ", informe[14])
    print("\t\t\t Intermedio - Código 2:        ", informe[15])
    print("\t\t\t Superior - Código 3:          ", informe[16])
    print("\t\t\t Presidencial - Código 4:      ", informe[17])
    print("\n\t\t\t==================================")
    print("\n\t\t\t* Catering: *                  ", total_catering)
    print("\t\t\t Normal - Código 010:          ", informe[8])
    print("\t\t\t Intermedio - Código 020:      ", informe[9])
    print("\t\t\t Superior - Código 030:        ", informe[10])
    return informe
#Muestra la ficha del difunto (Puede interpretarse como un certificado de defuncion)
def ficha_difunto(servicios):
    nombre_buscar = input("\n\t\tIngrese el nombre o apellido del difunto: ").strip().lower()
    servicios_encontrados = [servicio for servicio in servicios.values() if nombre_buscar in servicio['nombre'].lower()]# Filtrar por nombre o apellido
    if not servicios_encontrados:
        print("\n\tNo se encontraron servicios para el nombre o apellido ingresado.")
        return
    for servicio in servicios_encontrados:
        input("\n\tPresione Enter para ver la ficha del difunto...")

        # Mostrar la ficha del difunto
        print("\n\t\t\t--- Ficha del Difunto ---")
        print("\n\t\t\tNombre:           " + servicio['nombre'])
        print("\n\t\t\tFecha Nacimiento: " + str(servicio['fecha_nacimiento'].strftime("%d/%m/%Y")))
        print("\n\t\t\tFecha Defunción:  " + str(servicio['fecha_defuncion'].strftime("%d/%m/%Y")))
        print("\n\t\t\tEdad:             " + str(servicio['edad']))
        print("\n\t\t\tFecha Servicio:   " + str(servicio['fecha_servicio'].strftime("%d/%m/%Y")))
        print("\n\t\t\tTipo de Servicio: " + str(servicio['funeral']))

#Facura servicios registrados
def factura_servicio(servicios, stock):
    def buscar_producto_por_codigo(stock_categoria, codigo):
        """Busca un producto en una categoría del stock por su código de forma manual."""
        for producto in stock[stock_categoria]:
            if producto[0] == codigo:
                return producto
        return ["No disponible", "Descripción no disponible", 0.0]

    id_servicio = input("Ingrese el Id del servicio a facturar: ").strip()
    try:
        id_servicio = int(id_servicio)
    except ValueError:
        print "Error: El ID del servicio debe ser un número entero."
        return

    if not (id_servicio in servicios):
        print "Error: No se pudo encontrar el servicio con ID " + str(id_servicio) + "."
        return

    servicio = servicios[id_servicio]
    subtotal = 0.0
    if "detalles" in servicio and len(servicio["detalles"]) > 0:
        subtotal = servicio["detalles"][-1]  # Suponiendo que el subtotal está al final de la lista
    impuestos = subtotal * 0.21
    total = subtotal + impuestos

    # Solicitar datos de facturación
    apenom_factura = raw_input("\nDATOS DE FACTURACION: Ingrese nombre y apellido o razón social: ").strip()
    id_factura = raw_input("DNI, CUIL o CUIT para la facturación: ").strip()
    try:
        id_factura = int(id_factura)
    except ValueError:
        print "Error: El DNI, CUIL o CUIT debe ser un número entero."
        return

    print "\n\t--- FACTURA ---"
    print "Empresa: L'Obito Servicios Funerarios"
    print "Fecha de Emisión: " + datetime.now().strftime("%d/%m/%Y")
    print "Número de Factura: " + str(id_servicio)
    print "\n--- Datos del Cliente ---"
    print "Nombre o Razón Social: " + apenom_factura
    print "DNI, CUIL o CUIT: " + str(id_factura)
    print "\n--- Detalles del Servicio ---"
    print "Nombre del Difunto: " + servicio.get("nombre", "Desconocido")
    print "Fecha de Nacimiento: " + servicio.get("fecha_nacimiento", "No disponible")
    print "Fecha del Servicio: " + servicio.get("fecha_servicio", "No disponible")
    print "Edad del Difunto: " + str(servicio.get("edad", "Desconocida"))

    funeral = servicio.get("funeral")
    if funeral == 1001:  # Cremación
        print "Tipo de funeral: Cremación"
        urna = buscar_producto_por_codigo("urnas", servicio["detalles"][0])
        catering = buscar_producto_por_codigo("catering", servicio["detalles"][1])
        print "Tipo de urna: cod: " + str(urna[0]) + " - " + urna[1] + " - costo: $" + str(urna[3])
        print "Tipo de catering: cod: " + str(catering[0]) + " - " + catering[1] + " - costo: $" + str(catering[3])
    elif funeral == 1002:  # Cementerio
        print "Tipo de funeral: Cementerio"
        feretro = buscar_producto_por_codigo("feretros", servicio["detalles"][0])
        auto = buscar_producto_por_codigo("autos", servicio["detalles"][1])
        catering = buscar_producto_por_codigo("catering", servicio["detalles"][2])
        destino = servicio["detalles"][3]
        print "Tipo de féretro: cod: " + str(feretro[0]) + " - " + feretro[1] + " - costo: $" + str(feretro[3])
        print "Tipo de caravana: cod: " + str(auto[0]) + " - " + auto[1] + " - costo: $" + str(auto[3])
        print "Tipo de catering: cod: " + str(catering[0]) + " - " + catering[1] + " - costo: $" + str(catering[3])
        print "Destino del féretro: " + destino

    print "\n--- Desglose de Costos ---"
    print "Subtotal: $" + str(subtotal)
    print "Impuestos (21%): $" + str(impuestos)
    print "Total a Pagar: $" + str(total)
    print "\n--- Fin de la Factura ---"
    raw_input("\nPresione Enter para volver al menú de reportes...")

    # Asegúrate de pasar todos los argumentos necesarios a guardar_datos
    servicios, estadistica, stock = obtener_datos()
    guardar_datos('archivo.dat', servicios, estadistica, stock)

#Lista las facturaciones de un periodo seleccionado por el usuario
def listar_facturaciones_por_rango(servicios):
    menu_listar_facturaciones = (
        "\n\t\t\t----Seleccione el intervalo ----", 
        "1. Diario", 
        "2. Semanal", 
        "3. Quincenal", 
        "4. Mensual", 
        "5. Trimestral", 
        "6. Semestral", 
        "7. Anual", 
        "8. Rango definido"
    )
    
    while True:
        for opcion in menu_listar_facturaciones:
            print(opcion)
        try:
            intervalo = raw_input("\nSeleccione una opción: ").strip()
            intervalo = int(intervalo)
            if intervalo == 8:
                fecha_inicio = raw_input("\nFecha de inicio (DD/MM/AAAA): ").strip()
                fecha_final = raw_input("\nFecha de fin (DD/MM/AAAA): ").strip()
                # Validación de fechas
                try:
                    fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%d/%m/%Y')
                    fecha_final = datetime.datetime.strptime(fecha_final, '%d/%m/%Y')
                    if fecha_inicio > fecha_final:
                        print "\nError: La fecha de inicio no puede ser mayor que la fecha final."
                        continue
                except ValueError:
                    print "\nError: Formato de fecha incorrecto. Use DD/MM/AAAA." 
                    continue
            elif 1 <= intervalo <= 7:
                fecha_inicio, fecha_final = calcular_intervalo(intervalo)

                if not fecha_inicio or not fecha_final:
                    print "\nError: No se pudo calcular el intervalo de fechas."
                    continue
            else:
                print "\nError: Opción no válida. Seleccione un número entre 1 y 8."
                continue
            # Filtrar facturas en el rango de fechas
            facturas_rango = [
                factura for factura in servicios.values()
                if "fecha" in factura and 
                fecha_inicio <= datetime.strptime(factura.get("fecha", ""), '%Y-%m-%d %H:%M:%S') <= fecha_final
            ]
            # SALIDA
            if facturas_rango:
                print("\n{:<12} {:<25} {:<20} {:>12}".format("ID", "Difunto", "Fecha", "Monto ($)"))
                print("=" * 75)
                for factura in facturas_rango:
                    id_factura = factura.get("dni", "Sin ID") # Usamos el DNI como identificador
                    cliente = factura.get("nombre", "Cliente no registrado") # No hay campo 'cliente'
                    fecha = factura.get("fecha", "Fecha no disponible")
                    # Extraer monto del servicio
                    monto = 0.0
                    if "detalles" in factura and isinstance(factura["detalles"], list):
                        try:
                            monto = float(factura["detalles"][-1]) # Último valor debería ser el total
                        except (IndexError, ValueError):
                            monto = 0.0 # Si hay error, asumimos monto cero
                    print("{:<12} {:<25} {:<20} {:>12,.2f}".format(id_factura, cliente, fecha, monto))
                print("=" * 75)
            else:
                print "\nNo se encontraron facturas en el rango de fechas especificado."
            return facturas_rango # Se retorna la lista de facturas para posible uso posterior
        except ValueError as error:
            print("\nError:", str(error))
            print "\nPor favor, seleccione una opción válida." 
    
    # Guardar los datos actualizados en el archivo .dat
    guardar_datos('archivo.dat', servicios, estadistica, stock)

#Sub Menú de gestión de servicios
def menu_gestion_servicios():
    servicios, estadistica, stock = obtener_datos()
    while True:
        print "\n\t\t\t---- Gestión de Servicios ----"
        print "\t\t\t1. Mostrar servicios pendientes"
        print "\t\t\t2. Mostrar servicios realizados"
        print "\t\t\t3. Listar todos los servicios"
        print "\t\t\t4. Estadísticas de servicios"
        print "\t\t\t5. Generar Factura"
        print "\t\t\t6. Ficha del difunto"
        print "\t\t\t7. Listar facturas por rango de fechas"
        print "\t\t\t8. Volver al menú principal"
        try:
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
                servicios_mas_contratados(estadistica)
            elif opcion == 5:
                cleaning()
                factura_servicio(servicios, stock)  # Modificación aquí
            elif opcion == 6:
                cleaning()
                ficha_difunto(servicios)
            elif opcion == 7:
                cleaning()
                listar_facturaciones_por_rango(servicios)
            elif opcion == 8:
                cleaning()
                print "\n\t\t\t\tSaliendo del menú de gestión de servicios..."
                break
            else:
                print "\n\t\t\t\tOpción no válida. Por favor, intente de nuevo."
            raw_input("\n\t\t\t\tPresione Enter para volver al menú...")
        except ValueError:
            print "\n\t\t\t\tEntrada inválida. Debe ingresar un número entero."

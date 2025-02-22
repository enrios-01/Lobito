# -*- coding: utf-8 -*-


import utils
import datetime
from carga import carga_servicios, estadistica
from stock import stock
from utils import cleaning
from tools import guardar_datos, obtener_datos

#Aloja los valores contabilizados por los contadores del diccionario estadistica
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
   
    # Print la estadística
    print u"\n\t\t\tReporte de Servicios Contratados:"
    print u"\n\t\t\tTotal de servicios realizados: ", total_servicios_realizados
    print u"\t\t\t== Cremación: {}==".format(informe[1])
    print u"\t\t\t Urnas:"
    print u"\t\t\t Madera - Código 1: {}".format(informe[2])
    print u"\t\t\t Fibra de vidrio - Código 2: {}".format(informe[3])
    print u"\t\t\t Cristal/ Ceramica - Código 3: {}".format(informe[4])
    print u"\t\t\t Marmol - Código 4: {}".format(informe[5])
    print u"\t\t\t Acero - Código 5: {}".format(informe[6])
    print u"\t\t\t Bronce/ Cobre - Código 6: {}".format(informe[7])
    print u"\t\t\t============================================="
    print u"\t\t\t== Cementerio: {} ==".format(informe[0])
    print u"\t\t\t Caravanas:", total_caravana
    print u"\t\t\t Autos Código 100: {}".format(informe[11])
    print u"\t\t\t Autos Código 200: {}".format(informe[12])
    print u"\t\t\t Autos Código 300: {}".format(informe[13])
    print u"\t\t\t Féretros:"
    print u"\t\t\t Básico - Código 1: {}".format(informe[14])
    print u"\t\t\t Intermedio - Código 2: {}".format(informe[15])
    print u"\t\t\t Superior - Código 3: {}".format(informe[16])
    print u"\t\t\t Presidencial - Código 4: {}".format(informe[17])
    print u"\t\t\t============================================="
    print u"\t\t\t Catering:", total_catering
    print u"\t\t\t Normal - Código 010: {}".format(informe[8])
    print u"\t\t\t Intermedio - Código 020: {}".format(informe[9])
    print u"\t\t\t Superior - Código 030: {}".format(informe[10])
    return informe

#Muestra la ficha del difunto (Puede interpretarse como un certificado de defuncion)
def ficha_difunto(servicios):
    nombre_buscar = raw_input("\n\t\t\ttIngrese el nombre o apellido del difunto: ").strip().lower()

    # Filtrar servicios por nombre o apellido
    servicios_encontrados = [servicio for servicio in servicios.values() if nombre_buscar in servicio['nombre'].lower()]

    if not servicios_encontrados:
        print "\n\tNo se encontraron servicios para el nombre o apellido ingresado."
        return

    for servicio in servicios_encontrados:
        raw_input("\n\tPresione Enter para ver la ficha del difunto...")

        # Mostrar la ficha del difunto
        print "\n\t--- Ficha del Difunto ---"
        print "\tDNI:              {}".format(servicio['dni'])
        print "\tNombre:           {}".format(servicio['nombre'])
        print "\tFecha Nacimiento: {}".format(servicio['fecha_nacimiento'])
        print "\tFecha Defunción:  {}".format(servicio['fecha_defuncion'])
        print "\tEdad:             {}".format(servicio['edad'])
        print "\tFecha Servicio:   {}".format(servicio['fecha_servicio'])
        print "\tTipo de Servicio: {}".format(servicio['funeral'])
        print "\tImporte del Servicio: ${:,.2f}".format('importe_factura')
        cleaning()

def factura_servicio(servicios):
    id_servicio = raw_input("Ingrese el Id del servicio a facturar: ").strip()
    # Intentar convertir el ID a entero
    try:
        id_servicio = int(id_servicio)
    except ValueError:
        print "Error: El ID del servicio debe ser un número entero."
        return
    # Verificar si el servicio existe en el diccionario
    if id_servicio not in servicios:
        print("Error: No se pudo encontrar el servicio con ID {}.".format(id_servicio))
        return
    servicio = servicios[id_servicio]  # Extraemos el servicio del diccionario
    
    # DEPURACIÓN: Mostrar el servicio cargado para verificar su contenido
    print("\n[INFO] Servicio encontrado con ID: {}".format(id_servicio))
    print(" Nombre del difunto: {}".format(servicio.get("nombre", "Desconocido")))
    print(" Fecha de servicio: {}".format(servicio.get("fecha_servicio", "No disponible")))
    print(" Detalles del servicio: {}".format(servicio.get("detalles", [])))
    nombre_difunto = servicio.get("nombre", "Desconocido")
    fecha_nacimiento = servicio.get("fecha_nacimiento", "Fecha no disponible")
    fecha_servicio = servicio.get("fecha_servicio", "Fecha no disponible")
    edad = servicio.get("edad", "Desconocida")
    detalles = servicio.get("detalles", [])
    
    # Solicitar datos de facturación
    apenom_factura = raw_input("\nDATOS DE FACTURACION: Ingrese nombre y apellido o razón social: ").strip()
    id_factura = raw_input("DNI, CUIL o CUIT para la facturación: ").strip()
    try:
        id_factura = int(id_factura)
    except ValueError:
        print "Error: El DNI, CUIL o CUIT debe ser un número entero." 
        return
    
    # CALCULAR COSTOS
    subtotal = 0.0
    if isinstance(detalles, list) and detalles:
        try:
            subtotal = float(detalles[-1])  # Último valor de la lista debería ser el total
        except (IndexError, ValueError):
            subtotal = 0.0  # Si hay error, asumimos $0.00
    impuestos = subtotal * 0.21  # 21% de IVA
    total = subtotal + impuestos
    
    # SALIDA ORDENADA
    print("\n\t--- FACTURA ---")
    print("Empresa: L'Obito Servicios Funerarios")
    print("Fecha de Emisión: {}".format(datetime.datetime.now().strftime("%d/%m/%Y")))
    print("Número de Factura: {}".format(id_servicio))
    print("\n--- Datos del Cliente ---")
    print("Nombre o Razón Social: {}".format(apenom_factura))
    print("DNI, CUIL o CUIT: {}".format(id_factura))
    print("\n--- Detalles del Servicio ---")
    print("Nombre del Difunto: {}".format(nombre_difunto))
    print("Fecha de Nacimiento: {}".format(fecha_nacimiento))
    print("Fecha del Servicio: {}".format(fecha_servicio))
    print("Edad del difunto: {}".format(edad))
    
    # Detalles adicionales del servicio según el tipo de funeral
    funeral = servicio.get("funeral")
    if funeral == 1001:  # Cremación
        print("Tipo de funeral: Cremación")
        urna_codigo = detalles[0] if len(detalles) > 0 else "No disponible"
        catering_codigo = detalles[1] if len(detalles) > 1 else "No disponible"
        urna = next((item for item in stock["urnas"] if item[0] == urna_codigo), ["No disponible", "Descripción no disponible", 0.0])
        catering = next((item for item in stock["catering"] if item[0] == catering_codigo), ["No disponible", "Descripción no disponible", 0.0])
        print("Tipo de urna: cod: {} - {} - costo: ${:,.2f}".format(
            urna[0], urna[1], urna[3]
        ))
        print("Tipo de catering: cod: {} - {} - costo: ${:,.2f}".format(
            catering[0], catering[1], catering[3]
        ))
    elif funeral == 1002:  # Cementerio
        print("Tipo de funeral: Cementerio")
        feretro_codigo = detalles[0] if len(detalles) > 0 else "No disponible"
        caravana_codigo = detalles[1] if len(detalles) > 1 else "No disponible"
        catering_codigo = detalles[2] if len(detalles) > 2 else "No disponible"
        destino = detalles[3] if len(detalles) > 3 else "No disponible"
        feretro = next((item for item in stock["feretros"] if item[0] == feretro_codigo), ["No disponible", "Descripción no disponible", 0.0])
        caravana = next((item for item in stock["autos"] if item[0] == caravana_codigo), ["No disponible", "Descripción no disponible", 0.0])
        catering = next((item for item in stock["catering"] if item[0] == catering_codigo), ["No disponible", "Descripción no disponible", 0.0])
        print("Tipo de feretro: cod: {} - {} - costo: ${:,.2f}".format(
            feretro[0], feretro[1], feretro[3]
        ))
        print("Tipo de caravana: cod: {} - {} - costo: ${:,.2f}".format(
            caravana[0], caravana[1], caravana[3]
        ))
        print("Tipo de catering: cod: {} - {} - costo: ${:,.2f}".format(
            catering[0], catering[1], catering[3]
        ))
        print("Destino del feretro: {}".format(destino))
    
    print("\n--- Desglose de Costos ---")
    if subtotal > 0:
        print("Subtotal: ${:,.2f}".format(subtotal))
        print("Impuestos (21%): ${:,.2f}".format(impuestos))
        print("Total a Pagar: ${:,.2f}".format(total))
    else:
        print "No se encontraron costos para este servicio."
    print("\n--- Fin de la Factura ---")
    raw_input("\nPresione Enter para volver al menú de reportes...")
    
    # Guardar los datos actualizados en el archivo .dat
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
                fecha_inicio, fecha_final = utils.calcular_intervalo(intervalo)
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
                fecha_inicio <= datetime.datetime.strptime(factura.get("fecha", ""), '%Y-%m-%d %H:%M:%S') <= fecha_final
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

# Submenú del módulo reportes.py
def generar_reportes():
    servicios, estadistica, stock = obtener_datos()
    
    while True:
        print "\n\t\t\t---- Gestión de Reportes ----"
        print "\t\t\t1. Estadísticas de servicios"
        print "\t\t\t2. Generar Factura"
        print "\t\t\t3. Ficha del difunto"
        print "\t\t\t4. Listar facturas por rango de fechas"
        print "\t\t\t5. Volver al menú principal"
        
        try:
            opcion = raw_input("\nSeleccione una opción: ")
            opcion = int(opcion)
            if opcion == 1:
                cleaning()
                servicios_mas_contratados(estadistica)
                raw_input("\nPresione Enter para volver al menú de reportes...")            
            elif opcion == 2:
                cleaning()
                factura_servicio(servicios)
                raw_input("\nPresione Enter para volver al menú de reportes...")
            elif opcion == 3:
                cleaning()
                ficha_difunto(servicios)
                raw_input("\nPresione Enter para volver al menú de reportes...")
            elif opcion == 4:
                cleaning()
                listar_facturaciones_por_rango(servicios)
                raw_input("\nPresione Enter para volver al menú de reportes...")
            elif opcion == 5:
                cleaning()
                print "Saliendo del menú Reportes..."
                break
            else:
                print "\nOpción no válida. Por favor, intente de nuevo."
        except ValueError:
            print "\nEntrada inválida. Debe ingresar un número entero."

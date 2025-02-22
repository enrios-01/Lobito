# -*- coding: utf-8 -*-


from utils import cleaning
from tools import guardar_datos, obtener_datos


# Diccionarios stock, contiene 4 listas: feretros, urnas, autos, catering.
# Código, descripción, cantidad, precio
stock = {
    "feretros": [
        [1, "Básico", 10, 1000.0],
        [2, "Intermedio", 5, 2000.0],
        [3, "Superior", 2, 3000.0],
        [4, "Presidencial", 1, 5000.0]
    ],
    "urnas": [
        [1, "Madera", 10, 500.0],
        [2, "Fibra de vidrio", 5, 1000.0],
        [3, "Cristal/Cerámica", 2, 1500.0],
        [4, "Mármol", 1, 2000.0],
        [5, "Acero", 3, 2500.0],
        [6, "Bronce/Cobre", 2, 3000.0]
    ],
    "autos": [
        [1, "2 autos", 5, 1000.0],
        [2, "3 autos", 3, 1500.0],
        [3, "5 autos", 1, 2000.0]
    ],
    "catering": [
        [10, "Normal (incluido)", 10, 500.0],
        [20, "Intermedio", 5, 1000.0],
        [30, "Superior", 2, 1500.0]
    ]
}

#Funcion que obtiene los precios del diccionario stock
def obtener_precio(tipo, codigo):
    # Asegurar que los datos vienen de archivo.dat
    servicios, estadistica, stock_actualizado = obtener_datos() # Función que lee el archivo
    if tipo not in stock_actualizado:
        print("Error: Tipo '{}' no encontrado en el stock.".format(tipo))
        return 0
    for item in stock_actualizado[tipo]: # datos del archivo
        if item[0] == codigo:
            return item[3] # Precio actualizado
    return 0 # Si no se encuentra, devuelve 0

#Muestra Todos los productos en stock    
def listar_productos():
    servicios, estadistica, stock = obtener_datos()  # Cargar los datos desde el archivo
    for categoria, productos in stock.items():
        print categoria + ":"
        print "{:<10} {:<30} {:<15} {:<10}".format("Código", "Descripción", "Cantidad", "Precio")
        print "-" * 70
        for producto in productos:
            print "{:<10} {:<30} {:<15} {:<10.2f}".format(producto[0], producto[1], producto[2], producto[3])
        print "-" * 70
    raw_input("\n\tPresione Enter para volver al menú.")

def modificar_producto(stock):
    servicios, estadistica, stock = obtener_datos()  # Cargar los datos desde el archivo .dat
    print "\n\tSeleccionar producto para modificar:"
    categoria = raw_input("\n\tIngrese la categoría (feretro = 1, urna = 2, auto = 3, catering = 4): ")
    categoria = int(categoria)
    if categoria == 1:
        productos = stock["feretros"]
    elif categoria == 2:
        productos = stock["urnas"]
    elif categoria == 3:
        productos = stock["autos"]
    elif categoria == 4:
        productos = stock["catering"]
    else:
        print "\n\tCategoría no válida."
        return
    codigo = raw_input("\n\tIngrese el código del producto a modificar o presione ENTER para retornar al menú: ")
    try:
        codigo = int(codigo)
        producto = next((p for p in productos if p[0] == codigo), None)
        if not producto:
            print("\n\tCódigo no encontrado.")
            return
    except ValueError:
        print("\n\tCódigo inválido.")
        return
    descripcion, cantidad, precio = producto[1], producto[2], producto[3]
    print("\n\tProducto encontrado: {}, Cantidad: {}, Precio: ${}".format(descripcion, cantidad, precio))
    nueva_cantidad = raw_input("\n\tIngrese la nueva cantidad: ")
    nuevo_precio = raw_input("\n\tIngrese el nuevo precio: ")
    try:
        nueva_cantidad = int(nueva_cantidad)
        nuevo_precio = float(nuevo_precio)
        producto[2] = nueva_cantidad
        producto[3] = nuevo_precio
        print("\n\tProducto {} modificado exitosamente.".format(codigo))
        # Guardar los datos actualizados en el archivo .dat
        guardar_datos('archivo.dat', servicios, estadistica, stock)
    except ValueError:
        print "\n\tValores inválidos."

# Función para agregar un nuevo producto
def agregar_producto(stock):
    servicios, estadistica, stock = obtener_datos()  # Cargar los datos desde el archivo .dat
    print "\n\tSeleccionar producto para agregar:"
    categoria = raw_input("\n\tIngrese la categoría (feretro, urna, auto, catering): ").lower()
    if categoria == "feretro":
        cleaning()
        productos = stock["feretros"]
    elif categoria == "urna":
        cleaning()
        productos = stock["urnas"]
    elif categoria == "auto":
        cleaning()
        productos = stock["autos"]
    elif categoria == "catering":
        cleaning()
        productos = stock["catering"]
    else:
        print "\n\tCategoría no válida."
        return
    descripcion = raw_input("\n\tIngrese la descripción del producto: ")
    cantidad = raw_input("\n\tIngrese la cantidad: ")
    precio = raw_input("\n\tIngrese el precio: ")
    try:
        cantidad = int(cantidad)
        precio = float(precio)
        codigo_nuevo = max(p[0] for p in productos) + 1  # Generar un nuevo código automáticamente
        productos.append([codigo_nuevo, descripcion, cantidad, precio])
        print("\n\tProducto agregado exitosamente con código {}.".format(codigo_nuevo))
        # Guardar los datos actualizados en el archivo .dat
        guardar_datos('archivo.dat', servicios, estadistica, stock)
    except ValueError:
        print "\n\tValores inválidos."

#Sub menu modulo stock
def menu_stock(stock):
    sub_menu_stock = ("\n\t---- Menú de Gestión de Stock ----", "\n\t1. Listar productos", "\n\t2. Modificar producto",
                      "\n\t3. Agregar producto", "\n\t4. Volver al menú principal")
    while True:
        for opcion in sub_menu_stock:
            print opcion
        opcion = raw_input("\n\tSeleccione una opción: ")
        try:
            opcion = int(opcion)
            if opcion == 1:
                cleaning()
                listar_productos()
                cleaning()
            elif opcion == 2:
                cleaning()
                modificar_producto(stock)
            elif opcion == 3:
                cleaning()
                agregar_producto()
            elif opcion == 4:
                break
            else:
                print "\n\tOpción no válida."
        except ValueError:
            print "\n\tOpción inválida. Por favor ingrese un número."

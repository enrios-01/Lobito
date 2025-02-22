# -*- coding: utf-8 -*-

from tools import guardar_datos, obtener_datos, cleaning

# Diccionarios stock, contiene 4 listas: feretros, urnas, autos, catering.
# Código, descripción, cantidad, precio
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

# Función que obtiene los precios del diccionario stock
def obtener_precio(tipo, codigo):
    servicios, estadistica, stock_actualizado = obtener_datos()
    if tipo not in stock_actualizado:
        print("Error: Tipo '{}' no encontrado en el stock.".format(tipo))
        return 0
    for item in stock_actualizado[tipo]:
        if item[0] == codigo:
            return item[3]
    return 0

# Muestra todos los productos en stock    
def listar_productos():
    servicios, estadistica, stock = obtener_datos()
    for categoria, productos in stock.items():
        print(categoria + ":")
        print("{:<10} {:<30} {:<15} {:<10}".format("Código", "Descripción", "Cantidad", "Precio"))
        print("-" * 70)
        for producto in productos:
            print("{:<10} {:<30} {:<15} {:<10.2f}".format(producto[0], producto[1], producto[2], producto[3]))
        print("-" * 70)
    input("\n\tPresione Enter para volver al menú.")

# Modifica productos cargados en stock
def modificar_producto(stock):
    servicios, estadistica, stock = obtener_datos()
    print("\n\tSeleccionar producto para modificar:")
    categoria = input("\n\tIngrese la categoría (feretro = 1, urna = 2, auto = 3, catering = 4): ")
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
        print("\n\tCategoría no válida.")
        return
    codigo = input("\n\tIngrese el código del producto a modificar o presione ENTER para retornar al menú: ")
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
    nueva_cantidad = input("\n\tIngrese la nueva cantidad: ")
    nuevo_precio = input("\n\tIngrese el nuevo precio: ")
    try:
        nueva_cantidad = int(nueva_cantidad)
        nuevo_precio = float(nuevo_precio)
        producto[2] = nueva_cantidad
        producto[3] = nuevo_precio
        print("\n\tProducto {} modificado exitosamente.".format(codigo))
        guardar_datos('archivo.dat', servicios, estadistica, stock)
    except ValueError:
        print("\n\tValores inválidos.")

# Submenú módulo stock
def menu_stock(stock):
    sub_menu_stock = (
        "\n\t---- Menú de Gestión de Stock ----",
        "\n\t1. Listar productos",
        "\n\t2. Modificar producto",
        "\n\t3. Volver al menú principal"
    )
    while True:
        for opcion in sub_menu_stock:
            print(opcion)
        opcion = input("\n\tSeleccione una opción: ")
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
                break
            else:
                print("\n\tOpción no válida.")
        except ValueError:
            print("\n\tOpción inválida. Por favor ingrese un número.")

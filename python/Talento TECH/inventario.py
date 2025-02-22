# -*- coding: utf-8 -*-


import os
from tabulate import tabulate

inventario = {}

def cleaning():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")

def mostrar_menu(menu_opciones):
    for opcion in menu_opciones:
        print(opcion)
    while True:
        try:
            opcion = input("\n\tSeleccione una opción: ")
            opcion = int(opcion)
            return opcion
        except ValueError:
            print("\n\tError: Debe ingresar un número válido.")


def agregar_producto():
    nombre = input("\n\tIngrese el nombre del producto: ")
    if nombre in inventario:
        print("\n\tProducto ya listado en el stock, acceda a la opción 5 del menú principal para modificar cantidades.")
        return

    cantidad = input("\n\tIngrese la cantidad del producto: ")
    cantidad = int(cantidad)
    costo_unit = input("\n\tIngrese el costo unitario del producto: ")
    costo_unit = int(costo_unit)

    costo_total = costo_unit * cantidad
    inventario[nombre] = {
        "cantidad": cantidad,
        "costo_unit": costo_unit,
        "costo_total": costo_total
    }

    print("\n\t¡Operación exitosa!")
    print("\n\tEl producto: {}, Cantidad: {}, Costo Unitario: ${}, Costo Total: ${}".format(nombre, cantidad, costo_unit, costo_total))
    print("\n\tse encuentra registrado en el inventario.")

def mostrar_inventario():
    if not inventario:
        print("\n\t\tNo hay productos en el inventario.")
    else:
        print("\n\t\t\t\t---- Inventario ----")
        tabla = [[nombre, datos["cantidad"], datos["costo_unit"], datos["costo_total"]] for nombre, datos in inventario.items()]
        tabla_str = tabulate(tabla, headers=["Nombre", "Cantidad", "Costo Unitario", "Costo Total"], tablefmt="grid")

        print(tabla_str)
        print("\n\t\t\t\t--Final del listado--")

def modificar_producto():
    nombre = input("\n\tIngrese el nombre del producto a modificar: ")
    if nombre in inventario:
        nuevo_nombre = input("\n\tIngrese el nuevo nombre del producto (o presione Enter para mantener el actual): ")
        if not nuevo_nombre:
            nuevo_nombre = nombre

        cantidad = input("\n\tIngrese la nueva cantidad del producto (o presione Enter para mantener la actual): ")
        if not cantidad:
            cantidad = inventario[nombre]["cantidad"]
        else:
            cantidad = int(cantidad)

        costo_unit = input("\n\tIngrese el nuevo costo unitario del producto (o presione Enter para mantener el actual): ")
        if not costo_unit:
            costo_unit = inventario[nombre]["costo_unit"]
        else:
            costo_unit = int(costo_unit)

        costo_total = costo_unit * cantidad

        inventario.pop(nombre)
        inventario[nuevo_nombre] = {
            "cantidad": cantidad,
            "costo_unit": costo_unit,
            "costo_total": costo_total
        }

        print("\n\tProducto modificado exitosamente.")
        print("\n\tEl producto: {}, Cantidad: {}, Costo Unitario: ${}, Costo Total: ${}".format(nuevo_nombre, cantidad, costo_unit, costo_total))
    else:
        print("\n\tEl producto no se encuentra en el inventario.")

def eliminar_producto():
    nombre = input("\n\tIngrese el nombre del producto a eliminar: ")
    if nombre in inventario:
        inventario.pop(nombre)
        print("\n\tProducto eliminado exitosamente.")
    else:
        print("\n\tEl producto no se encuentra en el inventario.")

def control_de_stock():
    stock_minimo = input("\n\tIngrese la cantidad mínima para considerar stock bajo: ")
    if not stock_minimo.isdigit():
        print("\n\tError: La cantidad debe ser un número.")
        return
    stock_minimo = int(stock_minimo)

    stock_bajo = {nombre: datos for nombre, datos in inventario.items() if datos["cantidad"] < stock_minimo}

    if not stock_bajo:
        print("\n\tNo hay productos con stock bajo.")
    else:
        print("\n\t\t\t\t---- Productos con Stock Bajo ----")
        tabla = [[nombre, datos["cantidad"], datos["costo_unit"], datos["costo_total"]] for nombre, datos in stock_bajo.items()]
        tabla_str = tabulate(tabla, headers=["Nombre", "Cantidad", "Costo Unitario", "Costo Total"], tablefmt="grid")

        print(tabla_str)
        print("\n\t\t\t\t--Final del listado--")

def ventas():
    nombre = input("\n\tIngrese el nombre del producto a vender: ")
    cantidad_vender = input("\n\tIngrese la cantidad a vender: ")
    if not cantidad_vender.isdigit():
        print("\n\tError: La cantidad debe ser un número.")
        return
    cantidad_vender = int(cantidad_vender)

    if nombre in inventario:
        cantidad_disponible = inventario[nombre]["cantidad"]
        if cantidad_vender <= cantidad_disponible:
            nueva_cantidad = cantidad_disponible - cantidad_vender
            inventario[nombre]["cantidad"] = nueva_cantidad
            inventario[nombre]["costo_total"] = nueva_cantidad * inventario[nombre]["costo_unit"]

            print("\n\t¡Venta realizada con éxito!")
            print("\n\tProducto: {}, Cantidad Vendida: {}, Stock Restante: {}".format(
                nombre, cantidad_vender, nueva_cantidad))
        else:
            print("\n\tError: Stock insuficiente. Cantidad disponible: {}".format(cantidad_disponible))
    else:
        print("\n\tError: El producto no está registrado en el inventario.")

menu_opciones = ("\n\t---- Menú de Gestión de Inventario ----", "\n\t1. Control de Stock", "\n\t2. VENTAS",
                 "\n\t3. Listar productos del inventario", "\n\t4. Agregar producto al inventario",
                 "\n\t5. Modificar producto del inventario","\n\t6. Eliminar producto del inventario" , "\n\t7. Salir")

while True:
    cleaning()
    opcion = mostrar_menu(menu_opciones)

    if opcion == 1:
        cleaning()
        control_de_stock()
    elif opcion == 2:
        cleaning()
        ventas()
    elif opcion == 3:
        cleaning()
        mostrar_inventario()
    elif opcion == 4:
        cleaning()
        agregar_producto()
    elif opcion == 5:
        cleaning()
        modificar_producto()
    elif opcion == 6:
        cleaning()
        eliminar_producto()
    elif opcion == 7:
        cleaning()
        print("\n\tSaliendo del sistema. ¡Adiós, vuelva pronto!")
        break
    else:
        print("\n\tOpción no válida. Por favor, intente de nuevo.")

    input("\n\tPresione Enter para continuar...")


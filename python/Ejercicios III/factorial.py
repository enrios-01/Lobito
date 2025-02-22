# -*- coding: utf-8 -*- 


numero = input("Ingrese un número: ")
numero = int(numero)

factorial = 1
contador = numero

while contador > 0:
    factorial *= contador
    contador -= 1

print ("El factorial de"), numero, "es", factorial

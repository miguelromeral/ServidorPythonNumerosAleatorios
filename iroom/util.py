#!/usr/bin/python
# -­*-­ coding: utf-­8 -­*-­

# Imprime con formato de error un mensaje
def print_error(string):
	print '\033[1;41m%s\033[1;m' % string


# Imprime con formato de éxito un mensaje
def print_success(string):
	print '\033[1;42m%s\033[1;m' % string


# Suma los elementos de una lista
def suma_lista(lista):
	suma = 0
	for i in lista:
		suma += i
	return suma


# Filtra los números de una tupla que sean menores que el umbral (num)
def comprueba_menores_que(tupla_original, num):
	filtrada = []
	for el in tupla_original:
		if(float(el[0]) < float(num)):
			filtrada.append(el)
	return filtrada

# Código HTML para introducir el botón de vuelta a la página principal
boton_menu = "<form><input type=\"submit\" value=\"VOLVER AL MENÚ PRINCIPAL\" name=\"b_back_main_menu\" action=\"main.html\"></form>"

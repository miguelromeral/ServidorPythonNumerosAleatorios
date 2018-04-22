#!/usr/bin/python
# -­*-­ coding: utf-­8 -­*-­
from flask import *
import threading
import atexit
import time
import urllib2
import re
import random
from decimal import *
from modelo import *
from util import *

# Solicita un número al azar a la web.
def get_numero():
	# URL de la web
	url = 'http://www.numeroalazar.com.ar/'
	try:
		response = urllib2.urlopen(url)	#	Solicitamos la página	
		hora = time.ctime(time.time()) # Recogemos la hora actual
		html = response.read() #Leemos el contenido (codigo html)
		response.close() #Cerramos la solicitud.
		#Selecciono unicamente los numeros que se han generado (que acaban todos con <br>
		lista_numeros = re.findall("\d+\.\d+<", html)
		#Si existe al menos un numero...		
		if lista_numeros:
			random.shuffle(lista_numeros) # Los mezclamos (más aleatorio)
			num_aux = lista_numeros[0] # Cogemos el primero
			leng = len(num_aux) # Eliminamos el caracter "<" de <br>
			numero = num_aux[:leng - 1]
			insertar(numero, hora) # Inserta en la BD el numero obtenido.
			return numero
		else:
			print_error("ERROR: No he encontrado ningun numero")
			#Se retorna 'None' indicando que no hubo numero aleatorio.
			return 'None'
	except urllib2.URLError:
		#Si no se ha podido establecer conexión con la url.
		print_error('ERROR: Ha ocurrido un error al intentar solicitar la página %s.' % url)
		return 'None'


# Se accede a las gráficas que ThingSpeak proporciona
def ver_graficas():
	try:
		# Solicitamos la web de la gráfica
		response = urllib2.urlopen('https://thingspeak.com/channels/384828/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=20&type=line&update=1')
		# Leemos el html
		html = response.read()
		# Cerramos la solicitud
		response.close()
		# Añadimos el botón de vuelta al menú principal
		leng = len(html)
		nuevohtml = html[:leng - 8]
		return nuevohtml + "<br><br><br><br><br><br><br><br><br><br><br><br><br><br>    " + boton_menu + "</html>"
 	except urllib2.URLError:
		# En caso de error con la solicitud, se devuelve la web de error.	
		print_error('ERROR: No se ha podido contactar con la base de datos externa')
		return render_template('error.html')


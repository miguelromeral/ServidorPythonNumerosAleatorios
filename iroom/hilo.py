#!/usr/bin/python
# -­*-­ coding: utf-­8 -­*-­
from util import *
from web_interface import *
import threading
import time

# Hilo que se encarga cada 2 minutos de obtener un nuevo número.
class hilo_consultor (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		# Comienza a solicitar números aleatorios
		print "En ejecución el hilo consultor."
		bucle_solicitar_numeros()

# Función que, dependiendo de la ejecución del programa principal, solicita números.
def bucle_solicitar_numeros():
	# Lock que comprueba si debe continuar solicitando numeros o no.
	threadLock.acquire()
	tmp = continuar
	threadLock.release()
	# Si se puede, se pide un número y espera 2 minutos.
	if tmp:
		get_numero()
		time.sleep(120)
		return bucle_solicitar_numeros()	
	else:
		return False

# Cierra el hilo poniendo una variable a falso.
def cerrar_hilo():
	threadLock.acquire()
	continuar = False
	print("Se ha solicitado la parada del hilo consultor.")
	threadLock.release()

continuar = True
threadLock = threading.Lock()

# Función que crea el hilo.
def crear_hilo():
	thread = hilo_consultor()
	thread.daemon = True
	thread.start()



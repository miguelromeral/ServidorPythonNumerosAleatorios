#!/usr/bin/python
# -­*-­ coding: utf-­8 -­*-­
from pymongo import *
import random
import datetime, json, time
from datetime import datetime
import httplib, urllib, urllib2
from pprint import pprint
from util import *

# Inicialización de variables al arrancar la app.
try:

	# Base de datos local (MongoDB)

	#Nos conectamos como cliente a localhost puerto 27017
	url_conex = 'mongodb://localhost:27017/'
	client = MongoClient(url_conex)
	#Obtenemos la base de datos con nombre 'dblocal'
	db_name = 'dblocal'
	db = client[db_name]
	#obtenemos la coleccion (o tabla) de la BD local
	col = db.numeros
	print 'Abierta la conexion con la base de datos \"%s" de %s.' % (db_name, url_conex)
	# Registramos aquí el nombre de las columnas de la BD.
	columnas = ["numero","fecha"]
	
	# Base de datos externa (ThingSpeak)

	#Obtenemos las claves que proporciona ThingSpeak para escribir y leer en la BD respectivamente.
	key = 'JEAZQU3SQR42RBQ6'
	r_key = 'EUJRTPSUBTIS79KB'
	# Identificador del repositorio en el que está la BD.
	ch_id = '384828'
	# Abrimos la conexión con la API de ThingSpeak
	conn_ts = httplib.HTTPConnection("api.thingspeak.com:80")
	print 'Abierta la conexión con la base de datos de ThingSpeak'
except:
	# En caso de error al abrirlas, se cierran ambas por seguridad.
	print_error('ERROR al inicializar las bases de datos.')
	cerrar_conexion()




# Cierra la conexión con las dos bases de datos si es que estában activas.
def cerrar_conexion():
	if client:
		client.close()
		print 'Cerrada la conexion con %s' % url_conex
	if conn_ts:	
		conn_ts.close()
		print 'Cerrada la conexión con ThingSpeak'



# ---------------------------------------------------
# -- CONSULTA TUPLAS EN BASES DE DATOS
# ---------------------------------------------------

# Retorna todos los registros de la BD externa
def get_tuplas_numero_fecha_externa():
	try:
		# Obtenemos el documento con todos los registros.
		c = urllib2.urlopen("https://api.thingspeak.com/channels/%s/feeds.json?results=1000000" % ch_id)
		# Recogemos el contenido del documento.
		response = c.read()
		# Decodificamos el JSON obtenido
		data=json.loads(response)
		# Por cada documento dentro del JSON, se almacena en una lista de tuplas
		lista = []
		for e in data['feeds']:
			numero = e['field1']
			fecha = e['created_at']
			lista.append([float(numero), fecha])
		# Cerramos la conexión
		c.close()
		return lista
	except:
		# En caso de que algo fuese mal, se retorna una lista vacía
		print_error("ERROR: no se ha podido consultar la BD externa.")
		return []		


# Retorna todos los registros de la BD local
def get_tuplas_numero_fecha_local():
	try:
		# Obtenemos todos los documentos de la BD.
		cursor = col.find({},{columnas[1]:1, columnas[0]:1, "_id":0})
		# Para cada documento, añadimos en una tupla el número y fecha y se añade a una lista
		lista = []
		for i in cursor:
			numero = i[columnas[0]]
			fecha = i[columnas[1]]
			# La fecha viene sin formatear, por lo que debemos darla formato ahora (para que sea más legible)
			estructura_fecha = time.strptime(fecha, '%a %b %d %H:%M:%S %Y')
			fecha_str = '%s/%s/%s - %s:%s:%s' % (
				estructura_fecha[2], # Dia
				estructura_fecha[1], # Mes
				estructura_fecha[0], # Año
				estructura_fecha[3], # Hora
				estructura_fecha[4], # Mins
				estructura_fecha[5] # Segs
			)
			lista.append([float(numero), fecha_str])
		return lista
	except:
		# En caso de que algo fuese mal, se retorna una lista vacía
		print_error("ERROR: no se ha podido consultar la BD local.")
		return []	

# ---------------------------------------------------
# -- INSERCIONES EN LAS BASES DE DATOS
# ---------------------------------------------------

# Inserta registros (o documentos) en la BD externa.
def insertar_thingspeak(num, fec):
	# Introducimos los valores en un documento JSON y lo codificamos
	params = urllib.urlencode(
		{
			'field1': num, #numero
			'field2': fec, #fecha
			'key':key
		})
	# Añadimos las cabeceras a la solicitud POST que haremos a la API
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	try:
		# Realizamos una conexión POST para registrar los valores en la BD
		conn_ts.request("POST", "/update", params, headers)
		# Recogeos la respuesta.
		response = conn_ts.getresponse()
		# Obtenemos el ID de la inserción		
		data = response.read()
		# Si el ID es 0, resulta que no pudo añadirse (debemos esperar entre 10 - 15 segundos para insertar un nuevo registro.
		if (int(data)!=0):
			print_success("Insertado a la BD EXTERNA el número %s (%s)" % (num,fec))
		else:
			print_error("ERROR: no se pudo registrar %s en la BD externa" % num)
	except:
		print_error("ERROR: no se pudo registrar %s en la BD externa" % num)


# Inserta registros en la BD local
def insertar_mongo(num, fec):
	try: 
		# Añadimos los valores a las columnas
		post = {
			columnas[0]: num,
			columnas[1]: fec
		}
		# Insertamos en la BD el registro.
		result = col.insert_one(post)
		print_success("Insertado a la BD LOCAL el número %s (%s)" % (num,fec))
	except:
		print_error("ERROR: no se pudo registrar %s en la BD local" % num)


# Realiza la inserción del mismo registro en ambas bases de datos.
def insertar(num, fec):
	insertar_mongo(num, fec)
	insertar_thingspeak(num, fec)


# ---------------------------------------------------
# -- OBTIENE EL ÚLTIMO NÚMERO DE LA BD INT O EXT
# ---------------------------------------------------

def get_last():
	try:
		# De manear aleatoria, obtiene las listas de una base de datos u otra.
		aleatorio = random.random()
		lista = []
		if(aleatorio < 0.5):
			lista = get_numeros_bd_local()
		else:
			lista = get_numeros_bd_externa()
		# Cogemos únicamente el último número de la lista.
		lon = len(lista)
		return lista[(lon - 1)]
	except:
		return 'None'
	

# ---------------------------------------------------
# -- OBTIENE LA LISTA DE NUMEROS
# ---------------------------------------------------

# Obtiene una lista con todos los números de la BD externa
def get_numeros_bd_externa():
	try:
		# Abrimos la conexión y obtenemos todos los registros
		c = urllib2.urlopen("https://api.thingspeak.com/channels/%s/feeds.json?results=10000000" % ch_id)
		# Leemos la página
		response = c.read()
		# Obtenemos todos los documentos de la respuesta
		data=json.loads(response)
		# Por cada documento, obtenemos únicamente los números
		lista = []
		for e in data['feeds']:
			numero = e['field1']		
			lista.append(float(numero))
		c.close()
		return lista
	except:
		# En caso de que algo fuese mal, se retorna una lista vacía
		print_error("ERROR: no se ha podido consultar la BD externa.")
		return []	
		
# Obtiene una lista ocn todos los números de la BD local
def get_numeros_bd_local():
	try:
		# Conseguimos todos los registros.
		cursor = col.find({},{columnas[1]:1, columnas[0]:1, "_id":0})
		# Por cada registro, añadimos a la lista solo los numeros
		lista = []
		for i in cursor:
			numero = i[columnas[0]]
			lista.append(float(numero))
		return lista
	except:
		# En caso de que algo fuese mal, se retorna una lista vacía
		print_error("ERROR: no se ha podido consultar la BD local.")
		return []	


#!/usr/bin/python
# -­*-­ coding: utf-­8 -­*-­
from flask import *
import threading
import atexit
import time
#importamos los demás módulos de la aplicación.
from web_interface import *
from modelo import *
from util import *
from hilo import *

#indicamos que las webs están en la carpeta "static". 
app = Flask(__name__, template_folder = "static")

# ******************************************************
# **			GET /
# ******************************************************

@app.route('/', methods=['GET'])
def main_get():
	#n_random = get_numero() #Se obtiene un número aleatorio
	n_random = get_last()
	if(n_random == "None"): #Si no pudo encontrarse ninguno...
		return render_template('error.html') #devuelve una web de error.
	else:
		#Sino, devuelve la web principal con el número obtenido.
		return render_template('main.html', random=n_random)


# ******************************************************
# **			POST / (Se pulsa un botón del formulario)
# ******************************************************

@app.route('/', methods=['POST'])
def main_post():
	#Obtenemos la elección del usuario (qué botón ha pulsado):
	opcion = request.form['b_choice']

	# --------------------------------
	#	--	Ir a ver el UMBRAL
	# --------------------------------

	if opcion == 'UMBRAL':
		try:
			# Cogemos el umbral seleccionado.
			numero = request.form['umbral']
			# Si no es un número entre 0 y 100, se retorna un error.
			if (0 <= float(numero) <= 100):

				#Base de datos local

				# Cogemos todas las tuplas (numero,fecha) de la BD local
				tuplas = get_tuplas_numero_fecha_local()
				# Obtenemos la cantidad total de numeros de la BD local			
				total_numeros = len(tuplas)
				# Filtramos las tuplas menores que el umbral.
				tuplas_filtradas = comprueba_menores_que(tuplas,numero)
				# Seleccionamos la última tupla de todas (se muestra primero)			
				ultima_tupla_local = tuplas_filtradas[len(tuplas_filtradas) - 1]
			
				#Base de datos externa

			
				# Cogemos todas las tuplas (numero,fecha) de la BD externa			
				tup_ex = get_tuplas_numero_fecha_externa()
				# Obtenemos la cantidad total de numeros de la BD externa (ThingSpeak)
				tne = len(tup_ex)
				# Filtramos las tuplas menores que el umbral
				tup_fil_ex = comprueba_menores_que(tup_ex,numero)
				# Seleccionamos la última tupla de todas (se muestra primero)
				ultima_tupla_externa = ()			
				if(tne != 0):
					ultima_tupla_externa = tup_fil_ex[len(tup_fil_ex) - 1]
	
				# Devolvemos la página con todas las variables inicializadas.
				return render_template('view_umbral.html',
					umbral=numero,
					# BD local
					total_num=len(tuplas_filtradas),
					total=total_numeros,
					lista=tuplas_filtradas,
					utl = ultima_tupla_local,
					# BD externa
					total_num_ex=len(tup_fil_ex),
					total_ex=tne,
					lista_ex=tup_fil_ex,
					ute = ultima_tupla_externa)
			else:
				# Página de error si algo sale mal
				return render_template('error.html')
		except:
				return render_template('error.html')

	# --------------------------------
	#	--	Ir a ver la MEDIA
	# --------------------------------

	elif opcion == 'MEDIA':

		# Base de datos local

		
		# Lista todos los números (sin la fecha)
		lista_local = get_numeros_bd_local()
		# Número total de registros en la BD local.
		total_local = len(lista_local)
		# Calculamos la suma de todos los elementos de la lista
		suma_local = suma_lista(lista_local)
		# La media por defecto es NaN (Not a Number)
		media_externa = "NaN"
		# La media solo cambia si existe al menos un registro en la BD
		if(total_local != 0):
			media_local = suma_local / total_local

		# Base de datos externa:

		
		# Lista todos los números (sin la fecha)
		lista_externa = get_numeros_bd_externa()
		# Número total de registros en la BD externa
		total_externa = len(lista_externa)
		# Sumamos todos los números de la lista
		suma_externa = suma_lista(lista_externa)
		# La media por defecto es NaN (Not a Number)
		media_externa = "NaN"
		# La media solo acmbia si existe al menos un registro en la BD
		if(total_externa != 0):
			media_externa = suma_externa / total_externa

		# Devolvemos la página con todas las variables inicializadas.
		return render_template('media.html',
			#Base Datos Local:
			tnl=total_local,
			ll=lista_local,
			sl=suma_local,
			ml=media_local,
			#Base Datos Externa:
			tne=total_externa,
			le=lista_externa,
			se=suma_externa,
			me=media_externa)

	# --------------------------------
	#	--	Ir a ver las GRAFICAS
	# --------------------------------

	elif opcion == 'GRAFICAS':
		# Devuelve una página con las gráficas de los números de la base de datos externa
		return ver_graficas()

	# En caso de errores
	else:
		# Avisamos en la terminal y devolvemos la página de error.
		print_error('ERROR: No se ha introducido ninguna solicitud')
		return render_template('error.html')


# Al terminar la ejecución de la aplicación
@atexit.register
def salir():
	# Cerramos de manera segura las conexiones con las bases de datos.
	print ''
	cerrar_hilo()
	cerrar_conexion()


# main de la aplicación, escucha a cualquier hot.
if __name__ == "__main__":
	crear_hilo()
	app.run(host='0.0.0.0')

	



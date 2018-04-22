# Servidor en Python para obtener números aleatorios

## Introducción

Aplicación con Flask para tener un servidor web que vaya recogiendo números aleatorios cada 2 minutos mediante peticiones URL y las almacene en dos bases de datos, una local (con MongoDB) y otra remota (ThingSpeak). Además, si se realizan peticiones, mostrará una interfaz web en la que se pueden observar los datos de manera amigable, obteniendo gráficas, rangos o incluso la media de los números.

## Motivación

Esta aplicación web fue desarrollada para la asignatura Tecnología y Servicios de Red de la Universidad de Alcalá. Cumple con la funcionalidad requerida, la memoria fue aprobada y la aplicación defendida con éxito.

## Instalación

Para poder hacer uso de la misma será necesario tener instalado Python junto al módulo Flask, MongoDB y haber creado una cuenta en ThingSpeak con una base de datos remota. Tras ello, iniciar la aplicación tal y como se describe en la memoria.

## Funcionalidades

* Obtención de números aleatorios cada 2 minutos en el servidor realizando peticiones al URL www.numeroalazar.com.ar.

* Observar valores por debajo de un cierto umbral.

* Obtener la media de los números en ambas bases de datos.

* Registro de números en la base de datos mediante interfaz web.

* Gráficas gracias a la API de ThingSpeak.

## Pruebas

Puesto que se trata de una práctica que tuvo que ser entregada, se realizaron bastantes pruebas para comprobar que la inserción de los números resultaba correcta, así como el servidor fuera capaz de lidiar con las peticiones que recibiese y el tratamiento de cada una de ellas, mandando la web oportuna y realizando sus funciones (obtener el número aleatorio) en su debido tiempo.

## Contacto

Correo electrónico: miguelangel.garciar@edu.uah.es, miguel.romeral@gmail.com

LinkedIn: Miguel Romeral (https://www.linkedin.com/in/miguelromeral/)

Twitter: @MiguelRomeral (https://twitter.com/MiguelRomeral)

## Licencia

Licencia Pública General GNU 3.0

# Repositorio Backend Grupo Peluche

Backend para la implementacion del juego misterio, desarrollado para la catedra Ingenieria del software I 
de la Facultad de Matemática, Astronomía, Física y Computación de la Universidad Nacional de Córdoba.  
Desarrollado en python con ayuda de las librerias de pony.orm y FastAPI.

## Instalar el entorno virtual

* Crear un entorno nuevo con `virtualenv`

       virtualenv env

* Activar el entorno virtual

       source env/bin/activate

* Instalar las dependencias

       pip install -r requirements.txt


## Iniciar servidor

* Para activar el entorno virtual

       source env/bin/activate

* Para iniciar el servidor de manera local utilizar el programa uvicorn con el siguiente comando:

       uvicorn main:app --reload

* Para probar que funciona el servidor podemos ejecutar el siguiente comando:

       curl -X GET "http://localhost:8000/home" -H "accept: aplication/json" -w "\n"

Esperando como resultado {"message" : "Project home Grupo Peluche"}

## Testeo

* Para correr los test utilizar el comando:

       py.test -s test_main.py --disable-warnings
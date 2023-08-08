Lemo Miniblog en Flask
======================
A miniblog/twitter clone made in Python using Flask and SQLAlchemy.

## Conocimientos
 - Flask
 - SQLAlchemy
 - Bootstrap
 - Python
 - HTML

## Capturas

<img src="https://i.ibb.co/wsFttrx/miniblog-muro.png" alt="miniblog-muro" border="0">

----

<img src="https://i.ibb.co/B4cSyH9/miniblog-filter1.png" alt="miniblog-filter1" border="0">

----

<img src="https://i.ibb.co/Tq9jw6H/miniblog-user.png" alt="miniblog-user" border="0">

----

<img src="https://i.ibb.co/DWbc0b1/miniblog-edit.png" alt="miniblog-edit" border="0">

## Set-Up

Para correr este projecto, se necesita una versión actualizada de python funcionar y [Xampp](https://www.apachefriends.org/es/index.html) para simular la base de datos de manera local. Se deben seguir los siguientes pasos:

Primero debemos clonar el repositorio de manera local.
Una vez lo tenemos, debemos crearle un entorno virtual con python e instalarle los requerimientos provistos, que incluyen Flask y SQLAlchemy, entre otros.
Creamos el entorno virtual con el siguiente comando:
```bash
  python3 -m venv venv
```
Ahora debemos ingresar dentro del entorno para instalarle los requerimientos. 
Si estamos en LINUX, lo hacemos con el siguiente comando:
```bash
  source venv/bin/activate
```
En cambio, en WINDOWS es de la siguiente manera:
```bash
   venv/Scripts/activate
```
Una vez activado el entorno virtual, le vamos a instalar los requerimientos con el siguiente comando:
```bash
  pip install -r requirements.txt
```
---
Ahora, sin cerrar la terminal, abriremos [Xampp](https://www.apachefriends.org/es/index.html) e iniciaremos sus servicios.
En windows puede ser abierto su acceso directo, pero en linux debemos ingresar el siguiente comando:
```bash
  sudo /opt/lampp/manager-linux-x64.run
```
Una vez abierto, y con sus servicios inicializados, queda crear e iniciar la base de datos.
Ingresaremos al módulo de [base de datos de Xampp](http://localhost/phpmyadmin/index.php?route=/server/databases) y la creamos con el siguiente nombre:
```bash
  lemo_miniblog
```
de tener otro nombre la aplicación NO FUNCIONARÁ.
Para iniciarla, volveremos a la terminal donde tenemos activado el entorno virtual e iniciamos la base de datos:
```bash
  flask db init
```
---

y finalmente, corremos el proyecto con un:
```bash
  flask run
```
y accedemos a [localhost:5000](http://localhost:5000/). Con eso, estás listo para disfrutar el miniblog!


## Autor
Hecho con mucho cariño por [@Facundo Lemo](https://github.com/FacundoEsteban-Lemo).


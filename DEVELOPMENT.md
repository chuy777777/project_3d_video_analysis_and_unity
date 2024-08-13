# Project 3d video analysis and unity 

## Versiones de herramientas utilizadas:
- ***git: 2.25.1***
- ***pip: 24.2***
- ***python: 3.8.10***
- ***Unity***
    - ***Unity Hub: 3.8.0***
    - ***Editor: 2020.3.7f1***

## Temas
***
### Aplicacion 
![app](./project/app/public/images/app.png)

***
### Organizacion 
- `project/app`
    - Aplicacion local
- `project/app_docker`
    - Aplicacion encapsulada con Docker

Script para automatizar todo el proceso de lanzamiento de servicios Docker-Compose: 
- `project/app.sh`
    - Para el lanzamiento de  servicios en:
        - `app_docker`

Archivo `.dockerignore` para ignorar archivos y directorios, ya que el directorio de contexto para la construccion de imagenes es `project/`. 

***
### Nombre de la plantilla
El nombre de la plantilla se encuentra en los siguientes archivos (por si se desea modificar el nombre):
- `project/app.sh`
- `project/app_docker/docker-compose.yaml`

***
### `project/app`
### ***Entorno virtual Python***
Instalar paquetes necesarios de Python:
- Instalar python:
    - `sudo apt install python3.8`
- Instalar paquete venv (para crear entornos virtuales):
    - `sudo apt install python3.8-venv`

Comandos entorno virtual:
- Crear entorno virtual:
    - `python3.8 -m venv app_env`
- Activar entorno virtual:
    - `source app_env/bin/activate`
- Desactivar entorno virtual:
    - `deactivate`
- Eliminar entorno virtual:
    - `rm -rf app_env`
- Instalar dependencias a partir del archivo requirements.txt:
    - `pip install -r ../app_docker/requirements.txt`

Una vez activado el entorno virtual, la aplicacion se ejecuta con el siguiente comando:
- `python3.8 app.py`

### ***Variables de entorno***
En esta carpeta debe existir un archivo `.env` con la siguiente estructura:
```
APP_HOST=0.0.0.0
APP_PORT=5000
```

***
### `project/app_docker`
### ***Archivo de dependencias de la aplicacion***
Crear archivo de dependencias del entorno virtual:
> Es importante tener activado el entorno virtual y estar situados en el directorio `project/app`.

> Este archivo es necesario a la hora de construir la imagen Docker de la aplicacion.

- `pip freeze > ../app_docker/requirements.txt`








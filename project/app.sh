#!/bin/bash 

# Al crear el archivo se le dieron permisos de ejecucion:
#   - chmod 777 app.sh 

# Funcion que imprime el nombre de la aplicacion
# figlet App (de aqui se optiene el texto para el logo)
app_name="project_3d_video_analysis_and_unity"

function print_logo(){
    figlet $app_name
    echo ""
}

# Funcion que imprime los 'logs' de los servicios
function print_logs(){
    service=$1
    tail=$2
    service_name=$([ "$service" = "app_docker" ] && echo "Aplicacion")
    echo "  - $service_name (logs):"
    while IFS= read -r line
    do
        echo -e "\t$line"
    done < <(docker-compose -f ./$service/docker-compose.yaml logs --tail $([ "$tail" = "" ] && echo "all" || echo $tail))
    echo ""
}

# Funcion que imprime el estado actual de los servicios
function print_status(){
    echo "Estado actual de los servicios:"
    for service in "app_docker" 
    do
        service_name=$([ "$service" = "app_docker" ] && echo "Aplicacion")
        res=$(is_active $service)
        if [ "$res" -eq 0 ]; then
            # Servicio detenido
            echo -e "\033[31m  - '$service_name' detenido \033[0m"
        else
            # Servicio iniciado
            echo -e "\033[32m  - '$service_name' iniciado \033[0m"
        fi
    done
    echo ""
}

# Funcion que verifica el estado de los servicios
#   - Aplicacion 
function is_active(){
    count=0
    while IFS=: read -r elem ; 
    do
        ((count++))
    done < <(docker compose -f ./$1/docker-compose.yaml ps --format json)
    
    if [ "$count" -eq 0 ]; then
        # Esta detenido el servicio
        echo 0
    else
        # Esta iniciado el servicio
        echo 1
    fi
}

# Funcion para confirmar una accion critica
function ask_yes_no(){
    read -e -p "$1 (si/no)? " sino
    echo "$sino"
}

# Funcion para crear una red en Docker
function create_network(){
    network_exists=false
    while IFS= read -r network
    do
        if [ "$network" == "network_$app_name" ]; then
            network_exists=true
        fi
    done < <(docker network ls | awk '{print $2}' | tail -n+2)
    if ! $network_exists; then
        res=$(docker network create -d bridge network_$app_name)
    fi
}

# Funcion para eliminar contenedores con 'status=exited'
function delete_exited_containers(){
    while IFS= read -r container_id
    do
        res=$(docker rm -f $container_id)
    done < <(docker ps -a -f status=exited -q)
}

delete_exited_containers
clear
print_logo
print_status

# Si no existe la red 'network_$app_name' la creamos 
# Esta red permite la comunicacion entre servicios 
create_network
                                                                                                                                               
option_1="Salir"
option_2="Iniciar/Detener aplicacion"
option_3="Recargar"
option_4="Mostrar logs"
option_5="Eliminar volumenes de la aplicacion"

select option in "$option_1" "$option_2" "$option_3" "$option_4" "$option_5";
do
    logs=false

    if [ "$option" = "$option_1" ]; then
        exit
    elif [ "$option" = "$option_2" ]; then
        # Este comando es necesario para dar permisos de que Docker abra interfaces graficas
        res=$(xhost +local:docker)
        # Iniciamos/Detenemos el servicio de aplicacion
        res=$(is_active "app_docker")
        if [ "$res" -eq 0 ]; then
            # Iniciamos el servicio de aplicacion
            docker-compose -f ./app_docker/docker-compose.yaml up -d
        else
            # Detenemos el servicio de aplicacion
            docker-compose -f ./app_docker/docker-compose.yaml down
        fi
    elif [ "$option" = "$option_3" ]; then
        :
    elif [ "$option" = "$option_4" ]; then
        logs=true
    elif [ "$option" = "$option_5" ]; then
        while IFS= read -r sino
        do
            if [ "$sino" = "si" ]; then
                res=$(docker volume rm volume_$app_name)
            fi
        done < <(ask_yes_no "Desea eliminar los volumenes de la aplicacion")
    else 
        echo "Opcion invalida"
    fi 

    delete_exited_containers
    print_logo
    if $logs; then
        print_logs "app_docker" "10"
    fi
    print_status

    REPLY=
done

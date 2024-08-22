# Guía de Configuración y Despliegue de la Aplicación Django con Docker y Docker Swarm

## 1. Clonar el Repositorio

```bash
git clone <URL-del-repositorio>
cd <nombre-del-repositorio>
```
## 2. Construir y Levantar los Contenedores

### Construir las Imágenes

```bash
docker-compose build
```
### Levantar los Contenedores

```bash
docker-compose up -d
```
## 3. Correr el Script `seeder.py`

### Accede al contenedor de la aplicación Django para ejecutar el script de inicialización:

```bash
docker-compose exec book-review-app python /code/seeder.py
```
## 4. Inicializar Docker Swarm

### Inicializa Docker Swarm en el nodo:

```bash
docker swarm init
```
## 5. Desplegar la Stack en Docker Swarm

### Despliega la stack usando el archivo `docker-stack.yml`:

```bash
docker stack deploy -c docker-stack.yml bookreview_stack
```
### Verifica el estado:

```bash
docker stack services bookreview_stack
```

## 6. Escalar el Servicio

### Escala el servicio book-review-app a 4 réplicas:

```bash
docker service scale bookreview_stack_book-review-app=4
```
### Verifica el estado:

```bash
docker stack services bookreview_stack
```

## 7. Verifica el estado

### Verificar los Contenedores:

```bash
docker ps
```
## 8. Parar Todos los Servicios y Eliminar la Stack

### Detén y elimina todos los servicios de la stack:

```bash
docker stack rm bookreview_stack
```
## 9. (Opcional) Detener Todos los Contenedores

### Detén todos los contenedores en ejecución:

```bash
docker stop $(docker ps -q)
```
## 10. (Opcional) Eliminar Todos los Contenedores

### Elimina todos los contenedores (activos e inactivos):

```bash
docker rm $(docker ps -a -q)
```
## 11. (Opcional) Desactivar Docker Swarm

### Desactiva Docker Swarm en el nodo:

```bash
docker swarm leave --force
```
## 12. (Opcional) Eliminar Redes y Volúmenes

### Eliminar Redes y volumenes

```bash
docker network prune
docker volume prune
```

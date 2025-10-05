# Normal DockerFile Commands

### create a network called "fastapi-network"
sudo docker network create fastapi-network

### create Postgres Instance and name the container as "my-postgres-container-fastapi"
sudo docker run -d --name my-postgres-container-fastapi --network fastapi-network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=e_cloud_learniverse_db postgres:17


### build image
sudo docker build --tag e-cloud-fastapi-docker-image .

### run image on (Host---> 8002 Port & Inside Container's Port 9998)
sudo docker run --rm --name my-fastapi-web-container --network fastapi-network --publish 8002:9998 -v $(pwd)/.env_docker:/web_app/.env e-cloud-fastapi-docker-image

### Going into the Docker Container
sudo docker exec -it <CONTAINER_ID> /bin/bash

# Docker-Compose Commands
sudo docker-compose build
sudo docker-compose up

### eksathe UP & BUILD dite hobe naile kaaj korbe Nah
sudo docker-compose up --build (naile `DEPENDS_ON` property of docker-compose er ta kaaj kore Nah)
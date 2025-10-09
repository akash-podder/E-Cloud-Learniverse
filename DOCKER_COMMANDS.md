# Normal DockerFile Commands

### create a network called "fastapi-network"
```shell script
sudo docker network create fastapi-network
```

### create Postgres Instance and name the container as "my-postgres-container-fastapi"
```shell script
sudo docker run -d --name my-postgres-container-fastapi --network fastapi-network -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=e_cloud_learniverse_db postgres:17
```

### build image
```shell script
sudo docker build --tag e-cloud-fastapi-docker-image ./backend
```

### run image on (Host---> 8002 Port & Inside Container's Port 9998)
```shell script
sudo docker run --rm --name my-fastapi-web-container --network fastapi-network --publish 8002:9998 -v $(pwd)/backend/.env_docker:/web_app/.env e-cloud-fastapi-docker-image
```

### Going into the Docker Container
```shell script
sudo docker exec -it <CONTAINER_ID> /bin/shell script
```

# Docker-Compose Commands
```shell script
sudo docker-compose build
sudo docker-compose up
```

### eksathe UP & BUILD dite hobe naile kaaj korbe Nah
```shell script
sudo docker-compose up --build (naile `DEPENDS_ON` property of docker-compose er ta kaaj kore Nah)
```
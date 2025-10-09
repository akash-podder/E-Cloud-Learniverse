# FastAPI Tutorial

### Setup Instructions

### 1. Clone the Repository
```shell script
git clone https://github.com/akash-podder/E-Cloud-FastAPI-Learniverse.git
```

### 2. Create and Activate Virtual Environment and install dependencies
```shell script
python -m venv my_venv
source my_venv/bin/activate
pip install -r requirements.txt
```

### 3. To run in Development Mode
```shell script
fastapi dev main.py
```

### 4. Start Uvicorn Server for Production
```shell script
uvicorn main:app --reload
```

For Production run with Multiple Workers (Example shown with 4 workers)
```shell script
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --reload
```

## Run using the Docker Image

Run the following command in the project root (where your Dockerfile is located):

```shell script
docker build -t my-fastapi-app .
docker run --rm -d -p 9998:9998 --name my-fastapi-container my-fastapi-app
```

### Postgres in Docker Command
```shell script
docker run --rm -it --name my-postgres-container -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=e_cloud_learniverse_db -p 5433:5432 postgres:17
```

###
psycopg2-binary installation Command
```shell script
pip install --no-build-isolation --only-binary :all: psycopg2-binary sqlalchemy
```
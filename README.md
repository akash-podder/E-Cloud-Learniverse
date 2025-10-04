# FastAPI Tutorial

### Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/RatedRAkash/FastAPI_Tutorial.git
```

### 2. Create and Activate Virtual Environment and install dependencies
```bash
python -m venv my_venv
source my_venv/bin/activate
pip install -r requirements.txt
```

### 3. To run in Development Mode
```bash
fastapi dev main.py
```

### 4. Start Uvicorn Server for Production
```bash
uvicorn main:app --reload
```

For Production run with Multiple Workers
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --reload
```

## Run using the Docker Image

Run the following command in the project root (where your Dockerfile is located):

```bash
docker build -t my-fastapi-app .
docker run --rm -d -p 9998:9998 --name my-fastapi-container my-fastapi-app
```
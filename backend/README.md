# FastAPI Backend - E-Cloud Learniverse

## Overview

This directory contains the FastAPI backend application for the E-Cloud Learniverse project. The application provides a RESTful API and serves HTML templates for a message board application with PostgreSQL database integration.

---

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── schemas.py              # Pydantic models for request/response validation
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image configuration
├── .env                   # Environment variables (local development)
├── .env_docker           # Environment variables (Docker)
├── database/             # Database configuration
│   ├── database_init.py  # Database initialization with retry logic
│   ├── config.py         # Database settings
│   └── create_tables.py  # Manual table creation script
├── models/               # SQLAlchemy ORM models
│   └── message_model.py  # Message table model
├── static/              # Static files (CSS, JS, images)
└── templates/           # Jinja2 HTML templates
    └── index.html       # Main page template
```

---

## Features

### API Endpoints

#### REST API (JSON)
- `GET /api/messages` - Get all messages
- `POST /api/messages` - Create a new message
- `GET /api/messages/{id}` - Get a single message by ID
- `DELETE /api/messages/{id}` - Delete a message by ID

#### HTML Pages
- `GET /` - Main message board page (HTML template)
- `POST /` - Submit new message via form

#### Health Check
- `GET /health-check` - Application health status

### Key Technologies
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database operations
- **AsyncPG** - Async PostgreSQL driver
- **Pydantic** - Data validation
- **Jinja2** - HTML templating
- **Uvicorn** - ASGI server

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 15+ (or Docker)

### Local Development

1. **Create Virtual Environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env .env.local  # Copy and modify as needed
   ```

   Edit `.env`:
   ```env
   DATABASE_USER=postgres
   DATABASE_PASSWORD=postgres
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=e_cloud_learniverse_db
   ```

4. **Start PostgreSQL** (if not using Docker)
   ```bash
   # Using Homebrew (macOS)
   brew services start postgresql@15

   # Or use Docker
   docker run -d --name postgres-dev \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=e_cloud_learniverse_db \
     -p 5432:5432 \
     postgres:15
   ```

5. **Run the Application**

   Development mode (auto-reload):
   ```bash
   fastapi dev main.py
   # Access at: http://localhost:8000
   ```

   Production mode:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 9998
   # Access at: http://localhost:9998
   ```

---

## Docker Deployment

### Build Docker Image

```bash
# From project root
docker build -t e-cloud-fastapi-backend ./backend

# Or from backend directory
cd backend
docker build -t e-cloud-fastapi-backend .
```

### Run with Docker

```bash
# Run standalone (requires external PostgreSQL)
docker run -p 8002:9998 \
  -e DATABASE_HOST=host.docker.internal \
  -e DATABASE_USER=postgres \
  -e DATABASE_PASSWORD=postgres \
  -e DATABASE_NAME=e_cloud_learniverse_db \
  e-cloud-fastapi-backend
```

### Run with Docker Compose

From project root:
```bash
docker-compose up --build
# Backend will be available at: http://localhost:8002
```

---

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8002/docs
- **ReDoc**: http://localhost:8002/redoc

### Example API Usage

#### Get All Messages
```bash
curl http://localhost:8002/api/messages
```

#### Create Message
```bash
curl -X POST http://localhost:8002/api/messages \
  -H "Content-Type: application/json" \
  -d '{"username": "John", "content": "Hello World!"}'
```

#### Get Single Message
```bash
curl http://localhost:8002/api/messages/1
```

#### Delete Message
```bash
curl -X DELETE http://localhost:8002/api/messages/1
```

---

## Database

### Configuration

Database settings are managed via environment variables (see `.env` file):
- `DATABASE_USER` - PostgreSQL username
- `DATABASE_PASSWORD` - PostgreSQL password
- `DATABASE_HOST` - Database host (localhost or container name)
- `DATABASE_PORT` - Database port (default: 5432)
- `DATABASE_NAME` - Database name

### Retry Logic

The application includes automatic retry logic for database connections (configured in `database/database_init.py`):
- **Max Retries**: 5
- **Retry Delay**: 2 seconds
- **Purpose**: Wait for PostgreSQL to be ready in containerized environments

### Manual Table Creation

If needed, create tables manually:
```bash
cd backend
python -m database.create_tables
```

---

## Development

### Code Structure

**main.py** - Application setup and routes
```python
- FastAPI app initialization
- CORS configuration
- Lifespan events (database initialization)
- Route handlers (HTML and API endpoints)
```

**schemas.py** - Data models
```python
- MessageCreate: Request model for creating messages
- MessageRead: Response model with database fields
```

**database/database_init.py** - Database setup
```python
- AsyncEngine creation
- Session management
- Table creation with retry logic
```

**models/message_model.py** - ORM models
```python
- Message table definition
- SQLAlchemy Column definitions
```

### Adding New Endpoints

1. Define Pydantic schema in `schemas.py`:
```python
class NewModelCreate(BaseModel):
    field1: str
    field2: int
```

2. Create ORM model in `models/`:
```python
class NewModel(Base):
    __tablename__ = "new_table"
    id = Column(Integer, primary_key=True)
    field1 = Column(String)
```

3. Add route in `main.py`:
```python
@app.post("/api/newmodel", response_model=NewModelRead)
async def create_item(item: NewModelCreate, db: AsyncSession = Depends(get_db)):
    # Implementation
```

---

## Testing

### Health Check
```bash
curl http://localhost:8002/health-check
# Response: {"message": "Health is Okay"}
```

### Manual Testing
1. Access web interface: http://localhost:8002
2. Submit messages via form
3. View messages on the page

### API Testing
Use the interactive docs: http://localhost:8002/docs

---

## Troubleshooting

### Common Issues

**Issue**: Database connection refused
```bash
Error: Connection refused [Errno 111]
```
**Solution**:
- Ensure PostgreSQL is running
- Check DATABASE_HOST environment variable
- In Docker, use service name (e.g., `learniverse_db`) instead of `localhost`

**Issue**: Module not found
```bash
ModuleNotFoundError: No module named 'fastapi'
```
**Solution**:
```bash
pip install -r requirements.txt
```

**Issue**: Port already in use
```bash
Error: Address already in use
```
**Solution**:
```bash
# Find process using port
lsof -i :9998

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8000
```

### Logs

Enable debug logging:
```python
# In database_init.py, the engine has echo=True
engine = create_async_engine(DATABASE_URL, echo=True)
```

View SQL queries in console output.

---

## Environment Variables Reference

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `DATABASE_USER` | PostgreSQL username | postgres | postgres |
| `DATABASE_PASSWORD` | PostgreSQL password | postgres | secretpass |
| `DATABASE_HOST` | Database host | localhost | learniverse_db |
| `DATABASE_PORT` | Database port | 5432 | 5432 |
| `DATABASE_NAME` | Database name | e_cloud_learniverse_db | mydb |

---

## Deployment

### Production Considerations

1. **Security**:
   - Use strong database passwords
   - Enable HTTPS
   - Configure CORS properly
   - Use environment-specific .env files

2. **Performance**:
   - Use multiple Uvicorn workers: `--workers 4`
   - Enable connection pooling
   - Add caching where appropriate

3. **Monitoring**:
   - Add logging
   - Set up health checks
   - Monitor database connections

### Production Command

```bash
uvicorn main:app \
  --host 0.0.0.0 \
  --port 9998 \
  --workers 4 \
  --log-level info
```

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

## License

See main project LICENSE file.

---

## Contributing

See main project CONTRIBUTING guidelines.

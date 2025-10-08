from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager
from typing import List

from database.database_init import init_models, get_db
from models import message_model
from schema.message_schema import MessageCreate, MessageUpdate, MessageRead

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()  # 👈 Startup logic, without this you to manually type: python -m database.create_tables
    yield
    # (Optional) Cleanup logic

app = FastAPI(lifespan=lifespan)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# for enabling "static" files and "Jinja" templates
# =====================================================
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# for Health check
@app.get("/health-check")
async def root():
    return {"message": "Health is Okay"}

# =====================================================
# MAIN VIEW for FASTAPI Jinja Template FRONTEND
# =====================================================

# GET
@app.get("/", response_class=HTMLResponse)
async def show_index(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(message_model.Message))
    messages = result.scalars().all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "messages": messages}
    )

# ----- FORM HANDLER -----
# POST
@app.post("/", response_class=HTMLResponse)
async def add_message(
    request: Request,
    username: str = Form(...),
    content: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    new_msg = message_model.Message(username=username, content=content)
    db.add(new_msg)
    await db.commit()
    await db.refresh(new_msg)
    # Redirect to refresh message list
    return RedirectResponse(url="/", status_code=303)



# =====================================================
# REST API ENDPOINTS FOR REACT FRONTEND
# =====================================================

# GET all messages - REST API endpoint
@app.get("/api/messages", response_model=List[MessageRead])
async def get_messages(db: AsyncSession = Depends(get_db)):
    """
    Get all messages from the database
    Returns: List of messages with id, username, and content
    """
    result = await db.execute(select(message_model.Message))
    messages = result.scalars().all()
    return messages


# POST new message - REST API endpoint
@app.post("/api/messages", response_model=MessageRead, status_code=201)
async def create_message(
    message: MessageCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new message
    Request body: {"username": "string", "content": "string"}
    Returns: Created message with id
    """
    new_msg = message_model.Message(
        username=message.username,
        content=message.content
    )
    db.add(new_msg)
    await db.commit()
    await db.refresh(new_msg)
    return new_msg


# GET single message by ID - REST API endpoint
@app.get("/api/messages/{message_id}", response_model=MessageRead)
async def get_message(message_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single message by ID
    Returns: Message with the specified ID
    """
    result = await db.execute(
        select(message_model.Message).where(message_model.Message.id == message_id)
    )
    message = result.scalar_one_or_none()
    if not message:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Message not found")
    return message


# PUT update message by ID - REST API endpoint
@app.put("/api/messages/{message_id}", response_model=MessageRead)
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a message by ID
    Request body: {"username": "string", "content": "string"}
    Returns: Updated message
    """
    result = await db.execute(
        select(message_model.Message).where(message_model.Message.id == message_id)
    )
    message = result.scalar_one_or_none()
    if not message:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.username = message_update.username
    message.content = message_update.content
    await db.commit()
    await db.refresh(message)
    return message


# DELETE message by ID - REST API endpoint
@app.delete("/api/messages/{message_id}", status_code=204)
async def delete_message(message_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a message by ID
    Returns: 204 No Content on success
    """
    result = await db.execute(
        select(message_model.Message).where(message_model.Message.id == message_id)
    )
    message = result.scalar_one_or_none()
    if not message:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Message not found")

    await db.delete(message)
    await db.commit()
    return None
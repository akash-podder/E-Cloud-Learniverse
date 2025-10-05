from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from contextlib import asynccontextmanager

from database.database_init import init_models, get_db
from models import message_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()  # 👈 Startup logic, without this you to manually type: python -m database.create_tables
    yield
    # (Optional) Cleanup logic

app = FastAPI(lifespan=lifespan)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/index")
async def root():
    return {"message": "Hola World from Index"}

# ----- MAIN VIEW -----
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
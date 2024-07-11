from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from .middleware.chatbot import process_chat
from .database import init_db, add_chat_entry, get_chat_history, clear_chat_history
import uuid
from app.chatbot_manager import chatbot_manager

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Setup templates directory
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    await init_db()
    await chatbot_manager.update_store_info()

@app.post("/clear", response_class=HTMLResponse)
async def clear_chat(request: Request):
    session_id = request.session.get("session_id")
    if session_id:
        await clear_chat_history(session_id)
    return RedirectResponse(url="/", status_code=303)

@app.post("/", response_class=HTMLResponse)
async def handle_chat(request: Request, user_input: str = Form(...)):
    session_id = request.session.get("session_id")
    chat_history = await get_chat_history(session_id)
    
    chat_response = await process_chat(user_input, chat_history)
    
    await add_chat_entry(session_id, user_input, chat_response)
    
    updated_chat_history = await get_chat_history(session_id)
    
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "chat_history": updated_chat_history,
            "disable_loading": True  # New context variable
        }
    )

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    if "session_id" not in request.session:
        request.session["session_id"] = str(uuid.uuid4())
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def handle_chat(request: Request, user_input: str = Form(...)):
    session_id = request.session.get("session_id")
    chat_history = await get_chat_history(session_id)
    
    chat_response = await process_chat(user_input, chat_history)
    
    # Add chat entry to database
    await add_chat_entry(session_id, user_input, chat_response)
    
    # Get updated chat history
    updated_chat_history = await get_chat_history(session_id)
    
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": updated_chat_history,
    })

@app.post("/clear", response_class=HTMLResponse)
async def clear_chat(request: Request):
    session_id = request.session.get("session_id")
    if session_id:
        await clear_chat_history(session_id)
    # Generate a new session ID
    request.session["session_id"] = str(uuid.uuid4())
    return RedirectResponse(url="/", status_code=303)
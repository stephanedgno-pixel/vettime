import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_303_SEE_OTHER

from app.database import get_db
from app.models import Utilisateur
from app.security import verify_password

load_dotenv() 

app = FastAPI(title="VetTime")

def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=HTTP_303_SEE_OTHER, headers={"Location": "/login"})
    return user_id

templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"), https_only=os.getenv("VETTIME_HTTPS_ONLY", "true").lower() != "false")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db(db: Session = Depends(get_db)):
    # Vérifie que la base répond (requête minimale).
    # Si la DB est injoignable, get_db lève déjà 503 ; on ajoute un garde explicite.
    try:
        db.execute(text("SELECT 1")).scalar()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=503, detail=f"database unreachable: {e}")
    return {"status": "ok", "database": "connected"}

@app.get("/login")
def login_page(request: Request):
    if "csrf_token" not in request.session:
        request.session["csrf_token"] = secrets.token_hex(32)
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), csrf_token: str = Form(...), db: Session = Depends(get_db)):
    if not request.session.get("csrf_token") or csrf_token != request.session.get("csrf_token"):
        raise HTTPException(status_code=403, detail="Jeton CSRF invalide")
    user = db.query(Utilisateur).filter(Utilisateur.email == email).first()
    if user and user.actif and verify_password(password, user.mot_de_passe_hash):
        request.session["user_id"] = user.id_utilisateur
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"error": "Identifiants invalides"})

@app.get("/")
def home(request: Request, user_id: int = Depends(get_current_user)):
    return templates.TemplateResponse(request, "home.html")

@app.post("/logout")
def logout(request: Request, csrf_token: str = Form(...)):
    if not request.session.get("csrf_token") or csrf_token != request.session.get("csrf_token"):
        raise HTTPException(status_code=403, detail="Jeton CSRF invalide")
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

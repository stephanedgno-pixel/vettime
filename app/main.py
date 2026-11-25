import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app.database import get_db
from app.models import Utilisateur
from app.security import verify_password

load_dotenv() 

app = FastAPI(title="VetTime")

templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"), https_only=True)

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
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(Utilisateur).filter(Utilisateur.email == email).first()
    if user and user.actif and verify_password(password, user.mot_de_passe_hash):
        request.session["user_id"] = user.id_utilisateur
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"error": "Identifiants invalides"})

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html")

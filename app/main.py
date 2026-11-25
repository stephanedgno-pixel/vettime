import os
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db


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

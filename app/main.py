from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db

app = FastAPI(title="VetTime")

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

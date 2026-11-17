# app/database.py — le module de connexion à PostgreSQL
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()  # lit .env (contient l'URL avec le mot de passe)

# URL de connexion : postgresql://utilisateur:***@hote:port/nomdb
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# engine = le "pont" vers la base. Créé seulement si l'URL existe
# (sinon l'import ne plante pas en CI / sans .env).
engine = create_engine(SQLALCHEMY_DATABASE_URL) if SQLALCHEMY_DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None

# get_db = donnée aux routes pour obtenir une connexion, puis la ferme
def get_db():
    if SessionLocal is None:
        raise HTTPException(status_code=503, detail="DATABASE_URL non configurée")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# app/database.py — le module de connexion à PostgreSQL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

load_dotenv()  # lit .env (contient l'URL avec le mot de passe)

# URL de connexion : postgresql://utilisateur:***@hote:port/nomdb
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# engine = le "pont" vers la base
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = usine à sessions (chaque session = une conversation avec la DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# get_db = donnée aux routes pour obtenir une connexion, puis la ferme
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
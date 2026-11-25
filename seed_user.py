
from dotenv import load_dotenv

from app.database import SessionLocal
from app.models import Role, Utilisateur
from app.security import hash_password

# Charge .env (DATABASE_URL + SECRET_KEY)
load_dotenv()

db = SessionLocal()

# 1) Role de test (get or create)
role = db.query(Role).filter(Role.nom == "employe").first()
if not role:
    role = Role(nom="employe", description="Compte employe (test)")
    db.add(role)
    db.commit()
    db.refresh(role)
    print(f"[seed] role cree: id={role.id_role} nom={role.nom}")

# 2) Utilisateur de test (get or create)
email = "test@vettime.local"
user = db.query(Utilisateur).filter(Utilisateur.email == email).first()
if user:
    print(f"[seed] utilisateur {email} deja present (id={user.id_utilisateur})")
else:
    user = Utilisateur(
        email=email,
        mot_de_passe_hash=hash_password("MotDePasse123!"),
        id_role=role.id_role,
        nom_complet="Utilisateur Test",
        actif=True,
    )
    db.add(user)
    db.commit()
    print(f"[seed] utilisateur cree: {email} / MotDePasse123!")

db.close()

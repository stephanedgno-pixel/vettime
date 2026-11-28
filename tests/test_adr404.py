import os

os.environ["VETTIME_HTTPS_ONLY"] = "false"  # cookie de session non-Secure en test (HTTP)

import re

from fastapi.testclient import TestClient

from app.database import SessionLocal
from app.main import app
from app.models import Poincon

EMAIL = "test@vettime.local"
PASSWORD = "MotDePasse123!"


def test_csrf_pointe():
    c = TestClient(app, base_url="http://127.0.0.1:8000")

    # Authentification -> session + jeton CSRF
    r = c.get("/login")
    m = re.search(r'name="csrf_token" value="([^"]+)"', r.text)
    assert m, "jeton CSRF absent du formulaire de login"
    tok = m.group(1)
    r = c.post(
        "/login",
        data={"email": EMAIL, "password": PASSWORD, "csrf_token": tok},
        follow_redirects=False,
    )
    assert r.status_code in (302, 303), r.status_code

    # Token valide -> 303 (succès, redirection vers l'accueil)
    r_ok = c.post("/pointe", data={"csrf_token": tok}, follow_redirects=False)
    assert r_ok.status_code == 303, f"attendu 303, recu {r_ok.status_code}"

    # Token invalide -> 403 (rejeté par la validation CSRF, ADR-004)
    r_bad = c.post("/pointe", data={"csrf_token": "mauvais"}, follow_redirects=False)
    assert r_bad.status_code == 403, f"attendu 403, recu {r_bad.status_code}"

    # Token absent -> 422 (FastAPI refuse le champ requis ; requête rejetée)
    r_none = c.post("/pointe", data={}, follow_redirects=False)
    assert r_none.status_code == 422, f"attendu 422, recu {r_none.status_code}"

    # Nettoyage du poinçon de test
    db = SessionLocal()
    db.query(Poincon).delete()
    db.commit()
    db.close()

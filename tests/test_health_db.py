from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

def test_health_db_responds():
    client = TestClient(app)
    r = client.get("/health/db")
    # 200 = base connectée ; 503 = base injoignable. Les deux prouvent que la
    # route fonctionne sans faire planter le serveur.
    assert r.status_code in (status.HTTP_200_OK, status.HTTP_503_SERVICE_UNAVAILABLE)
    if r.status_code == status.HTTP_200_OK:
        assert r.json() == {"status": "ok", "database": "connected"}

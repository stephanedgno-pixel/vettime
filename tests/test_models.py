from app.models import Base


def test_onze_tables():
    # Le modèle doit refléter exactement les 11 tables du schéma v1.1.
    assert len(Base.metadata.tables) == 11

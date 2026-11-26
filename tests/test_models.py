from app.models import Base


def test_douze_tables():
    # Le modele doit refleter exactement les 12 tables (11 du schema v1.1 + poincons issue #2).
    assert len(Base.metadata.tables) == 12

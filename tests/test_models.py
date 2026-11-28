from app.models import Base


def test_treize_tables():
    # Modele = 11 tables schema v1.1 + poincons (issue #2) + mouvements_banque (ADR-006) = 13.
    assert len(Base.metadata.tables) == 13
    assert "mouvements_banque" in Base.metadata.tables

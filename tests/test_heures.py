from dataclasses import dataclass
from datetime import datetime, timedelta

from app.heures import calculer_total_heures, regrouper_par_jour


@dataclass
class _Poincon:
    type_poincon: str
    horodatage: datetime


def _p(type_p, heure):
    return _Poincon(type_p, heure)


def test_total_8h_une_journee():
    ps = [
        _p("entree", datetime(2026, 1, 5, 8, 0)),
        _p("sortie", datetime(2026, 1, 5, 16, 0)),
    ]
    assert calculer_total_heures(ps) == timedelta(hours=8)


def test_total_16h_deux_journees():
    ps = [
        _p("entree", datetime(2026, 1, 5, 8, 0)),
        _p("sortie", datetime(2026, 1, 5, 16, 0)),
        _p("entree", datetime(2026, 1, 6, 9, 0)),
        _p("sortie", datetime(2026, 1, 6, 17, 0)),
    ]
    assert calculer_total_heures(ps) == timedelta(hours=16)


def test_entree_sans_sortie_ignoree():
    # 1re entree (8h) sans sortie -> ignoree ; 2e entree (12h)+sortie(16h) = 4h
    ps = [
        _p("entree", datetime(2026, 1, 5, 8, 0)),
        _p("entree", datetime(2026, 1, 5, 12, 0)),
        _p("sortie", datetime(2026, 1, 5, 16, 0)),
    ]
    assert calculer_total_heures(ps) == timedelta(hours=4)


def test_regrouper_par_jour():
    ps = [
        _p("entree", datetime(2026, 1, 5, 8, 0)),
        _p("sortie", datetime(2026, 1, 5, 16, 0)),
        _p("entree", datetime(2026, 1, 6, 9, 0)),
        _p("sortie", datetime(2026, 1, 6, 17, 0)),
    ]
    groupes = regrouper_par_jour(ps)
    assert len(groupes) == 2
    assert groupes[0]["total"] == timedelta(hours=8)
    assert groupes[1]["total"] == timedelta(hours=8)

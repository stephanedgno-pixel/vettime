import os
import uuid

os.environ["VETTIME_HTTPS_ONLY"] = "false"

from datetime import date, datetime

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.banques import approuver_demande_conge, calculer_solde, ecrire_mouvement
from app.database import engine
from app.models import (
    BanqueMaladie,
    BanqueVacances,
    DemandeConge,
    Employe,
    MouvementBanque,
    Role,
    Utilisateur,
)


@pytest.fixture
def db():
    """Session isolée par transaction : tout est annulé après le test.

    Évite la pollution inter-tests (pas de commit visible hors transaction) et
    ne touche pas à l'utilisateur seed (test_adr404 en dépend)."""
    if engine is None:
        pytest.skip("DATABASE_URL absent : test ledger sauté en CI (pas de DB)")
    from app.models import Base

    Base.metadata.create_all(engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def _creer_employe(db):
    """Crée role admin + utilisateur + employé + banques vides (email unique)."""
    suffixe = uuid.uuid4().hex[:8]
    role = db.scalar(select(Role).where(Role.nom == "admin"))
    if role is None:
        role = Role(nom="admin")
        db.add(role)
        db.flush()
    user = Utilisateur(
        email=f"ledger-{suffixe}@vettime.local",
        mot_de_passe_hash="x",
        id_role=role.id_role,
        nom_complet="Test Ledger",
    )
    db.add(user)
    db.flush()
    emp = Employe(
        utilisateur_id=user.id_utilisateur,
        nom="Ledger",
        prenom="Test",
        poste="vet",
    )
    db.add(emp)
    db.flush()
    db.add(BanqueVacances(id_employe=emp.id_employe, solde_actuel=0))
    db.add(BanqueMaladie(id_employe=emp.id_employe, solde_actuel=0))
    db.flush()
    return emp


def test_solde_actuel_egal_sum(db):
    emp = _creer_employe(db)
    ecrire_mouvement(
        db,
        emp.id_employe,
        "vacances",
        "accumulation",
        10.0,
        cree_par=1,
        date_mouvement=datetime(2026, 3, 1),
    )
    ecrire_mouvement(
        db,
        emp.id_employe,
        "vacances",
        "utilisation",
        -4.0,
        cree_par=2,
        date_mouvement=datetime(2026, 7, 10),
    )
    ecrire_mouvement(
        db,
        emp.id_employe,
        "vacances",
        "ajustement",
        2.0,
        cree_par=1,
        date_mouvement=datetime(2026, 8, 5),
    )
    db.flush()
    somme = calculer_solde(db, emp.id_employe, "vacances")
    banque = db.scalar(
        select(BanqueVacances).where(BanqueVacances.id_employe == emp.id_employe)
    )
    assert somme == pytest.approx(8.0)
    assert float(banque.solde_actuel) == pytest.approx(8.0)


def test_chaine_solde_apres_coherente(db):
    emp = _creer_employe(db)
    ecrire_mouvement(
        db,
        emp.id_employe,
        "vacances",
        "accumulation",
        10.0,
        date_mouvement=datetime(2026, 3, 1),
    )
    ecrire_mouvement(
        db,
        emp.id_employe,
        "vacances",
        "utilisation",
        -4.0,
        date_mouvement=datetime(2026, 7, 10),
    )
    ecrire_mouvement(
        db,
        emp.id_employe,
        "vacances",
        "ajustement",
        2.0,
        date_mouvement=datetime(2026, 8, 5),
    )
    db.flush()
    mvts = db.scalars(
        select(MouvementBanque)
        .where(
            MouvementBanque.id_employe == emp.id_employe,
            MouvementBanque.type_banque == "vacances",
        )
        .order_by(MouvementBanque.date_mouvement)
    ).all()
    precedent = 0.0
    for m in mvts:
        assert float(m.solde_apres) == pytest.approx(precedent + float(m.montant))
        precedent = float(m.solde_apres)
    assert precedent == pytest.approx(8.0)


def test_cash_out_maladie(db):
    emp = _creer_employe(db)
    ecrire_mouvement(
        db,
        emp.id_employe,
        "maladie",
        "accumulation",
        5.0,
        date_mouvement=datetime(2026, 11, 1),
    )
    ecrire_mouvement(
        db,
        emp.id_employe,
        "maladie",
        "cash_out",
        -5.0,
        date_mouvement=datetime(2027, 1, 1),
    )
    db.flush()
    banque = db.scalar(
        select(BanqueMaladie).where(BanqueMaladie.id_employe == emp.id_employe)
    )
    assert float(banque.solde_actuel) == pytest.approx(0.0)
    assert calculer_solde(db, emp.id_employe, "maladie") == pytest.approx(0.0)


def test_ajustement_administratif(db):
    emp = _creer_employe(db)
    ecrire_mouvement(
        db,
        emp.id_employe,
        "vacances",
        "accumulation",
        10.0,
        date_mouvement=datetime(2026, 3, 1),
    )
    ecrire_mouvement(
        db,
        emp.id_employe,
        "vacances",
        "ajustement",
        2.0,
        cree_par=1,
        note="correction paie",
        date_mouvement=datetime(2026, 8, 5),
    )
    db.flush()
    ajust = db.scalar(
        select(MouvementBanque).where(
            MouvementBanque.type_mouvement == "ajustement",
            MouvementBanque.id_employe == emp.id_employe,
        )
    )
    assert ajust.cree_par == 1
    assert ajust.note == "correction paie"
    assert float(ajust.solde_apres) == pytest.approx(12.0)


def test_utilisation_liee_demande(db):
    emp = _creer_employe(db)
    demande = DemandeConge(
        id_employe=emp.id_employe,
        type_conge="vacances",
        date_debut=date(2026, 7, 10),
        date_fin=date(2026, 7, 12),
        statut="en_attente",
    )
    db.add(demande)
    db.flush()
    approuver_demande_conge(db, demande.id_demande, emp.utilisateur_id)
    db.flush()
    mvts = db.scalars(
        select(MouvementBanque).where(MouvementBanque.id_demande == demande.id_demande)
    ).all()
    assert len(mvts) == 1
    assert mvts[0].type_mouvement == "utilisation"
    assert mvts[0].id_demande == demande.id_demande
    # 3 jours * 7.5h = 22.5h déduites
    assert float(mvts[0].montant) == pytest.approx(-22.5)
    banque = db.scalar(
        select(BanqueVacances).where(BanqueVacances.id_employe == emp.id_employe)
    )
    assert float(banque.solde_actuel) == pytest.approx(-22.5)

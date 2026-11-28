# seed_banques.py — Amorçage du ledger (mouvements 'initial')
#
# À exécuter APRÈS migrations/002_add_mouvements_banque.sql.
# Pour chaque (employe, banque) existant, crée un mouvement 'initial' dont le
# montant = solde_actuel, afin que SUM(montant) == solde_actuel dès le départ.
# Idempotent : n'insère un 'initial' que si aucun mouvement n'existe déjà.
from sqlalchemy import func, select

from app.database import SessionLocal
from app.models import BanqueMaladie, BanqueVacances, MouvementBanque


def seed_banque(db, banque, type_banque):
    existe = db.scalar(
        select(func.count(MouvementBanque.id_mouvement)).where(
            MouvementBanque.id_employe == banque.id_employe,
            MouvementBanque.type_banque == type_banque,
        )
    )
    if existe and existe > 0:
        return  # déjà amorcé
    db.add(
        MouvementBanque(
            id_employe=banque.id_employe,
            type_banque=type_banque,
            type_mouvement="initial",
            montant=float(banque.solde_actuel),
            solde_apres=float(banque.solde_actuel),
            cree_par=None,
            note="Amorçage initial (migration ledger ADR-006)",
        )
    )


def main():
    db = SessionLocal()
    try:
        for b in db.scalars(select(BanqueVacances)).all():
            seed_banque(db, b, "vacances")
        for b in db.scalars(select(BanqueMaladie)).all():
            seed_banque(db, b, "maladie")
        db.commit()
        print("Amorçage ledger terminé.")
    finally:
        db.close()


if __name__ == "__main__":
    main()

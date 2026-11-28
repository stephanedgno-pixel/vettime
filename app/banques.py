# app/banques.py — Helpers du ledger des banques (ADR-006)
#
# Toute variation de solde PASE par ecrire_mouvement() : c'est la source unique
# d'écriture. Cela garantit l'invariant solde_apres(N) == solde_apres(N-1) +
# montant(N) et la synchronisation du cache solde_actuel (banques_*).
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import BanqueMaladie, BanqueVacances, DemandeConge, MouvementBanque


def calculer_solde(db: Session, id_employe: int, type_banque: str) -> float:
    """Solde autoritatif = somme des montants (source de vérité)."""
    total = db.scalar(
        select(func.coalesce(func.sum(MouvementBanque.montant), 0)).where(
            MouvementBanque.id_employe == id_employe,
            MouvementBanque.type_banque == type_banque,
        )
    )
    return float(total)


def dernier_solde_apres(db: Session, id_employe: int, type_banque: str) -> float | None:
    """Dernier solde_apres connu pour (employe, banque), ou None si aucun mouvement."""
    return db.scalar(
        select(MouvementBanque.solde_apres)
        .where(
            MouvementBanque.id_employe == id_employe,
            MouvementBanque.type_banque == type_banque,
        )
        .order_by(
            MouvementBanque.date_mouvement.desc(), MouvementBanque.id_mouvement.desc()
        )
        .limit(1)
    )


def ecrire_mouvement(
    db: Session,
    id_employe: int,
    type_banque: str,
    type_mouvement: str,
    montant: float,
    *,
    id_demande: int | None = None,
    cree_par: int | None = None,
    note: str | None = None,
    date_mouvement: datetime | None = None,
) -> MouvementBanque:
    """Écrit un mouvement et met à jour le solde courant (cache) de la banque.

    solde_apres = (dernier solde_apres ou 0) + montant.
    Invariant : solde_apres(N) == solde_apres(N-1) + montant(N).
    """
    precedent = dernier_solde_apres(db, id_employe, type_banque)
    solde_apres = float(precedent or 0) + float(montant)
    m = MouvementBanque(
        id_employe=id_employe,
        type_banque=type_banque,
        type_mouvement=type_mouvement,
        montant=montant,
        solde_apres=solde_apres,
        id_demande=id_demande,
        cree_par=cree_par,
        note=note,
        date_mouvement=date_mouvement or func.now(),
    )
    db.add(m)
    db.flush()
    # Mise à jour du cache solde_actuel (banques_*)
    if type_banque == "vacances":
        banque = db.scalar(
            select(BanqueVacances).where(BanqueVacances.id_employe == id_employe)
        )
    else:
        banque = db.scalar(
            select(BanqueMaladie).where(BanqueMaladie.id_employe == id_employe)
        )
    if banque is not None:
        banque.solde_actuel = solde_apres
    return m


def approuver_demande_conge(
    db: Session, id_demande: int, id_utilisateur: int
) -> DemandeConge:
    """Approuve une demande et écrit le mouvement 'utilisation' lié.

    Le nombre d'heures est estimé (jours * 7.5h) ; le calcul précis (jours
    ouvrés, heures de contrat) appartient à la future UI d'approbation.
    type_banque = type_conge ('vacances' ou 'maladie') -> banque correspondante.
    """
    d = db.get(DemandeConge, id_demande)
    if d is None:
        raise ValueError(f"demande {id_demande} introuvable")
    d.statut = "approuve"
    d.approuve_par = id_utilisateur
    d.approuve_le = func.now()
    jours = (d.date_fin - d.date_debut).days + 1
    heures = float(jours) * 7.5
    ecrire_mouvement(
        db,
        d.id_employe,
        d.type_conge,
        "utilisation",
        -heures,
        id_demande=d.id_demande,
        cree_par=id_utilisateur,
        note=f"Congé approuvé #{d.id_demande}",
    )
    return d

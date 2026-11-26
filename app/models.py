# app/models.py
# Modèles ORM (SQLAlchemy 2.0) — 11 tables du schéma v1.1 (validé cliente 2026-11-03)
# LOI 25 (dès la conception) : minimisation — on mappe UNIQUEMENT les champs
# nécessaires à la paie (aucun surplus). Rétention 7 ans gérée à l'export comptable.
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Classe de base : tous les modèles héritent de Base (métadonnées partagées)."""


# ---------- Auth & rôles ----------
class Role(Base):
    __tablename__ = "roles"
    id_role: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(100))
    cree_le: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    utilisateurs: Mapped[list["Utilisateur"]] = relationship(back_populates="role")


class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id_utilisateur: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    mot_de_passe_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # bcrypt
    id_role: Mapped[int] = mapped_column(ForeignKey("roles.id_role"), nullable=False)
    nom_complet: Mapped[str | None] = mapped_column(String(100))
    actif: Mapped[bool] = mapped_column(Boolean, default=True)
    cree_le: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    modifie_le: Mapped[DateTime | None] = mapped_column(DateTime)
    role: Mapped["Role"] = relationship(back_populates="utilisateurs")
    employe: Mapped["Employe | None"] = relationship(back_populates="utilisateur")


# ---------- Référence ----------
class StatutJournee(Base):
    __tablename__ = "statuts_journee"
    id_statut: Mapped[int] = mapped_column(Integer, primary_key=True)
    libelle: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # Travail, Congé, Maladie
    pointages: Mapped[list["Pointage"]] = relationship(back_populates="statut")
    horaires: Mapped[list["Horaire"]] = relationship(back_populates="statut")


# ---------- Employés (RH) ----------
class Employe(Base):
    __tablename__ = "employes"
    id_employe: Mapped[int] = mapped_column(Integer, primary_key=True)
    utilisateur_id: Mapped[int | None] = mapped_column(
        ForeignKey("utilisateurs.id_utilisateur")
    )
    nom: Mapped[str] = mapped_column(String(50), nullable=False)
    prenom: Mapped[str] = mapped_column(String(50), nullable=False)
    poste: Mapped[str | None] = mapped_column(String(50))
    heures_contrat_semaine: Mapped[float | None] = mapped_column(Numeric(4, 2))
    utilisateur: Mapped["Utilisateur | None"] = relationship(back_populates="employe")
    pointages: Mapped[list["Pointage"]] = relationship(back_populates="employe")
    horaires: Mapped[list["Horaire"]] = relationship(back_populates="employe")
    demandes_conge: Mapped[list["DemandeConge"]] = relationship(
        back_populates="employe"
    )
    banque_vacances: Mapped["BanqueVacances | None"] = relationship(
        back_populates="employe"
    )
    banque_maladie: Mapped["BanqueMaladie | None"] = relationship(
        back_populates="employe"
    )


# ---------- Pointages ----------
class Pointage(Base):
    __tablename__ = "pointages"
    __table_args__ = (UniqueConstraint("id_employe", "date_jour"),)
    id_pointage: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_employe: Mapped[int] = mapped_column(
        ForeignKey("employes.id_employe"), nullable=False
    )
    date_jour: Mapped[Date] = mapped_column(Date, nullable=False)
    arrivee_matin: Mapped[Time | None] = mapped_column(Time)
    debut_diner: Mapped[Time | None] = mapped_column(Time)
    fin_diner: Mapped[Time | None] = mapped_column(Time)
    depart_soir: Mapped[Time | None] = mapped_column(Time)
    id_statut: Mapped[int | None] = mapped_column(
        ForeignKey("statuts_journee.id_statut")
    )
    employe: Mapped["Employe"] = relationship(back_populates="pointages")
    statut: Mapped["StatutJournee | None"] = relationship(back_populates="pointages")


# ---------- Jours fériés ----------
class JourFerie(Base):
    __tablename__ = "jours_feries"
    id_jour_ferie: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_jour: Mapped[Date] = mapped_column(Date, nullable=False, unique=True)
    nom: Mapped[str] = mapped_column(String(60), nullable=False)
    indemnite_payee: Mapped[bool] = mapped_column(Boolean, default=True)


# ---------- Verrouillage périodes ----------
class PeriodeVerrouillage(Base):
    __tablename__ = "periodes_verrouillage"
    id_periode: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_debut: Mapped[Date] = mapped_column(Date, nullable=False)
    date_fin: Mapped[Date] = mapped_column(Date, nullable=False)
    verrouillee: Mapped[bool] = mapped_column(Boolean, default=False)
    verrouillee_par: Mapped[int | None] = mapped_column(
        ForeignKey("utilisateurs.id_utilisateur")
    )
    verrouillee_le: Mapped[DateTime | None] = mapped_column(DateTime)
    verrouillee_par_user: Mapped["Utilisateur | None"] = relationship("Utilisateur")


# ---------- Horaire planifié ----------
class Horaire(Base):
    __tablename__ = "horaires"
    __table_args__ = (UniqueConstraint("id_employe", "date_jour"),)
    id_horaire: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_employe: Mapped[int] = mapped_column(
        ForeignKey("employes.id_employe"), nullable=False
    )
    date_jour: Mapped[Date] = mapped_column(Date, nullable=False)
    heure_debut: Mapped[Time | None] = mapped_column(Time)
    heure_fin: Mapped[Time | None] = mapped_column(Time)
    id_statut: Mapped[int | None] = mapped_column(
        ForeignKey("statuts_journee.id_statut")
    )
    employe: Mapped["Employe"] = relationship(back_populates="horaires")
    statut: Mapped["StatutJournee | None"] = relationship(back_populates="horaires")


# ---------- Demandes de congé ----------
class DemandeConge(Base):
    __tablename__ = "demandes_conge"
    id_demande: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_employe: Mapped[int] = mapped_column(
        ForeignKey("employes.id_employe"), nullable=False
    )
    type_conge: Mapped[str] = mapped_column(
        String(30), nullable=False
    )  # vacances, maladie
    date_debut: Mapped[Date] = mapped_column(Date, nullable=False)
    date_fin: Mapped[Date] = mapped_column(Date, nullable=False)
    motif: Mapped[str | None] = mapped_column(Text)
    statut: Mapped[str] = mapped_column(String(20), default="en_attente")
    approuve_par: Mapped[int | None] = mapped_column(
        ForeignKey("utilisateurs.id_utilisateur")
    )
    approuve_le: Mapped[DateTime | None] = mapped_column(DateTime)
    cree_le: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    approuve_par_user: Mapped["Utilisateur | None"] = relationship("Utilisateur")
    employe: Mapped["Employe"] = relationship(back_populates="demandes_conge")


# ---------- Banques de vacances ----------
class BanqueVacances(Base):
    __tablename__ = "banques_vacances"
    id_banque: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_employe: Mapped[int] = mapped_column(
        ForeignKey("employes.id_employe"), nullable=False, unique=True
    )
    solde_actuel: Mapped[float] = mapped_column(Numeric(6, 2), default=0)
    renouvellement: Mapped[Date | None] = mapped_column(Date)
    annee: Mapped[int | None] = mapped_column(Integer)
    employe: Mapped["Employe"] = relationship(back_populates="banque_vacances")


# ---------- Banques de maladie ----------
class BanqueMaladie(Base):
    __tablename__ = "banques_maladie"
    id_banque: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_employe: Mapped[int] = mapped_column(
        ForeignKey("employes.id_employe"), nullable=False, unique=True
    )
    solde_actuel: Mapped[float] = mapped_column(Numeric(6, 2), default=0)
    renouvellement: Mapped[Date | None] = mapped_column(Date)
    annee: Mapped[int | None] = mapped_column(Integer)
    employe: Mapped["Employe"] = relationship(back_populates="banque_maladie")


# ---------- Poincons (journal d'evenements de pointage) ----------
class Poincon(Base):
    __tablename__ = "poincons"
    id_poincon: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_utilisateur: Mapped[int] = mapped_column(
        ForeignKey("utilisateurs.id_utilisateur"), nullable=False
    )
    type_poincon: Mapped[str] = mapped_column(
        String(10), nullable=False
    )  # "entree" | "sortie"
    horodatage: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

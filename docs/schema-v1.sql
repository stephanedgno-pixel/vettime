-- ============================================================
-- VetTime — Schéma de données commenté (v1)
-- Jalon 2 : Architecture et données
-- ============================================================
-- But : ce script crée le modèle relationnel PostgreSQL. Chaque table et
-- chaque champ sont commentés. Les relations (clés étrangères) sont explicites.
-- Convention : clés primaires = id_<table> (SERIAL). Tout est en français
-- dans les noms de colonnes pour rester lisible pour la cliente.
--
-- Loi 25 (dès la conception) : on minimise les données personnelles.
-- Aucun champ sensible superflu (ex: pas de numéro d'assurance sociale ici).
-- Le consentement et la rétention seront documentés dans un ADR dédié.
--
-- [À VALIDER CLIENTE] = point à confirmer avec la propriétaire des cliniques
-- (voir docs/questions-blanche.md) avant de figer le schéma.
-- ============================================================

-- ---------- Auth & rôles (issue #1) ----------
-- Gère qui peut se connecter et avec quel niveau d'accès.

CREATE TABLE roles (
    id_role      SERIAL PRIMARY KEY,
    nom          VARCHAR(30) NOT NULL UNIQUE,  -- 'employe', 'gerant', 'admin'
    description  VARCHAR(100),
    cree_le      TIMESTAMP NOT NULL DEFAULT NOW()
);
-- Relation : 1 rôle -> plusieurs utilisateurs (utilisateurs.id_role)

CREATE TABLE utilisateurs (
    id_utilisateur      SERIAL PRIMARY KEY,
    email               VARCHAR(100) NOT NULL UNIQUE,       -- identifiant de connexion
    mot_de_passe_hash   VARCHAR(255) NOT NULL,             -- bcrypt, JAMAIS en clair
    id_role             INT NOT NULL REFERENCES roles(id_role),
    nom_complet         VARCHAR(100),
    actif               BOOLEAN NOT NULL DEFAULT TRUE,     -- compte désactivable sans suppression
    cree_le             TIMESTAMP NOT NULL DEFAULT NOW(),
    modifie_le          TIMESTAMP
);
-- Relation : utilisateurs.id_role -> roles.id_role

-- ---------- Référence : statuts d'une journée ----------
-- Qualifie la nature d'une journée ou d'un pointage.

CREATE TABLE statuts_journee (
    id_statut   SERIAL PRIMARY KEY,
    libelle     VARCHAR(50) NOT NULL  -- 'Travail Normal', 'Garde Clinique', 'Astreinte Domicile', 'Congé', 'Maladie'
);
-- [À VALIDER CLIENTE] : confirmer la liste complète des statuts.

-- ---------- Employés (RH) ----------
-- Dossier personnel de l'employé. Lié à un compte utilisateur (auth).

CREATE TABLE employes (
    id_employe              SERIAL PRIMARY KEY,
    utilisateur_id          INT REFERENCES utilisateurs(id_utilisateur),  -- lien auth (NULL si pas encore de compte)
    nom                     VARCHAR(50) NOT NULL,
    prenom                  VARCHAR(50) NOT NULL,
    poste                   VARCHAR(50),  -- 'Vétérinaire', 'ASV', 'Secrétaire'
    heures_contrat_semaine  DECIMAL(4,2)  -- ex: 39.00 — base du calcul des heures supplémentaires
);
-- Relation : employes.utilisateur_id -> utilisateurs.id_utilisateur (1:1 souhaité)
-- Relation : employes.id_employe -> pointages.id_employe, horaires.id_employe, demandes_conge.id_employe, banques.*.id_employe

-- ---------- Pointages (attendance — cœur du totalisateur) ----------
-- Une ligne par journée travaillée. Champs TIME nullable pour le punch ouvert.

CREATE TABLE pointages (
    id_pointage   SERIAL PRIMARY KEY,
    id_employe    INT NOT NULL REFERENCES employes(id_employe),
    date_jour     DATE NOT NULL,
    arrivee_matin TIME,        -- nullable : rempli à l'arrivée
    debut_diner   TIME,        -- nullable
    fin_diner     TIME,        -- nullable
    depart_soir   TIME,        -- nullable : rempli au départ (punch ouvert)
    id_statut     INT REFERENCES statuts_journee(id_statut),
    -- [À VENIR #7/#9] : corrige_par, corrige_le, est_discordance, approuve_admin
    UNIQUE(id_employe, date_jour)   -- pas 2 pointages le même jour
);
-- Relation : pointages.id_employe -> employes.id_employe
-- Relation : pointages.id_statut -> statuts_journee.id_statut
-- Heures travaillées = (depart_soir - arrivee_matin) - (fin_diner - debut_diner)

-- ---------- Jours fériés (paie Québec) ----------
-- Indemnité payée si absent ; majoration si travaillé.

CREATE TABLE jours_feries (
    id_jour_ferie   SERIAL PRIMARY KEY,
    date_jour       DATE NOT NULL UNIQUE,
    nom             VARCHAR(60) NOT NULL,       -- 'Noël', 'Jour de l'An', 'Action de grâce'
    taux_majoration DECIMAL(3,2),               -- 1.50 = temps et demi, 2.00 = double, NULL = fermé
    indemnite_payee BOOLEAN NOT NULL DEFAULT TRUE  -- si absent ce jour, l'employé reçoit l'indemnité
);
-- [À VALIDER CLIENTE] : taux par jour (1.5x vs 2x), jours fermés vs ouverts.
-- Pas de FK : table de référence consultée par la logique de paie.

-- ---------- Verrouillage des périodes (sécurité paie) ----------
-- Règle métier : FastAPI refuse toute modif de pointage dans une période verrouillée.

CREATE TABLE periodes_verrouillage (
    id_periode      SERIAL PRIMARY KEY,
    date_debut      DATE NOT NULL,   -- début de quinzaine
    date_fin        DATE NOT NULL,   -- fin de quinzaine
    verrouillee     BOOLEAN NOT NULL DEFAULT FALSE,
    verrouillee_par INT REFERENCES utilisateurs(id_utilisateur),
    verrouillee_le  TIMESTAMP
);
-- [À VALIDER CLIENTE] : période = quinzaine ? Qui peut déverrouiller (admin seulement) ?
-- Relation : periodes_verrouillage.verrouillee_par -> utilisateurs.id_utilisateur

-- ---------- Horaire planifié (issues #3/#6) [PROPOSÉ] ----------
-- Le QUAND prévu (vs pointages = le QUAND réel). Sert aux discordances (#9).

CREATE TABLE horaires (
    id_horaire  SERIAL PRIMARY KEY,
    id_employe  INT NOT NULL REFERENCES employes(id_employe),
    date_jour   DATE NOT NULL,
    heure_debut TIME,
    heure_fin   TIME,
    id_statut   INT REFERENCES statuts_journee(id_statut),
    UNIQUE(id_employe, date_jour)
);
-- Relation : horaires.id_employe -> employes.id_employe
-- Discordance (#9) = ecart entre horaires (prévu) et pointages (réel)

-- ---------- Demandes de congé (issues #4/#5) [PROPOSÉ] ----------
CREATE TABLE demandes_conge (
    id_demande   SERIAL PRIMARY KEY,
    id_employe   INT NOT NULL REFERENCES employes(id_employe),
    type_conge   VARCHAR(30) NOT NULL,  -- 'vacances', 'maladie', 'personnel'
    date_debut   DATE NOT NULL,
    date_fin     DATE NOT NULL,
    motif        TEXT,
    statut       VARCHAR(20) NOT NULL DEFAULT 'en_attente',  -- 'en_attente', 'approuve', 'refuse'
    approuve_par INT REFERENCES utilisateurs(id_utilisateur),
    approuve_le  TIMESTAMP,
    cree_le      TIMESTAMP NOT NULL DEFAULT NOW()
);
-- Relation : demandes_conge.id_employe -> employes.id_employe
-- Relation : demandes_conge.approuve_par -> utilisateurs.id_utilisateur

-- ---------- Banques de vacances (issue #10) [PROPOSÉ] ----------
-- Solde d'heures de vacances, renouvelable ~1er mai.

CREATE TABLE banques_vacances (
    id_banque     SERIAL PRIMARY KEY,
    id_employe    INT NOT NULL REFERENCES employes(id_employe) UNIQUE,
    solde_actuel  DECIMAL(6,2) NOT NULL DEFAULT 0,
    renouvellement DATE,  -- ~1er mai
    annee         INT
);
-- [À VALIDER CLIENTE] : reset le 1er mai ? solde reporté ou perdu ?
-- Relation : banques_vacances.id_employe -> employes.id_employe (1:1)

-- ---------- Banques de maladie (issue #11) [PROPOSÉ] ----------
-- Solde d'heures de maladie, renouvelable ~1er janvier.

CREATE TABLE banques_maladie (
    id_banque     SERIAL PRIMARY KEY,
    id_employe    INT NOT NULL REFERENCES employes(id_employe) UNIQUE,
    solde_actuel  DECIMAL(6,2) NOT NULL DEFAULT 0,
    renouvellement DATE,  -- ~1er janvier
    annee         INT
);
-- [À VALIDER CLIENTE] : reset le 1er janvier ?
-- Relation : banques_maladie.id_employe -> employes.id_employe (1:1)

-- ============================================================
-- Résumé des relations (FK) :
--   utilisateurs.id_role        -> roles.id_role
--   employes.utilisateur_id     -> utilisateurs.id_utilisateur
--   pointages.id_employe        -> employes.id_employe
--   pointages.id_statut         -> statuts_journee.id_statut
--   horaires.id_employe         -> employes.id_employe
--   demandes_conge.id_employe   -> employes.id_employe
--   demandes_conge.approuve_par -> utilisateurs.id_utilisateur
--   banques_vacances.id_employe  -> employes.id_employe
--   banques_maladie.id_employe   -> employes.id_employe
--   periodes_verrouillage.verrouillee_par -> utilisateurs.id_utilisateur
--   (jours_feries = table de référence autonome, consultée par la paie)
-- ============================================================

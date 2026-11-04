-- ============================================================
-- VetTime — Schéma de données commenté (v1.1)
-- Jalon 2 : Architecture et données
-- ============================================================
-- Statut : v1.1 — raffiné après validation de la cliente (propriétaire
-- de clinique vétérinaire), 2026-11-03. Les parties [VALIDÉ CLIENTE]
-- reflètent ses réponses ; [PROPOSÉ] = à confirmer.
--
-- CONVENTIONS
--   - Clés primaires : SERIAL (INT auto-incrément), nommées id_xxx.
--   - Références : INT + FOREIGN KEY explicite.
--   - Horodatage : TIMESTAMP (heure serveur, timezone locale Québec).
--   - Pas d'UUID (simplicité MVP).
--
-- LOI 25 (dès la conception)
--   - minimisation : on ne stocke que les données nécessaires à la paie ;
--   - consentement : à documenter (champ prévu si requis) ;
--   - rétention : données de paie conservées selon normes comptables (7 ans).
--
-- ============================================================
-- RÈGLES DE PAIE — VALIDÉES CLIENTE (2026-11-03)
-- ============================================================
--  1. Paie aux 2 semaines (quinzaine). Verrou après export comptable.
--  2. Heures supplémentaires : taux 1.5x au-delà de 40 h/semaine (hebdo).
--  3. Jours fériés : clinique FERMÉE, personne ne travaille. Indemnité
--     légale QC versée (calculée sur les semaines précédentes). Aucune
--     majoration (pas de travail ce jour-là).
--  4. Banque vacances : au renouvellement (~1er mai), solde REPORTÉ.
--  5. Banque maladie : au renouvellement (~1er janvier), solde PAYÉ si
--     inutilisé (cash-out), sinon perdu.
--  6. Correction après verrou : reportée à la paie suivante (heures
--     ajoutées au prochain traitement). Toute modification/discrepance
--     approuvée par admin OU gérant (jamais par l'employé seul).
--  7. Heures prévues varient par employé et d'une semaine à l'autre
--     (planifiées dans horaires).
-- ============================================================

-- ---------- Auth & rôles (issue #1) ----------
CREATE TABLE roles (
    id_role      SERIAL PRIMARY KEY,
    nom          VARCHAR(30) NOT NULL UNIQUE,  -- employe, gerant, admin
    description  VARCHAR(100),
    cree_le      TIMESTAMP NOT NULL DEFAULT NOW()
);
-- [VALIDÉ CLIENTE] rôles pertinents : employe, gerant (gestionnaire), admin.

CREATE TABLE utilisateurs (
    id_utilisateur      SERIAL PRIMARY KEY,
    email               VARCHAR(100) NOT NULL UNIQUE,
    mot_de_passe_hash   VARCHAR(255) NOT NULL,  -- bcrypt, JAMAIS en clair
    id_role             INT NOT NULL REFERENCES roles(id_role),
    nom_complet         VARCHAR(100),
    actif               BOOLEAN NOT NULL DEFAULT TRUE,
    cree_le             TIMESTAMP NOT NULL DEFAULT NOW(),
    modifie_le          TIMESTAMP
);

-- ---------- Référence ----------
CREATE TABLE statuts_journee (
    id_statut   SERIAL PRIMARY KEY,
    libelle     VARCHAR(50) NOT NULL  -- [VALIDÉ CLIENTE] 'Travail', 'Congé', 'Maladie'
);
-- [VALIDÉ CLIENTE] 3 statuts de journée seulement : Travail, Congé, Maladie.
-- Congé = journée de vacances (peut déduire banques_vacances) ; Maladie =
-- congé de maladie (banques_maladie). Garde/Astreinte non retenues.

-- ---------- Employés (RH) ----------
CREATE TABLE employes (
    id_employe              SERIAL PRIMARY KEY,
    utilisateur_id          INT REFERENCES utilisateurs(id_utilisateur),
    nom                     VARCHAR(50) NOT NULL,
    prenom                  VARCHAR(50) NOT NULL,
    poste                   VARCHAR(50),  -- [VALIDÉ CLIENTE] vétérinaire, technicienne, animalière, réceptionniste, gestionnaire
    heures_contrat_semaine  DECIMAL(4,2)  -- [VALIDÉ CLIENTE] valeur nominale; le réel est planifié dans horaires (varie / sem.)
);

-- ---------- Pointages (attendance) ----------
CREATE TABLE pointages (
    id_pointage     SERIAL PRIMARY KEY,
    id_employe      INT NOT NULL REFERENCES employes(id_employe),
    date_jour       DATE NOT NULL,
    arrivee_matin   TIME,
    debut_diner     TIME,
    fin_diner       TIME,
    depart_soir     TIME,
    id_statut       INT REFERENCES statuts_journee(id_statut),
    -- [VALIDÉ CLIENTE] Heures sup : 1.5x > 40h/sem (calcul hebdo).
    -- Champs à venir (#7/#9) : corrige_par, corrige_le, est_discordance, approuve_admin
    UNIQUE(id_employe, date_jour)
);

-- ---------- Jours fériés (paie QC) ----------
CREATE TABLE jours_feries (
    id_jour_ferie   SERIAL PRIMARY KEY,
    date_jour       DATE NOT NULL UNIQUE,
    nom             VARCHAR(60) NOT NULL,
    indemnite_payee BOOLEAN NOT NULL DEFAULT TRUE  -- clinique FERMÉE, indemnité légale QC
);
-- [VALIDÉ CLIENTE] Clinique fermée les jours fériés, personne ne travaille.
-- taux_majoration SUPPRIMÉ : aucun travail ce jour → pas de majoration.
-- L'indemnité est calculée selon les règles QC (semaines précédentes).

-- ---------- Verrouillage périodes (sécurité paie) ----------
CREATE TABLE periodes_verrouillage (
    id_periode      SERIAL PRIMARY KEY,
    date_debut      DATE NOT NULL,   -- [VALIDÉ CLIENTE] quinzaine (2 sem.)
    date_fin        DATE NOT NULL,
    verrouillee     BOOLEAN NOT NULL DEFAULT FALSE,
    verrouillee_par INT REFERENCES utilisateurs(id_utilisateur),
    verrouillee_le  TIMESTAMP
);
-- [VALIDÉ CLIENTE] Paie 2 semaines. Après export comptable -> verrou.
-- Correction post-verrou : reportée à la paie suivante (heures ajoutées
-- au prochain traitement). Modif/discrepance approuvée par admin OU gérant.

-- ---------- Horaire planifié (issues #3/#6) [PROPOSÉ] ----------
CREATE TABLE horaires (
    id_horaire   SERIAL PRIMARY KEY,
    id_employe   INT NOT NULL REFERENCES employes(id_employe),
    date_jour    DATE NOT NULL,
    heure_debut  TIME,
    heure_fin    TIME,
    id_statut    INT REFERENCES statuts_journee(id_statut),
    UNIQUE(id_employe, date_jour)
);
-- [VALIDÉ CLIENTE] Heures prévues varient / employé et / semaine.

-- ---------- Demandes de congé (issues #4/#5) [PROPOSÉ] ----------
CREATE TABLE demandes_conge (
    id_demande   SERIAL PRIMARY KEY,
    id_employe   INT NOT NULL REFERENCES employes(id_employe),
    type_conge   VARCHAR(30) NOT NULL,  -- vacances (banque), maladie (banque)
    date_debut   DATE NOT NULL,
    date_fin     DATE NOT NULL,
    motif        TEXT,
    statut       VARCHAR(20) NOT NULL DEFAULT 'en_attente',  -- en_attente, approuve, refuse
    approuve_par INT REFERENCES utilisateurs(id_utilisateur),
    approuve_le  TIMESTAMP,
    cree_le      TIMESTAMP NOT NULL DEFAULT NOW()
);
-- [VALIDÉ CLIENTE] Approbation par admin OU gérant (règle #6).

-- ---------- Banques de vacances (issue #10) [PROPOSÉ] ----------
CREATE TABLE banques_vacances (
    id_banque     SERIAL PRIMARY KEY,
    id_employe    INT NOT NULL REFERENCES employes(id_employe) UNIQUE,
    solde_actuel  DECIMAL(6,2) NOT NULL DEFAULT 0,
    renouvellement DATE,  -- ~1er mai
    annee         INT
);
-- [VALIDÉ CLIENTE] Renouvellement (~1er mai) : solde REPORTÉ (carry-over).

-- ---------- Banques de maladie (issue #11) [PROPOSÉ] ----------
CREATE TABLE banques_maladie (
    id_banque     SERIAL PRIMARY KEY,
    id_employe    INT NOT NULL REFERENCES employes(id_employe) UNIQUE,
    solde_actuel  DECIMAL(6,2) NOT NULL DEFAULT 0,
    renouvellement DATE,  -- ~1er janvier
    annee         INT
);
-- [VALIDÉ CLIENTE] Renouvellement (~1er janvier) : solde PAYÉ si inutilisé
-- (cash-out), sinon perdu.

-- ============================================================
-- RELATIONS (résumé)
--   utilisateurs 1—1 employes.utilisateur_id
--   roles 1—N utilisateurs.id_role
--   employes 1—N pointages / horaires / demandes_conge / banques_*
--   statuts_journee 1—N pointages / horaires
--   utilisateurs 1—N periodes_verrouillage.verrouillee_par / demandes_conge.approuve_par
--   (jours_feries est indépendant : consulté par la logique de paie)
-- ============================================================
-- Migration v1.2 — Ledger des banques (ADR-006)
-- Répond à la critique du professeur : les banques de congés ne gardent ni
-- historique ni mouvements. Désormais, toute variation de solde est un
-- mouvement tracé, et le solde = SUM(montant) (reconstructible et auditable).
--
-- Prérequis : schema-v1.sql déjà appliqué (tables employes, demandes_conge,
-- utilisateurs, banques_vacances, banques_maladie existent).
-- Post-migration : exécuter seed_banques.py pour amorcer les mouvements
-- 'initial' à partir des soldes actuels existants.

CREATE TABLE mouvements_banque (
    id_mouvement     SERIAL PRIMARY KEY,
    id_employe       INT NOT NULL REFERENCES employes(id_employe),
    type_banque      VARCHAR(10) NOT NULL
                     CHECK (type_banque IN ('vacances', 'maladie')),
    type_mouvement   VARCHAR(15) NOT NULL
                     CHECK (type_mouvement IN
                         ('accumulation', 'utilisation', 'ajustement',
                          'cash_out', 'renouvellement', 'initial')),
    montant          DECIMAL(6,2) NOT NULL,
    solde_apres      DECIMAL(6,2) NOT NULL,
    date_mouvement   TIMESTAMP NOT NULL DEFAULT NOW(),
    id_demande       INT REFERENCES demandes_conge(id_demande),
    cree_par         INT REFERENCES utilisateurs(id_utilisateur),
    note             VARCHAR(200),
    UNIQUE (id_employe, type_banque, date_mouvement, type_mouvement)
);

CREATE INDEX idx_mouv_employe_banque
    ON mouvements_banque (id_employe, type_banque, date_mouvement);

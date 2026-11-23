# VetTime — Jalon 2 : Architecture et données (document de remise)

*Projet fil rouge INF1410 (TÉLUQ) · Pondération : 15 % · Livrable après le module 3.*

## Liens vers les livrables

- **Dépot de code** : https://github.com/stephanedgno-pixel/vettime
- **Site (GitHub Pages)** : https://stephanedgno-pixel.github.io/vettime/
- **Blogue technique 1** : `docs/blogue-technique-1.md`
- **Blogue technique 2** : `docs/blogue-technique-2.md`
- **Schéma de données commenté** : `docs/schema-v1.sql`
- **ADR-001 / 002 / 003 / 004 / 005** : `docs/adr/`
- **Transcriptions de sessions IA (T1–T4)** : `docs/transcriptions-ia.md`
- **Synthèse des interactions IA** : `docs/ia-interactions.md`
- **Plan Jalon 2** : `docs/jalon2-plan.md`
- **Problématique** : `docs/problematique.md`

## Ce qui a été livré (Jalon 2)

### 1. ADRs (`docs/adr/`)
- **ADR-001** — Framework web : FastAPI + Jinja2 + HTMX (rejet de React SPA pour éviter la complexité frontend inutile).
- **ADR-002** — Base de données : PostgreSQL (rejet de SQLite/Mongo ; intégrité référentielle, rôles, contraintes).
- **ADR-003** — Banques de congés/maladie (suivi des soldes, report ~1er mai, cash-out ~1er janvier).
- **ADR-004** — Authentification : sessions `httpOnly` + bcrypt + CSRF (rejet JWT Bearer), aligné avec le README.
- **ADR-005** — Organisation du code : couches (main/app, modèles ORM, database, tests), modèles ↔ schéma en miroir.

### 2. Schéma de données commenté (`docs/schema-v1.sql`)
- **11 tables** mappées en ORM SQLAlchemy 2.0 (`app/models.py`), vérifiées par un test automatisé (`test_onze_tables`).
- **Règles de paie validées avec la cliente** (propriétaire de clinique) le 2026-11-03 : quinzaine, 1.5× > 40 h, jours fériés fermés, banques vacances/maladie.
- **Loi 25** : minimisation des données dès la conception (aucun surplus), rétention 7 ans gérée à l'export comptable.

### 3. Blogue technique 2 (`docs/blogue-technique-2.md`)
- Décision architecturale + contexte + alternatives rejetées.
- **Obstacle concret résolu** : encodage du mot de passe de base de données (`#` en clair côté SQL vs `%23` encodé côté URL/`.env`) — documenté dans `ia-interactions.md` (#5).
- Ce que le schéma révèle du domaine vétérinaire (paie, congés, banques, verrouillage).

### 4. Évolution du board (GitHub Issues)
- **12 issues** ouvrant le domaine (authentification, horaires, congés, banques, rapports, multi-clinique).
- Le design est figé dans le schéma ; l'implémentation (CRUD/UI) est planifiée en Jalon 3, avec fermeture progressive des issues.

## Démonstration et qualité

- Application déployée (Docker Compose + Cloudflare Tunnel) ; aucune installation pour les correcteurs.
- **CI GitHub Actions** : `pytest` (tests) + `ruff` (lint) + build Docker à chaque `git push`.
- **Transparence IA** : transcriptions brutes (T1–T4) + synthèse ; l'étudiant a validé chaque artefact (tests, diagnostic, distinctions) — usage critique, pas copie aveugle.

## Trace de l'usage de l'IA

Conformément au cadre du cours, l'IA a servi d'outil d'aide (génération de code ORM, explications, diagnostic), et l'étudiant a gardé le contrôle : vérification par tests, diagnostic d'échecs, et compréhension des leçons (ex. encodage `#`/`%23`). Les mots de passe et secrets ne figurent jamais dans le dépôt (`.env` gitignoré, rôles tournés).

## Problematique

L'enonce formel du probleme adresse par VetTime (contexte, douleur client, solution)
est documente dans [docs/problematique.md](docs/problematique.md).

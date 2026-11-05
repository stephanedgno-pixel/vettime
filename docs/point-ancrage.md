# Point d'ancrage — Jalon 2 (2026-11-05)

> Checkpoint pour reprendre la session. État RÉEL du projet VetTime à la fin de la présente session.

## Livrables Jalon 2
| Livrable | État |
|---|---|
| Schéma SQL v1.1 (11 tables, validé cliente) | ✅ dans repo |
| 3 ADRs (`docs/adr/001-003`) | ✅ créés, **à pousser** |
| Blogue technique 2 (`docs/blogue-technique-2.md`) | ✅ écrit (prose via Copilot, contenu validé par l'étudiant), **à pousser** |
| Projects board | ⏳ optionnel solo |
| Transcriptions gist (IA) | ⏳ J4 |

## Étape 4 — FastAPI ↔ PostgreSQL
- `app/database.py` créé (engine + SessionLocal + get_db). ✅
- `.env` créé (**gitignored**) : `DATABASE_URL=postgresql+psycopg2://vettime:***@127.0.0.1:5432/vettime`. ✅
- Dépendances : `sqlalchemy`, `psycopg2-binary`, `python-dotenv` (via uv). ✅
- Connexion prouvée : `engine.connect().execute(text("SELECT 1")).scalar()` → `1`. ✅
- **Reste (4b)** : route `/health/db` dans `app/main.py` utilisant `get_db` + test pytest.

## Décisions techniques clés (à connaître pour l'entretien)
- **Pilote DB** : `psycopg2-binary`. SQLAlchemy 2.1.8 + psycopg v3.3.8 avaient un bug `bytes`/`str` ; en 2.1, `postgresql://` pointe par défaut vers le dialecte **v3** → URL explicite `postgresql+psycopg2://`.
- **Mot de passe** : `#` encodé en `%23` dans l'URL (sinon tronqué à `#`). `.env` gitignored, **jamais committé**. Mot de passe caviardé dans toute la doc.
- **pytest** : restauré via `uv sync --extra dev` (retiré en cascade par `uv remove psycopg`).
- **Accès infra** : clé SSH `ct_key` (`~/.ssh`) donne accès direct au ThinkCentre (192.168.10.131). L'IA s'en sert pour vérifier/déboguer à distance (voir `ia-interactions.md`).
- **Loi 25** : minimisation (aucun surplus), hashage mots de passe, rétention 7 ans — documenté dans ADR + blogue 2.

## Prochaine session
1. **Finir 4b** : route `/health/db` dans `app/main.py` (utilise `get_db`) + test pytest.
2. Mapper les 11 tables en modèles SQLAlchemy (ORM) dans `app/models.py`.
3. **Jalon 3** : auth (rôles employé/gérant/admin), CRUD pointages/congés, UI Jinja+HTMX, déploiement public (ThinkCentre + Cloudflare Tunnel).
4. Publier transcriptions gist IA (J4) + vidéos YouTube unlisted.

## Commandes de reprise
- ThinkCentre : `cd ~/audit && git pull` (après le push de cette session).
- Local Windows : `cd C:/Users/Utilisateur/vettime`.
- L'IA relira ce fichier + `ia-interactions.md` + `jalon2-plan.md` pour reprendre le fil.

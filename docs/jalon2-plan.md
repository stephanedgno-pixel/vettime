# Jalon 2 — Plan d'étapes (Architecture et données)

> Pondération : 15 % · Livrable après le module 3.
> Document de suivi du travail — à cocher au fur et à mesure.
> Le prof veut voir : ADRs, schéma de données commenté, blogue, évolution du board.

## Livrables du Jalon 2 (du cours)
1. 2-3 ADRs (docs/adr/) — framework, organisation du code, type de BD
2. Schéma de données commenté (tables, champs, relations) dans le dépôt
3. (équipe) Mise à jour du board Projects — optionnel solo, mais on le fait
4. Blogue technique 2 : décision architecturale + contexte + alternatives rejetées + obstacle concret résolu + ce que le schéma révèle du domaine

## Retours du Jalon 1 à intégrer (dès maintenant)
- ⏱️ **Commits réguliers** au fil de l'eau (pas en 3 soirées)
- 🔒 **Loi 25** dès la conception du modèle de données (consentement, minimisation)
- 📜 **Transcriptions de session** publiées (gist) liées au blogue
- 🧪 **Étendre les tests** (le prof voulait + qu'un seul test)
- 🌐 Blogue **rendu + hébergé** (GitHub Pages) ; remise en PDF rendu

## Étapes cibles

### ⬜ Étape 1 — Valider le domaine avec la cliente
- Prendre `docs/questions-blanche.md`, rencontrer la proprio, noter ses réponses
  (règles de paie, jours fériés, banques, verrouillage).
- Livrable : questions-blanche.md complété.

### ⬜ Étape 2 — Schéma de données commenté
- Enrichir `docs/schema-v1.sql` : commentaire par table/champ + relations (FK).
- Intégrer Loi 25 (consentement, minimisation).
- Setup PostgreSQL sur ThinkCentre + exécuter le schéma (le rendre réel).
- Livrable : `docs/schema-v1.sql` commenté + BD créée.

### ⬜ Étape 3 — ADRs (docs/adr/)
- ADR-001 : Framework web (FastAPI + Jinja/HTMX vs React SPA)
- ADR-002 : Base de données (PostgreSQL vs SQLite/Mongo)
- ADR-003 (recommandé) : organisation du code / couches
- Chaque ADR : contexte, décision, alternatives rejetées + pourquoi.
- Livrable : `docs/adr/adr-001.md`, `adr-002.md`, `adr-003.md`.

### ⬜ Étape 4 — Implémentation M2 (code réel)
- Connexion FastAPI ↔ PostgreSQL (SQLAlchemy ou psycopg).
- Modèles de base + premiers endpoints.
- Étendre les tests automatisés.
- Livrable : app fonctionnelle branchée sur la BD + tests verts.

### ⬜ Étape 5 — Blogue technique 2
- `docs/blogue-technique-2.md` : décision archi + contexte + alt. rejetées
  + obstacle concret J2 rencontré/résolu + ce que le schéma révèle du domaine.
- Publier 1-2 transcriptions de session (gist) et les lier.
- Livrable : blogue 2 + transcriptions.

### ⬜ Étape 6 — Board + remise
- Mise à jour Projects board (tâches J2).
- `docs/remise-jalon2.md` (PDF rendu) → ENA.
- Commits réguliers tout au long, puis push + remise.
- Livrable : board à jour + remise envoyée.

## Prochain départ
Commencer par **Étape 2** (commenter le schéma + setup PostgreSQL) en parallèle
de l'**Étape 1** (rencontre cliente) pour affiner.

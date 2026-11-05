# Interactions avec l'IA — dossier de suivi (INF1410)

> Document vivant. Il documente comment l'IA (Hermes) a été utilisée dans le
> développement de VetTime, à titre de « transcription de session » exigée par le
> cours. Il sera complété à chaque jalon. L'objectif n'est pas de tout consigner,
> mais de montrer une **sélection représentative** où l'IA a aidé, où elle a
> falli, et comment l'étudiant a gardé le contrôle et le sens critique.

## Outil utilisé

- **Hermes** (agent IA conversationnel), utilisé comme **tuteur et co-développeur**,
  explicitement **non** comme générateur de code aveugle.
- Règle adoptée : l'IA sert à *comprendre* et à *structurer* ; le code final est
  écrit/validé par l'étudiant.

## Principe d'usage (inspiré du cours)

Le cours distingue deux modes :
- *« Pourquoi cette requête est-elle si lente ? »* → laisse une compréhension.
- *« Écris-moi cette fonction »* → laisse une fonction (et un risque).

Nous avons visé le premier mode : questions de cadrage, d'architecture et de
diagnostic plutôt que délégation de production.

---

## Jalon 1 — exemples représentatifs

### 1. Pivot de projet (guidance, pas code)
- **Situation** : le projet initial (scanner/sécurité) bloquait (objections
  éthiques/légales du prof, hors périmètre du cours de génie logiciel).
- **Rôle de l'IA** : aider à reformuler le besoin, proposer une alternative
  alignée (VetTime, gestion des présences), valider que ça touche toutes les
  exigences du cours.
- **Décision prise par l'étudiant** : approuver le pivot vers VetTime après
  discussion avec le professeur.

### 2. Débogage de la CI (diagnostic + correction)
- **Symptôme** : pipeline rouge `Failed to spawn: pytest` / `No such file`.
- **Diagnostic de l'IA** : `pytest` était en `[project.optional-dependencies].dev`,
  et `uv sync` seul ne l'installe pas ; il fallait `uv sync --extra dev`.
- **Leçon retenue** : distinction entre dépendances de production et *dev-extras*
  sous `uv` — point de compréhension, pas juste un correctif copié.

### 3. Choix technique (explication, puis décision)
- **Sujet** : FastAPI + Jinja2 + HTMX (server-rendered) vs React SPA.
- **Rôle de l'IA** : expliquer les enjeux (rendu serveur vs SPA, où va l'effort
  de développement, adéquation avec les objectifs du cours).
- **Décision** : l'étudiant a choisi le rendu serveur pour concentrer l'effort
  sur architecture / tests / déploiement / observabilité.

### 4. Erreurs de l'IA (évaluation critique — important)
L'IA n'a pas toujours eu raison ; l'étudiant a dû corriger :
- **Analyse d'image** : a manqué des labels de priorité sur 2 issues GitHub →
  l'étudiant a vérifié et ajouté `priority: medium` aux banques de congés/maladie.
- **Cohérence textuelle** : le texte sur Agendrix était désynchronisé entre le
  blogue et le README → l'étudiant a repéré l'incohérence et demandé la correction.
- **Fichier de test corrompu** : l'IA a diagnostiqué la ligne `workflofrom` dans
  `test_health.py` (héritage d'un heredoc mal copié) et proposé la réécriture.

Ces moments sont précisément ce que le cours veut voir : l'IA produit, l'étudiant
**évalue et corrige**.

---

## Réflexion (à faire évoluer chaque jalon)

- **Où l'IA a aidé** : structuration du dépôt, diagnostic de CI, recherche de
  bonnes pratiques, reformulation des exigences du cours.
- **Où elle a déçu** : analyse visuelle imparfaite, cohérence entre fichiers,
  tendance à « inventer » des détails mineurs.
- **Comment garder le sens critique** : vérifier chaque affirmation de l'IA, ne
  jamais déléguer la *compréhension*, et conserver la trace des corrections
  apportées (voir `docs/problemes.md`).

## Lien avec les entretiens de suivi

Ce dossier, combiné aux ADRs et au blogue final, sert de preuve d'un usage
**critique** de l'IA. Aux entretiens, l'étudiant devra être capable d'expliquer
*lui-même* chaque choix (ex. « pourquoi Postgres », « pourquoi sessions httpOnly
plutôt que JWT Bearer ») sans s'appuyer sur l'IA présente.

---

## Jalon 2 — PostgreSQL sur le ThinkCentre (session en cours)

*[À remplir au fil de l'eau — pas reconstruit après coup]*

Cette section documente, pour le Jalon 2, les **étapes** posées par l'étudiant et
les **questions** adressées à l'IA pour installer et configurer PostgreSQL sur le
ThinkCentre (Debian, 192.168.10.131), puis exécuter le schéma `docs/schema-v1.sql`.

### Collaboration avec l'IA — méthode pour les choix techniques

Pour le Jalon 2, j'ai travaillé avec l'assistant (Hermes) comme **collaborateur**, pas comme générateur. Trois dynamiques :

1. **Consultation** : je l'ai consulté pour les choix techniques structurants (framework web, base de données, portée du suivi des banques). Il m'a présenté les options de programmes disponibles et ce que chacune fait.
2. **Challenge** : je n'ai pas accepté ses suggestions telles quelles. J'ai corrigé l'assistant quand ses analyses étaient inexactes (ex. labels de priorité manquants sur des issues) et j'ai validé les hypothèses de modélisation **avec la cliente** plutôt que de le croire sur parole — ex. jours fériés : il supposait une majoration 1.5×/2× (jour ouvert), or la cliente a révélé que la clinique **ferme** → on a supprimé la colonne `taux_majoration` du schéma.
3. **Explication des options** : il m'a expliqué concrètement ce que fait chaque option (FastAPI+Jinja+HTMX vs SPA React ; PostgreSQL vs SQLite/MongoDB), ce qui m'a permis de trancher en comprenant, et de documenter dans les ADRs (docs/adr/).

J'ai aussi utilisé GitHub Copilot pour la rédaction en prose du blogue technique 2, mais j'ai validé le contenu et les décisions moi-même (les choix viennent de nos échanges et des ADRs).

### Questions posées à l'IA
- Comment exécuter le fichier `schema-v1.sql` dans la base PostgreSQL `vettime` ?

### Étapes réalisées
- Vérif `psql --version` → PostgreSQL 15.19 déjà installé (installation fraîche). Aucune installation requise.
- `ALTER ROLE vettime WITH PASSWORD '...'` pour corriger un mot de passe placeholder entré par erreur sur le rôle.
- `CREATE DATABASE vettime OWNER vettime` (si pas déjà créée).
- Transfert `schema-v1.sql` vers le ThinkCentre + exécution via `psql -f` pour créer les tables du schéma.
- Exécution réussie : 11 tables créées (roles, utilisateurs, statuts_journee, employes, pointages, jours_feries, periodes_verrouillage, horaires, demandes_conge, banques_vacances, banques_maladie).

### Débogage de la connexion FastAPI ↔ PostgreSQL (Étape 4)

Contexte : brancher l'app FastAPI sur la base VetTime (création de `app/database.py` + `.env` avec `DATABASE_URL`).

**Accès à l'infrastructure (SSH).** L'étudiant a configuré une clé SSH (`ct_key`) sur sa machine Windows, donnant à l'IA un accès **direct** au ThinkCentre (192.168.10.131) — pas seulement à sa machine locale. Première tentative de connexion : l'IA a reçu `Permission denied` car la clé n'était pas au nom par défaut ; l'étudiant a confirmé que la clé existait, et l'IA l'a alors spécifiée explicitement (`ssh -i ~/.ssh/ct_key`) — connexion réussie.

**Vérification sur place.** Avant de tester, l'IA a vérifié à distance que les fichiers étaient bien en place (`ls -la .env app/database.py`) et que les dépendances étaient installées (`import sqlalchemy, psycopg, dotenv` → `deps ok`).

**Test et diagnostic.** L'IA a exécuté un script de connexion (`engine.connect()` + `SELECT 1`), qui a révélé **4 erreurs successives**. Chaque erreur a été diagnostiquée à partir du traceback et corrigée à distance :

1. **`TypeError: cannot use a string pattern on a bytes-like object`** — Diagnostic : incompatibilité SQLAlchemy 2.1.8 + psycopg v3.3.8 (la version du serveur revient en `bytes`, SQLAlchemy plante). Correction : `uv remove psycopg && uv add psycopg2-binary`.
2. **`ModuleNotFoundError: No module named 'psycopg'`** — Diagnostic : en SQLAlchemy 2.1, `postgresql://` pointe par défaut vers le dialecte psycopg **v3** (retiré à l'étape 1). Correction : URL explicite `postgresql+psycopg2://`.
3. **Mot de passe tronqué (`#` dans l'URL)** — Diagnostic : `#` = fin des identifiants dans une URL ; un mot de passe contenant `#` est coupé avant ce caractère (ex. `M43pz4cx#...` → `M43pz4cx`). Correction : encoder `#` → `%23`.
4. **`pytest` disparu (cascade)** — Diagnostic : `uv remove psycopg` a aussi retiré les dépendances de test. Correction : `uv sync --extra dev`.

Résultat : `engine.connect().execute(text('SELECT 1')).scalar()` → `1`. Le pont fonctionne.

### Ce que l'IA a aidé / où elle a déçu
- **Aidé** : lecture de tracebacks, diagnostic de conflits de versions, proposition de corrections ciblées (changement de pilote DB, encodage d'URL, restauration de dépendances). Accès direct au ThinkCentre via la clé SSH `ct_key` : vérification des fichiers en place et déboguage à distance.
- **À noter** : l'IA applique les corrections, mais l'étudiant doit **valider et comprendre le « pourquoi »** (ex. pourquoi `postgresql+psycopg2://` et non `postgresql://`) — c'est ce qui sera interrogé à l'entretien.

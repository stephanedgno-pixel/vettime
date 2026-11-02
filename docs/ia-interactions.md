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

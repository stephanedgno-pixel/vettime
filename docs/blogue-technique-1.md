# Blogue technique — Entrée 1 : amorçage de VetTime

## Qui sont nos utilisateurs et quel problème résolvons-nous ?

VetTime vise les petites cliniques vétérinaires. Deux profils concrets :

- **Les employés** (vétérinaires, techniciens en santé animale, réception) qui pointent
  leurs heures de travail et consultent leur horaire.
- **Les gérants et propriétaires** qui planifient les quarts, corrigent les poinçons
  et valident les congés.

Le problème observé sur le terrain : dans une clinique, le suivi des présences se fait
**encore sur papier** (feuilles perdues, erreurs de saisie, correction lente) ; dans une
autre, un outil externe (Agendrix) est utilisé, mais il est trop cher à implanter pour une petite clinique de 10 employés et moins. Les données restent fragmentées et peu fiables.

VetTime centralise le punch, les horaires, les demandes de congé et les rapports dans
une seule application web transactionnelle. La propriétaire des cliniques a validé le
concept et ajouté des besoins réels : afficher en **gras les discordances entre l'horaire
planifié et les heures réellement travaillées** (approuvées par un administrateur), et
gérer des **banques de vacances** (renouvellement annuel ~1er mai) et de **maladie**
(renouvellement ~1er janvier).

## Quels sont nos premiers choix techniques et quelles alternatives avons-nous considérées ?

- **Langage** : Python (FastAPI). *Alternative* : Node.js / Express — écartée, Python
  étant plus accessible et FastAPI couvrant à la fois l'API et le rendu de templates.
- **Framework** : FastAPI + Jinja2 + HTMX (rendu côté serveur). *Alternative* : SPA
  React — rejetée car elle ajoute deux chaînes de build, du CORS et de la complexité
  inutile pour le MVP.
- **Base de données** : PostgreSQL (relationnelle, fiable en production). *Alternative* :
  SQLite en développement — écartée, on part directement sur Postgres pour coller à la
  cible de déploiement.
- **Hébergement** : ThinkCentre dédié + Docker Compose + Cloudflare Tunnel (accès public
  aux correcteurs sans installation). *Alternative* : VPS cloud — écartée pour garder le
  contrôle et limiter le coût.
- **CI** : GitHub Actions (lint + tests automatisés à chaque push).
- **Observabilité** : Grafana + Prometheus (module 5), traité en stretch.

## Qu'est-ce qui est encore incertain à ce stade ?

- Le **modèle de données** exact (rôles, poinçons, banques de congés/maladie) reste à
  concevoir.
- L'**authentification** (sessions sécurisées vs JWT) n'est pas encore tranchée.
- La **multi-clinique** est différée : trop lourde pour le MVP (une seule clinique visée
  au départ).
- Nous avons déjà rencontré et documenté plusieurs friction d'outillage (voir
  `docs/problemes.md`) : fichier de test corrompu par copier-coller, `pytest` absent en
  CI parce qu'il était déclaré en extra optionnel non installé par `uv sync`, et scope
  `workflow` manquant sur le token GitHub. Ces erreurs, loin d'être bloquantes, ont
  validé que la pipeline CI remplissait bien son rôle de filet de sécurité.

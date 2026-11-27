# VetTime

Plateforme web de gestion des présences, des horaires et des congés pour cliniques vétérinaires.

## Vision client

*Rédigé du point de vue des utilisateurs réels de VetTime : les équipes des cliniques vétérinaires.*

### Qui sont nos utilisateurs ?

VetTime s'adresse aux petites et moyennes cliniques vétérinaires, et plus précisément :

- **Les employés** (vétérinaires, techniciens en santé animale, réceptionnistes) qui pointent leurs heures et consultent leur horaire.
- **Les gérants** qui planifient les quarts, corrigent les poinçons et approuvent les congés.
- **Les propriétaires de clinique** qui veulent une vue d'ensemble multi-établissement et des données fiables pour la paie.

### Quel problème VetTime résout

Deux situations réelles :

- Dans une clinique, le suivi des présences se fait **encore sur papier**. Les feuilles se perdent, les erreurs de saisie sont fréquentes et corriger un poinçon prend du temps.
- Dans une autre, on utilise **Agendrix**, un outil externe, mais il est trop cher à implanter pour une petite clinique de 10 employés et moins.

Dans les deux cas, les données sont **fragmentées, peu fiables et difficiles à consolider**. Calculer les heures travaillées, les retards ou les heures supplémentaires devient une tâche manuelle sujette aux erreurs.

### La solution envisagée

VetTime est une **application web transactionnelle** qui centralise la gestion des présences :

- L'employé **pointe son entrée et sa sortie** en quelques clics, depuis n'importe quel poste.
- Le gérant **gère les horaires, corrige les poinçons et approuve les congés** dans la même interface.
- La clinique obtient des **rapports d'heures, de présence, de retards et de heures supplémentaires** automatiques et exportables.
- Les cliniques à **plusieurs établissements** gardent tout dans un seul système.

Le tout est **accessible en ligne, sans installation**, et les correcteurs du cours y accèdent directement.

### Pourquoi maintenant

Le besoin est réel et observé sur le terrain. Une solution légère, adaptée aux petites cliniques et moins coûteuse qu'un abonnement générique, comble un vide concret — tout en servant de terrain d'apprentissage pour les notions de génie logiciel du cours (authentification, base de données, déploiement, observabilité).

Le concept a déjà été validé auprès des propriétaires vétérinaires des cliniques visées, qui appuient le projet et confirment le besoin sur le terrain.

## Contexte

Le projet initial consistait à développer une plateforme d'audit/scanner de sécurité. Après
discussion avec le professeur, plusieurs enjeux ont été soulevés concernant l'autorisation de
scanner des systèmes tiers, les aspects légaux et les contraintes d'hébergement. L'idée a donc été
abandonnée au profit d'un projet plus aligné avec les objectifs du cours (génie logiciel).

Le nouveau projet répond à un besoin réel observé dans deux cliniques vétérinaires : une utilise
Agendrix pour la gestion des heures, tandis qu'une seconde effectue encore le suivi des présences
sur papier.

## Objectif

Développer une application web transactionnelle permettant aux employés de pointer leurs heures de
travail et aux gestionnaires de suivre les présences, gérer les horaires et approuver les demandes
de congé.

## Fonctionnalités MVP

### Authentification
- Création de compte
- Connexion / Déconnexion
- Gestion des rôles

### Employés
- Consultation de leur profil
- Consultation de leur horaire
- Consultation de leur historique d'heures

### Gestion des présences
- Punch In / Punch Out
- Historique des poinçons
- Calcul automatique des heures travaillées

### Gestion des congés
- Soumission d'une demande
- Approbation ou refus par un gestionnaire

### Gestion multi-clinique _(PROPOSÉ — hors périmètre MVP, absente du schéma v1)_
- Plusieurs cliniques
- Employés associés à une clinique

### Rapports
- Heures travaillées
- Présences
- Retards
- Heures supplémentaires

## Rôles

- **Employé** : pointer ses heures, voir son horaire, demander un congé
- **Gestionnaire** : gérer les horaires, corriger les poinçons, approuver les congés, consulter les rapports
- **Administrateur** : gérer les cliniques, gérer les utilisateurs, gérer les permissions

## Technologies retenues

| Couche | Technologie |
|--------|-------------|
| Frontend | Jinja2 + HTMX + Bootstrap |
| Backend | FastAPI |
| Base de données | PostgreSQL |
| Authentification | Sessions sécurisées en cookie httpOnly + bcrypt + protection CSRF |
| Tests | pytest + ruff (lint) |
| Intégration continue | GitHub Actions (pytest + lint + build Docker) |
| Conteneurisation | Docker Compose |
| Observabilité | Prometheus + Grafana |

### Authentification (détail)
- Mots de passe hachés avec bcrypt (jamais en clair)
- Sessions en cookie `httpOnly` + `Secure` + `SameSite`
- Tokens CSRF sur tous les formulaires HTMX (POST)
- JWT Bearer rejeté (voir ADR-004) — les sessions httpOnly suffisent pour du server-rendered

## Assurance qualité

- **Tests automatisés pytest dès le MVP** : auth, calcul d'heures, permissions par rôle
- **CI GitHub Actions** : pytest exécuté à chaque push — lint (ruff) + build Docker exécutés à chaque push
- **Pas de mot de passe en clair** : bcrypt obligatoire
- **Sessions httpOnly + CSRF** : protection contre le vol de session et le CSRF

## Déploiement

Infrastructure prévue (jalon M6, module 5) :
- ThinkCentre dédié (Docker Compose)
- Cloudflare Tunnel (URL publique, aucune installation pour les correcteurs)

L'application sera déployée (M6, module 5) puis accessible publiquement aux correcteurs.

## Architecture

```
Utilisateur (navigateur)
      │  HTTP (Jinja2 / HTMX)
      ▼
FastAPI (app web + API)
      │  SQL (psycopg2)
      ▼
PostgreSQL (données transactionnelles)
      │  expose /metrics
      ▼
Prometheus (scrape les métriques de FastAPI)
      │  requêtes PromQL
      ▼
Grafana (dashboards d'observabilité)
```

Note : Prometheus récupère les métriques exposées par FastAPI (pas directement
PostgreSQL). Grafana lit dans Prometheus pour afficher les tableaux de bord.

## Métriques d'observabilité (Grafana / Prometheus)

- Nombre de connexions
- Nombre de punchs
- Temps de réponse API (p95/p99)
- Taux d'erreurs
- Utilisateurs actifs

## Lien avec les objectifs du cours

Le projet couvre directement :
- Git et gestion de versions
- Architecture logicielle
- Développement API
- Base de données SQL
- Authentification et gestion des rôles
- Tests automatisés (pytest)
- Intégration continue (GitHub Actions)
- Déploiement web (Docker Compose + Cloudflare Tunnel)
- Observabilité (Grafana / Prometheus)
- Méthodologie Agile

## Pourquoi ce projet ?

- Répond à un besoin réel (2 cliniques)
- Véritables utilisateurs potentiels
- Testable en environnement professionnel
- Respecte toutes les exigences du cours
- Intègre plusieurs concepts de génie logiciel modernes sans complexité frontend inutile (pas de React SPA)

## Décision technique

**FastAPI + Jinja2 + HTMX + PostgreSQL + Docker Compose + Grafana**

Ce choix maximise le temps consacré à l'architecture, aux tests, au déploiement et à
l'observabilité — les objectifs principaux du cours — plutôt qu'à la complexité d'un SPA React.

## Fonctionnalités futures (hors MVP)

Ces fonctionnalités ne font pas partie du périmètre MVP et sont réservées à une
itération ultérieure si le temps le permet :

- **QR Code** pour punch rapide (bornes sur le plancher)
- **Notifications par courriel** (rappels de congé, approbations)
- **Export PDF** des feuilles de temps (pour l'employé)
- **Export Excel** pour la paie (pour le gestionnaire)
- **Géolocalisation optionnelle** lors du punch (horodatage de lieu)
- **Application mobile responsive** (PWA ou native)

## Ordonnancement (milestones)

- **M1** : Git + structure de dépôt + CI GitHub Actions + documentation
- **M2** : Modèle SQL (PostgreSQL) + connexion DB
- **M3** : Authentification + gestion des rôles
- **M4** : CRUD présences / horaires / congés
- **M5** : Rapports + gestion multi-clinique
- **M6** : Déploiement public + observabilité Grafana (module 5)

---

## Documentation du projet

- `docs/blogue-technique-1.md` et `docs/blogue-technique-2.md` : blogues techniques (récit du projet, décisions, réconciliation de l'authentification).
- `docs/transcriptions-ia.md` : transcriptions brutes des sessions de travail avec l'IA (setup PostgreSQL sur le ThinkCentre, affinement du schéma avec la cliente, débogage de la connexion FastAPI ↔ PostgreSQL).
- `docs/ia-interactions.md` : synthèse des interactions IA, décisions et leçons — notamment le **piège d'encodage `#`** : en clair côté SQL (`ALTER ROLE ... PASSWORD '...#...'`), encodé `%23` côté URL / `.env`.
- ADRs : décisions architecturales documentées (voir `docs/`).
- ADR-004 : authentification (sessions `httpOnly` + bcrypt + CSRF) — `docs/adr/adr-004.md`.
- ADR-005 : organisation du code (couches, modèles ORM, tests) — `docs/adr/adr-005.md`.

> Note de renommage : le dépôt et l'infrastructure portaient initialement le nom `audit` (héritage du projet de scanner de sécurité abandonné) ; ils ont été renommés `vettime` (pyproject, docker-compose, dossier, documentation).

## Modèle de données

- **11 tables** SQLAlchemy 2.0 (ORM) couvrant utilisateurs, rôles, présences, horaires, congés, etc.
- Schéma relationnel validé (clés étrangères, contraintes d'intégrité référentielle).
- Connexion DB gracieuse : `/health/db` renvoie `503` (au lieu de crasher) si PostgreSQL est injoignable.

## Confidentialité et Loi 25 (minimisation des données)

Conformément à la *Loi 25*, le modèle de données applique le principe de **minimisation** : seules les données strictement nécessaires au fonctionnement (présences, horaires, rôles, cliniques) sont collectées ; aucune donnée personnelle sensible superflue.

- Mots de passe hachés avec **bcrypt**, jamais en clair.
- Aucun mot de passe, clé ou secret n'est exposé dans la documentation ni le dépôt (`.env` gitignoré).

## Videos

- Enregistree le 2026-11-21 — Mettre en ligne des videos sur YouTube (acces correcteur) : https://youtu.be/lMnci8FpNdY

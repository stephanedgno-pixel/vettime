# VetTime

Plateforme web de gestion des présences, des horaires et des congés pour cliniques vétérinaires.

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

### Gestion multi-clinique
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
| Tests | pytest |
| Intégration continue | GitHub Actions |
| Conteneurisation | Docker Compose |
| Observabilité | Prometheus + Grafana |

### Authentification (détail)
- Mots de passe hachés avec bcrypt (jamais en clair)
- Sessions en cookie `httpOnly` + `Secure` + `SameSite`
- Tokens CSRF sur tous les formulaires HTMX (POST)
- JWT signé optionnel si API en bonus (sinon sessions suffisent pour du server-rendered)

## Assurance qualité

- **Tests automatisés pytest dès le MVP** : auth, calcul d'heures, permissions par rôle
- **CI GitHub Actions** : lint + pytest + build Docker exécutés à chaque push (module 2)
- **Pas de mot de passe en clair** : bcrypt obligatoire
- **Sessions httpOnly + CSRF** : protection contre le vol de session et le CSRF

## Déploiement

Infrastructure déjà disponible :
- ThinkCentre dédié (Docker Compose)
- Cloudflare Tunnel (URL publique, aucune installation pour les correcteurs)

L'application sera accessible publiquement aux correcteurs sans aucune installation.

## Architecture

```
Utilisateur (navigateur)
      │  HTTP (Jinja2 / HTMX)
      ▼
FastAPI (app web + API)
      │  SQL (psycopg)
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

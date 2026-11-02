# Journal des problématiques — Jalon 1

*Document de suivi des difficultés rencontrées lors de la mise en place de
l'environnement de développement VetTime (INF1410). Objectif : tracer les
frictions et les leçons tirées, comme demandé pour le blogue technique du
Jalon 1.*

## Contexte

Première mise en place de l'environnement : serveur dédié (ThinkCentre,
Debian), dépôt Git local, conteneurisation Docker, pipeline CI GitHub Actions.
Ces problèmes sont normaux à l'amorçage d'un projet et documentent
l'apprentissage des outils de génie logiciel.

## Problématiques

### 1. Connexion SSH — utilisateur incorrect
- **Symptôme** : `ssh root@192.168.10.131` → `Permission denied` (3 tentatives).
- **Cause** : le compte du serveur est `Silverwaffen`, pas `root`.
- **Solution** : `ssh Silverwaffen@192.168.10.131`.
- **Leçon** : vérifier le bon compte avant de supposer un problème réseau.

### 2. scp exécuté dans la mauvaise session
- **Symptôme** : `Could not resolve hostname c:`.
- **Cause** : la commande scp a été lancée à l'intérieur de la session SSH
  (côté Linux), qui a interprété `C:` comme un hôte.
- **Solution** : lancer scp depuis le terminal Windows (hors SSH).
- **Leçon** : distinguer ce qui s'exécute localement vs sur le serveur.

### 3. Format de chemin incompatible (MSYS vs Windows natif)
- **Symptôme** : `/c/Users/...` → `No such file or directory` avec le scp natif.
- **Cause** : le scp natif (`C:\Windows\System32\OpenSSH\scp.exe`) ne comprend
  pas le format Unix `/c/`.
- **Solution** : utiliser `C:/Users/...` (chemin Windows, slash droits).
- **Leçon** : adapter le format de chemin à l'outil utilisé.

### 4. Dossier de destination inexistant + mauvais emplacement
- **Symptôme** : `dest open ".../vettime/README.md": No such file or directory`.
- **Cause** : le dossier cible n'existait pas (scp ne crée pas le dossier
  parent) et le projet se trouvait déjà dans `~/audit`, pas `~/vettime`.
- **Solution** : réutiliser `~/audit` (scaffold existant compatible VetTime).
- **Leçon** : vérifier l'état réel du serveur avant de créer de nouveaux
  dossiers.

### 5. Plusieurs commandes Git sur une seule ligne
- **Symptôme** : `unknown switch 'm'`.
- **Cause** : `git add . git commit -m "..." git status` collés sur une ligne →
  interprétés comme un seul argument.
- **Solution** : une commande par ligne, ou `&&` pour enchaîner.
- **Leçon** : chaque commande shell est séparée par un saut de ligne ou `&&`.

### 6. Identité Git non configurée
- **Symptôme** : `Author identity unknown` / `empty ident name`.
- **Cause** : `user.name` et `user.email` jamais définis.
- **Solution** : `git config --global user.name` + `user.email`
  (email = compte GitHub pour lier les commits).
- **Leçon** : Git exige une identité traçable pour chaque commit
  (indispensable en travail d'équipe).

### 7. CLI `gh` absente
- **Symptôme** : `gh command not found` sur le serveur.
- **Cause** : GitHub CLI non installée sur le ThinkCentre.
- **Solution** : création du dépôt via l'interface web + token HTTPS
  (aucune installation requise).
- **Leçon** : plusieurs chemins mènent à GitHub ; le web UI est un fallback
  fiable.

### 8. Token PAT sans scope `workflow`
- **Symptôme** : push rejected — « refusing to allow a PAT to create or update
  workflow `.github/workflows/ci.yml` without `workflow` scope ».
- **Cause** : le scope `workflow` est requis pour modifier un fichier de CI.
- **Solution** : ajouter le scope `workflow` au token
  (Settings → Developer settings → Personal access tokens).
- **Leçon** : GitHub sépare les permissions ; pousser une CI exige un scope
  explicite (mesure anti-abus).

### 9. Fichier de test corrompu → échec CI

- **Symptôme** : la pipeline CI envoie un email « test fail » ; le test
  `test_health` ne passe pas.
- **Cause** : la première ligne de `tests/test_health.py` était corrompue —
  un fragment « workflo » (issu du mot « workflow » du `ci.yml`) était collé
  devant `from fastapi.testclient import TestClient`, créant une erreur de
  syntaxe. pytest ne pouvait pas collecter le test.
- **Solution** : réécriture propre du fichier (heredoc), puis `commit` + `push`
  → la CI repasse au vert.
- **Leçon** : un copier-coller accidentel suffit à corrompre un fichier et
  faire échouer toute la suite de tests en CI. La CI sert précisément à
  attraper ça. Vérifier localement (`uv run pytest`) avant de pousser évite
  un cycle rouge inutile.

### 10. pytest absent en CI (extra optionnel non installé)

- **Symptôme** : la CI échoue sur `uv run pytest` avec
  « Failed to spawn: pytest / No such file or directory » (exit 2).
- **Cause** : `pytest` était déclaré dans `[project.optional-dependencies]`
  (extra `dev`). Or, `uv sync` n'installe PAS les extras optionnels par
  défaut — seul `uv sync --extra dev` les installe. Donc pytest manquait
  dans le venv CI.
- **Solution** : changer `uv sync` pour `uv sync --extra dev` dans le
  `ci.yml` → pytest est installé, `uv run pytest` passe.
- **Leçon** : distinction entre dépendances principales et extras
  optionnels. `uv sync` seul n'installe pas les extras ; pour les dev
  deps, soit `--extra dev`, soit les déclarer dans `[dependency-groups]`
  (uv les installe par défaut). Bien déclarer les dépendances de test
  est au cœur de la gestion des dépendances (module 2).

## Bilan

Ces frictions sont typiques de la phase d'amorçage d'un projet. Aucune n'est
bloquante une fois comprise ; elles renforcent la maîtrise des outils
(SSH, transfert de fichiers, Git, GitHub, CI) au cœur du module 2 du cours.
Documenter ces étapes fait partie de la démarche de génie logiciel : on apprend
autant de ses erreurs d'outillage que de la conception elle-même.

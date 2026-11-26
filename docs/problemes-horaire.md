# Problematiques — Issue #3 (Horaire / heures cumulees)

*Journal des problemes rencontres pendant l'implementation de la consultation
d'horaire + heures cumulees. Format : Symptome / Cause / Solution / Lecon.*

## 1. Totalisateur : decision de scope (heures cumulees = issue #3)
- **Symptome** : l'utilisateur se demande si le "totalisateur" (somme des
  heures) fonctionnera et ou le placer.
- **Cause** : le user story #2 ne mentionnait que bouton + horodatage serveur +
  historique — pas le total. Le total semblait appartenir aux issues #7/#9 (paie).
- **Solution** : le user story #3 (« consulter mon horaire et mes heures
  cumulees ») inclut explicitement les heures cumulees → le totalisateur est
  implemente DANS #3 via `calculer_total_heures()` + `regrouper_par_jour()`.
  Prouve par **test pytest a donnees connues** (8h, 16h, entree sans sortie
  ignoree).
- **Lecon** : un test unitaire avec valeurs connues prouve un calcul (bien plus
  fiable que de cliquer dans le navigateur). Le scope d'une issue se definit par
  son user story, pas par intuition.

## 2. Lint I001 — import order oublie avant commit
- **Symptome** : `ruff check` → I001 sur `app/main.py` (import `app.heures`
  place apres `app.models` au lieu de avant), "4 fixable".
- **Cause** : j'ai ajoute l'import `from app.heures import ...` APRES
  `from app.models import ...`, puis commite SANS lancer `ruff --fix` au
  prealable → commit avec du lint casse (la CI aurait echoue).
- **Solution** : reordonne manuellement (`app.heures` avant `app.models`) +
  commit `style: ruff fix import order`.
- **Lecon** : TOUJOURS lancer `ruff --fix` PUIS `ruff check` **avant** `git
  commit`. Le format (`ruff format .`) ne corrige PAS l'ordre des imports
  (I001) — seul `ruff --fix` le fait.

## 3. `git pull` sur branche neuve echoue
- **Symptome** : `git pull` sur `feat/horaire` → "no tracking information".
- **Cause** : une nouvelle branche n'a pas de suivi distant tant qu'elle n'est
  pas poussee.
- **Solution** : 1re fois `git push -u origin feat/horaire` (cree la branche +
  suivi) ; ensuite `git push`/`git pull` simples.
- **Lecon** : sur une feature fraiche, on PUSH (pas pull) pour la 1re fois.

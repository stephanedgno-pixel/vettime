# Problématiques — Issue #2 (Pointage / punch)

*Journal des problèmes rencontrés pendant l'implémentation du pointage
(option B : journal d'événements `poincons`). Format : Symptôme / Cause /
Solution / Leçon.*

## 1. Ajout table `poincons` → test `assert 12 == 11` casse
- **Symptôme** : `pytest` échoue →
  `AssertionError: assert 12 == 11` dans `tests/test_models.py:6`.
- **Cause** : on a ajouté la table `poincons` (journal d'événements de
  pointage, issue #2, choix B), portant le total à **12 tables**. Le test
  attendait **11** (schéma v1.1).
- **Solution** : mis l'assertion à `== 12` (fonction renommée
  `test_douze_tables`), et documenté l'ajout ici.
- **Leçon** : à chaque ajout de table au schéma, **toujours** mettre à jour
  le test de décompte (`test_models.py`) ET le documenter.

## 2. Découverte : `pointages` existe déjà (feuille de temps quotidienne)
- **Symptôme** : tentative d'ajout d'un modèle `Pointage` → erreur ruff
  `F811 redefinition` (classe déjà définie ligne 71).
- **Cause** : le schéma v1.1 contient DÉJÀ une table `pointages` (arrivée /
  départ / dîner du jour, `id_employe`, `date_jour`) — cliente-validée.
  Mon 1er essai (option A) voulait réutiliser cette table, mais elle est
  figée à 4 créneaux/jour → **perte de données** si l'employé pointe
  plusieurs fois.
- **Solution (choix B)** : nouvelle table `poincons` (événementielle) :
  `id_utilisateur`, `type_poincon` (`entree`/`sortie`),
  `horodatage TIMESTAMP DEFAULT NOW()` (heure **serveur**). Chaque pression
  = 1 ligne → **aucune donnée perdue**, historique = liste des lignes.
- **Leçon** : vérifier le schéma EXISTANT avant d'ajouter une table —
  on a failli créer un doublon / écraser une table validée.

## 3. Note de conception - table `poincons` = flexibilite
- **Choix** : ajouter une table `poincons` (journal d'evenements) pour **ajouter de la flexibilite au programme** plutot que reutiliser `pointages` (4 creneaux figes/jour).
- **Avantage** : chaque pression = **1 ligne** (`entree`/`sortie` + `horodatage` serveur). Aucune limite au nombre de pointages/jour (pause, rendez-vous, retours) -> **aucune perte de donnees**. On peut ensuite **deriver** n'importe quel resume (arrivee, departs, total d'heures) a partir du journal.
- **Contraste** : `pointages` (schema v1.1) est fige a 4 champs/jour -> aurait provoque une perte de donnees si l'employe pointe plusieurs fois. C'est pourquoi on a choisi B.

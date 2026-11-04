# Questions à valider avec la cliente (propriétaire de clinique)

> But : valider les règles métiers réelles AVANT de figer le schéma et la
> logique de paie. La cliente utilise VetTime au quotidien — ses réponses
> pilotent les choix de conception (et alimenteront le blogue / les ADRs).
> À revoir avec elle dès que possible ; noter ses réponses directement ici.

## 1. Période de paie
La paie est-elle calculée à la **quinzaine** (2 semaines) ? Cela détermine
comment on découpe `periodes_verrouillage` (verrou par quinzaine).
- [ ] Réponse : __________

## 2. Majoration des jours fériés
Quel taux si un employé **travaille** un jour férié : temps et demi (1.5x) ou
double (2x) ? Et est-ce le même taux pour tous les jours fériés, ou varie-t-il
(Noël/Jour de l'An = double, Action de grâce = temps et demi) ?
- [ ] Réponse : __________

## 3. Jours fériés fermés vs ouverts
Lesquels sont des **jours fermés** (personne ne travaille, indemnité payée aux
employés absents) vs des **jours ouverts** (gardes, majoration) ?
- [ ] Réponse : __________

## 4. Banques de congés / maladie — dates de renouvellement
Confirmes-tu : **vacances renouvelées ~1er mai**, **maladie renouvelée ~1er
janvier** ? Le solde non utilisé est-il perdu ou reporté ?
- [ ] Réponse : __________

## 5. Correction après verrouillage de paie
Si une ASV oublie un punch et que la paie est déjà versée (période verrouillée),
peut-elle corriger si la **gérante approuve** ? (On prévoit un blocage + piste
d'audit, mais le niveau d'exemption compte.)
- [ ] Réponse : __________

## 6. Discordances horaire vs réel — qui approuve ?
Le rapport met en gras les écarts entre horaire planifié et heures réelles.
Qui doit approuver ces écarts : **admin seulement** ou **gérante aussi** ?
(Issue #9.)
- [ ] Réponse : __________

## 7. Postes / rôles employés
Liste des postes : Vétérinaire, ASV, Secrétaire — y en a-t-il d'autres
(réceptionniste, gestionnaire, technicien) ? Cela alimente `employes.poste`.
- [ ] Réponse : __________

## 8. Heures de contrat
Contrats à 35h, 39h, ou variables selon l'employé ? (Base du calcul des
heures supplémentaires dans `employes.heures_contrat_semaine`.)
- [ ] Réponse : __________

## 9. Statuts de journée
La liste (Travail Normal, Garde Clinique, Astreinte Domicile, Congé, Maladie)
est-elle complète ? Autres statuts possibles ?
- [ ] Réponse : __________

## 10. Multi-clinique (reporté pour l'instant)
On a reporté le multi-clinique. Si ça revient : une seule base de données avec
un `clinique_id`, ou des bases séparées par clinique ?
- [ ] Réponse : __________

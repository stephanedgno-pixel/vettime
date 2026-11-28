# Interactions avec l'IA — dossier de suivi (INF1410)

> **Ce dossier est un index.** Les **transcriptions brutes** des sessions de
> travail avec l'IA (Hermes) sont publiées dans `docs/transcriptions-ia.md`
> — c'est elles la pièce demandée par le cours, pas ce résumé.

## Moment clé : « je n'ai aucune idée de ce qui se passe »
Extrait brut de la session **T2** (voir `docs/transcriptions-ia.md`) :

> **Étudiant** : « je vais te dire mon ti père, je n'ai aucune idée de ce qu'on fait »
>
> **IA** : « pytest = les tests. "5 passed" = ton app passe les 5 contrôles.
> ruff = le linter (correcteur de style). "All checks passed" = code propre.
> ci.yml = la pipeline GitHub. À chaque git push, GitHub lance automatiquement
> tes tests. On veut qu'elle lance AUSSI ruff + build Docker. »

**Commentaire de l'étudiant :** j'ai été honnête sur mon incompréhension plutôt
que de laisser l'IA produire à ma place. L'IA m'a alors expliqué le *rôle* de
chaque outil (usage « pourquoi », pas « écris le code »), et j'ai repris le
contrôle du sens. Ce genre de moment — où je ne comprends pas encore — est
précisément ce que le cours veut voir : on n'avance pas dans le flou, on
demande, on comprend, puis on continue.

## Autres transcriptions publiées (`docs/transcriptions-ia.md`)
- **T1** — Débogage de la CI (lint + Docker) : j'ai diagnostiqué un heredoc aplati et corrigé avec `printf` (pas de copie aveugle).
- **T3** — Génération du modèle ORM : j'ai vérifié par un test (`test_onze_tables`) au lieu de faire confiance aveugle.
- **T4** — Encodage du mot de passe (`#` vs `%23`) : j'ai fait la distinction SQL littéral vs URL encodée et corrigé sans aide aveugle.

## Réflexion (à faire évoluer chaque jalon)
L'IA produit ; moi j'évalue, je diagnostique et je corrige. Où elle a déçu
(analyse visuelle imparfaite, tendance à inventer des détails) : je vérifie
chaque affirmation et je conserve la trace des corrections (`docs/problemes.md`).
Aux entretiens, je dois pouvoir expliquer *moi-même* chaque choix.
- **T8** — Discussion sur le perimetre et l'auteur du travail : l'etudiant a repris le controle quand l'IA a deborde (implementation du ledger des banques sans validation etape par etape). Voir `docs/transcriptions-ia.md`.

## T1 - Debogage de la CI (lint + Docker) - 2026-11-16

Contexte : ajout d'un job `lint` (ruff) et `docker` au pipeline GitHub Actions.
Une commande `cat > .github/workflows/ci.yml << 'YAML_EOF' ...` a echoue
(delimiteur colle au contenu) ; le fichier n'a pas ete ecrit et seul le job
`test` apparaissait dans GitHub Actions.

Etudiant :
> y'as juste test
> [image GitHub Actions : 1 seul job `test` vert]

IA (diagnostic) :
> Le fichier `ci.yml` local est toujours l'ancien (que `test`). Ton message de
> commit disait "lint+docker" mais le heredoc n'a pas ecrit le fichier - c'est
> le meme bug de heredoc aplati. Correction avec `printf` (ligne unique).

Etudiant (execute la commande `printf`, puis `git push`) :
> [image GitHub Actions : 3 jobs `test` / `lint` / `docker` verts]

IA :
> C'est regle [OK] - la derniere execution affiche les 3 jobs au vert.
> L'ecart du prof ("la CI ne lance ni lint ni Docker") est ferme.

Reflexion : l'IA a fourni la commande, l'etudiant a DIAGNOSTIQUE l'echec
(heredoc aplati) et choisi une approche robuste (`printf` ligne unique).
Preuve de sens critique, pas de copie aveugle.

## T2 - Comprehension du pipeline (usage "pourquoi") - 2026-11-16

Etudiant :
> je vais te dire mon ti pere, je n'ai aucune idee de se qu'on fait

IA (extrait) :
> - `pytest` = les tests. "5 passed" = ton app passe les 5 controles.
> - `ruff` = le linter (correcteur de style). "All checks passed" = code propre.
> - `ci.yml` = la pipeline GitHub. A chaque `git push`, GitHub lance automatiquement
>   tes tests. On veut qu'elle lance AUSSI ruff + build Docker.

Reflexion : usage "pourquoi cette commande ?" (comprehension) plutot que
"ecris-moi le code" (production). L'etudiant reprend le controle du sens.

## T3 - Redaction du blogue technique 2 (GitHub Copilot)

[A remplir : colle ici un extrait VERIDIQUE de ta session Copilot pour le blogue 2
- prompt + reponse, tel quel. Ex. : ton prompt sur le choix FastAPI+Jinja+HTMX vs
React et la reponse de Copilot, puis ta validation du contenu.]

Reflexion : l'outil produit la prose, l'etudiant garde la responsabilite
editoriale et valide les decisions (issues de nos echanges + ADRs).

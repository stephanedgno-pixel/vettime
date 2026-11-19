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

## T3 - Generation du modele ORM (SQLAlchemy) - 2026-11-16

Contexte : creation de `app/models.py` (11 tables mappees en classes SQLAlchemy 2.0).
L'IA a genere le code complet a partir du schema `docs/schema-v1.sql`.

IA (extrait) :
> Voici `app/models.py` genere du schema (11 tables, commentaire Loi 25, relations
> pour J3). Valide avec : uv run python -c "from app.models import Base;
> print('tables =', len(Base.metadata.tables))"

Etudiant (ecrit le fichier, cree tests/test_models.py, lance) :
> uv run pytest -v  ->  tests/test_models.py::test_onze_tables PASSED

IA :
> 5.2 vert : les tests passent (dont test_models -> 11 tables confirmees).

Reflexion : l'IA a produit le code ORM, l'etudiant a VERIFIE par un test
(test_onze_tables == 11 tables) plutot que de faire confiance aveugle. Meme
reflexe que T1/T2 : l'IA genere, l'etudiant valide et garde le controle.

## T4 - Encodage du mot de passe (# vs %23) - 2026-11-17

Contexte : rotation du mot de passe de la base de donnees (role PostgreSQL `vettime`)
apres la decouverte d'un ancien mot de passe dans l'historique Git. Le nouveau
mot de passe contenait un caractere `#` (ex. `MonMotDePasse#87654`).

Etudiant :
> la connexion DB fait le tour en rond : `curl /health/db` renvoie
> `password authentication failed` (503) en boucle, meme mot de passe apparent

IA (diagnostic) :
> Ton mot de passe contient un `#`. Dans une URL / un `.env`, `#` tronque l'URL
> (fin des identifiants) -> il faut l'encoder `%23`. Mais cote SQL
> (`ALTER ROLE ... PASSWORD '...'`), le `#` est LITTERAL -> il doit rester en clair.
> Ton erreur : tu as mis `%23` des DEUX cotes. L'ALTER a stocke litteralement
> `%23`, alors que le `.env` decode `%23` -> `#` : les deux ne correspondent pas.

Etudiant (applique : `ALTER ROLE vettime WITH PASSWORD 'MonMotDePasse#87654'` cote
SQL, puis `.env` avec `MonMotDePasse%2387654` cote URL, relance l'app) :
> curl /health/db -> {"status":"ok","database":"connected"}   [OK]

IA :
> C'est regle. Regle a retenir : `#` en clair cote SQL, `%23` encode cote
> URL/`.env` -- jamais identique des deux cotes. A consigner au rapport et dans
> `ia-interactions.md` (entree #5) + `problemes.md` (Jalon 2, probleme #2).

Reflexion : l'IA a explique la nuance d'encodage, l'etudiant a FAIT la
distinction (literal SQL vs encode URL) et corrige sans aide aveugle. Ce bogue
reel, resolu en boucle, est la preuve concrete d'un debogage compris --
exactement ce que le prof veut voir a la video et a l'entretien.

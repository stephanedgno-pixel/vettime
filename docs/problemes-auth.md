# Journal des problématiques — Jalon 3 (auth #1, 6 étapes)

*Document de suivi des difficultés rencontrées lors de l'implémentation de
l'authentification VetTime (issue #1, 6 étapes) en FastAPI/Starlette.
Objectif : tracer les frictions et les leçons tirées pour le blogue technique
et l'entretien oral du Jalon 3.*

## Contexte

Mise en place de l'authentification : hachage bcrypt, templates Jinja2 + page
`/login`, sessions httpOnly signées (`SECRET_KEY` dans `.env`), connexion
`POST /login` (vérification + session + redirection), protection des routes et
logout + CSRF. Environnement : serveur dédié (ThinkCentre, Debian), `uv` comme
gestionnaire, GitHub Actions pour la CI.

## Problématiques

### 1. `uv run pytest` → « Failed to spawn: pytest » (Pièce 1)
- **Symptôme** : `uv run pytest` → `error: Failed to spawn: pytest / cause: No such file or directory`.
- **Cause** : les shebangs des exécutables dans `.venv/bin/` pointaient vers l'ancien chemin de la machine (`/home/Silverwaffen/audit/.venv`) après un renommage. Le venv était corrompu.
- **Solution** : recréer le venv proprement : `rm -rf .venv && uv venv && uv sync`.
- **Leçon** : après un renommage ou déplacement de machine, les shebangs d'un venv cassent ; une recréation propre règle tous les « Failed to spawn » d'un coup. (Détail dans `docs/ia-interactions.md`.)

### 2. passlib 1.7.4 + bcrypt 5.0.0 → ValueError (Pièce 1)
- **Symptôme** : `uv run pytest` → `ValueError` au chargement du backend bcrypt.
- **Cause** : passlib (plus maintenu) est incompatible avec bcrypt 5.x.
- **Solution** : épingler `bcrypt==4.0.1` (`uv add "bcrypt==4.0.1"`).
- **Leçon** : passer par passlib n'est pas recommandé avec les bcrypt récents ; utiliser bcrypt directement ou épingler une version compatible. (Détail dans `docs/ia-interactions.md`.)

### 3. CI/LINT rouge — ruff I001 (Pièce 1)
- **Symptôme** : le job lint de la CI échoue (import en trop ou mal ordonné).
- **Cause** : règle isort d'imports (I001) non respectée dans `tests/test_security.py`.
- **Solution** : `ruff --fix` (réordonne automatiquement) puis commit.
- **Leçon** : lancer `uv run ruff check .` **avant** chaque `git push` pour éviter le rouge CI.

### 4. 500 sur GET /login — TypeError: unhashable type: 'dict' (Pièce 2)
- **Symptôme** : `GET /login` → Internal Server Error, traceback `TypeError: unhashable type: 'dict'`.
- **Cause** : signature obsolète de Starlette — `templates.TemplateResponse("login.html", {"request": request})`. Dans les versions récentes, `request` doit être le **1er argument positionnel** : `TemplateResponse(request, "login.html")`.
- **Solution** : corriger la ligne 29 de `app/main.py` vers `templates.TemplateResponse(request, "login.html")`.
- **Leçon** : l'API Starlette a changé ; vérifier la signature actuelle de `TemplateResponse` (request en 1er). Symptôme typique d'un tutoriel obsolète.

### 5. `uv run` → « Failed to spawn » car mauvais répertoire (Pièce 3)
- **Symptôme** : `uv run ruff check` / `uv run uvicorn` → `Failed to spawn`.
- **Cause** : le terminal était dans `~` (home), pas dans `~/vettime` ; `uv run` ne trouvait pas le `pyproject.toml`.
- **Solution** : `cd ~/vettime` avant tout `uv run`.
- **Leçon** : `uv run` se base sur le répertoire courant ; toujours être à la racine du projet.

### 6. curl 500 — processus uvicorn « fantôme » (Pièce 3)
- **Symptôme** : `curl http://localhost:8000/login` → « Internal Server Error » alors que le code était corrigé.
- **Cause** : un ancien uvicorn (avec l'ancien code buggé) tournait encore et occupait le port 8000.
- **Solution** : `pkill -9 -f uvicorn` puis relancer.
- **Leçon** : avant de tester, tuer les serveurs fantômes qui gardent le port ; sinon on teste l'ancien code.

### 7. ModuleNotFoundError: No module named 'itsdangerous' (Pièce 3)
- **Symptôme** : uvicorn plante au démarrage : `import itsdangerous` échoue.
- **Cause** : `SessionMiddleware` (starlette) dépend de `itsdangerous`, dépendance transitive non installée après la recréation du venv.
- **Solution** : `uv add itsdangerous` (installe + ajoute à pyproject/uv.lock).
- **Leçon** : après recréation de venv, vérifier que toutes les dépendances transitives sont présentes ; committer pyproject/uv.lock pour que la CI les installe aussi.

### 8. NameError: name 'app' is not defined (Pièce 3)
- **Symptôme** : uvicorn → `NameError: name 'app' is not defined` à la ligne `app.add_middleware(...)`.
- **Cause** : `app.add_middleware(...)` avait été ajouté **deux fois**, une fois avant `app = FastAPI(...)` (où `app` n'existe pas encore) et une fois après (correct).
- **Solution** : supprimer la ligne dupliquée placée trop haut.
- **Leçon** : `app` n'existe qu'après `app = FastAPI(...)` ; on ne peut pas appeler une méthode sur un objet non encore créé.

### 9. Même TypeError TemplateResponse sur home/erreur (Pièce 4)
- **Symptôme** : `GET /` et le cas d'erreur POST /login → `TypeError: unhashable type: 'dict'`.
- **Cause** : les nouvelles routes utilisaient encore l'ancienne signature `TemplateResponse("nom", {"request": request})`.
- **Solution** : uniformiser toutes les routes sur `TemplateResponse(request, "nom")`.
- **Leçon** : appliquer la même signature corrigée partout ; un oubli suffit à faire planter la route.

### 10. 422 sur GET /login — routes GET/POST fusionnées (Pièce 4)
- **Symptôme** : `GET /login` → 422 Unprocessable Entity.
- **Cause** : la route `GET /login` contenait les paramètres `email: str = Form(...), password: str = Form(...)` du login ; un GET sans formulaire échoue la validation.
- **Solution** : séparer en deux routes — `GET /login` → `login_page` (affiche le formulaire, sans paramètre) et `POST /login` → `login` (vérifie + session + redirection).
- **Leçon** : GET (afficher) et POST (traiter) doivent être des routes distinctes ; ne pas mélanger les paramètres de formulaire dans le GET.

### 11. CI/LINT rouge à nouveau — ruff I001 (Pièce 4)
- **Symptôme** : job lint CI rouge après l'ajout des imports (`Form`, `RedirectResponse`, `Utilisateur`, `verify_password`).
- **Cause** : ordre des imports non conforme (isort).
- **Solution** : `uv run ruff check --fix .` puis commit des 2 fichiers (`app/main.py` + pyproject/uv.lock pour itsdangerous).
- **Leçon** : re-vérifier le lint après chaque ajout d'import ; `ruff --fix` corrige automatiquement.

### 12. `pkill -9 -f uvicorn` tue le shell lui-même (Pièce 4)
- **Symptôme** : la commande de test se termine en `exit 255` sans sortie ; uvicorn fantôme non tué.
- **Cause** : `pkill -f uvicorn` a matché la propre ligne de commande du shell (qui contenait le mot « uvicorn »), tuant le shell.
- **Solution** : tuer par **PID/port** plutôt que par nom : `ss -ltnp | grep :8000` → `kill -9 <PID>` (et son parent reloader).
- **Leçon** : `pkill -f` peut matcher le shell courant ; préférer un kill par port (`ss`/`lsof`/`fuser`) pour les serveurs de dev.

### 13. `PPID: readonly variable` (Pièce 4)
- **Symptôme** : `bash: PPID: readonly variable` → le parent (reloader) n'était pas tué, le worker respawnait.
- **Cause** : tentative d'assigner une valeur à `PPID`, variable réservée (lecture seule) de bash.
- **Solution** : utiliser une autre variable (`parent=$(ps -o ppid= -p "$p")`).
- **Leçon** : ne pas réutiliser les noms de variables spéciales du shell (PPID, UID, etc.).

### 14. Mapper SQLAlchemy plante — back_populates désaligné (Pièce 4, test login)
- **Symptôme** : `POST /login` (ou tout query ORM sur `Utilisateur`) → `InvalidRequestError: Mapper 'Mapper[Employe(employes)]' has no property 'employe'`.
- **Cause** : `Utilisateur.employe` avait `back_populates="employe"`, mais l'attribut inverse côté `Employe` s'appelle `utilisateur` → désalignement de la relation.
- **Solution** : changer `Utilisateur.employe` → `back_populates="utilisateur"` (aligné avec `Employe.utilisateur`).
- **Leçon** : `back_populates` doit nommer **exactement** l'attribut inverse ; un désalignement casse la configuration du mapper (et donc tout query ORM). Ce bug latent n'était pas visible au démarrage de l'app (aucun query ORM au boot) — **c'est le test réel du login (option A) qui l'a révélé**.

### 15. Dépendance qui renvoie RedirectResponse ne court-circuite pas (Pièce 5)
- **Symptôme** : `GET /` sans session → **200** (page d'accueil rendue) au lieu de **303 → /login**. La protection ne s'active pas.
- **Cause** : en FastAPI 0.159 / Starlette 1.9, retourner un objet `Response` (ex. `RedirectResponse`) depuis une **dépendance** n'interrompt PAS le traitement. La valeur est passée au paramètre de la route (`user_id`), qui rend alors la page → 200.
- **Solution** : dans `get_current_user`, **lever une exception** au lieu de retourner un Response :
  `raise HTTPException(status_code=303, headers={"Location": "/login"})`. FastAPI court-circuite toujours sur une exception → la redirection est envoyée.
- **Leçon** : pour protéger une route et rediriger si non authentifié, la dépendance doit **lever** (`HTTPException` 3xx + `Location`), pas retourner un `Response`. Vérifier le comportement réel (test live) : un simple `ruff` vert ne prouve pas que la redirection fonctionne.



### 16. Starlette n'applique pas de CSRF automatiquement (Pièce 6)
- **Symptôme** : on s'attendait à une protection CSRF « gratuite » via SessionMiddleware.
- **Cause** : `grep csrf` dans `starlette/middleware/sessions.py` → aucune référence ; le middleware signe le cookie mais ne valide aucun jeton sur les méthodes non sûres.
- **Solution** : implémenter un **double-submit token** manuel — générer `request.session["csrf_token"]` (secrets.token_hex), injecter `<input type="hidden" name="csrf_token">` dans les formulaires POST, et vérifier `csrf_token == request.session["csrf_token"]` dans les routes (sinon 403).
- **Leçon** : jamais supposer qu'un middleware fait la sécurité pour nous ; vérifier le code source. CSRF = jeton de session + champ de formulaire + comparaison côté serveur.

### 17. Cookie `secure` (https_only) casse le test de session en HTTP local (Pièce 6)
- **Symptôme** : tous les POST (login/logout) retournaient 403 en test local (http://localhost, http://testserver).
- **Cause** : `SessionMiddleware(https_only=True)` pose l'attribut `Secure` sur le cookie ; les clients (curl, httpx, navigateur) refusent d'envoyer un cookie `Secure` sur une connexion non chiffrée → la session ne fait pas le aller-retour → `csrf_token` absent → 403.
- **Solution (test)** : tester la logique via une copie temporaire de `main.py` avec `https_only=False` (round-trip HTTP OK) ; en production, tester via l'URL tunnel **HTTPS**. Ne PAS désactiver `https_only` en prod (ADR-004).
- **Leçon** : un cookie `Secure` protège en prod mais empêche le test local en HTTP ; toujours valider via HTTPS (tunnel) ou un environnement de test dédié.

## Synthèse des leçons (pour l'oral)

1. **Venv** : recréer proprement après renommage machine ; vérifier les dépendances transitives.
2. **Signatures d'API** : Starlette `TemplateResponse(request, "nom")` en 1er argument ; GET/POST séparés.
3. **Ordre de code** : `app` doit exister avant `app.add_middleware`.
4. **Outils** : `cd ~/vettime` avant `uv run` ; `ruff --fix` avant `git push` ; tuer uvicorn par port, pas par `pkill -f`.
5. **CI** : un job lint rouge = presque toujours I001 (isort) ; `--fix` règle.
6. **Modèle** : une relation `back_populates` doit nommer EXACTEMENT l'attribut inverse ; tester un query ORM révèle les bugs latents.
7. **FastAPI 0.159** : une dépendance qui **retourne** un `Response` ne court-circuite pas ; pour rediriger, **lever** `HTTPException(3xx, Location=...)`.
8. **CSRF** : Starlette ne le fait pas pour nous ; implémenter double-submit token (session + champ + comparaison serveur).
9. **Cookie Secure** : empêche le test HTTP local ; tester via HTTPS (tunnel) ou copie `https_only=False`.

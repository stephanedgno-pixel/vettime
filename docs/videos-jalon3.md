# Vidéos — Jalon 3 (transcriptions)

*Preuves vidéo des étapes d'implémentation de l'authentification VetTime
(livrable Jalon 3). Visibilité : **Unlisted** sur YouTube.*

## 1. Étape 2 — Templates + page /login (Pièce 2)
- **URL** : https://youtu.be/JnJaYskMpZY
- **Publié** : 2026-11-25
- **Contenu** : création de `templates/base.html` et `templates/login.html`,
  route `GET /login` rendant le formulaire via
  `TemplateResponse(request, "login.html")`.

## 2. Pièce 6 — logout + CSRF (double-submit token)
- **URL** : https://youtu.be/3m-Ge0sEsSE
- **Publié** : 2026-11-25
- **Contenu** : route `POST /logout` (vide la session via `request.session.clear()`),
  jeton CSRF (généré en session + champ caché dans les formulaires + vérification
  côté serveur, **403** si invalide).
- **Note** : la démo live finale (logout + 403 sur token invalide) n'a pas été
  filmée ; le comportement est vérifié par test (voir `docs/problemes-auth.md`,
  problèmes #16 et #17).

## Récapitulatif
| # | Pièce | Vidéo |
|---|-------|-------|
| 1 | Templates + `/login` (Pièce 2) | JnJaYskMpZY |
| 2 | logout + CSRF (Pièce 6) | 3m-Ge0sEsSE |

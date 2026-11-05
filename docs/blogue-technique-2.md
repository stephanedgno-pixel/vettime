# Blogue technique 2 — Jalon 2 : Architecture et données

> **À rédiger à TA voix.** Le prof veut ton récit réflexif. Utilise les points-clés ci-dessous comme matière première,
> mais écris les phrases toi-même, à la première personne. Structure imposée
> par le cours : les 3 questions ci-dessous.

---

## 1. Quelle décision architecturale importante avez-vous prise, quel était son contexte, et quelles alternatives avez-vous rejetées et pourquoi ?

### Décision la plus réfléchie

La décision qui m'a demandé le plus de réflexion a été le choix du framework web (ADR-001). Mon premier réflexe était d'utiliser une architecture moderne de type React SPA avec une API REST, puisque cette approche est très répandue dans l'industrie. Cependant, après avoir analysé les besoins réels du projet, j'ai constaté que VetTime repose principalement sur des formulaires, des tableaux de données et des opérations CRUD (pointages, horaires, congés, rapports).

L'utilisation d'une SPA aurait ajouté une couche de complexité importante : gestion du frontend séparé, compilation, état applicatif, authentification par jetons, CORS et déploiement de deux applications distinctes. Cette complexité ne semblait pas apporter de valeur significative aux utilisateurs ni aux objectifs pédagogiques du cours. J'ai donc retenu FastAPI avec Jinja2 et HTMX, qui permet d'obtenir une interface dynamique tout en conservant une architecture plus simple à développer, tester et maintenir.

### Décision la plus risquée

La décision la plus risquée concerne probablement l'ADR-003, soit l'intégration du suivi des banques de vacances et de maladie.

Au départ, j'envisageais de limiter l'application à la gestion des présences et des horaires. Il aurait été possible de laisser le calcul des soldes de vacances à la comptable ou à un système externe. Cette approche respectait le principe YAGNI (« You Aren't Gonna Need It »), qui encourage à ne développer que ce qui est réellement nécessaire.

Toutefois, après discussion avec l'utilisatrice principale visée par le projet, il est apparu que le suivi des soldes constitue une fonctionnalité importante du processus actuel. Ne pas l'inclure aurait réduit l'utilité pratique du système et obligé les utilisateurs à conserver un second outil parallèle. J'ai donc accepté cette complexité supplémentaire afin que l'application réponde réellement au besoin métier observé sur le terrain.

Dans les deux cas, j'ai privilégié les besoins réels du projet plutôt que les technologies les plus populaires ou les solutions les plus simples. L'objectif principal n'est pas de démontrer l'utilisation d'un framework à la mode, mais de concevoir un logiciel cohérent, maintenable et adapté à son contexte d'utilisation. Les décisions retenues favorisent la qualité de l'architecture, la simplicité opérationnelle et la valeur apportée aux utilisateurs finaux, tout en demeurant alignées avec les objectifs du cours en matière de génie logiciel.

---

## 2. Quel obstacle concret avez-vous rencontré et comment l'avez-vous résolu ?

L'un des premiers obstacles rencontrés est apparu pendant la phase de modélisation de la base de données. J'avais initialement supposé que les jours fériés fonctionnaient comme dans plusieurs milieux de travail, c'est-à-dire que les employés pouvaient être appelés à travailler avec une majoration salariale (par exemple 1,5× ou 2× le taux horaire). Cette hypothèse m'avait amené à prévoir une colonne taux_majoration dans le schéma de données.

Avant de finaliser le modèle, j'ai validé cette hypothèse auprès de la cliente, propriétaire des cliniques visées par le projet. J'ai alors découvert que cette hypothèse était complètement fausse : les cliniques ferment lors des jours fériés et aucun employé n'est censé travailler durant ces périodes. Dans ce contexte, la notion de majoration salariale pour les jours fériés n'avait tout simplement aucune utilité.

Ma première réaction a été de réaliser que j'étais en train de concevoir le système à partir de mes propres suppositions plutôt qu'à partir de la réalité du métier. Même si la fonctionnalité semblait logique sur le plan technique, elle ne répondait à aucun besoin réel. J'ai donc modifié le schéma de données et supprimé la colonne taux_majoration avant même l'implantation de la logique applicative. Cela a permis d'éviter l'ajout d'une donnée inutile qui aurait complexifié la base de données et le code.

Cette correction a également simplifié une partie des règles de calcul liées aux heures travaillées et aux rapports. Comme aucun employé ne travaille les jours fériés, il n'était plus nécessaire de prévoir de calculs spéciaux ou de règles de paie associées à ces journées dans la première version du système.

Cette expérience m'a appris qu'une bonne modélisation de données repose d'abord sur la compréhension du domaine d'affaires. Il est facile de créer des tables, des colonnes ou des règles basées sur des hypothèses raisonnables, mais celles-ci peuvent être complètement inutiles si elles ne sont pas validées auprès des utilisateurs. J'ai donc retenu une leçon importante pour le reste du projet : la cliente demeure l'experte du domaine, et chaque élément important du modèle doit être confirmé avec elle avant d'être intégré à la solution.

---

## 3. Qu'est-ce que votre schéma de données révèle de votre compréhension du domaine ?

Je considère que ce schéma démontre une compréhension réelle du fonctionnement d'une clinique vétérinaire parce qu'il a été construit à partir des règles d'affaires validées avec la cliente et non à partir d'hypothèses génériques sur les systèmes de gestion du temps.

Un premier exemple est la simplification volontaire des types de journées. Le système ne gère que trois statuts : Travail, Congé et Maladie. D'un point de vue technique, il aurait été facile d'ajouter plusieurs catégories supplémentaires (astreinte, garde, télétravail, formation, etc.), mais ces situations n'existent pas dans la réalité de l'entreprise. Ce choix reflète une volonté de représenter fidèlement le métier plutôt que de construire un modèle artificiellement complexe.

Les règles de paie ont également été validées avant d'être intégrées au schéma. Les heures supplémentaires sont calculées au-delà de 40 heures par semaine avec une majoration de 1,5×, la paie est produite aux deux semaines, les banques de vacances sont reportées lors du renouvellement annuel et les banques de maladie suivent leurs propres règles de renouvellement. Ces éléments influencent directement la structure de la base de données et la logique applicative.

Le détail qui révèle selon moi le plus ma compréhension du métier est la présence du mécanisme de verrouillage des périodes de paie (periodes_verrouillage). Lors de mes discussions avec la cliente, j'ai réalisé qu'une fois une paie produite et transmise à la comptabilité, il ne doit plus être possible de modifier rétroactivement les heures. Si une erreur est découverte par la suite, elle doit être corrigée dans la période suivante plutôt que de réécrire l'historique. Cette règle n'est pas évidente lorsqu'on développe un système de gestion d'horaires, mais elle est essentielle dans un contexte comptable réel. Elle influence autant la conception de la base de données que les permissions applicatives.

J'ai également intégré des considérations liées à la protection des renseignements personnels dès la conception. Les données recueillies sont limitées à ce qui est nécessaire pour la gestion des présences, les rôles permettent de contrôler l'accès aux informations sensibles, et les périodes de conservation devront respecter les obligations comptables et les principes de la Loi 25.

Enfin, le modèle d'autorisation reflète les responsabilités observées dans l'entreprise. Les employés peuvent consulter leurs informations et soumettre des demandes, tandis que seuls les gestionnaires et administrateurs peuvent approuver des modifications ou résoudre des divergences. Cette séparation des responsabilités correspond aux processus actuellement utilisés dans les cliniques.

En résumé, ce schéma n'est pas seulement un ensemble de tables relationnelles. Il traduit des règles d'affaires réelles validées avec l'utilisatrice principale du système. La présence du verrouillage des périodes de paie est probablement l'élément qui démontre le mieux cette compréhension du domaine, car il s'agit d'un besoin métier concret qui n'aurait probablement pas émergé sans une analyse approfondie du fonctionnement de la clinique.

---

## Transcriptions de session (à publier)

- [ ] Publier 1-2 sessions sur gist.github.com (ex. : setup PostgreSQL sur le ThinkCentre, affinement du schéma avec la cliente).
- [ ] Coller les liens ici :
  - Session 1 : ___________________________
  - Session 2 : ___________________________

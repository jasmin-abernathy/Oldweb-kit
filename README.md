# Oldweb-kit — Web des années 2000 pour Verger CMS

Kit indépendant de styles visuels pour `jasmin-abernathy/mon-manager-web-cms`, gérable à terme par Mon Manager Web. Les styles se combinent avec les kits fonctionnels existants et ne remplacent pas leurs contenus.

## Livré

- Trois définitions de style **au format réel du CMS v1** : page personnelle, portail à encadrés, blog illustré.
- Schémas de compatibilité figés et provenance du CMS vérifiée.
- Validation sans dépendance, compilation des tokens existants, packaging ZIP déterministe, vérification des empreintes.
- Installation locale prudente dans le catalogue `design-styles/` : aucun écrasement et aucune activation automatique sur un site.
- Contrats de blocs rétro, exemple de composition compatible, feuille de route MMW et documentation UX/sécurité.
- Tests locaux des archives hostiles, erreurs de schéma, collisions et installation. Aucun workflow GitHub Actions.

**Limite actuelle : les tokens expriment une direction, pas tout le rendu rétro.** Le compilateur du CMS produit des variables CSS ; il ne crée pas une mise en page 1999/2004/2008. Le CMS lu ne contient pas encore d’adaptateur public complet ni d’API de gestion de styles. Le kit est installable dans son catalogue ; le rendu et la sélection depuis MMW restent à raccorder. Les modules communautaires sont décrits, pas activés ni faussement implémentés.

## Utilisation

Python 3.10+ ; aucune installation de dépendance. Depuis ce dépôt :

```sh
python3 tools/oldweb.py validate
python3 -m unittest discover -s tests -v
python3 tools/oldweb.py compile oldweb-personal
python3 tools/oldweb.py build dist/oldweb-kit-0.1.0.zip
python3 tools/oldweb.py verify dist/oldweb-kit-0.1.0.zip
python3 tools/oldweb.py install dist/oldweb-kit-0.1.0.zip /chemin/mon-manager-web-cms --dry-run
python3 tools/oldweb.py install dist/oldweb-kit-0.1.0.zip /chemin/mon-manager-web-cms
```

Puis, dans le CMS et avec sa toolchain PHP ≥ 8.5 :

```sh
php bin/compile-design-style.php oldweb-personal
```

L’installation ne modifie ni la composition d’un site, ni ses paramètres, ni sa base, ni son authentification. Si un des trois identifiants existe déjà, l’opération est refusée entièrement. Pour une future mise à jour, prévoir une migration explicite ; ce premier installateur ne remplace pas des styles en place.

## Choix visuels proposés

| ID | Libellé | Intention |
| --- | --- | --- |
| `oldweb-personal` | Page personnelle — années 2000 | Encadrés francs, liens visibles, identité personnelle |
| `oldweb-portal` | Portail à encadrés — années 2000 | Rubriques compactes, nouvelles et liens voisins |
| `oldweb-blog` | Blog illustré — années 2000 | Articles, bannière et archives |

Les dates 1999/2004/2008 sont des repères d’ambiance issus des échanges du 15 août, pas une promesse de reconstitution historique. La création du rendu visuel doit commencer par trois maquettes et le choix d’une direction ; ces fichiers ne sélectionnent pas cette direction à la place de Jasmin.

## Documentation

- [Installation et limites](docs/INSTALLATION.md)
- [Compatibilité vérifiée et protocole MMW](docs/COMPATIBILITY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [UX/UI](docs/UX-UI.md)
- [Modules rétro](docs/MODULES.md)
- [Plan d’intégration](docs/INTEGRATION.md)
- [Origine du projet](docs/ORIGINS.md)

Les sources et les scripts sont destinés au mainteneur. Le ZIP produit contient seulement un manifeste, les styles JSON et leurs empreintes : aucun code exécutable n’est importé par le client ou le CMS.

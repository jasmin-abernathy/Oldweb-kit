# Architecture proposée

## Trois couches

| Couche | Responsabilité | Distribution |
| --- | --- | --- |
| Style OldWeb | Tokens, compositions, apparence des blocs standards, ressources locales | Kit de design téléchargé |
| Blocs OldWeb | Boutons 88×31, liens voisins, journal des nouveautés, galerie rétro | Données déclaratives rendues par des composants de confiance |
| Modules communautaires | Livre d’or, réseau de sites, éventuelles statistiques | Code serveur installé par le mainteneur, séparément du kit |

Un style ne crée ni comptes ni contenus obligatoires. Il ne modifie ni les URL, ni les champs SEO, ni les formulaires, ni les permissions, ni les connecteurs métier. Une désactivation conserve les données des blocs et les rend avec un composant générique ou un avertissement dans l’aperçu ; elle ne les supprime pas.

## Format cible du téléchargement

Le format minimal livré actuellement est décrit dans INSTALLATION : manifeste, trois définitions JSON et empreintes. Les ressources/CSS évoqués ci-dessous sont une évolution à auditer ; ils ne sont pas acceptés par l’importeur v0.1.

Archive versionnée : manifeste, tokens, préréglages, CSS audité, ressources autorisées, notices de licences, documentation et empreintes. Pas de PHP, script shell, JavaScript arbitraire, migrations SQL ou templates exécutables dans un ZIP importé par un utilisateur. Les composants exécutables appartiennent au moteur déjà installé et audité.

Si le moteur actuel impose des templates PHP, ceux-ci seront une extension de confiance livrée par le mainteneur. Le ZIP de style utilisateur restera déclaratif. Ne jamais prétendre qu’une simple interdiction de PHP suffit à sécuriser l’import.

Le manifeste final devra annoncer : identifiant, version de kit, version du format, plage de versions CMS testées, identifiants/version des adaptateurs de rendu, blocs requis et facultatifs, fichiers autorisés, budget de ressources, licence et comportement de repli. Ces versions ne sont pas renseignées ici : elles doivent provenir du code lu.

## Installation et activation

1. Importer en quarantaine hors du répertoire servi au public.
2. Contrôler signature provenant d’un catalogue de confiance si disponible, provenance, taille compressée et décompressée, nombre de fichiers, doublons, collisions de casse, chemins absolus, traversée de répertoires, liens symboliques et noms spéciaux. Limiter aussi l’espace et le temps de décompression.
3. Valider le schéma et le contenu réel des fichiers. Rejeter ressources exécutables, SVG actifs et HTML arbitraire. Pour les images animées, prévoir une image fixe associée. Interdire imports CSS distants, URL externes, polices distantes et constructions hors de la grammaire admise ; idéalement compiler des tokens vers le CSS de confiance.
4. Vérifier les capacités du moteur. Sans adaptateur compatible, bloquer l’activation et expliquer ce qui manque. Une fonction facultative absente reste désactivée.
5. Calculer les empreintes et enregistrer une version immuable du paquet. Une empreinte seule ne prouve pas la confiance : elle détecte un changement, sans authentifier un auteur.
6. Créer une configuration de design en brouillon, associée à la révision de contenu courante. Produire un aperçu autorisé, non indexable, sans exposer un brouillon par URL devinable.
7. Publier atomiquement le couple révision de contenu / version de design / ressources. Interdire une publication fondée sur une révision devenue obsolète ; proposer de recharger l’aperçu. Clé d’idempotence et contrôle de concurrence côté serveur.
8. Conserver le pointeur de publication précédent pour revenir en arrière. Le retour crée une nouvelle publication auditée, sans réécrire les révisions historiques.

Installation, réglage, publication et activation des modules sont des permissions distinctes à raccorder aux permissions réelles du CMS. Aucune modification de design publique depuis une mutation hors ligne non revalidée.

## Portée du rendu

Le style s’applique au site public. Le back-office et MMW gardent leurs conventions de navigation et leurs composants accessibles ; seuls le nom et les aperçus identifient le style choisi. Les sélecteurs restent sous une racine dédiée au site, jamais sur le document du back-office.

Préserver les structures sémantiques : header/nav/main/aside/footer, un titre principal, liens natifs, formulaires étiquetés. Les anciennes tables de mise en page sont remplacées par un rendu moderne ; les vraies tables de données restent des tables.

Objectifs initiaux à mesurer, pas résultats observés : CSS du kit ≤ 35 Ko non compressé ; aucune requête vers un tiers ; pas de police Web obligatoire ; décor initial ≤ 200 Ko ; JavaScript supplémentaire nul pour le premier style. Les images éditoriales sont optimisées par le pipeline média existant, avec dimensions explicites.

Les kits métier, les contenus et les styles sont des objets séparés. Si un champ `design_styles` existe déjà, le réutiliser après lecture au lieu d’ajouter un second registre. Prévoir export du design avec références des médias et licences, jamais des secrets ou données de visiteurs.

# Fonctions rétro : périmètre

| Élément | Première livraison | Contrat et comportement |
| --- | --- | --- |
| Encadrés / navigation rétro | Oui | Rendu des menus et blocs existants |
| Boutons 88×31 | Oui si bloc générique adapté | image média, texte accessible, URL HTTP(S) validée, ordre, regroupement ; aucune image distante automatique |
| Journal des nouveautés | Oui | Représentation d’actualités déjà publiées ; pas de second système éditorial |
| Galerie rétro | Oui | Galerie existante, liens explicites, légendes et alt ; pas de carrousel automatique |
| Liens vers les sites voisins | Oui | Collection de liens administrée, sans pisteur ni widget tiers |
| GIF / blinkies | Après validation | Média fixe associé obligatoire ; pas de flashes ; choix visiteur pour lancer une animation |
| Livre d’or | Module ultérieur | Soumissions en attente, modération, protection anti-bot et quotas, échappement, suppression ; aucun HTML libre |
| Webring automatique | Module ultérieur | Annuaire géré serveur et liens stables précédent/suivant ; le front ne télécharge pas de scripts tiers |
| Compteur | Facultatif, ultérieur | Comptage agrégé via le module de statistiques adapté, sans prétendre compter des personnes uniques ; défaut désactivé |
| Bandeau défilant | Hors v0.1 | Nécessite contrôle d’arrêt et alternative fixe ; intérêt à valider |

## Livre d’or

Champs publics minimaux : pseudonyme et message ; date de publication générée serveur. Pas d’e-mail public, collecte d’e-mail non nécessaire par défaut. États : en attente, publié, refusé. Le serveur applique longueur maximum, quotas, anti-bot du socle et règles de modération. Les entrées en attente ne sont jamais dans le snapshot public ou le cache du site.

MMW pourrait exposer le livre d’or via `requests` pour la modération et `records` pour la consultation, selon le contrat réellement disponible. Les autorisations de lecture et de publication sont distinctes. Toute nouvelle primitive doit servir d’autres cas que OldWeb.

La durée de conservation des soumissions non publiées et des traces anti-abus doit être paramétrable et documentée avant ouverture. Ne pas exporter ces traces dans le kit de design ou dans Git.

## Webring

Commencer par des liens manuels : c’est suffisant pour retrouver l’esprit d’un réseau de sites. Une vérification serveur future des URL nécessite blocage des adresses privées, loopback, métadonnées cloud, redirections non autorisées et contrôle DNS à chaque connexion ; sinon risque SSRF. Aucune vérification d’URL arbitraire n’est incluse dans ce kit.

## Désactivation

Désactiver un style n’efface pas un livre d’or. Désactiver le module retire son accès public et conserve les données selon sa politique propre. Désinstaller avec suppression est une opération explicite séparée. Les exports distinguent contenu du site, réglages de style et données communautaires.

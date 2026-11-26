# Installer le catalogue

[English](INSTALLATION.en.md)

L’outil est un CLI de mainteneur, pas une route Web. Ne pas le mettre à disposition de visiteurs ni construire une commande shell à partir d’entrées utilisateur.

## Préconditions

- Source officielle du dépôt Oldweb-kit et téléchargement autorisé par le mainteneur.
- Python ≥ 3.10 pour la préparation. Le CMS cible exige PHP ≥ 8.5 selon son composer.json ; le CLI Python ne remplace pas cette exigence.
- Répertoire CMS comportant `schemas/design-style.schema.json`, `schemas/site-composition.schema.json` et `design-styles/`.
- Schémas exactement identiques aux snapshots enregistrés. Une différence bloque l’installation : relire les évolutions avant de mettre à jour la référence.
- Les chemins cibles ne sont pas des liens symboliques et aucun style OldWeb n’est déjà présent.

Exécuter d’abord `validate`, `build`, `verify` et `install --dry-run` comme indiqué dans le README. Une installation réussie ajoute trois répertoires dans `design-styles/`, chacun avec `style.json` et un reçu local `.oldweb-install.json`.

Pour un catalogue en anglais, utiliser `build ... --language en`. Le ZIP français reste le défaut. Les deux variantes partagent les mêmes identifiants et schémas v1 ; seuls les libellés, descriptions et mots-clés changent. Aucun changement de langue à chaud n’est ajouté au CMS, et aucune réinstallation n’écrase un style existant.

Le paquet est contrôlé **avant** d’écrire dans le CMS : seuls cinq fichiers prédéfinis sont admis ; chemins malveillants, doublons, collisions de casse, liens symboliques, fichiers chiffrés, excès de taille/nombre, manifeste erroné et empreintes différentes sont refusés. Les JSON sont revalidés avant l’import. Il n’y a pas d’extraction générale du ZIP : seuls les octets des fichiers connus sont lus.

L’installateur prépare tous les styles sous un répertoire temporaire local, puis les renomme. Si une erreur survient, il retire les répertoires qu’il vient de créer pour revenir à l’état précédent. Cela ne constitue pas une transaction durable couvrant un arrêt brutal du processus ou une panne de disque. Un arrêt brutal peut laisser un lot partiellement installé, **sans changer le site actif** : inspecter les reçus avant de reprendre.

## Confiance et concurrence

Les SHA-256 prouvent l’intégrité interne du paquet, pas l’identité de son auteur. Un attaquant peut reconstruire un paquet avec d’autres empreintes. Utiliser la source approuvée et contrôler le téléchargement ; une future distribution publique devra ajouter une chaîne de confiance/signature.

Un verrou local exclusif empêche deux instances de cet installateur d’écrire simultanément. Le CMS doit être un checkout sous le contrôle du mainteneur ; le CLI ne promet pas de protéger un répertoire contre un autre processus malveillant disposant des mêmes droits. Un verrou laissé après un crash n’est pas supprimé automatiquement : vérifier qu’aucun import ne tourne avant de le retirer.

## Après installation

Le catalogue est prêt pour le compilateur existant du CMS. Le site public ne changera que lorsqu’un adaptateur et son cycle d’aperçu/publication seront implémentés. L’exemple `examples/site-composition.json` illustre le choix d’un style, mais ne doit pas remplacer une composition réelle.

Réinstallation/mise à jour : refusée tant qu’un style existe. Ne pas supprimer automatiquement des styles utilisés. Désactivation : conserver les données et revenir à la configuration publiée précédente via le futur cycle de publication. Aucun bouton de publication, suppression de données ou faux gestionnaire MMW n’est livré.

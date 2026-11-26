# Compatibilité réellement lue

[English](COMPATIBILITY.en.md)

CMS lu via l’accès GitHub direct le 30 septembre 2026 : commit `49f95c98a904fbb116e698006b42232c505bb65c` de `jasmin-abernathy/dendrila-cms`.

## Présent

- `schemas/design-style.schema.json`, format 1, vocabulaire fermé et aucun champ additionnel.
- `schemas/site-composition.schema.json` : `functional_kit` et `design_style` séparés.
- `src/Design/DesignStyleDefinition.php` : validation des tokens et contraintes.
- `src/Design/CssTokenCompiler.php` : dix variables CSS et réduction des mouvements.
- `bin/compile-design-style.php` : lecture depuis `design-styles/<id>/style.json`.
- Six presets initiaux, documentation et exemple de galerie.

Les trois styles du kit utilisent uniquement ce contrat. Les palettes/badges/compositions rétro ne sont pas ajoutés comme champs inconnus dans style.json : le schéma les refuserait. Leur extension reste un contrat séparé à développer côté adaptateur.

## Non démontré / restant

L’arbre lu et les fichiers de design inspectés ne fournissent pas de moteur public complet OldWeb, d’importeur de paquets ni de route de sélection de style dans MMW. Le kit ajoute un outil d’import local, pas une nouvelle API dans le noyau. Aucun test PHP 8.5 ou test réel MMW n’a été exécuté dans cette session ; Python et la cohérence avec les sources lues sont vérifiés localement.

## MMW v1

Le protocole actuel propose `form`, `records`, `gallery`, `requests`, `calendar`, `dashboard`. `settings` est réservé. Les champs disponibles comprennent `single_choice`, `boolean`, `text` et `url` ; ne pas créer un type client `oldweb`.

La sélection de style pourrait être un champ `single_choice` dans un formulaire fourni par le serveur. Cependant, `update_fields` ne prouve pas qu’une API de publication des styles existe déjà. Ajouter le stockage, les permissions, révisions et aperçu avant d’exposer le formulaire. Pour une action sur `records`, utiliser seulement une action serveur autorisée et en ligne (`allow_offline=false`). Les anciens clients ignorent les types inconnus ; aucune extension de code mobile n’est téléchargée.

Les schémas sont figés par SHA-256 dans `compatibility/upstream.json`. L’installateur compare les schémas du CMS ciblé à ces copies et bloque toute divergence. La compatibilité ne s’appuie pas sur un numéro de version inventé.

### Dendrila du 19 novembre 2026

L’installateur accepte également l’empreinte exacte du schéma de composition
du commit Dendrila `e45aca880ee08e442094227cb710d524555b6be3`. Ce schéma
ajoute des options de marque et impose HTTPS pour le logo. La composition
fournie par le kit reste valide. Les empreintes dans le manifeste et les
archives 0.1.0 existantes restent compatibles. Une autre révision de schéma
requiert toujours une vérification avant d’être acceptée.

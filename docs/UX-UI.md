# UX et direction UI

[English](UX-UI.en.md)

## Catalogue par résultat graphique

Entrée « Web des années 2000 » dans le catalogue visuel, au même niveau que « Centré sur les images » ou « Sobre et élégant ». Les dates sont des indices d’ambiance, pas des catégories métier ni une garantie de reconstitution historique.

| Direction à maquetter | Résultat visible | Usage de la composition |
| --- | --- | --- |
| Page personnelle, vers 1999 | Cadres nets, navigation latérale, petits badges, liens soulignés, fond personnalisable | Présentation personnelle, liens, journal et galerie |
| Portail à encadrés, vers 2004 | Bandeau, menus en onglets, modules compacts et actualités au centre | Pages riches en rubriques et nouvelles |
| Blog illustré, vers 2008 | Bannière illustrée, articles dominants, archives latérales, commentaires visuellement distingués | Lecture et publication régulière |

Ces trois directions sont des propositions à visualiser et sélectionner avant de coder le rendu. La première livraison doit porter sur **une direction complète** ; les deux autres viennent après validation. Le CMS doit permettre de combiner le même style avec plusieurs kits métier.

## Identité et lisibilité

Conserver une expressivité rétro réelle : cadres, hiérarchie des encadrés, badges, densité maîtrisée, liens explicitement visibles. Éviter de tout transformer en grosses cartes arrondies de landing page moderne. La nostalgie ne justifie pas les textes minuscules, les fenêtres surgissantes, le son automatique, les clignotements ni une navigation imprévisible.

Fond, bannière et badges sont des ressources locales choisies dans la bibliothèque média ; alt pertinent pour une image informative, alt vide pour un décor. Les packs ne doivent pas copier les marques ou images de services historiques sans licence. Typographie système par défaut, taille de lecture relative, contraste vérifié sur les couleurs réellement choisies.

Personnalisation guidée : ambiance, palette, bannière, largeur de lecture, densité, bordures, placement des encadrés. Pas de CSS libre dans le parcours client initial. Si une couleur rend le texte illisible, afficher le résultat et proposer une correction avec aperçu ; conserver des garde-fous sur les éléments interactifs.

## Mobile

Ordre sémantique : identité → navigation → contenu principal → encadrés secondaires → pied de page. Une grille peut afficher les encadrés latéralement sur ordinateur sans déplacer le contenu essentiel dans le DOM. Sur mobile, une colonne ; menu compact activable au clavier, focus visible, retour du focus après fermeture. L’éditeur peut choisir un ordre des encadrés secondaires, sans masquer un contenu essentiel.

Les boutons 88×31 gardent la dimension graphique historique ; le lien qui les contient offre une zone tactile plus grande. Les images ne débordent pas, le texte reste utilisable au zoom, aucun défilement horizontal de page à 320 px. Une vraie table peut avoir son propre conteneur de défilement annoncé.

## Mouvements

Version initiale statique. Les GIF éventuels sont opt-in et accompagnés d’un visuel fixe. Le choix « Réduire les animations » remplace l’image animée par sa version fixe ; `prefers-reduced-motion` déclenche aussi ce remplacement, car du CSS ne met pas un GIF en pause. Aucun effet à flashes. Un futur bandeau défilant doit avoir un arrêt visible, le même texte accessible et une version fixe ; jamais de balise marquee ou blink.

Le mode accessible est un complément : la version normale doit déjà être utilisable. Il réduit les textures et décorations, agrandit l’interligne, renforce les contrastes et conserve les contenus et liens.

## Parcours propriétaire

1. Apparence → Styles → « Web des années 2000 » → détails du kit, compatibilité et taille.
2. Installer sans publier : l’ancien site reste servi.
3. Choisir l’ambiance et quelques réglages. « Tester avec mes contenus » ouvre une prévisualisation ; aucun texte d’exemple n’écrase le site.
4. Comparer ordinateur/mobile, mode accessible et animations réduites. Liste lisible des blocs dont le repli diffère.
5. « Publier ce style » affiche la révision concernée. Après publication : état actif, date et commande de retour au style précédent.

Un module communautaire se configure ailleurs, depuis les fonctionnalités : explication courte, données conservées, modération et permissions. Le style n’active jamais automatiquement un livre d’or public.

## États à concevoir

Téléchargement en cours, archive invalide, moteur incompatible, dépendance facultative absente, aperçu expiré, modification concurrente, publication réussie/échouée, retour effectué, média introuvable, bloc inconnu et absence de réseau dans MMW. Une erreur conserve les réglages de brouillon ; elle n’affiche jamais « style actif » avant confirmation du serveur.

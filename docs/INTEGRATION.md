# Prochaine intégration dans Dendrila

Le kit est autonome dans `jasmin-abernathy/Oldweb-kit`. Le noyau reste dans `dendrila-cms` et l’app dans `lepotager-site-manager`.

## Premier lot livré

Catalogue installable localement, trois définitions v1, compilation des tokens fermés, archives reproductibles et tests du pipeline d’import. Le compilateur Python reproduit les dix mappings observés dans le compilateur CMS ; l’outil officiel PHP demeure la référence après installation.

## Rendu visuel

1. Préparer trois maquettes de direction à partir du brief UX, puis choisir une cible visuelle.
2. Implémenter un adaptateur public de confiance : sémantique HTML, navigation, cadres, zones secondaires, galerie, liens 88×31 et journal des nouveautés.
3. Vérifier les captures en mobile/ordinateur, clavier, zoom, mode accessible et animations réduites ; les tokens seuls ne sont pas un test visuel.
4. Garder l’apparence publique isolée de MMW et du back-office.

## Publication et gestion

Réutiliser le noyau CMS pour des réglages en brouillon, aperçu autorisé, validation serveur et publication versionnée. Vérifier qu’aucune mutation hors ligne ne publie implicitement. Le retour au style précédent doit restaurer une publication cohérente, sans supprimer les données. Ne pas modifier l’authentification existante.

## Blocs et modules

`contracts/retro-blocks.json` décrit les données souhaitées, **ce n’est pas un fichier à importer dans les schémas du CMS**. Raccorder les boutons/liens/galeries au modèle générique existant. Livre d’or, compteur et webring automatique demandent un vrai backend, modération, contrôle de données et tests de sécurité ; ils ne sont pas nécessaires au premier rendu.

## Fonds animés (extension facultative, non encore implémentée)

La spécification et le plan d'intégration sont dans [ANIMATED-BACKDROPS.md](ANIMATED-BACKDROPS.md). La première version reste statique ; les effets (vidéo, Canvas/SVG/WebGL) seront ajoutés **dans un renderer de confiance côté Dendrila** et paramétrés via un contrat déclaratif versionné, avec poster, pause, reduced-motion et repli sans WebGL. Les ZIP de design n'importent aucun script arbitraire.

## Tests restants

- Exécuter le compilateur PHP ≥ 8.5 sur un checkout cible avec son autoload.
- Intégrer le rendu pilote et vérifier contenu, URL, SEO, formulaires et connecteurs.
- Tester la publication concurrente, son idempotence et le rollback serveur.
- Tester le vrai client MMW sur le même SHA de référence.
- Mesurer le poids, les requêtes et EcoIndex avant toute annonce de score.

Ne pas activer de workflow pour ce kit tant que les Actions doivent être économisées. Les sources du kit sont regroupées ; `dist/` est généré localement et exclu de Git.

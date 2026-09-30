# Travail dans Oldweb-kit

- Lire `repo-factory/AGENTS.md`, son playbook de compatibilité, les consignes du CMS et le protocole v1 MMW avant une intégration.
- Styles visuels indépendants des kits fonctionnels ; classement par résultat graphique.
- Ne pas modifier les contenus, URL, permissions, authentification ou réglages actifs pendant l’installation du catalogue.
- Aucun code téléchargé exécuté dans MMW ; les fonctions communautaires restent serveur.
- Aucun workflow GitHub Actions pour ce kit à ce stade. Packaging et tests locaux, un lot cohérent par push, `[skip ci]`.
- Ne pas présenter les tokens comme un rendu rétro complet ; ni les contrats de livre d’or comme un backend déjà prêt.
- Ne pas ajouter de dépendances pour les tâches couvertes par la bibliothèque standard Python.
- L’installateur n’importe que les trois fichiers JSON connus et n’écrase jamais un chemin existant. Toute évolution de cette règle nécessite des tests de non-régression.
- Aucun vrai message de visiteur, secret, token ou adresse privée dans les fixtures.
- Le rendu UI demande une cible visuelle choisie, vérification mobile/clavier et captures ; l’accessibilité de la version normale est obligatoire.

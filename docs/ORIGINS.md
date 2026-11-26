# Origine et décisions

[English](ORIGINS.en.md)

La recherche des anciennes discussions retrouve un échange du 15 août 2026 : Jasmin demandait un CMS autonome reprenant le Web des années 90–2000, appelé dans les réponses « OldWeb CMS ». Les propositions incluaient thèmes 1999/2004/2008, compteurs, livres d’or, boutons 88×31, blinkies, GIF, bandeaux défilants, webrings et galeries. Il faut distinguer la demande de Jasmin des propositions de l’assistant, qui ne sont pas toutes validées.

Le 30 septembre, Jasmin souhaite préparer cette expérience comme kit supplémentaire pour Dendrila CMS. Il privilégie un catalogue par résultat graphique, indépendant du métier. Le dépôt privé `Oldweb-kit` a été fourni et son état vide vérifié avec l’accès GitHub direct.

Décision : conserver l’expérience complète dans le noyau Dendrila plutôt que fabriquer un second CMS autonome. Séparer le style, les blocs et les fonctions communautaires. Le téléchargement doit rester léger et ne peut pas envoyer de code dynamique dans MMW.

Les documents de conception initiaux dans `docs/` expriment la cible de produit ; les capacités réellement livrées et leurs limites sont précisées dans README, INSTALLATION et COMPATIBILITY.

Le nom commercial confirmé le 30 septembre est **Dendrila CMS**. Les chemins de dépôt, namespaces et variables `--mmw-*` sont conservés ici pour correspondre au code réellement lu ; leur migration se fait séparément avec compatibilité. Aucun relais temporaire entre modèles n’est committé.

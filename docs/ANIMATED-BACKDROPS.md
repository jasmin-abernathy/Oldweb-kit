# Fonds animés rétro — Flash sans Flash (proposition d'intégration)

Statut : **spécification et recherche, pas encore rendu intégré**. Ce document prépare une extension facultative d'Oldweb-kit et de l'adaptateur public **Dendrila CMS**. Il ne change ni le schéma des styles v1, ni le contenu du ZIP v0.1, ni les sites publiés.

## Intention

Retrouver la créativité des fonds Flash des années 2000 sans Flash Player, greffon propriétaire, scripts tiers ni démarrage sonore. S'inspirer des *principes* des fonds Cargo/Ragekit, sans copier le code, les médias ou les effets propriétaires. Les animations ne doivent pas être obligatoires pour bénéficier du style OldWeb.

### Familles d'effets à prévoir

| Famille | Rendu | Technique à privilégier | Repli |
| --- | --- | --- | --- |
| Ondulations / déformations | Image qui ondule au passage du pointeur, ou lentement | WebGL avec shader local audité ; éventuellement Canvas 2D | Image source fixe |
| Kaléidoscope / miroir | Symétries et rotation d'une texture | WebGL local ; géométrie simple en CSS/SVG si possible | Image fixe |
| Slitscan / balayage | Bandes mouvantes et décalages | WebGL ou Canvas 2D selon coût GPU/CPU mesuré | Image fixe |
| Pixellisation / tramage | Esthétique rétro basse résolution | CSS (image-rendering) / Canvas 2D avant WebGL | Image fixe |
| Boucle vidéo décorative | Animation source courte sans son | Vidéo MP4/H.264, WebM si utile, poster local, streaming HTTP progressif | Poster |
| Dégradés animés simples | Fonds organiques ou rétro | CSS/SVG en premier | Dégradé fixe |

Ne pas promettre que WebGL est toujours plus léger qu'une vidéo : comparer **octets transférés, CPU/GPU, batterie et stabilité** sur mobile.

## Architecture de confiance

- Le **style Oldweb-kit** reste déclaratif : nom d'effet dans une **liste fermée**, identifiant de média de la médiathèque native, paramètres bornés (intensité, vitesse, réaction au pointeur, cadrage), référence de poster fixe et choix d'activation. Aucun GLSL, JS, HTML ou CSS arbitraire importé du ZIP.
- Le moteur d'animation et les shaders, s'ils existent, sont **livrés et audités avec Dendrila CMS**, pas chargés depuis une URL de thème ou depuis Cargo. Ne pas ajouter de dépendance tierce par défaut.
- Les fonds vidéo utilisent des fichiers locaux de la médiathèque ; aucune intégration YouTube/Vimeo par défaut, pour éviter requêtes externes et cookies.
- Réutiliser le pipeline média du CMS et son modèle de composition ; ne pas ajouter des champs aux schémas v1 sans versionner un contrat compatible. Aucune modification automatique des réglages existants.
- Les fonds sont purement décoratifs (hors parcours clavier et lecteur d'écran), avec texte, navigation et liens indépendants, lisibles sur une couche de contraste.
- Sur une page, limiter le nombre de moteurs actifs ; laisser le fond statique tant qu'il n'est pas visible.

## Comportement et accessibilité requis

1. Réglage **« Fond animé »** désactivé par défaut pour les styles existants ; configuration explicite par l'administrateur, aperçu avant publication, rollback.
2. Poster local visible avant initialisation et après toute erreur, y compris WebGL indisponible ou perte de contexte.
3. Respecter `prefers-reduced-motion: reduce` : poster fixe, **sans initialiser le moteur animé**. Idem pour le mode accessible si l'animation est désactivée.
4. Contrôle visible **« Mettre le fond en pause / Reprendre »** si l'animation dure plus de cinq secondes ou se répète ; état accessible au clavier et conservé pendant la visite.
5. Désactiver les effets réactifs au pointeur sur appareils sans pointeur fin ; ne jamais rendre le fond indispensable pour comprendre les contenus.
6. Déclenchement différé via `IntersectionObserver`, arrêt lorsque l'onglet est masqué via `visibilitychange`, et plafond de fréquence/densité de pixels. Pas d'audio automatique, pas de flash/stroboscope.
7. Pour la vidéo : `muted playsinline loop` seulement si volontairement activée, `poster`, `preload="none"` ou `metadata` selon tests ; `object-fit: cover` pour le décor. Ne pas compter sur un poster pour réduire les octets si `preload` télécharge déjà la vidéo.

## Parcours dans l'éditeur (à implémenter côté CMS)

`Apparence → Styles → Web des années 2000 → Fond` puis :
- **Statique / Effet animé / Vidéo courte**
- choix du média source + poster fixe via médiathèque ;
- préréglage fermé (ondulation, kaléidoscope, balayage, pixellisation) ;
- vitesse (lente/normale), intensité (douce/marquée), réaction à la souris (oui/non) ;
- bouton pause et aperçu mobile / mode animations réduites ;
- avertissement sur le coût de transfert et l'énergie estimés, sans chiffre inventé.

Le CMS doit garder une version statique toujours fonctionnelle. Oldweb-kit n'active aucune animation lors d'une simple installation.

## Vérification de Ragekit avec WebInspector

À chercher **dans Elements**, en évitant les occurrences dans la grande feuille CSS générique : `[data-backdrop]`, `data-backdrop="..."`, `canvas`, `<video`, `<source`, `video_background`, `shader`, `src=`, `data-src`. Une propriété CSS générique ne prouve pas qu'un effet est actif.

À chercher **dans Network** : `_jsapps/backdrop`, `t/webgl`, `freight.cargo.site`, `interlace.png`, `.mp4`, `.webm`, `videoplayback`, `.frag`, `.vert`, `.glsl`. Une requête `googlevideo.com/videoplayback` peut venir d'une intégration YouTube sans rapport avec le fond. Une URL `/t/webgl/` suggère une texture préparée pour un rendu WebGL, **pas** le type exact de l'effet.

Vérifier ensuite : élément effectivement affiché, type MIME, poids transféré, nombre de requêtes au premier écran, présence d'un poster, pause hors écran, rendu mobile, repli sans WebGL.

### Sources utiles

- Site étudié : https://ragekit.org/ (captures d'inspection transmises le 19 novembre 2026).
- Documentation Cargo Backdrops : https://cargo.site/docs (backdrops vidéo et interactifs).
- Compatibilité Cargo : https://cargo.site/docs/browser-support (certaines animations requièrent WebGL).

## Observation confirmée du 19 novembre 2026

Une inspection du **DOM de page (hors CSS)** sur Ragekit montre dans un bloc `page-3` :

```html
<div data-backdrop="ripple" style="">
  <canvas width="1219" height="0" class="displacement_canvas"></canvas>
</div>
```

**Fait établi :** Ragekit configure au moins un fond Cargo de type **Ripple** avec un Canvas de déplacement. La requête réseau `freight.cargo.site/w/2048/t/webgl/i` rend plausible une texture pour un rendu WebGL, sans prouver que ce Canvas utilisait WebGL ni qu'il dessinait au moment de la capture (`height="0"`). Aucune balise `<video>` n'a été trouvée par WebInspector dans les recherches rapportées, mais ceci ne prouve pas l'absence de vidéo sur toutes les pages. Les flux `googlevideo.com` peuvent être les vidéos YouTube intégrées.

**Conséquence pour la P1 :** implémenter en premier une **ondulation Ripple originale**, sans copier le shader Cargo ; démonstrateur avec `canvas` et poster local, et repli explicite si WebGL indisponible. Relever ensuite les vrais coûts en téléchargement et GPU.

## Phases et critères d'acceptation

- [x] **P0a — Identification** : un effet concret confirmé sur une page de Ragekit, `data-backdrop="ripple"` et `<canvas class="displacement_canvas">` (capture WebInspector du 19/11/2026).
- [ ] **P0b — Validation du rendu** : constater l'animation effective, le type exact de contexte Canvas, les médias et les octets transférés ; les autres sections de Ragekit peuvent utiliser d'autres fonds.
- [ ] **P1 — Preuve de concept** : un effet original local audité, un poster fixe, un contrôle pause et aucun appel réseau tiers ; démo autonome et mesures.
- [ ] **P2 — API Dendrila** : renderer commun, liste blanche de presets, validation des paramètres, pipeline médias/ressources, séparation kit/moteur.
- [ ] **P3 — Éditeur** : choix et aperçu réversible, publication/rollback, mobile.
- [ ] **P4 — Tests** : clavier, contraste, reduced-motion, sans WebGL, perte contexte, pause onglet masqué, mobile basse puissance, consommation et budget réseau.

**Budgets à tester, non garantis** : garder le décor statique initial à l'objectif existant de 200 Ko ; comparer plusieurs qualités et durées des vidéos, fixer les plafonds sur mesures. Toute régression mesurée doit permettre de désactiver l'effet sans impact sur les contenus.

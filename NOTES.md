# Notes et trouvailles — « Dans les rêves » 🌙

Journal des choix, des découvertes et des décisions, au fil de l'eau. Petit frère de
[*Dans mon corps*](https://github.com/w3cdotorg/dans-mon-corps) et de
[*Dans le volcan*](https://github.com/w3cdotorg/dans-le-volcan).

## 2026-10-29 — Naissance du projet

**Ce qu'on fait.** Un explorateur pour un enfant de 4 ans ½ – 5 ans, qui ne lit pas
encore, pour expliquer ce que fait le cerveau la nuit : il reprend ce qu'on a vécu dans
la journée, le range, le mélange, et ça fabrique des rêves — beaux ou cauchemars — qui
transforment et exagèrent ce qu'on a vu.

**L'anecdote fondatrice.** Visite d'une expo de street art ; devant le bâtiment, le
pouce géant de César. Des amis (enfants de 3 ans ½) en rigolent comme d'un « pouce
d'ogre ». La nuit même, l'enfant se réveille plusieurs fois, terrorisé par « un ogre
gigantesque ». Les parents lui chantent « Hey, ho, les chiens pirates ! » (l'école des
loisirs) pour lui changer les idées. Le lendemain matin il raconte encore l'ogre.
→ C'est **l'histoire qu'on raconte** dans l'explainer, pas un exemple inventé.

**Décisions prises avec le propriétaire.**
- Double objectif : s'émerveiller (« mon cerveau travaille pendant que je dors ! »)
  **et** se rassurer (« l'ogre, c'est mon cerveau qui a mélangé le pouce et le mot
  ogre »). Le second impose de donner à l'enfant un **outil réutilisable** : la
  *télécommande* (changer de chaîne en chantant sa chanson préférée) — exactement ce
  que les parents ont fait, et ce que recommandent les spécialistes du sommeil.
- L'enfant **compose sa propre journée** avec des cartes-souvenirs, et le rêve de la
  nuit est fabriqué à partir de ces cartes (pouce + ogre − copains = ogre gigantesque ;
  glace + chien = chien en glace, on rigole).
- Usage **en journée, à tête reposée** (pas au coucher) ⇒ on peut dessiner le
  cauchemar franchement, et la page peut vivre le cycle jour → nuit → matin.
- La vidéo YouTube « Hey, ho, les chiens pirates ! » est **intégrée en embed**
  (autorisation obtenue par le propriétaire) : c'est le bouton « changer de chaîne ».
  Dégradation propre sans réseau.
- **Pas de bibliothèque externe** (même fabrication que le corps et le volcan : une
  page, SVG à la main). Three.js resterait possible plus tard en `vendor/` pour un
  bonus « tourne le cerveau », sans rien redessiner.
- **Anti-objectif n° 1 du propriétaire : « un style habituel dans les dessins ».**
  → Planche contact de styles à proposer avant toute spec (voir `docs/brainstorm/`).
- Notes fréquentes ici, commits fréquents, dépôt public `w3cdotorg/dans-les-reves`.

**En cours.** Recherche de fond (Canopé, Inserm, INSV, science du sommeil et des rêves
chez les 4-5 ans) lancée en arrière-plan ; résultat attendu dans
`docs/recherche-cerveau-sommeil.md`.

**Nom.** Le propriétaire a tranché : `dans-les-reves` (et non « dans ma tête »). Le titre affiché sera « Dans les rêves ».

## 2026-10-29 — Planche contact des styles

Huit styles proposés sur **la même géométrie** (tête de profil, cerveau, pouce-ogre rêvé,
jour à gauche / nuit à droite), pour que seule la manière compte :
`docs/brainstorm/2026-10-29-planche-styles.html` (fragment HTML servi par le compagnon
visuel de brainstorming ; les `<symbol>`/filtres partagés sont en tête du fichier).

| | Style | Références | Pourquoi ici |
|---|---|---|---|
| A | Risographe 3 encres | Blexbolex, Hélium, éd. 2024, Tom Gauld | le mélange des encres = le mélange des souvenirs |
| B | Théâtre d'ombres | Lotte Reiniger, Michel Ocelot | le cerveau-lanterne, le rêve en ombre chinoise projetée |
| C | Papier découpé | Eric Carle, Leo Lionni, Lotta Nieminen | les souvenirs = bouts de papier recollés autrement |
| D | Planche anatomique 1900 | Larousse, Bourgery, Brödel, Corpus | le sérieux savant, et l'ogre légendé comme le cervelet |
| E | Sérigraphie années 60 | Alain Grée, Dick Bruna, Paul Rand | aplats chaleureux, très lisibles, pas mièvres |
| F | Géométrique minimal | Charley Harper, Jean Jullien, Munari | le moins de traits possible, chacun juste |
| G | Craie sur ardoise | tableau d'école, Kentridge (doux) | tout a l'air dessiné à l'instant, on efface et on redessine |
| H | Feutrine et fil | livres en tissu, stop-motion feutre | le monde du doudou, rassurant |

Techniques SVG vérifiées en rendu (capture Chrome headless) : grain papier et bords
déchirés par `feTurbulence` + `feDisplacementMap`, craie par turbulence + masque,
feutrine par turbulence + ombre portée, trames de points et hachures par `<pattern>`,
encres riso par `mix-blend-mode:multiply` avec décalage de calage. Tout tient dans une
page sans dépendance.

Explicitement écarté : le planétarium néon / verre dépoli du corps et du volcan
(« le style habituel » de la famille, anti-objectif du propriétaire).

## 2026-10-29 — Choix du style : feutrine, avec un second thème riso

Le propriétaire a choisi **H · Feutrine et fil** (« c'est top ») et demande un rendu
textile travaillé : doux **mais avec du volume**, « comme si on avait découpé et posé les
éléments », avec des **imperfections (des bouloches, mais pas vilaines)**. Il veut aussi
un **second thème risographe** (A), commutable.

**Architecture retenue pour les deux thèmes.** Le dessin est écrit une seule fois (mêmes
`<path>`). Un thème = un jeu de couleurs + un filtre de matière + un traitement des
contours : en feutrine les contours sont des **coutures** (traits pointillés, fil avec
relief), en riso ils sont la **passe d'encre bleue** décalée. Interrupteur 🧶 / 🖨️ en
haut de page, mémorisé en `localStorage`.

**Recette du filtre feutrine (v5, validée en capture)**, dans l'ordre :
1. découpe aux ciseaux : `feTurbulence` basse fréquence (.04) + `feDisplacementMap` 2.4 ;
2. bord pelucheux fin : turbulence 1.1 + déplacement 1.1 ;
3. fibres **mates** : bump map (`fractalNoise` 1.5×1.1, 3 octaves) → `feDiffuseLighting`
   (surfaceScale 1, lumière 225°/60°) **ramené vers le blanc** par `feComponentTransfer`
   (slope .3, intercept .78) puis `multiply` — sans cet aplatissement, la v2 ressemblait à
   du tissu-éponge / crochet ;
4. volume « coussin » : érosion 3.2 + flou 2.2 → le pourtour est un peu plus sombre (.16) ;
5. épaisseur : anneau érodé 1.2, liseré blanc (.5) décalé haut-gauche, liseré sombre (.3)
   décalé bas-droite, légèrement floutés ;
6. bouloches : `fractalNoise` **.3 à 1 octave, seuil alpha très dur (60·a − 46.5)** → une
   poignée de blobs par pièce, dilatés .55, floutés .45, blancs à .42 avec une ombre
   minuscule. ⚠ Calibré sur un banc d'essai de 4 variantes (capture) : avec un seuil plus
   doux (14·a − 8.4 en v3, 40·a − 27.5 en v4) c'est de la neige / des pois partout. Les
   bouloches doivent rester **rares** pour rester jolies ;
7. ombre portée douce (1.3, 2.6, σ 1.9, .34) : la pièce est posée sur la toile.
Toile de fond : motif de lin (`<pattern>` 7 px) + grain multiplié. Fil : filtre `thread`
(déplacement .9 + petite ombre) pour un point un peu irrégulier.

**Recette riso (v2)** : trois passes `mix-blend-mode:multiply` (jaune #ffe14a décalée
(−1.6, 1.1), rose #ff4fa8 (1.5, −1.3), bleu #0f6fb8 (.6, .4)), couverture d'encre
irrégulière par masque de bruit, bord qui bave (déplacement 1.4), étoiles en réserve.

**Coût** : chaque pièce feutrine porte un filtre à ~35 primitives. À surveiller sur
tablette ; prévoir une version allégée (`prefers-reduced-motion` ou détection de lenteur)
qui garde découpe + ombre + coutures et supprime fibres et bouloches.

## 2026-10-29 — Recherche de fond reçue

`docs/recherche-cerveau-sommeil.md` (271 lignes, une URL par affirmation). À retenir :
- **Source institutionnelle pivot** : synthèse CSEN « Mieux dormir pour mieux apprendre »
  (2022, dir. Stéphanie Mazza), diffusée par Canopé : hippocampe = « mise en mémoire
  temporaire », cortex = « stockage définitif », rejeu en sommeil lent profond ; 10-13 h
  de sommeil entre 3 et 6 ans ; lent profond concentré avant 2-3 h du matin. Corpus et
  Les Fondamentaux n'ont **pas** de vidéo sommeil identifiable.
- **Science** : cycles ~80-90 min (ne pas donner de chiffre à l'enfant), 6-7 cycles ;
  les rêves **mélangent** les éléments du jour, ils ne les rediffusent pas (Wamsley 2010) ;
  résidu diurne / dream-lag (Nielsen 2004) ; en paradoxal, amygdale + et préfrontal −
  (Maquet 1996) ⇒ rêves bizarres et non critiqués ; « thérapie de nuit » de Walker
  **contestée**, à présenter comme hypothèse. Enfants : distinction rêve/réalité acquise
  entre 3 et 5 ans ; cauchemars fréquents à 3-6 ans mais « souvent » seulement chez 1-4 %.
- **Cauchemar ≠ terreur nocturne** (REM, fin de nuit, réveil complet, souvenir, consolable
  vs lent profond, début de nuit, pas vraiment réveillé, aucun souvenir). L'ogre = cauchemar.
- **Recommandations** : nommer la peur sans se moquer, « c'était un rêve », doudou ; de
  jour, « changer le film » (Naître et grandir) ; **ne pas** proposer de « chasser le
  monstre » ; pas d'écran ni d'histoire effrayante le soir ⇒ l'explainer est un outil
  **de jour**, l'image de l'ogre doit être brève et immédiatement domestiquée, jamais en
  dernier plan.
- **Anatomie** : amygdale et hippocampe en temporal médial à hauteur du conduit auditif,
  amygdale **devant** l'hippocampe ; pinéale sous le splénium ; NSC au-dessus du chiasma.
- Trous : refrain exact des chiens pirates non vérifié en ligne ; épisode « 1 jour 1
  question » sur les rêves non confirmé.

## 2026-10-29 — Feutrine « à l'aiguille » (v6 → v7), d'après le renard

Le propriétaire a envoyé une référence : un **renard en laine feutrée à l'aiguille**
(photo Etsy, copie locale `docs/refs/renard-laine-feutree-etsy.jpg`, à usage de
référence de dessin uniquement). Ce qu'on en prend : pièces **bombées** (volume réel,
pas une découpe plate), **halo de fibres** sur tout le contour, **broderies blanches**
(volutes au point de tige + nœuds français) sur le corps, œil fermé brodé d'un trait,
laine mate à teinture légèrement irrégulière. Le riso reste tel quel (v5), validé.

Décisions du propriétaire : **la toile elle-même s'assombrit** pour la nuit (pas une
pièce bleue posée) en surveillant les contrastes ; cartes-souvenirs **épinglées, oui**,
avec des épingles plus grandes et plus réalistes.

**Recette laine feutrée (filtre `wool`, v7, validée en capture)** :
A. halo : `feMorphology dilate 1.3` sur SourceGraphic (garde la couleur de la pièce)
   → `turbulence 1.5` + déplacement 4.5 → flou .35 → alpha ×.5. ⚠ En v6 (dilate 2.2,
   déplacement 7) le halo faisait une bordure givrée trop large sur les petites cartes.
B. corps : contour feutré (fractalNoise .05 → déplacement 2.6, puis turbulence .8 →
   déplacement 1.4).
C. laine : fibres `fractalNoise .75×.6, 4 octaves` → diffuse (surfaceScale 1.6,
   230°/52°) ramenée par `feComponentTransfer` slope .4 / intercept .66, multipliée ;
   teinture `fractalNoise .12` très discrète (slope .12 / intercept .9).
D. bombé : alpha flouté σ 2.6 → diffuse surfaceScale 5 (225°/48°), slope .3 /
   intercept .7 (**jamais > 1**, sinon liseré blanc brûlé), multiplié ; spéculaire
   quasi nul (constante .12, exposant 6). ⚠ En v6, spéculaire .35 / exposant 22 et
   surfaceScale 9 donnaient un rendu **brillant, pâte d'amande / gelée** : la laine est
   mate, le reflet doit être à peine perceptible.
E. bouloches rares (mêmes réglages que la v5).
F. ombre portée (1.4, 3, σ 2, .4).
Broderie : fil blanc 1.25 px, tirets 2.6/1 (point de tige), nœuds français = petits
cercles à dégradé radial, filtre `thread` (déplacement .9 + ombre .35/.4).
Toile : lin (`<pattern>` 7 px + grain) × dégradé `dusk` en `mix-blend-mode:multiply`
(blanc jusqu'à 42 %, puis #8d8cae, #3f3f74, #262a58) : la trame reste visible dans la
nuit, les pièces crème / le fil blanc / le halo clair gardent leur contraste.
Épingles : groupe `#pin` (tige acier en dégradé + fil de lumière blanc, tête de verre
en dégradé radial rouge/bleu/jaune avec reflet, ombre de la tête et de la tige), tourné
à l'usage. ⚠ Les couleurs de tête par sélecteur CSS à travers `<use>` ne passent pas
(arbre fantôme) : dans le vrai dessin, utiliser `currentColor` ou trois symboles.
Œil fermé « comme le renard » côté nuit : un trait brodé courbe.

Point de vigilance de dessin repéré sur la maquette : l'oreille et le cervelet se
chevauchent dans la géométrie de test ; dans le vrai dessin, le cervelet est derrière et
au-dessus du conduit auditif, l'oreille devant.

## 2026-10-29 — Grain de la laine affiné (v8)

Retour du propriétaire sur la v7 : « un tout petit peu grossier, pour l'intérieur des
formes notamment ». Banc d'essai de 4 finesses de fibres (scène + zoom, capture) :
la v7 (`fractalNoise .75×.6`, 4 octaves, slope .4) lisait comme du papier froissé. Retenu :
**fibres `fractalNoise 2×1.6`, 2 octaves, surfaceScale 1.05, slope .27 / intercept .765**,
teinture presque imperceptible (slope .06 / intercept .95). Règle : la laine feutrée à
l'aiguille est **fine et régulière** ; la matière se lit au bord (halo, bombé) plus que
dans la surface, qui doit rester calme.

Épingles (v9, demande du propriétaire) : **tige plus grosse** — un trapèze d'acier de 2,8 px à la tête qui s'effile en pointe sur 25 px, fil de lumière blanc + fil d'ombre gris, ombre de la tige portée sur la toile ; tête de verre r 4,6 avec reflet principal et petit reflet secondaire.

Épingles **plantées** (v10, retour du propriétaire : « on ne dirait pas qu'elle est plantée ») : on ne voit que ~10 px de tige, qui entre dans la laine par un petit creux sombre entouré de fibres repoussées en clair ; l'ombre de la tige ne court que sur la partie visible. Validé en capture. Épingle déclarée « parfaite » par le propriétaire → **référence figée** pour le dessin final.

## 2026-10-29 — Spec de design écrite, en relecture

`docs/superpowers/specs/2026-10-29-dans-les-reves-design.md`. Choix structurants pris
dans la spec (à valider par le propriétaire) : deux curseurs croisés comme le volcan
(TEMPS : journée / soir / nuit profonde / nuit des rêves / matin ; VUE : dehors / dedans /
tout près) ; cartes-souvenirs avec **catégorie + charge**, 4 max par journée ; rêve
fabriqué par **base + greffe + modificateur** à partir des 2 cartes les plus chargées,
phrase à gabarit fixe ; **télécommande** = carte réconfort + transformation ridicule/gentille
+ chanson (embed) + phrase-clé ; mode guidé « L'histoire du pouce » ; second mini-jeu
« Rêve ou pour de vrai ? » ; carte « Pour les parents » ; budget de filtres + version
allégée automatique. Relecture par un constructeur neutre lancée (brainstorming skill,
builder check) avant remise au propriétaire.

## 2026-10-29 — Relecture constructeur : cinq questions, cinq décisions

Le relecteur (agent neutre, sans accès à la conversation) a trouvé cinq endroits où il
aurait dû deviner. Toutes tranchées par le rédacteur et intégrées à la spec (§11) :
1. **Rôles du rêve** : la recette initiale (« la carte n° 1 devient la base ») ne
   reproduisait pas l'histoire du pouce (l'ogre serait devenu un pouce, et en mode guidé le
   pouce n'était même pas ingrédient). Nouvelle règle : greffe = carte la plus chargée ;
   base = la plus concrète des autres (chose vue > gens > mot > ressenti) ; contexte = la
   suivante, effacée par « gigantesque ». Une seule carte → rêve seul, modificateur, « ton
   cerveau l'a rejouée ».
2. **Charges numériques** : peur 3, colère 2, joie 1, neutre 0, apaisante −2. Colère →
   « rêve bizarre » (à l'envers / n'obéit pas). Carte apaisante dans la journée → le
   cauchemar « finit bien » tout seul (la carte entre dans l'écran et change le film). La
   carte réconfort de la télécommande a son emplacement à part, hors plafond de 4.
3. **Avatar et narration** : commande garçon/fille/carnation/cheveux visible comme dans le
   corps, mémorisée ; toutes les phrases existent au masculin et au féminin via une
   fonction d'accord dans les données.
4. **Décor Dehors piloté par les cartes** : on ne voit dehors que ce qui entre dans la tête.
5. **Loupe en laine complète**, animations d'ambiance en pause pendant la loupe ; budget de
   40 pièces filtrées hors lentille.

## 2026-10-29 — Spec validée, plan écrit, réalisation en sous-agents

Le propriétaire a validé la spec (« OK, tu peux y aller avec le plan détaillé et la
réalisation en sous-agents »). Plan : `docs/superpowers/plans/2026-10-29-dans-les-reves.md`,
19 tâches. Choix de fabrication fixés dans le plan :
- **Zéro build** : `index.html` reste la seule source ; les données et fonctions pures sont
  dans un bloc `/* PURE-BEGIN */ … /* PURE-END */` que `test/_load.js` extrait et exécute
  dans `vm` → `node --test test/` sans dépendance (Node 26).
- **Paramètres d'URL de test** `?vue=&temps=&theme=&lite=&cartes=` pour capturer n'importe
  quel état en Chrome headless (`test/shot.sh`) : c'est ce qui rend les 15 combinaisons
  × thèmes vérifiables à chaque tâche.
- Copies locales des aînés dans `refs/aines/` (ignorées par git) pour les patterns de code.
- Coordonnées anatomiques fixées en pixels de scène (dérivées de la recherche §2.8) pour que
  le dessinateur ne place pas l'hippocampe « au centre ».

## 2026-10-29 — Task 1 : squelette

`index.html` (toile, deux thèmes, paramètres d'URL), `test/shot.sh`, `shots/` ignoré.
Découvertes et choix non évidents :
- **Détection de la version allégée** : `performance.now()` brut au 2e `requestAnimationFrame`
  vaut ~140 ms en Chrome headless à froid alors que la peinture coûte ~10 ms (le script ne
  s'exécute qu'à ~135 ms : c'est le démarrage du navigateur). Avec la valeur brute, **toutes
  les captures `theme=feutrine` sortaient en version allégée**, identiques octet pour octet à
  `lite=1`. Mesure retenue : `performance.now()` entre l'exécution du script (fin du
  `<body>`, rien n'est peint) et le 2e rAF (après la 1re peinture), seuil 120 ms. Si une
  future scène chargée (40 pièces en laine) dépasse ce seuil en headless `--disable-gpu`,
  ajouter `&lite=0` aux captures qui doivent montrer la laine complète.
- **Polices** : la feuille Google Fonts non bloquante (`media="print"` + `onload`) faisait
  partir la capture headless avant les polices (titre en Chalkboard). Gardée bloquante,
  comme chez les aînés ; hors ligne, la requête échoue vite et le repli système prend le relais.
- **Curseur vertical `#cut`** : dans `.cut-wrap` (flex, 48 px de large), l'input de 200 px
  était rétréci par le flex avant la rotation (piste de ~110 px). `flex:none` sur `#cut`.
- **Épingle** : une seule `#pin`, tête `fill="currentColor"` + un cercle `#glassShade`
  (dégradé radial blanc→transparent→noir aux arrêts 0 / .25 / .85 / 1 des `#glassRed…`)
  posé par-dessus : même modelé de verre pour n'importe quelle couleur, donnée à l'usage
  `<use href="#pin" style="color:var(--glass-red)">`. Les trois dégradés `#glass*` restent
  définis (recopiés de la v10).
- **Riso** : `#scene>g` du plan devient `#scene-inner>g` (tous les groupes sont dans
  `#scene-inner` pour la loupe) ; les `.w` sont aussi en `multiply`, sinon deux pièces
  d'encres différentes du même groupe se cachent au lieu de se superposer. La règle riso
  est placée APRÈS `[data-lite="1"] .w` (même poids) pour garder `#riso` en riso allégé.
- **Toile** : `#linenGrain` (le grain du lin de la v10) est gardé à côté de `#paperGrain` :
  c'est lui que porte le « rect grain » de `#g-toile` en feutrine. La primitive `dyeGrey` de
  `#wool`, jamais lue, est retirée (rendu identique).
- **`#dusk` est horizontal** (blanc jusqu'à x = 42 %, puis la nuit vers la droite) : avec
  la seule opacité du rect `.nuit`, la moitié gauche de la scène reste en plein jour. La
  tâche qui pilote la nuit devra soit déplacer le dégradé, soit en faire un autre.
- **Règle `.w`** : aucune pièce ne porte d'attribut `transform` (la `transform` CSS du
  décalage d'encre riso le remplacerait) ; écrit en commentaire à côté de la règle CSS.

## 2026-10-29 — Objectif ajouté : « il faut que ce soit fun à utiliser »

Demande du propriétaire en cours de réalisation. Inscrit dans la spec (§2, critères
concrets : retour immédiat < 100 ms à chaque appui, cerveau-personnage, surprises,
récompenses, mouvement à ressort mais doux) et dans les Global Constraints du plan, pour
que chaque sous-agent et chaque reviewer le portent. Les tâches déjà faites (1) seront
reprises au polish (Task 18) pour les retours des boutons et curseurs.
- **Correction après revue (tour 1)** — *trame du lin* : le « rect grain » de la v10 (aplat
  `#e8ddc7` à .9 filtré par `#linenGrain`) **masque la trame à 90 %** ; la scène paraissait
  lisse à côté du `body`. Désormais le rect grain est blanc (neutre) en `mix-blend-mode:multiply` :
  il n'apporte que le bruit, la trame reste entière. *Isolation* : sans `isolation:isolate` sur
  `#scene`, les `multiply` de la scène traversaient le SVG et se multipliaient avec le fond de la
  carte (en riso, papier × papier → scène beige). *Onglet en arrière-plan* : rAF suspendus,
  donc la mesure d'allègement n'a lieu que page visible, et est refaite au retour au premier plan
  si la page se cache pendant le laps.

## 2026-10-29 — Task 2 : données

Bloc `/* PURE-BEGIN */ … /* PURE-END */` dans son propre `<script>`, avant le script
principal : cartes, modificateurs, 46 zones, deux jeux, histoire du pouce, télécommande,
gabarits de phrases, `inflect`, `lerpArr`. Aucun accès au DOM : Node l'exécute dans un
`vm` vide (`test/_load.js`), `node --test test/` → 15 tests.

**Choix non évidents.**
- **23 cartes, pas 22.** Le brief dit « 22 » mais énumère 23 slugs, et la table du spec
  §4.3 compte 23 cartes distinctes (« un câlin » est à la fois ressenti et réconfort). On
  garde les 23 cartes nommées. Conséquence pour la tâche du rêve : « toutes les paires »
  font 253, pas 231.
- **Accords prêts pour le générateur de rêve.** Le gabarit figé « {BASE} est devenu
  {GREFFE} {MODIF} » casse sur « la piscine », « les copains », « une glace tout petit ».
  Champs ajoutés (en plus de l'interface) : `g` (m | f | mp | fp) sur chaque carte et sur
  chaque `greffe`, et `f / mp / fp` dans chaque `MODIFS` (« toute petite », « multipliés »,
  « qui n'obéissent pas »). Le gabarit lui-même reste mot pour mot celui du brief.
- **`ton`** sur les cartes réconfort (« ta chanson », « ton doudou », « un câlin ») : la
  carte dit « ma chanson » (voix de l'enfant), la phrase `finitBien` dit « ta chanson ».
- **Toutes les cartes ont une `greffe`**, ressentis et réconfort compris (le plan dessine
  une greffe pour chacune) : `peur` → « de grands yeux tout ronds », `fache` → « des
  sourcils fâchés », `calin` → « deux grands bras », `chanson` → « des notes de musique ».
- **Entrées** : les choses vues par l'œil, tout le reste par l'oreille (spec §4.3) ; le
  doudou, chose qu'on voit et qu'on touche, par l'œil.
- **Textes de la télécommande génériques** : elle sert pour tout cauchemar (dragon, orage,
  j'ai eu peur…), donc « ce qui faisait peur » plutôt que « l'ogre ». Dans l'histoire du
  pouce, « tout redevient comme dans ta journée » = le pouce de bronze.
- **`{PRENOM}`** : une seule fois par étape et jamais en début de phrase, car l'appelant
  fait un seul `replace` et met « {il|elle} » sans majuscule quand il n'y a pas de prénom
  (testé). La phrase du matin utilise `{PRENOM}` pour « Le lendemain, … a raconté » : sans
  prénom, le texte est exactement celui du spec.
- **`inflect` sans avatar** → forme du garçon (celle de l'anecdote).
- **Honnêteté testée** : aucun texte ne contient « se repose », « chass », « tromp »,
  « poison », « vainc », « tué », « cassé », « erreur » ; « beaucoup de chercheurs pensent
  que » (amygdale, synapse), « les chercheurs ne savent pas encore tout » (vague) ;
  sommeil profond et sommeil paradoxal nommés une fois, puis « le grand sommeil calme » et
  « le sommeil des rêves ».
- **Faits qui épatent, vérifiés** : pouce 12 m ≈ maison de 4 étages ; cortex déplié ≈ une
  serviette de table (~0,25 m²) ; cervelet = plus de neurones que tout le reste (~69 sur
  86 milliards) ; des milliards de neurones, plus que de gens sur Terre ; 10 à 13 h de
  sommeil à 3-5 ans (AASM) ; la lune renvoie la lumière du soleil ; pinéale grosse comme
  un petit pois ; on grandit « un peu » en dormant (jamais « seulement »).

**Laissé de côté exprès.** Pas de `{VRAI}` par carte : le brief de la tâche du rêve en
décide (« c'est une statue » pour le pouce). Mais « c'est {VRAI} » rempli avec « ce n'est
pas pour de vrai » donnerait « c'est ce n'est pas pour de vrai » : à régler là-bas. De
même, les ressentis en `{C1}`/`{C2}` (« mélangé un vélo avec j'ai ri ») sonnent mal ;
`greffe.nom` est probablement le meilleur choix pour eux.

## 2026-10-29 — Task 3 : la tête et le cerveau

**Coordonnées retenues** (scène 900 × 560, centres des boîtes englobantes, plan ±10 px) :
tête x 159–507 / y 51–562, bout du nez (507,250), bouche (468–488, 294–309), œil-bouton
(456,194) r 10, conduit auditif (299,251), cou x 304–414 ; cerveau x 198–467 / y 84–300 ;
sillon central (330,88) → (380,226) ; sillon latéral (421,231) → (262,211) ; pôle temporal
(434,252) ; amygdale (356,248) ; hippocampe de (351,243) à (300,210) (queue enroulée vers le
haut) ; thalamus (335,200) ; hypothalamus (347,222) ; chiasma (375,232) ; hypophyse (371,253)
sur sa tige ; pinéale (300,196) ; corps calleux de (254,190) à (421,190), sommet y 154 ;
cervelet x 196–316 / y 258–327, corps centré ≈ (240,292), séparé du cerveau par ~10 px de
« coussin d'eau » ; tronc (320,243) → (330,334), pont bombé jusqu'à x 349 ; moelle x 323–338
jusqu'en bas du cou ; nerf optique de (449,197) à (375,232).

**Petites libertés anatomiques assumées.** Le chiasma est 4 px DEVANT l'hypophyse (recherche
§2.8 : « en avant de l'hypophyse ») alors que le plan les donnait dans l'autre ordre (365 vs
368). L'hypophyse est descendue de 7 px pour ne pas toucher l'amygdale : en projection
latérale elles se superposent vraiment (l'amygdale est 2 cm plus en dehors). Le tronc commence
à y 234 (et non 250) pour rejoindre le thalamus ; son sommet passe sous l'hippocampe. Le
cervelet a un petit « bras » (pédoncule) qui le rattache au tronc : séparé du cerveau, pas du
tronc.
**Trois écarts HORS de la tolérance de ±10 px** (ratifiés par le contrôleur au tour de
correction 1, déclarés ici) :
- sillon central : il finit en (380,226) et non (380,210) (16 px), pour rejoindre le sillon
  latéral ; sinon le frontal et le pariétal ne seraient pas séparés jusqu'en bas ;
- queue de l'hippocampe : elle monte jusqu'à (300,203) et non (300,223) (20 px), enroulée
  vers le splénium du corps calleux (Kenhub : l'hippocampe s'étend « jusqu'au splénium ») ;
- sommet du tronc : y 234 et non 250 (16 px), pour rejoindre le thalamus.

**Astuces de dessin.**
- Tracés générés UNE fois par un petit script Python + shapely (hors dépôt) à partir de points
  d'ancrage écrits à la main, puis figés dans le HTML : courbes de Catmull-Rom à tangentes
  bornées par la corde (pas de boucles). shapely a servi à trois choses impossibles à la main :
  (1) découper le cerveau en 4 lobes par les deux sillons et la ligne pariéto-occipitale,
  chaque lobe rentré de 2,4 px → le cortex (plus sombre, 2,6 px plus large que le cerveau)
  apparaît en creux entre les lobes : les sillons sont de vrais sillons ; (2) les bandes
  crâne / coussin d'eau / calotte de cheveux par différences d'offsets ; (3) les tubes
  effilés (hippocampe, nerf, corps calleux, tronc, moelle) = enveloppes convexes de cercles
  successifs.
- Le coussin d'eau est UNE pièce pleine sous le cerveau et le cervelet (union, +14 −5 px :
  fermeture qui comble l'espace entre lobe occipital et cervelet) : il ne se voit qu'en liseré.
- Cheveux : cercles posés sur le contour de la tête, rayon qui ondule (sinus, période 31 px)
  et s'amincit vers la nuque, + trois mèches de frange en tubes ; fils plus clairs brodés
  dessus (`.meches`, `color-mix` de `--hair`). Un épi en fil épais sur le dessus.
- Régions profondes (`.profond`) : opacité .85 + duplicata du tracé en `.fil.couture`
  (1,7 px, point plus long) ; l'hippocampe a un œil (nœud brun), l'hypothalamus deux aiguilles
  d'horloge brodées, le chiasma une croix brodée, l'oreille un petit escargot en spirale.
- Oreille à opacité .72 par-dessus le cortex (elle est à la surface, le cerveau est dessous).
- Visage prêt pour la nuit : `#p-paupiere` (laine peau) et `#fil-oeil-ferme` (courbe + 3 cils)
  à opacité 0 ; `#p-sourcil` est un `<g>` (la pièce .w dedans) pour que `.fronce` (transform
  CSS) ne remplace pas le décalage d'encre riso de la pièce ; pivot au bout arrière
  (442,183), `transform-box:view-box`. `#p-pineale.allume` : trois drop-shadow violets.

**Ce qui a raté.**
- Calotte de cheveux v1 (bande de 17 px + boucles r 8,5 tous les 17 px) : un cadre perlé
  brun, pas des cheveux. v2 (bande fine + petites boucles) : une chenille. v3 retenue : épaisse
  sur le dessus, ondulée large, effilée à la nuque, frange en mèches.
- Les mèches de frange disparaissaient : elles étaient soustraites avec l'intérieur de la tête
  (`difference(H.buffer(-6))`) ; il faut les unir APRÈS la soustraction.
- Riso v1 : cortex rose + lobes roses + tête jaune en multiply = rouge sang, thalamus noir,
  hippocampe invisible. Corrigé : cortex en voile (.4), régions profondes et oreille sans
  multiply (« imprimées en réserve »).
- Playwright MCP refuse `file:` : servir le dossier (`python3 -m http.server`, port libre ;
  8765 est déjà pris par autre chose) ; son `browser_resize` ne répond pas (fenêtre 420 px).
  Dans cette session Playwright les rAF sont ralentis (5,7 s pour deux images) et la page
  s'allège toute seule : ne pas en conclure que le rendu est lent. En Chrome headless 1400 ×
  1000 : premier rendu 5–22 ms (Task 1 seule : 14 ms), pas d'allègement.

**Budget mesuré** : `#g-dedans .w:not(.lite)` = **18** (dont `#p-cheveux-long`, caché chez
le garçon) ; 8 pièces `.w.lite` (pinéale, hypothalamus, amygdale, hypophyse, joue, œil,
paupière, sourcil).

**Avatar** : la 2e carnation (par défaut) prend la laine chair de la palette (#f1c19c /
#c98e66) au lieu de #f7c79c / #d9976a du corps, pour que la tête par défaut soit exactement la
palette du plan. Pastilles de 44 px (cible au pouce), pompons de laine.

## 2026-10-29 — Task 3, tour de correction 1

- **Générateur versionné** : `tools/gen-tete.py`. C'est un outil de dessin, pas livré (le seul fichier livré reste index.html). Il est autonome : le gabarit SVG est dans le fichier, il réécrit `#g-dedans`, et `--sec` affiche seulement les positions et les octets. Il lui faut shapely, à installer dans un venv (mode d'emploi en tête du fichier).
- **Tracés allégés** : tous les tracés passent en commandes relatives (`c`), avec des nombres courts (`.5`, aucun séparateur devant `-`). Chaque point absolu est arrondi au dixième AVANT le calcul de l'écart, donc l'erreur ne s'accumule pas. Les sommets à moins de 1,6 px du précédent sont retirés après `simplify`. Le joint de nombres est testé aller-retour sur 2000 tirages : « 1.2.5 » se relit bien 1.2 puis .5. **Données `d` de `#g-dedans` : 35 875 → 23 242 octets à dessin égal (−35 %)**, puis 24 799 octets (−31 %) après les ajouts de ce tour (trois coutures, sillons ondulés).
- **Riso, le cerveau était brique** : même en voile, le rose multiplié par la tête jaune donne du rouge brique. Option retenue : le cerveau entier (cortex, lobes, cervelet) est **imprimé en réserve** (`mix-blend-mode:normal`), comme les régions profondes. Le cortex y est un rose clair (`color-mix` encre rose 45 % / papier), qu'on voit dans les sillons. C'est l'option la plus propre : elle continue la règle déjà posée pour les régions profondes (réserve = sans multiply), alors qu'imprimer la tête en papier sous le cerveau aurait percé un trou blanc dans la tête jaune et cassé la silhouette.
- `#g-hippocampe` enveloppe la pièce, sa couture et son œil, et porte le `transform-origin` : on fera gonfler le groupe, jamais la pièce `.w` (le piège du décalage d'encre riso). `#p-bouche` reste un `.fil` : en riso, les fils n'ont pas de transform, donc rien à craindre.
- Jetons ajoutés : `--fil-bouche` et `--lueur-pineale`. Le fil du sourire devient la 3e valeur de `SKINS` (foncé sur les peaux claires, rose clair sur la plus foncée) : CSS ne sait pas choisir une couleur selon la luminance d'une variable. Une inversion `oklch(from …)` échouait sur les peaux moyennes.
- Pinéale agrandie (7 × 5,6) et cousue ; coutures aussi pour l'hypothalamus et l'hypophyse ; liseré clair (`.bord-bouton`, `--fil-blanc`) autour de l'œil-bouton.
- Sillons central et pariéto-occipital ondulés : un point d'onde (±4 px, alternant de côté) entre deux ancres du plan, les ancres sont inchangées.
- Budget inchangé : 18 `.w:not(.lite)`.

## 2026-10-29 — Task 4 : la vue Dehors, le monde de jour et de nuit

- **`<use>` de la tête : ce qui marche et ce qui ne marche pas (Chrome 156, mesuré).** Chrome
  style les clones d'un `<use>` en appliquant les règles du document AU CLONE, dans son arbre
  fantôme : un combinateur descendant ne voit pas les ancêtres hors de l'arbre fantôme.
  Banc d'essai minimal (`html .x{filter}` : rien sur le clone ; `.x{filter}`, attribut
  `filter=`, `style=` : oui ; `[data-x] #e{fill}` et `#orig #d{fill}` : rien). Conséquence
  pour l'enfant repris par `<use>` : **pas de laine** (`[data-theme=feutrine] .w{filter}`),
  **pas de riso** (encre, décalage, multiply), **pas de cheveux longs** pour la fille
  (`[data-genre=fille] #p-cheveux-long`), pas de version allégée. Ce qui suit bien : les
  règles posées sur l'élément lui-même (`.peau`, `#p-paupiere{opacity:0}`), les changements
  de classe / d'attribut / de style sur l'original (Chrome reclone), `#p-oeil ~ .trou` à
  l'intérieur du groupe cloné, et **les propriétés personnalisées** (héritées à travers le
  `<use>`) : un second banc d'essai montre `filter`, `transform`, `fill` et `display` pilotés
  par des variables posées sur `<html>` qui passent dans le clone.
- **Décision (contrôleur) : on garde `<use>`, et le thème, l'allègement et le genre passent
  par des variables CSS.** `<html data-theme / data-lite / data-genre>` reste la source (JS
  inchangé) ; ces attributs posent des variables (`--w-filter`, `--w-lite-filter`,
  `--w-blend`, `--encre-jaune/rose/bleu`, `--off-jaune/rose/bleu`, `--fil-filter`,
  `--fil-dash`, `--fil-dash-couture`, `--fil-encre`, `--riso-papier`, `--cheveux-long`), et
  les pièces les lisent par des règles posées sur elles-mêmes (`.w`, `.w.lite`,
  `.w[data-ink=…]`, `.fil`, `.fil.couture`, `.fil.bord-bouton`, `.trou`, `#p-cheveux-long`).
  Les exceptions riso de Task 3 qui visent des pièces NON reprises (cortex, lobes, `.profond`,
  liquide, `.oeil-hippo`, pinéale) gardent leur `[data-theme=riso]`. `#p-oreille`, repris,
  passe à `mix-blend-mode:normal` sans condition (en feutrine, c'était déjà normal).
  **Parité vérifiée** : Dedans avant (commit b159d89) / après, feutrine et riso, avec et sans
  allègement, garçon et fille : **0 pixel de différence** dans la scène (capture Chrome avec
  `--virtual-time-budget=4000` ; sans lui, deux captures riso du MÊME fichier diffèrent déjà,
  car la bascule de thème se fait par transition CSS et la capture part pendant la transition).
  Dehors : la tête reprise prend la laine, l'allégement, les encres riso avec leur décalage, et
  les cheveux longs de la fille. Vérifié aussi dans Firefox 156 (le navigateur du MCP Playwright).

### ⚠ Discipline de la tête partagée (à suivre par toutes les tâches suivantes)

Tout ce qui est DANS la tête (pièces de `#p-tete`, `#g-oreille`, `#g-cheveux`, `#g-visage` :
œil, paupière, sourcil, bouche, joue…) se style **soit par une classe / un attribut posé sur
l'élément original, soit par une variable CSS posée sur `:root`**, **jamais par un sélecteur
d'ancêtre** (`[data-temps="2"] #p-paupiere`, `body.nuit #p-oeil`, `#g-dedans .x`…) : le
clone `<use>` de `#g-dehors` ne le suivrait pas. Les deux têtes partagent donc toujours leur
état (œil fermé dans les deux vues, sourcil froncé dans les deux), et c'est voulu.
Pour un nouveau rendu par thème : une variable de plus sur `[data-theme=…]`, lue par une
règle sur l'élément.
- **Groupes ajoutés dans Dedans** (dans `index.html` ET dans le gabarit de `tools/gen-tete.py`,
  qui reproduit toujours le fichier à l'octet) : `#g-oreille`, `#g-cheveux`, `#g-visage`, pour
  reprendre l'oreille, les cheveux et le visage entier en trois `<use>`.
- **Tête chauve Dehors** : Dedans, les cheveux courts sont une BANDE autour du crâne (le cerveau
  remplit le reste). Dehors, sans cerveau, l'enfant était chauve. Ajout de `#p-calotte` :
  la tête H au-dessus d'une ligne de cheveux ondulée qui passe au-dessus de l'oreille, unie
  à la bande ; générée par `tools/gen-dehors.py`, qui charge la géométrie de `gen-tete.py`.
- **Fil droit invisible** : un `.fil` parfaitement vertical ou horizontal (hampe du drapeau,
  tringle) disparaît en feutrine : sa boîte englobante a une largeur nulle, donc la région du
  filtre `#thread` (en % de la boîte) aussi. Ces deux-là sont devenus de petites pièces `.w.lite`.
- **Composition** : fenêtre de la chambre en haut à gauche (l'écran du rêve occupera le haut
  droit, centré (700,170)) ; derrière le cadre, le ciel de nuit (`#p-ciel-lune` : vitre bleu
  nuit, `#g-lune > #p-lune`, `#g-etoiles`), et PAR-DESSUS le ciel de jour (`#p-ciel-soleil` :
  vitre bleu clair + soleil) que la nuit éteint — c'est ce que dit la zone « fenêtre » (« par
  la fenêtre, tu vois s'il fait jour ou nuit »). L'expo à droite, devant elle les quatre
  emplacements. La nuit : lampe à gauche, lit en bas, l'enfant couché tête sur l'oreiller.
- **Riso du décor** : les grandes surfaces en encre pleine étaient sombres (vitres, sol,
  expo, couverture bleu pétrole). Deux demi-teintes, `.pale` (35 % d'encre sur papier) et
  `.teinte` (60 %), lues par `--encre` que chaque `.w[data-ink]` pose sur lui-même ; le sol
  est un vert d'impression (jaune 55 % + bleu, à 62 % sur papier) ; `.w.reserve` (sans
  multiply) pour la lune, le soleil et la calotte, sinon le jaune sur bleu tourne au vert ;
  `#g-enfant-dehors` est isolé en riso, pour que la peau ne se multiplie pas avec le sol.
  Reste pour Task 7 : en riso, `#scene-inner>g` se multiplie avec la toile, donc la nuit
  assombrit aussi les pièces (en feutrine, non).
- **Couché (pour Task 7)** : pivot au cou (359,440) ; essai validé en capture :
  `#g-enfant-dehors{transform:translate(61px,-90px) rotate(-80deg) scale(.6)}`. La couverture
  `#p-couverture` est dessinée PAR-DESSUS l'enfant (elle le borde), le lit `#p-lit` dessous.

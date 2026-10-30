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

## 2026-10-29 — Task 3b : une tête « anatomiquement correcte »

Demande du propriétaire : « Pourras-tu faire une tête plus anatomiquement correcte ? ». Avant, la tête était un gros œuf avec une bosse pour le nez : pas de menton, pas de mâchoire, la bouche à la place du menton, le profil qui glissait tout droit dans un cou large, et une oreille en forme de « 6 ».

**Proportions retenues (enfant de 5 ans).** Référence : les proportions classiques de la tête d'enfant en dessin (A. Loomis, *Drawing the Head and Hands*, chapitre sur l'enfant), donc de mémoire, sans recherche en ligne, et recoupées avec les repères du brief :
- les yeux à mi-hauteur entre le sommet et le menton (sommet y 48, œil y 190, menton y 348) ;
- la base du nez vers les ¾ (y 266) ;
- la bouche dans le tiers inférieur du visage (jonction des lèvres y 297) ;
- l'oreille entre la ligne des sourcils et la base du nez ;
- un crâne très grand devant une face petite ;
- un nez court et retroussé, un menton peu avancé.

**Nouveaux repères** (scène 900 × 560) :

| repère | coordonnées |
|---|---|
| racine du nez (creux) | (486,194) |
| bout du nez | (507,249) |
| base du nez | (489,266) |
| lèvre supérieure | (492,284–292) |
| jonction des lèvres | (488,297) |
| **bouche brodée** | de (472,298) à (490,298), centre **(481,299)** |
| sillon sous la lèvre | (480,320) |
| menton | (484,333) en avant, (472,348) en bas |
| gorge | (424,376) |
| angle de la mâchoire | **(330,328)** |
| trou occipital | x 309–337 sous y 326, centre ≈ (323,340) |
| cou | x 301–419 sous y 440 |
| nuque | creusée de (301,452) à (184,340) |
| pivot du cou (inchangé) | (359,440) |

**Choix et écarts.**
- **Angle de la mâchoire en (330,328), pas en (330,365) comme le suggérait le brief.** Avec le menton à y 348, un angle à y 365 ferait DESCENDRE le bord de la mâchoire vers l'arrière. Or chez l'enfant, il monte vers l'oreille d'environ 10°. La première version (bord quasi horizontal à y 365) se lisait comme une sangle en travers du cou.
- **Trou occipital sous l'oreille, à x ≈ 323, pas derrière elle.** Le conduit auditif (300,250) et le tronc (plan : x 320–330) sont figés. Le bas du tronc recule de 8 px (dans la tolérance), et la moelle passe dans le tiers arrière du cou (x 322–338 sur 301–419).
- **Cerveau recalé** : seule la face orbitaire du lobe frontal remonte de 7 à 9 px, pour laisser la place au toit de l'orbite au-dessus de l'œil. Le reste du cerveau ne bouge pas.
- **Œil** : vu de profil, c'est une amande de laine blanche (`#p-oeil-blanc`, nouvel id), avec le bouton cousu à l'avant (`#p-oeil`, r 6,3), le bord de paupière et 3 cils brodés (`.cils`), le pli de la paupière et le creux vers le nez (`.pli`). `#p-paupiere` et `#fil-oeil-ferme` suivent l'amande. Le pivot de `#p-sourcil` passe à (444,181).
- **Mâchoire** : une fine ombre de laine `#p-ombre-cou` (lite, `--skin-shade` à opacité .3) court du dessous du menton à l'angle, puis le long de la branche montante.
- **Crâne** : la voûte va du sourcil à l'occiput. Le plancher est un anneau de 9 px autour du coussin d'eau (toit de l'orbite, fosse du lobe temporal, dessous du cervelet), percé du trou occipital.
- **Oreille** : un pavillon (hélix enroulé, anthélix, conque, lobe, tragus devant le conduit) de y 185 à y 288. Dehors, son `<use>` pose `--oreille-opacite:1` : une variable traverse le clone, alors qu'un sélecteur d'ancêtre ne le ferait pas.
- **Cheveux** : la lisière libère le front (vers (486,100)) et ne garde que deux petites mèches de frange. Dedans, la bande s'arrête au-dessus de la nuque creusée (y < 358). Dehors (`tools/gen-dehors.py`, `HAIRLINE`) : tempe, petite patte devant l'oreille, passage AU-DESSUS du pavillon (y ≈ 176), derrière l'oreille, puis la nuque.

**Ce qui a raté.**
1. Bord de mâchoire à y 365 : une sangle en travers du cou.
2. Grande ombre pleine sous la mâchoire : un col roulé.
3. Fil brodé le long de la mâchoire : trop dur, il coupait la moelle.
4. Nuque convexe, tirée en diagonale de l'occiput au cou : la tête posée sur un sac. Elle est maintenant creusée.
5. Cheveux coupés par `intersection(H.buffer(9))` : les boucles ont disparu. On ne coupe plus que sous la nuque.
6. Oreille à .72 Dehors : on voyait les cheveux à travers. Corrigé par la variable `--oreille-opacite`.

**Contrôles.**
- Les deux générateurs reproduisent `index.html` à l'octet (md5 identique après une seconde passe).
- `.w:not(.lite)` : 18 Dedans, 15 Dehors (plus 5 `<use>` ; la reprise ajoute au plus 4 pièces non lite).
- 0 `.w[transform]`, console propre, 15/15 tests.
- Pose couchée (−80° comme en Task 4, puis −90°) : la tête repose sur l'oreiller, le pivot (359,440) reste bon.
- Données `d` de `#g-dedans` : 24 799 → 27 290 octets (pièces du visage en plus).

## 2026-10-29 — Task 3b, passe 2 : crâne moins profond, nuque, cou

Retour du contrôleur sur la passe 1 : la tête restait un œuf, pour deux raisons. Le crâne était trop profond d'avant en arrière (370 px de long pour ~308 px de haut, rapport 1,2, alors qu'un enfant de profil est vers 0,9), et l'arrière de la tête descendait jusqu'à y ≈ 450 derrière le cou, comme un casque. Décision du contrôleur : la tête du plan passe de « x 150–520 » à « x ≈ 185–520 ».

**Proportions retenues.**
- **Occiput** : son point le plus en arrière est à x 187, vers la hauteur des yeux (y 190–232).
- **Voûte** : elle remonte vers l'avant jusqu'au sommet (peau y 56, cheveux y 42), un peu aplatie (sommet (330,56)–(386,57)).
- **Bas de l'occiput** : (205,323) → (248,344), juste sous le cervelet. La nuque descend ensuite vers l'avant et rejoint le bord arrière du cou en (312,352). Rien de la tête (peau ou cheveux) ne descend sous y 352 derrière le cou.
- **Cou** : x 312–408. Son bord avant sort du dessous du menton par une gorge douce : (452,357) → (436,363) → (422,374) → (412,396) → (408,440).
- **Moelle** : centres (323,328) → (334,580), dans le tiers arrière du cou, à 9 px au moins du bord.
- **Pivot** : toujours (359,440), au milieu du cou.
- **Rapport** : longueur peau 187→507 = 320 px pour une hauteur sommet → menton de 56→348 = 292 px, soit **1,10** (cheveux compris : 183→507 pour 42→348, 1,06). On ne peut pas descendre à 0,9 : la boîte de cerveau x 200–470 et la face jusqu'au nez (507) sont figées par le plan.

**Couches minces à l'arrière.** Le cerveau (pôle occipital x 199) et la peau (x 187) ne sont qu'à 12 px. On y loge, dans l'ordre : peau 2 px, os 5 px, coussin d'eau 3 à 5 px.
- Le coussin d'eau est désormais coupé à 7 px de la peau (`intersection(H.buffer(-7))`).
- Sous les cheveux, l'os monte jusqu'à 2 px de la peau (`H.buffer(-2) ∩ cap_keep`) ; au front, il laisse 7 px de peau.
- Les cheveux commencent à 2,5 px sous la peau (au lieu de 6), sinon ils cachaient l'os de l'arrière.
- Les boucles sont rases tout à l'arrière (`arriere` = 0 à x 187, rayon 3,6) : le bord des cheveux est à x 183.
- La frange garde ses mèches. La nuque a une courte lisière : les cheveux s'arrêtent à y 326, à la fois Dedans (`box(0,326,…)`) et Dehors (`HAIRLINE` finit en (204,330)).

**Cervelet.** Le plan le place à (240,290) r ~40, soit un bas à y 327. Avec un bas d'occiput à y ≈ 305 comme demandé, il sortait de la tête : pas de solution avec un recalage ≤ 10 px. J'ai sondé tous les décalages avec shapely, en mesurant la distance à la peau et l'écart au cerveau. **Retenu : (9,2), soit 9,2 px.** Il reste 8,9 px jusqu'à la peau (os et eau compris) et 3,1 px de coussin d'eau entre cervelet et lobe occipital, donc ils restent séparés. Pour cela, le bas de l'occiput descend à (205,323)–(248,344) au lieu de y ≈ 305.

**Ce qui a raté.**
- **Décalage (7,−7) du cervelet** : il touchait le lobe occipital (écart 0).
- **Contour d'occiput à y ≈ 305** : 380 px² de cervelet hors de la tête.
- **Moelle aux centres de la passe 1** : à 2 px du bord arrière du cou, une fois celui-ci passé à x 312 ; elle a été avancée de 4 à 6 px.

**Contrôles.**
- Générateurs reproductibles à l'octet : même md5 après deux passes.
- `.w:not(.lite)` : 18 Dedans, 15 Dehors.
- 0 `.w[transform]`, console propre, 15/15 tests.
- Pose couchée à −80° et −90° : la tête repose sur l'oreiller.
- Données `d` de `#g-dedans` : 27 021 octets.

## 2026-10-29 — Task 4, tour de correction 1 : la chambre, le soleil dehors, le riso

**Décision du contrôleur : la fenêtre appartient à la chambre.** Elle remplace le partage
jour / nuit du brief pour ces pièces. Trois attributs, pilotés par Task 7 :

| attribut | quand | pièces |
|---|---|---|
| `data-jour="1"` | le jour seul (t = 0) | `#p-ciel-soleil`, `#p-expo` |
| `data-chambre="1"` | du soir au matin (t ≥ 1) | `#p-fenetre` (cadre, tringle, rideaux, rebord), `#p-lampe`, `#p-lit`, `#p-couverture`, `#p-doudou` |
| `data-nuit="1"` | ce qui n'est QUE la nuit | `#p-ciel-lune` (la vitre de nuit, une pièce), `#p-lune`, `#g-etoiles`, `#p-lampe-lueur` |
| (aucun) | toujours | `#p-sol`, `#g-enfant-dehors`, les emplacements |

- `#p-lampe-lueur` est dans `#p-lampe` : son opacité s'ajoute à celle de la lampe (la lueur ne
  se voit que si la chambre ET la nuit sont là).
- **Le soleil est dans le ciel ouvert**, en haut à gauche ; plus de vitre de jour. La fenêtre de
  la chambre se pose au même endroit dès le soir. Le matin (soleil .8, chambre 1), on voit le
  soleil À TRAVERS la fenêtre, comme le dit la zone « fenêtre ».
- La lune et les 7 étoiles sont toutes DANS la vitre, entre les rideaux. Les 5 étoiles qui
  étaient hors du cadre ont été rentrées ou retirées.
- **Riso.** La vitre de jour (`.pale` multipliée sur la vitre de nuit) imprimait plus sombre que
  la nuit ; elle n'existe plus. La vitre de nuit est à pleine encre bleue, la lune en réserve
  dessus. Couverture, revers, matelas, oreiller et doudou passent en `.reserve` (sans
  multiply) : avant, le cou se voyait à travers la couverture et l'herbe à travers le matelas.
  Le grain du filtre `#riso` laisse toujours passer un peu de ce qui est dessous ; c'est le
  grain de l'encre, comme partout ailleurs.
- **Expo.** La fenêtre la plus à droite (x 838) dépassait du mur : elle est à x 826. Les deux
  fenêtres du toit chevauchaient la corniche (y 200–214) : elles sont passées dans la rangée,
  sous la corniche (y 226–248).
- **Jetons.** `--p-bois` pour la tringle, la hampe et le pied de lampe ; `--p-drapeau` pour le
  drapeau (avant : `--fil-rouge`, un jeton de fil). `--p-ciel-jour` est retiré, il ne sert plus.
- Mode d'emploi de `gen-dehors.py` : il renvoie au venv décrit dans `gen-tete.py`.
- **Contrôles.**
  - `.w:not(.lite)` = 14 Dehors + 4 de la tête reprise, soit 18.
  - 0 `.w[transform]`, console propre (riso et feutrine), 15/15 tests.
  - Les deux générateurs reproduisent `index.html` à l'octet.

## 2026-10-29 — Task 3b, passe 3 : proportions mesurées sur photo

Retour du propriétaire sur la passe 2 : « Ce n'est pas mieux ». Il a fourni deux photos de référence de profil (`refs/photos/`, ignorées par git). Elles n'ont servi qu'à mesurer : rien n'en est reproduit ni copié.

**Rapports mesurés** (verticalement, du sommet des cheveux = 0 % au bas du menton = 100 %) :

| repère | photo 1 | photo 2 | dessin |
|---|---|---|---|
| œil (centre) | 58 % | 60 % | 58 % |
| sourcil | 54 % | 56 % | 54 % |
| bout du nez | 64 % | 71 % | 72 % |
| base du nez | 71 % | 78 % | 78 % |
| bouche | 83 % | 89 % | 85 % |
| haut de l'oreille | 66 % | 62 % | 49 % |
| conduit de l'oreille | 77 % | 74 % | 65 % |
| bas de l'oreille | 88 % | 86 % | 81 % |
| occiput le plus en arrière | 47 % | 45 % | 58 % |
| nuque → cou | 91 % | 94 % | ≈ 99 % |
| longueur nuque → bout du nez / hauteur | 1,13 | 1,02 | 1,01 |
| épaisseur du cou / hauteur | ≈ 54 % | ≈ 51 % | 42 % |

- Sur la photo 1, la tête est renversée vers le haut d'environ 15 à 25° (le plan oreille–orbite monte vers l'avant). Le nez y remonte et l'oreille y descend : c'est ce qui explique l'écart entre les deux colonnes.
- Le conduit de l'oreille reste en (300,250), fixé par décision, avec la boîte de cerveau : 65 % au lieu des 74–77 % mesurés. C'est l'écart principal qui reste (voir le rapport).
- `shots/t3b-photo-vs-dessin.png` superpose ces rapports à la tête Dehors, sans rien reproduire de la photo.

**Ce qui a changé.**
- **Visage plus bas.** Repères (rapports au tableau) :
  - œil (458,228), à hauteur du pôle temporal (434,252) ;
  - nerf optique presque horizontal, de (446,229) au chiasma (375,232) ;
  - sourcil vers y 207–219, pivot de `.fronce` (442,218) ;
  - racine du nez (487,222), bout du nez (507,272), base du nez (489,290) ;
  - philtre court, jonction des lèvres (488,314), bouche brodée de (472,315) à (490,315), centre ≈ (481,316) ;
  - menton petit et rond, un peu en retrait : (482,349), bas (472,362) ;
  - joue pleine (449,288) ;
  - angle de la mâchoire (322,338).
- **Front en dôme continu**, le plus en avant en (499,162) ; plus de front vertical. **Sommet au-dessus de l'oreille** (310,52), plus de sommet aplati.
- **Occiput rond**, le plus en arrière en (186,228), à hauteur des yeux ; bas de l'occiput (204,323)–(244,342).
- **Nuque courte** qui rejoint le cou en (290,360). **Cou** x 292–428 (42 % de la hauteur) ; pivot inchangé (359,440). **Moelle** x 311–325, dans le tiers arrière.
- **Oreille** : pavillon descendu de 12 px (y 197–300) ; le conduit ne bouge pas.
- **Os du front** : il s'arrête au-dessus de l'arcade (y 188), la peau va jusqu'à l'œil. Le lobe frontal reprend sa face orbitaire d'origine, puisque l'œil n'est plus dessous.
- **Cheveux** :
  - plus ébouriffés, par une seconde ondulation de période 13 px ;
  - lisière haute sur le dôme (vers (490,112)) ;
  - patte devant l'oreille, puis passage au-dessus du pavillon (y ≈ 192) ;
  - courte lisière de nuque (vers (206,332)).

**Ce qui a raté.**
- **Os du front jusqu'à y 206** : quand le visage est descendu, un grand pan blanc couvrait le front. L'os s'arrête maintenant à l'arcade.
- **Lecture des proportions du contrôleur** (nez à 74 %) : elle plaçait le nez trop bas par rapport aux mesures (64–71 %). Le nez a été remonté de 6 px.
- **Captures « jour » Dehors** : masquer tous les `[data-chambre]` masquait aussi la fenêtre. On ne masque plus que le lit, la couverture, la lampe et le doudou.

**Contrôles.**
- `.w:not(.lite)` : 18 Dedans, 14 Dehors.
- 0 `.w[transform]`, console propre, 15/15 tests.
- Générateurs reproductibles (md5 identique).
- Pose couchée à −80° et −90° : correcte.
- Données `d` de `#g-dedans` : 27 140 octets.

## 2026-10-29 — Task 3b, passe 4 : la tête redessinée d'après les photos

Retour du propriétaire après la passe 2 (« Ce n'est pas mieux ») et constat du contrôleur après la passe 3 : la tête restait une **boîte** (arrière vertical, sommet plat, front droit, cheveux en casque, cou long et large, oreille trop haute), parce que le crâne épousait un cerveau en pain plat et que chaque passe ne bougeait qu'une ancre. Cette passe repart de la **silhouette entière**, tracée comme un illustrateur (dôme, occiput, nuque, visage, cou, col), puis le cerveau est posé dedans, puis le visage et les cheveux. Les photos (`refs/photos/`, git-ignorées) n'ont servi qu'à mesurer ; rien n'en est copié ni décalqué.

**Rapports mesurés sur les photos** (verticalement : sommet des cheveux = 0 %, bas du menton = 100 % ; la photo 1 est renversée vers le haut d'environ 15–20°, ce qui descend l'oreille et remonte le front) :

| repère | photo 1 | photo 2 | dessin (passe 4) |
|---|---|---|---|
| lisière du front | 38 % | 32 % | 34 % |
| sourcil | 57 % | 55 % | 56 % |
| œil (centre) | 62 % | 60 % | 60 % |
| bout du nez | 73 % | 73 % | 73 % |
| base du nez | 77 % | 77 % | 78 % |
| bouche | 85 % | 87 % | 86 % |
| haut de l'oreille | 72 % | 65 % | 61 % |
| conduit de l'oreille | 82 % | 76 % | 75 % |
| bas de l'oreille | 92 % | 86 % | 83 % |
| hauteur de l'oreille / hauteur de tête | 20 % | 21 % | 22 % |
| occiput le plus en arrière | 46 % | 44 % | 50 % |
| menton → haut du col | 14 % | 14 % | 20 % |
| longueur (arrière → nez) / hauteur | 1,22 (renversée) | 1,10 | 0,99 (peau 1,01) |
| conduit, en % de la longueur depuis l'arrière | 49 % | 31 % | 37 % |
| sommet, en % de la longueur depuis l'arrière | 56 % | 51 % | 49 % |
| front le plus en avant, en retrait du bout du nez | 17 % | 18 % | 3 % |
| épaisseur visible du cou / hauteur | ≈ 35 % | ≈ 34 % | 31 % |

Ce que montrent les photos et que le dessin reprend : un front qui bombe au-dessus des yeux et file sans cassure jusqu'au sommet ; le sommet au-dessus de l'oreille ; un occiput rond et plein ; un visage petit et bas (la face fait 45 % de la hauteur, sourcil → menton) ; une oreille petite (un cinquième de la tête) et basse, dégagée ; un cou court et fin, attaché loin en arrière, qui disparaît presque aussitôt dans le col ; des cheveux courts et ébouriffés, qui couvrent la nuque jusqu'au col.

**Nouveaux repères** (scène 900 × 560) :
- **Dôme** : sommet de la peau (340,44), cheveux jusqu'à y 31 ; front le plus en avant (497,182) ; lisière des cheveux sur le front vers (488,143).
- **Occiput** : le plus en arrière (186,198), cheveux à x 180 ; bas de l'occiput (199,300) → (210,326) → (232,340) ; nuque courte (256,348) → (280,356) → (300,366) → (311,378), qui rejoint le bord arrière du cou à x 316.
- **Cou** : x 316–418 (102 px, 31 % de la hauteur) ; gorge sous le menton (456,369) → (438,376) → (426,388) → (420,404) → x 418. Pivot `#g-enfant-dehors` **inchangé (359,440)**, au milieu du cou.
- **Col du pyjama** `#g-col` : `#p-col` (laine `--p-pyjama`, en réserve) de (296,432)/(324,429) à (438,452)/(450,464), puis le haut du pyjama x 272–456 jusqu'au bas de la scène ; `#p-col-bord` (lite, 20 px plus clair) est le bourrelet côtelé, cousu d'un fil blanc à son bord bas. Menton → col : 67 px (20 %).
- **Visage** (inchangé à 2 px près) : sourcil y 206–219, œil (458,228), racine du nez (487,222), bout du nez (507,272), base (489,290), bouche (481,316), menton (482,349)/(472,362), joue (449,288) ; angle de la mâchoire (322,340), ombre `#p-ombre-cou` du dessous du menton (456,370) à la branche montante (317,302).
- **Oreille** : le gabarit de la passe 3 réduit à 0,7 autour du conduit, puis descendu : pavillon x 272–309 / y 234–307, **conduit (300,280)** (le plus bas que le brief permette). Les fils de l'oreille (hélix, anthélix, lobe) subissent la même transformation (`ear_path`) ; l'escargot et le trou sont seulement descendus de 30 px.
- **Cerveau** : cortex plus rond et bombé, x 199–472 / y 62–300 (boîte permise x 195–475 / y 55–340) ; pôle frontal (472,150) derrière le front, dôme pariétal (322,62), pôle occipital (199,205). Sillons inchangés. Entre la peau et le cerveau au sommet : 2 de peau, 7 d'os, 9 d'eau.
- **Bloc profond** (corps calleux, thalamus, hypothalamus, pinéale, hippocampe, amygdale, hypophyse, chiasma, tronc, cervelet) translaté ensemble de **(4,−4)** (5,7 px) : thalamus (339,196), amygdale (360,244), hippocampe x 302–357, tronc (324,239) → (326,330), cervelet x 209–329 / y 256–325. Le nerf optique part toujours de l'œil (446,229) et rejoint le chiasma décalé (379,228). Les petits fils écrits à la main (stries du cervelet, aiguilles de l'horloge, croix du chiasma, œil de l'hippocampe) suivent le bloc par `shift()`.
- **Trou occipital** x 318–346 sous y 322 ; **moelle** (326,324) → (336,440), x 329–343, dans le tiers arrière du cou, puis sous le col.
- **Cheveux** (Dedans) : bande de boucles rayon 3 + jusqu'à 10,4 px, jamais rase à l'arrière (facteur ,3 + ,7·avant), effilée vers la nuque jusqu'à y 352 ; deux mèches de frange qui tombent sur le front (vers (498,150) et (486,134)) ; épi à (350,36). Dehors (`gen-dehors.py`, `HAIRLINE`) : lisière du front y 134, tempe, patte devant l'oreille, par-dessus le pavillon (y ≈ 226), derrière l'oreille, nuque couverte jusqu'à (306,358).

**Choix et écarts.**
- **Amygdale et hippocampe à 36 px au-dessus du conduit** (le brief disait ± 30 px « suffisant ») : le bloc profond ne peut pas descendre, car le cervelet, qui en fait partie, a besoin de ≥ 9 px d'os et de peau sous l'occiput arrondi (sondé avec shapely : à (0,0) il n'en restait que 4 ; à (4,−4), 10,0). Les deux restent dans la hauteur du pavillon (y 234–307), c'est ce que disent les textes.
- **Menton → col à 20 %** et non aux « 45–50 % » du brief : sur les deux photos, le col est à 14 % sous le menton ; 45 % mettrait le col à y 510, hors de la fenêtre y 430–475 demandée par le même brief. J'ai lu 45–50 % comme l'épaisseur du cou (cible des passes précédentes) et gardé un cou court.
- **Front en retrait du nez de 3 % seulement** (photos : 17–18 %) : le pôle frontal du cerveau (boîte jusqu'à x 475) impose un front ≥ 485 et le nez est plafonné à 510. C'est l'écart principal qui reste ; la tête est un peu plus haute que longue (0,99 contre 1,10).
- Le pédoncule du cervelet chevauche de 15 px² le bas du lobe temporal : il est caché sous le cortex (dessiné après). Le corps du cervelet garde 6,6 à 31 px d'eau sous le lobe occipital.
- Cheveux longs (fille) : le rideau passe DERRIÈRE le col, comme des cheveux rentrés dans le pyjama ; l'inverse (hair sur le col) demanderait le col sous la tête, donc sous la peau du cou.

**Ce qui a raté.**
1. Première version du col : un bloc uni avec un simple fil, qui se lisait comme un **bavoir**. Ajout du bourrelet clair `#p-col-bord` (lite).
2. Bloc profond à (0,0) : le cervelet à 4 px de la peau derrière l'occiput arrondi.
3. Riso : le pyjama à 40 % d'encre laissait voir le sol et le matelas au travers du grain ; passé à 55 %.
4. Patte de cheveux devant l'oreille (Dehors) en pointe de crochet : arrondie.

**Contrôles.**
- `node --test test/` : 15/15 ; console propre (Playwright, http://localhost:8793, `lite=0`).
- `.w:not(.lite)` : **19** Dedans (18 + `#p-col`), **14** Dehors (+ 6 `<use>`) ; 0 `.w[transform]` ; tous les ids présents ; `#p-tete` reste `class="w peau"` ; pivot calculé 359px 440px.
- Générateurs reproductibles à l'octet (même md5 après deux passes de `gen-tete.py` puis `gen-dehors.py`).
- Pose couchée à −90° : la tête repose sur l'oreiller, le col dépasse de la couverture, le pyjama passe dessous.
- Fille, peau 5, riso (Dedans et Dehors), allégé : captures `shots/t3b-apres-*`.
- Données `d` de `#g-dedans` : 29 169 octets (27 140 à la passe 3 : col et bourrelet en plus).

## Task 1b — Interface « Plein ciel », retrait du son (29/10)

**Ce qui est construit** (spec §6 bis, maquette « direction 1 ») : `.app` en une colonne : `header.bandeau` (titre + tagline courte, `#vue` segmenté à trois `button.seg[data-cut]` + pouce indigo glissant, `#reglages` « ⋯ ») ; `main.scene` (`.cadre` arrondi 24 px avec le SVG et le volet `#info`, puis `#rail`) ; `nav.dock` (`#jeu1` corail, `#jeu2` indigo, `#histoire` vert ; `#zones`, `#loupeBtn`, `#journee` sable à droite) ; `dialog#feuille` (avatar `.who` déplacé tel quel, `#theme`, `checkbox#lite`, `<details id="parents">` vide pour Task 17). Le SVG n'a pas bougé d'un octet (diff vérifié).

**Décisions.**
- Jetons `--ui-*` dans `:root`, indépendants des thèmes de scène ; les couleurs du rail sont figées (`--ui-soleil`, `--ui-nuit`… = valeurs de `--p-soleil`, `--nuit-2`) pour que le riso n'y touche pas. `--ui-ciel` (#9fc9ff, fond de l'icône du volet) vient de la maquette, hors liste de la spec.
- Polices : Fredoka + Nunito ; Baloo 2 retirée du lien (plus aucun usage : aucun texte dans le SVG pour l'instant ; le rêve écrit pourra la rajouter).
- Jetons retirés (plus lus par personne) : `--fibres`, `--grain`, `--pad`, `--r-card`, `--font-ui`, `--encre-douce`, `--ombre`. `--encre` reste : les pièces riso le redéfinissent localement et `.w.pale/.teinte` le lisent.
- `#cut` reste un `range 0..200` (vue × 100), désormais `hidden` : les segments le règlent ; `#time` reste `0..400` et devient le vrai contrôle du rail (`writing-mode:vertical-lr`, min en haut ; horizontal sur téléphone), piste et pouce transparents (pouce de 64 px). `#railBtn` est un dessin qui suit `--k = t/4` ; sa course = longueur moins 64 px, mesurée identique à celle du pouce (centre 491 px attendu, 491 px mesuré).
- `uiCut(c)` (c ∈ [0,2] : `aria-pressed`, pouce à `--c`, donc continu) et `uiTime(t)` (t ∈ [0,4] : `--k`, icône ☀️🌇💤🌙🐓 avec petit rebond, `aria-valuetext`) ne touchent qu'à l'habillage ; appelées par les gestionnaires `input` de `#cut`/`#time`. `setCut`/`setTime` (Tasks 6–7) les appelleront aussi.
- Aimantation : continu pendant le glissé ; au lâcher (pointerup sur window), 280 ms d'easeOutBack doux vers le cran le plus proche ; immédiat en mouvement réduit.
- Clavier (provisoire, à reprendre par Tasks 6–7) : ←→ temps ± 25 (0,25), ↑↓ vue ± 50 (0,5 ; ↓ = plus profond), partout sauf champ de saisie et feuille ouverte ; sur le rail focalisé, ces touches remplacent celles du navigateur. Échap ferme le volet ; la feuille se ferme par Échap (`cancel` → sortie animée), ✕ ou un appui sur le fond.
- Volet : `openInfo(opener, contenu?)` / `closeInfo()` (classe `open`) — voir « Fix round 1 ».
- Paramètres de test ajoutés : `?info=1` (volet ouvert) et `?reglages=1` (feuille ouverte), pour les captures.
- `html:not([data-pret]) *{transition:none}` : sans cela, le pouce de `#vue` glissait depuis « Dehors » au chargement (vu sur la capture `vue=1`). `data-pret` arrive deux images après le script.

**Ce qui a raté.**
1. Téléphone : la grille du bandeau en `1fr auto` débordait (min-content des segments `nowrap`) et le « ⋯ » tombait sur une 3e ligne : `minmax(0,1fr)` + `grid-template-areas`.
2. **Les captures « téléphone » de Chrome headless mentent** : `--window-size=420,900` donne une fenêtre de **500 px** (largeur minimale de Chrome, en `--headless=new` comme `old`) et le PNG est rogné à 420 : tout semblait déborder à droite. Mesuré (`innerWidth` = 500). Les captures téléphone sont faites avec Playwright (`setViewportSize 420×900`, viewport réel 420).
3. Mouvement réduit : l'aimant immédiat posait 300 puis le curseur natif reposait la valeur sous le doigt (289) à son propre mouseup, qui suit pointerup. L'aimant part donc à la tâche suivante (`setTimeout 0`).
4. Le « knob » cachait l'étiquette « jour » du rail horizontal : `--bord` 44 px sur téléphone.

**Contrôles.** `node --test test/` 16/16 (nouveau test : ni `speechSynthesis`, ni `id="sound"`, ni `id="say"`, ni `soundOn`, ni `reves.son`). Playwright (http://127.0.0.1:8794, `lite=0`) : console 0 erreur / 0 avertissement ; aucun élément au-delà de 420 px, `scrollWidth` 420 ; toutes les cibles ≥ 56 px ; segment, ↑, →, glissé (261 → 300 au lâcher), volet (Échap, ✕), feuille (Échap, ✕, `aria-expanded`), thème, genre, allégé (mémorisé) ; mouvement réduit : transitions à 0 s, pas d'animation de la feuille, aimant immédiat. Captures : `shots/t1b-bureau*.png`, `shots/t1b-tel*.png`.

**Fix round 1 (revue).** Corail `#ff7a59` → `#ff6038` (blanc 3,01:1 ; vert 3,02:1 inchangé) et gros boutons du dock ≥ 17 px partout (téléphone compris) : le seuil 3:1 « grand texte » s'applique. Rail à `right:-20px` (32 px sur la scène) ; la marge de page passe à 28 px sur bureau (`--marge`) car le bouton de 64 px dépasse alors de 26 px (débord de 2–4 px vu à 900–1024 px). Couleurs isolées en jetons (`--ui-gris-fonce`, `color-mix` sur `--ui-indigo` / `--ui-encre`). Étiquette « jour » à l'encre (blanc sur soleil : 1,6:1). Test « aucun son » renforcé (`prefs.get/set('son')`, `id='say'|'sound'` en guillemets simples). Feuille : sous-titres « Peau » / « Cheveux » (`aria-labelledby` des deux rangées) ; `#theme` devient un choix à deux boutons (🧶 Feutrine | 🖨️ Riso, `aria-pressed`, `data-theme-choix`), `setTheme` inchangé dans sa signature. **Pour Task 12 :** ouvrir le volet par `openInfo(opener, { emoji, titre, texte })` — le focus revient à `opener` à la fermeture (✕ / Échap), et le texte est écrit une image APRÈS l'ouverture, sinon la région `aria-live` (cachée par `visibility:hidden` jusque-là) n'est pas annoncée. Ne pas écrire `#infoText` avant `openInfo`.

## 2026-10-29 — Task 5 : la vue « Tout près », à hauteur de neurones

**Ce qui est dessiné** (`#g-pres`, tracés générés par `tools/gen-pres.py`, même venv et mêmes helpers que `gen-tete.py` ; reproductible à l'octet) : de l'arrière vers l'avant,
- une sous-couche unie `.sous-pres` (papier en riso) puis `#p-fond-pres`, laine rose pâle plein cadre (−20…920 × −20…580), un grain `.toile-grain` par-dessus ; deux volutes blanches terminées par un nœud (les plis) et 26 nœuds minuscules (`.loin`, « des milliards d'autres neurones ») ;
- `#g-vagues` (`data-phase="nuit"`) : trois bandes translucides bleu pâle (sinusoïdes de période 300 px, y ≈ 178 / 282 / 452) bordées de deux points de tige ;
- `#g-fuseaux` (`nuit`) : trois zigzags blancs en fuseau (amplitude qui enfle puis retombe), **posés sur les crêtes des vagues 1 et 3** et qui glissent avec elles — comme dans le vrai sommeil profond, où les fuseaux arrivent sur la crête des ondes lentes ;
- `#g-rincage` (`nuit`) : quatre gouttes bleu pâle (`.w.lite`) avec leur sillage brodé et un reflet ;
- `#g-neurones` : sept `<g id="p-neurone-N">` = corps + grosses dendrites en UNE pièce `.w` (tubes effilés unis par shapely, puis fermés buffer +3,2 / −3,2 pour que les branches sortent du corps par un congé), dendrites fines brodées en Y, noyau en nœud français, axone en couture épaisse qui finit par un bouton au bord d'une étincelle. Deux laines : rose (1, 3, 5, 7) et lilas (2, 4, 6) ;
- `#g-synapses` (`data-phase="synapses"`) : cinq étincelles (nœud jaune `#knotJaune` + 8 rayons brodés) entre N1→N2, N2→N3, N3→N4, N6→N5, N7→N6, et un influx jaune qui court sur l'axone de N1 ;
- `#p-cellule` (`nuit`) : une cellule verte qui bourgeonne (corps, noyau, petit bourgeon), dans un anneau cousu qui pulse.

**Budget.** 15 pièces `.w` dans la vue (brief : ≤ 20), dont 8 `.w:not(.lite)` (7 neurones + la cellule ; plafond 40). 0 `.w[transform]`. Données `d` : 32,8 ko (les vagues font 300 px de plus que le cadre de chaque côté pour la boucle).

**Animations (12 nœuds animés, tout en CSS, section « 7 quinquies »).** `.glisse` (vagues, translateX 0 → 300 px = une période, 8 s et 6,5 s, linéaire : boucle sans saut) ; `.rafale` (3 fuseaux, éclat opacité + échelle, 4 s) ; `.clignote` (2 enveloppes d'étincelles, opacité .35 ↔ 1, 2,8 s et 3,4 s) ; `.influx` (stroke-dashoffset sur `pathLength=100`, 2,8 s, réglé pour arriver sur l'étincelle s1 quand elle est la plus vive) ; `.descend` (2 enveloppes de gouttes, 7 s et 8,5 s) ; `.anneau` (scale 1 → 1,08, 3 s). Retards négatifs : les éléments ne démarrent pas ensemble.
- Mouvement réduit : la règle globale coupe tout. **Version allégée : `animation:none`** (et non `paused`) : la pose de repos montre tout (un fuseau en pause pouvait être figé éteint). **Loupe : `--pres-play:paused`** (variable posée par `html.loupe-active` ou `#scene.loupe-active`, lue par `animation-play-state:var(--pres-play, running)`) : pas de saut quand elle s'ouvre, et le clone `<use>` suit. *(Task 18 : depuis le tour 1, l'allègement passe par `--pres-anim:none` posé sur `[data-lite="1"]`, même effet ; la pause de la loupe est restée telle quelle.)*
- ~~⚠ **Synchronisation fuseaux / vagues**~~ *(obsolète depuis le tour 1 de Task 5, plus bas : il n'y a plus d'enveloppe qui glisse, chaque fuseau a une seule animation de 8 s qui finit éteinte ; texte d'origine gardé pour l'historique)* : l'enveloppe des fuseaux glisse avec `.glisse-1` (8 s) et revient de 300 px à chaque tour. Le saut est invisible parce qu'à t = 0, 8 s, 16 s… chaque fuseau est éteint (cycle de 4 s = 8 s / 2, retards −1,5 / −2,5 / −3,5 s, éteint dès 34 % du cycle). Si on change l'une de ces durées, garder la règle (écrite en commentaire dans le CSS). Et si une tâche relance les animations (display, classe), relancer les deux ensemble.
- Les fuseaux sont éteints la plupart du temps (éclat de ~1,4 s toutes les 4 s) : pour la zone « fuseau » (Task 12), prévoir une cible par la boîte de `#g-fuseaux`, pas par ce qui est visible.

**Riso (3 encres).** Fond rose en voile (`.voile`, 22 % d'encre), neurones rose et bleu pleins (multipliés), étincelles et influx en jaune, fils en bleu, fuseaux en réserve du papier (blancs) sur les bandes bleues.
- ⚠ `#g-pres` doit être en `mix-blend-mode:normal` en riso, sinon toute la vue se multiplie avec Dehors et Dedans dessous (on voyait la tête au travers). `[data-theme=riso] #g-pres` ne suffit pas : `#scene-inner>g` est plus fort ; la règle est `#scene-inner>#g-pres`. *(Task 14 : `#scene-inner>#g-pres{mix-blend-mode:normal}` sans condition de thème ; Task 18 : en riso, tous les groupes sont isolés et posés en normal.)*
- La sous-couche unie est indispensable : le filtre `#riso` ne couvre qu'à ~75 % (masque de bruit), le fond seul laissait voir les vues du dessous.
- **Ce qui a raté** : les bandes multipliées sur le rose viraient au mauve gris → imprimées en réserve (normal, .8). La cellule verte (réserve) sur le rose, à 75 % de couverture, devenait olive délavé, et les gouttes gris ardoise → sous chacune, un `.papier-pres` (même tracé, papier en riso, `fill:none` en feutrine) : le rose y est « réservé », comme en vraie impression. Vert = `color-mix(in oklab, jaune 62 %, bleu)`.

**Feutrine, ce qui a raté.** Le fond en laine complète (`#wool`) sur 940 × 600 px : les bouloches, calibrées pour de petites pièces, devenaient une poussière de petits carrés gris partout. Le fond est donc `.w.lite` (découpe + halo + ombre, tous hors cadre) avec le grain de la toile par-dessus : surface calme, et bien moins coûteux. Premier jet : plis en fil rose foncé (des cheveux tombés sur la laine) → volutes blanches, deux retirées ; fuseaux blancs sur le rose pâle (presque invisibles) → posés sur les bandes bleues ; étincelles trop petites (r 4,2) → r 5,6, 8 rayons de 15 px ; gouttes sous le rail (x 845) → toutes à x < 810.

**Pour les tâches suivantes.** Task 7 : la vue est opaque, donc la toile qui s'assombrit ne se voit pas ici ; si la nuit doit se lire Tout près, il faudra un voile propre à `#g-pres`. Task 14 : *(corrigé au tour 1 de Task 5 puis par Task 14)* les règles de la vue passent par des variables, le clone `<use>` de la loupe les suit.

Contrôles : `node --test test/` 16/16 ; console 0 erreur / 0 avertissement (feutrine et riso, Playwright, http://localhost:8796, `lite=0`) ; deux mesures à 2 s d'écart : vagues 26 → 101 px, gouttes −0,4 → 20 px, étincelle .36 → .83 ; `lite` → `animation:none`, loupe → `paused` (valeurs figées sur 0,8 s). Captures : `shots/t5-feutrine.png`, `t5-riso.png`, `t5-repos.png` (mouvement réduit), `t5-riso-repos.png`, `t5-lite.png`, `t5-pw-a/b.png` (2 s d'écart).

### Task 5, tour de correction 1

- **Fuseaux robustes par construction** : plus d'enveloppe qui glisse. Chaque fuseau a UNE animation de 8 s qui combine la translation (0 → 300 px, linéaire : 3 px par %) et ses deux éclats, opacité 0 à 0 % et 100 % : le retour se fait toujours éteint, quels que soient les retards. Trois jeux d'images clés (éclats à 4/54, 18/68, 32/82 %) au lieu de retards, pour que chaque fuseau reste sur sa crête. 11 nœuds animés.
- **Règles de la vue joignables par un clone `<use>`** (loupe, Task 14) : plus de sélecteur d'ancêtre, hormis `[data-theme=riso] #scene-inner>#g-pres` (le groupe lui-même). Le riso passe par des variables posées sur `[data-theme=riso]` (`--pres-bande-op/-blend`, `--pres-pli-op`, `--pres-loin/-op`, voile par `.w.voile[data-ink]{--encre:color-mix(… var(--encre-rose) 22% …)}`) ; l'allègement par `[data-lite="1"]{--pres-anim:none;--pres-lueur:none}` (`animation-name:var(--pres-anim, …)`, lueur des étincelles coupée) ; la pause par `--pres-play:paused` posé sur `html.loupe-active` ET `#scene.loupe-active`, lu par `animation-play-state` (règle placée après les raccourcis `animation`, qui remettent `running`). ⚠ **Task 14 : pour figer le clone de la lentille, poser `--pres-play:paused` sur le `<use>` de la lentille, ou la classe `loupe-active` sur `html` (ou `#scene` si la lentille est dedans)** : les variables traversent le clone, les classes d'ancêtre non.
- Gouttes riso : pleine encre bleue (elles étaient grises et pâles en `.pale`) ; reflet en `--fil-blanc` en feutrine ; `.clignote` déclaré une seule fois ; traits des étincelles, sillages et fuseaux en commandes relatives (plus aucun `L` absolu ; `#g-pres` 42,2 ko).
- Contrôles : 16/16 ; console propre ; `getAnimations()` sur `#g-pres` = 11 en cours, 0 en allégé, 11 en pause sous `#scene.loupe-active` comme sous `html.loupe-active`, 0 en mouvement réduit ; générateur reproductible à l'octet.

## Task 6 : curseur VUE (fondu Dehors / Dedans / Tout près)

- **`setCut(c)`** (global, c clampé à [0,2]) est le seul point d'entrée : opacités `#g-dehors = 1-min(1,c)`, `#g-dedans = 1-|c-1|`, `#g-pres = max(0,c-1)`, `#g-ecran` et `#g-boite` = `1-max(0,c-1)` ; `body.dataset.vue = round(c)` ; classe `.active` sur la vue arrondie (les autres ont `pointer-events:none`) ; `#cut` synchronisé ; `uiCut(c)` appelé. `?vue=` est lu au chargement (`setCut` initial). L'événement `input` de `#cut` appelle `setCut`.
- **Une vue à opacité 0 est aussi `visibility:hidden`** (jamais `display:none` : il relancerait les animations CSS et forcerait un reflow) ; à opacité > 0 elle est `visible`. Ainsi seules les vues visibles sont rendues : le budget des filtres de laine est réel (à `vue=2`, Dehors et Dedans ne coûtent rien).
- **`animateCut(cible, ms = 500)`** (global, pour la Task 15) : glisse `c` en `requestAnimationFrame`, ralentie en fin (ease-out cubique), appelle `setCut` à chaque image ; immédiat en mouvement réduit. Les segments l'appellent.
- **Clavier** : le gestionnaire unique de la Task 1b est repris. ↑↓ appellent `pasCut(±0,5)` ; après 450 ms de répit la vue glisse (250 ms) vers la vue voisine dans le sens de la touche (`ceil` pour ↓, `floor` pour ↑, donc ↑ depuis 2 va bien à 1). ←→ (temps) inchangés, pour la Task 7.
- **« Tourner de page »** : la vue qui s'efface grossit de 2 % (`scale(1 + .02·(1-op))`, transform CSS posé en style sur le groupe, `transform-box:view-box; transform-origin:center`), retiré à opacité 0 ou 1 et en mouvement réduit. Aucune pièce `.w` ne porte de transform.
- À `vue=0.5` les deux têtes se superposent sans décalage (la tête est partagée) ; en riso, les groupes se multiplient et le résultat reste lisible (pas de fantôme décalé). `#g-pres` reste en `normal`, donc seule la vue 2 est opaque.
- Contrôles : 16/16, console 0 erreur / 0 avertissement ; clic sur chaque segment, ↑↓ au clavier, `?vue=2` au chargement vérifiés (opacité, visibility, pointer-events, aria-pressed). Captures : `shots/t6-v0.png`, `t6-v1.png`, `t6-v2.png`, `t6-v05.png`, `t6-riso0.png`, `t6-riso05.png`.

## Task 7 : curseur TEMPS (la journée, le soir, les deux nuits, le matin)

- **`setTime(t)`** (global, t borné à [0,4]) est le seul point d'entrée. Les tables `TEMPS` (une ligne par effet, 5 valeurs `[jour, soir, profonde, rêves, matin]`) passent par `lerpArr`. Elles sont reprises telles quelles du brief et des décisions du contrôleur : nuit `[0,.55,1,1,.1]` ; `data-jour` `[1,.3,0,0,.8]` ; `data-chambre` `[0,1,1,1,1]` ; `data-nuit` `[0,.6,1,1,.2]` ; `data-decor` `[1,.5,0,0,.6]` (prête pour Task 8) ; couché `[0,.5,1,1,0]` ; paupière `[0,1,1,1,0]` ; pinéale `[0,1,.6,.4,0]` ; rem `[0,0,0,1,0]` ; zzz `[0,0,1,1,0]` ; amygdale `[0,0,.3,1,0]` ; Tout près `data-phase="nuit"` `[0,0,1,.2,0]` et `"synapses"` `[1,.5,.2,1,.8]`. setTime pose aussi `body.dataset.temps = round(t)`, `#time` (t × 100) et `uiTime(t)`.
  - Il émet `temps` (`{t, phase}`) une fois par changement de phase arrondie. Rien n'est émis au chargement (ce n'est pas un changement) : un abonné lit `document.body.dataset.temps` ou `tempsCourant` à son initialisation.
  - `?temps=` est lu au chargement.
  - **`animateTime(cible, ms = 600)`** : même mécanique qu'`animateCut`.
- **Têtes partagées.** Les variables sur `:root` sont `--paupiere-op`, `--pineale-lueur` et `--amygdale-lueur` (plus `--nuit` pour la toile). Les classes sont posées sur les éléments eux-mêmes : `.allume` (pinéale), `.lueur`/`.pulse` (amygdale), `.cligne` (paupière et œil fermé, le jour), `.rem` (œil fermé brodé, nuit des rêves). Aucun sélecteur d'ancêtre.
  - Le va-et-vient `rem` est sur `#fil-oeil-ferme` et non sur `#p-oeil` : le bouton est une pièce `.w` cachée sous une paupière opaque, et une transform l'aurait privé de son décalage riso.
  - La lueur de l'amygdale bat grâce à une propriété enregistrée (`@property --amygdale-pouls`) animée, lue dans les rayons des `drop-shadow`. Un filtre avec `url()` ne s'interpole pas.
- **Nuit de la toile.** Le dégradé horizontal `#dusk` est supprimé. `.nuit` est un aplat `--nuit-3` en multiply, d'opacité `--nuit × --nuit-max`.
  - Plafond feutrine **.8** : la trame du lin reste visible, et les pièces (en `normal`) gardent tout leur contraste.
  - Plafond riso **.4** : tous les groupes s'y multiplient avec la toile. À .5, tout tournait au gris-mauve terne (tête ocre, draps boueux) ; à .4, c'est lisible. *(Remplacé en Task 18 : groupes isolés en normal, nuit riso bleue à .65.)*
  - Le « `.nuit` en `normal` » proposé par la décision 4 n'aurait rien changé : les groupes au-dessus se multiplient de toute façon avec la toile.
- **Lueur de la lampe** : `mix-blend-mode:screen`, `fill-opacity:.8`. Elle éclaire la toile assombrie au lieu d'être salie par elle. En `normal` à .55, la nuit transparaissait.
- **Riso, œil fermé** : la paupière se multipliait avec le bouton bleu, et l'œil « fermé » restait vert et ouvert. La paupière est donc en réserve, et le bouton, ses trous et son liseré s'effacent avec `1 − --paupiere-op`. Le masque de bruit du filtre `#riso` ne couvre jamais tout.
- **L'enfant de Dehors (écart assumé).** La translation et l'échelle (« dans son lit ») suivent la table **chambre** ; la rotation (« couché ») suit la table **couche**.
  - En appliquant tout sur la table couche, le matin (chambre 1, couché 0) mettait l'enfant debout en grand, derrière la couverture qui lui cachait la bouche et le menton : un orphelin.
  - Maintenant, le soir il est assis dans son lit à moitié allongé (−40°), la nuit couché, et le matin assis, réveillé, la couverture sous le menton.
  - Pose de nuit recalée de (61,−90) à **(72,−74)** (rot −80°, échelle .6) pour rentrer le col sous la couverture. La tête s'enfonce un peu plus dans l'oreiller.
- **`#g-zzz`** : trois z brodés (fil `--nuit-2`) sur le lobe frontal, entre le sillon central et les volutes. Ajouté aussi au gabarit de `tools/gen-tete.py`, pour qu'une régénération ne le perde pas (non relancée : shapely absent ici).
- **Animations d'ambiance.** Même mécanique que Tout près, avec des variables propres : `--amb-anim:none` en allégé, `--amb-play:paused` sous `html.loupe-active` / `#scene.loupe-active`. Le mouvement réduit coupe tout par la règle globale. La liste :
  - clignement de l'œil le jour ;
  - respiration ×1,01 de `#g-dedans` et de `#g-enfant-dehors`, par la **propriété `scale`**, qui se compose avec la transform du fondu (Task 6) et du coucher au lieu de l'écraser ;
  - frémissement du point des sillons et du cervelet (`stroke-dashoffset`) ;
  - scintillement des 7 nœuds-étoiles ;
  - pouls de l'amygdale ;
  - « zzz » qui montent (au repos : immobiles et visibles) ;
  - va-et-vient REM.
  - ⚠ La règle `animation-play-state` inclut `#scene-inner>#g-dedans` pour que `:is()` soit plus spécifique que le raccourci `animation`.
- **Surprises** (pas en mouvement réduit) :
  - clin d'œil de la lune une fois sur dix en passant du jour (ou du matin) au soir ou à la nuit ;
  - bâillement (`#p-bouche`, scale) au passage nuit des rêves → matin.
  - Les classes sont posées sur les fils eux-mêmes et retirées à la fin de l'animation.
- **Clavier et aimantation.**
  - ←→ appellent `pasTemps(±.25)` ; après 450 ms, le moment voisin dans le sens de la touche (comme ↑↓).
  - `animateCut` vide `posCut` : un clic sur un segment annule l'aimantation ↑↓ en attente (mineur de Task 6), et l'entrée `#cut` aussi.
  - La saisie sur le rail et `pointerdown` annulent `animTemps`/`posTemps` ; l'aimant du rail passe par `setTime`.
- **Ce qui a raté.**
  - Lueur de l'amygdale en rose sur le cerveau rose : invisible. Elle est maintenant blanche + rouge vif.
  - Pose de Task 4 (61,−90) : le col dépassait de la couverture.
  - Translation sur la table couche : la couverture sur le visage le matin.
  - `--virtual-time-budget` de Chrome avec des animations infinies ne rend jamais la main : ne pas l'utiliser pour lire la console.
- **À surveiller.** Tout près reste rose la nuit : la vue est opaque, la toile assombrie ne s'y voit pas, et la nuit s'y lit par les métiers. La respiration redessine toute la tête filtrée à chaque image, comme les animations de Tout près ; si une tablette peine, c'est la première à couper.
- **Contrôles.**
  - `node --test test/` : 16/16.
  - 15 captures `shots/t7-v{0..2}-t{0..4}.png`, plus `t7-riso-v0-t2.png` et `t7-riso-v1-t3.png`.
  - Playwright (Firefox 156, http://127.0.0.1:8801, `lite=0`) : console 0 erreur / 0 avertissement ; `temps` émis une fois par phase (0→3,9 : 1, 2, 3, 4) ; `animateTime(3)` OK ; glissé du rail 2,19 → 2 au lâcher ; → sur le rail 2,25 puis 3.
  - ↓ puis clic sur « Dehors » : on reste à Dehors.
  - Loupe : `paused` ; allégé : `none`.
  - Mouvement réduit : 0 animation, `animateTime` immédiat, pas de bâillement.
  - 0 `.w[transform]`, un seul `keydown`.
- **Task 7, tour de correction 1.**
  - Le sol et les touffes d'herbe tirent vers `--nuit-3` (à 40 % en feutrine, 20 % en riso, par `--sol-nuit`). La règle riso du sol passe par une variable (`--sol-base`).
  - L'expo quitte la table du soleil : `#p-expo` a sa propre table, `[1,0,0,0,.3]`, par une entrée par id (`DECOR_ID`). Le balisage de Dehors ne change pas, et `gen-dehors.py` le reproduit toujours.
  - Amygdale en rêve : liseré clair, deux anneaux serrés, deux couronnes rouges et un halo.
    - ⚠ En riso, `url(#riso)` avale les `drop-shadow` qui le suivent (mesuré en Chrome). Les glandes allumées y sont donc imprimées à plat (`--glande-base:saturate(1)`). Cela explique aussi pourquoi la lueur riso de la pinéale de Task 3 ne s'est jamais vue.
    - En riso, l'amygdale allumée est rose × jaune (`#ff4631`), avec des couronnes jaunes et un halo papier : rouge ou rose sur le rose du cerveau, rien ne se voyait.
  - La pinéale bat (`@property --pineale-pouls`, intensité selon `--pineale-lueur`). Sa règle riso passe par des variables (`--pineale-c1..3` : papier et bleu pâle).
  - `setCut` pose `--amb-play` et `--pres-play` à `paused` sur une vue à opacité 0, puis les retire quand elle revient, pour que l'héritage de la loupe reste intact. Mesuré : à Dedans, 8 animations en pause dans Dehors, 11 dans Tout près, 7 en cours dans Dedans.
  - **La lune a deux yeux** (demande du propriétaire : « la lune n'a qu'un œil »).
    - `#fil-lune-oeil` est à (61,79), le nouveau `#fil-lune-oeil-2` à (72,79), séparés de 11 px : le croissant n'a que 22 px de large à leur hauteur. Le sourire est centré dessous.
    - Le clin d'œil ne ferme que l'œil gauche (`#fil-lune-clin` déplacé en `M57 79`) ; l'autre reste ouvert.
    - Fait aussi dans `tools/gen-dehors.py` (géométrie `lune-oeil` / `lune-oeil-2` / `lune-clin` et gabarit) pour qu'une régénération garde les deux yeux. Le script n'a pas été relancé : shapely est absent ici.

## Task 8 : les cartes-souvenirs (boîte, épingles, journée de 4 cartes, entrée dans la tête)

- **Dessins** (`tools/gen-cartes.py`, sans dépendance, reproduit le bloc `<!-- CARTES-BEGIN -->…<!-- CARTES-END -->` de `<defs>` à l'octet) : 23 vignettes `#v-<slug>` (40 × 40, centrées sur 0,0), 14 décors `#d-<slug>` (les 14 cartes `base:true`, doudou compris), `#ic-oeil` / `#ic-oreille` (la porte d'entrée brodée au bas de chaque carte : on apprend par où chaque souvenir entre). Les « mots entendus » sont dans une bulle de parole bleu pâle. Les décors des choses vues sont les vignettes dont les tracés sont multipliés par ~2,2 (jamais de `transform` sur un `.w`) ; les gens sont dessinés debout, à part ; le pouce de César est dessiné pour `#slot-1` : socle à y 452, ongle à y 196 de la scène, bronze (`--p-pouce` passe de #b9b2a0, inutilisé, à un bronze #a8713a ; Task 11 le reprend). Tout est `.w.lite` : 0 pièce non allégée ajoutée (Dehors reste à 14 + 4).
- **Filtres** : `#woolLite` coupait net (en carré) le halo et l'ombre des petites pièces, sa région n'étant que −16 % de la boîte englobante. Deux copies à région plus large : `#woolVignette` (région FIXE 56 × 56 en `userSpaceOnUse`, bornée quelle que soit la pièce) pour les vignettes, `#woolMini` (−60 % / 220 %) pour les décors. Classes `.vig` / `.mini`, variables `--w-vig-filter` / `--w-mini-filter` (riso : `#riso`).
- **Riso dans un clone `<use>`** : `.pale`/`.teinte` sont des sélecteurs d'ancêtre, inutilisables. Classes posées sur la pièce : `.pastel[data-ink=…]` (encre sur papier), `.orange`, `.brun` (variables `--encre-orange`, `--encre-brun`), `.vert`/`.vert-fonce` (Task 5). Un décor est isolé en riso (`--decor-iso`) et le pouce a une sous-couche de papier (`.papier-pres`) : sans elle on voyait l'expo au travers.
- **Boîte** : `#g-boite` > `.boite-grise` (bac `#p-boite` + `#boite-rail`) + `#g-vols` + `#bulle-boite`. Défilement **par translation** de `#boite-rail` (glisser au doigt avec un peu d'élan, molette, focus clavier qui ramène la carte en vue), pas de `<svg>` imbriqué : le `<svg>` racine coupe déjà ce qui dépasse. Le glissé ne capture le pointeur qu'au-delà de 8 px (un appui reste un clic) ; `touch-action:pan-y` sur la boîte. Le glissé ne touche pas `#time` (hors SVG). Riso : `#g-boite` en `normal` (comme `#g-pres`) avec une sous-couche de papier.
- **Épingles** : seulement sur les cartes choisies (rouge / bleu / jaune selon le rang de la carte) ; la carte se soulève de 2 px et l'épingle tombe avec `cubic-bezier(.34,1.56,.64,1)`. Doublon : la carte tremble. Appui : la carte s'enfonce (< 100 ms).
- **Bulles** : dessinées DANS la scène, au-dessus de la boîte, queue vers la carte, 3 s (un appui la ferme), annoncées par `#boite-annonce` (`aria-live`). Pas le volet `#info` : il monte exactement sur la boîte et la cachait. Textes dans le bloc PURE (`BULLES`) : « Oups, trop de choses ! », « Le cerveau dort, on choisira demain ! » (moments 2 et 3), et au matin (moment 4, aussi refusé : t ≥ 2) « Pour choisir, touche « Nouvelle journée » ! » — dire « le cerveau dort » au réveil aurait été faux.
- **Nuit** : moment arrondi ≥ 2 → classe `dort` sur `#g-boite` (variables `--boite-op:.45`, `--boite-filtre:saturate(.2)` lues par `.boite-grise`, l'opacité de `#g-boite` reste à `setCut`), `aria-disabled` sur les cartes, refus avec bulle. Abonné à `temps`, lu aussi au chargement.
- **Décor** : `#decor-<slug>` `data-decor="1"` (Task 7 l'éteint la nuit ; l'opacité est posée dès l'insertion). Le pouce prend toujours `#slot-1` (l'occupant est déplacé) ; les autres prennent `#slot-0, 2, 3, 1` dans cet ordre ; les gens vont dans `#slot-gens`, côte à côte tous les 62, recentrés (transition). L'orage est dessiné haut dans le ciel au-dessus de son emplacement.
- **Voyage** : l'état (décor, vignette d'hippocampe, épingle) est posé TOUT DE SUITE ; les animations (Web Animations) ne sont que du dessin. Vue arrondie 0 : la vignette vole de la carte au décor qui sort de terre (rebond) — ou, sans décor, entre dans l'œil / l'oreille de l'enfant. Vue 1 : carte → œil (458,228) ou oreille (300,280) → thalamus (335,200) → sa place dans l'hippocampe, 1,2 s ; la petite carte apparaît, son épingle tombe, `#g-hippocampe` gonfle (1 → 1,08 → 1, 400 ms). Mouvement réduit ou `anim:false` : rien ne bouge, tout est posé.
- **Hippocampe** : `#g-hippo-cartes` (dans Dedans, après le nerf optique), une petite carte crème `.hippo-carte[data-slug]` par carte, en éventail juste SOUS la courbe de l'hippocampe (posées dessus, elles le cachaient entièrement), épingle plantée dans son bord. Une carte retirée : les autres glissent d'une place.
- **API** : `journee`, `pickCard(slug, {anim, forcer})` (renvoie true/false ; `forcer` passe outre la nuit : `?cartes=` au chargement, et le récit guidé de Task 15, qui appelle `pickCard` avant `setTime(0)`), `resetDay()` (ne touche pas au temps), le bouton `#journee` = `resetDay()` + défilement à 0 + `animateTime(0)` (spec : « remet le temps au matin » de la journée). Événement `journee` (copie du tableau) à chaque changement.
- **Ce qui a raté** : (1) la lunule et le bord de l'ongle du pouce faisaient une bouche triste : l'ongle a maintenant un bord libre clair en haut et la peau brodée autour de sa base ; (2) les arcs blancs du nuage d'orage faisaient des yeux ; (3) un trait vertical (pot d'échappement) a une boîte englobante de largeur nulle : filtre vide, pièce invisible → petite pièce ; (4) premier essai des places de l'hippocampe : les 4 cartes couvraient tout l'hippocampe ; (5) riso : le pouce gris mauve et transparent → encre brune plus chaude, ombre en rose, papier dessous.
- **À surveiller** : Firefox (Playwright) a une image de ~270 ms au premier choix d'une carte (le voyage repart ensuite, 1,2 s) ; le défilement de la boîte refait les filtres des cartes à chaque image (médiane 16 ms, max 33 ms mesurés en Firefox). Si une tablette peine : couper le filtre des vignettes pendant le glissé.
- **Contrôles** : `node --test test/` 22/22 (6 nouveaux dans `test/cartes.test.js`). Playwright (Firefox 156, http://127.0.0.1:8804, `lite=0`) : console 0 erreur / 0 avertissement ; 5 clics réels → bulle « Oups », pouce retiré (épingle, décor, hippocampe) ; doublon refusé ; glissé (−574) puis clic sur les copains qui étaient hors champ ; molette ; `setTime(2)` + clic → « Le cerveau dort… », boîte à .45 ; matin → bulle du matin ; Entrée au clavier sur une carte focalisée (défilement automatique) ; `#journee` vide tout et remet t = 0 ; `journee` émis à chaque changement ; mouvement réduit : 0 animation ; 0 `.w[transform]`. Captures : `shots/t8-dehors.png`, `t8-dedans.png`, `t8-nuit.png`, `t8-dehors-riso.png`, `t8-dedans-riso.png`.

### Task 8, tour de correction 1

- **Le pouce est géant** : `#d-pouce` est agrandi ×1,65 dans le générateur, autour du bas du socle (toujours à y 452). L'ongle monte à y ≈ 30, plus haut que le sommet du crâne de l'enfant (≈ 44), et le pouce cache l'expo et son drapeau. Le vol vise le milieu du pouce (y 260). Retirés : deux petits plis isolés, qui faisaient un visage.
- **Places réservées** : `SLOT_PREFERE = { pouce: 1, orage: 2 }`. L'orage a rapetissé (×1,8) et se range dans le ciel à droite du pouce, au-dessus du toit (nuage centré vers (814,160)) : il ne couvre plus l'ongle. Un décor qui occupait la place réservée est déplacé. Les autres décors prennent d'abord `#slot-0`, puis `#slot-3`.
- **Une seule règle pour la nuit** : `phaseCourante` (le moment arrondi, donc t ≥ 1,5) sert à la fois à griser la boîte et à refuser les cartes. L'événement `temps` part à chaque changement de moment arrondi : la boîte n'est jamais grise quand on peut choisir, ni l'inverse.
- **Molette** : elle ne retient l'événement que si la boîte a vraiment défilé. En butée, la page défile (vérifié : `defaultPrevented` faux à 0 et à `DEFIL_MIN`, vrai au milieu). `#journee` annule l'élan d'un glissé avant de revenir au début.
- **Hippocampe** : les places s'écartent (pas d'environ 20). Chaque petite carte montre au moins la moitié de sa face.
- **Vignette du pouce** : contour brodé épais. L'ongle est clair, avec son contour et un reflet blanc, et les plis sont épais : il se lit à 40 × 40 dans les deux thèmes.
- **Ce qui vole où, Dehors** : une carte qui a un décor (`base:true`) vole dans son décor, qui sort de terre (spec §4.3 : « elle devient un élément du décor du jour »). Une carte sans décor (mots, ressentis, chanson) vole dans l'œil ou l'oreille de l'enfant (spec §4.1 : on la voit entrer dans la tête).
- **Contrôles** : 22/22, console propre. Composition contrôlée avec `glace, velo, tracteur`, puis `orage`, puis `pouce` : `tracteur@slot-0`, `pouce@slot-1`, `orage@slot-2`, `velo@slot-3`. Captures relues : `shots/t8-dehors.png`, `t8-dehors-4.png` (`pouce,glace,orage,copains`), `t8-dedans.png`.

## Task 9 : le rangement (nuit profonde)

- **Déclencheur** : écouteur de `temps`. Phase 2 : `rangerTout` (les cartes de `#g-hippo-cartes` partent vers `#g-cartes-rangees`, dans le nouveau `#g-cortex-cartes`, posé dans `#g-dedans` après les sillons, avant les zzz et la tête). Phase 0 : `sortirTout` (retour à l'hippocampe, épingles revenues). Les phases 1, 3 et 4 ne touchent à rien : les cartes restent au cortex pour le rêve et le matin. `resetDay()` vide tout. Au chargement, `?cartes=` avec phase ≥ 2 : `pickCard` appelle `ranger(…, false)`, sans animation.
- **Places** `CORTEX` : frontal (440,152), pariétal (300,116), occipital (224,150), temporal (405,262), dans l'ordre de la journée. Échelle : `CORTEX_ECHELLE` 1,9 × la vignette de l'hippocampe, × .55 si charge 0. Éviction (5e carte) : `retirerCarte` supprime aussi la copie du cortex et son fil, puis `rangerCortex` recale les autres.
- **Animations** (toutes par `animer()`, donc nulles en mouvement réduit ; placement immédiat alors) : vague en S de 1 s (`vague`, images clés calculées à la main), décalée de 250 ms par carte ; huit points de couture bruns (groupe `.points`, filtre sur le groupe : un trait droit n'a pas de boîte pour son filtre) qui apparaissent en 400 ms et restent en bord cousu ; fil `<line class="fil-amygdale cN">` qui défile 700 ms (`stroke-dashoffset`) ; l'hippocampe expire (1 → .96 → 1). Jamais de transform animée sur une `.w`.
- **Fils** : jetons `--fil-orange`, `--fil-rose-doux`, `--fil-bleu-doux` (`:root`) ; classes `c3 c2 c1 cm2`. Riso : le cortex est rose, un fil rose y disparaîtrait ; peur = bleu, colère = jaune, joie = papier, apaisant = bleu à moitié (3 encres).
- **« je grandis »** : `<text>` sur `<textPath>` le long de la bande d'os du front (l'arrière du crâne est trop étroit et couvert par les cheveux), opacité `var(--grandis)` posée par `setTime` d'après `TEMPS.grandis = [0,0,1,.3,0]`.
- Vérifié : tests 22/22 ; Playwright (console propre) : phase 2 → 4 cartes, 3 fils, hippocampe vide ; phase 4 idem ; phase 0 → retour, 0 fil ; `resetDay()` tout vidé ; mouvement réduit : immédiat, 0 animation.
- **Task 9, tour de correction 1** : le rangement se fait dès toute phase ≥ 2 (idempotent via `rangees`), animé seulement en entrant en phase 2 par le bas (`phaseAvant`) ; de 0 on saute à 3 ou 4 et les cartes sont au cortex. « je grandis » : `<textPath>` sur le bord extérieur du crâne au sommet, 10,5 px, halo crème (`paint-order:stroke`), au-dessus des cheveux. Fils d'amygdale à 3 de large. Commentaire des points corrigé (huit).

## Task 10 : le générateur de rêve et l'écran

- **`composeDream(slugs, { seed, genre })`** (bloc PURE, section J ; testé dans `test/reve.test.js`, 18 tests : les cas du brief, les 253 paires dans les deux ordres × 3 genres × 3 graines, 2 000 journées de 3-4 cartes tirées au hasard, les dessins). Rôles :
  - une carte apaisante n'est jamais greffe ; si la greffe fait peur et que la journée a une carte apaisante, la plus récente est mise de côté (`reconfort`, verdict `finitBien`) : le doudou ne devient jamais l'ogre ;
  - **ex æquo de charge : la base se choisit d'abord.** Le brief dit « greffe = charge max, ex æquo la dernière », mais exige aussi `glace, chien → base chien` (et le spec : « le chien est devenu un chien en glace ») : avec la greffe d'abord, le chien serait la greffe. Règle retenue : une seule carte la plus forte → elle est la greffe ; plusieurs → la base (la plus concrète, la plus récente) d'abord, puis la greffe parmi les autres plus fortes. Tous les cas du brief passent ;
  - concret : vu > gens > mot > ressenti ; une carte réconfort selon sa porte (le doudou, qu'on voit, comme une chose vue ; la chanson comme un mot) ;
  - sans base possible (ogre + j'ai ri, une seule carte, journée tout apaisante) : mode **« seul »** (gabarit `PHRASES.seul`) ; modificateur « tout petit / multiplié / d'une autre couleur » par la graine (spec), sauf la peur (gigantesque) et la colère (envers / n'obéit pas), pour que le dessin dise le verdict.
- **Accords** (post-traitement, gabarits de `PHRASES` inchangés) : base au défini (`un chien` → `le chien`, `un orage` → `l'orage`, `mon doudou` → `ton doudou` via `ton`) ; « est devenu » accordé à la base (devenue, sont devenus, sont devenues) ; une greffe-attribut (ressenti) donne « avait / avaient » (« le vélo avait des sourcils fâchés ») ; base plurielle → greffe au pluriel (table `PLURIEL` : « des pirates », « de grands sourires ») ; modificateur accordé à la greffe (`MODIFS.f/mp/fp`) ; « qui n'obéit pas » → imparfait du récit ; « était … l'a rejoué » accordé ; `c'est {VRAI}` → « c'est une statue » (base pouce) ou « ce n'est pas pour de vrai » ; de le → du, à le → au, le/la + voyelle → l' ; espaces ; `inflect`. Champ ajouté : `nomPhrase` des ressentis (« le moment où tu as ri ») pour {C1}/{C2}. L'affichage remplace l'espace devant ! ? : ; » et après « par une insécable (sinon « ! » seul en début de ligne).
- **Dessins** (`tools/gen-reve.py`, reproductible à l'octet, réutilise les vignettes et les aides de `gen-cartes.py`) : 15 `#g-base-<forme>` = vignettes × 3 (≈ 120 px), avec `data-tete="x y s[;…]"` (deux têtes pour les copains et les parents) et `data-corps` ; 23 `#g-greffe-<forme>` en deux parties `.a-tete` / `.a-corps`, placées par des **variables posées sur le `<use>`** (`--tete-x/-y/-s`, `--corps-…`, `--corps-vis`) — une classe d'ancêtre ne traverserait pas le clone ; 4 `#g-greffe-<forme>-dos` derrière la base (ailes du dragon, cornet, queue qui remue, mât du manège) ; `#g-reve-flou` ; `#clip-ecran` et `#clip-ecran-grand`. Tout en `.w.lite` (`#woolMini`), 0 `.w[transform]`.
- **Écran** : le nuage `#p-ecran` (UNE pièce `.w` complète, crème, centré (700,165), x 552–848 : rien sous le rail), épingle jaune en haut à droite ; le film dans `#g-reve` (clip du nuage ; le gigantesque passe au grand clip et sort par le haut du nuage, transform-origin 50 % 72 %) ; `#encore` (pilule de 156 × 44, en haut à gauche du nuage, `role=button`, Entrée/Espace, s'enfonce sous le doigt) ; `#t-phrase` (Baloo 2, 18 px, `foreignObject`) sur une étiquette de feutrine.
- **⚠ Phrase et « 3 lignes au plus »** : les phrases font 75 à **340** caractères (le gabarit `reve` seul ≈ 205) ; à 18 px, 3 lignes demanderaient ≈ 1 000 px de large. Choix : 18 px tenus, autant de lignes qu'il faut (6 pour l'histoire du pouce, 10 pour la plus longue). En vue Dedans, l'étiquette est posée sur la boîte (bas à y 462) et monte, si la phrase est longue, sur le bas du nuage ; en vue Dehors, elle est sur le mur à gauche du nuage (x 182–518, en haut), car sous le nuage il y a le lit et le doudou. Elle glisse entre les deux avec le fondu (`--vue` posée par `setCut`, `--leg-dy` par le script selon sa hauteur).
- **Verdicts** : `document.body.dataset.verdict` ; le CSS ne pose que des variables sur `body` (elles traversent les clones) : cauchemar (nuit des rêves) → `.nuit` en `--nuit-4` ; bizarre → `--p-amygdale` orange et sa lueur (`--amygdale-orange`, riso `--encre-orange`) ; beau / rigolo / finitBien → nuage en `--p-ecran-doux`. Classes sur les éléments : `#p-sourcil.fronce` (cauchemar, bizarre), `#p-amygdale.alarme` (bat à .95 s), `#p-bouche.sourit` (aussi au matin), `.ecran-tremble.tremble`. finitBien : la vignette apaisante entre dans le nuage (1,9 s) ; la transformation elle-même est pour Task 11.
- **Déclenchement** : `temps` phase 3 → rendu animé ; phase 4 → le rêve reste (rendu sans animation si on a sauté la phase 3) ; autres → tout effacé. `journee` (phases 3-4) et le genre (MutationObserver) le refont. Au chargement, phase lue directement (aucun `temps` émis). Le nuage suit la table `TEMPS.ecran` `[0,.3,1,1,1]` : il n'est pas là le jour (il couvrirait l'expo et le pouce). Les cartes du cortex qui ne servent pas au rêve pâlissent (`.oubliee`).
- **« Encore un rêve »** : `seed++`, la bobine clignote 300 ms, puis le rêve se refait avec la projection. Une graine sur deux, le film est retourné gauche-droite et le contexte change de côté : même pour l'ogre (charge 3, modificateur fixe), « Encore » change quelque chose.
- **Animations** (toutes par `animer()` ou CSS gardé par `--amb-anim`/`--amb-play`, rien en mouvement réduit, vérifié) : projection 400 ms (opacité + échelle + luminosité), croissance du géant 1,3 s avec dépassement, effacement du contexte, retournement, rétrécissement ; secousse `desobeit`, queue qui remue, taches floues qui flottent, tremblement doux de l'écran.
- **Riso** : `#g-ecran` en `normal` + sous-couche de papier (`.sous-ecran`), étiquette sans filtre (`--legende-filtre:none`), texte bleu d'encre.
- **Ce qui a raté** : (1) première mise en page, phrase sous le nuage dans un cadre fixe : 7 lignes, « ! » orphelin, et la plus longue entrait dans la boîte ; (2) « sourcils fâchés » et « grand sourire » seuls sur un vélo ou un gâteau ne se lisaient pas : yeux ajoutés aux deux greffes ; (3) `\b` ne marche pas devant « à » (non-mot en JS) : `(^|\s)`.
- **Pour Task 11** : `reveCourant`, `seed`, `renderDream(dream, {anim})`, `direPhrase(texte)`, `poserVerdict(v)`, `ancresDe(forme)` ; transformer le film = agir sur les `.reve-pose` (wrapper sans `.w`) ou y ajouter un `<use>` de greffe avec les variables d'ancre.
- **Contrôles** : `node --test test/` 40/40. Budget Dedans, cartes rangées + écran : 19 `.w:not(.lite)` visibles. Playwright (Chromium, http://127.0.0.1:8810, `lite=0`) : console 0 / 0 ; `animateTime(3)` → rêve, `verdict` cauchemar, sourcil froncé (matrice mesurée), nuit `rgb(20,21,51)`, pose `scale(2.2)`, grand clip ; clic réel sur `#encore` → `seed` 0 → 1, rêve refait (retourné) ; `animateTime(4)` → gardé, plus de froncement ni de tremblement ; `animateTime(0)` → vidé, bouton caché, nuage à 0 ; `?temps=3` sans carte → flou + phrase `flou`, sans erreur ; `pickCard` forcé la nuit → refait, `resetDay()` → flou ; mouvement réduit : 0 animation, Entrée au clavier → `seed` 1. Captures : `shots/t10-ogre.png`, `t10-dehors.png`, `t10-glace.png`, `t10-flou.png`, `t10-riso.png`, `t10-riso-dehors.png`, `t10-pirates.png`, `t10-bizarre.png`, `t10-long.png`, `t10-finitbien.png`, `t10-matin.png`.
- **Task 10, tour de correction 1** : en mode « seul », « desobeit » donnait « les sourcils fâchés étaient qui n'obéissaient pas » ; le verbe remplace maintenant « était » : « ne voulait / ne voulaient pas obéir » (« Dans le rêve, les sourcils fâchés ne voulaient pas obéir, parce que ton cerveau les a rejoués. »). `defini()` donne « les deux grands bras » au sujet (câlin seul). Tests : aucune phrase « était/étaient qui » (toutes les cartes seules et toutes les paires × graines 0–2 × genres), aucun sujet « deux … » sans article ; 43/43. **Pour Task 11** : `dream.reconfort` n'est non nul que les jours de cauchemar (charge 3, spec §4.5-4) ; `applyRemote` ajoute lui-même la carte réconfort d'après `prefs` et ne doit pas compter sur `dream.reconfort`.

## Task 11 : la télécommande — changer de chaîne

- **Dessins** (dans `tools/gen-reve.py`, toujours reproductible à l'octet ; deux relances successives ne changent rien) :
  - `#g-greffe-lapin` : deux grandes oreilles roses (l'une retombe), nez rose, moustaches, carotte. Posée sur les ancres de tête de la base.
  - `#g-greffe-chiens-pirates` : deux chiens debout, bras levés, chapeau de pirate, l'un avec un bandeau. Posée sans ancre, au centre du film, à ±88.
  - Groupes animés (`.oreille-lapin`, `.nez-lapin`, `.carotte`, `.danse-chien`) : un nouveau tuple `('G', classes, éléments, dx, échelle)` dans `greffe_partie`.
  - La télécommande : bloc `TELECOMMANDE-BEGIN/END`, que le générateur écrit dans `#g-ui`.
    - Feutre gris `--p-telecommande` (UNE pièce `.w` complète), 66 × 128 en x 788–854, y 330–458, inclinée de −5° par un `<g>` de placement.
    - Quatre boutons-pressions de couleur (laine + anneau brodé + nœud), une lampe rouge, une télé brodée, trois ondes.
    - L'étiquette de feutre épinglée au-dessus (x 779–859, y 272–322).
    - Une cible transparente (x 758–862, ≥ 44 px même sur téléphone).
  - Dans le bloc écran : `#t-cle` (dans le `foreignObject` de la légende, hauteur 250 → 330) et `#g-reconfort`.
- **Légende en vue Dedans (écart nécessaire)** : à x 524–860, elle passait exactement sous la télécommande. Elle est maintenant à x 504–772 (`translate` 342 → 322, largeur `324 − 68·min(1, --vue)`).
  - `ajusterLegende` lit la largeur du texte et la hauteur de la phrase + la phrase-clé.
  - Le `ResizeObserver` suit les deux, donc le fond se recale pendant le fondu.
  - Le menton (x ≈ 492) reste dégagé.
- **Phrase-clé** : `direPhrase(texte, cle)`. Avec une clé, la phrase passe à 16 px, puis vient une ligne de points et `PHRASES.cle` en Baloo 2 700 (ajouté au lien des polices), 19 px, au fil indigo (riso : bleu). C'est le « sous-titre » de l'écran.
  - Après un appui : le texte de la transformation (`TRANSFOS`) + la clé.
  - En finitBien automatique : « Ton doudou était dans ta tête, alors le film a changé tout seul. » (la queue de la phrase du rêve, sans « … mais ») + la clé. Ajouter la clé à la phrase complète aurait couvert l'enfant Dehors et le nuage Dedans.
- **Machine à états** (`tc`, section 10) :
  - `compteur` : il ne revient jamais à zéro, `remoteStep(compteur++)`.
  - `utilise` : il coupe la pulsation.
  - `transfo`, `texte`, `cle` : `journee + seed`.
  - `enCours` : les éclairs.
  - Deux minuteries : l'automatique et les 4 s de la chanson.
  - Événement **`reve`** (`{anim}`), émis par `renderDream` et `effacerReve`. Le même rêve redessiné sans animation (l'avatar change) garde sa chaîne ; tout autre rendu remet à zéro (Encore, journée, nouvelle nuit des rêves). Au chargement, `surReve(false)` lit l'état.
  - `temps` → `majTelecommande` : `tc-on` aux phases 3–4, libellé, `tabindex`, `aria-hidden`. Hors 3–4, la chanson est fermée sèchement.
- **L'appui** : la pièce s'enfonce, les boutons descendent de 2 px, retour à ressort ; les ondes partent.
  1. La carte réconfort de `prefs` file de la télécommande vers le bas du nuage, du côté opposé au contexte, et l'épingle se plante. Pas de carte si le film montre déjà la même (finitBien).
  2. La chanson s'ouvre dans le geste même, pour que l'autoplay soit permis.
  3. Deux éclairs doux du film (380 ms).
  4. `transformer(id)` puis la phrase.
- **`transformer`** :
  - Il annule les animations de projection encore en cours, retire `m-<modif>`, et joue la descente en WAAPI depuis la transform du modificateur. L'origine 50 % 72 % du géant est gardée. Pendant ce temps, `transition:none` en ligne, sinon la transition CSS l'emporte sur l'animation.
  - bronze : dégonflage à rebonds de 1,1 s, trois « pfff » de fil, greffes `.efface`, et `.bronze-teinte` (sépia) si la base n'est pas le pouce. Le contexte revient.
  - lapin : un `<use>` par tête.
  - danse : `.danse` sur les poses, contexte `.cache`, les chiens arrivent à ressort.
  - Le grand cadre du géant est rendu au nuage après 1,15 s.
  - Ensuite `poserVerdict('finitBien')` : nuit `--nuit-3`, plus d'alarme ni de froncement, sourire.
- **Chanson** : `dialog#chanson.feuille.chanson`, en bas à gauche, fond voilé à 10 %. Échap, ✕ ou un appui sur le fond la ferment ; `close` vide la fenêtre, ce qui arrête la musique.
  - `prefs.chanson` est validée (`ytid` `[\w-]{6,20}`).
  - L'iframe est créée seulement dans `openSong` : `loading=lazy`, `referrerPolicy` `strict-origin-when-cross-origin` (YouTube refuse un lecteur sans référent).
  - `allow` est posé seulement si `document.featurePolicy` connaît la fonction. Firefox signalait « Skipping unsupported feature name » dans la console.
  - Hors ligne, sur `error`, ou sans `load` en 4 s : « 🎵 Chante ta chanson ! » + le titre.
  - Le gestionnaire de clavier global se tait quand un `dialog` est ouvert.
- **finitBien automatique** : à 3,2 s, après l'entrée de la carte apaisante de Task 10 (immédiat sans animation, et aussi au matin si on y saute), on joue la transformation et la phrase, sans chanson ni carte en plus.
- **Riso** : `#g-ui` en `normal` + sous-couches de papier ; l'étiquette est en papier.
- **Mouvement réduit** : tout est posé d'un coup (0 animation mesurée). Le halo jaune d'appel reste, immobile.
- **Contrôles** :
  - `node --test test/` : 49/49 (6 nouveaux dans `test/telecommande.test.js`, qui charge le bloc PURE lui-même : `_load.js` n'est pas touché).
  - Playwright (Firefox, http://127.0.0.1:8812, `lite=0`) :
    - au chargement, aucune requête YouTube ;
    - 1er appui : bronze, `youtube-nocookie.com/embed/jqGPppvVmBc?autoplay=1` demandé à ce moment-là, et la vidéo joue ;
    - Échap : fermé, la lecture s'arrête (`state=paused final=1`) ;
    - hors ligne, 2e appui : lapin, « Chante ta chanson ! », aucune requête ;
    - 3e appui : danse ;
    - Tab (29) puis Entrée : déclenche ;
    - `animateTime(4)` : « Tu veux lui changer sa tête ? » ;
    - `animateTime(0)` avec la chanson ouverte : fermée, télécommande cachée, carte et clé retirées ;
    - retour à 3 : pulse de nouveau. Encore : remis à zéro. Avatar : la chaîne reste ;
    - finitBien (`pouce,ogre,doudou`) : transformation seule à 3,2 s, pas de dialog, aucune requête ;
    - mouvement réduit + riso : immédiat, 0 animation ;
    - 0 `.w[transform]` ; téléphone 420 : `scrollWidth` 420 ;
    - console : 0 erreur, 0 avertissement de la page (les avertissements restants viennent du lecteur YouTube lui-même, `google.com/js/th`).
  - Captures : `shots/t11-avant.png`, `t11-avant-pw.png`, `t11-apres-bronze.png`, `t11-apres-lapin.png`, `t11-apres-danse.png`, `t11-finitbien-dehors.png`, `t11-riso-bronze.png`, `t11-riso-lapin.png`, `t11-lapin-zoom.png`, `t11-danse-zoom.png`, `t11-chien-danse-dehors.png`, `t11-tel.png`.
- **À surveiller** :
  - Ouvert en `file://`, YouTube n'a pas de référent et peut refuser la lecture (erreur 153). L'iframe se charge quand même, donc pas de repli « Chante ta chanson ». GitHub Pages et http ne sont pas touchés.
  - En danse, l'ogre garde ses crocs et ses sourcils : il danse, il ne change pas de tête.
  - Chrome n'a pas été piloté (Playwright = Firefox). `allow` y est posé par détection.

### Task 11, tour de correction 1
- **La chanson ne reste jamais muette.**
  - Sous la fenêtre 16:9, toujours : « 🎵 Chante avec elle ! » + le titre.
  - Au même appui, une sonde `fetch(youtube-nocookie.com/favicon.ico, no-cors, no-store, sans cookie)`. Si elle échoue, le lecteur est retiré et la fenêtre dit « Chante ta chanson ! ». Il le fallait : Chrome envoie `load` pour sa page d'erreur.
  - Prédicat pur `videoPossible(enLigne, protocole)` : hors ligne ou en `file://`, pas d'iframe ni de requête. Testé en node, puisque Playwright n'ouvre pas `file:`.
- **Greffes adoucies** (lapin, danse) :
  - dans `gen-reve.py`, les pièces qui font peur sont groupées en `.mechant` : crocs et sourcils de l'ogre ; sourcils, bouche et fumée de « fâché » ; sourcils, bouche et goutte de « peur » ; flamme du dragon ; éclairs de l'orage ; sabre du pirate ;
  - un visage `.gentil` est ajouté : sourire, joues et sourcils levés pour l'ogre ; sourire et sourcils pour « fâché » ; sourire pour « peur » ;
  - `transformer` pose `.doux` sur les `<use>` de greffe (sauf bronze, qui les efface). Les variables `--doux-mechant` / `--doux-gentil` traversent le clone.
- **finitBien automatique** : la forme courte `dream.courte`, nouvelle (`COURTES` + `phraseCourte` dans le bloc PURE, mêmes accords que la phrase du rêve par `finir()`). Exemple : « Ton cerveau a mélangé le pouce géant avec le mot « ogre »… mais ta chanson était dans ta tête, alors le film a changé tout seul. » Le réconfort est au défini (« le câlin »).
  - `COURTES` est à part de `PHRASES`, dont les gabarits sont figés par `data.test.js`.
- **Petites corrections** :
  - phrase-clé à 21 px ;
  - journée vide + appui : seulement `PHRASES.flou`, sans phrase-clé ;
  - la cible s'arrête à x 860 ;
  - `fermerSurFond(dialog, fermer)` sert aux deux dialogs.
- **Contrôles** :
  - 52/52 ;
  - Playwright (Firefox) : chargement sans YouTube ; appui → sonde + iframe + « Chante avec elle » ; `page.route` en `internetdisconnected` → lecteur retiré, chant ; hors ligne → chant, 0 requête ;
  - lapin et danse : l'ogre sourit, sans crocs ;
  - console de la page propre ; le fond referme la feuille de réglages.
  - Captures : `shots/t11f-*.png`.

## Task 12 : zones cliquables, volet d'info, « Montrer les zones »
- `ZONES` (bloc PURE, donnée pure) : id de INFO → `{cible:'#id'|[ids], forme, marge 6-10, enfants?, bande?}`. 33 entrées (INFO a 46 zones : 13 `decor-*` naissent avec les cartes, `ZONE_DECOR`). `test/zones.test.js` teste la table (couverture de INFO, cibles présentes dans index.html, marges, code d'accessibilité) ; `_load.js` expose `ZONES`.
- Génération (section 11 du script, après `document.fonts.ready` + rAF) : `getBBox` + `getScreenCTM` → repère de `#g-hs`, borné à la scène et au rail (x ≤ 866), élargi de la marge ; ellipse = boîte × 1,1 + marge. Triées par aire (les petites dessus). `enfants` : une forme par enfant (neurones, étincelles, bandes de vagues, fuseaux). `#hs-0/1/2` en HTML ; écran et boîte ont une forme dans 0 et 1.
- `boite` : `bande:6`, seul le rebord (sinon la zone couvrirait les cartes). `ecran` : `#scene[data-encore]` (MutationObserver sur `#encore`) rend la zone inerte tant que la pilule « Encore un rêve » est visible.
- Vue active : `majZones()` appelée par `setCut` ; groupes inactifs `display:none` (ni clic, ni focus, ni lecteur d'écran), tabindex 0/-1.
- `showInfo(id, evt)` → `openInfo`; `.sel` posé par `marquerZone` (appelée par openInfo/closeInfo, aucun code de volet dupliqué) ; étiquette `#label` seulement souris/stylet. Entrée/Espace au clavier.
- Zones `decor-*` : événement `journee` → rAF puis +900 ms (le décor s'installe).
- « Montrer les zones » : `#scene.hint` 6 s, `aria-pressed`, battement `--amb-anim` ; mouvement réduit : liserés fixes.
- Limites connues : zones de vagues/fuseaux mesurées au chargement (elles glissent) ; zones de décor présentes même quand le décor est éteint la nuit ; les formes ne suivent pas le « respire » (×1,01) de Dedans.
- `window.__zonesManquantes()` → `[]`.
- Fix round 1 (Task 12) : « Montrer les zones » = une pastille de feutre + emoji par zone active (`#g-hint`, 6 s, se repoussent à 32 px) au lieu de liserés ; `.sel` posé sur la pièce visée quand `cible` est un seul élément (liseré indigo par 4 `drop-shadow`, après le filtre laine ; le cercle `.hs` ne reste que pour les zones multi/`<use>`) ; `evaluerZones()` (vue, `temps`, journée) rend « off » (pointer-events none, tabindex -1, aria-hidden) toute zone dont la pièce a une opacité cumulée < .3 ou visibility:hidden ; bande de la boîte à 10 px. La télécommande n'est pas une zone de INFO (elle a son propre `tc-on`).

## Task 14 : la loupe
- **Mécanisme.** `#lens` (div rond de 160 px dans `.cadre`, rogné par lui) contient `<svg viewBox><use href="#scene-inner"/></svg>`. `#loupeBtn` bascule `html.loupe-active` (les animations d'ambiance se figent par `--pres-play` / `--amb-play`, lues par `animation-play-state`, clone compris), `aria-pressed`, `.lens-on` sur `.cadre` (`touch-action:none`). Pointeurs sur `.cadre`, un calcul par image (rAF, dernier événement gagnant). Elle apparaît au milieu de la scène à l'allumage (ressort `scale .6 → 1`, reflet du rebord une fois), se cache quand la souris quitte le cadre (sauf si elle a le focus clavier), se montre au doigt 96 px au-dessus du point visé. `pointer-events:none` : un clic sur l'amygdale avec la loupe allumée ouvre bien le volet (pas besoin du relais de clic du volcan : ici le `<use>` est dans le même `<svg>` racine… à vérifier si `#scene-inner` change de racine).
- **Grossissement ×2,4 relatif à la scène affichée** : échelle = largeur de `#scene` / 900 ; côté de la fenêtre = 160 / (échelle × 2,4) unités (53,8 à 1115 px de large, 154,6 à 388 px) ; mesuré 2,400 aux deux largeurs. La fenêtre est bornée au viewBox (rien au-delà du cadre).
- **Clavier** : `#lens` a `tabindex=0` quand elle est allumée (`role=img`, `aria-label`) ; seule, elle prend les flèches (20 px ; elles ne volent pas ←→↑↓ de la page). Allumée au clavier, elle prend le focus ; Échap l'éteint et rend le focus au bouton. Échap ferme d'abord le volet d'info s'il est ouvert (écouteur en capture), puis la loupe.
- **Règles riso converties en variables** (le sélecteur d'ancêtre `[data-theme=riso] …` ne traverse pas le clone) : `#scene-inner>g` (`--grp-blend`), `#g-pres/#g-boite/#g-ecran/#g-ui` (normal sans condition : identique en feutrine), `.oeil-hippo` (`--oeil-hippo`), `.oeil-lune/.nez-doudou` (`--oeil-lune`), `#p-liquide` (`--liquide-op`), `#p-cortex` (`--cortex-fill`), lobes + `.profond` (normal sans condition, `--profond-op`), `.w.pale/.teinte` (`--pale-mix`, `--teinte-mix`, seulement avec `data-ink`), `#g-enfant-dehors` (`--enfant-iso`), `.toile-lin/.toile-grain` (`--toile-lin`, `--toile-grain`), `.fil-amygdale` (`--amy-c1/c2/c3/cm2`, `--amy-cm2-op`). Plus aucune règle riso à sélecteur d'ancêtre ne vise un descendant de `#scene-inner` (restent celles qui visent un groupe direct sous `#scene-inner`, que le clone retrouve par l'id).
- **Mesures (Chromium headless, logiciel)** : image à ~19 ms sans loupe ; avec loupe immobile 16 ms ; **loupe en mouvement en feutrine complète Dedans : ~148 ms/image (p90 166)**, Dehors ~80 ms, riso ~145 ms, **allégé 17 ms**. Le clone refait le rendu des filtres de laine à chaque déplacement. Non basculé en allégé automatiquement (décision du contrôleur).
- Vérifié : console propre (feutrine, riso, allégé, 420 px), `getAnimations()` en cours : 0 pendant la loupe, 16 après ; Échap ; clic à travers ; mouvement réduit (lentille visible, sans animation). Captures `shots/t14-*.png`.

## Task 15 : le mode guidé « L'histoire du pouce »
- **La fiche est le volet** (`#info`, classe `histoire`) : emoji 📖, titre « L'histoire du pouce » + compteur « n / 11 » (span ajouté par `majPuces`), le texte (`#infoText`), onze pastilles de feutre (`#recitPuces`, l'étape en indigo, ressort), puis `#suite` « Et après ? » (indigo, 56 px) et `#stop` ✖ (rond 56 px). Rien de tout cela n'est visible sans la classe. Mobile : l'emoji disparaît pendant l'histoire et le texte se resserre, pour que titre et boutons tiennent dans la scène.
- **Flux** : `startStory()` → annule les glissés, `resetDay()`, `setTime(0)`, `setCut(0)`, `seed = 0`, `pickCard` × pouce/ogre/copains/ri (`anim:false, forcer:true`), étape 0, focus sur `#suite`. `#suite` → `allerEtape(i+1)` : pastilles et événement tout de suite, `animateCut`/`animateTime` (600 ms, en parallèle), puis (≈640 ms, ou tout de suite sans mouvement/changement) le texte, « tourné » (200 ms, ressort ; rien en mouvement réduit). Un appui pendant le glissé montre d'abord le texte en attente. `reve` : graine 0, le rêve se dessine à la phase 3 par l'événement `temps` ; refait une fois si la phase n'a pas changé. `telecommande` : `applyRemote()` ; à la fermeture de la chanson le focus va sur `#suite` (le `close` du dialog y pense avant la télécommande). Pas d'avance automatique.
- **Fin** (écart assumé avec la lettre du ruling) : l'étape 11 « À toi de faire ta journée ! » s'affiche (journée remise à zéro, `setTime(0)`), `#suite` devient « C'est parti ! » et `#stop` disparaît ; l'appui suivant ferme la fiche. Sinon l'enfant ne lirait jamais la dernière phrase. Pour fermer d'emblée : appeler `stopStory()` à la place du texte dans `montrer` (action `fin`).
- **Arrêt** : `#stop`, ✕ du volet, second appui sur `#histoire`, ou une zone qui reprend le volet → `finirRecit()` (hooks `recitActif` dans `openInfo`/`closeInfo`, `var` car `openInfo` peut tourner avant la section) ; la scène reste comme elle est. `#histoire` devient « ✖ Arrêter l'histoire » (`aria-pressed`).
- **Texte** : `texteEtape(i)` = `{PRENOM}` → prénom (sans `{}|`) sinon `{il|elle}` (`{Il|Elle}` en début de phrase), puis `inflect`. HISTOIRE[7] commence par « Mais on a une télécommande ! ».
- **Événement** `histoire` (`detail:{etape, fin}`) à l'étape 0 et à chaque étape ; `fin:true` à la dernière (pour Task 16).
- Limite : en Chromium logiciel (feutrine complète) certains changements de moment prennent > 1 s ; le texte arrive alors avant la fin du glissé.

## Task 16 : les deux mini-jeux, les récompenses et le badge
- **La fiche est le volet** (`#info`, classes `jeu` et `jeu2`, comme `histoire` pour Task 15) : titre du jeu + compteur « Question n / 3 » (span `.recit-num`), le texte (`#infoText`, live), le score `#jeuScore` (région live à part : « ⭐ n / 3 » visible, « n sur 3 » lu), puis `.jeu-bt` : `#vrai` 👀 Pour de vrai (corail) / `#reve` 💭 C'est un rêve (indigo), `#jeuSuite`, `#rejouer` « Encore ! », `#fini` « Fini » (56 px, `hidden` selon l'étape). `jeu2` agrandit l'émoji (76 px) : c'est l'« image » de l'énoncé. Téléphone : fiche resserrée comme l'histoire, émoji du jeu 2 flottant à gauche, réponses côte à côte ; aucun défilement dans la fiche (mesuré à 420 px).
- **Tirage** : `tirer3(seed, n = 8)` dans le bloc PURE (mulberry32, sans remise), appelé avec `Date.now()`. `test/jeux.test.js` (7 tests, son propre chargeur vm pour `tirer3`, `_load.js` intact) : cibles ∈ `ZONES` et `INFO`, huit cibles distinctes ; `JEU_REVE` : réponse `vrai|reve` et **`explication`** (champ ajouté : il n'existait pas ; une ligne ≤ 90 caractères, « Pour de vrai : … » / « C'est un rêve : … ») ; mots interdits (plus « faux », « nul », « raté », « perdu ») ; `tirer3` : 3 indices distincts, déterministe, toutes les questions sortent.
- **Jeu 1 « Trouve la partie ! »** : la vue glisse vers celle de la cible (toutes en vue 1, visibles à tous les moments — vérifié). Tant que `jeuActif === 1`, les clics / Entrée sur les `.hs` passent par `jeuToucheZone(z)` (section 11 : `if(!jeuToucheZone(z)) showInfo(…)`) ; relâché dès la fin du jeu (vérifié : un clic sur l'amygdale rouvre son volet). Bonne zone → pièce cousue d'indigo (`marquerZone`), « Bravo ! 🤸 Le cervelet. », une étoile + confettis + « Bravo ! », question suivante après 1,8 s (les touches pendant la fête sont avalées). Mauvaise → liseré corail qui se dandine (`.hs.non`, `animer`), « Presque ! Cherche encore… » + la question, et la pastille de la bonne zone (le dessin des pastilles de Task 12, extrait en `poserPastille`) bat 2 s ; si la vue n'est pas la bonne, elle glisse d'abord. On cherche jusqu'à trouver ; seul le premier essai compte au score.
- **Jeu 2** : réponse → « Bravo ! » ou « Presque ! » + l'explication, étoile et confettis si juste, focus sur « Suite » (« Fin du jeu » à la 3e). Clavier : Tab / Entrée sur `#vrai` / `#reve` (le focus va sur `#vrai` à chaque question).
- **Fin** : 🏆, « Bravo, tu connais ton cerveau ! », max(1, score) étoiles (on ne gronde jamais : 0 sur 3 donne une étoile et « Tu as bien cherché ! On rejoue ? »), confettis, « Encore ! » (nouveau tirage) / « Fini ».
- **Arrêt / histoire** : `var jeuActif, jeuOuvre, finirJeu` à côté de `recitActif` ; `openInfo` (sauf ouverture par le jeu) et `closeInfo` appellent `finirJeu` : ✕, Échap, une zone pendant le jeu 2, l'histoire qui prend le volet arrêtent le jeu. Lancer un jeu appelle `stopStory()`. Second appui sur `#jeu1`/`#jeu2` : le jeu s'arrête (`aria-pressed`, donc indigo pendant le jeu, comme `#histoire`).
- **Récompenses** (`#g-fete`, dans `#g-ui`) : étoiles de feutre (`.w.lite` jaune + couture brune + nœud, ressort décalé de 170 ms), « Bravo ! » brodé sur une étiquette de feutre épinglée (glisse d'en haut), 24 confettis de laine (ellipses `.w.lite.mini`, quatre laines : soleil, drapeau, couverture, pyjama ; chute 1,5 s, rotation de 25 à 70°, retirés à 1,9 s). Tout par `animer()` sur des `<g>` enveloppes, jamais de `transform` sur une `.w` (vérifié) ; aucune `.w` non allégée ajoutée. Mouvement réduit : étoiles et étiquette posées, aucun confetti, 0 animation (mesuré). Version allégée : pas de confettis non plus (fix round 1).
- **Badge** (`#badge`, `role=img`) : rond de feutre jaune cousu, 🧠, ruban rose « Je connais / mon cerveau », épingle bleue ; arrivée à ressort (700 ms après les étoiles), frétille s'il était déjà là. **Placé en haut à droite (x ≈ 744–840, y ≈ 20–92), pas à gauche** : le soleil et la lune occupent le haut à gauche de la vue Dehors ; à droite, le ciel est vide dans les trois vues (le rail commence à x 866). `pointer-events:none`. `setBadge(on)` (global, pour la feuille de réglages de Task 17) écrit `reves.badge` ; montré au chargement si `true` ; `resetDay()` n'y touche pas. Gagné par l'événement `histoire` `fin:true` et par un 3 sur 3.
- **Vérifié** (Playwright, `?lite=0&vue=1`, 1280 et 420 px, feutrine et riso, mouvement réduit) : console propre (seuls avertissements : l'iframe YouTube de l'histoire, tiers) ; jeu 1 de bout en bout depuis la vue Dehors (3 sur 3 → badge, `prefs.get('badge')` true, toujours là après rechargement et « Nouvelle journée ») ; jeu 2 au clavier (2 sur 3, deux étoiles) ; histoire pendant un jeu et jeu pendant l'histoire ; fin de l'histoire → badge ; `__zonesManquantes()` → `[]`. Captures `shots/t16-*.png`.
- Limite : sur téléphone, la fiche du jeu 1 couvre la moitié basse de la scène ; le cerveau reste visible au-dessus, mais le bas du tronc cérébral est sous la fiche (non mesuré zone par zone).
- **Fix round 1** : confettis coupés aussi en version allégée (`root.dataset.lite === '1'`) ; `#jeuScore` n'est réécrit (annoncé) qu'au début, quand le score change et à la fin ; `#jeu1`/`#jeu2` gardent leur couleur pendant le jeu, un anneau indigo (fond + 3 px) montre l'état ; badge : texte 13,5 unités sur deux lignes avec halo `paint-order:stroke`, ruban `.reserve` (rouge en feutrine, papier en riso, texte à l'encre bleue), et sur téléphone (< 900 px) le badge grossit ×1,45 ancré en haut à droite (`.badge-zoom`) : texte ≈ 8,4 px au lieu de ≈ 4,5 ; au chargement `reves.badge` est lu, plus réécrit (`afficherBadge`) ; condition redondante de la vue retirée.

## Task 17 : « Pour ton enfant », « Pour les parents » et réglages
- **Tout dans `dialog#feuille`**, sous le dessin / la version allégée (pas de doublon, pas de case son) : section « Pour ton enfant » (`#prenom` maxlength 24 ; `select#reconfort` 🎵 / 🧸 / 🤗 ; `#chansonTitreIn` (et non `#chansonTitre`, déjà le `h2` du dialogue de la chanson) ; `#chansonId` + `#chansonEtat` `aria-live=polite` ; boutons « Remettre la chanson des chiens pirates » et « Enlever le badge », ce dernier `hidden` tant que `reves.badge` n'est pas `true`), puis `<details id="parents">`. Chaque champ a son `<label>` ; contrôles ≥ 56 px.
- **Écritures** : texte débouncé à 300 ms (et tout de suite au `change`), `prefs.set('prenom' | 'chanson' | 'reconfort')`. Rien à recharger : `startStory` lit `prenom`, `openSong` lit `chanson`, `applyRemote` lit `reconfort` à l'appui (vérifié). Titre vide → titre par défaut ; lien non reconnu → rien n'est écrit, « Je ne reconnais pas ce lien » ; « Remettre » réécrit les valeurs par défaut et remplit les champs. Le JS des réglages est placé après `afficherBadge` (il a besoin de `CHANSON`, `chansonPrefs`) ; `afficherBadge` règle aussi `#badgeOff.hidden`.
- **`parseYt(str)`** dans le bloc PURE : `watch?v=`, `youtu.be/`, `shorts/`, `embed/` (youtube.com, youtube-nocookie.com), ou un id `[\w-]{6,20}` ; sinon `null`. Par expression régulière, **sans objet `URL`** : le bloc PURE tourne dans un contexte vm sans DOM (un premier essai avec `new URL` y échouait). `_load.js` n'exporte pas `parseYt` (hors périmètre de ce commit) : `test/data.test.js` charge le bloc lui-même. 1 test, 12 assertions ; 67 tests.
- **Texte pour les parents** : 11 lignes d'une phrase, vouvoiement (de jour ; la nuit ; le lendemain « changer le film » ; cauchemar vs terreur nocturne ; ne pas réveiller ; en parler seulement si l'enfant s'en souvient ; « beaucoup de chercheurs pensent que » ; quand consulter), puis le lien « Lire la synthèse des sources » (GitHub, `target=_blank rel=noopener`).
- **✓ qui pousse** : `.ok` (prénom, réconfort, titre), ressort 0,5 s ; en mouvement réduit la règle globale coupe l'animation, la classe `.vu` garde le ✓ posé 1,4 s.
- **Vérifié** (Playwright, `?lite=0`, 1280 et 420 px) : console sans erreur ; prénom écrit à 300 ms (pas à 150) ; lien `youtu.be/…?t=3` → id et « ✓ Lien reconnu » ; « bla bla » → message, préférence inchangée ; réconfort écrit ; l'histoire cite « Léa » sans recharger ; la télécommande ouvre la chanson : iframe avec le nouvel id et `h2#chansonTitre` « 🎵 Ma chanson » (revérifié après le fix d'un id en double) ; « Enlever le badge » caché, visible après `setBadge(true)`, puis `reves.badge` = false et le focus passe à ✕ ; Échap ferme ; aucun débordement horizontal (feuille et page) ; aucun contrôle < 43 px.
- **Fix round 1** : l'`input` des réglages avait le même id que le `h2` du dialogue de la chanson (`openSong` écrivait le titre dans l'input) ; renommé `#chansonTitreIn`. Test « aucun id en double » dans `data.test.js` ; tests `parseYt` pour `m.youtube.com` et `?list=x&v=`.

## Task 18 : ambiance, accessibilité, polish, 15 combinaisons (30/10)

**Ce qui a changé, par thème** (quatre commits « Polish : … »).
- *Refactors.* `glisser({ max, lire, poser, annuler })` : un seul mécanisme de glissé pour la vue et le temps ; `animateCut`, `animateTime`, `pasCut`, `pasTemps` en sont des enveloppes (mêmes signatures, mêmes durées, même « cran voisin dans le sens de la touche »). `anime`/`pas` annulent aussi `annuler` (l'aimant du rail) ; `stop` non, car l'aimant passe par l'événement `input` du rail, qui appelle `stop`. Vérifié sur les deux axes (Playwright) : segment, ↑/↓ puis aimantation, ↓ puis clic de segment (rien en attente), →→← puis cran 1, `animateTime`, glissé du rail 2,23 → 2 au lâcher, `pointerdown` qui fige un glissé en cours.
  - **Propriétaire du volet** : `openInfo(opener, contenu, fin)`. Une activité qui fait du volet sa fiche (le récit, un jeu) passe sa fin ; toute autre ouverture (une zone, l'autre activité) et toute fermeture (✕, Échap, `closeInfo`) appellent cette fin une fois ; la même activité qui rouvre sa fiche (« Encore ! », l'autre jeu) la garde. Remplace `recitOuvre`/`jeuOuvre` et les `var finirRecit/finirJeu` : `finirRecit` et `finirJeu` sont des fonctions ordinaires, `stopStory`/`stopJeu` = `closeInfo()`. Restent en `var`, en section 7, les deux drapeaux lus par d'autres sections (`recitActif`, `jeuActif`). Vérifié : histoire → jeu 2 → histoire → jeu 1 → jeu 2 → second appui, Échap, ✕, zone par-dessus l'histoire, #stop, « Encore ! ».
  - CSS téléphone de `.volet.histoire` / `.volet.jeu` fusionné par `:is()` (l'image du jeu 2 reste après la règle qui cache l'émoji, même poids).
  - `test/shot.sh` trouve la page à côté de lui (plus de `$PWD`) et passe les options Chrome en plus (`--virtual-time-budget=4000 --force-prefers-reduced-motion`).
- *Accessibilité.* Boutons blancs sur corail / vert en graisse 700 et à 1.17rem (18,7 px) partout, téléphone compris : seuil « grand texte » (18,66 px gras) atteint sans ambiguïté, le 3:1 s'applique. Compteur du titre du volet précédé d'une espace (« L'histoire du pouce 1 / 11 »). Titres des jeux en insécables. Anneau indigo sur les liens. La nuit, les 23 cartes refusées sortent du parcours Tab (`tabindex=-1` avec `aria-disabled`). Mouvement réduit demandé pendant la visite : allégé (sauf choix explicite). `?theme=` n'écrase plus la préférence.
- *Contrastes et combinaisons.* Voir plus bas. Plus : rêve d'un ressenti seul (câlin : les deux bras autour de la vignette), texte « statue de bronze » quand la base n'est pas le pouce (`TRANSFOS[0].statue`), textes de Task 2.
- *Ambiance.* Deux surprises : l'épingle d'une carte choisie brille au survol ; une bouloche de pyjama se décroche du col, une fois par visite, à la deuxième carte posée par l'enfant (pas par l'URL ni l'histoire). Rien en mouvement réduit.

**Riso de nuit (décision).** Les groupes de la scène se multipliaient avec la toile : la nuit assombrissait aussi les pièces, d'où le plafond .4 et une nuit gris-mauve terne, et l'alarme de l'amygdale à peine visible. Maintenant, en riso, chaque groupe de `#scene-inner` est **isolé** (`--grp-iso:isolate`) et **posé en normal** (`--grp-blend:normal`) : ses pièces se multiplient entre elles (le mélange d'encres reste), puis le groupe se pose sur la toile. La nuit est une encre bleue (`color-mix(--ink-bleu 45 %, --nuit-3)`) à .65 ; cauchemar : `color-mix(--ink-bleu 30 %, --nuit-4)` par `--nuit-cauchemar`. Les pièces restent « en réserve » par-dessus, franches. De jour, sur le papier presque blanc, la différence ne se voit pas (captures comparées). Le fondu à `vue=0.5` se fait en transparence (comme en feutrine) au lieu d'une multiplication : lisible. Variables : le clone `<use>` de la loupe suit. Essais (captures `scratchpad`) : normal sans isolation → la peau se multipliait avec la nuit (visage olive) ; nuit grise à .7 → pièces vives mais fond terne ; bleu d'encre retenu.

**Budget** (`.w:not(.lite)` des vues visibles, feutrine `lite=0`, `cartes=pouce,ogre,copains,ri`, Playwright 1400 × 1000 ; plafond 40) :

| vue \ temps | 0 jour | 1 soir | 2 nuit profonde | 3 rêves | 4 matin |
|---|---|---|---|---|---|
| 0 Dehors | 4 | 14 | 13 | 14 | 16 |
| 1 Dedans | 19 | 20 | 20 | 21 | 21 |
| 2 Tout près | 7 | 7 | 8 | 8 | 7 |

Dehors, le `<use>` de la tête ajoute 4 pièces filtrées (5 pour la fille : cheveux longs) qu'un `querySelectorAll` ne voit pas : 20 au plus. 43 pièces `.w:not(.lite)` dans tout le document. La loupe allumée ajoute un clone complet (Task 14).

**Contrastes de nuit (15 combinaisons, deux thèmes et allégé).** 45 captures `shots/t18-{feutrine,riso,lite}-v{0..2}-t{0..4}.png` (`lite=0`, mouvement réduit, budget virtuel 4 s), comparées aux 45 d'avant (`shots/t18base-*`). Feutrine et allégé : scène identique au pixel (seul le texte du dock change, 0,42 % des pixels). Trouvé et corrigé : riso, nuit grise et pièces salies ; riso, alarme de l'amygdale modeste ; riso, « je grandis » mangé par le grain sur les cheveux bleus (imprimé net, gras, halo 3,4). Vérifié lisible : phrase du rêve (brun sur crème ; riso bleu `#0f6fb8` sur papier, 4,7:1), phrase-clé, « Encore un rêve », étiquette de la télécommande, étiquettes du rail (« jour » à l'encre, « nuit » en blanc), étoiles dans le carreau (Task 4 les y a ramenées ; riso : points de papier sur le bleu), badge. Laissé tel quel, voulu : la boîte grisée la nuit (elle dort, `.45`), Tout près rose la nuit (vue opaque, la nuit s'y lit par les vagues et les fuseaux), la cellule à 20 % en nuit des rêves (table `phaseNuit` [0,0,1,.2,0] du brief de Task 7), le pouce et le nuage en demi-teinte au soir (fondu du décor).

**Autres vérifications.**
- Mouvement réduit émulé (Playwright, sans `reves.lite`) : `data-lite="1"`, `document.getAnimations()` = 0 à `vue=1&temps=3`, et encore 0 après « Encore un rêve ». Passage à `reduce` en cours de visite : allégé, 0 animation, rien d'écrit dans le stockage.
- Ordre de Tab : segments → ⋯ → « Encore un rêve » → cartes (de jour seulement) → zones de la vue (des plus grandes aux plus petites : l'ordre du DOM est celui de l'empilement) → télécommande → rail → dock. `#cut` (`hidden`) : non focalisable (`display:none`). Noms accessibles : 65 contrôles relevés dans l'arbre d'accessibilité (feuille ouverte), aucun sans nom. Régions live comptées pendant nuit + rêve + télécommande + trois étapes d'histoire : `#t-phrase` 4, `#t-cle` 2, `#infoText` 4, rien d'autre ; aucune écriture par image.
- Retours < 100 ms (spec §2) : segments, ✕, `.bouton`, pastilles d'avatar (`:active` 60 ms), bouton du rail (`.tire` 80 ms), cartes (`.appui` 60 ms), « Encore » et télécommande (`.appui`), zones (liseré au survol, `.sel` dès l'appui), épingles (plantées à ressort, et maintenant l'éclat au survol). Surprises en place : « Encore un rêve », clin d'œil de la lune, bâillement, épingle qui brille, bouloche, transformations ridicules de la télécommande. Absente : le chien pirate qui passe dans un coin après la chanson (la danse des chiens pirates en tient lieu).
- `z-index` (loupe allumée) : les deux dialogs (couche du dessus, `showModal`) > `#lens` (6) > volet `#info` (2) > étiquette `#label` (1), tous trois dans `.cadre`. Captures `shots/t18-z-loupe-volet.png`, `t18-z-loupe-chanson.png`, `t18-z-loupe-feuille.png`.
- Thème changé en plein rêve (`setTheme('riso')` à `temps=3`, badge gagné) : verdict, film, phrase, télécommande, journée, 4 cartes du cortex, 2 décors, badge identiques avant / après. `shots/t18-theme-avant.png`, `t18-theme-apres.png`, `t18-theme-apres-dedans.png`.
- Téléphone 420 × 900 (Playwright, Firefox) : `scrollWidth` 420, une colonne, rail horizontal sous la scène (curseur 300 × 64), dock sur deux rangées (jeux 121 × 114, outils 124 × 56), fiche de l'histoire et du jeu 2 sans défilement interne, feuille de réglages pleine largeur sans débord. `shots/t18-tel-reve.png`, `t18-tel-histoire.png`, `t18-tel-feuille.png`, `t18-tel-jeu2.png`, `t18-dock-420.png`.
- Parcours complet, console (Playwright Firefox, http://127.0.0.1:8828, `lite=0`) : chargement → 4 cartes (clics réels et clavier) → glissé du rail jusqu'à la nuit → Dedans → rêve (cauchemar) → télécommande en ligne (chanson, iframe) → hors ligne (`setOffline` : « Chante ta chanson ! ») → histoire jusqu'au bout (badge) → jeu 1 (3 sur 3) → jeu 2 → loupe promenée → réglages (prénom, riso, fille) → rechargement (riso, fille, Léa, badge gardés). **0 erreur, 0 avertissement de la page** ; 18 avertissements « unreachable code after return statement » de `https://www.google.com/js/th/…` (le lecteur YouTube, tiers).
- Tests : 69/69. Générateurs `gen-cartes.py` et `gen-reve.py` relancés : `index.html` inchangé à l'octet (les autres demandent shapely ; leurs blocs ne sont pas touchés).

**Loupe : différences résiduelles (note demandée par la revue de Task 14).** Le clone `<use href="#scene-inner">` ne reprend que le SVG : les calques HTML posés sur la scène (le volet `#info`, l'étiquette `#label`, le rail) n'y sont pas, et les états `:hover` (liseré d'une zone survolée, carte qui se soulève) ne s'appliquent qu'à l'original. Parité au pixel vérifiée par la revue sur 10 configurations sinon.

**Registre des mineurs différés** (corrigé : comment ; laissé : pourquoi).
- Task 1 — police Google en feuille bloquante : *laissé*, choix documenté dans `<head>` (captures fidèles, la mesure de l'allégé part de l'exécution du script ; hors ligne, repli système).
- Task 1 — `?theme=` écrase la préférence : *corrigé* (`setTheme(nom, memo)`).
- Task 1 — mouvement réduit lu une seule fois : *corrigé* (écouteur `change` de `REDUIT`).
- Task 1 — `URL_ETAT.cartes` inutilisé : *sans objet* (lu par Task 8). `#glassRed/Blue/Yellow` : *laissés*, référence figée de l'épingle v10 que `#glassShade` reproduit (commentaire en place).
- Task 1 — riso, fond de scène plus sombre que la carte : *sans objet* (habillage « Plein ciel » de Task 1b, plus de carte).
- Task 1 — `test/shot.sh` dépend de `$PWD` : *corrigé*.
- Task 2 — carte « peur » « va s'en occuper » : *corrigé* (« va ranger ce souvenir avec les autres »).
- Task 2 — `crane` affirme la croissance la nuit : *corrigé*, aligné sur `cellule` (une hormone aide les os à grandir).
- Task 2 — « Pfffuiiit ! » mal prononcé par la synthèse vocale : *sans objet* (aucun son depuis Task 1b).
- Task 2 — titres à parenthèses lus avec une pause : *laissé* (forme utile aux parents, qui lisent ; pas de synthèse vocale).
- Task 2 — étapes 5-6 de l'histoire trop longues : *corrigé* (31 et 35 mots au lieu de 43 et 45 ; les termes « sommeil profond » et « sommeil paradoxal » restent, testés).
- Task 2 — `amygdale` ne dit pas « devant le sac à souvenirs » : *corrigé*.
- Task 2 — 18 t / La Défense non utilisés : *laissé* (choix de contenu : la statue de 12 m suffit à 4 ans).
- Task 2 — test des cibles de JEU_PARTIES en vue 1 : *déjà fait* en Task 16 (`test/jeux.test.js`).
- Task 2 — `entree:'oreille'` pour le câlin : *laissé* (il faudrait une 3e porte brodée, « la peau », dans `gen-cartes.py` ; l'oreille reste défendable : « je t'aime » s'entend).
- Task 2 — émoji 👹 → 🧌 : *laissé* (🧌 date d'Unicode 14, 2021 : carré vide sur les tablettes anciennes ; l'émoji n'apparaît que dans le jeu 2 et le volet).
- Task 2 — gabarit `reve` à post-traiter : *déjà fait* en Task 10.
- Task 3 — couture de la pinéale à peine visible, coude de l'hypophyse : *laissés* (invisibles à 1×, générateur à relancer avec shapely).
- Task 4 — étoiles hors du cadre, fenêtre d'expo, `/tmp/venv`, jetons : *déjà faits* au tour 1 de Task 4 (vérifié : les étoiles sont dans le carreau, jetons `--p-bois`, `--p-drapeau`).
- Task 4 — décors sous le lit la nuit : *déjà fait* en Task 7 (table `decor`, éteints la nuit).
- Task 4 — grain du filtre `#riso` qui laisse un fantôme du cou sous la couverture : *laissé* (encore visible, très léger, en riso de nuit ; il faudrait une sous-couche de papier sous `#p-couverture` dans `gen-dehors.py`, qui demande shapely).
- Task 4 — pas de zone « soleil » : *déjà fait* en Task 12.
- Task 3b — octets et md5 dans le rapport, capture en plein fondu : *sans objet* (rapports historiques).
- Task 3b — `/tmp/venv` volatil dans les commentaires des générateurs : *laissé* (commentaire de méthode ; le venv se recrée avec shapely, NOTES le dit).
- Task 1b — dock en graisse 700 : *corrigé* (et 18,7 px).
- Task 5 — NOTES décrit l'ancien mécanisme (fuseaux, allégé) : *corrigé* (lignes annotées « obsolète », texte d'origine gardé).
- Task 6 — images lentes en headless avec deux vues laine visibles : *laissé* (mesure logicielle ; l'allégé automatique existe).
- Task 7 — amygdale riso modeste : *corrigé* (nuit riso en groupes isolés : elle n'est plus assombrie ; halo jaune et liseré de papier nets sur le rose).
- Task 7 — coût de repaint de la tête filtrée (lueur, pouls, respiration) : *laissé* (allégé : `--amb-anim:none`).
- Task 7 — nuit riso .4 terne : *corrigé* (voir « Riso de nuit »).
- Task 7 — refactor `glisser()` : *fait*.
- Task 8 — vignette `v-pouce` peu lisible : *déjà fait* au tour 1 de Task 8 (contour épais, ongle clair) ; revu à 40 × 40 dans les deux thèmes : lisible.
- Task 8 — image lente au 1er choix (Firefox), filtres refaits au défilement : *laissé* (note de performance, allégé).
- Task 9 — étiquette « je grandis » pâle en riso : *corrigé*.
- Task 10 — ressenti seul, image ≠ phrase : *corrigé* pour le câlin (bras autour du cœur) ; les autres ressentis (visage qui rit, a peur, est fâché) et les mots se lisaient déjà dans leur vignette.
- Task 11 — l'ogre garde ses crocs en dansant : *déjà fait* au tour 1 (`.doux`). Chrome non piloté : Chrome headless pour les 45 captures ; les parcours Playwright restent sous Firefox (le navigateur de l'outil).
- Task 11 — texte « bronze » faux quand la base n'est pas le pouce : *corrigé* (`TRANSFOS[0].statue`).
- Task 12 — zones de vagues mesurées au chargement, zones qui ne respirent pas : *laissé* (écart de quelques unités, marges de 6 à 10).
- Task 14 — commentaire « 184 unités » : *corrigé* (142,9 ; 154,6 sur téléphone) ; commentaire `aria-label` : *corrigé* ; différences résiduelles : *notées* plus haut ; note historique : *corrigée* (Task 5).
- Task 15 — « pouce1 / 11 » : *corrigé*. Rêve refait sans animation si déjà en phase 3 : *laissé*, voulu (le film déjà à l'écran est redessiné à la graine 0 sans rejouer la projection, pas de clignement).
- Task 16 — doublon des crochets recit/jeu : *corrigé* (propriétaire du volet). Fiche du jeu 1 qui couvre la moitié basse de la scène sur téléphone : *laissé* (le cerveau reste visible au-dessus de la fiche ; non mesuré zone par zone, comme noté en Task 16).
- Task 17 — ✓ seulement visuel, lien non reconnu qui garde l'ancien id : *laissé*, voulu (le message `#chansonEtat` est lu ; garder la chanson qui marche vaut mieux que l'effacer).
- Documentation de `#woolVignette` / `#woolMini` : *déjà faite* (NOTES, Task 8 ; commentaire dans `<defs>`).

**Ce qui a raté.** (1) Le premier essai de nuit riso en normal sans isolation : la peau, en multiply, se multipliait avec la toile de nuit (visage olive). (2) La bouloche couleur cheveux, posée sur les cheveux : invisible ; elle est devenue une bouloche de pyjama qui monte du col. (3) Déclenchée par l'événement `journee`, elle partait aussi pour `?cartes=` et l'histoire : elle est appelée par le seul geste de l'enfant. (4) `boundingBox()` d'une carte `<g>` en Firefox englobe les symboles débordants : les clics réels visent `.carte-fond`. (5) Le dock passait déjà sur deux rangées à 1280 × 900 avant cette tâche (et toujours) : `--hors-scene` suppose un dock d'une rangée ; à 1400 × 1000 il tient sur une.

### État au 30 octobre 2026

La page est complète : trois vues croisées avec cinq moments, une journée de 1 à 4 cartes rangée la nuit puis mélangée en un rêve dessiné et expliqué, la télécommande qui change le film (chanson YouTube sur appui, repli « Chante ta chanson ! » hors ligne), l'histoire vraie du pouce en onze étapes, deux mini-jeux avec étoiles, confettis et badge, la loupe, les zones nommées dans les deux thèmes (feutrine par défaut, riso), la version allégée automatique, les réglages pour l'enfant et les conseils pour les parents. 15 combinaisons vue × temps vérifiées en feutrine, riso et allégé, sans élément orphelin ; budget de laine ≤ 21 pièces par vue visible ; console propre sur tout le parcours ; mouvement réduit, clavier et téléphone 420 px vérifiés ; 69 tests. Restent, connus et acceptés : le fantôme du cou sous la couverture en riso, le chien pirate qui ne passe pas après la chanson, les étapes qui arrivent avant la fin d'un glissé sur une machine lente, le coût de la loupe en feutrine complète (~150 ms par image en Chromium logiciel). Prochaine étape : Task 19.

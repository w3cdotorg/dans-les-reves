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

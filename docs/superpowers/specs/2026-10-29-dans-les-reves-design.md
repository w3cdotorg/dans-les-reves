# « Dans les rêves » 🌙 — spec de design

**Date :** 2026-10-29
**Projet :** explorateur du cerveau et des rêves pour un enfant de 4 ans ½ – 5 ans qui ne lit
pas encore, en français. Dépôt public `w3cdotorg/dans-les-reves`, publié sur GitHub Pages.
**Famille :** petit frère de *Dans mon corps* (un curseur de couches) et de *Dans le volcan*
(deux curseurs croisés), dont on reprend les mécanismes d'interaction, **pas** l'esthétique.
**Pièces jointes :** `docs/recherche-cerveau-sommeil.md` (science et sources),
`docs/brainstorm/2026-10-29-feutrine-aiguille-v10.html` (rendu de référence des deux
thèmes), `docs/refs/renard-laine-feutree-etsy.jpg` (référence de matière), `NOTES.md`
(journal des décisions, recettes de filtres).

## 1. Intention et pourquoi

Un jour, l'enfant a vu le pouce géant de César devant une expo de street art. Des copains
ont ri : « c'est le pouce d'un ogre ». La nuit même, il s'est réveillé plusieurs fois,
terrorisé par « un ogre gigantesque ». Ses parents lui ont chanté « Hey, ho, les chiens
pirates ! » pour lui changer les idées, et ça a marché.

L'explorateur raconte ce qui s'est passé dans sa tête, et le lui fait **manipuler** :
dans la journée, le cerveau prend des morceaux de ce qu'on vit ; la nuit, il les range,
il les rejoue et il les **mélange** ; parfois le mélange fait un beau rêve, parfois un
cauchemar, et dans les deux cas ce n'est pas pour de vrai. Et quand le film fait peur, on
peut **changer de chaîne** — avec sa chanson préférée.

Double objectif, les deux comptent autant :
- **S'émerveiller** : « mon cerveau travaille pendant que je dors ! »
- **Se rassurer** : « l'ogre, c'est mon cerveau qui a mélangé le pouce et le mot ogre. »
  Le second objectif impose de donner à l'enfant un **outil réutilisable** la nuit, sans
  écran : la télécommande (§4.6) et sa phrase-clé.

**Usage : en journée, à tête reposée, avec un parent.** Jamais au coucher (toutes les
sources convergent : pas d'écran ni de contenu lié à la peur dans l'heure qui précède le
coucher). Cela libère deux choses : on peut dessiner le cauchemar franchement, et la page
peut vivre tout le cycle jour → nuit → matin.

## 2. Objectifs, non-objectifs, anti-objectifs

**Objectifs**
- **C'est fun à utiliser** (objectif ajouté par le propriétaire le 29/10, à égalité avec les
  deux autres). Concrètement, « fun » se vérifie :
  - *Tout répond au doigt, tout de suite* : chaque appui produit un retour visible en moins
    de 100 ms (la carte se soulève et oscille, l'épingle se plante avec un petit rebond, la
    pastille gonfle, le bouton s'enfonce). Rien n'est inerte.
  - *Le cerveau est un personnage* : il mange les souvenirs qui arrivent (petit « miam »
    visuel : l'hippocampe gonfle), il ronfle en nuit profonde, ses yeux s'agitent en nuit
    des rêves, il bâille au matin ; l'enfant endormi sourit ou fronce les sourcils.
  - *Des surprises* : « Encore un rêve » change la variante ; une bouloche se décroche
    parfois et flotte ; les épingles brillent quand on passe dessus ; la lune cligne de
    l'œil une fois sur dix ; un chien pirate passe dans un coin après la chanson.
  - *Le rire désamorce* : les transformations de la télécommande sont franchement
    ridicules (l'ogre rapetisse avec un bruit de ballon qui se dégonfle… **dessiné**, pas
    sonore ; oreilles de lapin ; danse maladroite) et la phrase le dit avec humour.
  - *Des récompenses* : étoiles, confettis de laine, un « bravo » brodé, et à la fin de
    l'histoire du pouce, un badge en feutrine « Je connais mon cerveau ».
  - *Le mouvement est juteux* : easings à ressort (`cubic-bezier(.34,1.56,.64,1)`),
    squash & stretch léger sur les pièces, jamais linéaire ; mais tout reste **doux**
    (pas de flash, pas de secousse violente, aucun son) et tout
    est coupé par `prefers-reduced-motion`.
- Un enfant de 5 ans pilote tout seul : gros boutons, pastilles, curseurs, cartes à toucher.
- Chaque zone touchée est nommée et expliquée en deux phrases, affichées en gros dans un
  volet ; c'est l'adulte qui lit (décision du propriétaire, 2026-10-29 : **aucun son**, pas
  de synthèse vocale).
- Le mécanisme « journée → rangement → mélange → rêve » est **manipulable** : l'enfant
  compose sa journée avec des cartes-souvenirs, et le rêve de la nuit est fabriqué à partir
  de ses cartes. Chaque rêve est expliqué en une phrase (« parce que ton cerveau a mélangé
  … avec … »).
- L'histoire vraie du pouce est racontée telle quelle, en mode guidé.
- La science est prise au sérieux (régions du cerveau à leur vraie place, sommeil profond
  ≠ sommeil des rêves, cauchemar ≠ terreur nocturne pour les parents), avec le vocabulaire
  et les formulations validés dans `docs/recherche-cerveau-sommeil.md` §5.
- Deux thèmes de rendu, **feutrine à l'aiguille (par défaut)** et **risographe**, sur un
  seul dessin.

**Non-objectifs (YAGNI)**
- Pas de backend, pas de compte, pas de sauvegarde autre que les préférences locales
  (thème, version allégée, prénom, chanson, carte réconfort, avatar : garçon/fille,
  carnation, cheveux, badge « Je connais mon cerveau » gagné).
- Pas d'autre langue que le français.
- **Aucun son** produit par la page (pas de synthèse vocale, pas de bruitages, pas de
  musique) ; la seule exception est la vidéo YouTube de la chanson, créée sur appui.
- Pas de 3D, pas de bibliothèque externe (Three.js resterait possible plus tard en
  `vendor/` pour un bonus « tourne le cerveau », hors de ce projet).
- Pas de générateur de rêves « intelligent » : les recettes sont des règles simples et
  lisibles (§4.5), pas un modèle.
- Pas de choix d'âge ni de niveau : un seul niveau, 4-5 ans.

**Anti-objectifs (ce qui serait un échec même si ça marche)**
- **Un style de dessin « habituel »** : le planétarium néon aux cartes de verre dépoli des
  deux grands frères, ou n'importe quel vectoriel lisse « mignon ». La matière est
  **feutrine / laine feutrée**, voir §6.
- L'ogre en dernière image. Le cauchemar est montré franchement mais **toujours
  immédiatement domestiqué**, et la séquence se termine toujours sur le film changé.
- Toute formulation qui confirme l'existence du monstre (« on va le chasser ») ou qui
  présente le cauchemar comme une erreur du cerveau (« ton cerveau s'est trompé »).
- Dire que « le cerveau se repose la nuit » : il **travaille**.
- Présenter comme certain ce qui est une hypothèse (la « thérapie de nuit » des rêves, le
  « nettoyage des poisons ») : on dit « beaucoup de chercheurs pensent que » et « les
  chercheurs ne savent pas encore tout » — c'est l'esprit Canopé / La main à la pâte.

## 3. Contraintes

- **Un seul fichier `index.html`** : HTML, CSS, JS en ligne, SVG dessiné à la main, aucune
  image bitmap. Aucun appel réseau obligatoire : Google Fonts (Fredoka, Baloo 2) avec repli
  système ; l'iframe YouTube n'est chargée que sur appui, via `youtube-nocookie.com`, et se
  dégrade hors ligne en un bouton « chante ta chanson ».
- Fonctionne en ouvrant le fichier (`open index.html`) et sur GitHub Pages, tablette et
  téléphone compris (grille deux colonnes → une colonne sous 900 px, comme les aînés).
- `prefers-reduced-motion` coupe toutes les animations d'ambiance (les transitions d'état
  restent, instantanées).
- Clavier : ←→ curseur temps, ↑↓ curseur vue, Tab sur toutes les zones, `aria-label` tenu à
  jour depuis la même source que le texte affiché.
- Cibles tactiles ≥ 44 px. Sur tablette il n'y a pas de survol : bouton « Montrer les
  zones » obligatoire.
- **Budget de rendu** : le filtre laine coûte ~35 primitives par pièce. Règles : ≤ 40 pièces
  filtrées en même temps par vue ; les petits détails (yeux, nœuds, fils) ne portent qu'un
  filtre léger ou aucun ; les zones cliquables sont des formes transparentes **non
  filtrées** posées au-dessus ; une **version allégée** du thème (découpe + ombre +
  coutures, sans fibres ni bouloches) s'active automatiquement si le premier rendu dépasse
  un seuil (mesure d'une image au chargement) ou si `prefers-reduced-motion` est actif, et
  reste choisissable à la main.
- Vie privée : la vidéo ne se charge que sur appui ; prénom et chanson restent dans
  `localStorage` ; aucun suivi.
- Licence MIT, comme les aînés.

## 4. Le mécanisme central

### 4.1 Deux curseurs croisés (repris du volcan)

**Curseur TEMPS** (flèches ←→, glissière continue + 5 pastilles) — « le fil de la journée » :

| | Pastille | Ce qui se passe |
|---|---|---|
| 1 | **La journée** ☀️ | L'enfant vit des choses. Les cartes-souvenirs choisies entrent par les yeux et les oreilles, passent par le thalamus (« la gare ») et vont se poser dans l'hippocampe (« le sac à souvenirs tout neufs »). |
| 2 | **Le soir** 🌇 | La toile s'assombrit. Dans la tête, la petite glande du milieu (pinéale) s'allume et envoie « c'est la nuit » ; les yeux se ferment ; c'est le moment de la chanson et du doudou. |
| 3 | **La nuit profonde** 💤 | *Sommeil profond.* Le trieur : de grandes vagues lentes roulent sur le cortex ; l'hippocampe **rejoue** les cartes et les envoie se ranger dans le cortex (« la grande couverture plissée où les souvenirs restent longtemps ») ; le cerveau se **rince** ; le corps **grandit**. Les cartes les moins importantes s'effacent. |
| 4 | **La nuit des rêves** 🌙 | *Sommeil paradoxal.* Le projecteur : les yeux bougent sous les paupières ; le « chef » (lobe frontal, celui qui réfléchit et vérifie) dort encore ; l'alarme de la peur (amygdale) est allumée ; le cortex **mélange** les morceaux et projette le film du rêve sur l'écran. C'est ici que le rêve est fabriqué (§4.5). |
| 5 | **Le matin** 🐓 | On se réveille, le film s'arrête, parfois on s'en souvient, parfois pas. On peut le raconter, et de jour, on peut **lui changer sa tête** (§4.6). |

Fondu continu entre les pastilles, comme dans le volcan : la glissière interpole opacités,
transformations et niveaux (lumière de la toile, position des cartes, ondes, lueur de
l'amygdale, vitesse des yeux), il n'y a pas 5 dessins séparés.

**Curseur VUE** (flèches ↑↓, 3 pastilles) — « où on regarde » :

1. **Dehors** 🏞️ — l'enfant dans son monde, de profil au centre. Le jour : la scène de la
   journée autour de lui (le pouce géant, les copains, le soleil, et les objets des cartes
   choisies). La nuit : son lit, le doudou, la lampe, la fenêtre et la lune. C'est **ici
   qu'on choisit les cartes** (§4.3) et qu'on les voit entrer par les yeux et les oreilles.
2. **Dedans** 🧠 — la tête en coupe, le cerveau et ses régions, les cartes qui circulent,
   l'écran du rêve au-dessus. La vue principale, celle de la maquette.
3. **Tout près** 🔬 — à l'intérieur du cerveau, à hauteur de neurones : des neurones qui
   « se parlent » par étincelles, les grandes vagues lentes, les petites rafales qui
   « collent » les souvenirs (fuseaux), le rinçage, les cellules qui grandissent. Vue plus
   légère (moins de zones), là pour l'émerveillement.

Les trois vues réagissent au temps (3 × 5 combinaisons sans état incohérent), avec des
éléments partagés (la tête, le ciel/la toile, les cartes).

### 4.2 La scène

Une seule scène SVG paysage (viewBox 900 × 560, même ratio que le volcan). La tête de
l'enfant, de profil et regardant vers la droite, occupe le centre-gauche ; le côté droit est
celui de la nuit et porte **l'écran du rêve** (une grande pièce de laine crème en forme de
nuage-écran, épinglée). En bas, la **boîte à souvenirs** : la rangée de cartes.

Garçon ou fille, carnation et cheveux : repris de *Dans mon corps* (mêmes variables
CSS, même commande visible en haut de la scène), parce que l'enfant doit se reconnaître ;
le choix est mémorisé. En feutrine, les cheveux sont une pièce de laine, les yeux des
boutons. **La narration s'accorde avec l'avatar** (choix du rédacteur après relecture) :
toutes les phrases de narration et de zones qui parlent de l'enfant existent en forme
masculine et féminine dès l'écriture, via une petite fonction d'accord dans les données
(`{il|elle}`, `{terrorisé|terrorisée}`) ; l'histoire du pouce suit donc l'avatar et le
prénom saisi, même si l'anecdote d'origine concerne un garçon.

**Le décor Dehors est piloté par les cartes** (choix du rédacteur après relecture) : la
scène de jour a un fond fixe (ciel, sol, le bâtiment de l'expo, l'enfant) et tout le
reste — le pouce de César, les copains, la glace, le chien… — n'apparaît que si sa carte a
été choisie (ou pré-remplie par le mode guidé). On ne voit donc jamais dehors une chose
qui n'entre pas dans la tête : le décor **est** la journée. Les zones Dehors « le pouce de
César » et « les copains » ne sont cliquables que lorsqu'elles sont présentes.

### 4.3 Les cartes-souvenirs

Des pièces de feutrine crème épinglées en bas de la scène (épingle à tête de verre, voir
NOTES.md « épingles plantées »). Chaque carte porte un petit dessin en laine, un nom lu à
voix haute, une **catégorie** et une **charge** :

| Catégorie | Cartes (nom lu) | Charge |
|---|---|---|
| Choses vues | le pouce géant 👍, une glace, un chien, un vélo, la piscine, un gâteau d'anniversaire, un tracteur, un orage, un manège | neutre, sauf **orage** (peur) |
| Mots entendus | le mot « ogre », le mot « pirate », le mot « dragon », le mot « anniversaire » | **ogre, dragon** (peur) ; pirate (joie) |
| Gens | les copains, papa et maman, mamie, la maîtresse | joie |
| Ce que j'ai ressenti | j'ai ri, j'ai eu peur, je me suis fâché, un câlin | selon le nom |
| Réconfort (cartes spéciales, voir §4.6) | ma chanson, mon doudou, un câlin | **apaisante** |

- L'enfant touche une carte : elle se dé-épingle, s'anime vers la scène « Dehors » (elle
  devient un élément du décor du jour) et, en vue « Dedans », on la voit entrer par l'œil
  (choses vues) ou par l'oreille (mots entendus, gens, ressentis) puis aller dans
  l'hippocampe. **Au plus 4 cartes** dans une journée (au-delà, la plus ancienne revient
  dans la boîte avec un petit « oups, trop de choses ! » qui est aussi une vraie leçon :
  le cerveau ne garde pas tout). La carte réconfort ajoutée par la télécommande (§4.6)
  occupe un **emplacement à part** et ne compte pas dans les 4.
- **Échelle des charges** (choix du rédacteur après relecture), une valeur par carte dans
  les données : **peur = 3** (ogre, dragon, orage, j'ai eu peur), **colère = 2** (je me suis
  fâché), **joie = 1** (copains, pirate, anniversaire, câlin, j'ai ri, gens), **neutre = 0**
  (choses vues ordinaires, le pouce géant compris), **apaisante = −2** (ma chanson, mon
  doudou, un câlin quand il est choisi comme carte réconfort). La « charge la plus forte »
  est la plus grande valeur absolue, peur avant colère avant joie.
- Le bouton **« Nouvelle journée »** renvoie toutes les cartes dans la boîte et remet le
  temps au matin.
- Les cartes sont la **seule** source du rêve : pas de carte, pas de rêve (« Tu n'as rien
  mis dans ta journée : cette nuit, le cerveau range et se rince, et le rêve est tout
  flou », ce qui est honnête).

### 4.4 Le rangement (nuit profonde)

Quand le curseur traverse la nuit profonde : chaque carte quitte l'hippocampe sur une
vague lente, va se coudre dans le cortex (petite animation de point de couture), et
**rétrécit** : les cartes de charge 0 deviennent petites (« rangé »), les cartes de charge
non nulle restent grandes et **restent accrochées à l'amygdale** par un fil : rouge pour la
peur, orange pour la colère, rose pour la joie, bleu doux pour une carte apaisante. C'est ce qui prépare le rêve : le cerveau garde en avant ce qui l'a remué.
Pendant ce temps, le rinçage (vagues bleu pâle qui passent dans les plis), les « zzz » du
lobe frontal, la petite étiquette « je grandis » sur l'os du crâne.

### 4.5 La fabrication du rêve (nuit des rêves)

Règles simples, lisibles, déterministes pour une même journée (pour que l'enfant puisse
refaire « sa » nuit), avec une part de variation visuelle sur « Encore un rêve » :

1. **Choisir les ingrédients** (règle corrigée après relecture) : la **greffe** est la
   carte de charge la plus forte (ex æquo : la plus récemment choisie). La **base** est la
   carte la plus *concrète* parmi les autres, dans l'ordre chose vue > gens > mot entendu >
   ressenti (ex æquo : la plus récente). Une troisième carte, la plus concrète des
   restantes, devient le **contexte** : elle apparaît en petit dans le fond de l'écran, et
   c'est elle qui s'efface quand le modificateur est « gigantesque ». Les autres cartes sont
   « oubliées » pour ce rêve (elles pâlissent). Vérification sur l'histoire du pouce (pouce
   géant, mot « ogre », copains, j'ai ri) : greffe = ogre, base = pouce géant, contexte =
   copains → « le pouce est devenu un ogre gigantesque, les copains ont disparu ». Avec une
   **seule carte**, elle est sa propre base, sans greffe : rêve de la carte seule avec un
   modificateur (« tout petit », « multiplié » ou « d'une autre couleur ») et la phrase
   « parce que ton cerveau l'a rejouée ». Si la carte la plus forte est une carte
   **apaisante**, elle n'est pas greffe mais **fin du rêve** (voir le verdict).
2. **Une base et une greffe** : la base donne sa grande forme de rêve, la greffe son
   attribut de rêve (des yeux et des dents pour « ogre », un chapeau et un sabre pour
   « pirate », des ailes et du feu pour « dragon », un cornet et des gouttes pour « glace »,
   une queue qui remue pour « chien », des guirlandes pour « anniversaire »…). Chaque carte
   possède donc trois dessins : sa vignette, sa forme de base, sa greffe ; les ressentis
   n'ont pas de forme de base (ils ne peuvent être que greffe ou contexte : « j'ai ri »
   greffe un grand sourire, « j'ai eu peur » de grands yeux).
3. **Un modificateur**, tiré de la charge de la greffe : peur → **gigantesque** (la base
   grandit jusqu'à déborder l'écran, le contexte s'efface) ; colère → **à l'envers** ou
   **qui n'obéit pas** (la base se tourne, se secoue) ; joie → **multiplié** ; neutre → **tout
   petit** ou **d'une autre couleur**. Le modificateur est toujours **nommé** dans la phrase.
4. **Verdict** : charge de la greffe = peur → **cauchemar** : la toile vire au bleu profond,
   l'amygdale pulse en rouge, l'enfant endormi fronce les sourcils, l'écran tremble
   légèrement. Colère → **rêve bizarre** (amygdale orange, sourcils froncés, pas de
   tremblement). Joie ou neutre → **beau rêve** ou **rêve rigolo** : l'écran se colore,
   l'enfant sourit. Si la journée contient **aussi** une carte apaisante (chanson, doudou,
   câlin choisi comme réconfort), un cauchemar devient un **mauvais rêve qui finit bien** :
   l'ogre apparaît, puis la carte apaisante entre dans l'écran et applique d'elle-même une
   transformation de la télécommande, avec la phrase « … mais ta chanson était dans ta
   tête, alors le film a changé tout seul ». C'est le message de la page, et c'est honnête :
   une routine apaisante réduit les cauchemars.
5. **La phrase** (affichée et lue) suit toujours le même gabarit :
   « Dans le rêve, *[base]* est devenu *[greffe + modificateur]*, parce que ton cerveau a
   mélangé *[carte 1]* avec *[carte 2]*. Le chef qui vérifie dormait, alors personne n'a
   dit "mais non, c'est une statue !" »
   Exemples : pouce géant + ogre → « le pouce est devenu un ogre gigantesque » ; glace +
   chien → « le chien est devenu un chien en glace, tout petit, qui fond » ; copains +
   pirate → « les copains sont devenus des pirates multipliés, il y en avait partout ».
6. **Jamais en dernier plan** : un cauchemar affiche aussitôt la **télécommande** (§4.6)
   avec une pulsation, et la narration enchaîne : « Mais on a une télécommande… ».

Le dessin du rêve est composé en SVG à partir des trois assets par carte, avec des
transformations CSS (échelle, répétition par `<use>`, retournement, teinte via variables).
Le constructeur fixe la grammaire exacte des greffes ; la spec exige seulement que **toute
paire de cartes produise un rêve lisible et une phrase correcte**, ce qui se vérifie par un
test qui parcourt toutes les paires.

### 4.6 La télécommande (changer de chaîne)

Un gros bouton en forme de télécommande en feutrine (avec des boutons-pressions), visible
en nuit des rêves et au matin, qui pulse après un cauchemar. Appuyer :
1. ajoute une **carte réconfort** au rêve (par défaut « ma chanson » ; « mon doudou » ou
   « un câlin » si le parent les a choisis dans les réglages) ;
2. **transforme le film** sous les yeux de l'enfant, sans faire disparaître l'ogre d'un
   coup : il rapetisse jusqu'à redevenir le pouce de bronze, ou reçoit des oreilles de
   lapin, ou se met à danser avec les chiens pirates — trois transformations possibles,
   choisies en rotation, toutes **ridicules ou gentilles**, jamais « vaincu » ;
3. lance la **chanson** : l'iframe YouTube « Hey, ho, les chiens pirates ! » (l'école des
   loisirs, autorisation obtenue par le propriétaire) s'ouvre dans une carte en verre…
   non : dans une **pièce de feutrine à fenêtre cousue**, et joue. Hors ligne, la pièce
   affiche « Chante ta chanson ! » avec le titre de la chanson saisi par le parent ;
4. dit la **phrase-clé** que l'enfant pourra réutiliser la nuit sans écran : « C'est mon
   cerveau qui a mélangé. C'est un rêve. Je change de chaîne. » — affichée en gros (l'adulte
   la lit avec l'enfant), c'est l'outil que la page laisse à l'enfant.

Au matin, la télécommande reste disponible : « Tu veux lui changer sa tête ? » (c'est la
version de jour, celle que recommandent les psychologues : transformer le rêve en quelque
chose de drôle, par le dessin ou l'histoire).

### 4.7 Le mode guidé : « L'histoire du pouce »

Un bouton en haut : **« Raconte-moi l'histoire du pouce »**. Il pré-remplit la journée
(le pouce géant, le mot « ogre », les copains, j'ai ri), met la vue sur Dehors, et fait
avancer le temps tout seul, étape par étape, avec une narration lue (une phrase par étape,
l'enfant appuie sur « Et après ? » pour continuer — pas d'auto-défilement). L'histoire va
jusqu'au cauchemar, à la télécommande et à la chanson, puis au matin : « Le lendemain, il a
raconté l'ogre gigantesque. Et maintenant, il sait d'où il venait. » Le prénom de l'enfant,
s'il a été saisi, remplace « il ». À la fin : « À toi de faire ta journée ! », qui renvoie
au mode libre.

Dans la scène Dehors de cette histoire, le pouce est **vraiment** le pouce de César : une
pièce de laine couleur bronze de 12 m à l'échelle de l'enfant (vingt fois sa taille), avec
l'ongle et les plis, cliquable : « C'est une statue en bronze, faite par un artiste qui
s'appelle César. Elle est très grande, mais elle ne bouge pas. »

## 5. Les zones nommées (étiquette + deux phrases)

Le constructeur écrit tous les textes avec le vocabulaire et les formulations-modèles de
`docs/recherche-cerveau-sommeil.md` §5 (mots validés, métaphores honnêtes, tournures de
prudence). Ton : celui des aînés, deux phrases, pas de jargon non expliqué, pas de
diminutif niais. Liste minimale (≈ 32 zones) :

**Dedans (≈ 18)** : le cerveau (cortex, « la grande couverture plissée ») · le lobe de
devant / le chef (frontal : réfléchit, vérifie, dort pendant les rêves) · le lobe des
yeux (occipital, à l'arrière) · le lobe des oreilles (temporal, à hauteur de l'oreille) ·
le lobe du toucher (pariétal) · l'hippocampe (le sac à souvenirs tout neufs, **dans le lobe
temporal, à hauteur du conduit auditif**, dessiné en transparence) · l'amygdale (l'alarme
de la peur, **devant** l'hippocampe) · le thalamus (la gare : tout ce que voient les yeux
et entendent les oreilles passe par là) · l'horloge (hypothalamus / noyaux
suprachiasmatiques, juste au-dessus du croisement des nerfs des yeux) · la petite glande
de la nuit (pinéale, **au centre, derrière le thalamus**, jamais au front) · le pont entre
les deux moitiés (corps calleux) · le cervelet (l'équilibre et les gestes, séparé et strié)
· le tronc (respirer, le cœur : ne dort jamais) · la moelle épinière · le nerf de l'œil
(vers l'arrière et le centre) · l'œil et les paupières (qui bougent pendant les rêves) ·
l'oreille et le petit escargot (cochlée) · le casque d'os (crâne) et le coussin d'eau
(liquide, qui rince).

**Dehors (≈ 9)** : le soleil / la lune · la lampe (lumière = « jour » pour l'horloge) · le
lit · le doudou · la fenêtre · le bâtiment de l'expo · la boîte à souvenirs · l'écran du
rêve · et, **quand leur carte est choisie**, chaque chose du décor (le pouce de César, les
copains, la glace…) avec son propre texte.

**Tout près (≈ 5)** : un neurone · une étincelle (synapse, « ils se parlent ») · une
grande vague lente · une petite rafale qui colle (fuseau) · une cellule qui grandit.

Erreurs de dessin interdites (recherche §2.8) : hippocampe « au centre », amygdale derrière
l'hippocampe, pinéale au front, cervelet collé et lisse, nerf optique qui monte.

## 6. Esthétique : deux thèmes, un dessin

Le rendu de référence est `docs/brainstorm/2026-10-29-feutrine-aiguille-v10.html` ; les
recettes de filtres, avec les réglages qui ont raté et pourquoi, sont dans `NOTES.md`.
Ces recettes sont **la** référence : on les transpose, on ne les réinvente pas.

**Thème « Feutrine » (par défaut)** — laine feutrée à l'aiguille, d'après le renard de
`docs/refs/` :
- Toile de lin (motif + grain) qui **s'assombrit elle-même** vers la nuit, par un dégradé
  multiplié qui suit le curseur temps ; la trame reste visible dans la nuit. Contrastes
  surveillés : pièces crème, fil blanc, halos clairs sur le bleu nuit.
- Chaque pièce est **bombée** (relief calculé sur sa forme, lumière douce du haut-gauche,
  reflet quasi nul : la laine est mate), avec un **halo de fibres** de sa couleur sur tout
  le contour, des fibres fines et régulières (la surface reste calme, la matière se lit au
  bord), une teinture presque imperceptible, des **bouloches rares**, une ombre portée
  d'objet épais.
- **Broderies** : les sillons du cerveau sont des volutes blanches au point de tige
  terminées par des nœuds français ; les étoiles sont des nœuds français de fil blanc ; les
  yeux fermés sont un trait brodé ; les cartes ont un bord cousu au point de surjet.
- **Épingles** à tête de verre (rouge, bleu, jaune) et grosse tige d'acier effilée,
  **plantées** (on ne voit que 10 px de tige, qui entre dans la laine par un petit creux).
- Yeux-boutons (deux trous), cheveux en pièce de laine, télécommande à boutons-pressions.
- Version allégée automatique (§3) : découpe + ombre + coutures seulement.

**Thème « Riso »** — trois encres (jaune, rose fluo, bleu) en `multiply`, chacune avec son
décalage de calage, couverture d'encre irrégulière, bords qui bavent, étoiles en réserve du
papier ; la nuit est la passe bleue. Validé tel quel en v5.

**Mécanique des thèmes** : un seul SVG. Les pièces portent des classes sémantiques
(`peau`, `cerveau`, `carte`, `ecran`…) et les contours sont des éléments séparés. Un thème
= une feuille de variables de couleur + un filtre de matière + un traitement des contours
(coutures en feutrine, passe bleue en riso). Interrupteur 🧶 / 🖨️ en haut de page,
mémorisé dans `localStorage`. Les deux thèmes partagent exactement la même géométrie.

Typographie : Fredoka (titres) et Baloo 2 (interface) avec repli système, comme les aînés.
Les cartes d'interface (panneau d'info, boutons) sont elles aussi en feutrine (pièces
bombées, bords cousus), **pas** en verre dépoli.

## 6 bis. L'interface « Plein ciel » (décision du propriétaire, 2026-10-29 19:54)

Le propriétaire n'a pas aimé l'habillage repris des aînés (cartes de feutrine à bord cousu,
piles de boutons-pilules) et a choisi, sur une planche de trois maquettes, la direction
**« Plein ciel »** : *la scène prend toute la place, l'habillage est moderne, calme et
plat ; la feutrine ne concerne que le dessin.* Rien de l'interface des aînés n'est à
reprendre.

**Principes**
- La scène SVG est la star : elle occupe toute la largeur disponible, dans un cadre arrondi
  (rayon 24 px), sur un fond de page uni et clair (`#fffdf8`), sans trame de lin hors de la
  scène, sans bord cousu, sans ombre « feutrine » sur les contrôles.
- Un seul geste par idée ; chaque contrôle est à l'échelle d'un doigt de 5 ans (≥ 56 px).
- Typographie : Fredoka (titres, boutons, étiquettes) et Nunito (texte courant), repli
  système. Pas d'emoji comme seul libellé : emoji + mot.
- Couleurs de l'habillage (jetons CSS, indépendants des thèmes de scène) : indigo
  `#3b3f8f` (sélection), corail `#ff7a59`, vert `#2aa876`, sable `#efeae0` (fonds de
  contrôles), encre `#2b2a33`, gris `#6c6a78`. Le thème riso ne change que la scène.

**Disposition (bureau, ≥ 900 px)**
1. **Bandeau haut** (une ligne) : à gauche le titre « 🌙 Dans les rêves » avec la tagline
   en petit ; au centre le **sélecteur de vue** segmenté (`#cut` reste l'état interne
   0..2 ; trois segments 🏞️ Dehors · 🧠 Dedans · 🔬 Tout près, segment actif indigo) ; à
   droite un bouton rond « ⋯ » (`#reglages`) qui ouvre la feuille de réglages.
2. **Scène** pleine largeur. Collé à son bord droit, le **rail du temps** (`#time`,
   0..400) : une glissière verticale de 52 px de large, dégradé soleil → coucher → nuit
   (`--p-soleil` en haut, `--nuit-2` en bas), étiquettes « jour » / « nuit », bouton rond
   blanc de 64 px dont l'icône change avec le temps (☀️ 🌇 💤 🌙 🐓). Les cinq moments
   restent accessibles au clavier (←→) et par cinq crans doux (aimantation légère).
3. **Volet d'information** (`#info`) : il monte par-dessus le bas de la scène (fond blanc à
   92 %, flou d'arrière-plan, rayon 20 px, ombre douce) avec une icône carrée à gauche
   (`#infoEmoji`), un titre (`#infoTitle`) et deux phrases (`#infoText`), un bouton ✕.
   Entrée à ressort (`cubic-bezier(.34,1.56,.64,1)`, 320 ms), sortie rapide. Le volet
   sert aussi au récit guidé (`#recit` : texte + « Et après ? » + ✖) et aux mini-jeux.
4. **Dock** sous la scène : trois gros boutons-pilules colorés, 🎯 Trouve la partie
   (corail, `#jeu1`), 💭 Rêve ou pour de vrai ? (indigo, `#jeu2`), 📖 L'histoire du pouce
   (vert, `#histoire`) ; à droite, plus petits et sable : ✨ Montrer les zones (`#zones`),
   🔍 La loupe (`#loupeBtn`), 🌅 Nouvelle journée (`#journee`).
5. **Feuille de réglages** (bouton « ⋯ », `#reglages`, `<dialog>` ou volet) : avatar
   (garçon/fille, carnations, cheveux — les pastilles de Task 3 y déménagent), thème
   (🧶 Feutrine / 🖨️ Riso, `#theme`), version allégée, et la carte « Pour les parents »
   (§8) repliée en bas. Fermée par ✕ ou Échap.

**Téléphone (< 900 px)** : bandeau sur deux lignes (titre, puis sélecteur de vue pleine
largeur) ; le rail du temps passe **sous la scène**, horizontal, même dégradé, même bouton
rond ; le dock s'empile sur deux lignes ; le volet d'information garde sa place sur la
scène. Jamais de défilement horizontal.

**Ce qui disparaît** : les boutons 🔊 Réécouter et 🔇 Son coupé, `speechSynthesis`,
`soundOn`, la clé `reves.son`, la ligne de pastilles `.moment`, les pilules `.pill`, les
cartes `.card` à bord cousu, la trame de lin sur le `body`, la ligne de pastilles d'avatar
au-dessus de la scène.

**Ce qui reste** : les ids que les tâches suivantes consomment (`#time`, `#cut`, `#info`,
`#infoEmoji`, `#infoTitle`, `#infoText`, `#zones`, `#loupeBtn`, `#jeu1`, `#jeu2`,
`#histoire`, `#journee`, `#theme`, `#parents`), `setCut`/`setTime`, les raccourcis clavier
(←→ temps, ↑↓ vue), `prefers-reduced-motion`.

**Fun** : le bouton du rail devient lune en glissant et « tombe » doucement dans le cran le
plus proche ; chaque segment ou bouton s'enfonce de 2 px et rebondit ; le volet arrive à
ressort ; le « ⋯ » tourne d'un quart de tour en s'ouvrant.

## 7. Interactions (reprises des aînés, sauf l'habillage)

- Zones cliquables : étiquette + explication dans le volet (§6 bis) ; pas de voix, pas de
  bouton son.
- **Loupe** au doigt ou à la souris (suivi cadencé sur `requestAnimationFrame`, comme dans
  le volcan après correction). La lentille clone la scène (`<use>`), donc elle **double
  temporairement** le nombre de pièces filtrées ; décision (après relecture) : en thème
  complet, la lentille montre la **laine complète** (c'est là qu'on la voit de près) et,
  tant que la loupe est active, les animations d'ambiance sont mises en pause pour
  compenser ; en version allégée, la lentille est allégée aussi. Le budget « ≤ 40 pièces
  filtrées par vue » s'entend **hors lentille**.
- **Montrer les zones** : fait pulser toutes les zones de la vue active.
- **Mini-jeu 1 « Trouve la bonne partie ! »** : 3 questions tirées d'une banque de 8,
  étoiles et confettis (en feutrine : des confettis de laine).
- **Mini-jeu 2 « Rêve ou pour de vrai ? »** (nouveau, justifié par la recherche : la
  distinction rêve / réalité se construit entre 3 et 5 ans) : une image, deux gros boutons
  « Pour de vrai » / « C'est un rêve ». Banque de 8 (« un pouce de 12 mètres » → pour de
  vrai, c'est une statue ; « un ogre gigantesque » → rêve ; « un chien qui mange une
  glace » → pour de vrai ; « un chien en glace qui fond » → rêve…). 3 questions, même
  récompense.
- Animations d'ambiance (coupées par `prefers-reduced-motion`) : clignement, respiration,
  yeux qui bougent sous les paupières la nuit des rêves, vagues lentes, rafales, rinçage,
  lueur de l'amygdale, pulsation de la pinéale au soir, « zzz » du lobe frontal, fils qui
  frémissent, épingles qui brillent.

## 8. Réglages (carte « Pour les parents », repliée par défaut)

- Prénom de l'enfant (optionnel, utilisé par la narration).
- Chanson de réconfort : titre (texte) et lien YouTube (par défaut « Hey, ho, les chiens
  pirates ! », `jqGPppvVmBc`) ; carte réconfort par défaut (chanson / doudou / câlin).
- Thème, version allégée.
- Un court texte pour les parents, tiré de la recherche §3 : outil **de jour** ; la nuit,
  aller voir, câlin, « c'était un rêve », pas de chasse au monstre ; le lendemain, « changer
  le film » ; différence cauchemar / terreur nocturne (ne pas réveiller) ; quand consulter ;
  lien vers `docs/recherche-cerveau-sommeil.md`.

## 9. Technique (choix fixés)

- Un fichier `index.html` ; SVG paysage `viewBox="0 0 900 560"` ; symboles et filtres dans
  un `<defs>` unique ; pièces appairées par `<use>` quand c'est possible.
- Les deux curseurs pilotent des interpolations par groupe (opacité, transformation,
  variables CSS) ; aucune vue n'est un dessin séparé.
- Les cartes, leurs trois assets (vignette, base, greffe), leur charge et leurs textes sont
  **des données** (un tableau JS en tête de script), de même que les textes des zones, les
  banques des deux mini-jeux et les phrases de narration. Un test parcourt toutes les
  paires de cartes et vérifie qu'un rêve et une phrase existent.
- Tests : le projet reprend l'approche des aînés (vérification visuelle par captures
  Chrome headless à chaque étape, voir NOTES.md) ; en plus, un petit script de test sans
  dépendance (Node) pour les données (paires de cartes, zones avec texte et `aria-label`,
  banques de jeu de taille attendue). Pas de framework.
- `NOTES.md` tenu à jour à chaque décision ; commits fréquents ; GitHub Pages sur `main`.

## 10. Ce qui est laissé au constructeur

- Le dessin lui-même (tête, cerveau en vue latérale avec régions profondes en
  transparence, scène Dehors de jour et de nuit, vue Tout près), dans le respect de §5 et
  de la recherche §2.8.
- La grammaire exacte des greffes et des trois transformations de la télécommande, tant
  que §4.5 et §4.6 sont respectés et que toutes les paires sont couvertes.
- L'ordre et la durée des étapes de l'histoire guidée.
- La répartition du budget de filtres (quelles pièces sont filtrées, lesquelles sont
  légères), et le seuil de bascule en version allégée.
- La structure du code et le découpage du travail.

## 11. Décisions prises après la relecture du constructeur

Les cinq questions du relecteur ont toutes été tranchées par le rédacteur (aucune ne
changeait l'intention) et intégrées ci-dessus : rôles base / greffe / contexte et cas d'une
seule carte (§4.5-1), échelle numérique des charges, colère et cartes apaisantes, emplacement
à part de la carte réconfort (§4.3, §4.5-4), narration accordée à l'avatar (§4.2), décor
Dehors piloté par les cartes (§4.2, §5), loupe en laine complète avec pause des animations
(§7).

## 12. Critères de réussite

- La page s'ouvre en local et hors ligne ; thème feutrine par défaut, riso d'un appui.
- Un enfant de 5 ans compose une journée de 1 à 4 cartes, fait avancer la nuit et obtient
  un rêve dessiné et expliqué en une phrase ; un cauchemar amène la télécommande, qui
  transforme le film, joue la chanson et dit la phrase-clé ; aucune séquence ne se termine
  sur l'ogre.
- L'histoire du pouce se raconte de bout en bout, étape par étape.
- Chaque zone est nommée et expliquée dans le volet ; les régions profondes sont à leur
  vraie place (checklist §5).
- 3 vues × 5 moments sans état incohérent ni élément orphelin.
- Les deux mini-jeux fonctionnent et félicitent l'enfant.
- Rendu fluide sur une tablette récente avec le thème complet ; version allégée lisible et
  jolie sur un appareil lent.
- `prefers-reduced-motion`, clavier, tablette : OK.
- Le style ne ressemble ni aux aînés ni à un vectoriel « habituel » : on voit la laine.
- **C'est fun** : chaque appui a un retour immédiat ; le cerveau-personnage réagit à chaque
  moment ; au moins cinq surprises et trois récompenses sont en place ; un parent qui
  teste la page sourit au moins une fois sans qu'on lui dise où regarder.

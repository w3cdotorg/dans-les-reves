# « Dans les rêves » — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Une page `index.html` unique qui fait manipuler à un enfant de 4-5 ans ce que fait son cerveau la nuit : il compose sa journée avec des cartes-souvenirs, un curseur fait passer du jour à la nuit, le cerveau range puis mélange les cartes en un rêve dessiné et expliqué, et une télécommande change le film quand c'est un cauchemar.

**Architecture:** Un seul fichier HTML/CSS/JS, SVG paysage dessiné à la main (`viewBox="0 0 900 560"`), **thème feutrine à l'aiguille par défaut** et thème riso, sur la même géométrie. Trois groupes de vue (`#g-dehors`, `#g-dedans`, `#g-pres`) en fondu piloté par `setCut(c)` (c ∈ [0,2]) ; cinq moments du temps interpolés par `setTime(t)` (t ∈ [0,4]) via `lerpArr`. Les **données** (cartes, textes des zones, banques des jeux, narration) et les **fonctions pures** (`composeDream`, `inflect`, `lerpArr`) vivent dans un bloc `/* PURE-BEGIN */ … /* PURE-END */` que les tests Node extraient et exécutent sans DOM.

**Tech Stack:** HTML/CSS/JS vanilla, SVG + filtres SVG à la main, Google Fonts (Fredoka, Baloo 2) avec repli système, `speechSynthesis`, iframe `youtube-nocookie.com` à la demande. Tests : `node --test test/` (Node 26, zéro dépendance) + captures Chrome headless / Playwright MCP.

**Spec :** `docs/superpowers/specs/2026-10-29-dans-les-reves-design.md` — la lire en entier avant de commencer une tâche. **Science et textes :** `docs/recherche-cerveau-sommeil.md` (§2.8 anatomie, §5 vocabulaire). **Rendu de référence :** `docs/brainstorm/2026-10-29-feutrine-aiguille-v10.html` (filtres `wool`, `thread`, `riso2`, `linen`, `dusk`, `#pin` à **recopier**, pas à réinventer ; leurs réglages et les erreurs évitées sont dans `NOTES.md`). **Aînés (patterns de code) :** `refs/aines/dans-le-volcan.html` (curseurs `setCut` l.2116 / `setTime` l.2175 / `lerpArr` l.2151, `INFO` l.2209, `showInfo` l.2320, voix `pickVoice` l.2459, `QUIZ_POOL` l.2628, `startQuiz` l.2645, `confetti` l.2733, loupe) et `refs/aines/dans-mon-corps.html` (avatar `.who` l.146 et l.689, variables `--skin/--skin-shade/--hair` l.35, carnations `#skins` l.2309). Ces deux copies sont ignorées par git ; si elles manquent : `gh repo clone w3cdotorg/dans-le-volcan` et `w3cdotorg/dans-mon-corps`, copier leurs `index.html` dans `refs/aines/`.

## Global Constraints

- **Un seul fichier livrable : `index.html`** (HTML, CSS, JS en ligne, SVG à la main). Pas de build. Les tests sont dans `test/` et ne font pas partie du livrable.
- **Aucune dépendance**, aucune image bitmap, aucun appel réseau obligatoire : Google Fonts avec repli `"Fredoka","Chalkboard SE","Comic Sans MS",system-ui,sans-serif` ; l'iframe YouTube n'est créée **que sur appui** sur la télécommande, domaine `https://www.youtube-nocookie.com/embed/<id>?autoplay=1`.
- **Langue : français**, tutoiement, phrases courtes, vocabulaire et formulations de `docs/recherche-cerveau-sommeil.md` §5 ; interdit : « le cerveau se repose », « on va chasser le monstre », « ton cerveau s'est trompé ». Les hypothèses sont dites « beaucoup de chercheurs pensent que ».
- **Voix coupée par défaut** : `let soundOn = false;`, bouton `#sound` initial `aria-pressed="false"`, libellé `🔇 Son coupé`.
- **Anti-objectif de style** : rien du planétarium néon / verre dépoli des aînés ; les cartes d'interface sont des pièces de feutrine bombées à bord cousu.
- **L'ogre jamais en dernière image** : toute séquence de cauchemar enchaîne sur la télécommande, et la télécommande termine toujours sur le film transformé + la phrase-clé.
- **Budget de rendu** : ≤ 40 éléments avec `filter:url(#wool)` visibles simultanément par vue, lentille de loupe exclue ; les petits détails (yeux, nœuds, fils, vignettes de cartes) portent `#woolLite` ou rien. Version allégée (`html[data-lite="1"]`) : `#woolLite` partout.
- **`prefers-reduced-motion: reduce`** coupe toutes les animations décoratives (`*{animation:none!important;transition:none!important}`) et active la version allégée.
- **Accessibilité** : cibles ≥ 44 px, ←→ temps, ↑↓ vue, Tab/Entrée sur chaque zone (`tabindex="0"`, `role="button"`, `aria-label` = étiquette de `INFO`).
- **Paramètres d'URL de test** (lus au chargement, Task 1) : `?vue=0..2&temps=0..4&theme=feutrine|riso&lite=1&cartes=pouce,ogre,copains` — chaque tâche s'en sert pour ses captures.
- **Vérification de chaque tâche** : `node --test test/` (quand un test existe) + ouverture de la page : Playwright MCP (`browser_navigate` sur `file:///Users/willow/Sites/dans-les-reves/index.html?…`, `browser_console_messages` **zéro erreur**, `browser_take_screenshot`) ou, à défaut, `test/shot.sh "<query>" <sortie.png>` puis lecture de l'image.
- **Commit à la fin de chaque tâche**, message en français, suffixé `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. **`NOTES.md`** reçoit une entrée à chaque décision ou découverte (réglage qui a raté, astuce), pas seulement à la fin.
- Clés `localStorage` (préfixe `reves.`) : `theme`, `lite`, `son`, `prenom`, `chanson` (JSON `{titre, ytid}`), `reconfort` (`chanson|doudou|calin`), `avatar` (JSON `{genre, skin, hair}`).
- Palette feutrine (variables dans `:root`) :
  ```css
  --toile:#e8ddc7; --toile-trame:#d8cbb0;
  --p-peau:#f1c19c; --p-peau-ombre:#c98e66; --p-cheveux:#4a2c1a;
  --p-cerveau:#ec8aa2; --p-cerveau-sombre:#d4657f; --p-cervelet:#c96a84; --p-tronc:#b9607a;
  --p-hippocampe:#f6c04f; --p-amygdale:#e0493f; --p-thalamus:#9fb8e6; --p-pineale:#b48be0;
  --p-ecran:#fbf3e0; --p-carte:#fbf3e0; --p-pouce:#b9b2a0; --p-soleil:#f3c74a; --p-lune:#fff1c9;
  --fil-blanc:#fff6f1; --fil-brun:#7a4b3a; --fil-sable:#c9b58d; --fil-rouge:#e0493f;
  --nuit-1:#8d8cae; --nuit-2:#3f3f74; --nuit-3:#262a58;
  ```
  Palette riso : `--ink-jaune:#ffe14a; --ink-rose:#ff4fa8; --ink-bleu:#0f6fb8; --papier:#f7f2e8`.
- Coordonnées SVG communes (toutes vues) : tête de profil **regardant vers la droite**, occupant x 150–520 / y 40–540 ; boîte de cerveau x 200–470 / y 90–320 (avant = droite) ; œil `(455,190)` ; conduit auditif `(300,250)` ; bout du nez `(505,250)` ; bouche `(480,300)` ; cou x 300–420 sous y 440. Écran du rêve : nuage-écran centré `(700,170)`, ~300 × 200. Boîte à souvenirs : bande y 470–550, cartes 58 × 70 espacées de 66 à partir de x 60.
- Positions anatomiques (recherche §2.8, en coordonnées scène ; à ajuster de ±10 px, pas plus) : sillon central oblique du sommet `(330,95)` vers `(380,210)` ; sillon latéral quasi horizontal de `(420,235)` vers `(260,215)` ; lobe temporal sous le sillon latéral, pointe vers l'avant `(430,250)` ; amygdale (amande) `(357,246)` ; hippocampe (hippocampe de mer couché) de `(346,242)` à `(300,223)`, montant vers l'arrière ; thalamus (ovale) `(335,200)` ; hypothalamus `(345,222)` ; chiasma optique `(365,232)` ; hypophyse `(368,246)` ; glande pinéale `(300,195)` derrière le thalamus ; corps calleux : arc épais au-dessus du thalamus de `(250,185)` à `(420,175)` ; cervelet strié `(240,290)` rayon ~40, **séparé** ; tronc de `(320,250)` à `(330,330)`, pont bombé vers l'avant, puis moelle dans le cou ; nerf optique de l'œil `(455,190)` **vers l'arrière et le centre** jusqu'au chiasma.

## Review Focus

1. **Journée vide puis nuit** : aucune carte choisie et le curseur passe la nuit des rêves → pas d'erreur, écran « tout flou » et phrase honnête (test dans Task 10).
2. **Une seule carte apaisante** (ex. « ma chanson » seule) → rêve calme, verdict `beau`, jamais `finitBien` ni `cauchemar` (test Task 10).
3. **Télécommande hors ligne** : `navigator.onLine === false` ou iframe en erreur → pièce « Chante ta chanson ! » avec le titre saisi, aucun appel réseau, aucune erreur console (test Task 11).
4. **Changement de thème ou de version allégée en plein rêve** : le rêve composé reste affiché, la phrase et les fils restent lisibles (test Task 18, captures `?theme=riso&temps=3&cartes=pouce,ogre`).
5. **Clavier seul** : ←→ ↑↓ changent les curseurs, Tab atteint toutes les zones de la vue active et Entrée ouvre la carte info ; les zones des vues inactives ne sont pas tabulables (test Task 12).

---

### Task 1 : Squelette de la page, toile, deux thèmes, paramètres d'URL

**Files:**
- Create: `index.html`, `test/shot.sh`, `.gitignore` (ajouter `shots/`)

**Interfaces:**
- Produces : `<html data-theme="feutrine">` (ou `riso`), `data-lite="1"` optionnel ; `header` ; `.wrap` grille 2 colonnes (`<main class="scene">` : `<svg id="scene" viewBox="0 0 900 560">` + curseur `#time` (`range 0..400`) avec 5 `.moment[data-time=0..4]` (☀️ La journée, 🌇 Le soir, 💤 La nuit profonde, 🌙 La nuit des rêves, 🐓 Le matin) ; `<aside class="panel">` : 3 `.pill[data-cut=0..2]` (🏞️ Dehors, 🧠 Dedans, 🔬 Tout près) + `#cut` (`range 0..200`), carte info `#info` (`#infoEmoji`, `#infoTitle`, `#infoText`), barre de boutons `#say` 🔊 Réécouter, `#sound` 🔇 Son coupé, `#zones` ✨ Montrer les zones, `#loupeBtn` 🔍 La loupe, `#jeu1` 🎯 Trouve la partie, `#jeu2` 💭 Rêve ou pour de vrai ?, `#histoire` 📖 L'histoire du pouce, `#journee` 🌅 Nouvelle journée, `#theme` 🧶/🖨️, `#parents` 👪 Pour les parents).
- Dans `<defs>` de `#scene` : filtres `#wool`, `#woolLite` (découpe + ombre portée seulement : les primitives A, B, F de `#wool`), `#thread`, `#riso`, `#paperGrain`, motifs `#linen`, `#knot`, dégradés `#dusk`, `#steel`, `#glassRed/Blue/Yellow`, symbole `#pin` — **recopiés de la maquette v10** (le `#pin` prend sa couleur de tête via `fill="currentColor"` sur le cercle `.pinhead`, et l'usage fait `<use href="#pin" style="color:var(--glass-red)">`).
- Groupes vides dans l'ordre : `#g-toile` (rect lin + rect grain + rect `.nuit` `fill="url(#dusk)"` `mix-blend-mode:multiply` `opacity="0"`), `#g-dehors`, `#g-dedans`, `#g-pres`, `#g-ecran`, `#g-boite`, `#g-hs` (zones cliquables), `#g-ui`.
- JS : `const Q = new URLSearchParams(location.search)` ; `setTheme(name)` (`'feutrine'|'riso'`, écrit `data-theme` + `localStorage reves.theme`) ; `setLite(on)` ; `prefs = {get(k, def), set(k, v)}` (JSON, préfixe `reves.`). Détection auto : au premier `requestAnimationFrame` après chargement, si `performance.now()` du premier rendu complet > 120 ms **ou** `matchMedia('(prefers-reduced-motion: reduce)').matches` → `setLite(true)` sauf si `reves.lite` est explicitement `false`.
- Règle de thème en CSS : `.w{fill:var(--p)}` où chaque pièce déclare `style="--p:var(--p-peau)"` et `data-ink="jaune|rose|bleu"` ; `[data-theme=feutrine] .w{filter:url(#wool)}` ; `[data-theme=feutrine] .w.lite, [data-lite="1"] .w{filter:url(#woolLite)}` ; `[data-theme=riso] .w{filter:url(#riso)}` + `[data-theme=riso] .w[data-ink=jaune]{fill:var(--ink-jaune);transform:translate(-1.6px,1.1px)}` (rose `(1.5px,-1.3px)`, bleu `(.6px,.4px)`) et `[data-theme=riso] #scene>g{mix-blend-mode:multiply}` ; contours `.fil` : feutrine → `stroke-dasharray:2.6 1;filter:url(#thread)` ; riso → `stroke:var(--ink-bleu);stroke-dasharray:none;filter:url(#riso)`.

- [ ] **Step 1 : Écrire `index.html`** — `<head>` (charset, viewport, `<title>Dans les rêves — petit explorateur du cerveau et des rêves</title>`, description, fonts), CSS (palettes du Global Constraints, toile de lin en fond de `body` via le même motif que `#linen` reproduit en CSS `repeating-linear-gradient`, cartes d'interface `.card` = fond `var(--p-carte)` + `border:2px dashed var(--fil-sable)` + `border-radius:22px` + ombre portée douce, boutons `.btn` ronds bombés en feutrine, curseurs à gros pouce ≥ 38 px, `h1` Fredoka « Dans les rêves 🌙 », tagline « Mets ta journée dans ta tête, et regarde ce que ton cerveau en fait la nuit ! », `@media (max-width:900px)` → 1 colonne, `@media (prefers-reduced-motion:reduce)` → tout coupé), SVG avec les `<defs>` et les groupes vides (un rectangle de test `.w` dans `#g-dedans` pour vérifier le filtre, à retirer en Task 3), JS des préférences / thème / allégé / paramètres d'URL, bouton `#theme` qui bascule et met à jour son libellé (`🧶 Feutrine` / `🖨️ Riso`).
- [ ] **Step 2 : Écrire `test/shot.sh`** — `#!/bin/bash` : `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1400,1000 --screenshot="$2" "file://$PWD/index.html?$1"` ; `chmod +x`.
- [ ] **Step 3 : Vérifier** — `test/shot.sh "theme=feutrine" shots/t1-feutrine.png` et `test/shot.sh "theme=riso" shots/t1-riso.png`, lire les deux images : toile de lin, layout 2 colonnes, cartes en feutrine (pas de verre dépoli), rectangle de test en laine bombée / en encre riso, boutons lisibles. Console propre (Playwright ou `--enable-logging=stderr`).
- [ ] **Step 4 : Commit** — `git add index.html test/shot.sh .gitignore && git commit -m "Squelette : toile, deux thèmes, paramètres d'URL"`.

### Task 2 : Données et fonctions pures (cartes, textes, accord de genre) + harnais de test Node

**Files:**
- Modify: `index.html` (bloc `<script>` `/* PURE-BEGIN */ … /* PURE-END */`, avant le reste du JS)
- Create: `test/_load.js`, `test/data.test.js`

**Interfaces:**
- Produces (globaux du bloc pur) :
  - `const CARTES = [{slug, nom, emoji, cat:'vu'|'mot'|'gens'|'ressenti'|'reconfort', charge:3|2|1|0|-2, entree:'oeil'|'oreille', base:boolean, greffe:{nom:string, forme:string}|null, texte:string}]` — les 22 cartes du spec §4.3 : `pouce` (le pouce géant, vu, 0, base, greffe `{nom:'un pouce géant', forme:'pouce'}`), `glace`, `chien`, `velo`, `piscine`, `gateau`, `tracteur`, `orage` (3), `manege`, `ogre` (mot, 3, base:false, greffe `{nom:'un ogre', forme:'ogre'}`), `pirate` (mot, 1), `dragon` (mot, 3), `anniversaire` (mot, 1), `copains` (gens, 1), `parents` (gens, 1), `mamie` (gens, 1), `maitresse` (gens, 1), `ri` (ressenti, 1, base:false), `peur` (ressenti, 3, base:false), `fache` (ressenti, 2, base:false), `calin` (ressenti, 1), `chanson` (reconfort, −2, base:false), `doudou` (reconfort, −2, base:true). Les `texte` sont les deux phrases lues quand on touche la carte.
  - `const MODIFS = {gigantesque:{nom:'gigantesque'}, envers:{nom:'à l\'envers'}, desobeit:{nom:'qui n\'obéit pas'}, multiplie:{nom:'multiplié'}, minuscule:{nom:'tout petit'}, couleur:{nom:'d\'une autre couleur'}}`.
  - `const INFO = { <idZone>: {emoji, titre, texte, vue:0|1|2} }` — les ≈ 32 zones du spec §5, ids : `cortex, frontal, occipital, temporal, parietal, hippocampe, amygdale, thalamus, horloge, pineale, calleux, cervelet, tronc, moelle, nerf-optique, oeil, oreille, crane, liquide` (vue 1) ; `soleil, lune, lampe, lit, doudou, fenetre, expo, boite, ecran` (vue 0) + une entrée par carte `vu`/`gens` (`decor-<slug>`) ; `neurone, synapse, vague, fuseau, cellule` (vue 2).
  - `const JEU_PARTIES` (8 questions `{q, cible:<idZone>}`) et `const JEU_REVE` (8 `{q, emoji, reponse:'vrai'|'reve'}`, dont « un pouce de 12 mètres » → `vrai`, « un ogre gigantesque » → `reve`).
  - `const HISTOIRE = [{vue, temps, texte}]` — les étapes du mode guidé, textes avec marqueurs `{il|elle}` `{terrorisé|terrorisée}` `{PRENOM}`.
  - `const TRANSFOS = [{id:'bronze', texte:…}, {id:'lapin', …}, {id:'danse', …}]` (télécommande, §4.6).
  - `const PHRASES = { reve: 'Dans le rêve, {BASE} est devenu {GREFFE} {MODIF}, parce que ton cerveau a mélangé {C1} avec {C2}. Le chef qui vérifie dormait, alors personne n\'a dit « mais non, c\'est {VRAI} ! »', seul: 'Dans le rêve, {BASE} était {MODIF}, parce que ton cerveau l\'a rejoué.', flou: 'Tu n\'as rien mis dans ta journée : cette nuit, ton cerveau range et se rince, et le rêve est tout flou.', finitBien: '… mais {RECONFORT} était dans ta tête, alors le film a changé tout seul.', cle: 'C\'est mon cerveau qui a mélangé. C\'est un rêve. Je change de chaîne.' }`.
  - `function inflect(str, genre)` → remplace chaque `{a|b}` par `a` si `genre==='garcon'`, `b` si `'fille'`.
  - `function lerpArr(arr, t)` (copie du volcan l.2151).
- `test/_load.js` : `module.exports = function load(){ const src = fs.readFileSync('index.html','utf8'); const m = src.match(/\/\* PURE-BEGIN \*\/([\s\S]*?)\/\* PURE-END \*\//); const ctx = {}; vm.runInNewContext(m[1] + ';this.__x = {CARTES, MODIFS, INFO, JEU_PARTIES, JEU_REVE, HISTOIRE, TRANSFOS, PHRASES, inflect, lerpArr, composeDream: typeof composeDream==="function"?composeDream:null}', ctx); return ctx.__x; }`.

- [ ] **Step 1 : Écrire `test/data.test.js`** (`node:test`, `node:assert/strict`) : `CARTES.length === 22` ; chaque carte a `slug` unique, `charge ∈ {3,2,1,0,-2}`, `cat` valide, `entree` valide, `texte` de 2 phrases (≥ 2 points) ; toute carte `cat:'ressenti'` a `base === false` ; toute carte avec `base:true` ou `greffe` a un `greffe.forme` ; `Object.keys(INFO).length >= 32` et chaque entrée a `emoji, titre, texte, vue` ; `JEU_PARTIES.length === 8` avec chaque `cible` dans `INFO` ; `JEU_REVE.length === 8` ; `HISTOIRE.length >= 8` ; `inflect('{il|elle} est {terrorisé|terrorisée}','fille') === 'elle est terrorisée'` ; `lerpArr([0,1,0,0,0], 0.5) === 0.5`.
- [ ] **Step 2 : Lancer** `node --test test/` → échec (bloc PURE absent).
- [ ] **Step 3 : Écrire le bloc PURE** dans `index.html` avec toutes les données (textes complets, deux phrases par zone et par carte, vocabulaire de la recherche §5).
- [ ] **Step 4 : Lancer** `node --test test/` → tout passe.
- [ ] **Step 5 : Commit** — `git commit -m "Données : cartes, zones, jeux, histoire, phrases ; tests Node"`.

### Task 3 : Vue « Dedans » — la tête, l'avatar, le cerveau à sa vraie place

**Files:**
- Modify: `index.html` (`#g-dedans`, CSS avatar, JS avatar)

**Interfaces:**
- Produces : dans `#g-dedans`, pièces `.w` avec ids : `#p-tete` (peau), `#p-cheveux`, `#p-oreille`, `#p-cortex` (le grand cerveau, avec `#p-frontal #p-parietal #p-occipital #p-temporal` en sous-pièces légèrement différenciées de teinte via `--p` dérivés), `#p-cervelet` (strié : 5 traits brodés horizontaux), `#p-tronc`, `#p-moelle`, `#p-calleux`, `#p-thalamus`, `#p-hypothalamus`, `#p-pineale`, `#p-hypophyse`, `#p-hippocampe` et `#p-amygdale` (dessinés **en transparence** : `opacity:.85` + bord cousu plus marqué), `#p-nerf-optique`, `#p-oeil` (bouton à deux trous, `#p-paupiere` par-dessus, fermée la nuit), `#p-crane` (liseré d'os brodé), broderie des sillons `#fil-sillons` (volutes blanches au point de tige + 6 nœuds `#knot`). Classes d'avatar : `.peau` (`fill:var(--skin)`), `.cheveux` (`fill:var(--hair)`) ; `#p-cheveux-long` visible si `genre==='fille'`.
- `.who` (commande visible au-dessus de la scène, comme le corps) : 2 boutons 👦/👧 `data-genre`, 5 pastilles `#skins` (valeurs `--skin/--skin-shade` du corps), 6 pastilles `#hairs` ; `setAvatar({genre, skin, hair})` écrit les variables, `data-genre` sur `<html>`, et `prefs.set('avatar', …)`.

- [ ] **Step 1 : Dessiner** la tête et le cerveau en respectant les coordonnées et positions anatomiques du Global Constraints (vérifier : amygdale **devant** l'hippocampe, pinéale derrière le thalamus, cervelet séparé et strié, nerf optique vers l'arrière). Chaque région est une pièce `.w` séparée ; les petites (pinéale, hypophyse, amygdale) sont `.w.lite`. Retirer le rectangle de test de Task 1.
- [ ] **Step 2 : Avatar** — HTML `.who`, JS `setAvatar`, lecture de `reves.avatar` au chargement.
- [ ] **Step 3 : Vérifier** — `test/shot.sh "vue=1" shots/t3-garcon.png` puis, via Playwright `browser_evaluate` `setAvatar({genre:'fille',skin:3,hair:5})` + capture ; lire les images : tête de profil regardant à droite, laine bombée, cerveau lisible, régions profondes visibles en transparence à hauteur de l'oreille, compte des `.w` ≤ 40 (`document.querySelectorAll('#g-dedans .w:not(.lite)').length`). Console propre.
- [ ] **Step 4 : Commit** — `git commit -m "Vue Dedans : tête, avatar, cerveau anatomique en laine"`.

### Task 4 : Vue « Dehors » — le monde de jour et de nuit, emplacements des cartes

**Files:**
- Modify: `index.html` (`#g-dehors`)

**Interfaces:**
- Produces : `#g-dehors` contient `#p-ciel-soleil`, `#p-ciel-lune` (+ étoiles = nœuds `#knot` dans `#g-etoiles`), `#p-sol`, `#p-expo` (le bâtiment de l'expo, pièce grise à fenêtres cousues), `#p-fenetre`, `#p-lit`, `#p-lampe`, `#p-doudou`, et la **tête de l'enfant de profil réutilisée** par `<use href="#p-tete">` + cheveux + œil (la même pièce que Dedans, sans cerveau : `#g-dehors` masque le cerveau par ordre de dessin). **Emplacements de décor** : 4 groupes vides `#slot-0..3` aux positions `(600,330)`, `(700,300)`, `(780,350)`, `(640,420)` où Task 8 insère la forme de décor des cartes choisies (`#d-<slug>`), les cartes `gens` à gauche de l'enfant `(120,380)`.
- Éléments de nuit (`#p-lit`, `#p-lampe`, `#p-lune`, `#g-etoiles`, `#p-doudou`) ont `data-nuit="1"` ; éléments de jour (`#p-ciel-soleil`, `#p-expo`) `data-jour="1"` — Task 7 pilote leur opacité.

- [ ] **Step 1 : Dessiner** la scène fixe de jour et de nuit (le lit est dans le même décor, l'enfant s'y couche par une simple translation + rotation de la tête en Task 7 — prévoir `#g-enfant-dehors` avec `transform-origin` au cou).
- [ ] **Step 2 : Vérifier** — `test/shot.sh "vue=0" shots/t4-jour.png` (temporairement `#g-dedans{opacity:0}` si Task 6 n'existe pas encore : retirer avant commit) ; lire : décor lisible, slots vides sans trou visible. Console propre.
- [ ] **Step 3 : Commit** — `git commit -m "Vue Dehors : décor fixe de jour et de nuit, emplacements des cartes"`.

### Task 5 : Vue « Tout près » — neurones, vagues, rafales, rinçage, cellule

**Files:**
- Modify: `index.html` (`#g-pres`)

**Interfaces:**
- Produces : `#g-pres` = fond laine rose pâle plein cadre, 7 neurones (`#p-neurone-1..7`, corps en laine + dendrites brodées), étincelles `#g-synapses` (nœuds jaunes qui clignotent), `#g-vagues` (3 larges bandes brodées bleu pâle qui glissent de gauche à droite), `#g-fuseaux` (rafales de petits traits blancs), `#g-rincage` (gouttes bleu pâle), `#p-cellule` (une cellule qui grandit, anneau pulsant). Ces groupes ont des `data-phase` que Task 7 active : `synapses` (jour et rêves), `vagues` + `fuseaux` + `rincage` + `cellule` (nuit profonde).

- [ ] **Step 1 : Dessiner** (pièces ≤ 20, les neurones en `.w`, le reste en broderie).
- [ ] **Step 2 : Vérifier** — capture `vue=2`, lire. Console propre.
- [ ] **Step 3 : Commit** — `git commit -m "Vue Tout près : neurones et métiers de nuit"`.

### Task 6 : Curseur VUE — fondu entre les trois vues

**Files:**
- Modify: `index.html` (JS)

**Interfaces:**
- Produces : `setCut(c)` (c ∈ [0,2], clampé) — opacités `#g-dehors = 1-min(1,c)`, `#g-dedans = 1-|c-1|`, `#g-pres = max(0,c-1)` ; `document.body.dataset.vue = Math.round(c)` ; `.pill.active` ; `#cut` synchronisé ; `#g-ecran` et `#g-boite` visibles pour vues 0 et 1 (opacité `1-max(0,c-1)`) ; `pointer-events` : seule la vue arrondie reçoit les clics (classe `.active` sur le groupe). Clavier ↑↓ (pas 0.5, pastilles 1). Lecture de `?vue=` au chargement.

- [ ] **Step 1 : Implémenter** d'après le volcan l.2116-2150 (adapter les ids).
- [ ] **Step 2 : Vérifier** — captures `vue=0`, `vue=1`, `vue=2`, `vue=0.5` ; `browser_press_key ArrowDown` ; console propre.
- [ ] **Step 3 : Commit** — `git commit -m "Curseur vue : fondu Dehors / Dedans / Tout près"`.

### Task 7 : Curseur TEMPS — la journée interpolée sur les trois vues

**Files:**
- Modify: `index.html` (JS + CSS animations d'ambiance)

**Interfaces:**
- Produces : `setTime(t)` (t ∈ [0,4]) pilotant, via des tables `lerpArr` sur `[jour, soir, profonde, rêves, matin]` :
  - `#g-toile .nuit` opacité `[0, .55, 1, 1, .1]` ; `#p-ciel-soleil` `[1,.3,0,0,.8]` ; `data-nuit` `[0,.6,1,1,.2]` ; `#g-enfant-dehors` couché (`rotate(-80)` + translation vers le lit) `[0,.5,1,1,0]` ;
  - `#p-paupiere` fermée `[0,1,1,1,0]` ; `#p-pineale` lueur `[0,1,.6,.4,0]` (classe `.allume`) ; `#p-oeil` mouvements rapides (animation `rem`) actif `[0,0,0,1,0]` ; `#p-frontal` « zzz » (`#g-zzz`) `[0,0,1,1,0]` ; `#p-amygdale` lueur `[0,0,.3,1,0]` ;
  - `#g-vagues/#g-fuseaux/#g-rincage/#p-cellule` `[0,0,1,.2,0]` ; `#g-synapses` `[1,.5,.2,1,.8]` ;
  - `document.body.dataset.temps = Math.round(t)` ; `.moment.active` ; `#time` synchronisé ; clavier ←→ (pas 0.25, pastilles 1) ; lecture de `?temps=`.
  - Émet `document.dispatchEvent(new CustomEvent('temps', {detail:{t, phase:Math.round(t)}}))` à chaque changement de phase arrondie — Tasks 9, 10, 11 s'y abonnent.
- Animations d'ambiance (CSS, coupées par reduced-motion) : clignement de l'œil le jour, respiration de la tête (scale 1.01), frémissement des fils, scintillement des nœuds-étoiles la nuit, pulsation de l'amygdale en rêves, « zzz » qui montent.

- [ ] **Step 1 : Implémenter** d'après le volcan l.2151-2208.
- [ ] **Step 2 : Vérifier** — les 15 captures `vue=0..2 × temps=0..4` via une boucle shell sur `test/shot.sh`, lire au moins `vue=0&temps=0`, `vue=0&temps=3`, `vue=1&temps=2`, `vue=1&temps=3`, `vue=2&temps=2` : toile qui s'assombrit avec trame visible, contrastes OK la nuit, enfant couché, yeux fermés, pinéale allumée au soir. Console propre.
- [ ] **Step 3 : Commit** — `git commit -m "Curseur temps : la journée, le soir, les deux nuits, le matin"`.

### Task 8 : Les cartes-souvenirs — boîte, épingles, choix, entrée dans la tête

**Files:**
- Modify: `index.html` (`#g-boite`, `#g-cartes-assets` dans `<defs>`, JS)
- Create: `test/cartes.test.js`

**Interfaces:**
- Produces : dans `<defs>`, pour chaque carte de `CARTES` : `<symbol id="v-<slug>">` (vignette 40 × 40, laine `.w.lite`) et, si `base:true`, `<symbol id="d-<slug>">` (forme de décor Dehors, ~90 px). `#g-boite` : 22 cartes `.carte[data-slug]` (pièce crème 58 × 70 bord cousu `.fil` + `<use href="#v-slug">` + épingle `<use href="#pin">` à tête rouge/bleue/jaune en rotation), défilables horizontalement au doigt (`#g-boite` dans un `<svg>` enfant avec `overflow` ou translation par glisser : **au choix du constructeur**, mais le scroll ne doit pas capturer le glisser du curseur temps).
- JS : `let journee = []` (slugs, ≤ 4) ; `pickCard(slug)` : refuse si déjà présent ; si 4, retire `journee[0]` avec bulle « Oups, trop de choses ! » lue ; ajoute, anime la carte (transition de `transform` vers le slot Dehors `#slot-n`, insère `<use href="#d-slug">` ou, pour `gens`, à gauche) puis, en vue Dedans, duplique une petite vignette qui voyage œil→thalamus→hippocampe (`entree:'oeil'`) ou oreille→thalamus→hippocampe (`'oreille'`) en ~1,2 s et reste épinglée dans l'hippocampe (`#g-hippo-cartes`, 4 places) ; `resetDay()` (bouton `#journee`) ; lecture de `?cartes=a,b,c` au chargement (appelle `pickCard` pour chacune, sans animation) ; `document.dispatchEvent(new CustomEvent('journee', {detail: journee}))` à chaque changement.
- Si `t ≥ 2` (nuit) on ne peut plus piquer de carte : la boîte se grise et la bulle dit « Le cerveau dort, on choisira demain ! ».

- [ ] **Step 1 : Écrire `test/cartes.test.js`** : pour chaque carte, `index.html` contient `id="v-<slug>"` ; pour chaque carte `base:true`, contient `id="d-<slug>"`.
- [ ] **Step 2 : Lancer** → échec.
- [ ] **Step 3 : Dessiner** les 22 vignettes et les 13 formes de décor (le pouce de César : bronze, ongle, plis, **grand** : 12 m à l'échelle = 4 × la tête de l'enfant dans le slot `(700,300)` ; une glace, un chien, un vélo, une piscine, un gâteau, un tracteur, un orage, un manège, les copains (deux silhouettes), papa et maman, mamie, la maîtresse, le doudou), puis la boîte et le JS.
- [ ] **Step 4 : Lancer** `node --test test/` → passe. Captures `vue=0&cartes=pouce,ogre,copains,ri` et `vue=1&cartes=pouce,ogre,copains,ri` ; clic réel sur une 5ᵉ carte via Playwright → « Oups » ; lire les images : pouce géant dehors, vignettes épinglées dans l'hippocampe. Console propre.
- [ ] **Step 5 : Commit** — `git commit -m "Cartes-souvenirs : boîte, épingles, journée de 4 cartes, entrée dans la tête"`.

### Task 9 : Le rangement — nuit profonde

**Files:**
- Modify: `index.html` (JS, CSS)

**Interfaces:**
- Produces : à l'événement `temps` phase 2 : chaque vignette de `#g-hippo-cartes` glisse sur une vague vers `#g-cortex-cartes` (4 places réparties sur le cortex), avec une animation de « point de couture » (traits courts qui apparaissent autour) ; échelle finale `.55` si `charge === 0`, `1` sinon ; les cartes de charge non nulle reçoivent un fil `<line class="fil-amygdale">` vers `#p-amygdale`, couleur `--fil-rouge` (3), orange `#f28c28` (2), rose `#f4a3b8` (1), bleu doux `#9ad3f2` (−2). Retour en phase 0 ou `resetDay()` : tout revient dans l'hippocampe / la boîte. Étiquette brodée « je grandis » sur `#p-crane` visible en phase 2 (opacité pilotée par `setTime`).

- [ ] **Step 1 : Implémenter.**
- [ ] **Step 2 : Vérifier** — capture `vue=1&temps=2&cartes=pouce,ogre,copains,ri` : pouce et copains rangés petits ? Non : pouce (0) petit, copains (1) grand avec fil rose, ogre (3) grand avec fil rouge, « j'ai ri » (1) grand fil rose. Lire l'image. Console propre.
- [ ] **Step 3 : Commit** — `git commit -m "Nuit profonde : rangement des cartes dans le cortex, fils vers l'amygdale"`.

### Task 10 : Le générateur de rêve et l'écran

**Files:**
- Modify: `index.html` (bloc PURE : `composeDream` ; `<defs>` : `#g-base-<forme>` et `#g-greffe-<forme>` ; `#g-ecran` ; JS `renderDream`)
- Create: `test/reve.test.js`

**Interfaces:**
- Produces (pur) : `composeDream(slugs, opts={})` → `null` si `slugs.length===0` (l'appelant affiche `PHRASES.flou`) ; sinon `{greffe:carte|null, base:carte, contexte:carte|null, oublies:carte[], modif:cléDeMODIFS, verdict:'cauchemar'|'bizarre'|'beau'|'rigolo'|'finitBien', reconfort:carte|null, phrase:string}` selon le spec §4.5 : la greffe est la carte de |charge| max (ordre peur > colère > joie, ex æquo = dernière choisie), sauf si c'est une carte `reconfort` (alors elle devient `reconfort` et la greffe est la suivante) ; la base est la plus concrète des autres (`vu` > `gens` > `mot` > `ressenti`, ex æquo = dernière) parmi celles avec `base:true`, sinon la greffe est sa propre base si `base:true`, sinon la première carte `base:true` de la journée, sinon la carte seule est traitée comme « seul » avec sa vignette ; `contexte` = la plus concrète des restantes ; `modif` : charge 3 → `gigantesque`, 2 → `opts.seed%2 ? 'envers':'desobeit'`, 1 → `multiplie`, 0 → `opts.seed%2 ? 'minuscule':'couleur'` ; `verdict` : 3 → `cauchemar` (ou `finitBien` si `reconfort`), 2 → `bizarre`, 1 → `rigolo`, 0 → `beau` ; `phrase` = `PHRASES.reve` rempli (`{VRAI}` = « c'est une statue » pour le pouce, sinon « ce n'est pas pour de vrai »), ou `PHRASES.seul`, suivi de `PHRASES.finitBien` si `finitBien`. `opts.genre` passe à `inflect`.
- DOM : `#g-ecran` = nuage-écran `#p-ecran` (laine crème, épinglé en haut à droite par `#pin` jaune) + `#g-reve` (contenu) + `#t-phrase` (texte en `foreignObject` 3 lignes max, Baloo 2 ≥ 18 px) ; `renderDream(dream)` : vide `#g-reve`, insère `<use href="#g-base-<forme>">` puis `<use href="#g-greffe-<forme>">` puis, en petit derrière, `#d-<contexte>` ; applique la classe `.m-<modif>` (CSS : `gigantesque` → `scale(2.2)` débordant via `clip-path` de l'écran, le contexte passe à `opacity:0` ; `multiplie` → 3 `<use>` décalés ; `envers` → `scale(1,-1)` ; `desobeit` → animation de secousse ; `minuscule` → `scale(.4)` ; `couleur` → `filter:hue-rotate(140deg)`) ; verdict : `document.body.dataset.verdict`, CSS : `cauchemar` → `.nuit` plus profonde (`--nuit-3` → `#141533`), `#p-amygdale.pulse`, sourcils `#p-sourcil` froncés, `#g-ecran` animation `tremble` ; `bizarre` → amygdale orange ; `beau`/`rigolo` → écran teinté `#fff3c4`, sourire. Déclenchement : à l'événement `temps` phase 3, `renderDream(composeDream(journee, {seed, genre}))` ; bouton `#encore` (🔁 Encore un rêve, dans l'écran) incrémente `seed`. Hors phase 3-4 : `#g-reve` vide, phrase vide.
- `speak(phrase)` est appelée par `renderDream` (Task 13 fournit `speak`; d'ici là, `window.speak = window.speak || (()=>{})`).

- [ ] **Step 1 : Écrire `test/reve.test.js`** : `composeDream([]) === null` ; `composeDream(['pouce','ogre','copains','ri'])` → `greffe.slug==='ogre'`, `base.slug==='pouce'`, `contexte.slug==='copains'`, `modif==='gigantesque'`, `verdict==='cauchemar'`, `phrase` contient « le pouce géant est devenu un ogre gigantesque » et « mélangé le pouce géant avec le mot « ogre » » et « c'est une statue » ; `composeDream(['glace','chien'])` → `verdict==='beau'`, `modif ∈ {minuscule, couleur}`, base `chien` (dernière choisie à égalité) ; `composeDream(['copains','pirate'])` → `modif==='multiplie'`, `verdict==='rigolo'` ; `composeDream(['pouce','ogre','chanson'])` → `verdict==='finitBien'`, `reconfort.slug==='chanson'`, phrase se termine par `PHRASES.finitBien` rempli ; `composeDream(['chanson'])` → `verdict==='beau'` (Review Focus 2) ; `composeDream(['ri'])` (ressenti seul, sans base) → `base` non nulle et `phrase` = modèle `seul` ; `composeDream(['fache','velo'])` → `verdict==='bizarre'` ; **toutes les paires** de `CARTES` (231) → résultat non nul, `phrase.length > 40`, `base.greffe||base.base` défini ; `inflect` appliqué : `composeDream(['peur','lit'] …)` n'est pas requis, mais `opts.genre:'fille'` ne laisse aucun `{` dans `phrase` sur toutes les paires.
- [ ] **Step 2 : Lancer** → échec.
- [ ] **Step 3 : Implémenter `composeDream`** dans le bloc PURE.
- [ ] **Step 4 : Lancer** `node --test test/` → passe.
- [ ] **Step 5 : Dessiner** les bases (`#g-base-pouce, glace, chien, velo, piscine, gateau, tracteur, orage, manege, copains, parents, mamie, maitresse, doudou, calin`) et les greffes (`#g-greffe-ogre` yeux + dents + sourcils, `pirate` chapeau + sabre, `dragon` ailes + feu, `glace` cornet + gouttes, `chien` queue + oreilles, `anniversaire` guirlande + bougies, `orage` éclairs, `pouce` ongle géant, `copains` deux têtes, `ri` grand sourire, `peur` grands yeux, `fache` sourcils, `calin` deux bras, `chanson` notes, `doudou` oreilles de doudou, `velo/piscine/gateau/tracteur/manege/parents/mamie/maitresse` un attribut simple chacun) ; l'écran, `renderDream`, les effets de verdict.
- [ ] **Step 6 : Vérifier** — captures `vue=1&temps=3&cartes=pouce,ogre,copains,ri` (ogre gigantesque, amygdale rouge, phrase lisible, télécommande absente pour l'instant), `vue=1&temps=3&cartes=glace,chien`, `vue=1&temps=3` sans cartes (écran flou + phrase `flou`, **aucune erreur console** — Review Focus 1), `theme=riso&vue=1&temps=3&cartes=pouce,ogre`. Lire les images.
- [ ] **Step 7 : Commit** — `git commit -m "Le rêve : générateur pur testé sur toutes les paires, écran, verdicts"`.

### Task 11 : La télécommande — changer de chaîne

**Files:**
- Modify: `index.html` (`#g-ui` : `#telecommande` en SVG ; `#chanson` carte HTML ; JS)
- Create: `test/telecommande.test.js`

**Interfaces:**
- Produces : `#telecommande` (pièce de feutrine grise 70 × 130 à 4 boutons-pressions, posée en bas à droite de la scène, visible aux phases 3-4, classe `.pulse` tant que `verdict==='cauchemar'` et non utilisée) ; `applyRemote()` : 1) ajoute la carte réconfort (`prefs.get('reconfort','chanson')`) dans un emplacement à part de l'écran (`#g-reconfort`), 2) applique `TRANSFOS[compteur % 3]` : `bronze` (la base rétrécit vers `scale(1)`, la greffe s'efface, la base reprend la couleur `--p-pouce`), `lapin` (greffe `#g-greffe-lapin` ajoutée, modif retiré), `danse` (greffe `#g-greffe-chiens-pirates` : deux chiens à chapeau, animation de balancement) — toujours avec retrait du verdict `cauchemar` → `body.dataset.verdict='finitBien'`, 3) lance la chanson : `openSong()` crée la carte `#chanson` (pièce de feutrine à fenêtre cousue, bouton ✖) contenant, si `navigator.onLine`, un `<iframe src="https://www.youtube-nocookie.com/embed/<ytid>?autoplay=1" allow="autoplay; encrypted-media">` (`ytid` de `prefs.get('chanson')`, défaut `jqGPppvVmBc`, titre « Hey, ho, les chiens pirates ! ») ; sinon ou si `iframe.onerror` ou si l'iframe n'a pas chargé en 4 s (`load` non reçu) : le contenu devient « 🎵 Chante ta chanson ! » + titre ; 4) affiche et lit `PHRASES.cle` en gros dans l'écran (`#t-cle`). Au matin (phase 4) la télécommande reste et son libellé devient « Tu veux lui changer sa tête ? ». `finitBien` automatique (Task 10) déclenche les étapes 1, 2 et 4 sans ouvrir la chanson.
- Pur : `function remoteStep(n)` → `TRANSFOS[n % TRANSFOS.length].id` (dans le bloc PURE, pour le test).

- [ ] **Step 1 : Écrire `test/telecommande.test.js`** : `TRANSFOS.map(t=>t.id)` = `['bronze','lapin','danse']` ; `remoteStep(0)==='bronze'`, `remoteStep(4)==='lapin'` ; `PHRASES.cle` = « C'est mon cerveau qui a mélangé. C'est un rêve. Je change de chaîne. » ; aucun texte de `TRANSFOS` ne contient « chass » ni « vainc » ni « tué ».
- [ ] **Step 2 : Lancer** → échec ; **Step 3 : Implémenter** ; **Step 4 : Lancer** → passe.
- [ ] **Step 5 : Vérifier** — Playwright : `?vue=1&temps=3&cartes=pouce,ogre,copains`, clic `#telecommande` → capture (ogre redevenu pouce de bronze, chiens pirates ou oreilles de lapin selon le compteur, phrase-clé, carte chanson ouverte avec iframe) ; `browser_evaluate` `Object.defineProperty(navigator,'onLine',{get:()=>false})` puis clic → carte « Chante ta chanson ! », `browser_network_requests` ne montre aucune requête YouTube (Review Focus 3) ; console propre dans les deux cas.
- [ ] **Step 6 : Commit** — `git commit -m "Télécommande : carte réconfort, trois transformations, chanson, phrase-clé"`.

### Task 12 : Zones cliquables, carte info, « Montrer les zones », cohérence

**Files:**
- Modify: `index.html` (`#g-hs`, JS `showInfo`)
- Create: `test/zones.test.js`

**Interfaces:**
- Produces : dans `#g-hs`, une forme transparente `.hs[data-id=<idZone>]` par entrée de `INFO` (sans filtre, `fill:rgba(255,255,255,.001)`, `tabindex="0"`, `role="button"`, `aria-label` = `INFO[id].titre`), regroupées par vue `#hs-0/#hs-1/#hs-2` ; seules les zones du groupe de la vue active sont `pointer-events:auto` et `tabindex="0"` (les autres `tabindex="-1"`). Les zones `decor-<slug>` n'existent que si la carte est dans `journee` (créées/retirées par `pickCard`/`resetDay`). `showInfo(id)` : remplit `#info`, pose `.sel` sur la zone, affiche une étiquette flottante `#label` près du pointeur, appelle `speak(titre + '. ' + texte)`. Bouton `#zones` : classe `hint` sur `#scene` → pulsation des `.hs` de la vue active 6 s. Survol (`@media (hover:hover)`) : liseré brodé.
- Boucle de cohérence (console, au chargement) : `Object.keys(INFO).filter(id => !document.querySelector('.hs[data-id="'+id+'"]') && !id.startsWith('decor-'))` doit renvoyer `[]`.

- [ ] **Step 1 : Écrire `test/zones.test.js`** : pour chaque `id` de `INFO` non `decor-`, `index.html` contient `data-id="<id>"` ; chaque `.hs` a `role="button"` et `tabindex`.
- [ ] **Step 2 : Lancer** → échec ; **Step 3 : Implémenter** (d'après le volcan l.2209-2360) ; **Step 4 : Lancer** → passe.
- [ ] **Step 5 : Vérifier** — Playwright : clic sur l'amygdale (`vue=1`) → carte info remplie + capture ; `#zones` → pulsation ; clavier : Tab × n puis Entrée ouvre une zone, et `document.activeElement` ne tombe jamais sur une zone d'une vue inactive (Review Focus 5) ; `browser_evaluate` de la boucle de cohérence → `[]`. Console propre.
- [ ] **Step 6 : Commit** — `git commit -m "Zones cliquables : 32 zones, carte info, montrer les zones, clavier"`.

### Task 13 : Synthèse vocale (coupée par défaut)

**Files:**
- Modify: `index.html` (JS)

**Interfaces:**
- Produces : `speak(text)` (annule la file : `speechSynthesis.cancel()` avant chaque énoncé ; voix choisie par `pickVoice()` copiée du volcan l.2459-2470 ; `lang='fr-FR'`, `rate=.92`) ; `soundOn` persisté dans `reves.son` (défaut `false`) ; `#sound` bascule libellé `🔇 Son coupé` / `🎧 Son allumé` et `aria-pressed` ; `#say` relit le dernier texte ; quand `soundOn` est faux, `speak` ne fait rien mais mémorise le texte.

- [ ] **Step 1 : Implémenter.** **Step 2 : Vérifier** — Playwright : au chargement `#sound` a `aria-pressed="false"` ; clic → `true` ; clic sur une zone → `speechSynthesis.speaking` passe à `true` (si une voix existe en headless, sinon vérifier que `speak` a été appelé via un compteur `window.__spoken`). Console propre.
- [ ] **Step 3 : Commit** — `git commit -m "Voix : synthèse française coupée par défaut"`.

### Task 14 : La loupe

**Files:**
- Modify: `index.html` (`#lens`, JS)

**Interfaces:**
- Produces : `#loupeBtn` bascule `loupeOn` ; `#lens` = `<div>` rond 160 px contenant un `<svg viewBox>` qui clone la scène par `<use href="#scene-inner">` (les groupes de scène sont enveloppés dans `<g id="scene-inner">` en Task 1 — sinon le faire ici), grossissement × 2.4, suivi du pointeur cadencé par `requestAnimationFrame` (volcan, commit « Loupe : cadence le suivi … »). Pendant `loupeOn` : `html[data-loupe="1"]` → CSS coupe les animations d'ambiance (`.ambiance{animation-play-state:paused}`) ; en `data-lite="1"` la lentille utilise `#woolLite` (hérité).

- [ ] **Step 1 : Implémenter** d'après le volcan. **Step 2 : Vérifier** — capture avec loupe active sur le cerveau (`browser_evaluate` d'un `pointermove`) : laine complète visible en gros, cohérente avec vue et temps ; les animations sont en pause (`getComputedStyle(...).animationPlayState==='paused'`). Console propre.
- [ ] **Step 3 : Commit** — `git commit -m "Loupe : laine de près, animations en pause"`.

### Task 15 : Le mode guidé « L'histoire du pouce »

**Files:**
- Modify: `index.html` (JS, `#recit` carte HTML)

**Interfaces:**
- Produces : `startStory()` (bouton `#histoire`) : `resetDay()`, `pickCard` × `['pouce','ogre','copains','ri']` sans animation, `setCut(0)`, `setTime(0)`, affiche la carte `#recit` (pièce de feutrine avec le texte de l'étape, bouton `#suite` « Et après ? », bouton `#stop` ✖) ; chaque étape de `HISTOIRE` règle `vue`/`temps` (par `setCut`/`setTime` animés sur 600 ms) puis affiche et lit `inflect(texte.replace('{PRENOM}', prenom||'{il|elle}'), genre)` ; les étapes couvrent : l'expo et le pouce, « pouce d'ogre », l'entrée dans la tête, le soir et la chanson, le rangement, le rêve (appelle `renderDream` avec `seed:0`), le réveil terrorisé, la télécommande (`applyRemote()` avec `openSong`), le matin (« Le lendemain, {il|elle} a raconté l'ogre gigantesque. Et maintenant, {il|elle} sait d'où il venait. »), puis « À toi de faire ta journée ! » qui ferme `#recit` et `resetDay()`. Pas d'auto-défilement.

- [ ] **Step 1 : Implémenter.** **Step 2 : Vérifier** — Playwright : clic `#histoire`, puis `#suite` jusqu'à la fin en capturant les étapes 1, 6 (rêve), 8 (télécommande), 10 ; `prefs.set('prenom','Raphaël')` + avatar fille → les textes s'accordent et nomment. Console propre.
- [ ] **Step 3 : Commit** — `git commit -m "Mode guidé : l'histoire du pouce, étape par étape"`.

### Task 16 : Les deux mini-jeux

**Files:**
- Modify: `index.html` (`#quiz` bandeau, JS)

**Interfaces:**
- Produces : `startQuiz(1)` (« Trouve la bonne partie ! », d'après le volcan l.2628-2740 : 3 questions tirées de `JEU_PARTIES`, l'enfant touche la zone cible, étoiles, confettis **en laine** : petits ronds `.w.lite` qui tombent) et `startQuiz(2)` (« Rêve ou pour de vrai ? » : 3 questions de `JEU_REVE`, deux gros boutons `#vrai` 👀 Pour de vrai / `#reve` 💭 C'est un rêve, même récompense). Bandeau `#quiz` en feutrine au-dessus de la scène ; `aria-live="polite"` pour le score.

- [ ] **Step 1 : Implémenter.** **Step 2 : Vérifier** — Playwright : jouer les deux jeux jusqu'aux confettis, captures. Console propre.
- [ ] **Step 3 : Commit** — `git commit -m "Mini-jeux : trouve la bonne partie, rêve ou pour de vrai"`.

### Task 17 : Carte « Pour les parents » et réglages

**Files:**
- Modify: `index.html` (`#parents` carte HTML repliée, JS)

**Interfaces:**
- Produces : `<details id="parents">` : champs prénom (`#prenom`), titre de chanson (`#chansonTitre`), lien ou id YouTube (`#chansonId`, accepte une URL `youtube.com/watch?v=` / `youtu.be/` ou un id ; `parseYt(str)` dans le bloc PURE → id ou `null`), carte réconfort (`select#reconfort` chanson/doudou/câlin), thème (bouton), version allégée (`checkbox#lite`), son (`checkbox#sonPref`) ; tout écrit via `prefs.set`. Texte pour les parents (≤ 12 lignes, spec §8) + lien `docs/recherche-cerveau-sommeil.md` (URL GitHub du dépôt).

- [ ] **Step 1 : Ajouter à `test/data.test.js`** : `parseYt('https://www.youtube.com/watch?v=jqGPppvVmBc&list=x')==='jqGPppvVmBc'`, `parseYt('https://youtu.be/jqGPppvVmBc')==='jqGPppvVmBc'`, `parseYt('jqGPppvVmBc')==='jqGPppvVmBc'`, `parseYt('pas un lien')===null`.
- [ ] **Step 2 : Lancer** → échec ; **Step 3 : Implémenter** ; **Step 4 : Lancer** → passe. Capture de la carte dépliée. Console propre.
- [ ] **Step 5 : Commit** — `git commit -m "Pour les parents : réglages, prénom, chanson, texte de conseils"`.

### Task 18 : Ambiance, accessibilité, polish, 15 combinaisons

**Files:**
- Modify: `index.html`

- [ ] **Step 1 : Chasse aux détails** — les 15 combinaisons `vue × temps` avec et sans cartes (`cartes=pouce,ogre,copains,ri`), en feutrine, en riso et en allégé (`lite=1`) : aucun élément orphelin, contrastes de nuit OK, phrase lisible, budget `document.querySelectorAll('#scene .w:not(.lite)').length ≤ 40` par vue visible ; changement de thème en plein rêve via `browser_evaluate` `setTheme('riso')` à `temps=3` → le rêve reste (Review Focus 4) ; reduced-motion émulé (`browser_emulate_media` `reducedMotion:'reduce'`) → `data-lite="1"` et aucune animation ; téléphone (`browser_resize` 390 × 844) → 1 colonne, curseurs utilisables ; `z-index` loupe vs bandeau quiz vs carte chanson.
- [ ] **Step 2 : Vérifier** — console vierge sur tout le parcours (chargement → cartes → nuit → rêve → télécommande → histoire → jeux → loupe) ; `node --test test/` passe.
- [ ] **Step 3 : Commit** — `git commit -m "Polish : combinaisons, contrastes, reduced-motion, téléphone"`.

### Task 19 : README, NOTES, publication GitHub Pages

**Files:**
- Create: `README.md` ; Modify: `NOTES.md`

- [ ] **Step 1 : README** sur le modèle des aînés (lien Pages `https://w3cdotorg.github.io/dans-les-reves/`, « Ce que ça fait », « La science est prise au sérieux » avec le tableau des régions et la distinction cauchemar / terreur nocturne, « Pour les parents » en 5 lignes, utilisation, technique : deux thèmes, filtres, budget, tests `node --test test/`, licence MIT, crédits : l'école des loisirs pour la chanson, César pour le pouce, la synthèse CSEN / Canopé pour la science).
- [ ] **Step 2 : NOTES.md** — entrée de clôture : ce qui a marché, ce qui a raté, budget réel de filtres mesuré, idées pour plus tard (Three.js « tourne le cerveau »).
- [ ] **Step 3 : Publier** — `gh api -X POST repos/w3cdotorg/dans-les-reves/pages -f build_type=legacy -f 'source[branch]=main' -f 'source[path]=/'` (ou l'interface), attendre le déploiement, ouvrir l'URL, capture finale.
- [ ] **Step 4 : Commit et push** — `git commit -m "README et publication"` ; `git push`.

## Self-review (fait à l'écriture du plan)

- **Couverture du spec** : §1-2 intention/anti-objectifs → Global Constraints + Tasks 10-11 (ogre jamais en dernier) ; §3 contraintes → Task 1 (thèmes, allégé, URL), 12 (clavier), 18 (reduced-motion, téléphone) ; §4.1 curseurs → 6-7 ; §4.2 scène, avatar, décor piloté → 3-4, 8 ; §4.3 cartes → 2, 8 ; §4.4 rangement → 9 ; §4.5 rêve → 10 ; §4.6 télécommande → 11 ; §4.7 histoire → 15 ; §5 zones → 2, 12 ; §6 thèmes → 1 ; §7 interactions → 12-14, 16 ; §8 parents → 17 ; §9 technique/tests → 2, 10-12, 17 ; §11 décisions relecture → 8 (décor piloté), 10 (rôles, charges), 14 (loupe), 15 (accord). Manque repéré et corrigé : « Encore un rêve » (ajouté en Task 10), étiquette « je grandis » (Task 9).
- **Cohérence des noms** : `setCut/setTime/lerpArr/pickCard/resetDay/composeDream/renderDream/applyRemote/openSong/showInfo/speak/setTheme/setLite/setAvatar/startStory/startQuiz/inflect/parseYt/remoteStep`, groupes `#g-toile/#g-dehors/#g-dedans/#g-pres/#g-ecran/#g-boite/#g-hs/#g-ui`, événements `temps` et `journee`, préfixe `reves.` — vérifiés dans toutes les tâches.
- **Review Focus** : 1 → Task 10 step 6 ; 2 → Task 10 test ; 3 → Task 11 step 5 ; 4 → Task 18 ; 5 → Task 12 step 5.
- **Proportion** : le plan fixe des noms, des coordonnées, des tables d'interpolation et des tests ; aucun corps de fonction n'est transcrit.

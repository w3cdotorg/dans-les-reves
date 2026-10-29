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

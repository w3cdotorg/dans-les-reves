/* Données du bloc PURE : cartes, zones, jeux, histoire, phrases, accord de genre.
   Lancer : node --test test/ */
const test = require('node:test');
const assert = require('node:assert/strict');
const load = require('./_load.js');

const D = load();
const { CARTES, MODIFS, INFO, JEU_PARTIES, JEU_REVE, HISTOIRE, TRANSFOS, PHRASES, inflect, lerpArr } = D;

/* Les objets créés dans le contexte vm ont un autre Object.prototype :
   deepEqual strict les refuse. On les compare en données simples. */
const plain = x => JSON.parse(JSON.stringify(x));

/* Nombre de phrases : une ponctuation finale (. ! ? …), éventuellement suivie
   d'un guillemet fermant, puis une majuscule ou la fin du texte.
   « C'est le pouce d'un ogre ! » Tout… compte pour une fin de phrase ;
   « attention ! ». ne compte qu'une fois. */
function phrases(s){
  return (s.match(/[.!?…](\s*»)?(?=\s+[A-ZÀ-ÖØ-Þ«]|\s*$)/g) || []).length;
}

/* Tous les textes que l'enfant peut entendre. */
function tousLesTextes(){
  return [
    ...CARTES.flatMap(c => [c.nom, c.texte, c.greffe ? c.greffe.nom : '', c.ton || '']),
    ...Object.values(INFO).flatMap(z => [z.titre, z.texte]),
    ...JEU_PARTIES.map(q => q.q),
    ...JEU_REVE.map(q => q.q),
    ...HISTOIRE.map(h => h.texte),
    ...TRANSFOS.map(t => t.texte),
    ...Object.values(PHRASES)
  ];
}

test('le compteur de phrases du test lui-même', () => {
  assert.equal(phrases('Un. Deux !'), 2);
  assert.equal(phrases('Ils ont dit : « C\'est le pouce d\'un ogre ! » Tout le monde a ri.'), 2);
  assert.equal(phrases('Elle sonne : « attention ! ». Puis elle se tait.'), 2);
  assert.equal(phrases('Un pouce de 12 m, en bronze.'), 1);
});

/* Le brief dit « 22 cartes » mais énumère 23 slugs, et la table du spec §4.3 compte
   23 cartes distinctes (« un câlin » y figure deux fois : ressenti et réconfort).
   On garde les 23 cartes nommées ; voir NOTES.md. */
test('23 cartes, slugs uniques, champs valides', () => {
  assert.equal(CARTES.length, 23);
  const slugs = CARTES.map(c => c.slug);
  assert.equal(new Set(slugs).size, 23);
  assert.deepEqual(plain(slugs), ['pouce','glace','chien','velo','piscine','gateau','tracteur','orage','manege',
    'ogre','pirate','dragon','anniversaire','copains','parents','mamie','maitresse',
    'ri','peur','fache','calin','chanson','doudou']);
  for(const c of CARTES){
    assert.ok([3,2,1,0,-2].includes(c.charge), c.slug + ' charge');
    assert.ok(['vu','mot','gens','ressenti','reconfort'].includes(c.cat), c.slug + ' cat');
    assert.ok(['oeil','oreille'].includes(c.entree), c.slug + ' entree');
    assert.equal(typeof c.base, 'boolean', c.slug + ' base');
    assert.ok(c.nom && c.emoji, c.slug + ' nom/emoji');
    assert.equal(phrases(c.texte), 2, c.slug + ' : deux phrases → ' + c.texte);
  }
});

test('charges, catégories et entrées du spec §4.3 et du ledger', () => {
  const by = Object.fromEntries(CARTES.map(c => [c.slug, c]));
  const attendu = {
    pouce:['vu',0,true], glace:['vu',0,true], chien:['vu',0,true], velo:['vu',0,true],
    piscine:['vu',0,true], gateau:['vu',0,true], tracteur:['vu',0,true], orage:['vu',3,true],
    manege:['vu',0,true], ogre:['mot',3,false], pirate:['mot',1,false], dragon:['mot',3,false],
    anniversaire:['mot',1,false], copains:['gens',1,true], parents:['gens',1,true],
    mamie:['gens',1,true], maitresse:['gens',1,true], ri:['ressenti',1,false],
    peur:['ressenti',3,false], fache:['ressenti',2,false], calin:['ressenti',1,false],
    chanson:['reconfort',-2,false], doudou:['reconfort',-2,true]
  };
  for(const [slug, [cat, charge, base]] of Object.entries(attendu)){
    assert.equal(by[slug].cat, cat, slug + ' cat');
    assert.equal(by[slug].charge, charge, slug + ' charge');
    assert.equal(by[slug].base, base, slug + ' base');
  }
  for(const c of CARTES) assert.equal(c.entree, c.cat === 'vu' ? 'oeil' : (c.slug === 'doudou' ? 'oeil' : 'oreille'), c.slug + ' entree');
  assert.deepEqual(plain(by.pouce.greffe), { nom:'un pouce géant', forme:'pouce', g:'m' });
  assert.equal(by.pouce.nom, 'le pouce géant');
  assert.equal(by.ogre.nom, 'le mot « ogre »');
  assert.equal(by.ogre.greffe.nom, 'un ogre');
  assert.equal(by.ogre.greffe.forme, 'ogre');
  assert.equal(by.calin.greffe.forme, 'calin');
  assert.equal(by.chanson.greffe.forme, 'chanson');
});

test('ressentis jamais base ; toute base ou greffe a une forme', () => {
  for(const c of CARTES){
    if(c.cat === 'ressenti') assert.equal(c.base, false, c.slug);
    if(c.base || c.greffe){
      assert.ok(c.greffe && c.greffe.forme && c.greffe.nom, c.slug + ' greffe.forme');
    }
  }
});

test('accords : genre des noms, formes du modificateur, « ta chanson »', () => {
  const G = ['m','f','mp','fp'];
  for(const c of CARTES){
    assert.ok(G.includes(c.g), c.slug + ' g');
    assert.ok(G.includes(c.greffe.g), c.slug + ' greffe.g');
  }
  for(const m of Object.values(MODIFS)) assert.ok(m.nom && m.f && m.mp && m.fp);
  const by = Object.fromEntries(CARTES.map(c => [c.slug, c]));
  assert.equal(by.chanson.ton, 'ta chanson');
  assert.equal(by.doudou.ton, 'ton doudou');
  assert.equal(by.calin.ton, 'un câlin');
});

test('MODIFS : six modificateurs nommés', () => {
  assert.deepEqual(plain(Object.fromEntries(Object.entries(MODIFS).map(([k, v]) => [k, v.nom]))), {
    gigantesque:'gigantesque', envers:'à l\'envers', desobeit:'qui n\'obéit pas',
    multiplie:'multiplié', minuscule:'tout petit', couleur:'d\'une autre couleur'
  });
});

test('INFO : ≥ 32 zones, ids du brief, deux phrases chacune', () => {
  assert.ok(Object.keys(INFO).length >= 32);
  const ids = {
    1:['cortex','frontal','occipital','temporal','parietal','hippocampe','amygdale','thalamus','horloge',
       'pineale','calleux','cervelet','tronc','moelle','nerf-optique','oeil','oreille','crane','liquide'],
    0:['soleil','lune','lampe','lit','doudou','fenetre','expo','boite','ecran'],
    2:['neurone','synapse','vague','fuseau','cellule']
  };
  for(const [vue, liste] of Object.entries(ids)){
    for(const id of liste){
      assert.ok(INFO[id], 'zone manquante : ' + id);
      assert.ok([].concat(INFO[id].vue).includes(Number(vue)), id + ' vue');
    }
  }
  for(const c of CARTES.filter(c => c.cat === 'vu' || c.cat === 'gens')){
    assert.ok(INFO['decor-' + c.slug], 'decor-' + c.slug);
    assert.equal(INFO['decor-' + c.slug].vue, 0);
  }
  for(const [id, z] of Object.entries(INFO)){
    assert.ok(z.emoji && z.titre && z.texte, id);
    /* vue : un nombre, ou un tableau non vide d'entiers 0..2 sans doublon */
    const vues = [].concat(z.vue);
    assert.ok(vues.length >= 1 && vues.every(v => [0,1,2].includes(v)), id + ' vue');
    assert.equal(new Set(vues).size, vues.length, id + ' vue sans doublon');
    assert.equal(phrases(z.texte), 2, id + ' : deux phrases → ' + z.texte);
  }
  /* l'écran du rêve et la boîte à souvenirs sont visibles Dehors et Dedans */
  assert.deepEqual(plain(INFO.ecran.vue), [0,1]);
  assert.deepEqual(plain(INFO.boite.vue), [0,1]);
  assert.match(INFO['decor-pouce'].texte, /statue en bronze/);
  assert.match(INFO['decor-pouce'].texte, /César/);
  assert.match(INFO['decor-pouce'].texte, /ne bouge pas/);
});

test('jeux : 8 + 8 questions', () => {
  assert.equal(JEU_PARTIES.length, 8);
  for(const q of JEU_PARTIES){
    assert.ok(q.q, 'question');
    assert.ok(INFO[q.cible], 'cible inconnue : ' + q.cible);
  }
  assert.equal(JEU_REVE.length, 8);
  for(const q of JEU_REVE){
    assert.ok(q.q && q.emoji);
    assert.ok(['vrai','reve'].includes(q.reponse));
  }
  assert.equal(JEU_REVE.find(q => q.q.includes('un pouce de 12 mètres')).reponse, 'vrai');
  assert.equal(JEU_REVE.find(q => q.q.includes('un ogre gigantesque')).reponse, 'reve');
  assert.equal(JEU_REVE.filter(q => q.reponse === 'vrai').length, 4);
  /* jamais la peur là où l'enfant dort (revue tâche 2) */
  for(const q of JEU_REVE) assert.doesNotMatch(q.q, /chambre|\blit\b/, q.q);
});

test('histoire du pouce : ≥ 10 étapes, actions, prénom', () => {
  assert.ok(HISTOIRE.length >= 10);
  for(const h of HISTOIRE){
    assert.ok([0,1,2].includes(h.vue), 'vue');
    assert.ok(Number.isInteger(h.temps) && h.temps >= 0 && h.temps <= 4, 'temps');
    assert.ok(h.texte);
    if('action' in h) assert.ok(['reve','telecommande','fin'].includes(h.action));
    /* l'appelant fait texte.replace('{PRENOM}', …) : une seule occurrence, et jamais en
       début de phrase (« il » y serait sans majuscule). */
    assert.ok((h.texte.match(/\{PRENOM\}/g) || []).length <= 1, 'un seul {PRENOM} : ' + h.texte);
    assert.doesNotMatch(h.texte, /(^|[.!?…]\s+)\{PRENOM\}/, '{PRENOM} en début de phrase : ' + h.texte);
  }
  const actions = HISTOIRE.map(h => h.action).filter(Boolean);
  assert.deepEqual(plain(actions), ['reve','telecommande','fin']);
  assert.equal(HISTOIRE.at(-1).action, 'fin');
  assert.equal(HISTOIRE.at(-1).texte, 'À toi de faire ta journée !');
  const iReve = HISTOIRE.findIndex(h => h.action === 'reve');
  const iTele = HISTOIRE.findIndex(h => h.action === 'telecommande');
  assert.ok(iReve < iTele, 'le rêve avant la télécommande');
  const tout = HISTOIRE.map(h => h.texte).join(' ');
  assert.match(tout, /12 mètres/);
  assert.match(tout, /bronze/);
  assert.match(tout, /pouce d'un ogre/);
  assert.match(tout, /\{terrorisé\|terrorisée\} par un ogre gigantesque/);
  assert.match(tout, /Hey, ho, les chiens pirates/);
  assert.match(tout, /a raconté l'ogre gigantesque\. Et maintenant, \{il\|elle\} sait d'où il venait\./);
  /* l'ogre n'est jamais la dernière image : rien après la télécommande ne fait peur */
  assert.ok(HISTOIRE.slice(iTele + 1).every(h => !/terroris|cauchemar/.test(h.texte)));
  const avecPrenom = inflect(HISTOIRE[0].texte.replace('{PRENOM}', 'Raphaël'), 'fille');
  assert.match(avecPrenom, /Raphaël/);
  assert.doesNotMatch(avecPrenom, /[{}]/);
});

test('télécommande : trois transformations gentilles', () => {
  assert.deepEqual(plain(TRANSFOS.map(t => t.id)), ['bronze','lapin','danse']);
  for(const t of TRANSFOS) assert.ok(t.texte && t.texte.length > 20);
});

test('PHRASES : gabarits exacts', () => {
  assert.deepEqual(plain(PHRASES), {
    reve: 'Dans le rêve, {BASE} est devenu {GREFFE} {MODIF}, parce que ton cerveau a mélangé {C1} avec {C2}. Le chef qui vérifie dormait, alors personne n\'a dit « mais non, c\'est {VRAI} ! »',
    seul: 'Dans le rêve, {BASE} était {MODIF}, parce que ton cerveau l\'a rejoué.',
    flou: 'Tu n\'as rien mis dans ta journée : cette nuit, ton cerveau range et se rince, et le rêve est tout flou.',
    finitBien: '… mais {RECONFORT} était dans ta tête, alors le film a changé tout seul.',
    cle: 'C\'est mon cerveau qui a mélangé. C\'est un rêve. Je change de chaîne.'
  });
});

test('inflect : accord garçon / fille', () => {
  assert.equal(inflect('{il|elle} est {terrorisé|terrorisée}', 'fille'), 'elle est terrorisée');
  assert.equal(inflect('{il|elle} est {terrorisé|terrorisée}', 'garcon'), 'il est terrorisé');
  assert.equal(inflect('rien à accorder', 'fille'), 'rien à accorder');
  assert.equal(inflect('{il|elle}', undefined), 'il', 'sans avatar : forme du garçon (l\'anecdote)');
  /* {PRENOM} et {BASE} ne sont pas des marqueurs d'accord */
  assert.equal(inflect('{PRENOM} {BASE}', 'fille'), '{PRENOM} {BASE}');
});

test('aucun marqueur cassé : après accord, plus d\'accolade d\'accord nulle part', () => {
  for(const s of tousLesTextes()){
    for(const genre of ['garcon','fille']){
      const out = inflect(s, genre).replace(/\{(PRENOM|BASE|GREFFE|MODIF|C1|C2|VRAI|RECONFORT)\}/g, '');
      assert.doesNotMatch(out, /[{}|]/, 'marqueur mal formé : ' + s);
    }
  }
});

test('honnêteté (recherche §5) : mots interdits absents, prudences présentes', () => {
  const tout = tousLesTextes().join(' \n ');
  assert.doesNotMatch(tout, /se repose|s'éteint/i, 'le cerveau travaille la nuit');
  assert.doesNotMatch(tout, /chass/i, 'on ne chasse pas le monstre');
  assert.doesNotMatch(tout, /tromp/i, 'le cerveau ne s\'est pas trompé');
  assert.doesNotMatch(tout, /poison|poubelle|déchet/i, 'on dit « se rince »');
  assert.doesNotMatch(tout, /vainc|vaincu|tué|tuer/i, 'jamais vaincu');
  assert.doesNotMatch(tout, /cassé|erreur/i, 'le cauchemar n\'est pas une erreur');
  /* le progrès moteur pendant le sommeil n'est pas établi chez l'enfant (revue tâche 2) */
  assert.doesNotMatch(tout, /encore mieux demain|mieux après une bonne nuit/i);
  assert.match(tout, /beaucoup de chercheurs pensent que/i);
  assert.match(tout, /les chercheurs ne savent pas encore tout/i);
  assert.match(tout, /sommeil profond/);
  assert.match(tout, /sommeil paradoxal/);
  assert.match(tout, /le grand sommeil calme/);
  assert.match(tout, /le sommeil des rêves/);
  assert.match(tout, /se rince/);
});

test('lerpArr : interpolation par morceaux', () => {
  assert.equal(lerpArr([0,1,0,0,0], 0.5), 0.5);
  assert.equal(lerpArr([0,1,0,0,0], 1), 1);
  assert.equal(lerpArr([0,1,0,0,4], 4), 4);
  assert.equal(lerpArr([0,1,0,0,4], 3.5), 2);
});

/* Décision du propriétaire (29/10, spec §6 bis) : aucun son produit par la page. */
test('aucun son : ni synthèse vocale, ni bouton son, ni préférence son', () => {
  const html = require('fs').readFileSync(require('path').join(__dirname, '..', 'index.html'), 'utf8');
  for(const interdit of ['speechSynthesis', 'id="sound"', 'id="say"', 'soundOn', 'reves.son']){
    assert.ok(!html.includes(interdit), 'index.html contient encore « ' + interdit + ' »');
  }
  assert.doesNotMatch(html, /prefs\.(get|set)\(\s*['"]son['"]/, 'préférence « son » lue ou écrite');
  assert.doesNotMatch(html, /id=['"](sound|say)['"]/, 'bouton son (guillemets simples ou doubles)');
});

/* Task 17 : parseYt (bloc PURE) lit un lien YouTube ou un identifiant. _load.js n'exporte pas
   parseYt : on charge le bloc ici, dans un contexte vm vide. */
const parseYt = (() => {
  const fs = require('fs'), path = require('path'), vm = require('vm');
  const src = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const m = src.match(/\/\* PURE-BEGIN \*\/([\s\S]*?)\/\* PURE-END \*\//);
  const ctx = {};
  vm.runInNewContext(m[1] + ';this.f = typeof parseYt === "function" ? parseYt : null', ctx);
  return ctx.f;
})();
test('parseYt : liens YouTube et identifiants', () => {
  assert.equal(typeof parseYt, 'function');
  assert.equal(parseYt('https://www.youtube.com/watch?v=jqGPppvVmBc&list=x'), 'jqGPppvVmBc');
  assert.equal(parseYt('https://youtu.be/jqGPppvVmBc'), 'jqGPppvVmBc');
  assert.equal(parseYt('https://youtu.be/jqGPppvVmBc?t=4'), 'jqGPppvVmBc');
  assert.equal(parseYt('https://www.youtube.com/shorts/jqGPppvVmBc'), 'jqGPppvVmBc');
  assert.equal(parseYt('https://www.youtube-nocookie.com/embed/jqGPppvVmBc?autoplay=1'), 'jqGPppvVmBc');
  assert.equal(parseYt('  jqGPppvVmBc  '), 'jqGPppvVmBc');
  assert.equal(parseYt('jqGPppvVmBc'), 'jqGPppvVmBc');
  assert.equal(parseYt('pas un lien'), null);
  assert.equal(parseYt(''), null);
  assert.equal(parseYt(null), null);
  assert.equal(parseYt('https://example.com/watch?v=jqGPppvVmBc'), null);
  assert.equal(parseYt('https://www.youtube.com/watch?v=x'), null);
});

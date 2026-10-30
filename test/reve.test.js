/* Le générateur de rêve (Task 10, spec §4.5) : composeDream est pur, déterministe,
   et toute paire de cartes donne un rêve lisible et une phrase correcte.
   Lancer : node --test test/ */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const load = require('./_load.js');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const { CARTES, MODIFS, PHRASES, composeDream } = load();
const compte = id => html.split(`id="${id}"`).length - 1;

/* Une phrase propre : rien à remplir, pas d'espace double ni avant une virgule ou un
   point, pas de « de le », pas de « le » ou « la » devant une voyelle, aucun mot interdit
   (spec §2 anti-objectifs ; recherche §5). */
const INTERDITS = ['se repose', 'chass', 'tromp', 'poison', 'vainc', 'tué', 'cassé', 'erreur'];
function propre(p, ctx){
  assert.equal(typeof p, 'string', ctx);
  assert.ok(!/[{}|]/.test(p), ctx + ' : reste à remplir → ' + p);
  assert.ok(!/ {2}/.test(p), ctx + ' : espace double → ' + p);
  assert.ok(!/ [,.]/.test(p), ctx + ' : espace avant la ponctuation → ' + p);
  assert.ok(!/\b[Dd]e (le|les) /.test(p), ctx + ' : « de le » → ' + p);
  assert.ok(!/\b[Àà] (le|les) /.test(p), ctx + ' : « à le » → ' + p);
  assert.ok(!/\b(le|la|Le|La) [aeiouyéèêàâîôœ]/.test(p), ctx + ' : élision manquante → ' + p);
  assert.ok(!/\bmon doudou\b/.test(p), ctx + ' : « mon doudou » dans la bouche du narrateur → ' + p);
  assert.ok(!/undefined|null|NaN/.test(p), ctx + ' → ' + p);
  assert.ok(!/\bétai(en)?t qui\b/.test(p), ctx + ' : « était qui » → ' + p);
  assert.ok(!/^Dans le rêve, deux /.test(p), ctx + ' : sujet « deux … » sans article → ' + p);
  for(const mot of INTERDITS) assert.ok(!p.toLowerCase().includes(mot), ctx + ' : « ' + mot + ' » → ' + p);
}

test('composeDream existe et une journée vide ne fait pas de rêve', () => {
  assert.equal(typeof composeDream, 'function');
  assert.equal(composeDream([]), null);
  assert.equal(composeDream([], { seed: 3, genre: 'fille' }), null);
  assert.equal(composeDream(['nimporte']), null, 'un slug inconnu est ignoré');
});

test("l'histoire du pouce : pouce, ogre, copains, j'ai ri", () => {
  const r = composeDream(['pouce', 'ogre', 'copains', 'ri']);
  assert.equal(r.greffe.slug, 'ogre');
  assert.equal(r.base.slug, 'pouce');
  assert.equal(r.contexte.slug, 'copains');
  assert.deepEqual([...r.oublies.map(c => c.slug)], ['ri']);   /* tableau du contexte vm : recopié */
  assert.equal(r.modif, 'gigantesque');
  assert.equal(r.verdict, 'cauchemar');
  assert.equal(r.reconfort, null);
  assert.ok(r.phrase.includes('le pouce géant est devenu un ogre gigantesque'), r.phrase);
  assert.ok(r.phrase.includes('mélangé le pouce géant avec le mot « ogre »'), r.phrase);
  assert.ok(r.phrase.includes("c'est une statue"), r.phrase);
  propre(r.phrase, 'pouce/ogre');
});

test('glace puis chien : beau rêve, le chien (dernière choisie) est la base', () => {
  for(const seed of [0, 1, 2, 7]){
    const r = composeDream(['glace', 'chien'], { seed });
    assert.equal(r.verdict, 'beau');
    assert.ok(['minuscule', 'couleur'].includes(r.modif), r.modif);
    assert.equal(r.base.slug, 'chien');
    assert.equal(r.greffe.slug, 'glace');
    assert.ok(r.phrase.includes('le chien est devenu une glace'), r.phrase);
    assert.ok(r.phrase.includes("ce n'est pas pour de vrai"), r.phrase);
    propre(r.phrase, 'glace/chien ' + seed);
  }
  assert.notEqual(composeDream(['glace', 'chien'], { seed: 0 }).modif, composeDream(['glace', 'chien'], { seed: 1 }).modif,
    '« Encore un rêve » change le modificateur');
});

test('copains et pirate : rêve rigolo, multiplié, accordé au pluriel', () => {
  const r = composeDream(['copains', 'pirate']);
  assert.equal(r.base.slug, 'copains');
  assert.equal(r.greffe.slug, 'pirate');
  assert.equal(r.modif, 'multiplie');
  assert.equal(r.verdict, 'rigolo');
  assert.ok(r.phrase.includes('les copains sont devenus des pirates multipliés'), r.phrase);
  assert.ok(r.phrase.includes('mélangé les copains avec le mot « pirate »'), r.phrase);
  propre(r.phrase, 'copains/pirate');
});

test('pouce, ogre, chanson : un mauvais rêve qui finit bien', () => {
  const r = composeDream(['pouce', 'ogre', 'chanson']);
  assert.equal(r.verdict, 'finitBien');
  assert.equal(r.reconfort.slug, 'chanson');
  assert.equal(r.greffe.slug, 'ogre');
  assert.equal(r.base.slug, 'pouce');
  assert.ok(r.phrase.endsWith(PHRASES.finitBien.replace('{RECONFORT}', 'ta chanson')), r.phrase);
  propre(r.phrase, 'pouce/ogre/chanson');
});

test('le doudou réconforte un cauchemar, il ne devient pas l\'ogre', () => {
  const r = composeDream(['doudou', 'ogre']);
  assert.equal(r.verdict, 'finitBien');
  assert.equal(r.reconfort.slug, 'doudou');
  assert.ok(r.phrase.includes('ton doudou était dans ta tête'), r.phrase);
  propre(r.phrase, 'doudou/ogre');
});

/* spec §4.3 / §4.5-4 : le câlin choisi comme carte réconfort dans les réglages est apaisant (−2) */
test('le câlin choisi comme réconfort finit bien un cauchemar ; sinon, cauchemar', () => {
  const r = composeDream(['pouce', 'ogre', 'calin'], { reconfort: 'calin' });
  assert.equal(r.verdict, 'finitBien');
  assert.equal(r.reconfort.slug, 'calin');
  assert.equal(r.greffe.slug, 'ogre');
  assert.ok(r.phrase.includes('un câlin était dans ta tête'), r.phrase);
  assert.ok(r.courte.includes('le câlin était dans ta tête'), r.courte);
  propre(r.phrase, 'pouce/ogre/calin (réconfort)');
  propre(r.courte, 'pouce/ogre/calin (réconfort, courte)');
  const sans = composeDream(['pouce', 'ogre', 'calin']);
  assert.equal(sans.verdict, 'cauchemar');
  assert.equal(sans.reconfort, null);
  assert.equal(composeDream(['pouce', 'ogre', 'calin'], { reconfort: 'chanson' }).verdict, 'cauchemar');
  assert.equal(composeDream(['pouce', 'ogre', 'chanson'], { reconfort: 'calin' }).reconfort.slug, 'chanson', 'la chanson reste apaisante');
  assert.equal(load().CARTES.find(c => c.slug === 'calin').charge, 1, 'CARTES ne change pas');
  assert.equal(CARTES.find(c => c.slug === 'calin').charge, 1);
});

test('une carte apaisante seule : beau rêve', () => {
  const r = composeDream(['chanson']);
  assert.equal(r.verdict, 'beau');
  assert.ok(r.base);
  assert.equal(r.greffe, null);
  propre(r.phrase, 'chanson');
});

test("un ressenti seul (j'ai ri) : sa propre base, gabarit « seul »", () => {
  const r = composeDream(['ri']);
  assert.ok(r.base);
  assert.equal(r.base.slug, 'ri');
  assert.equal(r.greffe, null);
  assert.ok(['minuscule', 'multiplie', 'couleur'].includes(r.modif), r.modif);
  assert.ok(r.phrase.startsWith('Dans le rêve, '), r.phrase);
  assert.ok(r.phrase.includes(', parce que ton cerveau l'), r.phrase);
  assert.ok(r.phrase.includes(' rejoué'), r.phrase);
  propre(r.phrase, 'ri');
});

test('une chose vue seule : gabarit « seul », accordé', () => {
  const r = composeDream(['piscine'], { seed: 0 });
  assert.equal(r.base.slug, 'piscine');
  assert.ok(/^Dans le rêve, la piscine était .+, parce que ton cerveau l'a rejouée\.$/.test(r.phrase), r.phrase);
  const p = composeDream(['parents'], { seed: 1 });
  assert.ok(/^Dans le rêve, papa et maman étaient .+, parce que ton cerveau les a rejoués\.$/.test(p.phrase), p.phrase);
});

test('je me suis fâché + vélo : rêve bizarre, à l\'envers ou qui n\'obéit pas', () => {
  const r0 = composeDream(['fache', 'velo'], { seed: 0 });
  const r1 = composeDream(['fache', 'velo'], { seed: 1 });
  assert.equal(r0.verdict, 'bizarre');
  assert.deepEqual([r0.modif, r1.modif].sort(), ['desobeit', 'envers']);
  assert.equal(r0.base.slug, 'velo');
  assert.equal(r0.greffe.slug, 'fache');
  assert.ok(r0.phrase.includes('le moment où tu t'), r0.phrase);
  const f = composeDream(['fache', 'velo'], { seed: 0, genre: 'fille' });
  assert.ok(f.phrase.includes("le moment où tu t'es fâchée"), f.phrase);
  propre(r0.phrase, 'fache/velo'); propre(r1.phrase, 'fache/velo 1'); propre(f.phrase, 'fache/velo fille');
});

test('déterministe : même journée, même graine → même rêve', () => {
  const a = composeDream(['pouce', 'ogre', 'copains', 'ri'], { seed: 4 });
  const b = composeDream(['pouce', 'ogre', 'copains', 'ri'], { seed: 4 });
  assert.equal(a.phrase, b.phrase);
  assert.equal(a.modif, b.modif);
});

test('composeDream ne modifie pas son entrée', () => {
  const j = ['pouce', 'ogre', 'copains', 'ri'];
  composeDream(j, { seed: 1 });
  assert.deepEqual(j, ['pouce', 'ogre', 'copains', 'ri']);
});

/* Toutes les paires (253 = C(23,2), dans les deux ordres), garçon et fille, deux graines. */
test('toutes les paires de cartes font un rêve lisible et une phrase correcte', () => {
  let n = 0;
  const paires = new Set();
  for(const a of CARTES) for(const b of CARTES){
    if(a === b) continue;
    paires.add([a.slug, b.slug].sort().join('+'));
    for(const genre of [undefined, 'garcon', 'fille']) for(const seed of [0, 1, 2]){
      const r = composeDream([a.slug, b.slug], { seed, genre });
      const ctx = `${a.slug}+${b.slug} (${genre}, ${seed})`;
      assert.ok(r, ctx);
      assert.ok(r.base, ctx + ' base');
      assert.ok(r.base.greffe || r.base.base, ctx + ' base dessinable');
      assert.ok(r.phrase.length > 40, ctx + ' : ' + r.phrase);
      assert.ok(Object.keys(MODIFS).includes(r.modif), ctx + ' modif');
      assert.ok(['cauchemar', 'bizarre', 'beau', 'rigolo', 'finitBien'].includes(r.verdict), ctx + ' verdict');
      assert.ok(r.phrase.includes(MODIFS[r.modif].nom) || r.phrase.includes(MODIFS[r.modif].f)
        || r.phrase.includes(MODIFS[r.modif].mp) || r.phrase.includes(MODIFS[r.modif].fp)
        || r.phrase.includes(MODIFS[r.modif].nom.replace("n'obéit", "n'obéissait"))
        || r.phrase.includes(MODIFS[r.modif].mp.replace("n'obéissent", "n'obéissaient"))
        || (r.modif === 'desobeit' && /ne voulai(en)?t pas obéir/.test(r.phrase)), ctx + ' : le modificateur est nommé → ' + r.phrase);
      if(r.greffe){
        assert.notEqual(r.greffe.slug, r.base.slug, ctx);
        assert.ok(r.greffe.charge >= 0, ctx + ' : une carte apaisante n\'est jamais greffe');
      }
      if(r.verdict === 'finitBien') assert.ok(r.reconfort && r.reconfort.charge < 0, ctx);
      propre(r.phrase, ctx);
      n++;
    }
  }
  assert.equal(paires.size, 253);
  assert.equal(n, 253 * 2 * 9);
});

/* Les mêmes paires, le câlin choisi comme carte réconfort (il n'est alors jamais greffe). */
test('toutes les paires, câlin réconfort : un rêve lisible et des phrases correctes', () => {
  let n = 0;
  for(const a of CARTES) for(const b of CARTES){
    if(a === b) continue;
    for(const genre of ['garcon', 'fille']) for(const seed of [0, 1]){
      const r = composeDream([a.slug, b.slug], { seed, genre, reconfort: 'calin' });
      const ctx = `${a.slug}+${b.slug} (câlin réconfort, ${genre}, ${seed})`;
      assert.ok(r && r.base, ctx);
      if(r.greffe) assert.ok(r.greffe.charge >= 0 && r.greffe.slug !== 'calin', ctx + ' : le câlin n\'est jamais greffe');
      if(r.verdict === 'finitBien') assert.ok(r.reconfort && r.reconfort.charge < 0, ctx);
      propre(r.phrase, ctx);
      if(r.courte) propre(r.courte, ctx + ' (courte)');
      n++;
    }
  }
  assert.equal(n, 253 * 2 * 4);
});

test('toutes les journées de 3 et 4 cartes tirées au hasard (graine fixe) restent correctes', () => {
  let x = 12345;
  const rnd = k => { x = (x * 1103515245 + 12345) % 2147483648; return x % k; };
  for(let i = 0; i < 2000; i++){
    const j = [];
    const k = 3 + rnd(2);
    while(j.length < k){ const s = CARTES[rnd(CARTES.length)].slug; if(!j.includes(s)) j.push(s); }
    const r = composeDream(j, { seed: rnd(5), genre: rnd(2) ? 'fille' : 'garcon' });
    assert.ok(r && r.base, j.join(','));
    const utilisees = [r.base, r.greffe, r.contexte, r.reconfort, ...r.oublies].filter(Boolean).map(c => c.slug);
    assert.deepEqual([...utilisees].sort(), [...j].sort(), j.join(',') + ' : chaque carte a un rôle, une seule fois');
    propre(r.phrase, j.join(','));
  }
});

/* Les dessins du rêve : une forme de base par carte de base (et par carte que le brief
   dessine en base), une greffe par carte, l'écran et ses pièces. */
const BASES = ['pouce', 'glace', 'chien', 'velo', 'piscine', 'gateau', 'tracteur', 'orage', 'manege',
  'copains', 'parents', 'mamie', 'maitresse', 'doudou', 'calin'];
test('chaque forme de base #g-base-<forme> existe, une seule fois', () => {
  for(const f of BASES) assert.equal(compte('g-base-' + f), 1, '#g-base-' + f);
  for(const c of CARTES.filter(c => c.base)) assert.equal(compte('g-base-' + c.greffe.forme), 1, '#g-base-' + c.greffe.forme);
});
test('chaque carte a sa greffe #g-greffe-<forme>, une seule fois', () => {
  for(const c of CARTES) assert.equal(compte('g-greffe-' + c.greffe.forme), 1, '#g-greffe-' + c.greffe.forme);
});
test("l'écran du rêve : nuage, contenu, phrase, bouton « Encore un rêve »", () => {
  for(const id of ['g-ecran', 'p-ecran', 'g-reve', 't-phrase', 'encore']) assert.equal(compte(id), 1, '#' + id);
  assert.ok(/<g[^>]*id="encore"[^>]*role="button"[^>]*tabindex="0"|<g[^>]*role="button"[^>]*tabindex="0"[^>]*id="encore"/.test(html), '#encore est un bouton SVG focalisable');
});
test('aucune pièce .w ne porte d\'attribut transform dans les dessins du rêve', () => {
  const bloc = html.match(/<!-- REVE-BEGIN -->([\s\S]*?)<!-- REVE-END -->/);
  assert.ok(bloc, 'bloc REVE-BEGIN … REVE-END');
  const ws = bloc[1].match(/<[^>]*class="w[ "][^>]*>/g) || [];
  assert.ok(ws.length > 50, 'des pièces de laine');
  for(const el of ws) assert.ok(!/\stransform=/.test(el), el.slice(0, 80));
  const ecran = html.match(/<g id="g-ecran"[\s\S]*?<!-- ECRAN-END -->/);
  assert.ok(ecran, 'écran');
  for(const el of ecran[0].match(/<[^>]*class="w[ "][^>]*>/g) || []) assert.ok(!/\stransform=/.test(el), el.slice(0, 80));
});

test('mode « seul » : chaque carte seule, toutes graines et genres, une phrase correcte', () => {
  for(const c of CARTES) for(const genre of [undefined, 'garcon', 'fille']) for(const seed of [0, 1, 2]){
    const r = composeDream([c.slug], { seed, genre });
    const ctx = `${c.slug} seul (${genre}, ${seed})`;
    assert.equal(r.mode, 'seul', ctx);
    assert.ok(!/étai(en)?t qui/.test(r.phrase), ctx + ' → ' + r.phrase);
    propre(r.phrase, ctx);
  }
});

test("« je me suis fâché » seul : ne voulaient pas obéir, accordé au pluriel", () => {
  const r = composeDream(['fache'], { seed: 0 });
  assert.equal(r.modif, 'desobeit');
  assert.equal(r.phrase, "Dans le rêve, les sourcils fâchés ne voulaient pas obéir, parce que ton cerveau les a rejoués.");
  const p = composeDream(['fache', 'pirate'], { seed: 0 });
  assert.ok(p.phrase.includes('ne voulaient pas obéir'), p.phrase);
  assert.ok(!/étai(en)?t qui/.test(p.phrase), p.phrase);
});

test('« deux grands bras » prend son article en mode « seul »', () => {
  for(const seed of [0, 1, 2]){
    const r = composeDream(['calin'], { seed });
    assert.ok(r.phrase.startsWith('Dans le rêve, les deux grands bras étaient '), r.phrase);
  }
});

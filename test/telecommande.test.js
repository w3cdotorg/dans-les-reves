/* La télécommande (Task 11, spec §4.6) : trois transformations en rotation,
   jamais « vaincu », et la phrase-clé que l'enfant garde pour la nuit.
   Lancer : node --test test/ */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
/* le bloc PURE, chargé sans DOM (comme test/_load.js), avec remoteStep en plus */
function charger(){
  const m = html.match(/\/\* PURE-BEGIN \*\/([\s\S]*?)\/\* PURE-END \*\//);
  assert.ok(m, 'bloc PURE introuvable');
  const ctx = {};
  vm.runInNewContext(m[1] + ';this.__x = {TRANSFOS, PHRASES, CARTES, composeDream, phraseCourte, videoPossible,'
    + ' remoteStep: typeof remoteStep === "function" ? remoteStep : null}', ctx);
  return ctx.__x;
}
const { TRANSFOS, PHRASES, CARTES, composeDream, phraseCourte, videoPossible, remoteStep } = charger();
const compte = id => html.split(`id="${id}"`).length - 1;

test('TRANSFOS : bronze, lapin, danse, dans cet ordre', () => {
  /* Array.from : un tableau de ce contexte-ci (celui du bloc PURE vient d'un autre « realm ») */
  assert.deepEqual(Array.from(TRANSFOS, t => t.id), ['bronze', 'lapin', 'danse']);
});

test('remoteStep(n) tourne sur les trois transformations', () => {
  assert.equal(typeof remoteStep, 'function', 'remoteStep doit être dans le bloc PURE');
  assert.equal(remoteStep(0), 'bronze');
  assert.equal(remoteStep(1), 'lapin');
  assert.equal(remoteStep(2), 'danse');
  assert.equal(remoteStep(3), 'bronze');
  assert.equal(remoteStep(4), 'lapin');
  assert.equal(remoteStep(301), 'lapin');
});

test('la phrase-clé, mot pour mot', () => {
  assert.equal(PHRASES.cle, "C'est mon cerveau qui a mélangé. C'est un rêve. Je change de chaîne.");
});

test('aucune transformation ne chasse, ne vainc ni ne tue (spec §2 anti-objectifs)', () => {
  for(const t of TRANSFOS){
    const s = t.texte.toLowerCase();
    for(const mot of ['chass', 'vainc', 'tué']) assert.ok(!s.includes(mot), `${t.id} : « ${mot} » → ${t.texte}`);
  }
});

test('les dessins de la télécommande sont dans la page, une seule fois', () => {
  for(const id of ['telecommande', 'g-greffe-lapin', 'g-greffe-chiens-pirates', 'g-reconfort', 't-cle', 'chanson']){
    assert.equal(compte(id), 1, '#' + id);
  }
});

test('aucune requête YouTube écrite dans la page : l\'iframe est créée sur appui (spec §3)', () => {
  assert.ok(!/<iframe/i.test(html), 'pas d\'<iframe> dans le balisage');
  assert.ok(html.includes('https://www.youtube-nocookie.com/embed/'), 'la vidéo passe par youtube-nocookie.com');
  assert.ok(!/https?:\/\/(www\.)?youtube\.com\//.test(html), 'jamais youtube.com (seulement youtube-nocookie.com)');
});

test('la vidéo ne se charge ni hors ligne ni depuis un fichier (file://)', () => {
  assert.equal(videoPossible(true, 'https:'), true);
  assert.equal(videoPossible(true, 'http:'), true);
  assert.equal(videoPossible(false, 'https:'), false);
  assert.equal(videoPossible(true, 'file:'), false);
  assert.equal(videoPossible(undefined, 'https:'), true, 'navigator.onLine inconnu : on essaie');
});

/* une phrase courte propre : rien à remplir, pas de « de le », pas de « mon doudou » */
function courtePropre(p, ctx){
  assert.equal(typeof p, 'string', ctx);
  assert.ok(!/[{}]/.test(p), ctx + ' : reste à remplir → ' + p);
  assert.ok(!/\b[Dd]e (le|les) /.test(p), ctx + ' : « de le » → ' + p);
  assert.ok(!/\b(le|la|Le|La) [aeiouyéèêàâîôœ]/.test(p), ctx + ' : élision manquante → ' + p);
  assert.ok(!/ {2}|undefined|null/.test(p), ctx + ' → ' + p);
  assert.ok(!/\bmon doudou\b/.test(p), ctx + ' : « mon doudou » → ' + p);
  assert.ok(p.startsWith('Ton cerveau a '), ctx + ' → ' + p);
  assert.ok(p.endsWith('alors le film a changé tout seul.'), ctx + ' → ' + p);
}

test('finitBien, forme courte : « Ton cerveau a mélangé … mais ta chanson était dans ta tête… »', () => {
  const r = composeDream(['pouce', 'ogre', 'chanson'], { seed: 0, genre: 'garcon' });
  assert.equal(r.verdict, 'finitBien');
  assert.equal(r.courte, "Ton cerveau a mélangé le pouce géant avec le mot « ogre »… mais ta chanson était dans ta tête, alors le film a changé tout seul.");
  assert.equal(composeDream(['pouce', 'ogre', 'copains']).courte, null, 'sans carte apaisante : pas de forme courte');
});

test('finitBien, forme courte : les trois réconforts et plusieurs journées', () => {
  const PAR = Object.fromEntries(Array.from(CARTES, c => [c.slug, c]));
  const attendu = { chanson: 'ta chanson', doudou: 'ton doudou', calin: 'le câlin' };
  const jours = [['pouce', 'ogre'], ['chien', 'peur'], ['copains', 'dragon'], ['glace', 'orage', 'velo'], ['ogre'], ['maitresse', 'pirate', 'fache']];
  for(const j of jours) for(const genre of ['garcon', 'fille']){
    for(const slug of ['chanson', 'doudou']){
      const r = composeDream([...j, slug], { seed: 1, genre });
      if(r.verdict !== 'finitBien') continue;
      courtePropre(r.courte, j.join(',') + '+' + slug);
    }
    const r = composeDream(j, { seed: 0, genre });
    for(const slug of Object.keys(attendu)){
      const p = phraseCourte({ mode: r.mode, base: r.base, greffe: r.greffe, reconfort: PAR[slug] }, genre);
      courtePropre(p, j.join(',') + ' / ' + slug);
      assert.ok(p.includes('mais ' + attendu[slug] + ' était'), p);
    }
  }
});

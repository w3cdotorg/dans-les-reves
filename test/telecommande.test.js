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
  vm.runInNewContext(m[1] + ';this.__x = {TRANSFOS, PHRASES, remoteStep: typeof remoteStep === "function" ? remoteStep : null}', ctx);
  return ctx.__x;
}
const { TRANSFOS, PHRASES, remoteStep } = charger();
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

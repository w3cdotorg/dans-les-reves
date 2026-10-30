/* Mini-jeux (Task 16) : les deux banques de questions et le tirage de 3 questions sur 8.
   tirer3 vit dans le bloc PURE ; on le charge ici avec le même vm que _load.js.
   Lancer : node --test test/ */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const { INFO, ZONES, JEU_PARTIES, JEU_REVE } = require('./_load.js')();

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const pure = html.match(/\/\* PURE-BEGIN \*\/([\s\S]*?)\/\* PURE-END \*\//)[1];
const ctx = {};
vm.runInNewContext(pure + ';this.__t = typeof tirer3 === "function" ? tirer3 : null', ctx);
const tirer3 = ctx.__t;

test('chaque cible de « Trouve la partie » est une zone (ZONES et INFO), dans une vue', () => {
  assert.equal(JEU_PARTIES.length, 8);
  for(const q of JEU_PARTIES){
    assert.ok(ZONES[q.cible], `${q.cible} n'est pas dans ZONES`);
    assert.ok(INFO[q.cible], `${q.cible} n'est pas dans INFO`);
    for(const v of [].concat(INFO[q.cible].vue)) assert.ok([0, 1, 2].includes(v), `${q.cible} : vue ${v}`);
    assert.ok(q.q.trim().length > 0);
  }
  assert.equal(new Set(JEU_PARTIES.map(q => q.cible)).size, 8, 'huit cibles différentes');
});

test('« Rêve ou pour de vrai » : réponse vrai|reve et une explication d\'une ligne', () => {
  assert.equal(JEU_REVE.length, 8);
  for(const q of JEU_REVE){
    assert.ok(['vrai', 'reve'].includes(q.reponse), q.q);
    assert.equal(typeof q.explication, 'string', q.q);
    assert.ok(q.explication.trim().length > 0, q.q);
    assert.ok(q.explication.length <= 90, `trop longue : ${q.explication}`);
    assert.doesNotMatch(q.explication, /\n/);
  }
});

test('les textes des jeux restent honnêtes et gentils (spec §2, §3)', () => {
  const INTERDITS = ['se repose', 'chass', 'tromp', 'poison', 'vainc', 'tué', 'cassé', 'erreur', 'faux', 'nul', 'raté', 'perdu'];
  const textes = [...JEU_PARTIES.map(q => q.q), ...JEU_REVE.flatMap(q => [q.q, q.explication])];
  for(const t of textes) for(const mot of INTERDITS) assert.ok(!t.toLowerCase().includes(mot), `« ${mot} » dans : ${t}`);
});

test('tirer3 est une fonction pure du bloc PURE', () => {
  assert.equal(typeof tirer3, 'function');
});

test('tirer3 : trois indices différents de 0 à 7', () => {
  for(let s = 0; s < 500; s++){
    const t = tirer3(s * 7919 + 12345);
    assert.equal(t.length, 3);
    assert.equal(new Set(t).size, 3, `doublon pour la graine ${s}`);
    for(const i of t) assert.ok(Number.isInteger(i) && i >= 0 && i < 8, `indice ${i}`);
  }
});

test('tirer3 : même graine, même tirage ; tailles autres que 8', () => {
  assert.deepEqual([...tirer3(42)], [...tirer3(42)]);
  assert.deepEqual([...tirer3(Date.UTC(2026, 9, 30))], [...tirer3(Date.UTC(2026, 9, 30))]);
  const t = tirer3(7, 4);
  assert.equal(new Set(t).size, 3);
  for(const i of t) assert.ok(i < 4);
});

test('tirer3 : toutes les questions finissent par sortir, les tirages varient', () => {
  const vus = new Array(8).fill(0);
  const tirages = new Set();
  const t0 = 1761800000000;   /* des graines comme Date.now(), à la milliseconde près */
  for(let k = 0; k < 400; k++){
    const t = tirer3(t0 + k);
    t.forEach(i => vus[i]++);
    tirages.add(t.join(','));
  }
  for(let i = 0; i < 8; i++) assert.ok(vus[i] > 60, `la question ${i} sort trop peu (${vus[i]}/400 tirages)`);
  assert.ok(tirages.size > 100, `${tirages.size} tirages différents seulement`);
});

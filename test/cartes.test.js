/* Cartes-souvenirs (Task 8) : chaque carte a sa vignette #v-<slug>, chaque carte
   « base » a sa forme de décor Dehors #d-<slug>, et rien n'est en double.
   Lancer : node --test test/ */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const load = require('./_load.js');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const { CARTES } = load();
const compte = id => html.split(`id="${id}"`).length - 1;

test('23 cartes, slugs uniques', () => {
  assert.equal(CARTES.length, 23);
  assert.equal(new Set(CARTES.map(c => c.slug)).size, 23);
});

test('une vignette #v-<slug> par carte, une seule fois', () => {
  for(const c of CARTES) assert.equal(compte(`v-${c.slug}`), 1, `#v-${c.slug}`);
});

test('une forme de décor #d-<slug> par carte base:true, une seule fois', () => {
  const bases = CARTES.filter(c => c.base);
  assert.equal(bases.length, 14);
  for(const c of bases) assert.equal(compte(`d-${c.slug}`), 1, `#d-${c.slug}`);
});

test('pas de décor pour une carte qui n\'est pas une base', () => {
  for(const c of CARTES.filter(c => !c.base)) assert.equal(compte(`d-${c.slug}`), 0, `#d-${c.slug}`);
});

test('les emplacements et la boîte existent', () => {
  for(const id of ['g-boite', 'g-hippo-cartes', 'slot-0', 'slot-1', 'slot-2', 'slot-3', 'slot-gens', 'journee'])
    assert.equal(compte(id), 1, `#${id}`);
});

test('aucune pièce .w ne porte d\'attribut transform dans les vignettes et les décors', () => {
  const bloc = html.match(/<!-- CARTES-BEGIN -->([\s\S]*?)<!-- CARTES-END -->/);
  assert.ok(bloc, 'bloc CARTES-BEGIN … CARTES-END');
  const fautifs = [...bloc[1].matchAll(/<[^>]*class="w[ "][^>]*>/g)].map(m => m[0]).filter(t => /\stransform=/.test(t));
  assert.deepEqual(fautifs, []);
});

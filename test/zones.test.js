/* Zones cliquables (Task 12) : les formes sont générées au chargement à partir de la
   table ZONES (bloc PURE) ; on teste donc la table contre INFO et contre index.html.
   Lancer : node --test test/ */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { INFO, ZONES } = require('./_load.js')();
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');

const ids = Object.keys(INFO).filter(id => !id.startsWith('decor-'));
const cibles = z => [].concat(z.cible);

test('ZONES est une table de données', () => {
  assert.ok(ZONES && typeof ZONES === 'object');
});

test('chaque zone non décor de INFO a une entrée dans ZONES', () => {
  assert.deepEqual(ids.filter(id => !ZONES[id]), []);
});

test('ZONES ne contient que des ids de INFO', () => {
  assert.deepEqual(Object.keys(ZONES).filter(id => !INFO[id]), []);
});

test('chaque cible est un #id présent dans index.html', () => {
  for(const [id, z] of Object.entries(ZONES)){
    for(const c of cibles(z)){
      assert.match(c, /^#[A-Za-z][\w-]*$/, `${id} : cible « ${c} » n'est pas un #id`);
      assert.ok(html.includes(`id="${c.slice(1)}"`), `${id} : ${c} introuvable dans index.html`);
    }
  }
});

test('forme et marge valides (marge 6 à 10 px)', () => {
  for(const [id, z] of Object.entries(ZONES)){
    assert.ok(['rect', 'ellipse'].includes(z.forme), `${id} : forme`);
    assert.ok(z.marge >= 6 && z.marge <= 10, `${id} : marge ${z.marge}`);
  }
});

test('le code crée des .hs accessibles (role, tabindex, aria-label, data-id)', () => {
  assert.match(html, /setAttribute\('role', 'button'\)/);
  assert.match(html, /setAttribute\('tabindex'/);
  assert.match(html, /setAttribute\('aria-label', INFO\[id\]\.titre\)/);
  assert.match(html, /setAttribute\('data-id', id\)/);
  assert.match(html, /__zonesManquantes/);
  for(const g of ['hs-0', 'hs-1', 'hs-2']) assert.ok(html.includes(g), g);
});

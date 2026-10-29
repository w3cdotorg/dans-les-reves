/* Charge le bloc PURE de index.html dans un contexte vm vide (aucun DOM),
   et renvoie ses globaux. Si le bloc touche à document/window/localStorage,
   l'exécution échoue : c'est voulu. */
const fs = require('fs');
const path = require('path');
const vm = require('vm');

module.exports = function load(){
  const src = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const m = src.match(/\/\* PURE-BEGIN \*\/([\s\S]*?)\/\* PURE-END \*\//);
  if(!m) throw new Error('Bloc /* PURE-BEGIN */ … /* PURE-END */ introuvable dans index.html');
  const ctx = {};
  vm.runInNewContext(m[1] + ';this.__x = {CARTES, MODIFS, INFO, ZONES: typeof ZONES==="undefined"?null:ZONES, JEU_PARTIES, JEU_REVE, HISTOIRE, TRANSFOS, PHRASES, inflect, lerpArr, composeDream: typeof composeDream==="function"?composeDream:null}', ctx);
  return ctx.__x;
};

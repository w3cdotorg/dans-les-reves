#!/bin/bash
# Capture de la page en Chrome headless.
# Usage : test/shot.sh "<requête sans ?>" <sortie.png>   (d'où l'on veut : la page est
# trouvée à côté de ce script, la sortie est relative au dossier courant)
# Exemple : test/shot.sh "theme=riso&vue=1&temps=3" shots/riso-nuit.png
# Captures stables (sans animation, rendu fini) : ajouter en 3e et 4e arguments
#   --virtual-time-budget=4000 --force-prefers-reduced-motion   (et lite=0 dans la requête)
PAGE="$(cd "$(dirname "$0")/.." && pwd)/index.html"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1400,1000 "${@:3}" --screenshot="$2" "file://$PAGE?$1"

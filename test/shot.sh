#!/bin/bash
# Capture de la page en Chrome headless.
# Usage : test/shot.sh "<requête sans ?>" <sortie.png>   (depuis la racine du dépôt)
# Exemple : test/shot.sh "theme=riso&vue=1&temps=3" shots/riso-nuit.png
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1400,1000 --screenshot="$2" "file://$PWD/index.html?$1"

#!/usr/bin/env python3
# Générateur des tracés de la vue « Dehors » de index.html (Task 4).
# Outil de dessin, PAS livré : index.html reste le seul fichier livré.
#
# Les formes sont des points d'ancrage écrits à la main, lissés en courbes
# (mêmes règles que tools/gen-tete.py : relatif, 1 décimale, chaque point
# arrondi AVANT l'écart). Le script remplace le contenu de
# <g id="g-dehors"> dans index.html par GABARIT (en bas du fichier), où chaque
# {{nom}} reçoit un tracé.
#
# Usage (depuis la racine du dépôt) :
#   (même venv que tools/gen-tete.py : la calotte de cheveux reprend la tête H)
#   /tmp/venv/bin/python tools/gen-dehors.py          # réécrit #g-dehors
#   /tmp/venv/bin/python tools/gen-dehors.py --sec    # n'écrit rien, affiche les octets
import contextlib, importlib.util, io, math, os, re, sys
from shapely.geometry import Polygon, LineString

# la géométrie de la tête vient de tools/gen-tete.py (chargé sans rien écrire)
_spec = importlib.util.spec_from_file_location(
    "gen_tete", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen-tete.py"))
T = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stderr(io.StringIO()):
    _spec.loader.exec_module(T)

def f(v):
    """Nombre court : 1 décimale au plus, sans zéro de tête (.5, -.5)."""
    s = f"{round(v, 1):.1f}"
    if s.endswith('.0'): s = s[:-2]
    if s.startswith('0.'): s = s[1:]
    elif s.startswith('-0.'): s = '-' + s[2:]
    return '0' if s in ('-0', '') else s

def nums(vals):
    """Nombres SVG compacts : pas de séparateur devant « - », ni devant « .5 »
    quand le nombre précédent a déjà sa virgule (« 1.2.5 » = 1.2 puis .5)."""
    out, prev = '', None
    for v in vals:
        t = f(v)
        if prev is not None and not t.startswith('-') and not (t.startswith('.') and '.' in prev):
            out += ' '
        out += t
        prev = t
    return out

R1 = lambda q: (round(q[0], 1), round(q[1], 1))

def smooth(pts, closed=True, tail=''):
    """Courbe lisse par pts (tangentes Catmull-Rom bornées par la corde), en relatif.
    Ouverte : `tail` (ex. « V560H0Z ») ferme la forme par des segments droits."""
    n = len(pts)
    P = (lambda i: pts[i % n]) if closed else (lambda i: pts[max(0, min(n-1, i))])
    cur = R1(pts[0]); out = "M" + nums(cur) + "c"; vals = []
    for i in range(n if closed else n-1):
        p0, p1, p2, p3 = P(i-1), P(i), P(i+1), P(i+2)
        k = math.dist(p1, p2) / 3
        def tang(a, b):
            l = math.dist(a, b) or 1
            return ((b[0]-a[0])/l, (b[1]-a[1])/l)
        t1, t2 = tang(p0, p2), tang(p1, p3)
        c1 = R1((p1[0]+t1[0]*k, p1[1]+t1[1]*k)); c2 = R1((p2[0]-t2[0]*k, p2[1]-t2[1]*k)); e = R1(p2)
        vals += [c1[0]-cur[0], c1[1]-cur[1], c2[0]-cur[0], c2[1]-cur[1], e[0]-cur[0], e[1]-cur[1]]
        cur = e
    return out + nums(vals) + ("Z" if closed else tail)

def rrect(x0, y0, x1, y1, r):
    """Rectangle aux coins arrondis (arcs), en relatif."""
    w, h = x1-x0-2*r, y1-y0-2*r
    a = f"a{nums([r, r])} 0 0 1 "
    H = lambda d: f"h{f(d)}" if round(d, 1) else ""        # pas de segment nul
    V = lambda d: f"v{f(d)}" if round(d, 1) else ""
    return (f"M{nums([x0+r, y0])}{H(w)}{a}{nums([r, r])}{V(h)}{a}{nums([-r, r])}"
            f"{H(-w)}{a}{nums([-r, -r])}{V(-h)}{a}{nums([r, -r])}Z")

def rect(x0, y0, x1, y1):
    return f"M{nums([x0, y0])}h{f(x1-x0)}v{f(y1-y0)}h{f(x0-x1)}Z"

def polar(cx, cy, radii, phase=0):
    """Fleur / soleil : un rayon par point, réparti sur le tour."""
    n = len(radii)
    return [(cx + r*math.cos(phase + 2*math.pi*i/n), cy + r*math.sin(phase + 2*math.pi*i/n))
            for i, r in enumerate(radii)]

def crescent(cx, cy, R, ang, r2):
    """Croissant ouvert vers la droite : grand arc du cercle (cx,cy,R) entre les
    angles ±ang (en passant par la gauche), retour par un arc de rayon r2."""
    a = math.radians(ang)
    A = (cx + R*math.cos(a), cy - R*math.sin(a)); B = (cx + R*math.cos(a), cy + R*math.sin(a))
    return (f"M{nums(R1(A))}A{nums([R, R])} 0 1 0 {nums(R1(B))}"
            f"A{nums([r2, r2])} 0 0 1 {nums(R1(A))}Z")

out = {}

# ---------------------------------------------------------------- l'enfant
# Dedans, les cheveux courts sont une BANDE autour du crâne (le cerveau remplit
# le reste). Dehors, sans cerveau, la tête paraissait chauve : une calotte pleine
# (la tête H au-dessus et derrière une ligne de cheveux qui passe au-dessus de
# l'oreille), posée SOUS la bande reprise par <use> (qui garde ses boucles).
HAIRLINE = [(480, 92), (452, 112), (414, 126), (378, 142), (350, 166), (332, 194), (318, 214),
            (298, 206), (276, 208), (260, 224), (254, 256), (248, 292), (236, 328), (214, 368)]
line = LineString(T.sample(HAIRLINE, closed=False, n=8))
wavy = []                                    # bord ondulé (±2,6 px), comme une découpe à la main
for i in range(int(line.length // 5) + 1):
    a, b = line.interpolate(i*5), line.interpolate(min(line.length, i*5 + 1))
    nx, ny = -(b.y - a.y), b.x - a.x; l = math.hypot(nx, ny) or 1
    w = 3.2 * math.sin(i * .95)
    wavy.append((a.x + nx/l*w, a.y + ny/l*w))
zone = Polygon(wavy + [(120, 430), (-40, 430), (-40, -40), (560, -40), (560, 80)])
calotte = T.rounded(T.unary_union([T.H.buffer(-1).intersection(zone), T.hair]).buffer(0), 2)
out['calotte'] = T.shape_path(calotte, .6)

# ---------------------------------------------------------------- le sol
# Une colline douce de bord à bord ; la boîte à souvenirs (y 470–550) la recouvrira.
SOL = [(-12, 404), (70, 396), (170, 404), (290, 398), (420, 404), (540, 394), (660, 400), (780, 392), (912, 398)]
out['sol'] = smooth(SOL, closed=False, tail="V572H-12Z")
# touffes d'herbe brodées (trois brins en éventail) et petites fleurs (nœuds)
TOUFFES = [(40, 430), (128, 452), (236, 424), (560, 428), (700, 446), (860, 424), (470, 456)]
# cinq brins qui s'ouvrent vers le haut, pointes recourbées vers l'extérieur
BRINS = [(-4, -4, -11, -10), (-2, -8, -6, -17), (0, -10, 1, -20), (2, -8, 7, -16), (4, -4, 12, -9)]
out['herbe'] = ' '.join(f"M{nums([x + i*2.2 - 4.4, y])}q{nums(b)}" for x, y in TOUFFES for i, b in enumerate(BRINS))

# ---------------------------------------------------------------- l'expo
# Un vieil entrepôt de feutre gris, avec un fronton au milieu et un drapeau.
out['expo'] = ("M578 212L668 211 672 194Q718 184 764 193L768 210 858 208Q861 306 857 404"
               "Q718 408 579 404Q575 308 578 212Z")
out['expo-toit'] = rrect(568, 200, 868, 214, 5)
out['expo-porte'] = "M700 406V372a18 18 0 0 1 36 0V406Z"
# fenêtres cousues (rectangles au point de tige) : rangée du haut, + deux hublots
out['expo-fen'] = ' '.join(rect(x, 226, x+26, 252) for x in (596, 636, 800, 838 - 0)) \
    + ' ' + rect(684, 202, 708, 220) + ' ' + rect(728, 202, 752, 220)
# street art : trois taches de peinture et un grand sourire peint
out['tache-1'] = smooth(polar(626, 318, [24, 19, 26, 20, 23, 18, 25, 21]))
out['tache-2'] = smooth(polar(816, 322, [22, 26, 19, 24, 20, 25, 18, 23], .3))
out['tache-3'] = smooth(polar(718, 300, [28, 27, 29, 27, 28, 27, 29, 27, 28, 27]))
out['graffiti'] = ("M700 302Q718 322 736 302 M708 288v4 M728 288v4 "
                   "M598 370l10-14 10 14 10-14 10 14 M786 366q10-16 20 0t20 0")

# ---------------------------------------------------------------- la fenêtre
# Coin haut gauche. Derrière le cadre : le ciel de nuit (vitre bleu nuit + lune +
# étoiles), puis PAR-DESSUS le ciel de jour (vitre bleu clair + soleil), que la
# nuit éteint. « Par la fenêtre, tu vois s'il fait jour ou nuit » (zone fenetre).
FX0, FY0, FX1, FY1 = 14, 14, 138, 178
out['vitre'] = rect(FX0+8, FY0+8, FX1-8, FY1-8)
out['cadre'] = rrect(FX0, FY0, FX1, FY1, 8) + rrect(FX0+12, FY0+12, FX1-12, FY1-12, 4)
out['rebord'] = rrect(FX0-8, FY1-6, FX1+8, FY1+6, 5)
out['rideau-g'] = smooth([(FX0+6, FY0+10), (FX0+34, FY0+10), (FX0+30, FY0+56), (FX0+22, FY0+92),
                          (FX0+30, FY0+134), (FX0+34, FY1-12), (FX0+6, FY1-12), (FX0+12, FY0+92)])
out['rideau-d'] = smooth([(FX1-6, FY0+10), (FX1-34, FY0+10), (FX1-30, FY0+56), (FX1-22, FY0+92),
                          (FX1-30, FY0+134), (FX1-34, FY1-12), (FX1-6, FY1-12), (FX1-12, FY0+92)])
# (un fil tout droit n'a pas de largeur de boîte : le filtre #thread l'efface ;
#  la tringle et la hampe sont donc de petites pièces de laine)
out['tringle'] = rrect(FX0-7, FY0+5, FX1+7, FY0+10, 2.5)
out['hampe'] = rrect(716, 148, 720.6, 190, 2.3)
SX, SY = 76, 82
out['soleil-rayons'] = smooth(polar(SX, SY, [31, 23] * 9))
out['soleil'] = smooth(polar(SX, SY, [19.5] * 10))
out['soleil-visage'] = (f"M{nums([SX-9, SY-3])}q3 3 6 0M{nums([SX+3, SY-3])}q3 3 6 0"
                        f"M{nums([SX-6, SY+6])}q6 6 12 0")
LX, LY = 80, 84
out['lune'] = crescent(LX, LY, 25, 58, 22)
# œil ouvert (point) / œil qui fait un clin (trait), sourire, sur le corps du croissant
out['lune-oeil'] = (LX-14, LY-5)
out['lune-clin'] = f"M{nums([LX-18, LY-5])}q4 3.5 8 0"
out['lune-sourire'] = f"M{nums([LX-18, LY+8])}q4 4.5 9 1"

# étoiles : croix brodée + nœud au centre ; dans la vitre et autour de la fenêtre
ETOILES = [(46, 42, 5), (112, 50, 4), (42, 140, 4), (104, 128, 5), (70, 154, 3.5),
           (178, 26, 5), (222, 52, 4), (160, 210, 4.5), (26, 214, 4), (250, 20, 3.5)]
out['etoiles-fil'] = ' '.join(f"M{nums([x-s, y])}h{f(2*s)}M{nums([x, y-s])}v{f(2*s)}" for x, y, s in ETOILES)
out['etoiles-noeuds'] = '\n'.join(f'                <circle cx="{f(x)}" cy="{f(y)}" r="1.9" fill="url(#knot)"/>' for x, y, s in ETOILES)

# ---------------------------------------------------------------- la lampe
# À gauche du lit, près de l'oreiller. Abat-jour, pied, et sa lueur à part
# (#p-lampe-lueur), pour qu'on puisse la faire respirer plus tard.
LPX, LPY = 70, 300          # centre de l'abat-jour
out['lueur'] = smooth(polar(LPX, LPY + 4, [60, 56, 61, 55, 59, 57, 60, 56, 61, 55]))
out['abat-jour'] = smooth([(LPX-20, LPY-22), (LPX, LPY-25), (LPX+20, LPY-22), (LPX+30, LPY+4),
                           (LPX+37, LPY+22), (LPX, LPY+26), (LPX-37, LPY+22), (LPX-30, LPY+4)])
out['pied'] = (f"M{nums([LPX-4, LPY+24])}h8l1 112c14 1 24 6 24 13h-58c0-7 10-12 24-13Z")
out['abat-jour-fil'] = f"M{nums([LPX-33, LPY+16])}Q{nums([LPX, LPY+21, LPX+33, LPY+16])}"

# ---------------------------------------------------------------- le lit
# L'enfant s'y couche en Task 7 : #g-enfant-dehors tourne de -80° autour du cou
# (359,440) et descend vers l'oreiller (voir NOTES.md, Task 4).
out['tete-lit'] = smooth([(132, 470), (130, 360), (136, 330), (150, 318), (164, 330), (170, 360), (170, 470)],
                         closed=False, tail="Z")
out['pied-lit'] = smooth([(720, 470), (720, 392), (731, 381), (742, 392), (742, 470)], closed=False, tail="Z")
out['matelas'] = rrect(150, 428, 730, 470, 9)
out['oreiller'] = smooth([(176, 404), (230, 392), (300, 394), (352, 404), (360, 428), (338, 446),
                          (270, 448), (196, 446), (172, 430)])
# la couverture, PAR-DESSUS l'enfant couché : elle borde le cou et bombe sur le corps
out['couverture'] = smooth([(392, 326), (450, 314), (530, 318), (610, 340), (680, 370), (716, 396),
                            (720, 472), (396, 472), (386, 400)])
out['revers'] = smooth([(392, 326), (450, 314), (530, 318), (534, 338), (452, 334), (396, 346)])
out['couverture-fil'] = ("M440 360c40 6 80 6 120 4 M430 410c60 6 130 6 190 2 M500 352c-4 40-4 80 0 116 "
                         "M610 362c-4 34-4 70 0 106")

# ---------------------------------------------------------------- le doudou
# Un petit lapin assis sur la couverture, contre l'enfant.
DX, DY = 560, 304           # centre de la tête du lapin
out['doudou-oreilles'] = (smooth([(DX-9, DY-12), (DX-16, DY-36), (DX-11, DY-46), (DX-4, DY-36), (DX-2, DY-12)]) +
                          smooth([(DX+3, DY-12), (DX+8, DY-38), (DX+15, DY-44), (DX+16, DY-32), (DX+10, DY-10)]))
out['doudou'] = smooth([(DX, DY-16), (DX+15, DY-10), (DX+16, DY+4), (DX+10, DY+14), (DX+20, DY+26), (DX+18, DY+42),
                        (DX, DY+46), (DX-18, DY+42), (DX-20, DY+26), (DX-10, DY+14), (DX-16, DY+4), (DX-15, DY-10)])
out['doudou-fil'] = f"M{nums([DX-9, DY])}q3 2.5 6 0M{nums([DX+3, DY])}q3 2.5 6 0M{nums([DX-3, DY+7])}q3 2.5 6 0"
out['doudou-nez'] = (DX, DY + 5)

# ---------------------------------------------------------------- gabarit SVG
GABARIT = r"""
            <!-- Le monde de l'enfant, de jour et de nuit. data-jour / data-nuit :
                 Task 7 pilote leur opacité avec le temps. Les éléments sans
                 attribut (sol, fenêtre, ciel de nuit, enfant) restent toujours.
                 Tracés générés par tools/gen-dehors.py (NOTES.md, Task 4). -->

            <!-- le sol : une colline douce, que la boîte à souvenirs recouvre en bas -->
            <path id="p-sol" class="w" style="--p:var(--p-sol)" data-ink="bleu" d="{{sol}}"/>
            <path class="fil herbe" d="{{herbe}}"/>

            <!-- le bâtiment de l'expo de street art : feutre gris, fenêtres cousues, peintures -->
            <g id="p-expo" data-jour="1">
              <path class="w pale" style="--p:var(--p-expo)" data-ink="bleu" d="{{expo}}"/>
              <path class="w lite teinte" style="--p:var(--p-expo-toit)" data-ink="bleu" d="{{expo-toit}}"/>
              <path class="w lite teinte" style="--p:var(--p-expo-toit)" data-ink="bleu" d="{{expo-porte}}"/>
              <path class="w lite" style="--p:var(--p-graffiti-1)" data-ink="rose" d="{{tache-1}}"/>
              <path class="w lite teinte" style="--p:var(--p-graffiti-2)" data-ink="bleu" d="{{tache-2}}"/>
              <path class="w lite" style="--p:var(--p-soleil)" data-ink="jaune" d="{{tache-3}}"/>
              <path class="fil" d="{{expo-fen}}"/>
              <path class="fil graffiti" d="{{graffiti}}"/>
              <path class="w lite" style="--p:var(--p-lit)" data-ink="rose" d="{{hampe}}"/>
              <path class="w lite" style="--p:var(--fil-rouge)" data-ink="rose" d="M719 150l28 8-28 9Z"/>
            </g>

            <!-- la fenêtre de la chambre, en haut à gauche : derrière le cadre, le ciel
                 de nuit (toujours là), puis le ciel de jour posé dessus -->
            <g id="p-ciel-lune">
              <path class="w teinte" style="--p:var(--p-ciel-nuit)" data-ink="bleu" d="{{vitre}}"/>
              <!-- la lune : #g-lune l'enveloppe (clin d'œil, Task 7 / 18) ;
                   #fil-lune-clin, caché, remplacera #fil-lune-oeil le temps du clin -->
              <g id="g-lune">
                <g id="p-lune" data-nuit="1">
                  <path class="w reserve" style="--p:var(--p-lune)" data-ink="jaune" d="{{lune}}"/>
                  <circle id="fil-lune-oeil" class="oeil-lune" cx="{{lune-oeil-x}}" cy="{{lune-oeil-y}}" r="2.2"/>
                  <path id="fil-lune-clin" class="fil" style="--f:var(--fil-brun)" d="{{lune-clin}}"/>
                  <path class="fil" style="--f:var(--fil-brun)" d="{{lune-sourire}}"/>
                </g>
              </g>
              <!-- les étoiles : une croix brodée et un nœud français -->
              <g id="g-etoiles" data-nuit="1">
                <path class="fil etoile" d="{{etoiles-fil}}"/>
{{etoiles-noeuds}}
              </g>
            </g>
            <g id="p-ciel-soleil" data-jour="1">
              <path class="w pale" style="--p:var(--p-ciel-jour)" data-ink="bleu" d="{{vitre}}"/>
              <path class="w reserve" style="--p:var(--p-soleil-rayons)" data-ink="rose" d="{{soleil-rayons}}"/>
              <path class="w lite reserve" style="--p:var(--p-soleil)" data-ink="jaune" d="{{soleil}}"/>
              <path class="fil" style="--f:var(--fil-brun)" d="{{soleil-visage}}"/>
            </g>
            <g id="p-fenetre">
              <path class="w" style="--p:var(--p-fenetre)" data-ink="jaune" fill-rule="evenodd" d="{{cadre}}"/>
              <path class="w lite" style="--p:var(--p-lit)" data-ink="rose" d="{{tringle}}"/>
              <path class="w lite" style="--p:var(--p-rideau)" data-ink="rose" d="{{rideau-g}}"/>
              <path class="w lite" style="--p:var(--p-rideau)" data-ink="rose" d="{{rideau-d}}"/>
              <path class="w lite" style="--p:var(--p-fenetre)" data-ink="jaune" d="{{rebord}}"/>
            </g>

            <!-- Emplacements du décor des cartes (Task 8 y insère <use href="#d-slug">) :
                 groupes vides, rien ne s'y voit tant qu'aucune carte n'est choisie.
                 #slot-gens : les cartes « gens », à gauche de l'enfant. -->
            <g id="slot-0" transform="translate(600,330)"></g>
            <g id="slot-1" transform="translate(700,300)"></g>
            <g id="slot-2" transform="translate(780,350)"></g>
            <g id="slot-3" transform="translate(640,420)"></g>
            <g id="slot-gens" transform="translate(120,380)"></g>

            <!-- la lampe de chevet et sa lueur (pièce à part) -->
            <g id="p-lampe" data-nuit="1">
              <path id="p-lampe-lueur" class="w lite" style="--p:var(--p-lueur)" data-ink="jaune" d="{{lueur}}"/>
              <path class="w lite" style="--p:var(--p-lit)" data-ink="rose" d="{{pied}}"/>
              <path class="w" style="--p:var(--p-lampe)" data-ink="rose" d="{{abat-jour}}"/>
              <path class="fil" d="{{abat-jour-fil}}"/>
            </g>

            <!-- le lit (sous l'enfant) : tête de lit, pied, matelas, oreiller -->
            <g id="p-lit" data-nuit="1">
              <path class="w" style="--p:var(--p-lit)" data-ink="rose" d="{{tete-lit}}"/>
              <path class="w" style="--p:var(--p-lit)" data-ink="rose" d="{{pied-lit}}"/>
              <path class="w pale" style="--p:var(--p-drap)" data-ink="jaune" d="{{matelas}}"/>
              <path class="w pale" style="--p:var(--p-oreiller)" data-ink="jaune" d="{{oreiller}}"/>
            </g>

            <!-- l'enfant : la MÊME tête que Dedans, reprise par <use> (avatar, genre,
                 paupière, sourcil suivent tout seuls). Pivot au cou (359,440) :
                 Task 7 le couche par une transform CSS sur ce groupe. -->
            <g id="g-enfant-dehors">
              <use href="#p-cheveux-long"/>
              <use href="#p-tete"/>
              <path id="p-calotte" class="w cheveux reserve" style="--p:var(--hair)" data-ink="bleu" d="{{calotte}}"/>
              <use href="#g-cheveux"/>
              <use href="#g-oreille"/>
              <use href="#g-visage"/>
            </g>

            <!-- la couverture, PAR-DESSUS l'enfant couché (elle le borde) -->
            <g id="p-couverture" data-nuit="1">
              <path class="w teinte" style="--p:var(--p-couverture)" data-ink="bleu" d="{{couverture}}"/>
              <path class="w lite pale" style="--p:var(--p-drap)" data-ink="jaune" d="{{revers}}"/>
              <path class="fil couture" d="{{couverture-fil}}"/>
            </g>

            <!-- le doudou : un petit lapin assis contre l'enfant -->
            <g id="p-doudou" data-nuit="1">
              <path class="w lite pale" style="--p:var(--p-doudou)" data-ink="rose" d="{{doudou-oreilles}}"/>
              <path class="w pale" style="--p:var(--p-doudou)" data-ink="rose" d="{{doudou}}"/>
              <path class="fil" style="--f:var(--fil-brun)" d="{{doudou-fil}}"/>
              <circle class="nez-doudou" cx="{{doudou-nez-x}}" cy="{{doudou-nez-y}}" r="2"/>
            </g>
"""

for k in ('lune-oeil', 'doudou-nez'):
    x, y = out.pop(k)
    out[k + '-x'], out[k + '-y'] = f(x), f(y)

if __name__ == "__main__":
    frag = re.sub(r"\{\{([\w-]+)\}\}", lambda m: out[m.group(1)], GABARIT)
    taille = sum(len(m) for m in re.findall(r' d="([^"]*)"', frag))
    print(f"données de tracé (attributs d) : {taille} octets", file=sys.stderr)
    if "--sec" not in sys.argv:
        idx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
        html = open(idx, encoding="utf-8").read()
        a = html.index('<g id="g-dehors">') + len('<g id="g-dehors">')
        b = html.index('</g>\n          <!-- ===== Vue « Dedans »', a)
        html = html[:a] + frag.rstrip() + '\n          ' + html[b:]
        open(idx, "w", encoding="utf-8").write(html)

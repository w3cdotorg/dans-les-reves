#!/usr/bin/env python3
# Générateur des tracés de la vue « Tout près » de index.html (Task 5).
# Outil de dessin, PAS livré : index.html reste le seul fichier livré.
#
# Les neurones sont un corps (ellipse un peu bosselée) et quelques grosses
# dendrites effilées (tubes = enveloppes convexes de cercles successifs, comme
# dans gen-tete.py), réunis par shapely puis « fermés » (buffer + / −) pour que
# les branches sortent du corps par un congé doux. Les fines dendrites, l'axone
# et tout le reste sont de la broderie (.fil) écrite en tracés ouverts.
# Le script remplace le contenu de <g id="g-pres"> dans index.html par GABARIT
# (en bas du fichier), où chaque {{nom}} reçoit un tracé.
#
# Usage (depuis la racine du dépôt) :
#   créer le venv comme l'indique l'en-tête de tools/gen-tete.py, puis
#   <venv>/bin/python tools/gen-pres.py          # réécrit #g-pres
#   <venv>/bin/python tools/gen-pres.py --sec    # n'écrit rien, affiche les octets
import contextlib, importlib.util, io, math, os, random, re, sys
from shapely.geometry import Point
from shapely.ops import unary_union

# helpers de tracé (smooth_path, shape_path, tube, ellipse, f, nums) : ceux de gen-tete.py
_spec = importlib.util.spec_from_file_location(
    "gen_tete", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen-tete.py"))
T = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stderr(io.StringIO()):
    _spec.loader.exec_module(T)
f, nums, smooth_path, shape_path, tube, ellipse = T.f, T.nums, T.smooth_path, T.shape_path, T.tube, T.ellipse

out = {}

def rad(a): return math.radians(a)
def pol(c, a, d): return (c[0] + d*math.cos(rad(a)), c[1] + d*math.sin(rad(a)))

def curve(p0, a0, length, bend, n=8):
    """Points d'une branche qui part de p0 dans la direction a0 (degrés) et tourne
    de `bend` degrés au total, régulièrement, sur `length` px."""
    pts, p, a = [p0], p0, a0
    step = length / n
    for _ in range(n):
        a += bend / n
        p = pol(p, a, step)
        pts.append(p)
    return pts, a

def open_path(pts):
    return smooth_path([(round(x, 1), round(y, 1)) for x, y in pts], closed=False)

# ---------------------------------------------------------------- les neurones
# (centre, rayons du corps, rotation, branches) ; branche = (angle, longueur en
# laine, courbure, longueur brodée en plus). Une branche « vers » une étincelle
# porte la cible : son prolongement brodé finit à 7 px de l'étincelle.
SYN = {   # les étincelles (synapses), entre l'axone d'un neurone et la dendrite d'un autre
    's1': (262, 96),    # N1 → N2
    's2': (532, 118),   # N2 → N3
    's3': (742, 262),   # N3 → N4
    's4': (428, 352),   # N6 → N5
    's5': (196, 396),   # N7 → N6
}
NEURONES = [
    # id, centre, rx, ry, rot, branches, axone (cible, courbure)
    (1, (138, 132), 25, 21, -20,
        [(200, 34, 25, 30), (250, 30, -30, 26), (140, 36, 20, 28), (95, 30, -20, 30)],
        ('s1', 10)),
    (2, (398, 92), 23, 20, 10,
        [(160, 32, 20, 'ss1'), (230, 28, 25, 24), (300, 30, -20, 22), (110, 30, -25, 28)],
        ('s2', -18)),
    (3, (652, 150), 26, 22, 25,
        [(180, 34, -20, 'ss2'), (260, 30, 25, 26), (320, 32, -25, 28), (120, 30, 20, 26)],
        ('s3', 16)),
    (4, (792, 350), 23, 21, -10,
        [(250, 32, 20, 'ss3'), (320, 30, -20, 22), (190, 30, -25, 26), (130, 30, 25, 24)],
        None),
    (5, (565, 378), 25, 21, 15,
        [(185, 34, 15, 'ss4'), (250, 30, -25, 26), (300, 30, 20, 24), (120, 28, -20, 26), (40, 30, 20, 24)],
        None),
    (6, (292, 312), 24, 21, -30,
        [(160, 32, -20, 'ss5'), (240, 30, 20, 26), (290, 28, -25, 22), (100, 30, 20, 28)],
        ('s4', 20)),
    (7, (112, 452), 22, 19, 20,
        [(150, 30, 20, 24), (210, 28, -25, 22), (100, 28, 25, 24), (260, 28, -20, 20)],
        ('s5', -20)),
]
rng = random.Random(5)

def neurone(n, c, rx, ry, rot, branches, axone):
    soma = ellipse(c[0], c[1], rx, ry, rot)
    parts = [soma]
    fils = []
    for a, L, bend, extra in branches:
        start = pol(c, a, min(rx, ry) * .55)
        if isinstance(extra, str):                  # dendrite tendue vers une étincelle
            s = SYN[extra[1:]]
            a = math.degrees(math.atan2(s[1] - c[1], s[0] - c[0]))
            start = pol(c, a, min(rx, ry) * .55)
            bend = bend * .4
        pts, a_end = curve(start, a, L + min(rx, ry) * .5, bend)
        rs = [6.2 - 3.9 * i / (len(pts) - 1) for i in range(len(pts))]
        parts.append(tube([(x, y, r) for (x, y), r in zip(pts, rs)]))
        tip = pts[-1]
        if isinstance(extra, str):
            s = SYN[extra[1:]]
            d = math.dist(tip, s)
            u = ((s[0] - tip[0]) / d, (s[1] - tip[1]) / d)
            end = (s[0] - u[0] * 8, s[1] - u[1] * 8)
            mid = ((tip[0] + end[0]) / 2 + u[1] * 4, (tip[1] + end[1]) / 2 - u[0] * 4)
            fils.append(open_path([pol(tip, a_end + 180, 3), mid, end]))
            # une petite fourche qui part du milieu
            fk, _ = curve(mid, math.degrees(math.atan2(u[1], u[0])) + 38, 12, 10, n=3)
            fils.append(open_path(fk))
        else:
            # le prolongement brodé : un tronc puis une fourche en Y
            p1, a1 = curve(pol(tip, a_end + 180, 3), a_end, extra * .55, bend * .5, n=4)
            fils.append(open_path(p1))
            for da in (-24, 22):
                p2, _ = curve(p1[-1], a1 + da, extra * .48, da * .9, n=4)
                fils.append(open_path(p2))
    g = unary_union(parts).buffer(3.2, 24).buffer(-3.2, 24)
    out[f'n{n}'] = shape_path(g, tol=.35)
    out[f'n{n}-fils'] = ' '.join(fils)
    # noyau : un nœud français, un peu décentré vers le haut-gauche
    k = pol(c, 215, 4)
    out[f'n{n}-kx'], out[f'n{n}-ky'] = f(k[0]), f(k[1])
    # l'axone : une broderie plus épaisse qui part du corps et finit en bouton
    if axone:
        s = SYN[axone[0]]
        a = math.degrees(math.atan2(s[1] - c[1], s[0] - c[0]))
        p0 = pol(c, a - axone[1] * .6, max(rx, ry) - 2)
        d = math.dist(p0, s)
        u = ((s[0] - p0[0]) / d, (s[1] - p0[1]) / d)
        end = (s[0] - u[0] * 8, s[1] - u[1] * 8)
        k = axone[1] / 40
        m1 = (p0[0] + (end[0] - p0[0]) * .33 - u[1] * d * k, p0[1] + (end[1] - p0[1]) * .33 + u[0] * d * k)
        m2 = (p0[0] + (end[0] - p0[0]) * .7 - u[1] * d * k * .5, p0[1] + (end[1] - p0[1]) * .7 + u[0] * d * k * .5)
        out[f'n{n}-axone'] = open_path([p0, m1, m2, end])
        out[f'n{n}-bx'], out[f'n{n}-by'] = f(end[0]), f(end[1])

for spec in NEURONES:
    neurone(*spec)

# ---------------------------------------------------------------- les étincelles
def etincelle(s, r0=7.5, r1=15, n=8, a0=0):
    segs = []
    for i in range(n):
        a = a0 + i * 360 / n
        p, q = pol(s, a, r0), pol(s, a, r1 if i % 2 == 0 else r1 - 3)
        segs.append(f"M{nums(p)}L{nums(q)}")
    return ''.join(segs)
for k, s in SYN.items():
    out[k] = etincelle(s, a0=rng.uniform(0, 60))
    out[k + '-x'], out[k + '-y'] = f(s[0]), f(s[1])

# ---------------------------------------------------------------- les grandes vagues lentes
# Une sinusoïde de période P, de x = −2P à 900 + P : le groupe glisse de 0 à +P
# (gauche → droite) puis reprend, sans saut.
P = 300
def vague(y0, amp, phase):
    pts = []
    x = -2 * P
    while x <= 900 + P + 1:
        pts.append((x, y0 + amp * math.sin(2 * math.pi * (x / P) + phase)))
        x += P / 8
    return open_path(pts)
for i, (y0, amp, ph) in enumerate([(178, 15, 0), (282, 13, 2.2), (452, 16, 4.1)], 1):
    out[f'v{i}'] = vague(y0, amp, ph)
    out[f'v{i}-a'] = vague(y0 - 8, amp, ph)
    out[f'v{i}-b'] = vague(y0 + 8, amp, ph)

# ---------------------------------------------------------------- les petites rafales (fuseaux)
# Un zigzag rapide dont l'amplitude enfle puis retombe : la forme d'un fuseau.
def fuseau(c, L=74, amp=11, n=15, rot=0):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = -L / 2 + L * t
        y = (amp * math.sin(math.pi * t) ** 1.4) * (1 if i % 2 else -1)
        a = rad(rot)
        pts.append((c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)))
    return 'M' + ' '.join(nums(p) for p in pts)
# Les fuseaux sont posés sur les crêtes des vagues 1 et 3 (comme dans le sommeil
# profond, où les fuseaux arrivent sur la crête des ondes lentes) et glissent avec
# elles : crête de la vague (y0, amp, phase) en x = P·(3π/2 − phase)/2π (+ k·P).
def crete(y0, amp, ph, k):
    x = P * ((1.5 * math.pi - ph) % (2 * math.pi)) / (2 * math.pi) + k * P
    return (x, y0 - amp)
for i, c in enumerate([crete(178, 15, 0, 0), crete(452, 16, 4.1, 1), crete(452, 16, 4.1, 2)], 1):
    out[f'f{i}'] = fuseau(c)

# ---------------------------------------------------------------- le rinçage
def goutte(c, s=1.0):
    x, y = c
    pts = [(x, y - 13 * s), (x + 5.6 * s, y - 2 * s), (x + 7.2 * s, y + 4.5 * s), (x, y + 10.5 * s),
           (x - 7.2 * s, y + 4.5 * s), (x - 5.6 * s, y - 2 * s)]
    return smooth_path([(round(a, 1), round(b, 1)) for a, b in pts])
GOUTTES = [((478, 52), 1.4), ((694, 512), 1.3), ((52, 300), 1.35), ((800, 74), 1.25)]
for i, (c, s) in enumerate(GOUTTES, 1):
    out[f'g{i}'] = goutte(c, s)
    x, y = c
    # le sillage : deux petits points de piqûre au-dessus de la goutte
    out[f'g{i}-sillage'] = f"M{nums((x - 3 * s, y - 20 * s))}L{nums((x - 3 * s, y - 27 * s))}M{nums((x + 3 * s, y - 22 * s))}L{nums((x + 3 * s, y - 33 * s))}"
    hx, hy = x - 2.4 * s, y + 2 * s
    out[f'g{i}-hx'], out[f'g{i}-hy'] = f(hx), f(hy)

# ---------------------------------------------------------------- la cellule qui grandit
CEL = (430, 478)
cell = ellipse(CEL[0], CEL[1], 37, 33, -8)
bud = ellipse(CEL[0] + 38, CEL[1] - 14, 15, 13, 20)
out['cellule'] = shape_path(unary_union([cell, bud]).buffer(4, 24).buffer(-4, 24), tol=.35)
out['cellule-noyau'] = shape_path(ellipse(CEL[0] - 7, CEL[1] + 2, 13.5, 12, 15), tol=.3)
out['cellule-bourgeon'] = shape_path(ellipse(CEL[0] + 39, CEL[1] - 14, 6, 5.2, 20), tol=.3)
out['cellule-cx'], out['cellule-cy'] = f(CEL[0] + 6), f(CEL[1] - 3)

# ---------------------------------------------------------------- les plis du cortex, vus de tout près
def volute(pts, sens=1):
    """Un pli : une courbe qui finit en petite spirale, et le nœud au bout."""
    a = math.degrees(math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0]))
    p, spi = pts[-1], []
    for i in range(1, 9):
        a += sens * 40
        p = pol(p, a, 9 - i * .8)
        spi.append(p)
    return open_path(pts + spi), spi[-1]
PLIS = [([(-10, 236), (70, 218), (150, 246), (214, 226)], 1),
        ([(232, 570), (286, 528), (262, 486)], -1),
        ([(910, 528), (820, 520), (760, 540)], 1)]
vol = [volute(pts, sens) for pts, sens in PLIS]
out['plis'] = ' '.join(v[0] for v in vol)
out['plis-noeuds'] = '\n'.join(f'              <circle cx="{f(q[0])}" cy="{f(q[1])}" r="2.3"/>' for _, q in vol)
# des milliards d'autres neurones, très loin : des nœuds minuscules
LOIN = []
for _ in range(400):
    if len(LOIN) >= 26: break
    p = (rng.uniform(15, 885), rng.uniform(15, 545))
    if all(math.dist(p, s[1]) > 60 for s in NEURONES) and all(math.dist(p, q) > 55 for q in LOIN) \
       and math.dist(p, CEL) > 70:
        LOIN.append(p)
out['loin'] = '\n'.join(f'              <circle cx="{f(x)}" cy="{f(y)}" r="{f(rng.uniform(1.3, 2.1))}"/>' for x, y in LOIN)

GABARIT = r"""
            <!-- Tout près : à l'intérieur du cerveau, à hauteur de neurones (spec §4.1, vue 3).
                 Tracés générés par tools/gen-pres.py (NOTES.md, Task 5). data-phase : Task 7
                 en pilote l'opacité (synapses = le jour et les rêves ; nuit = le sommeil profond).
                 Animations : section 7 quinquies du CSS, sur des <g> enveloppes, jamais sur un .w. -->
            <defs>
              <!-- nœud français jaune (étincelles) : le dégradé lit les jetons de laine -->
              <radialGradient id="knotJaune" cx="35%" cy="32%" r="65%"><stop offset="0" style="stop-color:var(--fil-etincelle)"/><stop offset=".6" style="stop-color:var(--p-etincelle)"/><stop offset="1" style="stop-color:var(--p-etincelle-ombre)"/></radialGradient>
            </defs>
            <!-- le fond : laine rose pâle plein cadre (le cortex vu de tout près), sur une
                 sous-couche unie qui garde la vue opaque même là où l'encre riso est mince -->
            <rect class="sous-pres" x="-20" y="-20" width="940" height="600"/>
            <path id="p-fond-pres" class="w lite reserve voile" style="--p:var(--p-pres-fond)" data-ink="rose" d="M-20-20H920V580H-20Z"/>
            <rect class="toile-grain" x="-20" y="-20" width="940" height="600"/>
            <path class="fil pli-pres" d="{{plis}}"/>
            <g class="loin" fill="url(#knot)">
{{plis-noeuds}}
            </g>
            <g class="loin" fill="url(#knot)">
{{loin}}
            </g>

            <!-- les grandes vagues lentes : trois larges bandes brodées qui glissent de gauche à droite -->
            <g id="g-vagues" data-phase="nuit">
              <g class="glisse glisse-1">
                <path class="bande" d="{{v1}}"/>
                <path class="fil vague" d="{{v1-a}} {{v1-b}}"/>
                <path class="bande" d="{{v3}}"/>
                <path class="fil vague" d="{{v3-a}} {{v3-b}}"/>
              </g>
              <g class="glisse glisse-2">
                <path class="bande" d="{{v2}}"/>
                <path class="fil vague" d="{{v2-a}} {{v2-b}}"/>
              </g>
            </g>

            <!-- les petites rafales qui collent (fuseaux) : de petits traits blancs, très rapides,
                 posés sur les crêtes des vagues 1 et 3 ; leur enveloppe glisse avec elles
                 (même animation que .glisse-1) -->
            <g id="g-fuseaux" data-phase="nuit">
              <g class="glisse glisse-1">
                <path class="fil fuseau rafale rafale-1" d="{{f1}}"/>
                <path class="fil fuseau rafale rafale-2" d="{{f2}}"/>
                <path class="fil fuseau rafale rafale-3" d="{{f3}}"/>
              </g>
            </g>

            <!-- le rinçage : des gouttes bleu pâle qui descendent doucement -->
            <g id="g-rincage" data-phase="nuit">
              <g class="descend descend-1">
                <path class="fil sillage" d="{{g1-sillage}} {{g3-sillage}}"/>
                <path class="papier-pres" d="{{g1}}"/>
                <path class="w lite pale" style="--p:var(--p-rincage)" data-ink="bleu" d="{{g1}}"/>
                <path class="papier-pres" d="{{g3}}"/>
                <path class="w lite pale" style="--p:var(--p-rincage)" data-ink="bleu" d="{{g3}}"/>
                <circle class="reflet" cx="{{g1-hx}}" cy="{{g1-hy}}" r="1.6"/>
                <circle class="reflet" cx="{{g3-hx}}" cy="{{g3-hy}}" r="1.6"/>
              </g>
              <g class="descend descend-2">
                <path class="fil sillage" d="{{g2-sillage}} {{g4-sillage}}"/>
                <path class="papier-pres" d="{{g2}}"/>
                <path class="w lite pale" style="--p:var(--p-rincage)" data-ink="bleu" d="{{g2}}"/>
                <path class="papier-pres" d="{{g4}}"/>
                <path class="w lite pale" style="--p:var(--p-rincage)" data-ink="bleu" d="{{g4}}"/>
                <circle class="reflet" cx="{{g2-hx}}" cy="{{g2-hy}}" r="1.5"/>
                <circle class="reflet" cx="{{g4-hx}}" cy="{{g4-hy}}" r="1.4"/>
              </g>
            </g>

            <!-- les neurones : corps et grosses dendrites en laine, fines dendrites et axone brodés,
                 le noyau en nœud français, le bouton de l'axone au bord de l'étincelle -->
            <g id="g-neurones">
""" + ''.join(f"""              <g id="p-neurone-{n}" class="neurone{' lilas' if n % 2 == 0 else ''}">
                <path class="fil dendrite" d="{{{{n{n}-fils}}}}"/>
""" + (f"""                <path class="fil couture axone" d="{{{{n{n}-axone}}}}"/>
                <circle class="bouton" cx="{{{{n{n}-bx}}}}" cy="{{{{n{n}-by}}}}" r="3.6"/>
""" if spec[6] else '') + f"""                <path class="w" style="--p:var(--p-neurone{'-2' if n % 2 == 0 else ''})" data-ink="{'bleu' if n % 2 == 0 else 'rose'}" d="{{{{n{n}}}}}"/>
                <circle class="noyau" cx="{{{{n{n}-kx}}}}" cy="{{{{n{n}-ky}}}}" r="5.2" fill="url(#knot)"/>
              </g>
""" for n, *_rest in NEURONES for spec in [[n, *_rest]]) + r"""            </g>

            <!-- les étincelles (synapses) : là où deux neurones se touchent presque -->
            <g id="g-synapses" data-phase="synapses">
              <g class="clignote clignote-1">
                <path class="fil rayon" d="{{s1}} {{s4}}"/>
                <circle class="noeud-jaune" cx="{{s1-x}}" cy="{{s1-y}}" r="5.6"/>
                <circle class="noeud-jaune" cx="{{s4-x}}" cy="{{s4-y}}" r="5.6"/>
              </g>
              <g class="clignote clignote-2">
                <path class="fil rayon" d="{{s2}} {{s3}} {{s5}}"/>
                <circle class="noeud-jaune" cx="{{s2-x}}" cy="{{s2-y}}" r="5.6"/>
                <circle class="noeud-jaune" cx="{{s3-x}}" cy="{{s3-y}}" r="5.6"/>
                <circle class="noeud-jaune" cx="{{s5-x}}" cy="{{s5-y}}" r="5.6"/>
              </g>
              <!-- un message qui court le long de l'axone de N1 jusqu'à l'étincelle -->
              <path class="influx" pathLength="100" d="{{n1-axone}}"/>
            </g>

            <!-- la cellule qui grandit : elle bourgeonne, son anneau pulse -->
            <g id="p-cellule" data-phase="nuit">
              <g class="anneau"><circle class="fil couture anneau-fil" cx="{{cellule-cx}}" cy="{{cellule-cy}}" r="54"/></g>
              <path class="papier-pres" d="{{cellule}}"/>
              <path class="w reserve vert" style="--p:var(--p-cellule)" data-ink="jaune" d="{{cellule}}"/>
              <path class="w lite reserve vert-fonce" style="--p:var(--p-cellule-noyau)" data-ink="bleu" d="{{cellule-noyau}}"/>
              <path class="w lite reserve vert-fonce" style="--p:var(--p-cellule-noyau)" data-ink="bleu" d="{{cellule-bourgeon}}"/>
            </g>
"""

if __name__ == "__main__":
    frag = re.sub(r"\{\{([\w-]+)\}\}", lambda m: out[m.group(1)], GABARIT)
    taille = sum(len(m) for m in re.findall(r' d="([^"]*)"', frag))
    print(f"données de tracé (attributs d) : {taille} octets", file=sys.stderr)
    if "--sec" not in sys.argv:
        idx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
        html = open(idx, encoding="utf-8").read()
        a = html.index('<g id="g-pres">') + len('<g id="g-pres">')
        b = html.index('</g>\n          <!-- ===== Écran du rêve', a)
        html = html[:a] + frag.rstrip() + '\n          ' + html[b:]
        open(idx, "w", encoding="utf-8").write(html)

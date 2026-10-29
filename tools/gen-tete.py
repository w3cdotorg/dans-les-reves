#!/usr/bin/env python3
# Générateur des tracés de la vue « Dedans » de index.html (Task 3).
# Outil de dessin, PAS livré : index.html reste le seul fichier livré.
#
# Les formes sont décrites à la main par des points d'ancrage ; shapely ne sert
# qu'aux découpes (lobes), aux bandes (crâne, coussin d'eau, cheveux) et aux
# tubes effilés (hippocampe, nerf, corps calleux, tronc, moelle). Le script
# remplace le contenu de <g id="g-dedans"> dans index.html par GABARIT (en bas
# du fichier), où chaque {{nom}} reçoit un tracé lisse.
#
# Usage (depuis la racine du dépôt) :
#   python3 -m venv /tmp/venv && /tmp/venv/bin/pip install shapely
#   /tmp/venv/bin/python tools/gen-tete.py          # réécrit #g-dedans ; positions sur stderr
#   /tmp/venv/bin/python tools/gen-tete.py --sec    # n'écrit rien, affiche positions et octets
import math, re, sys
from shapely.geometry import Polygon, LineString, Point, MultiPolygon, box
from shapely.ops import split, unary_union
from shapely import affinity

def f(v):
    """Nombre court : 1 décimale au plus, sans zéro de tête (.5, -.5)."""
    s = f"{round(v, 1):.1f}"
    if s.endswith('.0'): s = s[:-2]
    if s.startswith('0.'): s = s[1:]
    elif s.startswith('-0.'): s = '-' + s[2:]
    return '0' if s in ('-0', '') else s

def nums(vals):
    """Liste de nombres SVG compacte : pas de séparateur devant un « - », ni devant
    « .5 » quand le nombre précédent a déjà sa virgule (« 1.2.5 » = 1.2 puis .5)."""
    out, prev = '', None
    for v in vals:
        t = f(v)
        if prev is not None and not t.startswith('-') and not (t.startswith('.') and '.' in prev):
            out += ' '
        out += t
        prev = t
    return out

def smooth_path(pts, closed=True):
    """Courbe lisse passant par pts (tangentes Catmull-Rom, longueurs bornées par
    la corde). Écrite en relatif (c) pour la compacité : chaque point absolu est
    arrondi au dixième AVANT le calcul de l'écart, donc pas d'erreur cumulée."""
    n = len(pts)
    def P(i):
        return pts[i % n] if closed else pts[max(0, min(n-1, i))]
    R = lambda q: (round(q[0], 1), round(q[1], 1))
    cur = R(pts[0])
    out = "M" + nums(cur) + "c"
    segs = n if closed else n-1
    vals = []
    for i in range(segs):
        p0, p1, p2, p3 = P(i-1), P(i), P(i+1), P(i+2)
        d = math.dist(p1, p2)
        def tang(a, b):
            l = math.dist(a, b) or 1
            return ((b[0]-a[0])/l, (b[1]-a[1])/l)
        t1 = tang(p0, p2) if (closed or i > 0) else tang(p1, p2)
        t2 = tang(p1, p3) if (closed or i < n-2) else tang(p1, p2)
        k = d/3
        c1 = R((p1[0]+t1[0]*k, p1[1]+t1[1]*k))
        c2 = R((p2[0]-t2[0]*k, p2[1]-t2[1]*k))
        e = R(p2)
        vals += [c1[0]-cur[0], c1[1]-cur[1], c2[0]-cur[0], c2[1]-cur[1], e[0]-cur[0], e[1]-cur[1]]
        cur = e
    out += nums(vals)
    if closed: out += "Z"
    return out

def sample(pts, closed=True, n=16):
    """Échantillonne la même courbe (Bézier) pour en faire un polygone shapely."""
    m = len(pts); res = []
    segs = m if closed else m-1
    def P(i):
        return pts[i % m] if closed else pts[max(0, min(m-1, i))]
    for i in range(segs):
        p0, p1, p2, p3 = P(i-1), P(i), P(i+1), P(i+2)
        d = math.dist(p1, p2)
        def tang(a, b):
            l = math.dist(a, b) or 1
            return ((b[0]-a[0])/l, (b[1]-a[1])/l)
        t1 = tang(p0, p2) if (closed or i > 0) else tang(p1, p2)
        t2 = tang(p1, p3) if (closed or i < m-2) else tang(p1, p2)
        k = d/3
        c1 = (p1[0]+t1[0]*k, p1[1]+t1[1]*k); c2 = (p2[0]-t2[0]*k, p2[1]-t2[1]*k)
        for j in range(n):
            t = j/n; u = 1-t
            res.append((u**3*p1[0]+3*u*u*t*c1[0]+3*u*t*t*c2[0]+t**3*p2[0],
                        u**3*p1[1]+3*u*u*t*c1[1]+3*u*t*t*c2[1]+t**3*p2[1]))
    if not closed: res.append(pts[-1])
    return res

def poly(pts):
    return Polygon(sample(pts)).buffer(0)

def biggest(g):
    if isinstance(g, MultiPolygon):
        return max(g.geoms, key=lambda p: p.area)
    return g

def shape_path(g, tol=.6):
    """Polygone shapely -> tracé lisse. simplify(tol) retire les sommets inutiles,
    puis on saute tout sommet à moins de 1,6 px du précédent (segments
    sous-pixel, invisibles sous la laine)."""
    g = biggest(g).simplify(tol)
    pts = list(g.exterior.coords)[:-1]
    keep = [pts[0]]
    for q in pts[1:]:
        if math.dist(q, keep[-1]) >= 1.6: keep.append(q)
    if len(keep) > 3 and math.dist(keep[-1], keep[0]) < 1.6: keep.pop()
    return smooth_path(keep)

def tube(centers):
    """Tube effilé : enveloppes convexes de cercles successifs (x, y, r)."""
    cs = [Point(x, y).buffer(r, 32) for x, y, r in centers]
    parts = [unary_union([cs[i], cs[i+1]]).convex_hull for i in range(len(cs)-1)]
    return unary_union(parts)

def ellipse(cx, cy, rx, ry, rot=0):
    e = affinity.scale(Point(0, 0).buffer(1, 48), rx, ry)
    e = affinity.rotate(e, rot, origin=(0, 0))
    return affinity.translate(e, cx, cy)

def rounded(g, r):
    return g.buffer(-r).buffer(r)

# ---------------------------------------------------------------- formes de base
# Tête (peau), de profil, regard vers la droite. Bout du nez (507,250), bouche (480,300).
H_PTS = [(304,575),(304,500),(304,452),(292,428),(262,410),(212,386),(176,346),(161,290),
         (162,226),(178,164),(214,108),(262,72),(320,55),(380,51),(440,58),(480,84),
         (497,122),(498,158),(490,182),(491,204),(500,226),(507,244),(505,256),(495,262),
         (488,272),(489,288),(484,299),(488,311),(482,324),(479,344),(470,364),(450,380),
         (428,387),(416,402),(414,452),(414,500),(414,575)]
# Cerveau (hémisphère vu de côté, avant à droite).
S_PTS = [(466,142),(462,164),(442,180),(428,200),(421,228),(431,240),(434,256),(424,278),
         (398,294),(360,300),(328,296),(306,284),(290,266),(266,252),(240,247),(216,242),
         (202,228),(199,192),(210,156),(238,120),(280,95),(330,86),(380,85),(424,96),(452,115)]
# Cervelet : corps ovale + bras (pédoncule) qui rejoint le tronc.
C_PTS = [(196,290),(206,268),(236,258),(266,263),(285,281),(300,292),(314,296),(315,306),
         (299,311),(282,316),(262,325),(236,327),(210,321),(198,306)]
# Oreille (conduit auditif en (300,250)).
E_PTS = [(304,222),(287,214),(271,223),(265,245),(269,267),(281,285),(292,295),(302,293),
         (305,283),(304,274),(310,266),(314,252),(313,236)]

H = poly(H_PTS); S = poly(S_PTS); C = poly(C_PTS)

# lobes : on découpe le cerveau par trois lignes (prolongées hors du cerveau)
# sillons central et pariéto-occipital : les ancres du plan, plus un point d'onde
# (±4 px) entre deux ancres, pour que les lobes ne ressemblent pas à des carreaux
OB = LineString(sample([(222,70),(240,116),(244.7,143.2),(257,168),(268.3,189.8),(272,214),(276.7,241.2),(289,266),(300,310)], closed=False))
SY = LineString(sample([(480,238),(421,231),(380,226),(320,218),(262,211),(190,204)], closed=False))
CS = LineString(sample([(316,50),(330,88),(334.7,114.3),(347,138),(359.7,159.5),(365,184),(368.7,206.3),(380,226),(392,270)], closed=False))

def side(geom, line, keep_pt):
    parts = split(geom, line)
    for p in parts.geoms:
        if p.contains(Point(keep_pt)): return p
    raise SystemExit(f"pas de morceau contenant {keep_pt}")

occ = side(S, OB, (215,200))
rest = side(S, OB, (380,150))
temp = side(rest, SY, (400,270))
upper = side(rest, SY, (380,150))
front = side(upper, CS, (430,150))
par = side(upper, CS, (300,150))

GAP = 2.4
def lobe(g): return rounded(g.buffer(-GAP), 3)

cortex = S.buffer(2.6)
tronc = tube([(320,243,9.5),(323,258,10),(330,276,12.5),(335,293,14),(332,309,11.5),(330,322,8.6),(330,334,7.8)])
liq = unary_union([S, C, tronc.intersection(box(0,0,900,330))]).buffer(14).buffer(-5)
# crâne : la bande entre la peau et le coussin d'eau, du sourcil jusque sous le cervelet
helmet_keep = Polygon([(540,-20),(540,180),(470,180),(440,186),(400,250),(318,322),(304,346),(250,350),(196,338),(110,306),(110,-20)])
crane = rounded(H.buffer(-7).difference(liq).intersection(helmet_keep), 2.5)
# cheveux courts : une calotte de laine sur le haut et l'arrière, bord ondulé,
# qui s'amincit vers la nuque ; trois mèches de frange sur le front.
cap_keep = Polygon([(620,-60),(620,40),(499,126),(330,300),(200,392),(80,470),(-60,470),(-60,-60)])
ring = H.exterior
blobs = []; strands = []
L = ring.length
s0 = None
for i in range(int(L//5)):
    sd = i*5
    p = ring.interpolate(sd)
    if not cap_keep.contains(p) or p.y > 392: continue
    if s0 is None: s0 = sd
    taper = max(0.0, min(1.0, (392 - p.y)/120))          # 1 en haut, 0 à la nuque
    r = 3 + taper*(8.5 + 2.4*math.sin((sd-s0)/31*2*math.pi))
    blobs.append(p.buffer(r, 20))
locks = [tube([(478,84,8),(491,106,5.4),(494,128,2)]), tube([(462,72,8),(477,96,5.2),(482,116,1.8)]),
         tube([(446,64,7),(458,84,4.2),(462,99,1.6)])]
hair = unary_union([unary_union(blobs).difference(H.buffer(-6)).intersection(cap_keep)] + locks)
hair = rounded(biggest(hair.buffer(0)), 1)
# fils de laine plus clairs qui suivent la calotte
inner = H.buffer(1.5).exterior
for k in range(40):
    sd = k*46
    seg = [inner.interpolate(sd + t) for t in (0, 15, 30)]
    if all(cap_keep.buffer(-12).contains(q) and q.y < 330 for q in seg):
        strands.append([(q.x, q.y) for q in seg])
# cheveux longs (fille) : rideau derrière la tête et le cou
HL_PTS = [(262,84),(206,108),(166,150),(144,220),(144,300),(150,380),(160,450),(170,490),
          (186,512),(206,520),(226,512),(246,524),(268,516),(290,524),(306,512),(312,470),
          (300,410),(262,380),(214,320),(214,200)]
hairlong = poly(HL_PTS)

# régions profondes
calleux = tube([(254,190,7.5),(262,178,6),(282,168,5),(310,162,4.6),(345,159,4.6),(380,161,4.8),
                (406,166,5.5),(421,177,6.4),(422,190,4.6),(414,197,2.6)])
thalamus = ellipse(335,200,23,14,-6)
hypoth = ellipse(347,222,11,7,8)
pineale = ellipse(300,196,7,5.6,-20)
hippo = unary_union([tube([(345,243,6.4),(336,238,5.6),(325,232,4.6),(314,226,3.8),(305,219,3.1),
                           (301,212,2.7),(303,206,2.5),(308,206,2.3),(309,211,2)]),
                     Point(347,239).buffer(6,24)])
amygdale = ellipse(356,248,6.6,4.8,-22)
hypophyse = unary_union([tube([(354,228,1.6),(362,238,1.5),(369,248,1.7)]), Point(371,253).buffer(4.4,24)])
nerf = unary_union([tube([(449,197,3.4),(426,206,3.1),(400,218,2.9),(380,229,2.7)]), ellipse(375,232,6.2,4.2,-10)])
moelle = tube([(330,326,7.6),(331,380,7.2),(330,450,7),(331,520,7),(330,580,7)])

out = {}
out['H'] = smooth_path(H_PTS)
out['S'] = smooth_path(S_PTS)
out['C'] = smooth_path(C_PTS)
out['E'] = smooth_path(E_PTS)
out['HL'] = smooth_path(HL_PTS)
out['cortex'] = shape_path(cortex)
out['frontal'] = shape_path(lobe(front))
out['parietal'] = shape_path(lobe(par))
out['temporal'] = shape_path(lobe(temp))
out['occipital'] = shape_path(lobe(occ))
out['liquide'] = shape_path(liq)
out['crane'] = shape_path(crane)
out['cheveux'] = shape_path(hair, .6)
out['meches'] = ' '.join(smooth_path(st, closed=False) for st in strands)
out['tronc'] = shape_path(tronc)
out['moelle'] = shape_path(moelle)
out['calleux'] = shape_path(calleux, .3)
out['thalamus'] = shape_path(thalamus, .3)
out['hypothalamus'] = shape_path(hypoth, .2)
out['pineale'] = shape_path(pineale, .15)
out['hippocampe'] = shape_path(hippo, .25)
out['amygdale'] = shape_path(amygdale, .15)
out['hypophyse'] = shape_path(hypophyse, .2)
out['nerf'] = shape_path(nerf, .25)

# rapport des positions réelles (centres des boîtes)
def c(g):
    x0, y0, x1, y1 = biggest(g).bounds
    return f"bbox x{x0:.0f}–{x1:.0f} y{y0:.0f}–{y1:.0f} centre ({(x0+x1)/2:.0f},{(y0+y1)/2:.0f})"
for k, g in [('cerveau', S), ('cervelet', C), ('tronc', tronc), ('thalamus', thalamus), ('hypothalamus', hypoth),
             ('pineale', pineale), ('hippocampe', hippo), ('amygdale', amygdale), ('hypophyse', hypophyse),
             ('nerf', nerf), ('calleux', calleux), ('frontal', front), ('parietal', par), ('temporal', temp),
             ('occipital', occ), ('tete', H), ('crane', crane), ('liquide', liq), ('oreille', poly(E_PTS))]:
    print(f"{k:13s} {c(g)}", file=sys.stderr)


# ---------------------------------------------------------------- gabarit SVG
GABARIT = r"""
            <!-- La tête de profil (regard vers la droite) et le cerveau à sa vraie
                 place (recherche §2.8). Repères : œil (456,194), conduit auditif
                 (300,250), bout du nez (507,250), bouche (480,300), cou x 304–414.
                 Ordre d'empilement = du plus profond au plus proche de l'œil, sauf
                 les régions profondes, posées PAR-DESSUS le cortex en transparence
                 (.profond : opacité .85 + bord cousu .couture) pour qu'on les lise
                 « dedans ». Tracés générés une fois à partir de points d'ancrage
                 (NOTES.md, Task 3), puis figés ici. -->

            <!-- cheveux longs (fille) : rideau DERRIÈRE la tête et le cou -->
            <path id="p-cheveux-long" class="w cheveux" style="--p:var(--hair)" data-ink="bleu" d="{{HL}}"/>

            <!-- la tête et le cou, en laine couleur peau -->
            <path id="p-tete" class="w peau" style="--p:var(--skin)" data-ink="jaune" d="{{H}}"/>

            <!-- le crâne : bande d'os du sourcil jusque sous le cervelet, liseré brodé -->
            <path id="p-crane" class="w" style="--p:var(--p-crane)" data-ink="jaune" d="{{crane}}"/>
            <path class="fil" style="--f:var(--fil-sable)" d="{{crane}}"/>

            <!-- le coussin d'eau (liquide cérébro-spinal) tout autour du cerveau et du cervelet -->
            <path id="p-liquide" class="w" style="--p:var(--p-liquide)" data-ink="bleu" d="{{liquide}}"/>

            <!-- le cervelet, SÉPARÉ du cerveau, strié de 5 traits brodés -->
            <path id="p-cervelet" class="w" style="--p:var(--p-cervelet)" data-ink="rose" d="{{C}}"/>
            <path id="fil-cervelet" class="fil" d="M213,270 Q240,264 267,270 M205,281 Q240,274 275,281 M202,292 Q240,286 281,292 M205,303 Q240,298 276,303 M213,314 Q240,310 267,314"/>

            <!-- le cerveau : le cortex (couverture plissée, plus sombre) et ses quatre lobes
                 posés dessus ; les sillons entre les lobes laissent voir le cortex -->
            <path id="p-cortex" class="w" style="--p:var(--p-cerveau-sombre)" data-ink="rose" d="{{cortex}}"/>
            <path id="p-frontal" class="w" style="--p:var(--p-frontal)" data-ink="rose" d="{{frontal}}"/>
            <path id="p-parietal" class="w" style="--p:var(--p-parietal)" data-ink="rose" d="{{parietal}}"/>
            <path id="p-occipital" class="w" style="--p:var(--p-occipital)" data-ink="rose" d="{{occipital}}"/>
            <path id="p-temporal" class="w" style="--p:var(--p-temporal)" data-ink="rose" d="{{temporal}}"/>
            <!-- sillons brodés : volutes blanches au point de tige, nœuds français au bout -->
            <g id="fil-sillons">
              <path class="fil" d="M398,122 C410,108 428,116 424,128 C420,140 432,146 442,136 M390,170 C400,158 414,168 424,160 C432,154 441,159 437,168 M284,132 C296,118 312,128 320,120 C328,112 340,118 333,128 M209,174 C214,160 228,162 229,171 C230,181 240,185 246,177 M362,272 C374,262 388,274 400,266 C410,260 419,266 413,276 M210,214 C214,200 228,200 230,212 C232,224 244,230 252,222"/>
              <g class="noeuds">
                <circle cx="442" cy="136" r="1.9" fill="url(#knot)"/><circle cx="437" cy="168" r="1.9" fill="url(#knot)"/>
                <circle cx="333" cy="128" r="1.9" fill="url(#knot)"/><circle cx="246" cy="177" r="1.9" fill="url(#knot)"/>
                <circle cx="413" cy="276" r="1.9" fill="url(#knot)"/><circle cx="252" cy="222" r="1.9" fill="url(#knot)"/>
              </g>
            </g>

            <!-- l'oreille, en transparence par-dessus le cerveau : l'entrée des sons -->
            <path id="p-oreille" class="w peau" style="--p:var(--skin)" data-ink="jaune" d="{{E}}"/>
            <g id="fil-oreille" style="--f:var(--skin-shade)">
              <path class="fil" d="M302,231 C286,226 275,238 276,254 C277,268 285,278 293,284"/>
              <!-- le petit escargot (cochlée), juste au fond du conduit -->
              <path class="fil" d="M303,251 c2.6,-1 4.4,1.2 3.6,3.4 c-1,2.6 -5,2.8 -6.4,0.4 c-1.6,-3 0.6,-6.6 4,-7 c3.8,-0.4 6.8,2.8 6.2,6.6"/>
            </g>
            <ellipse class="trou" cx="299" cy="251" rx="2.4" ry="3.2"/>

            <!-- le tronc cérébral (pont bombé vers l'avant) et la moelle dans le cou -->
            <path id="p-moelle" class="w profond" style="--p:var(--p-tronc)" data-ink="rose" d="{{moelle}}"/>
            <path id="p-tronc" class="w profond" style="--p:var(--p-tronc)" data-ink="rose" d="{{tronc}}"/>
            <path class="fil couture" d="{{tronc}}"/>

            <!-- les régions profondes, en transparence -->
            <path id="p-calleux" class="w profond" style="--p:var(--p-calleux)" data-ink="jaune" d="{{calleux}}"/>
            <path class="fil couture" style="--f:var(--fil-sable)" d="{{calleux}}"/>
            <path id="p-thalamus" class="w profond" style="--p:var(--p-thalamus)" data-ink="bleu" d="{{thalamus}}"/>
            <path class="fil couture" d="{{thalamus}}"/>
            <path id="p-pineale" class="w lite profond" style="--p:var(--p-pineale)" data-ink="bleu" d="{{pineale}}"/>
            <path class="fil couture" d="{{pineale}}"/>
            <path id="p-hypothalamus" class="w lite profond" style="--p:var(--p-hypothalamus)" data-ink="jaune" d="{{hypothalamus}}"/>
            <path class="fil couture" d="{{hypothalamus}}"/>
            <!-- l'horloge : deux aiguilles brodées -->
            <path class="fil" style="--f:var(--fil-brun)" d="M347,222 L347,217.6 M347,222 L350.6,223.6"/>
            <!-- l'hippocampe dans son groupe : c'est #g-hippocampe qu'on fera gonfler
                 (une transform CSS sur la pièce .w écraserait le décalage d'encre riso) -->
            <g id="g-hippocampe">
              <path id="p-hippocampe" class="w profond" style="--p:var(--p-hippocampe)" data-ink="jaune" d="{{hippocampe}}"/>
              <path class="fil couture" d="{{hippocampe}}"/>
              <!-- l'œil du petit cheval de mer (nœud français brun) -->
              <circle class="oeil-hippo" cx="347.6" cy="238.4" r="1.25"/>
            </g>
            <path id="p-amygdale" class="w lite profond" style="--p:var(--p-amygdale)" data-ink="rose" d="{{amygdale}}"/>
            <path class="fil couture" d="{{amygdale}}"/>
            <path id="p-hypophyse" class="w lite profond" style="--p:var(--p-hypophyse)" data-ink="rose" d="{{hypophyse}}"/>
            <path class="fil couture" d="{{hypophyse}}"/>
            <!-- le nerf de l'œil, de l'arrière de l'œil vers l'arrière et le milieu, jusqu'au croisement (chiasma) -->
            <path id="p-nerf-optique" class="w profond" style="--p:var(--p-nerf)" data-ink="jaune" d="{{nerf}}"/>
            <path class="fil" style="--f:var(--fil-brun)" d="M372,229.6 L378,234.4 M378,229.6 L372,234.4"/>

            <!-- les cheveux courts : une calotte bouclée, et un épi sur le dessus -->
            <path id="p-cheveux" class="w cheveux" style="--p:var(--hair)" data-ink="bleu" d="{{cheveux}}"/>
            <path class="fil meches" d="{{meches}}"/>
            <path class="fil epi" d="M352,44 C350,32 356,24 364,26 C371,28 370,37 363,37 C358,37 358,31 362,31"/>

            <!-- le visage : joue, œil-bouton, paupière (fermée la nuit), sourcil, sourire -->
            <path id="p-joue" class="w lite" style="--p:var(--p-joue)" data-ink="rose" d="M434,266 C434,258 442,255 450,255 C459,255 463,260 463,266 C463,272 457,276 449,276 C441,276 434,273 434,266 Z"/>
            <path id="p-oeil" class="w lite" style="--p:var(--p-oeil)" data-ink="bleu" d="M446,194 C446,188 450,184 456,184 C462,184 466,188 466,194 C466,200 462,204 456,204 C450,204 446,200 446,194 Z"/>
            <circle class="trou" cx="452.6" cy="192.2" r="1.7"/><circle class="trou" cx="459.4" cy="195.8" r="1.7"/>
            <path class="fil" d="M452.6,192.2 L459.4,195.8"/>
            <!-- liseré clair cousu au bord du bouton : l'œil reste lisible sur toutes les peaux -->
            <circle class="fil bord-bouton" cx="456" cy="194" r="7.9"/>
            <path id="p-paupiere" class="w lite peau" style="--p:var(--skin)" data-ink="jaune" d="M443,195 C443,186 449,181 456,181 C463,181 469,186 469,195 C469,201 463,205 456,205 C449,205 443,201 443,195 Z"/>
            <path id="fil-oeil-ferme" class="fil" style="--f:var(--fil-brun)" d="M446,195 Q456,204 466,195 M449.5,199.5 L447.4,203 M456,201.2 L456,205.4 M462.5,199.5 L464.6,203"/>
            <g id="p-sourcil">
              <path class="w lite cheveux" style="--p:var(--hair)" data-ink="bleu" d="M441,182 C445,171 460,165 471,170 C473,172 472,175 469,175 C460,172 451,175 446,184 C444,186 440,185 441,182 Z"/>
            </g>
            <path id="p-bouche" class="fil" d="M488,301 C484,308 474,309 468,299 C467,297 467.6,295 469.4,294.4"/>
            <path class="fil narine" d="M497,257 C493,257.6 491.6,261 494,263"/>
"""

# ---------------------------------------------------------------- écriture
if __name__ == "__main__":
    import os
    frag = re.sub(r"\{\{(\w+)\}\}", lambda m: out[m.group(1)], GABARIT)
    taille = sum(len(m) for m in re.findall(r' d="([^"]*)"', frag))
    print(f"données de tracé (attributs d) : {taille} octets", file=sys.stderr)
    if "--sec" not in sys.argv:
        idx = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "index.html")
        html = open(idx, encoding="utf-8").read()
        start = html.index('<g id="g-dedans">') + len('<g id="g-dedans">')
        end = html.index('</g>\n          <!-- ===== Vue « Tout près »', start)
        html = html[:start] + frag.rstrip() + '\n          ' + html[end:]
        open(idx, "w", encoding="utf-8").write(html)

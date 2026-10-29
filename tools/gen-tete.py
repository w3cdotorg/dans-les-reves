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
# Tête (peau), de profil, regard vers la droite — profil d'enfant de 5 ans
# (Task 3b) : sommet y 56, œil y 190 à mi-hauteur sommet → menton (y 348),
# front bombé, arcade discrète, racine du nez en creux (486,194), nez court et
# retroussé (bout (507,249)), base du nez (489,266), lèvre supérieure un peu en
# avant de l'inférieure, jonction des lèvres (488,297), sillon sous la lèvre
# (480,320), menton rond (484,333)/(472,348), dessous du menton puis gorge (422,374).
# Passe 2 : crâne moins profond — l'occiput le plus en arrière à x 187 vers la
# hauteur des yeux (y 190–232), voûte un peu aplatie ; le bas de l'occiput
# (205,323)–(248,344) juste sous le cervelet, puis la nuque descend vers l'avant
# et rejoint le bord arrière du cou (x 312) vers y 352 ; cou x 312–408.
H_PTS = [(312,575),(312,500),(312,400),(310,355),(300,350),(276,347),(248,344),(222,338),(205,323),
         (195,300),(190,268),(187,232),(187,190),(191,148),(206,110),(234,80),(276,62),(330,56),
         (386,57),(434,68),(468,90),(488,118),(495,148),(494,170),(489,184),(486,194),
         (489,210),(495,228),(503,241),(507,249),(503,258),(495,262),(489,266),(487,275),(492,284),
         (492,292),(488,297),(491,303),(488,312),(480,320),(484,333),(472,348),(452,357),
         (436,363),(422,374),(412,396),(408,440),(408,500),(408,575)]
# Cerveau (hémisphère vu de côté, avant à droite).
S_PTS = [(466,142),(463,157),(443,171),(428,193),(421,228),(431,240),(434,256),(424,278),
         (398,294),(360,300),(328,296),(306,284),(290,266),(266,252),(240,247),(216,242),
         (202,228),(199,192),(210,156),(238,120),(280,95),(330,86),(380,85),(424,96),(452,115)]
# Cervelet : corps ovale + bras (pédoncule) qui rejoint le tronc.
# Passe 2 : avancé de (9,2) (9,2 px) pour garder de l'os derrière et dessous
# quand l'arrière du crâne a reculé.
C_DX, C_DY = 9, 2
C_PTS = [(x + C_DX, y + C_DY) for x, y in
         [(196,290),(206,268),(236,258),(266,263),(285,281),(300,292),(314,296),(315,306),
          (299,311),(282,316),(262,325),(236,327),(210,321),(198,306)]]
# Oreille : un pavillon (hélix qui s'enroule, lobe, tragus devant le conduit),
# de la ligne des sourcils (y 184) à la base du nez (y 286), conduit (300,250).
E_PTS = [(306,196),(294,186),(278,186),(266,198),(261,218),(262,242),(267,264),(276,280),
         (288,288),(297,284),(300,274),(306,266),(309,256),(306,244),(311,232),(313,214)]
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
# le tronc descend en arrière vers le trou occipital (bas recalé de 8 px vers l'arrière)
tronc = tube([(320,243,9.5),(323,258,10),(330,276,12.5),(334,293,14),(329,309,11.5),(324,322,8.6),(322,334,7.8)])
# le coussin d'eau : 9 px autour du cerveau, mais jamais à moins de 7 px de la peau
# (2 de peau + 5 d'os) : à l'arrière, devenu moins profond, il s'amincit.
liq = unary_union([S, C, tronc.intersection(box(0,0,900,330))]).buffer(14).buffer(-5).intersection(H.buffer(-7))
# crâne : la voûte (entre la peau et le coussin d'eau, de l'arcade sourcilière à
# l'occiput) + le plancher (un anneau de 9 px sous le coussin d'eau : toit de
# l'orbite, fosse sous le lobe temporal, sous le cervelet), percé du TROU
# OCCIPITAL sous l'oreille, par où le tronc sort vers la moelle.
# Sous les cheveux, l'os monte jusqu'à 2 px de la peau (l'arrière du crâne est
# mince) ; au front, sous la lisière, il laisse 7 px de peau.
vault_keep = Polygon([(540,-20),(540,178),(482,178),(446,184),(400,232),(330,300),(300,362),
                      (110,362),(110,-20)])
foramen = box(309, 326, 337, 380)
cap_keep = Polygon([(620,-60),(620,30),(486,100),(330,300),(210,390),(80,470),(-60,470),(-60,-60)])
voute = unary_union([H.buffer(-2).intersection(cap_keep), H.buffer(-7)]).intersection(vault_keep)
crane = rounded(unary_union([voute, liq.buffer(7)])
                .difference(liq).difference(foramen).intersection(H.buffer(-2)), 2)
# cheveux courts : une calotte de laine sur le haut et l'arrière, bord ondulé,
# qui s'amincit vers la nuque ; trois mèches de frange sur le front.
# implantation : front dégagé (lisière vers (486,100)), courte lisière de nuque
# (les cheveux s'arrêtent vers y 326) ; cap_keep est défini avec le crâne.
ring = H.exterior
blobs = []; strands = []
L = ring.length
s0 = None
for i in range(int(L//5)):
    sd = i*5
    p = ring.interpolate(sd)
    if not cap_keep.contains(p) or p.y > 392: continue
    if s0 is None: s0 = sd
    taper = max(0.0, min(1.0, (330 - p.y)/110))          # 1 en haut, 0 à la nuque
    arriere = max(0.0, min(1.0, (p.x - 187)/70))         # 0 tout à l'arrière : cheveux ras (bord x ≈ 183)
    r = 3.6 + taper*arriere*(7.5 + 2.4*math.sin((sd-s0)/31*2*math.pi))
    blobs.append(p.buffer(r, 20))
locks = [tube([(470,80,7),(482,96,4.6),(486,110,1.6)]), tube([(456,70,7),(468,88,4),(472,100,1.4)])]
hair = unary_union([unary_union(blobs).difference(H.buffer(-2.5)).intersection(cap_keep)] + locks)
hair = rounded(biggest(hair.buffer(0).difference(box(0,326,330,600))), 1)   # courte lisière de nuque
# fils de laine plus clairs qui suivent la calotte
inner = H.buffer(1.5).exterior
for k in range(40):
    sd = k*46
    seg = [inner.interpolate(sd + t) for t in (0, 15, 30)]
    if all(cap_keep.buffer(-12).contains(q) and q.y < 330 for q in seg):
        strands.append([(q.x, q.y) for q in seg])
# cheveux longs (fille) : rideau derrière la tête et le cou
HL_PTS = [(262,84),(214,104),(190,150),(178,220),(176,300),(180,380),(186,450),(192,490),
          (204,512),(222,520),(242,512),(262,524),(284,516),(304,524),(318,512),(322,470),
          (316,410),(290,370),(240,330),(220,200)]
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
# la moelle sort par le trou occipital et descend dans la moitié ARRIÈRE du cou
moelle = tube([(323,328,7.6),(328,380,7.2),(332,440,7),(334,500,7),(334,580,7)])   # passe 2 : cou x 312–408, moelle dans le tiers arrière

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
                 place (recherche §2.8). Repères (Task 3b, profil d'enfant de 5 ans) :
                 œil (460,191), conduit auditif (300,250), bout du nez (506,247),
                 bouche (481,299), menton (472,348), angle de la mâchoire (330,328),
                 trou occipital (323,340), occiput x 187, nuque → cou à (312,352), cou x 312–408.
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
            <path id="fil-cervelet" class="fil" d="M222,272 Q249,266 276,272 M214,283 Q249,276 284,283 M211,294 Q249,288 290,294 M214,305 Q249,300 285,305 M222,316 Q249,312 276,316"/>

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
            <!-- #g-oreille, #g-cheveux, #g-visage : regroupés pour être repris tels quels dans Dehors (<use>) -->
            <g id="g-oreille">
              <path id="p-oreille" class="w peau" style="--p:var(--skin)" data-ink="jaune" d="{{E}}"/>
              <g id="fil-oreille" style="--f:var(--skin-shade)">
                <!-- le rebord de l'hélix qui s'enroule, l'anthélix, et la conque autour du conduit -->
                <path class="fil" d="M303,199c-8-8-22-8-31 2-7 9-8 26-5 42 2 12 8 24 16 31"/>
                <path class="fil" d="M296,206c-10-3-19 5-20 17-1 10 4 18 6 24M287,232c5-2 10 0 12 4"/>
                <path class="fil" d="M292,262c-4 4-4 12 2 17"/>
                <!-- le petit escargot (cochlée), juste au fond du conduit -->
                <path class="fil" d="M303,251 c2.6,-1 4.4,1.2 3.6,3.4 c-1,2.6 -5,2.8 -6.4,0.4 c-1.6,-3 0.6,-6.6 4,-7 c3.8,-0.4 6.8,2.8 6.2,6.6"/>
              </g>
              <ellipse class="trou" cx="299" cy="251" rx="2.4" ry="3.2"/>
            </g>

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
            <!-- les cheveux courts et leurs fils -->
            <g id="g-cheveux">
              <path id="p-cheveux" class="w cheveux" style="--p:var(--hair)" data-ink="bleu" d="{{cheveux}}"/>
              <path class="fil meches" d="{{meches}}"/>
              <path class="fil epi" d="M352,44 C350,32 356,24 364,26 C371,28 370,37 363,37 C358,37 358,31 362,31"/>
            </g>

            <!-- le visage : joue, œil-bouton, paupière (fermée la nuit), sourcil, sourire -->
            <!-- le visage entier -->
            <g id="g-visage">
              <!-- la mâchoire : une fine ombre de laine sous son bord, du dessous du menton
                   à l'angle sous l'oreille (333,363), puis le long de la branche qui remonte -->
              <path id="p-ombre-cou" class="w lite" style="--p:var(--skin-shade)" data-ink="jaune" d="M452,357C420,349 372,337 333,327 325,317 320,305 317,294 314,307 317,320 324,331 366,342 410,353 442,363Z"/>
              <path id="p-joue" class="w lite" style="--p:var(--p-joue)" data-ink="rose" d="M439,270c0-6 6-9 13-9s13 3 13 9-6 9-13 9-13-3-13-9Z"/>
              <!-- l'œil de profil : une amande (blanc de laine), le bouton cousu devant,
                   le bord de la paupière et trois cils ; le creux du coin, vers le nez -->
              <path id="p-oeil-blanc" class="w lite" style="--p:var(--p-blanc-oeil)" data-ink="jaune" d="M443.5,191c5-5 13-7.5 21-7 3 2 4.6 4.6 4.6 7s-1.6 5-4.6 7c-8 .6-16-2-21-7Z"/>
              <path id="p-oeil" class="w lite" style="--p:var(--p-oeil)" data-ink="bleu" d="M454,190.6a6.3,6.3 0 1 0 12.6,0a6.3,6.3 0 1 0-12.6,0Z"/>
              <circle class="trou" cx="458.4" cy="189.4" r="1.25"/><circle class="trou" cx="462.2" cy="191.8" r="1.25"/>
              <path class="fil" d="M458.4,189.4 L462.2,191.8"/>
              <!-- liseré clair cousu au bord du bouton : l'œil reste lisible sur toutes les peaux -->
              <circle class="fil bord-bouton" cx="460.3" cy="190.6" r="5.1"/>
              <path class="fil cils" d="M443.5,191c6-5.4 14-7.8 21-7.2M460,184.2l2.6-4.4M464.6,184l3.6-3.6M467.6,185.4l4.4-2.2"/>
              <path class="fil pli" d="M446,185.6c6-5 15-6.6 22-4.6M473.4,186.4c1.6 1.6 1.8 4 .6 5.8"/>
              <path id="p-paupiere" class="w lite peau" style="--p:var(--skin)" data-ink="jaune" d="M441.5,191c5-6.4 14-9.4 23.6-8.4 3.4 2 5.2 5.4 5.2 8.4s-1.8 6.2-5.2 8.2c-9.6 1-18.6-1.8-23.6-8.2Z"/>
              <path id="fil-oeil-ferme" class="fil" style="--f:var(--fil-brun)" d="M443,191.6Q456,199 469.6,192.4M450,195.4l-1.6 3.8M456.6,196.8v4.2M463.2,195.8l1.8 3.8"/>
              <g id="p-sourcil">
                <path class="w lite cheveux" style="--p:var(--hair)" data-ink="bleu" d="M443,179c5-8 18-12 29-9 2 1 2 3.6-.6 3.8-10-1.6-20 .6-25.6 7.4-1.6 1.8-3.8.6-2.8-2.2Z"/>
              </g>
              <path id="p-bouche" class="fil" d="M489.6,297.6c-4,5.4 -12.6,6.4 -17.6,.4c-1,-2 -.4,-4 1.4,-4.6"/>
              <path class="fil narine" d="M497,255.4c-4,.6 -5.4,4 -3,6"/>
            </g>
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

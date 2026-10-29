#!/usr/bin/env python3
# Générateur des dessins des cartes-souvenirs de index.html (Task 8).
# Outil de dessin, PAS livré : index.html reste le seul fichier livré.
#
# Produit, dans <defs>, le bloc <!-- CARTES-BEGIN --> … <!-- CARTES-END --> :
#   - #ic-oeil / #ic-oreille : la petite porte d'entrée brodée au bas de chaque carte ;
#   - #v-<slug> : une vignette par carte (40 × 40, centrée sur (0,0)) ;
#   - #d-<slug> : la forme de décor Dehors de chaque carte « base » (~90 px,
#     centrée sur l'emplacement ; le pouce de César va du sol à y ≈ 196 de la scène).
# Toutes les pièces sont des .w.lite (laine allégée), jamais de transform sur un .w :
# les décors « agrandis » sont des vignettes dont les tracés sont multipliés ici.
# Aucune dépendance (pas de shapely). Pas d'arc (« a ») dans les tracés : le
# changement d'échelle multiplie simplement tous les nombres.
#
# Usage (depuis la racine du dépôt) :
#   python3 tools/gen-cartes.py          # réécrit le bloc dans index.html
#   python3 tools/gen-cartes.py --sec    # n'écrit rien, affiche la taille du bloc
import re, sys, os

K = .5523  # cercle en 4 cubiques

def f(v):
    """Nombre court : 1 décimale au plus, sans zéro de tête."""
    s = f"{round(v, 1):.1f}"
    if s.endswith('.0'): s = s[:-2]
    if s.startswith('0.'): s = s[1:]
    elif s.startswith('-0.'): s = '-' + s[2:]
    return '0' if s in ('-0', '') else s

def echelle_d(d, s, dx=0, dy=0):
    """Multiplie tous les nombres d'un tracé par s, puis décale les coordonnées
    ABSOLUES de (dx, dy). Pas d'arc dans les tracés de ce fichier."""
    out, cmd, idx = [], None, 0
    for tok in re.findall(r'[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?', d):
        if tok.isalpha():
            cmd, idx = tok, 0
            out.append(tok)
            continue
        v = float(tok) * s
        if cmd in 'MLCQST':
            v += dx if idx % 2 == 0 else dy
        elif cmd == 'H':
            v += dx
        elif cmd == 'V':
            v += dy
        idx += 1
        out.append(f(v))
    # compacte : pas d'espace devant un « - » ni après une lettre
    r = ''
    for t in out:
        if r and not t[0].isalpha() and not r[-1].isalpha() and not t.startswith('-'):
            r += ' '
        r += t
    return r

def circ(cx, cy, r):
    k = K * r
    return (f"M{cx-r} {cy}C{cx-r} {cy-k} {cx-k} {cy-r} {cx} {cy-r}C{cx+k} {cy-r} {cx+r} {cy-k} {cx+r} {cy}"
            f"C{cx+r} {cy+k} {cx+k} {cy+r} {cx} {cy+r}C{cx-k} {cy+r} {cx-r} {cy+k} {cx-r} {cy}Z")

def ell(cx, cy, rx, ry):
    kx, ky = K * rx, K * ry
    return (f"M{cx-rx} {cy}C{cx-rx} {cy-ky} {cx-kx} {cy-ry} {cx} {cy-ry}C{cx+kx} {cy-ry} {cx+rx} {cy-ky} {cx+rx} {cy}"
            f"C{cx+rx} {cy+ky} {cx+kx} {cy+ry} {cx} {cy+ry}C{cx-kx} {cy+ry} {cx-rx} {cy+ky} {cx-rx} {cy}Z")

def anneau(cx, cy, r, ri):
    """Disque percé (fill-rule evenodd) : la roue du vélo."""
    return circ(cx, cy, r) + circ(cx, cy, ri)

def rr(x, y, w, h, r):
    k = r * (1 - K)
    return (f"M{x+r} {y}H{x+w-r}C{x+w-k} {y} {x+w} {y+k} {x+w} {y+r}V{y+h-r}C{x+w} {y+h-k} {x+w-k} {y+h} {x+w-r} {y+h}"
            f"H{x+r}C{x+k} {y+h} {x} {y+h-k} {x} {y+h-r}V{y+r}C{x} {y+k} {x+k} {y} {x+r} {y}Z")

def goutte(cx, cy, r=2):
    """Flamme ou goutte : pointe en haut."""
    return (f"M{cx} {cy-1.8*r}C{cx+r} {cy-.5*r} {cx+r} {cy+.8*r} {cx} {cy+.8*r}"
            f"C{cx-r} {cy+.8*r} {cx-r} {cy-.5*r} {cx} {cy-1.8*r}Z")

# ---------------------------------------------------------------------------
# Éléments : W pièce de laine, T cordon de laine (trait), F fil brodé, N nœud
#   W(d, laine, encre, classes)   laine = jeton --p-… (sans « --p- »)
#   T(d, laine, encre, épaisseur, classes)
#   F(d, fil=None, classes)       fil = jeton --fil-… ou autre variable
#   N(cx, cy, r, sorte)           sorte : knot | brun | blanc (classe noeud-…)
def W(d, p, ink, cls=''):  return ('W', d, p, ink, cls)
def T(d, p, ink, w, cls=''): return ('T', d, p, ink, cls, w)
def F(d, fil=None, cls=''): return ('F', d, fil, cls)
def N(cx, cy, r, sorte='knot'): return ('N', cx, cy, r, sorte)

def rendu(el, s=1.0, dx=0, dy=0, fil_s=1.0, filtre='vig'):
    """filtre : vig (vignette, région fixe 56 × 56) ou mini (décor, région −60 %)."""
    kind = el[0]
    if kind == 'W':
        _, d, p, ink, cls = el
        fr = ' fill-rule="evenodd"' if 'evenodd' in cls else ''
        cls = ' '.join(c for c in cls.split() if c != 'evenodd')
        c = (f'w lite {filtre} ' + cls).strip()
        return f'<path class="{c}" style="--p:var(--p-{p})" data-ink="{ink}"{fr} d="{echelle_d(d, s, dx, dy)}"/>'
    if kind == 'T':
        _, d, p, ink, cls, w = el
        c = (f'w lite {filtre} trait ' + cls).strip()
        return f'<path class="{c}" style="--p:var(--p-{p});--tw:{f(w*s)}" data-ink="{ink}" d="{echelle_d(d, s, dx, dy)}"/>'
    if kind == 'F':
        _, d, fil, cls = el
        st = f' style="--f:var({fil})"' if fil else ''
        c = ' '.join(x for x in ('fil', cls, 'gros' if fil_s != 1 else '') if x)
        return f'<path class="{c}"{st} d="{echelle_d(d, s, dx, dy)}"/>'
    if kind == 'P':   # sous-couche de papier (riso) : rien en feutrine
        return f'<path class="papier-pres" d="{echelle_d(el[1], s, dx, dy)}"/>'
    if kind == 'N':
        _, cx, cy, r, sorte = el
        rr_ = r * min(s, 1.8)
        if sorte == 'knot':
            return f'<circle cx="{f(cx*s+dx)}" cy="{f(cy*s+dy)}" r="{f(rr_)}" fill="url(#knot)"/>'
        return f'<circle class="noeud-{sorte}" cx="{f(cx*s+dx)}" cy="{f(cy*s+dy)}" r="{f(rr_)}"/>'
    raise ValueError(kind)

# ---------------------------------------------------------------------------
# Vignettes 40 × 40, centrées sur (0,0)
BRUN = '--fil-brun'
BLANC = '--fil-blanc'
SABLE = '--fil-sable'

def bulle():
    """Le fond des « mots entendus » : une bulle de parole bleu pâle."""
    return W("M-17 -15C-17 -18 -15 -19 -12 -19H12C15 -19 17 -18 17 -15V7C17 10 15 11 12 11H-3L-9 17.5L-8 11H-12C-15 11 -17 10 -17 7Z",
             'bulle', 'bleu', 'pastel')

def yeux(cx, cy, e, r=1.3):
    return [N(cx - e, cy, r, 'brun'), N(cx + e, cy, r, 'brun')]

def sourire(cx, cy, w):
    return F(f"M{cx-w} {cy}Q{cx} {cy+w*.8} {cx+w} {cy}", BRUN)

V = {}

V['pouce'] = [
    W(rr(-13, 14, 26, 6, 2), 'socle', 'bleu', 'pastel'),
    W("M-9 15C-9.5 8 -10 2 -9.5 -5C-9 -13 -6 -19 0 -19C6 -19 9 -13 9.5 -5C10 2 9.5 8 9 15Z", 'bronze', 'jaune', 'brun'),
    W("M4.5 -17.5C8 -14.5 9.5 -9.5 9.5 -5C10 2 9.5 8 9 15H5.5C6.5 8 7 2 6.8 -5C6.6 -10 6 -14 4.5 -17.5Z", 'bronze-ombre', 'rose', 'pastel'),
    ('F', "M-9 15C-9.5 8-10 2-9.5-5C-9-13-6-19 0-19C6-19 9-13 9.5-5C10 2 9.5 8 9 15", BRUN, 'epais'),
    W("M-6.2-13.2C-6.2-18.6 6.2-18.6 6.2-13.2L5.8-7.5C5.6-5 4-3.8 0-3.8C-4-3.8-5.6-5-5.8-7.5Z", 'ongle', 'jaune', 'pastel'),
    ('F', "M-6.2-13.2C-6.2-18.6 6.2-18.6 6.2-13.2L5.8-7.5C5.6-5 4-3.8 0-3.8C-4-3.8-5.6-5-5.8-7.5Z", BRUN, ''),
    F("M-3.4-15.5Q-3.6-12-3-8.5", BLANC),
    ('F', "M-7.5 2Q0 4.5 7.5 2M-7 6.4Q0 8.4 7 6.4", BRUN, 'epais'),
]

V['glace'] = [
    W("M-7.5 -3H7.5L.8 18.5Q0 19.6-.8 18.5Z", 'cornet', 'jaune', 'orange'),
    F("M-5.5 0L2.5 10M0-2.5L5 4M5.5 0L-2.5 10M0-2.5L-5 4", BRUN),
    W("M-9-4C-11-8-9-14-4-15.5C-1-17.5 3-17.5 5-15.5C9.5-14 11-8 9-4C7.5-1.5 6-3.5 4.5-2C3-.5 1.5-3 0-1.5C-1.5 0-3-3-4.5-1.5C-6 0-7.5-1.5-9-4Z",
      'glace-rose', 'rose', 'pastel'),
    W(circ(1, -17.6, 2.6), 'cerise', 'rose'),
    F("M-5.5-10.5Q-4.5-13.5-1.5-14", BLANC),
]

V['chien'] = [
    T("M-12 10Q-19 6-17-1", 'chien', 'jaune', 3, 'orange'),
    W("M-14 17C-16 9-13 0-6-1C1-2 6 4 7 10C7.5 13 7 16 6 17Z", 'chien', 'jaune', 'orange'),
    W("M-1-9C-1-15 3-18 7-18C11-18 14-15 14-11C17-11 19-9 19-6.5C19-4 17-2.5 14-2.5C12-.5 9 .5 6 0C2-.5-1-4-1-9Z",
      'chien', 'jaune', 'orange'),
    W(ell(15, -5.6, 4, 2.8), 'chien-clair', 'jaune', 'pastel'),
    W("M3-16C-1-16-3-11-2-6C-1.5-3.5 1-3 2-5C3-8 5-12 3-16Z", 'chien-oreille', 'rose', 'brun'),
    T("M.5-1.5Q4 1 8-.5", 'cerise', 'rose', 2.2),
    N(18.4, -7, 1.7, 'brun'), N(9, -11, 1.3, 'brun'),
    F("M14.5-3.6Q16-2.6 17.5-3.6", BRUN),
    F("M-1 17V12M3 17V10", BRUN),
]

V['velo'] = [
    W(anneau(-10, 8, 8.5, 6.3), 'roue', 'bleu', 'evenodd'),
    W(anneau(10, 8, 8.5, 6.3), 'roue', 'bleu', 'evenodd'),
    F("M-10 2V14M-16 8H-4M10 2V14M4 8H16", SABLE),
    T("M-10 8L-3-4H8L10 8M-3-4L1 8H-10M1 8L8-4", 'velo', 'rose', 2.6),
    T("M-3-4L-4-7.5M8-4L7-10H11", 'roue', 'bleu', 2),
    W("M-7.5-9H-1C0-9 .5-7.5-.5-7H-7.5C-8.5-7.5-8.5-9-7.5-9Z", 'roue', 'bleu'),
    N(-10, 8, 1.4), N(10, 8, 1.4), N(1, 8, 1.6),
]

V['piscine'] = [
    W(rr(-19, -1, 38, 6, 2), 'bord-piscine', 'bleu', 'pastel'),
    W("M-17 4H17V15C17 17 16 18 14 18H-14C-16 18-17 17-17 15Z", 'eau', 'bleu', 'pastel'),
    F("M-14 9Q-11.5 6.5-9 9T-4 9T1 9T6 9M-12 14Q-9.5 11.5-7 14T-2 14T3 14T8 14", BLANC),
    T("M11-13V6M16-13V6", 'socle', 'bleu', 1.8),
    F("M11-9H16M11-4H16M11 1H16", SABLE),
    W(anneau(-7, -7.5, 6, 3), 'cerise', 'rose', 'evenodd'),
    F("M-12.5-7.5H-10.5M-3.5-7.5H-1.5M-7-13V-11M-7-4V-2", BLANC),
]

V['gateau'] = [
    W(rr(-18, 14, 36, 4, 2), 'assiette', 'bleu', 'pastel'),
    W(rr(-14, -1, 28, 16, 3), 'gateau', 'jaune', 'pastel'),
    W("M-15-1C-15-5 15-5 15-1V3C13 6 11 2 9 4C7 8 4 3 1.5 5C-1 8-4 3-6.5 5C-9 8-12 3-15 5Z", 'glacage', 'rose', 'pastel'),
    F("M-13 10.5H13", '--fil-rouge'),
    W(rr(-8, -13, 3, 10, 1), 'bougie', 'bleu'),
    W(rr(-1.5, -14.5, 3, 11, 1), 'bougie', 'bleu'),
    W(rr(5, -13, 3, 10, 1), 'bougie', 'bleu'),
    W(goutte(-6.5, -15.5, 1.8), 'flamme', 'jaune', 'reserve'),
    W(goutte(0, -17, 1.8), 'flamme', 'jaune', 'reserve'),
    W(goutte(6.5, -15.5, 1.8), 'flamme', 'jaune', 'reserve'),
]

V['tracteur'] = [
    W("M-15-1V-16C-15-17-14-18-13-18H-1C0-18 1-17 1-16V-1Z", 'tracteur', 'bleu', 'vert'),
    W(rr(-12.5, -15.5, 10.5, 7, 1.2), 'vitre', 'bleu', 'pastel'),
    W("M0-7H14C16-7 17-6 17-4V5H0Z", 'tracteur', 'bleu', 'vert'),
    W(rr(9.4, -14.5, 2.4, 8, 1), 'roue', 'bleu'),
    W(circ(-8, 8, 10), 'roue', 'bleu'),
    W(circ(-8, 8, 4.6), 'moyeu', 'jaune'),
    W(circ(12, 11.5, 6.5), 'roue', 'bleu'),
    W(circ(12, 11.5, 2.8), 'moyeu', 'jaune'),
    F("M3-3H14", BLANC),
    N(-8, 8, 1.4), N(12, 11.5, 1.1),
]

V['orage'] = [
    W("M-15 2C-19 2-20-4-16-6C-17-12-10-15-6-11C-4-17 5-18 7-12C11-15 17-11 15-6C19-5 19 2 15 2Z", 'nuage', 'bleu', 'pastel'),
    W("M1 0L-5 9H-1L-4 18L5 6H1L4 0Z", 'eclair', 'jaune', 'reserve'),
    F("M-12 6L-14 11M-8 9L-10 14M10 6L8 11M14 9L12 14", '--fil-vague'),
]

V['manege'] = [
    T("M-12-4V13M12-4V13M0-3V13", 'or', 'jaune', 1.6),
    W(rr(-17, 13, 34, 5, 2), 'assiette', 'bleu', 'pastel'),
    W("M-6 8C-6 4-3 2 1 2H3L5-1C6-2 8-2 8.5-.5L9 2C9.5 3.5 8.5 4.5 7 4L5.5 3.5L5 7C5 9 3.5 9.5 2 9.5H-4C-5 9.5-6 9-6 8Z",
      'cheval', 'jaune', 'reserve'),
    F("M-4 9.5L-5 12.5M2 9.5L3 12.5M3.5.5Q2 2.5 1.5 4", BRUN),
    N(6.6, .6, .9, 'brun'),
    W("M-17-6L0-18L17-6C14-3 11-6 8.5-3.5C6-1 3-4 0-2C-3-4-6-1-8.5-3.5C-11-6-14-3-17-6Z", 'manege', 'rose', 'pastel'),
    F("M0-17V-3M-8-11.5L-8.5-4.5M8-11.5L8.5-4.5", BLANC),
    N(0, -19, 2.2),
]

V['ogre'] = [
    bulle(),
    W("M-9-5C-12-6-12-1-9-1ZM10-5C13-6 13-1 10-1Z", 'ogre', 'jaune', 'vert'),
    W("M-9-2C-10-8-8-14-3-15C-1-17 2-17 4-15C9-14 11-8 10-2C10 4 6 7 .5 7C-5 7-9 4-9-2Z", 'ogre', 'jaune', 'vert'),
    F("M-6-10L-1-8.5M2-8.5L7-10", BRUN),
    N(-3.5, -6.5, 1.4, 'brun'), N(4, -6.5, 1.4, 'brun'),
    F("M0-5.5C-1-2.5 2-2.5 1.5-4.5", BRUN),
    W("M-5 0C-2 3.6 3 3.6 6 0C4 5-3 5-5 0Z", 'bouche', 'rose', 'brun'),
    W("M-3 .8L-2 3.2L-1 1.4ZM3 1.4L4 3.2L5 .8Z", 'blanc-oeil', 'jaune', 'reserve'),
]

V['pirate'] = [
    bulle(),
    W("M-14 3C-12-3-9-11 0-12C9-11 12-3 14 3C9 1 4 0 0 0C-4 0-9 1-14 3Z", 'pirate', 'bleu'),
    F("M-13 1.6Q0-3 13 1.6", SABLE),
    W(circ(0, -6, 3.2), 'blanc-oeil', 'jaune', 'reserve'),
    N(-1.1, -6.4, .8, 'brun'), N(1.1, -6.4, .8, 'brun'),
    F("M-4.5-.6L4.5-3.4M-4.5-3.4L4.5-.6", BLANC),
    N(-11.5, -14.5, 1.2), N(11, -15, 1.2), N(13, -5, 1),
]

V['dragon'] = [
    bulle(),
    W("M-12-8L-14-14L-8-10.5ZM-7-11L-7-17L-3-11.5ZM-2-11.5L0-16.5L2-10.5Z", 'piquant', 'jaune', 'orange'),
    W("M-15 4C-16-3-13-10-6-11C-2-12 2-10 4-7C7-7 11-6 12-3C13 0 11 2 8 2H1C-1 5-4 7-8 7C-12 7-15 6-15 4Z", 'dragon', 'bleu', 'vert'),
    W(circ(-4, -5, 2.4), 'blanc-oeil', 'jaune', 'reserve'),
    N(-3.4, -5, 1.1, 'brun'),
    F("M9-3.5V-2.5M-11 2Q-6 4-1 2", BRUN),
    W("M12.5-3C15-5.5 16.5-3 15.5-1.5C17.5-1.5 17.5 1.5 15.5 2C16.5 4 13.5 4.5 12.5 2Z", 'flamme', 'jaune', 'reserve'),
]

V['anniversaire'] = [
    bulle(),
    F("M-6-2Q-5 3-1 8M5-3Q4 2-1 8", BRUN),
    W(ell(-6, -8.5, 5, 6), 'cerise', 'rose'),
    W(ell(5.5, -10, 4.6, 5.6), 'bougie', 'bleu'),
    F("M-8-11Q-7.5-13-6-13.5M3.8-12.5Q4-14 5.2-14.5", BLANC),
    N(-12.5, 4, 1.1), N(11, 3, 1.1), N(13, -16, 1), N(-13, -15, 1),
]

def buste(cx, top, r, peau, cheveux, haut, haut_ink, style='court', haut_cls='', larg=None, che_ink='bleu', che_cls=''):
    """Un buste de face : épaules, tête, cheveux, visage. top = haut du crâne."""
    cy = top + r
    larg = larg or r * 1.35
    epy = cy + r * .95
    els = []
    if style == 'long':
        els.append(W(f"M{cx-r*1.1} {cy+r*1.6}C{cx-r*1.3} {cy-r*.4} {cx-r*1.1} {top-r*.1} {cx} {top-r*.1}C{cx+r*1.1} {top-r*.1} {cx+r*1.3} {cy-r*.4} {cx+r*1.1} {cy+r*1.6}Z",
                     cheveux, che_ink, che_cls))
    els.append(W(f"M{cx-larg} 20C{cx-larg} {epy+5} {cx-larg*.6} {epy} {cx} {epy}C{cx+larg*.6} {epy} {cx+larg} {epy+5} {cx+larg} 20Z",
                 haut, haut_ink, haut_cls))
    els.append(W(circ(cx, cy, r), peau, 'jaune'))
    if style in ('court', 'long', 'chignon', 'nattes'):
        els.append(W(f"M{cx-r*1.02} {cy-r*.1}C{cx-r*1.1} {cy-r*1.1} {cx-r*.6} {top-r*.12} {cx} {top-r*.12}C{cx+r*.6} {top-r*.12} {cx+r*1.1} {cy-r*1.1} {cx+r*1.02} {cy-r*.1}C{cx+r*.6} {cy-r*.65} {cx-r*.6} {cy-r*.65} {cx-r*1.02} {cy-r*.1}Z",
                     cheveux, che_ink, che_cls))
    if style == 'chignon':
        els.append(W(circ(cx, top - r * .25, r * .45), cheveux, che_ink, che_cls))
    if style == 'nattes':
        els.append(W(circ(cx - r * 1.05, cy + r * .2, r * .32), cheveux, che_ink, che_cls))
        els.append(W(circ(cx + r * 1.05, cy + r * .2, r * .32), cheveux, che_ink, che_cls))
    els += yeux(cx, cy + r * .05, r * .38, max(.9, r * .17))
    els.append(sourire(cx, cy + r * .42, r * .32))
    return els

V['copains'] = (buste(-8.5, -9, 6.3, 'peau-a', 'cheveux-a', 'copain-1', 'jaune', 'court', 'orange', 8)
                + buste(9, -10, 6.3, 'peau-b', 'cheveux-b', 'copain-2', 'bleu', 'nattes', 'vert', 8, 'jaune', 'orange'))
V['parents'] = (buste(-8.5, -14, 6.6, 'peau-d', 'cheveux-a', 'papa', 'bleu', 'court', '', 9)
                + buste(9, -14, 6.3, 'peau-c', 'cheveux-c', 'maman', 'rose', 'long', '', 9, 'rose', 'brun'))
V['mamie'] = buste(0, -14, 8, 'peau-b', 'gris', 'mamie', 'rose', 'chignon', 'pastel', 13, 'bleu', 'pastel') + [
    F("M-1.4-5.5H1.4", BRUN),
    ('F', "M-6.2-5.5C-6.2-7.3-1.6-7.3-1.6-5.5C-1.6-3.7-6.2-3.7-6.2-5.5ZM1.6-5.5C1.6-7.3 6.2-7.3 6.2-5.5C6.2-3.7 1.6-3.7 1.6-5.5Z", BRUN, 'lunettes'),
    N(-5, 7.5, 1.2), N(-2.5, 8.6, 1.2), N(0, 9, 1.2), N(2.5, 8.6, 1.2), N(5, 7.5, 1.2),
]
V['maitresse'] = [
    W(rr(-19, -18, 22, 16, 1.5), 'tableau', 'bleu', 'vert-fonce'),
    F("M-15.5-6L-12.5-14L-9.5-6M-14.3-9H-10.7M-6.5-14V-6M-6.5-14C-2.5-14-2.5-10-6.5-10C-2-10-2-6-6.5-6", BLANC),
] + buste(8, -10, 6.3, 'peau-c', 'cheveux-a', 'maitresse', 'jaune', 'chignon', 'orange', 9) + [
    T("M2 13L-5-1", 'bois', 'rose', 1.6),
]

V['ri'] = [
    W(circ(0, 0, 16), 'visage', 'jaune'),
    W(ell(-9.5, 4, 3.5, 2.4), 'joue', 'rose', 'pastel'),
    W(ell(9.5, 4, 3.5, 2.4), 'joue', 'rose', 'pastel'),
    ('F', "M-9.5-4Q-6.5-8.5-3.5-4M3.5-4Q6.5-8.5 9.5-4", BRUN, 'epais'),
    W("M-8 1.5C-7 13 7 13 8 1.5Z", 'bouche', 'rose', 'brun'),
    W("M-4 7.8C-3 10.8 3 10.8 4 7.8C2 6.4-2 6.4-4 7.8Z", 'joue', 'rose'),
    W(goutte(-14.5, -1, 1.6), 'eau', 'bleu', 'reserve'),
    W(goutte(14.5, -1, 1.6), 'eau', 'bleu', 'reserve'),
]

V['peur'] = [
    W(circ(0, 0, 16), 'visage-peur', 'bleu', 'pastel'),
    W(circ(-6, -3, 4.6), 'blanc-oeil', 'jaune', 'reserve'),
    W(circ(6, -3, 4.6), 'blanc-oeil', 'jaune', 'reserve'),
    N(-6, -2.4, 1.9, 'brun'), N(6, -2.4, 1.9, 'brun'),
    ('F', "M-10.5-10Q-6.5-13-2.5-10.5M2.5-10.5Q6.5-13 10.5-10", BRUN, 'epais'),
    W(ell(0, 8.5, 3.2, 4.2), 'roue', 'bleu'),
    W(goutte(12.5, -10.5, 1.8), 'eau', 'bleu', 'reserve'),
]

V['fache'] = [
    W(circ(0, 0, 16), 'fache', 'rose', 'orange'),
    T("M-11-8.5L-3-5.5M11-8.5L3-5.5", 'roue', 'bleu', 2.4),
    N(-6, -1.5, 1.9, 'brun'), N(6, -1.5, 1.9, 'brun'),
    ('F', "M-6.5 9.5Q0 4 6.5 9.5", BRUN, 'epais'),
    W(circ(-13, -15, 3) + circ(-16.5, -12.5, 2.2), 'nuage', 'bleu', 'pastel'),
    W(circ(13, -15, 3) + circ(16.5, -12.5, 2.2), 'nuage', 'bleu', 'pastel'),
]

V['calin'] = [
    W("M0 15C-6 10-15 5-15-3C-15-9-10-12-6-12C-3-12-1-10 0-8C1-10 3-12 6-12C10-12 15-9 15-3C15 5 6 10 0 15Z", 'coeur', 'rose'),
    F("M-9-6Q-8.5-8.5-6-9", BLANC),
    T("M-18.5-3C-15 8-5 10 1.5 6", 'peau-d', 'jaune', 3.6),
    T("M18.5-3C15 8 5 10-1.5 6", 'peau-a', 'jaune', 3.6),
    W(circ(1.8, 5.8, 2.6), 'peau-d', 'jaune'),
    W(circ(-1.8, 5.8, 2.6), 'peau-a', 'jaune'),
]

V['chanson'] = [
    F("M-18-7Q0-11 18-7M-18-2Q0-6 18-2M-18 3Q0-1 18 3", SABLE),
    W(ell(-8, 9.5, 4, 3), 'notes', 'bleu'),
    T("M-4.3 9V-11Q1-9 1.5-3.5", 'notes', 'bleu', 1.9),
    W(ell(6, 7, 3.6, 2.8), 'notes', 'bleu'),
    W(ell(14, 4, 3.6, 2.8), 'notes', 'bleu'),
    T("M9.3 7V-11.5M17.3 4V-14.5", 'notes', 'bleu', 1.8),
    T("M9.3-11.5L17.3-14.5", 'notes', 'bleu', 3.2),
]

V['doudou'] = [
    W("M-5-6C-8-12-9-19-6-20C-3-20-2-13-2-6ZM3-6C3-13 4-20 7-19.5C10-19 8-12 5-6Z", 'doudou', 'jaune', 'pastel'),
    W("M-5-8C-6.5-12-7-17-6-17.5C-4.5-17.5-3.6-13-3.5-8ZM4-8C4-13 5-17.5 6.5-17C7.5-16 6.5-12 5-8Z", 'joue', 'rose', 'pastel'),
    W("M-9 18C-11 12-8 5 0 5C8 5 11 12 9 18Z", 'doudou', 'jaune', 'pastel'),
    W(circ(0, -1.5, 7.2), 'doudou', 'jaune', 'pastel'),
    W(ell(-7, 17, 3, 2), 'doudou', 'jaune', 'pastel'),
    W(ell(7, 17, 3, 2), 'doudou', 'jaune', 'pastel'),
    F("M-4.2-2.6Q-2.7-1.1-1.2-2.6M1.2-2.6Q2.7-1.1 4.2-2.6", BRUN),
    N(0, 1, 1.2, 'brun'),
    W("M0 5.5L-5 3V8ZM0 5.5L5 3V8Z", 'cerise', 'rose'),
]

# ---------------------------------------------------------------------------
# Décors Dehors (~90 px, centrés sur l'emplacement)

def agrandi(slug, s=2.25, dx=0, dy=0):
    """La vignette, tracés multipliés (jamais de transform sur un .w)."""
    return [rendu(el, s, dx, dy, fil_s=1.6, filtre='mini') for el in V[slug]]

def personne(cx, H, peau, cheveux, haut, haut_ink, bas, style='court', robe=False,
             haut_cls='', che_ink='bleu', che_cls='', enfant=False, sol=45):
    """Une silhouette debout, de face, pieds sur y = sol."""
    r = H * (.15 if enfant else .12)
    cy = sol - H + r
    cou = cy + r
    hanche = cou + H * (.30 if enfant else .34)
    ep = H * (.2 if enfant else .19)
    els = []
    if style == 'long':
        els.append(W(f"M{cx-r*1.15} {cy+r*2.1}C{cx-r*1.35} {cy-r*.4} {cx-r*1.1} {cy-r*1.1} {cx} {cy-r*1.1}C{cx+r*1.1} {cy-r*1.1} {cx+r*1.35} {cy-r*.4} {cx+r*1.15} {cy+r*2.1}Z",
                     cheveux, che_ink, che_cls))
    # jambes et chaussures
    jx = ep * .42
    els.append(T(f"M{cx-jx} {hanche-2}V{sol-2}M{cx+jx} {hanche-2}V{sol-2}", bas, 'bleu', H * .085))
    els.append(W(ell(cx - jx - 1, sol - 1.2, H * .055, H * .028), 'roue', 'bleu'))
    els.append(W(ell(cx + jx + 1, sol - 1.2, H * .055, H * .028), 'roue', 'bleu'))
    # bras
    els.append(T(f"M{cx-ep+1} {cou+3}Q{cx-ep-3} {cou+H*.18} {cx-ep-1.5} {hanche+1}M{cx+ep-1} {cou+3}Q{cx+ep+3} {cou+H*.18} {cx+ep+1.5} {hanche+1}",
                 haut, haut_ink, H * .075, haut_cls))
    els.append(W(circ(cx - ep - 1.5, hanche + 2, H * .035), peau, 'jaune'))
    els.append(W(circ(cx + ep + 1.5, hanche + 2, H * .035), peau, 'jaune'))
    # le haut (ou la robe, jusqu'aux genoux)
    bas_y = hanche + (H * .2 if robe else 2)
    lb = ep * (1.25 if robe else 1)
    els.append(W(f"M{cx-lb} {bas_y}L{cx-ep} {cou+r*.5}C{cx-ep} {cou} {cx-ep*.5} {cou-1} {cx} {cou-1}C{cx+ep*.5} {cou-1} {cx+ep} {cou} {cx+ep} {cou+r*.5}L{cx+lb} {bas_y}Z",
                 haut, haut_ink, haut_cls))
    # tête, cheveux, visage
    els.append(W(circ(cx, cy, r), peau, 'jaune'))
    els.append(W(f"M{cx-r*1.03} {cy-r*.05}C{cx-r*1.1} {cy-r*1.1} {cx-r*.6} {cy-r*1.13} {cx} {cy-r*1.13}C{cx+r*.6} {cy-r*1.13} {cx+r*1.1} {cy-r*1.1} {cx+r*1.03} {cy-r*.05}C{cx+r*.6} {cy-r*.62} {cx-r*.6} {cy-r*.62} {cx-r*1.03} {cy-r*.05}Z",
                 cheveux, che_ink, che_cls))
    if style == 'chignon':
        els.append(W(circ(cx, cy - r * 1.2, r * .45), cheveux, che_ink, che_cls))
    if style == 'nattes':
        els.append(W(circ(cx - r * 1.1, cy + r * .3, r * .34), cheveux, che_ink, che_cls))
        els.append(W(circ(cx + r * 1.1, cy + r * .3, r * .34), cheveux, che_ink, che_cls))
    els += yeux(cx, cy + r * .05, r * .37, max(1.1, r * .14))
    els.append(sourire(cx, cy + r * .42, r * .32))
    return els, cy, r

def d_gens(*figs):
    out = []
    for els in figs:
        out += [rendu(e, filtre='mini') for e in els]
    return out

D = {}
for slug, s, dy in [('glace', 2.2, 0), ('chien', 2.1, 3), ('velo', 2.2, 0), ('piscine', 2.4, 0), ('gateau', 2.1, 0),
                    ('tracteur', 2.3, 0), ('manege', 2.3, 0), ('doudou', 1.9, 6)]:
    D[slug] = agrandi(slug, s, 0, dy)
# l'orage : à #slot-2 (780,350), le nuage est dans le ciel à droite du pouce
# géant (centre ≈ (814,160)), l'éclair s'arrête sur le toit de l'expo
D['orage'] = agrandi('orage', 1.8, 34, -176)

kid1, _, _ = personne(-15, 70, 'peau-a', 'cheveux-a', 'copain-1', 'jaune', 'jean', 'court', haut_cls='orange', enfant=True)
kid2, _, _ = personne(14, 74, 'peau-b', 'cheveux-b', 'copain-2', 'bleu', 'jean', 'nattes', robe=True, haut_cls='vert',
                      che_ink='jaune', che_cls='orange', enfant=True)
D['copains'] = d_gens(kid1, kid2)
papa, _, _ = personne(-14, 98, 'peau-d', 'cheveux-a', 'papa', 'bleu', 'jean', 'court')
maman, _, _ = personne(15, 92, 'peau-c', 'cheveux-c', 'maman', 'rose', 'jean', 'long', robe=True, che_ink='rose', che_cls='brun')
D['parents'] = d_gens(papa, maman)
mamie, mcy, mr = personne(0, 86, 'peau-b', 'gris', 'mamie', 'rose', 'jean', 'chignon', robe=True, haut_cls='pastel',
                          che_ink='bleu', che_cls='pastel')
D['mamie'] = d_gens(mamie) + [
    rendu(('F', f"M-{mr*.62} {mcy}C-{mr*.62} {mcy-mr*.36} -{mr*.12} {mcy-mr*.36} -{mr*.12} {mcy}C-{mr*.12} {mcy+mr*.36} -{mr*.62} {mcy+mr*.36} -{mr*.62} {mcy}Z"
                 f"M{mr*.12} {mcy}C{mr*.12} {mcy-mr*.36} {mr*.62} {mcy-mr*.36} {mr*.62} {mcy}C{mr*.62} {mcy+mr*.36} {mr*.12} {mcy+mr*.36} {mr*.12} {mcy}Z"
                 f"M-{mr*.12} {mcy-mr*.05}H{mr*.12}", BRUN, 'lunettes')),
    rendu(T("M19 44L21 0Q21-5 16-5", 'bois', 'rose', 2.6), filtre='mini'),
]
maitresse, _, _ = personne(0, 94, 'peau-c', 'cheveux-a', 'maitresse', 'jaune', 'jean', 'chignon', robe=True, haut_cls='orange')
D['maitresse'] = d_gens(maitresse) + [
    rendu(W(rr(-30, -6, 13, 17, 1.5), 'livre', 'rose'), filtre='mini'),
    rendu(F("M-23.5-4V9", BLANC)),
]

# Le pouce de César : bronze, ongle, plis. Posé à #slot-1 (700,300), dessiné
# ci-dessous à l'échelle 1 (socle à y local 152, ongle à −104) puis agrandi ×1,65
# autour du bas du socle : le socle reste à y 452 de la scène (au-dessus de la
# boîte, qui commence à 470), l'ongle monte à y ≈ 30, plus haut que la tête de
# l'enfant (≈ 12–330 de sommet à menton : il la dépasse de toute sa hauteur
# au-dessus du sol, y ≈ 404). Il couvre l'expo et son drapeau : c'est voulu.
POUCE_S = 1.65   # le pouce dépasse la tête de l'enfant : ongle à y ≈ 30 de la scène
D['pouce'] = [rendu(e, POUCE_S, 0, 152 * (1 - POUCE_S), fil_s=1.6, filtre='mini') for e in [
    W(rr(-66, 136, 132, 16, 4), 'socle', 'bleu', 'pastel'),
    F("M-60 144H60", SABLE),
    # riso : une sous-couche de papier, sinon l'expo se voit au travers du grain d'encre
    ('P', "M-54 140C-52 100-48 70-49 40C-50 15-44 0-45-20C-46-50-42-75-30-90C-18-104 18-106 30-92C42-78 46-52 45-25"
      "C44 0 50 15 49 40C48 70 52 100 56 140Z"),
    W("M-54 140C-52 100-48 70-49 40C-50 15-44 0-45-20C-46-50-42-75-30-90C-18-104 18-106 30-92C42-78 46-52 45-25"
      "C44 0 50 15 49 40C48 70 52 100 56 140Z", 'bronze', 'jaune', 'brun'),
    # ombre : le flanc droit, loin de la lumière
    W("M24-96C40-84 46-56 45-25C44 0 50 15 49 40C48 70 52 100 56 140H36C38 100 35 70 36 40C37 15 32 0 33-25C34-55 32-80 24-96Z",
      'bronze-ombre', 'rose', 'pastel'),
    # reflet : le bronze poli, côté lumière
    W("M-30-70C-36-46-33-20-34 4C-35 40-30 90-34 132H-24C-22 90-26 40-24 4C-23-20-26-46-22-74Z", 'bronze-clair', 'jaune', 'pastel'),
    # l'ongle, en haut : la plaque, son bord libre plus clair, la peau qui l'entoure
    W("M-25-78C-25-99 25-99 25-78L24-50C23-40 16-35 0-35C-16-35-23-40-24-50Z", 'bronze-clair', 'jaune'),
    W("M-24-82C-21-98 21-98 24-82C12-87-12-87-24-82Z", 'ongle', 'jaune', 'pastel'),
    F("M-29-52C-27-34 27-34 29-52", BRUN),
    F("M-18-74Q-17-60-16-48", BLANC),
    # les plis de la phalange et la base du pouce
    F("M-42-6Q-12 4 38-6M-38 6Q-6 16 40 4M-36 18Q-4 26 34 16", BRUN),
    F("M-44 92Q0 104 46 92M-40 104Q-4 112 40 104", BRUN),
]]

# Petites portes d'entrée au bas des cartes : un œil, une oreille (brodés)
IC = {
    'oeil': ['<path class="fil" style="--f:var(--fil-brun)" d="M-6 0Q0-5 6 0Q0 5-6 0Z"/>',
             '<circle class="noeud-brun" cx="0" cy="0" r="1.8"/>'],
    'oreille': ['<path class="fil" style="--f:var(--fil-brun)" d="M-3 4.5C-5 2-5.5-5 0-5.5C4-6 5.5-2 3.5 1C2.5 2.5 1 2.5 1 4.5C1 6-1.5 6.5-3 4.5ZM-1-1.5C-1-3 2-3 1.5-.5"/>'],
}

def bloc():
    L = ['<!-- CARTES-BEGIN -->',
         '<!-- ===== Cartes-souvenirs (Task 8) : généré par tools/gen-cartes.py, ne pas retoucher à la main =====',
         '     #v-<slug> : vignette 40 × 40 centrée sur (0,0) ; #d-<slug> : décor Dehors centré sur son emplacement ;',
         '     #ic-oeil / #ic-oreille : la porte d\'entrée brodée au bas de la carte. Pièces .w.lite seulement. -->',
         '<g id="g-cartes-assets">']
    for k, els in IC.items():
        L.append(f'<symbol id="ic-{k}" overflow="visible">' + ''.join(els) + '</symbol>')
    for slug, els in V.items():
        L.append(f'<symbol id="v-{slug}" overflow="visible">')
        L += ['  ' + rendu(e) for e in els]
        L.append('</symbol>')
    for slug, els in D.items():
        L.append(f'<symbol id="d-{slug}" overflow="visible">')
        L += ['  ' + e for e in els]
        L.append('</symbol>')
    L.append('</g>')
    L.append('<!-- CARTES-END -->')
    return '\n'.join('          ' + l for l in L) + '\n'

if __name__ == '__main__':
    racine = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    chemin = os.path.join(racine, 'index.html')
    src = open(chemin, encoding='utf-8').read()
    b = bloc()
    if '--sec' in sys.argv:
        print(len(b.encode()), 'octets,', len(V), 'vignettes,', len(D), 'décors')
        sys.exit(0)
    m = re.search(r' *<!-- CARTES-BEGIN -->.*?<!-- CARTES-END -->\n', src, re.S)
    if m:
        src = src[:m.start()] + b + src[m.end():]
    else:
        # première fois : juste avant la fin du premier <defs> de la scène
        i = src.index('        </defs>\n\n        <!-- Tous les groupes')
        src = src[:i] + b + src[i:]
    open(chemin, 'w', encoding='utf-8').write(src)
    print('index.html : bloc des cartes écrit,', len(b.encode()), 'octets')

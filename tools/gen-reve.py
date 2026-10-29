#!/usr/bin/env python3
# Générateur des dessins du rêve de index.html (Task 10).
# Outil de dessin, PAS livré : index.html reste le seul fichier livré.
#
# Écrit deux blocs dans index.html :
#   1. dans <defs>, <!-- REVE-BEGIN --> … <!-- REVE-END --> :
#      - #g-base-<forme> : la grande forme de rêve d'une carte (≈ 120 px, centrée
#        sur (0,0)) : sa vignette (tools/gen-cartes.py) aux tracés multipliés par 3.
#        data-tete="x y s[;x y s]" : où se pose la tête d'une greffe (une ou deux
#        têtes : les copains, papa et maman), s = échelle de la greffe ;
#        data-corps="x y s" : le milieu du corps (ailes, roues, queue, cornet…) ;
#      - #g-greffe-<forme> : l'attribut de rêve d'une carte, dessiné en deux
#        parties, <g class="a-tete"> (autour d'une tête de rayon ≈ 22 centrée en
#        (0,0)) et <g class="a-corps"> (autour du corps), que le CSS place par des
#        variables posées sur le <use> (--tete-x/-y/-s, --corps-x/-y/-s) : une
#        variable traverse le clone du <use>, une classe d'ancêtre non ;
#      - #g-greffe-<forme>-dos : ce qui passe DERRIÈRE la base (les ailes du
#        dragon, le cornet de la glace, la queue du chien, le mât du manège) ;
#      - #g-reve-flou : le rêve tout flou d'une journée vide ;
#      - #clip-ecran / #clip-ecran-grand : le cadre de l'écran (le nuage), et le
#        cadre agrandi par où le géant déborde.
#   2. dans la scène, le contenu de #g-ecran, <!-- ECRAN-BEGIN --> … <!-- ECRAN-END --> :
#      le nuage-écran #p-ecran (UNE pièce de laine complète, épinglée en haut à
#      droite), #g-reve (le film), le bouton #encore, la légende #t-phrase (et la
#      phrase-clé #t-cle), la place de la carte réconfort #g-reconfort (Task 11) ;
#   3. dans #g-ui, <!-- TELECOMMANDE-BEGIN --> … <!-- TELECOMMANDE-END --> : la
#      télécommande #telecommande (Task 11).
# Toutes les pièces des dessins sont des .w.lite (filtre #woolMini), jamais de
# transform sur un .w. Reprend les aides et les vignettes de tools/gen-cartes.py.
#
# Usage (depuis la racine du dépôt) :
#   python3 tools/gen-reve.py          # réécrit les deux blocs dans index.html
#   python3 tools/gen-reve.py --sec    # n'écrit rien, affiche la taille des blocs
import importlib.util, math, os, re, sys

ICI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('gen_cartes', os.path.join(ICI, 'gen-cartes.py'))
GC = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(GC)
f, circ, ell, rr, goutte, anneau = GC.f, GC.circ, GC.ell, GC.rr, GC.goutte, GC.anneau
W, T, F, N, rendu, V = GC.W, GC.T, GC.F, GC.N, GC.rendu, GC.V
BRUN, BLANC, SABLE = GC.BRUN, GC.BLANC, GC.SABLE

def R(el, s=1.0):
    return rendu(el, s, 0, 0, fil_s=1.6 if s != 1 else 1.0, filtre='mini')

def miroir(d):
    """Retourne un tracé gauche-droite (x → −x) : commandes absolues M L C Q H Z seulement."""
    out, cmd, idx = [], None, 0
    for tok in re.findall(r'[A-Za-z]|-?\d*\.?\d+', d):
        if tok.isalpha():
            cmd, idx = tok, 0
            out.append(tok)
            continue
        v = float(tok)
        if cmd in 'MLCQT' and idx % 2 == 0: v = -v
        if cmd == 'H': v = -v
        idx += 1
        out.append(f(v))
    r = ''
    for t in out:
        if r and not t[0].isalpha() and not r[-1].isalpha() and not t.startswith('-'):
            r += ' '
        r += t
    return r

# ---------------------------------------------------------------------------
# 1. Les bases : la vignette × 3 (≈ 120 px), et où poser la greffe
BASE_S = 3
ANCRES = {   # forme : (têtes [(x, y, s)…], corps (x, y, s)), en unités de la base
    'pouce':     ([(0, 0, 1)], (0, 0, 1)),
    'glace':     ([(0, -24, 1)], (0, 6, 1)),
    'chien':     ([(24, -27, 1)], (-12, 24, 1)),
    'velo':      ([(0, 0, .85)], (0, 10, 1)),
    'piscine':   ([(0, 24, .9)], (0, 8, 1)),
    'gateau':    ([(0, 18, .9)], (0, 6, 1)),
    'tracteur':  ([(-20, -30, .75)], (0, 6, 1)),
    'orage':     ([(0, -12, 1.1)], (0, 0, 1)),
    'manege':    ([(3, 9, .75)], (0, 6, 1)),
    'copains':   ([(-25.5, -8.1, .86), (27, -11.1, .86)], (0, 15, 1)),
    'parents':   ([(-25.5, -22.2, .9), (27, -23.1, .86)], (0, 10, 1)),
    'mamie':     ([(0, -18, 1.09)], (0, 10, 1)),
    'maitresse': ([(24, -11.1, .86)], (0, 10, 1)),
    'doudou':    ([(0, -4.5, .98)], (0, 10, 1)),
    'calin':     ([(0, 0, 1)], (0, 0, 1)),
}

def ancre(t):
    return ' '.join(f(v) for v in t)

def bases():
    L = []
    for forme, (tetes, corps) in ANCRES.items():
        L.append(f'<symbol id="g-base-{forme}" overflow="visible" data-tete="{";".join(ancre(t) for t in tetes)}" data-corps="{ancre(corps)}">')
        L += ['  ' + R(e, BASE_S) for e in V[forme]]
        L.append('</symbol>')
    return L

# ---------------------------------------------------------------------------
# 2. Les greffes : tête (autour de (0,0), tête de rayon ≈ 22) et corps
def tete_enfant(cx, cy, r, peau, cheveux, che_ink='bleu', che_cls=''):
    """Une petite tête de face (les copains qui surgissent)."""
    top = cy - r
    return [
        W(circ(cx, cy, r), peau, 'jaune'),
        W(f"M{cx-r*1.03} {cy-r*.05}C{cx-r*1.1} {cy-r*1.1} {cx-r*.6} {top-r*.13} {cx} {top-r*.13}C{cx+r*.6} {top-r*.13} {cx+r*1.1} {cy-r*1.1} {cx+r*1.03} {cy-r*.05}C{cx+r*.6} {cy-r*.62} {cx-r*.6} {cy-r*.62} {cx-r*1.03} {cy-r*.05}Z",
          cheveux, che_ink, che_cls),
        N(cx - r * .37, cy + r * .05, max(1.4, r * .15), 'brun'), N(cx + r * .37, cy + r * .05, max(1.4, r * .15), 'brun'),
        F(f"M{cx-r*.34} {cy+r*.4}Q{cx} {cy+r*.72} {cx+r*.34} {cy+r*.4}", BRUN),
    ]

OREILLE_CHIEN = "M-15-15C-25-19-33-9-31 6C-30 13-24 15-21 9C-19 2-17-7-13-13Z"
AILE = "M-22-6C-38-40-70-48-88-22C-78-26-68-22-64-14C-58-22-48-22-44-12C-38-18-30-16-26-6Z"
OREILLE_LAPIN = "M-15-15C-22-34-22-54-13-56C-4-56-4-36-7-17Z"
OREILLE_LAPIN_IN = "M-13-20C-17-34-17-49-12-50C-8-50-8-36-9-21Z"
NUAGE = "M-26-30C-32-30-32-40-26-42C-26-50-16-54-10-48C-6-56 6-56 10-48C16-54 26-50 25-42C32-41 32-30 25-30Z"

G = {}   # forme : {'tete': [...], 'corps': [...], 'dos': [...]}

G['ogre'] = {'tete': [
    W(ell(-23, -1, 7, 10), 'ogre', 'jaune', 'vert'), W(ell(23, -1, 7, 10), 'ogre', 'jaune', 'vert'),
    W(ell(-24, 0, 3.4, 5.5), 'bouche', 'rose', 'brun'), W(ell(24, 0, 3.4, 5.5), 'bouche', 'rose', 'brun'),
    W(ell(0, 1, 22, 21), 'ogre', 'jaune', 'vert'),
    F("M-6-19Q-4-24-1-20M2-20Q5-25 7-19", BRUN),
    W(circ(-8, -3, 5.6), 'blanc-oeil', 'jaune', 'reserve'), W(circ(8, -3, 5.6), 'blanc-oeil', 'jaune', 'reserve'),
    N(-7, -2.4, 2.5, 'brun'), N(9, -2.4, 2.5, 'brun'),
    T("M-16-12L-4-8M4-8L16-12", 'roue', 'bleu', 3.8),
    F("M-1.5 1C-3 5.5 2 6.5 2.5 3", BRUN),
    W("M-12 8C-7 18 7 18 12 8C6 11-6 11-12 8Z", 'bouche', 'rose', 'brun'),
    W("M-8 9.5L-6 15L-4 10.5ZM4 10.5L6 15L8 9.5Z", 'blanc-oeil', 'jaune', 'reserve'),
    N(14, 9, 1.6, 'brun'), N(-15, 12, 1.2, 'brun'),
]}

G['pirate'] = {'tete': [
    W("M-31-13C-25-22-15-38 0-38C15-38 25-22 31-13C18-19-18-19-31-13Z", 'pirate', 'bleu'),
    F("M-27-15.5Q0-23 27-15.5", SABLE),
    W(circ(0, -27, 4.6), 'blanc-oeil', 'jaune', 'reserve'),
    N(-1.6, -27.6, 1.1, 'brun'), N(1.6, -27.6, 1.1, 'brun'),
    F("M-5-21L5-17M-5-17L5-21", BLANC),
    F("M-21-13L20 5", BRUN),
    W(ell(8, -2, 6.5, 5.5), 'pirate', 'bleu'),
], 'corps': [
    W("M44 32C58 10 60-14 50-38C56-14 54 10 41 30Z", 'gris', 'bleu', 'pastel'),
    F("M47 26C56 8 57-12 51-32", BLANC),
    T("M34 28L50 38", 'or', 'jaune', 5),
    T("M42 33L37 44", 'bois', 'rose', 4.4),
    N(50, 38, 2.4),
]}

G['dragon'] = {'dos': [
    W(AILE, 'dragon', 'bleu', 'vert'), W(miroir(AILE), 'dragon', 'bleu', 'vert'),
    F("M-30-14L-60-34M-44-12L-68-26M30-14L60-34M44-12L68-26", '--fil-blanc'),
], 'tete': [
    W("M-14-18L-12-32L-6-20ZM14-18L12-32L6-20Z", 'piquant', 'jaune', 'orange'),
    W("M20 4C30-6 42-4 46 2C54-2 60 4 56 10C62 14 56 20 48 16C44 22 32 20 28 12C24 12 20 8 20 4Z", 'flamme', 'jaune', 'reserve'),
    W("M26 6C32 2 38 4 40 8C44 6 48 10 44 13C40 16 34 15 32 12C29 12 26 9 26 6Z", 'piquant', 'jaune', 'orange'),
]}

G['glace'] = {'dos': [
    W("M-27 38H27L2.5 98Q0 102-2.5 98Z", 'cornet', 'jaune', 'orange'),
    F("M-18 44L10 80M2 42L18 62M18 44L-10 80M-2 42L-18 62", BRUN),
], 'tete': [
    W("M-25-20C-30-31-22-45-8-46C0-51 11-48 15-43C26-41 30-30 25-20C21-15 17-20 12-17C8-14 4-19 0-16C-4-13-8-18-12-15C-16-12-21-16-25-20Z",
      'glace-rose', 'rose', 'pastel'),
    W(circ(3, -50, 5.4), 'cerise', 'rose'),
    F("M-16-33Q-13-41-5-42", BLANC),
    W("M-19-19C-19-9-16-4-15-4C-14-4-12-9-12-17Z", 'glace-rose', 'rose', 'pastel'),
    W("M12-17C12-7 14-1 15.5-1C17-1 18-7 18-19Z", 'glace-rose', 'rose', 'pastel'),
    W(goutte(16, 9, 2.6), 'glace-rose', 'rose', 'pastel'),
]}

G['chien'] = {'dos': [
    ('REMUE', [T("M-50 14Q-72 6-68-18", 'chien', 'jaune', 7, 'orange')]),
], 'tete': [
    W(OREILLE_CHIEN, 'chien-oreille', 'rose', 'brun'), W(miroir(OREILLE_CHIEN), 'chien-oreille', 'rose', 'brun'),
    W(ell(0, 5, 6.5, 4.8), 'roue', 'bleu'),
    N(-1.8, 3.6, 1.3, 'blanc'),
    W("M-3.5 11C-3.5 19 3.5 19 3.5 11Z", 'cerise', 'rose'),
]}

G['anniversaire'] = {'tete': [
    W(rr(-14, -39, 6, 16, 2), 'bougie', 'bleu'), W(rr(-3, -44, 6, 20, 2), 'bougie', 'bleu'), W(rr(8, -39, 6, 16, 2), 'bougie', 'bleu'),
    F("M-14-33L-8-31M-3-38L3-36M8-33L14-31", BLANC),
    W(goutte(-11, -43, 2.6), 'flamme', 'jaune', 'reserve'), W(goutte(0, -48, 2.6), 'flamme', 'jaune', 'reserve'),
    W(goutte(11, -43, 2.6), 'flamme', 'jaune', 'reserve'),
], 'corps': [
    F("M-56-22Q0 14 56-22", BRUN),
] + [W(f"M{x-6} {y}L{x+6} {y}L{x} {y+11}Z", c, ink) for (x, y, c, ink) in [
    (-42, -11.5, 'cerise', 'rose'), (-21, -2.5, 'bougie', 'bleu'), (0, .5, 'flamme', 'jaune'), (21, -2.5, 'cerise', 'rose'), (42, -11.5, 'bougie', 'bleu')]]}

G['orage'] = {'tete': [
    W(NUAGE, 'nuage', 'bleu', 'pastel'),
    W("M3-33L-6-18H0L-5-4L9-22H3L7-33Z", 'eclair', 'jaune', 'reserve'),
    F("M-18-26L-21-21M18-26L15-21", '--fil-vague'),
], 'corps': [
    W("M-52-12L-60 4H-54L-60 18L-46-2H-52L-48-12Z", 'eclair', 'jaune', 'reserve'),
    W("M56 4L48 20H54L48 34L62 14H56L60 4Z", 'eclair', 'jaune', 'reserve'),
]}

G['pouce'] = {'tete': [
    W("M-23-12C-23-42 23-42 23-12L21-5C14-9-14-9-21-5Z", 'bronze-clair', 'jaune', 'brun'),
    W("M-21-20C-17-38 17-38 21-20C10-25-10-25-21-20Z", 'ongle', 'jaune', 'pastel'),
    F("M-23-12C-23-42 23-42 23-12L21-5C14-9-14-9-21-5Z", BRUN),
    F("M-12-30Q-14-22-13-14", BLANC),
]}

G['copains'] = {'corps': tete_enfant(-50, -38, 13, 'peau-a', 'cheveux-a')
                + tete_enfant(50, -40, 13, 'peau-b', 'cheveux-b', 'jaune', 'orange')}

G['ri'] = {'tete': [
    ('F', "M-14-4Q-9-11-4-4M4-4Q9-11 14-4", BRUN, 'epais'),
    W(ell(-15, 4, 5.5, 3.6), 'joue', 'rose', 'pastel'), W(ell(15, 4, 5.5, 3.6), 'joue', 'rose', 'pastel'),
    W("M-14 3C-12 21 12 21 14 3C6 7-6 7-14 3Z", 'bouche', 'rose', 'brun'),
    W("M-10 5C-5 8 5 8 10 5L9 8.5C4 10.5-4 10.5-9 8.5Z", 'blanc-oeil', 'jaune', 'reserve'),
    W("M-5 15C-3 17.5 3 17.5 5 15C3 13.5-3 13.5-5 15Z", 'joue', 'rose'),
]}

G['peur'] = {'tete': [
    W(circ(-9, -3, 8.4), 'blanc-oeil', 'jaune', 'reserve'), W(circ(9, -3, 8.4), 'blanc-oeil', 'jaune', 'reserve'),
    N(-9, -2, 2.3, 'brun'), N(9, -2, 2.3, 'brun'),
    ('F', "M-17-16Q-10-23-3-16M3-16Q10-23 17-16", BRUN, 'epais'),
    W(ell(0, 12, 4, 5.4), 'roue', 'bleu'),
    W(goutte(22, -12, 2.8), 'eau', 'bleu', 'reserve'),
]}

G['fache'] = {'tete': [
    N(-8.5, -1, 2.6, 'brun'), N(8.5, -1, 2.6, 'brun'),
    ('F', "M-8 13Q0 6 8 13", BRUN, 'epais'),
    T("M-17-13L-3-6M17-13L3-6", 'roue', 'bleu', 4.6),
    W(circ(-25, -26, 6) + circ(-31, -20, 4.2), 'nuage', 'bleu', 'pastel'),
    W(circ(25, -26, 6) + circ(31, -20, 4.2), 'nuage', 'bleu', 'pastel'),
]}

G['calin'] = {'corps': [
    T("M-60-14C-58 24-24 36 6 22", 'peau-d', 'jaune', 9),
    T("M60-14C58 24 24 36-6 22", 'peau-a', 'jaune', 9),
    W(circ(6, 22, 6.5), 'peau-d', 'jaune'), W(circ(-6, 22, 6.5), 'peau-a', 'jaune'),
    W("M0-38C-4-42-10-41-10-36C-10-31-4-28 0-24C4-28 10-31 10-36C10-41 4-42 0-38Z", 'coeur', 'rose'),
]}

G['chanson'] = {'tete': [
    W(ell(-30, -14, 5.6, 4.2), 'notes', 'bleu'), T("M-25-15V-38Q-19-35-18-29", 'notes', 'bleu', 2.6),
    W(ell(22, -24, 5, 3.8), 'notes', 'bleu'), W(ell(34, -28, 5, 3.8), 'notes', 'bleu'),
    T("M26.5-25V-46M38.5-29V-50", 'notes', 'bleu', 2.4), T("M26.5-46L38.5-50", 'notes', 'bleu', 4.2),
    W(ell(-6, -40, 4.4, 3.4), 'notes', 'bleu'), T("M-2-41V-58", 'notes', 'bleu', 2.2),
]}

G['doudou'] = {'tete': [
    W(OREILLE_LAPIN, 'doudou', 'jaune', 'pastel'), W(miroir(OREILLE_LAPIN), 'doudou', 'jaune', 'pastel'),
    W(OREILLE_LAPIN_IN, 'joue', 'rose', 'pastel'), W(miroir(OREILLE_LAPIN_IN), 'joue', 'rose', 'pastel'),
]}

G['velo'] = {'corps': [
    W(anneau(-34, 54, 17, 12.5), 'roue', 'bleu', 'evenodd'), W(anneau(34, 54, 17, 12.5), 'roue', 'bleu', 'evenodd'),
    F("M-34 41V67M-47 54H-21M34 41V67M21 54H47", SABLE),
    T("M-34 54L0 40L34 54", 'velo', 'rose', 4),
    N(-34, 54, 2.6), N(34, 54, 2.6),
]}

G['piscine'] = {'tete': [
    T("M-16-2H-27M16-2H27", 'eau', 'bleu', 3),
    W(anneau(-8.5, -2, 7.5, 4.8), 'eau', 'bleu', 'evenodd'), W(anneau(8.5, -2, 7.5, 4.8), 'eau', 'bleu', 'evenodd'),
    F("M-2-3Q0-5 2-3", BRUN),
], 'corps': [
    W(goutte(-50, 30, 4), 'eau', 'bleu', 'reserve'), W(goutte(-60, 14, 3), 'eau', 'bleu', 'reserve'),
    W(goutte(52, 24, 4), 'eau', 'bleu', 'reserve'), W(goutte(60, 40, 3), 'eau', 'bleu', 'reserve'),
]}

G['gateau'] = {'tete': [
    W(rr(-18, -36, 36, 17, 3), 'gateau', 'jaune', 'pastel'),
    W("M-19-36C-19-41 19-41 19-36V-31C17-27 14-32 11-29C8-25 5-31 2-28C-1-25-4-31-7-28C-10-25-13-31-16-28C-18-26-19-29-19-31Z", 'glacage', 'rose', 'pastel'),
    W(rr(-2.5, -50, 5, 13, 1.5), 'bougie', 'bleu'),
    W(goutte(0, -53, 2.6), 'flamme', 'jaune', 'reserve'),
]}

G['tracteur'] = {'corps': [
    W(circ(-36, 42, 23), 'roue', 'bleu'), W(circ(-36, 42, 10), 'moyeu', 'jaune'),
    W(circ(42, 52, 14), 'roue', 'bleu'), W(circ(42, 52, 6), 'moyeu', 'jaune'),
    F("M-52 42H-20M-36 26V58", '--fil-blanc'),
    N(-36, 42, 2.4), N(42, 52, 1.8),
]}

G['manege'] = {'dos': [
    T("M0-92V78", 'or', 'jaune', 5),
    F("M0-80V70", BLANC),
], 'tete': [
    W("M-31-24L0-46L31-24C25-19 19-25 15-20C10-15 5-21 0-17C-5-21-10-15-15-20C-19-25-25-19-31-24Z", 'manege', 'rose', 'pastel'),
    F("M0-45V-20M-15-37L-15-21M15-37L15-21", BLANC),
    N(0, -48, 3),
]}

G['parents'] = {'tete': [
    W("M0 5C-4 0-13 0-18 6C-13 9-4 9 0 7C4 9 13 9 18 6C13 0 4 0 0 5Z", 'cheveux-a', 'bleu'),
    W("M-12-12C-10-16-3-16-2-12C-1-16 6-16 8-12C10-8 4-4-2 0C-8-4-14-8-12-12Z", 'coeur', 'rose'),
]}

G['mamie'] = {'tete': [
    W(circ(0, -27, 10), 'gris', 'bleu', 'pastel'),
    F("M-6-30Q0-25 6-30", SABLE),
    ('F', "M-16-2C-16-8-3-8-3-2C-3 4-16 4-16-2ZM3-2C3-8 16-8 16-2C16 4 3 4 3-2ZM-3-3H3", BRUN, 'epais'),
]}

G['maitresse'] = {'corps': [
    W(rr(34, -34, 40, 30, 2.5), 'tableau', 'bleu', 'vert-fonce'),
    W(rr(31, -37, 46, 36, 3.5) + rr(34, -34, 40, 30, 2.5), 'bois', 'rose', 'evenodd'),
    F("M40-10L45-28L50-10M42-17H48M56-28V-10M56-28C63-28 63-19 56-19C64-19 64-10 56-10", BLANC),
    T("M30 20L58 -2", 'bois', 'rose', 3),
]}

# Les greffes de la télécommande (Task 11, spec §4.6) : jamais tirées par le rêve,
# posées par applyRemote. « lapin » : deux grandes oreilles roses (l'une retombe), un
# nez rose qui remue, des moustaches et une carotte, sur la tête (les ancres de la base) ;
# « chiens-pirates » : deux chiens à chapeau de pirate qui dansent de part et d'autre du
# film (posés sans ancre : --corps-x/-y restent à 0, le centre de l'écran).
OREILLE_G = "M-15-15C-27-38-29-70-17-75C-6-79-4-47-7-17Z"
OREILLE_G_IN = "M-13-21C-21-40-22-63-15-67C-9-69-8-45-9-23Z"
OREILLE_D = "M7-17C5-40 7-60 18-66C27-71 41-64 38-55C36-49 29-52 25-50C20-46 17-33 15-16Z"
OREILLE_D_IN = "M10-22C9-40 11-56 19-61C25-64 33-60 32-56C30-53 26-55 22-53C17-48 15-36 13-22Z"

G['lapin'] = {'tete': [
    ('G', 'oreille-lapin', [W(OREILLE_G, 'glace-rose', 'rose'), W(OREILLE_G_IN, 'calleux', 'rose', 'pastel'),
                            F("M-16-17Q-11-13-6-17", BRUN)], 0, 1),
    ('G', 'oreille-lapin o2', [W(OREILLE_D, 'glace-rose', 'rose'), W(OREILLE_D_IN, 'calleux', 'rose', 'pastel'),
                               F("M6-17Q11-13 16-17", BRUN)], 0, 1),
    F("M-4 5L-18 2M-4 7.5L-18 10.5M4 5L18 2M4 7.5L18 10.5", BRUN),
    ('G', 'nez-lapin', [W(ell(0, 3.5, 3.8, 2.8), 'glace-rose', 'rose'), F("M-1.6 2.6Q-.6 1.9.4 2.4", BLANC)], 0, 1),
    ('G', 'carotte', [W("M3 11C11 6 27 2 35 3C31 9 15 16 5 17Z", 'piquant', 'jaune', 'orange'),
                      F("M14 9L16 12.5M21 6.5L23 10M28 4.5L29.5 7.5", BRUN),
                      T("M34 3Q37-4 43-5M35 4Q41 0 46 3", 'tracteur', 'jaune', 2.6, 'vert')], 0, 1),
]}

def chien_pirate(sens, cache):
    """Un chien debout qui danse, de face, bras levés, chapeau de pirate ; pieds à y ≈ 34."""
    m = (lambda d: d) if sens > 0 else miroir
    L = [
        T(m("M-9 8Q-19 2-21-10"), 'chien', 'jaune', 5.5, 'orange'),
        T(m("M9 8Q19 5 23-4"), 'chien', 'jaune', 5.5, 'orange'),
        W(circ(-21 * sens, -11, 3.4), 'chien-clair', 'jaune', 'pastel'),
        W(circ(23 * sens, -5, 3.4), 'chien-clair', 'jaune', 'pastel'),
        W(ell(-6, 31, 6.2, 3.6), 'chien-oreille', 'rose', 'brun'),
        W(ell(6, 31, 6.2, 3.6), 'chien-oreille', 'rose', 'brun'),
        W(ell(0, 15, 11.5, 14.5), 'chien', 'jaune', 'orange'),
        W(ell(0, 18, 6.5, 8.5), 'chien-clair', 'jaune', 'pastel'),
        W("M-8-14C-17-15-21-6-19 3C-18 8-14 8-12 4C-11-1-10-7-7-11Z", 'chien-oreille', 'rose', 'brun'),
        W(miroir("M-8-14C-17-15-21-6-19 3C-18 8-14 8-12 4C-11-1-10-7-7-11Z"), 'chien-oreille', 'rose', 'brun'),
        W(circ(0, -7, 11), 'chien', 'jaune', 'orange'),
        W(ell(0, -2, 6.6, 4.8), 'chien-clair', 'jaune', 'pastel'),
        W(ell(0, -4.6, 2.9, 2.1), 'roue', 'bleu'),
        F("M-3.2 0Q0 2.6 3.2 0", BRUN),
        W("M-1.9 .8C-1.9 4.8 1.9 4.8 1.9 .8Z", 'cerise', 'rose'),
        N(-4.2, -10, 1.6, 'brun'), N(4.2, -10, 1.6, 'brun'),
        W("M-16-15C-12-23-7-29 0-29C7-29 12-23 16-15C8-18-8-18-16-15Z", 'pirate', 'bleu'),
        F("M-13-16.6Q0-20 13-16.6", SABLE),
        W(circ(0, -23.5, 2.7), 'blanc-oeil', 'jaune', 'reserve'),
    ]
    if cache:   # le bandeau sur l'œil (côté extérieur)
        L += [F(m("M-10-17L9-6"), BRUN), W(ell(4.2 * sens, -10, 3.2, 2.7), 'pirate', 'bleu')]
    return L

G['chiens-pirates'] = {'corps': [
    ('G', 'danse-chien', chien_pirate(1, False), -88, 1.1),
    ('G', 'danse-chien d2', chien_pirate(-1, True), 88, 1.1),
]}

def greffe_partie(els):
    L = []
    for e in els:
        if e[0] == 'REMUE':   # la queue qui remue : un groupe animé, jamais la pièce
            L.append('<g class="remue">' + ''.join(R(x) for x in e[1]) + '</g>')
        elif e[0] == 'G':     # ('G', classes, éléments, dx, échelle) : un groupe animé (Task 11)
            _, cls, sous, dx, s = e
            L.append(f'<g class="{cls}">' + ''.join(rendu(x, s, dx, 0, fil_s=1.0, filtre='mini') for x in sous) + '</g>')
        else:
            L.append(R(e))
    return L

def greffes():
    L = []
    for forme, parts in G.items():
        if parts.get('dos'):
            L.append(f'<symbol id="g-greffe-{forme}-dos" overflow="visible"><g class="a-corps">')
            L += ['  ' + x for x in greffe_partie(parts['dos'])]
            L.append('</g></symbol>')
        L.append(f'<symbol id="g-greffe-{forme}" overflow="visible">')
        if parts.get('corps'):
            L.append('<g class="a-corps">')
            L += ['  ' + x for x in greffe_partie(parts['corps'])]
            L.append('</g>')
        if parts.get('tete'):
            L.append('<g class="a-tete">')
            L += ['  ' + x for x in greffe_partie(parts['tete'])]
            L.append('</g>')
        L.append('</symbol>')
    return L

# ---------------------------------------------------------------------------
# 3. Le nuage-écran : centré (700,165), ≈ 300 × 200, jamais au-delà de x 860
#    (le rail du temps couvre la scène à partir de x 868)
CX, CY = 700, 165
EX, EY = 548, 34      # le bouton « Encore un rêve » (coin haut gauche de la pilule)

def nuage(rx, ry, cx=CX, cy=CY):
    """Un nuage : des bosses (cubiques) posées sur une ellipse, plus plates en bas."""
    angles = [-90, -52, -18, 14, 48, 78, 102, 132, 166, 198, 232]
    pts = []
    for a in angles:
        t = math.radians(a)
        pts.append((cx + rx * math.cos(t), cy + ry * math.sin(t)))
    def normale(x, y):
        nx, ny = (x - cx) / rx ** 2, (y - cy) / ry ** 2
        n = math.hypot(nx, ny)
        return nx / n, ny / n
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(len(pts)):
        (ax, ay), (bx, by) = pts[i], pts[(i + 1) % len(pts)]
        am = math.radians((angles[i] + (angles[(i + 1) % len(angles)] + (360 if i == len(angles) - 1 else 0))) / 2)
        bas = math.sin(am) > .55          # le bas du nuage : des bosses plus plates
        h = math.hypot(bx - ax, by - ay) * (.32 if bas else .58)
        nax, nay = normale(ax, ay)
        nbx, nby = normale(bx, by)
        d += (f"C{f(ax + nax * h)} {f(ay + nay * h)} {f(bx + nbx * h)} {f(by + nby * h)} {f(bx)} {f(by)}")
    return d + 'Z'

NUAGE_D = nuage(128, 80)               # bosses comprises : ≈ x 552–848, y 62–262
COUTURE_D = nuage(119, 72)
CLIP_D = nuage(124, 77)

def flou():
    """Le rêve d'une journée vide : des taches pâles, floues (CSS), qui flottent."""
    return ['<symbol id="g-reve-flou" overflow="visible"><g class="flou">',
            '  <path class="tache" style="--t:var(--p-lune)" d="' + ell(-50, -10, 46, 30) + '"/>',
            '  <path class="tache" style="--t:var(--p-pineale)" d="' + ell(30, -30, 40, 26) + '"/>',
            '  <path class="tache" style="--t:var(--p-vague)" d="' + ell(40, 30, 50, 28) + '"/>',
            '  <path class="tache" style="--t:var(--p-glace-rose)" d="' + ell(-30, 40, 34, 22) + '"/>',
            '</g></symbol>']

def bloc_defs():
    L = ['<!-- REVE-BEGIN -->',
         '<!-- ===== Le rêve (Task 10) : généré par tools/gen-reve.py, ne pas retoucher à la main =====',
         '     #g-base-<forme> : la grande forme de rêve (vignette × 3, ≈ 120 px, centrée sur (0,0)) ;',
         '       data-tete / data-corps : où se posent les deux parties d\'une greffe (x y échelle) ;',
         '     #g-greffe-<forme> : .a-tete et .a-corps, placées par des variables (--tete-x… --corps-s) ;',
         '     #g-greffe-<forme>-dos : ce qui passe derrière la base ; #g-reve-flou : la journée vide.',
         '     Pièces .w.lite (filtre #woolMini) seulement. -->',
         '<g id="g-reve-assets">']
    L += bases()
    L += greffes()
    L += flou()
    L.append('</g>')
    L.append(f'<clipPath id="clip-ecran"><path d="{CLIP_D}"/></clipPath>')
    L.append('<clipPath id="clip-ecran-grand"><rect x="520" y="0" width="346" height="330"/></clipPath>')
    L.append('<!-- REVE-END -->')
    return '\n'.join('          ' + l for l in L) + '\n'

def bloc_ecran():
    I = '            '
    L = ['<!-- ECRAN-BEGIN -->',
         '<!-- Le nuage-écran (Task 10, généré par tools/gen-reve.py) : #ecran-corps (le nuage, le film, l\'épingle ;',
         '     opacité selon le temps, tremble en cauchemar), le bouton #encore, la légende #t-phrase. -->',
         '<g id="ecran-corps">',
         '  <g class="ecran-tremble">',
         f'    <path class="sous-ecran" d="{NUAGE_D}"/>',
         f'    <path id="p-ecran" class="w ecran-laine" style="--p:var(--ecran-laine, var(--p-ecran))" data-ink="jaune" d="{NUAGE_D}"/>',
         f'    <path class="fil couture ecran-couture" d="{COUTURE_D}"/>',
         '    <g id="g-reve-cadre" clip-path="url(#clip-ecran)">',
         f'      <g id="g-reve" transform="translate({CX} {CY + 3})" aria-hidden="true"></g>',
         '    </g>',
         '    <g transform="translate(818 92) rotate(14)"><use href="#pin" style="color:var(--glass-yellow)"/></g>',
         '  </g>',
         '</g>',
         '<!-- « Encore un rêve » : une pilule de feutre cousue en haut à gauche du nuage (≥ 44 de haut) -->',
         '<g id="encore" class="encore" role="button" tabindex="0" aria-label="Encore un rêve" aria-hidden="true">',
         '  <g class="encore-corps">',
         f'    <path class="encore-focus" d="{rr(EX - 4, EY - 4, 164, 52, 26)}"/>',
         f'    <path class="w lite reserve encore-fond" style="--p:var(--p-ecran-bouton)" data-ink="bleu" d="{rr(EX, EY, 156, 44, 22)}"/>',
         f'    <path class="fil couture" style="--f:var(--fil-blanc)" d="{rr(EX + 5, EY + 5, 146, 34, 17)}"/>',
         f'    <text class="encore-texte" x="{EX + 78}" y="{EY + 28}">🔁 Encore un rêve</text>',
         '  </g>',
         '</g>',
         '<!-- La phrase du rêve : dessinée à sa place de la vue Dehors (sur le mur, à gauche du nuage,',
         '     en haut) ; en vue Dedans, elle glisse sous le nuage, posée sur la boîte (translation selon',
         '     --vue et --leg-dy, CSS) ; le fond se règle sur la hauteur du texte (script). -->',
         '<g id="g-legende" class="legende">',
         '  <path class="legende-fond w lite reserve" style="--p:var(--riso-papier, var(--p-carte))" d=""/>',
         '  <path class="legende-bord fil couture" style="--f:var(--fil-sable)" d=""/>',
         '<!-- … et, après un appui sur la télécommande (Task 11), la phrase-clé en gros (#t-cle) -->',
         '  <foreignObject x="188" y="26" width="324" height="330">',
         '    <div xmlns="http://www.w3.org/1999/xhtml" id="t-phrase" class="t-phrase" aria-live="polite"></div>',
         '    <div xmlns="http://www.w3.org/1999/xhtml" id="t-cle" class="t-cle" aria-live="polite" hidden=""></div>',
         '  </foreignObject>',
         '</g>',
         '<!-- La carte réconfort que la télécommande épingle sur l\'écran (Task 11, rempli par le script) -->',
         '<g id="g-reconfort" aria-hidden="true"></g>',
         '<!-- ECRAN-END -->']
    return '\n'.join(I + l for l in L) + '\n'

# ---------------------------------------------------------------------------
# 4. La télécommande (Task 11, spec §4.6) : une pièce de feutrine grise ≈ 66 × 128, quatre
#    boutons-pressions de couleur, une petite lampe rouge en haut (d'où partent les ondes),
#    une télé brodée en bas ; une étiquette de feutre épinglée au-dessus porte le libellé
#    (écrit par le script). En bas à droite de la scène, au-dessus de la boîte (y ≥ 466),
#    jamais au-delà de x 860 (le rail du temps). Inclinée de −5° par un <g> de placement
#    (aucune transform sur une pièce .w). La cible (transparente, non filtrée) couvre tout.
TC_X, TC_Y, TC_W, TC_H = 788, 330, 66, 128
TC_CX, TC_CY = TC_X + TC_W / 2, TC_Y + TC_H / 2
TAG = (779, 272, 80, 50)
PRESSIONS = [(806, 368, 'drapeau', 'rose', ''), (836, 368, 'soleil', 'jaune', ''),
             (806, 398, 'couverture', 'bleu', ''), (836, 398, 'tracteur', 'jaune', 'vert')]

def arc(cx, cy, r, a1, a2):
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    p2 = (cx + r * math.cos(math.radians(a2)), cy + r * math.sin(math.radians(a2)))
    return f"M{f(p1[0])} {f(p1[1])}A{f(r)} {f(r)} 0 0 1 {f(p2[0])} {f(p2[1])}"

def bloc_telecommande():
    I = '            '
    corps = rr(TC_X, TC_Y, TC_W, TC_H, 20)
    tx, ty, tw, th = TAG
    L = ['<!-- TELECOMMANDE-BEGIN -->',
         '<!-- La télécommande (Task 11, généré par tools/gen-reve.py) : visible la nuit des rêves et au matin',
         '     (classe tc-on), elle pulse après un cauchemar (.pulse), s\'enfonce sous le doigt (.appui). -->',
         '<g id="telecommande" class="telecommande" role="button" tabindex="-1" aria-label="Je change de chaîne !" aria-hidden="true">',
         '  <g class="tc-etiquette">',
         f'    <path class="sous-tc" d="{rr(tx, ty, tw, th, 12)}"/>',
         f'    <path class="w lite reserve tc-etiquette-fond" style="--p:var(--riso-papier, var(--p-carte))" d="{rr(tx, ty, tw, th, 12)}"/>',
         f'    <path class="fil couture" style="--f:var(--fil-sable)" d="{rr(tx + 4, ty + 4, tw - 8, th - 8, 9)}"/>',
         f'    <text class="tc-label" x="{f(tx + tw / 2)}" y="{f(ty + th / 2 + 4)}"></text>',
         f'    <g transform="translate({tx + tw - 7} {ty + 4}) rotate(18)"><use href="#pin" style="color:var(--glass-red)"/></g>',
         '  </g>',
         f'  <g transform="rotate(-5 {f(TC_CX)} {f(TC_CY)})">',
         '    <g class="tc-pulse">',
         '      <g class="tc-corps">',
         f'        <path class="tc-halo" d="{rr(TC_X - 5, TC_Y - 5, TC_W + 10, TC_H + 10, 25)}"/>',
         f'        <path class="sous-tc" d="{corps}"/>',
         f'        <path class="w pastel tc-laine" style="--p:var(--p-telecommande)" data-ink="bleu" d="{corps}"/>',
         f'        <path class="fil couture" style="--f:var(--fil-blanc)" d="{rr(TC_X + 5, TC_Y + 5, TC_W - 10, TC_H - 10, 15)}"/>',
         '        ' + rendu(W(ell(TC_CX, TC_Y + 11, 8, 4.6), 'drapeau', 'rose'), filtre='mini'),
         '        ' + rendu(F(f"M{f(TC_CX - 4)} {TC_Y + 9.5}Q{f(TC_CX - 1)} {TC_Y + 8} {f(TC_CX + 2)} {TC_Y + 9}", BLANC)),
         '        <g class="tc-boutons">']
    for x, y, laine, ink, cls in PRESSIONS:
        L += ['          ' + rendu(W(circ(x, y, 11), laine, ink, cls), filtre='mini'),
              '          ' + rendu(F(circ(x, y, 6.6), BLANC)),
              '          ' + rendu(N(x, y, 2.6))]
    L += ['        </g>',
          '        ' + rendu(F(rr(TC_CX - 12, 424, 24, 17, 3.5) + f"M{f(TC_CX - 5)} 424L{f(TC_CX - 9)} 417M{f(TC_CX + 5)} 424L{f(TC_CX + 9)} 417", BLANC, 'epais')),
          '        ' + rendu(F(f"M{f(TC_CX - 7)} 433Q{f(TC_CX - 3.5)} 429 {f(TC_CX)} 433Q{f(TC_CX + 3.5)} 437 {f(TC_CX + 7)} 433", BLANC)),
          '        <g class="tc-ondes">']
    for k, r in enumerate((10, 17, 24)):
        L.append(f'          <path class="fil tc-onde o{k + 1}" d="{arc(TC_CX, TC_Y + 8, r, -168, -92)}"/>')
    L += ['        </g>',
          f'        <path class="tc-focus" d="{rr(TC_X - 6, TC_Y - 6, TC_W + 12, TC_H + 12, 26)}"/>',
          '      </g>',
          '    </g>',
          '  </g>',
          '  <rect class="tc-cible" x="758" y="268" width="104" height="196" rx="18"/>',
          '</g>',
          '<!-- TELECOMMANDE-END -->']
    return '\n'.join(I + l for l in L) + '\n'

if __name__ == '__main__':
    chemin = os.path.join(ICI, '..', 'index.html')
    src = open(chemin, encoding='utf-8').read()
    d, e = bloc_defs(), bloc_ecran()
    if '--sec' in sys.argv:
        print(len(d.encode()), 'octets (defs),', len(e.encode()), 'octets (écran),', len(ANCRES), 'bases,', len(G), 'greffes')
        sys.exit(0)
    m = re.search(r' *<!-- REVE-BEGIN -->.*?<!-- REVE-END -->\n', src, re.S)
    if m:
        src = src[:m.start()] + d + src[m.end():]
    else:   # première fois : juste après le bloc des cartes
        i = src.index('<!-- CARTES-END -->\n') + len('<!-- CARTES-END -->\n')
        src = src[:i] + d + src[i:]
    m = re.search(r' *<!-- ECRAN-BEGIN -->.*?<!-- ECRAN-END -->\n', src, re.S)
    if m:
        src = src[:m.start()] + e + src[m.end():]
    else:
        a = '          <g id="g-ecran"></g>\n'
        assert src.count(a) == 1
        src = src.replace(a, '          <g id="g-ecran">\n' + e + '          </g>\n')
    t = bloc_telecommande()
    m = re.search(r' *<!-- TELECOMMANDE-BEGIN -->.*?<!-- TELECOMMANDE-END -->\n', src, re.S)
    if m:
        src = src[:m.start()] + t + src[m.end():]
    else:   # première fois (Task 11) : dans #g-ui, le groupe d'interface en haut de la scène
        a = '          <g id="g-ui"></g>\n'
        assert src.count(a) == 1
        src = src.replace(a, '          <g id="g-ui">\n' + t + '          </g>\n')
    open(chemin, 'w', encoding='utf-8').write(src)
    print('index.html : rêve, écran et télécommande écrits,', len(d.encode()) + len(e.encode()) + len(t.encode()), 'octets')

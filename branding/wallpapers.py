#!/usr/bin/env python3
"""Fonds d'écran origami Tunudan : 5 motifs, chacun en version claire et sombre.

    python3 branding/wallpapers.py [dossier_sortie] [--preview]

Produit pour chaque fond un SVG (source, redimensionnable) et un PNG 3840x2160.
Tout est déterministe (graines fixes) : mêmes images à chaque génération.
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080          # repère de dessin (rendu ensuite en 3840x2160)

# Palette Tunudan
ORANGE, ORANGE_L, ORANGE_D, ORANGE_DD = "#FF6B1A", "#FF9A5C", "#C2410C", "#8A2E08"
NOIR, ANTHRA, PAPIER, CREME = "#0D0D0D", "#1C1C1E", "#FBF8F3", "#F5F1EA"

# Grue du logo (repère 256 px) : (points, couleur d'origine)
CRANE = [
    ([(92, 150), (40, 118), (106, 169)], "#FF6B1A"),
    ([(164, 150), (206, 96), (150, 169)], "#FF9A5C"),
    ([(206, 96), (234, 94), (198, 110)], "#FF6B1A"),
    ([(128, 108), (92, 150), (30, 56)], "#FF9A5C"),
    ([(128, 108), (164, 150), (226, 56)], "#C2410C"),
    ([(128, 108), (92, 150), (118, 160)], "#FF6B1A"),
    ([(128, 108), (164, 150), (138, 160)], "#E8590C"),
    ([(128, 108), (118, 160), (138, 160)], "#FFB685"),
    ([(92, 150), (128, 204), (118, 160)], "#C2410C"),
    ([(164, 150), (128, 204), (138, 160)], "#FF6B1A"),
    ([(118, 160), (138, 160), (128, 204)], "#FF9A5C"),
]
# Grue en papier blanc (fonds clairs) : ailes et corps clairs, accents orange
WHITE_CRANE = {"#FF9A5C": "#FFFFFF", "#C2410C": "#E7E0D5", "#FF6B1A": ORANGE,
               "#E8590C": "#F0EAE0", "#FFB685": "#FFFFFF"}


# ----------------------------------------------------------------- couleurs
def rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def hexc(c):
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(v))) for v in c)


def mix(a, b, t):
    a, b = rgb(a), rgb(b)
    return hexc([a[i] + (b[i] - a[i]) * t for i in range(3)])


def shade(c, f):
    """f > 1 éclaircit (vers le blanc), f < 1 assombrit."""
    return mix(c, "#FFFFFF", f - 1) if f >= 1 else mix(c, "#000000", 1 - f)


# ----------------------------------------------------------------- SVG
def poly(pts, fill, opacity=1.0, stroke=True):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    st = f' stroke="{fill}" stroke-width="0.6" stroke-linejoin="round"' if stroke else ""
    op = f' fill-opacity="{opacity:.3f}"' if opacity < 1 else ""
    if opacity < 1:
        st = ""
    return f'<polygon points="{p}" fill="{fill}"{op}{st}/>'


def svg(body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}"><defs>{defs}</defs>{"".join(body)}</svg>')


def crane(x, y, size, mapping=None, rot=0.0, opacity=1.0, flip=False):
    """Grue Tunudan centrée en (x, y), largeur ≈ size."""
    s = size / 204.0
    out = []
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    for pts, col in CRANE:
        tp = []
        for px, py in pts:
            dx, dy = (px - 132) * s, (py - 130) * s
            if flip:
                dx = -dx
            tp.append((x + dx * ca - dy * sa, y + dx * sa + dy * ca))
        out.append(poly(tp, (mapping or {}).get(col, col), opacity))
    return "".join(out)


def crane_shadow(x, y, size, color, rot=0.0, steps=7, dx=3.0, dy=4.5, alpha=0.035, flip=False):
    """Ombre douce : la silhouette répétée en léger décalage."""
    return "".join(crane(x + dx * k, y + dy * k, size * (1 + 0.004 * k), {c: color for _, c in CRANE},
                         rot, alpha, flip) for k in range(1, steps + 1))


# ----------------------------------------------------------------- papier froissé (low-poly éclairé)
def lowpoly(seed, cols, rows, color_at, zamp=0.35, light=(-0.5, -0.7, 0.9), jitter=0.32):
    """Triangles dont la teinte dépend de leur orientation (relief tiré au hasard)."""
    rnd = random.Random(seed)
    cw, rh = W / cols, H / rows
    pts = [[(c * cw + (rnd.uniform(-jitter, jitter) * cw if 0 < c < cols else 0),
             r * rh + (rnd.uniform(-jitter, jitter) * rh if 0 < r < rows else 0),
             rnd.uniform(-1, 1) * zamp * cw)
            for c in range(cols + 1)] for r in range(rows + 1)]
    lx, ly, lz = light
    ln = math.sqrt(lx * lx + ly * ly + lz * lz)
    lx, ly, lz = lx / ln, ly / ln, lz / ln
    out = []
    for r in range(rows):
        for c in range(cols):
            a, b, d, e = pts[r][c], pts[r][c + 1], pts[r + 1][c], pts[r + 1][c + 1]
            tris = ((a, b, e), (a, e, d)) if (r + c) % 2 == 0 else ((a, b, d), (b, e, d))
            for t in tris:
                (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = t
                ux, uy, uz = x2 - x1, y2 - y1, z2 - z1
                vx, vy, vz = x3 - x1, y3 - y1, z3 - z1
                nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
                n = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
                if nz < 0:
                    nx, ny, nz = -nx, -ny, -nz
                lam = (nx * lx + ny * ly + nz * lz) / n
                cx, cy = (x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3
                out.append(poly([(x1, y1), (x2, y2), (x3, y3)], color_at(cx / W, cy / H, lam)))
    return out


def radial(id_, cx, cy, r, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return (f'<radialGradient id="{id_}" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" '
            f'r="{r}">{s}</radialGradient>')


def linear(id_, x1, y1, x2, y2, stops):
    s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
    return (f'<linearGradient id="{id_}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" '
            f'x2="{x2}" y2="{y2}">{s}</linearGradient>')


# ================================================================= 1. Grue
def grue(dark):
    if dark:
        bg = lowpoly(11, 18, 10, lambda u, v, l: shade(mix("#161618", "#0E0E10", v), 0.92 + 0.16 * l), 0.14)
        defs = radial("glow", 1180, 520, 620, [(0, ORANGE, 0.30), (0.45, ORANGE_D, 0.10), (1, ORANGE_D, 0)])
        body = bg + ['<rect width="1920" height="1080" fill="url(#glow)"/>',
                     crane_shadow(1180, 540, 640, "#000000", rot=-8, steps=8, alpha=0.10),
                     crane(1180, 540, 640, rot=-8)]
    else:
        bg = lowpoly(12, 18, 10, lambda u, v, l: shade(mix(PAPIER, "#EFE9DF", v * 0.8 + u * 0.2), 0.95 + 0.07 * l), 0.25)
        defs = radial("glow", 1180, 520, 700, [(0, "#FFD7BF", 0.55), (1, "#FFD7BF", 0)])
        body = bg + ['<rect width="1920" height="1080" fill="url(#glow)"/>',
                     crane_shadow(1180, 540, 640, "#5A3A20", rot=-8, steps=10, dx=4, dy=6, alpha=0.03),
                     crane(1180, 540, 640, WHITE_CRANE, rot=-8)]
    return svg(body, defs)


# ================================================================= 2. Envolée (vol de grues)
def envolee(dark):
    rnd = random.Random(21)
    if dark:
        bg = lowpoly(23, 16, 9, lambda u, v, l: shade(mix("#141416", "#0B0B0C", v), 0.93 + 0.14 * l), 0.12)
        defs = linear("sky", 0, 1080, 1920, 0, [(0, NOIR, 0), (1, ORANGE_D, 0.25)])
    else:
        bg = lowpoly(24, 16, 9, lambda u, v, l: shade(mix("#FFF9F2", "#F1EADF", v), 0.97 + 0.05 * l), 0.12)
        defs = linear("sky", 0, 1080, 1920, 0, [(0, "#FFFFFF", 0), (1, "#FFC9A6", 0.40)])
    body = bg + ['<rect width="1920" height="1080" fill="url(#sky)"/>']
    birds = []
    n = 24
    for i in range(n):
        t = i / (n - 1)
        # courbe douce du bas gauche vers le haut droit
        x = 40 + 1330 * t + rnd.uniform(-70, 70) * (1 - t * 0.5)
        y = 930 - 560 * t - 110 * math.sin(math.pi * t) + rnd.uniform(-70, 70) * (1 - t * 0.4)
        size = 30 + 120 * t ** 1.5 + rnd.uniform(-6, 6)
        birds.append((t, x, y, size, rnd.uniform(-24, 6)))
    birds.append((1.0, 1640, 210, 300, -14))           # la grue de tête
    birds.sort(key=lambda b: b[3])
    for idx, (t, x, y, size, rot) in enumerate(birds):
        if dark:
            op = 0.45 + 0.55 * t
            mapping = None if t > 0.4 else {c: mix(c, "#2A2A2C", 0.5 - t) for _, c in CRANE}
            body.append(crane(x, y, size, mapping, rot, op))
        else:
            body.append(crane_shadow(x, y, size, "#5A3A20", rot, steps=5, dx=1.5 + size / 110,
                                     dy=2.5 + size / 75, alpha=0.035))
            mapping = None if (idx % 4 == 0 or size > 250) else WHITE_CRANE
            body.append(crane(x, y, size, mapping, rot, 1.0))
    return svg(body, defs)


# ================================================================= 3. Sommets (montagnes pliées)
def sommets(dark):
    rnd = random.Random(33)
    if dark:
        sky_c = [(0, "#0A0A0B", 1), (0.5, "#151011", 1), (0.8, "#4A1E0A", 1), (1, "#A8380C", 1)]
        layers = ["#3A2216", "#26191A", "#18161A", "#0E0E10"]
    else:
        sky_c = [(0, "#FFFFFF", 1), (0.45, "#FFF4EA", 1), (0.8, "#FFD9BC", 1), (1, "#FFBC8E", 1)]
        layers = ["#F4DCCB", "#E8D9C9", "#D7C7B5", "#BFAD99"]
    defs = linear("sky", 0, 0, 0, 640, sky_c)
    body = ['<rect width="1920" height="1080" fill="url(#sky)"/>']
    sx, sy, r = 1240, 470, 230
    for k in range(18):
        a1, a2 = 2 * math.pi * k / 18, 2 * math.pi * (k + 1) / 18
        body.append(poly([(sx, sy), (sx + r * math.cos(a1), sy + r * math.sin(a1)),
                          (sx + r * math.cos(a2), sy + r * math.sin(a2))],
                         ORANGE if k % 2 else "#FF7F38"))
    # trois grues dans le ciel
    for (x, y, sz, rot) in ((520, 230, 70, -10), (610, 300, 46, -16), (450, 330, 38, -6)):
        if dark:
            body.append(crane(x, y, sz, None, rot, 0.9))
        else:
            body.append(crane_shadow(x, y, sz, "#5A3A20", rot, steps=4, alpha=0.04))
            body.append(crane(x, y, sz, WHITE_CRANE, rot))
    bases = [600, 700, 830, 960]
    amps = [230, 260, 300, 330]
    for li, base_col in enumerate(layers):
        y0, amp = bases[li], amps[li]
        far = 1 - li / 3
        x = -150 + rnd.uniform(0, 200)
        ridge = [(x, y0)]
        while x < W + 150:
            wpk = rnd.uniform(260, 520)
            px = x + wpk * rnd.uniform(0.35, 0.65)
            py = y0 - amp * rnd.uniform(0.45, 1.0)
            ridge += [(px, py), (x + wpk, y0 - amp * rnd.uniform(0.05, 0.3))]
            x += wpk
        body.append(poly(ridge + [(ridge[-1][0], H), (ridge[0][0], H)], base_col))
        for i in range(1, len(ridge) - 1, 2):
            pl, pk, pr = ridge[i - 1], ridge[i], ridge[i + 1]
            foot = (pk[0] + (pr[0] - pl[0]) * rnd.uniform(-0.05, 0.12), H + 20)
            sun_k = max(0.0, 1 - abs(pk[0] - sx) / 1000) * (0.75 if dark else 0.30) * (0.35 + 0.65 * far)
            lit = mix(shade(base_col, 1.16 if dark else 1.05), ORANGE, sun_k)
            dark_side = shade(base_col, 0.72 if dark else 0.9)
            body.append(poly([pl, pk, foot], lit))
            body.append(poly([pk, pr, foot], dark_side))
            # facette intermédiaire (le pli du versant éclairé)
            m1 = (pl[0] + (pk[0] - pl[0]) * 0.5, pl[1] + (pk[1] - pl[1]) * 0.5)
            m2 = (pk[0] + (foot[0] - pk[0]) * 0.45, pk[1] + (foot[1] - pk[1]) * 0.45)
            body.append(poly([pk, m1, m2], shade(lit, 1.12 if dark else 1.04)))
            m3 = (pk[0] + (pr[0] - pk[0]) * 0.5, pk[1] + (pr[1] - pk[1]) * 0.5)
            body.append(poly([pk, m3, m2], shade(dark_side, 0.88 if dark else 0.96)))
    return svg(body, defs)


# ================================================================= 4. Miura-ori (le papier se plie de gauche à droite)
def miura(dark):
    a, bb, sh = 104.0, 92.0, 34.0               # largeur, hauteur, décalage du zigzag
    cols, rows = int(W / a) + 4, int(H / bb) + 4
    light = (0.55, -0.55, 0.42)                  # lumière rasante venant du haut à droite
    ln = math.sqrt(sum(c * c for c in light))
    light = tuple(c / ln for c in light)
    def fold(x):                                 # 0 = papier à plat, 1 = plié à fond
        t = max(0.0, min(1.0, (x - 120) / (W - 300)))
        return t * t * (3 - 2 * t)
    def P(i, j):
        x = (i - 2) * a + (sh if j % 2 else 0)
        y = (j - 2) * bb
        z = (i % 2) * 70.0 * fold(x)
        return (x, y, z)
    body = []
    for j in range(rows):
        for i in range(cols):
            q = [P(i, j), P(i + 1, j), P(i + 1, j + 1), P(i, j + 1)]
            (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) = q[0], q[1], q[3]
            ux, uy, uz = x2 - x1, y2 - y1, z2 - z1
            vx, vy, vz = x3 - x1, y3 - y1, z3 - z1
            nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
            n = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
            if nz < 0:
                nx, ny, nz = -nx, -ny, -nz
            lam = max(0.0, (nx * light[0] + ny * light[1] + nz * light[2]) / n)
            pts = [(p[0], p[1]) for p in q]
            cx = sum(p[0] for p in pts) / 4 / W
            cy = sum(p[1] for p in pts) / 4 / H
            glow = max(0.0, 1 - math.hypot(cx - 0.95, cy - 1.0) / 1.0) ** 1.7
            if dark:
                base = shade("#26262A", 0.55 + 0.75 * lam)
                col = mix(base, ORANGE if lam > 0.5 else ORANGE_DD, glow * 0.9)
            else:
                base = shade("#E6DDCF", 0.88 + 0.30 * lam)
                col = mix(base, ORANGE_L if lam > 0.5 else "#E98A55", glow * 0.55)
            body.append(poly(pts, col))
    # Une grue posée là où le papier est le plus plié
    if dark:
        body.append(crane(1500, 330, 210, None, -8))
    else:
        body.append(crane_shadow(1500, 330, 210, "#5A3A20", -8, steps=7, alpha=0.04))
        body.append(crane(1500, 330, 210, WHITE_CRANE, -8))
    return svg(body)


# ================================================================= 5. Éventail plié
def eventail(dark):
    if dark:
        bg = lowpoly(51, 16, 9, lambda u, v, l: shade(mix("#141416", "#0C0C0D", u), 0.93 + 0.14 * l), 0.12)
        pleat = ("#2C2C30", "#17171A")
        band = (ORANGE, ORANGE_D)
        rib, shadow_col, shadow_a = "#3A2418", "#000000", 0.10
    else:
        bg = lowpoly(52, 16, 9, lambda u, v, l: shade(mix("#FFFBF6", "#F0E9DE", u * 0.7 + v * 0.3), 0.97 + 0.05 * l), 0.12)
        pleat = ("#FFFFFF", "#E9E1D4")
        band = (ORANGE, ORANGE_D)
        rib, shadow_col, shadow_a = "#B88A66", "#5A3A20", 0.04
    px, py = 1460, 1050                       # pivot de l'éventail
    r_in, r_band, r_out = 140, 680, 870
    a0, a1 = math.radians(196), math.radians(338)
    n = 22                                    # nombre de plis
    body = list(bg)
    def pt(r, ang, dr=0.0):
        return (px + (r + dr) * math.cos(ang), py + (r + dr) * math.sin(ang))
    # ombre portée
    outline = [pt(r_out, a0 + (a1 - a0) * k / 60) for k in range(61)] + [pt(r_in, a1), pt(r_in, a0)]
    for s_ in range(1, 10):
        body.append(poly([(x + 6 * s_, y + 8 * s_) for x, y in outline], shadow_col, shadow_a))
    for k in range(n):
        t0, t1 = a0 + (a1 - a0) * k / n, a0 + (a1 - a0) * (k + 1) / n
        tm = (t0 + t1) / 2
        even = k % 2 == 0
        # pli en accordéon : arête médiane saillante (rouge) ou rentrante
        ridge_out = r_out + (14 if even else -6)
        for (ra, rb_, cols) in ((r_in, r_band, pleat), (r_band, r_out, band)):
            rb2 = ridge_out if rb_ == r_out else rb_ + (8 if even else -4)
            left = [pt(ra, t0), pt(rb_, t0), pt(rb2, tm), pt(ra, tm)]
            right = [pt(ra, tm), pt(rb2, tm), pt(rb_, t1), pt(ra, t1)]
            light_first = even
            body.append(poly(left, cols[0] if light_first else cols[1]))
            body.append(poly(right, cols[1] if light_first else cols[0]))
    # nervures et rivet
    for k in range(n + 1):
        t = a0 + (a1 - a0) * k / n
        body.append(poly([pt(40, t - 0.006), pt(r_in + 40, t - 0.006), pt(r_in + 40, t + 0.006), pt(40, t + 0.006)], rib))
    for k in range(24):
        a_, b_ = 2 * math.pi * k / 24, 2 * math.pi * (k + 1) / 24
        body.append(poly([(px, py), (px + 34 * math.cos(a_), py + 34 * math.sin(a_)),
                          (px + 34 * math.cos(b_), py + 34 * math.sin(b_))], ORANGE_D if k % 2 else ORANGE))
    # Grue en vol au-dessus
    if dark:
        body.append(crane(470, 300, 230, None, -12))
    else:
        body.append(crane_shadow(470, 300, 230, "#5A3A20", -12, steps=7, alpha=0.035))
        body.append(crane(470, 300, 230, WHITE_CRANE, -12))
    return svg(body)


MOTIFS = [
    ("grue", "Grue", grue),
    ("envolee", "Envolée", envolee),
    ("sommets", "Sommets", sommets),
    ("miura", "Miura-ori", miura),
    ("eventail", "Éventail", eventail),
]


def render(svg_text, path, width, height):
    import cairosvg
    cairosvg.svg2png(bytestring=svg_text.encode(), write_to=path, output_width=width, output_height=height)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = os.path.abspath(args[0]) if args else os.path.join(HERE, "out", "wallpapers", "origami")
    preview = "--preview" in sys.argv
    os.makedirs(out, exist_ok=True)
    src = os.path.join(HERE, "wallpapers-svg")
    os.makedirs(src, exist_ok=True)
    for slug, _name, fn in MOTIFS:
        for variant, dark in (("clair", False), ("sombre", True)):
            name = f"origami-{slug}-{variant}"
            text = fn(dark)
            with open(os.path.join(src, name + ".svg"), "w", encoding="utf-8") as f:
                f.write(text)
            if preview:
                render(text, os.path.join(out, name + "-preview.png"), 960, 540)
            else:
                render(text, os.path.join(out, name + ".png"), 3840, 2160)
            print("  ->", name)


if __name__ == "__main__":
    main()

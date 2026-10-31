#!/usr/bin/env python3
"""Génère les visuels Tunudan OS (fonds d'écran, splash GRUB, logos PNG).

Usage : python3 branding/generate.py [dossier_sortie]
Dépendance : cairosvg (pip install cairosvg) ou rsvg-convert.
Les visuels sont déterministes (graine fixe) pour des builds reproductibles.
"""
import os
import random
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "out")

PALETTE = {
    "orange": "#FF6B1A",
    "orange_clair": "#FF9A5C",
    "orange_brule": "#C2410C",
    "noir": "#0D0D0D",
    "anthracite": "#1C1C1E",
    "blanc": "#F5F1EA",
}

LOGO_BODY = open(os.path.join(HERE, "logo.svg"), encoding="utf-8").read()
LOGO_INNER = LOGO_BODY[LOGO_BODY.index("<polygon"):LOGO_BODY.rindex("</svg>")]


def render(svg: str, path: str, width: int, height: int) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        import cairosvg  # type: ignore

        cairosvg.svg2png(bytestring=svg.encode(), write_to=path,
                         output_width=width, output_height=height)
    except ImportError:
        if not shutil.which("rsvg-convert"):
            sys.exit("Installer cairosvg (pip) ou rsvg-convert (librsvg2-bin)")
        subprocess.run(["rsvg-convert", "-w", str(width), "-h", str(height),
                        "-o", path], input=svg.encode(), check=True)
    print("  ->", os.path.relpath(path, OUT))


def facets(w: int, h: int, seed: int, dark: bool) -> str:
    """Grille de triangles « papier plié » qui s'éclaire vers le bas à droite."""
    rnd = random.Random(seed)
    cols, rows = 16, 9
    cw, rh = w / cols, h / rows
    pts = [[(c * cw + (rnd.uniform(-0.3, 0.3) * cw if 0 < c < cols else 0),
             r * rh + (rnd.uniform(-0.3, 0.3) * rh if 0 < r < rows else 0))
            for c in range(cols + 1)] for r in range(rows + 1)]
    out = []
    for r in range(rows):
        for c in range(cols):
            a, b = pts[r][c], pts[r][c + 1]
            d, e = pts[r + 1][c], pts[r + 1][c + 1]
            # intensité : diagonale du coin haut-gauche (sombre) au bas-droit (orange)
            t = (c / cols * 0.6 + r / rows * 0.4)
            for tri, shade in (((a, b, e), 0.0), ((a, e, d), 0.08)):
                k = max(0.0, min(1.0, t + shade + rnd.uniform(-0.06, 0.06)))
                if dark:
                    if k < 0.62:
                        g = int(13 + k * 22)
                        col = f"rgb({g},{g},{g + 1})"
                    else:
                        z = (k - 0.62) / 0.38
                        col = f"rgb({int(40 + z * 215)},{int(30 + z * 77)},{int(26 + z * 0)})"
                else:
                    g = int(245 - k * 30)
                    col = f"rgb({g},{g - 4},{g - 11})"
                p = " ".join(f"{x:.1f},{y:.1f}" for x, y in tri)
                out.append(f'<polygon points="{p}" fill="{col}" stroke="{col}" stroke-width="0.6"/>')
    return "".join(out)


def logo(x: float, y: float, size: float) -> str:
    s = size / 256
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">{LOGO_INNER}</g>'


def wallpaper(w: int, h: int, variant: str) -> str:
    dark = variant != "clair"
    bg = PALETTE["noir"] if dark else PALETTE["blanc"]
    txt = PALETTE["blanc"] if dark else PALETTE["noir"]
    body = [f'<rect width="{w}" height="{h}" fill="{bg}"/>', facets(w, h, 42, dark)]
    if variant == "slogan":
        size = h * 0.22
        body.append(logo(w * 0.08, h * 0.30, size))
        fs = h * 0.075
        body.append(
            f'<text x="{w * 0.08 + size * 1.05:.0f}" y="{h * 0.30 + size * 0.48:.0f}" '
            f'font-family="Inter, DejaVu Sans, sans-serif" font-weight="700" '
            f'font-size="{fs:.0f}" fill="{txt}">Apprendre. Coder. '
            f'<tspan fill="{PALETTE["orange"]}">Avancer.</tspan></text>')
        body.append(
            f'<text x="{w * 0.08 + size * 1.05:.0f}" y="{h * 0.30 + size * 0.48 + fs * 1.1:.0f}" '
            f'font-family="Inter, DejaVu Sans, sans-serif" font-size="{fs * 0.42:.0f}" '
            f'fill="{txt}" fill-opacity="0.7">tunudan.fr</text>')
    else:
        size = h * 0.16
        body.append(logo(w * 0.5 - size / 2, h * 0.42 - size / 2, size))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{"".join(body)}</svg>')


def splash(w: int, h: int, with_logo: bool = True) -> str:
    body = [f'<rect width="{w}" height="{h}" fill="{PALETTE["noir"]}"/>']
    if with_logo:
        size = h * 0.28
        body.append(logo(w / 2 - size / 2, h * 0.12, size))
        body.append(
            f'<text x="{w / 2}" y="{h * 0.12 + size + h * 0.07:.0f}" text-anchor="middle" '
            f'font-family="Inter, DejaVu Sans, sans-serif" font-weight="700" '
            f'font-size="{h * 0.06:.0f}" fill="{PALETTE["blanc"]}">Tunudan OS</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">{"".join(body)}</svg>')


def main() -> None:
    print("Génération des visuels dans", OUT)
    for variant in ("sombre", "clair", "slogan"):
        for (w, h) in ((1920, 1080), (3840, 2160)):
            render(wallpaper(w, h, variant),
                   os.path.join(OUT, "wallpapers", f"tunudan-{variant}-{w}x{h}.png"), w, h)
    render(splash(640, 480), os.path.join(OUT, "boot", "splash-640x480.png"), 640, 480)
    render(splash(1920, 1080), os.path.join(OUT, "boot", "splash-1920x1080.png"), 1920, 1080)
    render(splash(1920, 1080, False), os.path.join(OUT, "boot", "grub-background.png"), 1920, 1080)
    logo_svg = LOGO_BODY
    for size in (16, 24, 32, 48, 64, 128, 256, 512):
        render(logo_svg, os.path.join(OUT, "logo", f"tunudan-{size}.png"), size, size)
    mono = open(os.path.join(HERE, "logo-mono-light.svg"), encoding="utf-8").read()
    render(mono, os.path.join(OUT, "logo", "tunudan-mono-256.png"), 256, 256)


if __name__ == "__main__":
    main()

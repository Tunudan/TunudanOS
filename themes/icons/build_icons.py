#!/usr/bin/env python3
"""Thème d'icônes Tunudan : style origami (tuiles pliées, dossiers en papier plié).

    python3 themes/icons/build_icons.py [--preview]

Écrit themes/shared/icons/Tunudan/ (SVG « scalable » + alias en liens symboliques).
Les icônes absentes (symboliques, état, actions…) viennent de Papirus-Dark par héritage.
Les icônes d'applications de marque utilisent un pictogramme générique de leur fonction :
aucun logo de marque n'est reproduit.
"""
import math
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "shared", "icons", "Tunudan")

ORANGE, ORANGE_L, ORANGE_D, ORANGE_DD = "#FF6B1A", "#FF9A5C", "#C2410C", "#8A2E08"
NOIR, ANTHRA, SLATE, CREME = "#0D0D0D", "#1C1C1E", "#3A3A3E", "#F5F1EA"
COL = {
    "orange": ORANGE, "ember": ORANGE_D, "slate": SLATE, "dark": ANTHRA,
    "blue": "#3A7BD5", "teal": "#23998E", "green": "#2E9E5B", "violet": "#7B5EA7",
    "red": "#E5484D", "sand": "#D9A441", "pink": "#D6577F", "cyan": "#2B9FC7",
}


def rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def mix(a, b, t):
    a, b = rgb(a), rgb(b)
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def lighter(c, t=0.18):
    return mix(c, "#FFFFFF", t)


def darker(c, t=0.18):
    return mix(c, "#000000", t)


def svg(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
            + body + "</svg>\n")


# ----------------------------------------------------------------- supports (tuile, dossier, feuille)
def tile(color):
    """Tuile carrée en papier plié : deux tons en diagonale et coin replié en haut à droite."""
    c = COL.get(color, color)
    return (
        # ombre portée
        '<rect x="7" y="9" width="50" height="50" rx="12" fill="#000" fill-opacity=".22"/>'
        f'<path d="M19 6h20l19 19v20c0 7-5 12-12 12H19C12 57 7 52 7 45V18C7 11 12 6 19 6z" fill="{lighter(c, .08)}"/>'
        # moitié basse plus sombre (pli diagonal)
        f'<path d="M57 25v20c0 7-5 12-12 12H19c-6 0-10.5-4-11.7-9.6z" fill="{darker(c, .12)}"/>'
        # coin replié (dos du papier)
        f'<path d="M39 6v12c0 4 3 7 7 7h11z" fill="{lighter(c, .45)}"/>'
        f'<path d="M39 18c0 4 3 7 7 7h11l-2 2H44c-4 0-7-3-7-7V8z" fill="#000" fill-opacity=".16"/>'
    )


def folder(glyph_fn=None, base=ORANGE):
    back, front, tab = darker(base, .28), base, darker(base, .38)
    s = (
        '<path d="M6 16c0-3 2-5 5-5h14l5 5h23c3 0 5 2 5 5v31c0 3-2 5-5 5H11c-3 0-5-2-5-5z" fill="#000" fill-opacity=".2" transform="translate(0 2)"/>'
        f'<path d="M6 16c0-3 2-5 5-5h14l5 5h23c3 0 5 2 5 5v31c0 3-2 5-5 5H11c-3 0-5-2-5-5z" fill="{back}"/>'
        f'<path d="M6 16c0-3 2-5 5-5h14l5 5H6z" fill="{tab}"/>'
        # feuille qui dépasse
        f'<path d="M12 20h40v10H12z" fill="{CREME}"/>'
        # face avant en deux plis
        f'<path d="M4 27c0-2 1.5-3.5 3.5-3.5h49c2 0 3.5 1.5 3.5 3.5l-3 25c-.3 3-2.5 5-5.5 5H12.5c-3 0-5.2-2-5.5-5z" fill="{front}"/>'
        f'<path d="M60 26.8l-3 25.2c-.3 3-2.5 5-5.5 5H32L60 26.8z" fill="{darker(front, .12)}"/>'
        f'<path d="M4 27c0-2 1.5-3.5 3.5-3.5h49c2 0 3.5 1.5 3.5 3.5v.6H4z" fill="{lighter(front, .25)}"/>'
    )
    if glyph_fn:
        s += f'<g transform="translate(20 29) scale(.375)" opacity=".92">{glyph_fn("#FFFFFF")}</g>'
    return s


def sheet(band, label=None, glyph_fn=None):
    c = COL.get(band, band)
    s = (
        '<path d="M13 6h26l14 14v36c0 2-2 4-4 4H13c-2 0-4-2-4-4V10c0-2 2-4 4-4z" fill="#000" fill-opacity=".2" transform="translate(1 2)"/>'
        '<path d="M13 6h26l14 14v36c0 2-2 4-4 4H13c-2 0-4-2-4-4V10c0-2 2-4 4-4z" fill="#FBF8F3"/>'
        '<path d="M31 6h8l14 14v36c0 2-2 4-4 4H28z" fill="#ECE5DA" opacity=".55"/>'
        f'<path d="M39 6v10c0 2 2 4 4 4h10z" fill="{lighter(c, .35)}"/>'
        f'<path d="M9 42h44v14c0 2-2 4-4 4H13c-2 0-4-2-4-4z" fill="{c}"/>'
        f'<path d="M31 42h22v14c0 2-2 4-4 4H25z" fill="{darker(c, .12)}"/>'
    )
    if label:
        size = 11 if len(label) <= 3 else 9
        s += (f'<text x="31" y="55.5" font-family="Inter, DejaVu Sans, sans-serif" font-weight="800" '
              f'font-size="{size}" text-anchor="middle" fill="#FFFFFF">{label}</text>')
    if glyph_fn:
        s += f'<g transform="translate(17 12) scale(.42)">{glyph_fn(darker(c, .1))}</g>'
    return s


def app(color, glyph_fn, glyph_color="#FFFFFF"):
    return tile(color) + f'<g transform="translate(14 15) scale(.5625)">{glyph_fn(glyph_color)}</g>'


# ----------------------------------------------------------------- pictogrammes (repère 64, trait)
def S(c, w=5):
    return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'


G = {}


def glyph(name):
    def deco(fn):
        G[name] = fn
        return fn
    return deco


@glyph("globe")
def _(c):
    return (f'<circle cx="32" cy="32" r="24" {S(c)}/><ellipse cx="32" cy="32" rx="10" ry="24" {S(c, 4)}/>'
            f'<path d="M9 24h46M9 40h46" {S(c, 4)}/>')


@glyph("terminal")
def _(c):
    return f'<path d="M10 18l14 14-14 14M30 48h24" {S(c, 6)}/>'


@glyph("folder")
def _(c):
    return f'<path d="M6 18c0-2 2-4 4-4h14l5 5h25c2 0 4 2 4 4v25c0 2-2 4-4 4H10c-2 0-4-2-4-4z" {S(c)}/>'


@glyph("gear")
def _(c):
    pts = []
    for k in range(16):
        r = 26 if k % 2 == 0 else 19
        a = math.pi * 2 * (k - 0.5) / 16
        pts.append(f"{32 + r * math.cos(a):.1f},{32 + r * math.sin(a):.1f}")
        a2 = math.pi * 2 * (k + 0.5) / 16
        pts.append(f"{32 + r * math.cos(a2):.1f},{32 + r * math.sin(a2):.1f}")
    return f'<polygon points="{" ".join(pts)}" {S(c, 4)}/><circle cx="32" cy="32" r="8" {S(c, 5)}/>'


@glyph("pen")
def _(c):
    return f'<path d="M44 8l12 12-30 30-16 4 4-16zM38 14l12 12" {S(c)}/>'


@glyph("calculator")
def _(c):
    return (f'<rect x="12" y="6" width="40" height="52" rx="6" {S(c)}/><path d="M20 16h24v8H20z" {S(c, 4)}/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{c}"/>' for x in (22, 32, 42) for y in (34, 42, 50)))


@glyph("bag")
def _(c):
    return f'<path d="M10 22h44l-4 34H14zM22 22v-6a10 10 0 0 1 20 0v6" {S(c)}/>'


@glyph("refresh")
def _(c):
    return (f'<path d="M50 26A19 19 0 0 0 16 20M14 38a19 19 0 0 0 34 6" {S(c)}/>'
            f'<path d="M16 8v12h12M48 56V44H36" {S(c)}/>')


@glyph("chart")
def _(c):
    return f'<path d="M8 54h48M14 46V32M26 46V18M38 46V26M50 46V10" {S(c, 6)}/>'


@glyph("disk")
def _(c):
    return (f'<rect x="8" y="14" width="48" height="36" rx="6" {S(c)}/><path d="M8 38h48" {S(c, 4)}/>'
            f'<circle cx="46" cy="44" r="3" fill="{c}"/>')


@glyph("archive")
def _(c):
    return (f'<path d="M8 20h48v34H8zM6 10h52v10H6z" {S(c)}/>'
            f'<path d="M32 26v4M32 34v4M32 42v6" {S(c, 4)}/>')


@glyph("image")
def _(c):
    return (f'<rect x="6" y="10" width="52" height="44" rx="6" {S(c)}/>'
            f'<path d="M8 48l14-16 10 10 8-8 16 14" {S(c)}/><circle cx="42" cy="24" r="5" fill="{c}"/>')


@glyph("brush")
def _(c):
    return (f'<path d="M54 8L30 34" {S(c, 6)}/><path d="M28 36c-6-2-12 2-12 8 0 5-4 8-8 8 12 6 26 2 24-10z" fill="{c}"/>')


@glyph("play")
def _(c):
    return f'<path d="M18 10l34 22-34 22z" {S(c)}/>'


@glyph("music")
def _(c):
    return (f'<path d="M24 46V12l30-6v34" {S(c)}/><circle cx="17" cy="47" r="8" fill="{c}"/>'
            f'<circle cx="47" cy="41" r="8" fill="{c}"/>')


@glyph("camera")
def _(c):
    return (f'<path d="M6 20h12l5-8h18l5 8h12v32H6z" {S(c)}/><circle cx="32" cy="35" r="10" {S(c)}/>')


@glyph("doc")
def _(c):
    return f'<path d="M14 6h24l12 12v40H14zM38 6v12h12M22 30h20M22 38h20M22 46h14" {S(c)}/>'


@glyph("calendar")
def _(c):
    return (f'<rect x="8" y="12" width="48" height="44" rx="6" {S(c)}/><path d="M8 24h48M20 6v10M44 6v10" {S(c)}/>'
            + "".join(f'<rect x="{x}" y="{y}" width="6" height="6" rx="1" fill="{c}"/>' for x in (16, 29, 42) for y in (31, 43)))


@glyph("clock")
def _(c):
    return f'<circle cx="32" cy="32" r="25" {S(c)}/><path d="M32 16v16l11 8" {S(c)}/>'


@glyph("weather")
def _(c):
    return (f'<circle cx="24" cy="22" r="9" {S(c, 4)}/><path d="M24 4v4M8 22H4M12 10l-3-3M36 10l3-3" {S(c, 4)}/>'
            f'<path d="M20 52h28a10 10 0 0 0 0-20 14 14 0 0 0-27 3 8.5 8.5 0 0 0-1 17z" {S(c)}/>')


@glyph("pin")
def _(c):
    return f'<path d="M32 58S12 38 12 24a20 20 0 0 1 40 0c0 14-20 34-20 34z" {S(c)}/><circle cx="32" cy="24" r="7" {S(c)}/>'


@glyph("person")
def _(c):
    return f'<circle cx="32" cy="20" r="11" {S(c)}/><path d="M10 56c2-12 11-18 22-18s20 6 22 18" {S(c)}/>'


@glyph("people")
def _(c):
    return (f'<circle cx="24" cy="22" r="9" {S(c)}/><path d="M6 54c2-10 9-15 18-15s16 5 18 15" {S(c)}/>'
            f'<circle cx="44" cy="20" r="7" {S(c, 4)}/><path d="M46 34c7 1 12 6 13 14" {S(c, 4)}/>')


@glyph("bell")
def _(c):
    return f'<path d="M14 46h36l-5-8V26a13 13 0 0 0-26 0v12zM26 52a6 6 0 0 0 12 0" {S(c)}/>'


@glyph("shield")
def _(c):
    return f'<path d="M32 6l22 8v16c0 14-10 24-22 28C20 54 10 44 10 30V14z" {S(c)}/><path d="M22 32l7 7 13-14" {S(c)}/>'


@glyph("key")
def _(c):
    return f'<circle cx="20" cy="40" r="12" {S(c)}/><path d="M29 31L54 6M44 16l8 8M38 22l6 6" {S(c)}/>'


@glyph("chat")
def _(c):
    return f'<path d="M8 14c0-3 2-6 6-6h36c4 0 6 3 6 6v24c0 3-2 6-6 6H26L14 56V44h0c-4 0-6-3-6-6z" {S(c)}/>'


@glyph("mail")
def _(c):
    return f'<rect x="6" y="14" width="52" height="36" rx="5" {S(c)}/><path d="M8 18l24 18 24-18" {S(c)}/>'


@glyph("monitor")
def _(c):
    return f'<rect x="6" y="8" width="52" height="36" rx="5" {S(c)}/><path d="M24 56h16M32 44v12" {S(c)}/>'


@glyph("laptop")
def _(c):
    return f'<rect x="12" y="12" width="40" height="28" rx="4" {S(c)}/><path d="M4 50h56l-4-6H8z" {S(c, 4)}/>'


@glyph("keyboard")
def _(c):
    return (f'<rect x="4" y="16" width="56" height="32" rx="5" {S(c)}/><path d="M18 40h28" {S(c, 4)}/>'
            + "".join(f'<rect x="{x}" y="{y}" width="5" height="5" rx="1" fill="{c}"/>' for x in (11, 20, 29, 38, 47) for y in (23, 31)))


@glyph("mouse")
def _(c):
    return f'<rect x="16" y="6" width="32" height="52" rx="16" {S(c)}/><path d="M32 6v16" {S(c)}/>'


@glyph("speaker")
def _(c):
    return f'<path d="M8 24h10l14-12v40L18 40H8zM42 22a14 14 0 0 1 0 20M48 14a24 24 0 0 1 0 36" {S(c)}/>'


@glyph("battery")
def _(c):
    return f'<rect x="4" y="18" width="50" height="28" rx="5" {S(c)}/><path d="M60 28v8" {S(c, 6)}/><path d="M11 25h26v14H11z" fill="{c}"/>'


@glyph("wifi")
def _(c):
    return (f'<path d="M4 24a40 40 0 0 1 56 0M12 33a28 28 0 0 1 40 0M20 42a16 16 0 0 1 24 0" {S(c)}/>'
            f'<circle cx="32" cy="51" r="4" fill="{c}"/>')


@glyph("bluetooth")
def _(c):
    return f'<path d="M18 20l26 24-12 12V8l12 12-26 24" {S(c)}/>'


@glyph("printer")
def _(c):
    return f'<path d="M16 22V6h32v16M16 46H8V24h48v22h-8M16 38h32v20H16z" {S(c)}/>'


@glyph("network")
def _(c):
    return (f'<rect x="24" y="6" width="16" height="12" rx="2" {S(c, 4)}/><rect x="6" y="44" width="16" height="12" rx="2" {S(c, 4)}/>'
            f'<rect x="42" y="44" width="16" height="12" rx="2" {S(c, 4)}/><path d="M32 18v12M14 44V32h36v12" {S(c, 4)}/>')


@glyph("lock")
def _(c):
    return f'<rect x="12" y="28" width="40" height="28" rx="5" {S(c)}/><path d="M20 28v-8a12 12 0 0 1 24 0v8" {S(c)}/>'


@glyph("power")
def _(c):
    return f'<path d="M20 16a22 22 0 1 0 24 0M32 6v24" {S(c, 6)}/>'


@glyph("search")
def _(c):
    return f'<circle cx="27" cy="27" r="18" {S(c, 6)}/><path d="M40 40l16 16" {S(c, 7)}/>'


@glyph("download")
def _(c):
    return f'<path d="M32 6v34M18 28l14 14 14-14M8 54h48" {S(c, 6)}/>'


@glyph("upload")
def _(c):
    return f'<path d="M32 44V10M18 22l14-14 14 14M8 54h48" {S(c, 6)}/>'


@glyph("star")
def _(c):
    pts = []
    for k in range(10):
        r = 26 if k % 2 == 0 else 11
        a = -math.pi / 2 + math.pi * k / 5
        pts.append(f"{32 + r * math.cos(a):.1f},{33 + r * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" {S(c, 4)}/>'


@glyph("trash")
def _(c):
    return f'<path d="M8 16h48M24 16V8h16v8M14 16l4 40h28l4-40M28 26v20M36 26v20" {S(c)}/>'


@glyph("home")
def _(c):
    return f'<path d="M6 30L32 8l26 22M14 24v32h14V40h8v16h14V24" {S(c)}/>'


@glyph("cube")
def _(c):
    return f'<path d="M32 6l24 13v26L32 58 8 45V19zM8 19l24 13 24-13M32 32v26" {S(c)}/>'


@glyph("film")
def _(c):
    return (f'<rect x="8" y="6" width="48" height="52" rx="4" {S(c)}/><path d="M18 6v52M46 6v52M18 32h28" {S(c, 4)}/>'
            + "".join(f'<rect x="{x}" y="{y}" width="4" height="4" fill="{c}"/>' for x in (11, 49) for y in (12, 22, 38, 48)))


@glyph("wave")
def _(c):
    return f'<path d="M4 32h6M14 22v20M22 12v40M30 24v16M38 8v48M46 18v28M54 28v8M60 32h0" {S(c, 5)}/>'


@glyph("sliders")
def _(c):
    return (f'<path d="M8 16h48M8 32h48M8 48h48" {S(c, 4)}/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{c}"/>' for x, y in ((40, 16), (20, 32), (46, 48))))


@glyph("palette")
def _(c):
    return (f'<path d="M32 6C17 6 6 17 6 31c0 12 9 21 20 21 4 0 5-3 4-6s1-6 5-6h8c9 0 15-6 15-14C58 15 46 6 32 6z" {S(c)}/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>' for x, y in ((20, 26), (30, 16), (43, 18), (48, 30))))


@glyph("font")
def _(c):
    return f'<path d="M6 54L22 10l16 44M12 38h20M44 30a8 8 0 1 1 0 16 8 8 0 0 1 0-16zM52 28v26" {S(c)}/>'


@glyph("help")
def _(c):
    return (f'<circle cx="32" cy="32" r="25" {S(c)}/><path d="M24 24a8 8 0 1 1 11 7c-2 1-3 3-3 5v2" {S(c)}/>'
            f'<circle cx="32" cy="46" r="3.5" fill="{c}"/>')


@glyph("info")
def _(c):
    return f'<circle cx="32" cy="32" r="25" {S(c)}/><path d="M32 30v16" {S(c, 6)}/><circle cx="32" cy="20" r="3.5" fill="{c}"/>'


@glyph("code")
def _(c):
    return f'<path d="M22 16L6 32l16 16M42 16l16 16-16 16M36 10l-8 44" {S(c)}/>'


@glyph("bug")
def _(c):
    return (f'<rect x="18" y="18" width="28" height="36" rx="14" {S(c)}/><path d="M24 14l-4-6M40 14l4-6M18 30H6M46 30h12M18 44H8M46 44h10M32 22v32" {S(c, 4)}/>')


@glyph("gamepad")
def _(c):
    return (f'<path d="M18 18h28c8 0 12 8 12 18 0 8-3 12-7 12-5 0-7-8-12-8H25c-5 0-7 8-12 8-4 0-7-4-7-12 0-10 4-18 12-18z" {S(c)}/>'
            f'<path d="M20 27v10M15 32h10" {S(c, 4)}/><circle cx="42" cy="29" r="3" fill="{c}"/><circle cx="48" cy="35" r="3" fill="{c}"/>')


@glyph("vm")
def _(c):
    return f'<rect x="4" y="6" width="40" height="30" rx="4" {S(c, 4)}/><rect x="20" y="22" width="40" height="30" rx="4" {S(c)}/><path d="M20 30h40" {S(c, 4)}/>'


@glyph("database")
def _(c):
    return (f'<ellipse cx="32" cy="14" rx="22" ry="8" {S(c)}/><path d="M10 14v36c0 4 10 8 22 8s22-4 22-8V14M10 32c0 4 10 8 22 8s22-4 22-8" {S(c)}/>')


@glyph("crane")
def _(c):
    pts = [((92, 150), (40, 118), (106, 169)), ((128, 108), (92, 150), (30, 56)), ((128, 108), (164, 150), (226, 56)),
           ((92, 150), (128, 204), (164, 150)), ((164, 150), (206, 96), (150, 169)), ((206, 96), (234, 94), (198, 110))]
    out = ""
    for i, tri in enumerate(pts):
        p = " ".join(f"{(x - 132) * .27 + 32:.1f},{(y - 128) * .27 + 32:.1f}" for x, y in tri)
        op = 1 if i in (1, 3) else .78
        out += f'<polygon points="{p}" fill="{c}" fill-opacity="{op}"/>'
    return out


@glyph("phone")
def _(c):
    return f'<path d="M20 6h8l4 12-6 4c3 7 8 12 14 14l4-6 12 4v8c0 4-3 6-6 6C27 48 16 37 14 12c0-3 2-6 6-6z" {S(c)}/>'


@glyph("eye")
def _(c):
    return f'<path d="M4 32s10-18 28-18 28 18 28 18-10 18-28 18S4 32 4 32z" {S(c)}/><circle cx="32" cy="32" r="8" {S(c)}/>'


@glyph("accessibility")
def _(c):
    return f'<circle cx="32" cy="10" r="5" fill="{c}"/><path d="M10 20l22 4 22-4M32 24v14l-10 18M32 38l10 18" {S(c)}/>'


@glyph("language")
def _(c):
    return f'<path d="M6 12h28M20 6v6M28 12c-2 12-10 20-20 24M14 22c4 6 10 10 16 12M36 56l10-26 10 26M40 46h12" {S(c, 4)}/>'


@glyph("cloud")
def _(c):
    return f'<path d="M18 50h30a12 12 0 0 0 0-24 16 16 0 0 0-31 3 10.5 10.5 0 0 0 1 21z" {S(c)}/>'


@glyph("backup")
def _(c):
    return (f'<path d="M50 30a19 19 0 1 1-6-14" {S(c)}/><path d="M46 6v12H34" {S(c)}/><path d="M32 20v14l8 5" {S(c)}/>')


@glyph("box")
def _(c):
    return f'<path d="M6 18l26-10 26 10v28L32 58 6 46zM6 18l26 10 26-10M32 28v30M19 13l26 10" {S(c, 4)}/>'


@glyph("record")
def _(c):
    return f'<circle cx="32" cy="32" r="25" {S(c)}/><circle cx="32" cy="32" r="12" fill="{c}"/>'


@glyph("notes")
def _(c):
    return f'<path d="M12 6h40v40L38 58H12zM52 46H38v12M20 18h24M20 28h24M20 38h14" {S(c)}/>'


@glyph("screenshot")
def _(c):
    return (f'<path d="M6 18V8h10M48 8h10v10M58 46v10H48M16 56H6V46" {S(c)}/>'
            f'<circle cx="32" cy="32" r="10" {S(c)}/>')


@glyph("torrent")
def _(c):
    return f'<path d="M22 6v40M10 34l12 12 12-12M42 58V18M30 30l12-12 12 12" {S(c, 5)}/>'


@glyph("windows")
def _(c):
    return f'<rect x="6" y="8" width="52" height="48" rx="5" {S(c)}/><path d="M6 20h52M32 20v36" {S(c, 4)}/>'


@glyph("display")
def _(c):
    return (f'<rect x="6" y="8" width="52" height="36" rx="5" {S(c)}/><path d="M24 56h16M32 44v12" {S(c)}/>'
            f'<path d="M18 34l10-12 8 8 6-6 6 10" {S(c, 4)}/>')


@glyph("tunudan")
def _(c):
    return G["crane"](c)


# ----------------------------------------------------------------- catalogue
# Applications : nom canonique -> (couleur, pictogramme, [alias…])
APPS = {
    "system-file-manager": ("orange", "folder", ["org.gnome.Nautilus", "nautilus", "nemo", "thunar", "org.xfce.thunar", "Thunar",
                                                   "org.kde.dolphin", "dolphin", "pcmanfm-qt", "pcmanfm", "caja", "file-manager",
                                                   "com.system76.CosmicFiles", "system-file-manager-root"]),
    "utilities-terminal": ("dark", "terminal", ["org.gnome.Terminal", "gnome-terminal", "org.gnome.Ptyxis", "org.gnome.Console",
                                                 "xfce4-terminal", "org.xfce.terminal", "mate-terminal", "org.kde.konsole", "konsole",
                                                 "kitty", "foot", "footclient", "Alacritty", "alacritty", "qterminal", "terminator",
                                                 "tilix", "com.system76.CosmicTerm", "xterm", "terminal", "lxterminal"]),
    "web-browser": ("blue", "globe", ["firefox", "firefox-esr", "org.mozilla.firefox", "chromium", "chromium-browser",
                                       "google-chrome", "brave-browser", "librewolf", "io.gitlab.librewolf-community",
                                       "org.gnome.Epiphany", "epiphany", "falkon", "org.kde.falkon", "internet-web-browser",
                                       "applications-internet"]),
    "internet-mail": ("cyan", "mail", ["thunderbird", "org.mozilla.Thunderbird", "evolution", "org.gnome.Evolution",
                                        "geary", "org.gnome.Geary", "kmail", "org.kde.kmail2", "mail-client"]),
    "libreoffice-writer": ("blue", "doc", ["org.libreoffice.LibreOffice.writer", "libreoffice-main", "x-office-document",
                                            "abiword", "accessories-word-processor", "wps-office-wpsmain"]),
    "libreoffice-calc": ("green", "chart", ["org.libreoffice.LibreOffice.calc", "x-office-spreadsheet", "gnumeric"]),
    "libreoffice-impress": ("orange", "display", ["org.libreoffice.LibreOffice.impress", "x-office-presentation"]),
    "libreoffice-draw": ("sand", "brush", ["org.libreoffice.LibreOffice.draw", "x-office-drawing"]),
    "libreoffice-base": ("violet", "database", ["org.libreoffice.LibreOffice.base"]),
    "libreoffice-math": ("teal", "font", ["org.libreoffice.LibreOffice.math"]),
    "libreoffice-startcenter": ("orange", "doc", ["org.libreoffice.LibreOffice", "libreoffice"]),
    "accessories-text-editor": ("sand", "pen", ["org.gnome.TextEditor", "gedit", "org.gnome.gedit", "mousepad",
                                                "org.xfce.mousepad", "pluma", "xed", "org.kde.kate", "kate", "kwrite",
                                                "org.kde.kwrite", "featherpad", "com.system76.CosmicEdit", "text-editor"]),
    "code-editor": ("dark", "code", ["code", "codium", "vscodium", "com.visualstudio.code", "com.vscodium.codium",
                                      "visual-studio-code", "org.gnome.Builder", "geany", "nvim", "vim", "emacs",
                                      "applications-development", "zed", "dev.zed.Zed"]),
    "accessories-calculator": ("slate", "calculator", ["org.gnome.Calculator", "gnome-calculator", "galculator",
                                                        "mate-calc", "org.kde.kcalc", "kcalc", "qalculate", "calculator"]),
    "preferences-system": ("slate", "gear", ["org.gnome.Settings", "gnome-control-center", "systemsettings",
                                              "xfce4-settings-manager", "org.xfce.settings.manager", "cinnamon-settings",
                                              "mate-control-center", "lxqt-config", "budgie-desktop-settings",
                                              "com.system76.CosmicSettings", "preferences-desktop", "applications-system",
                                              "configurator", "system-settings"]),
    "system-software-install": ("orange", "bag", ["org.gnome.Software", "gnome-software", "mintinstall",
                                                   "plasmadiscover", "org.kde.discover", "software-store",
                                                   "com.system76.CosmicStore", "pamac", "octopi", "applications-other"]),
    "system-software-update": ("green", "refresh", ["mintupdate", "update-manager", "software-update-available",
                                                     "tunudan-update", "pamac-updater", "system-upgrade"]),
    "utilities-system-monitor": ("teal", "chart", ["org.gnome.SystemMonitor", "gnome-system-monitor", "mate-system-monitor",
                                                    "xfce4-taskmanager", "org.xfce.taskmanager", "plasma-systemmonitor",
                                                    "org.kde.plasma-systemmonitor", "ksysguard", "htop", "btop",
                                                    "io.missioncenter.MissionCenter"]),
    "drive-harddisk-utility": ("slate", "disk", ["org.gnome.DiskUtility", "gnome-disks", "gparted", "partitionmanager",
                                                  "org.kde.partitionmanager", "mintstick", "disk-utility"]),
    "utilities-archive": ("sand", "archive", ["org.gnome.FileRoller", "file-roller", "engrampa", "xarchiver",
                                               "org.kde.ark", "ark", "lxqt-archiver", "archive-manager"]),
    "image-viewer": ("teal", "image", ["org.gnome.eog", "eog", "org.gnome.Loupe", "ristretto", "org.xfce.ristretto",
                                        "xviewer", "eom", "gwenview", "org.kde.gwenview", "lximage-qt", "shotwell",
                                        "org.gnome.Shotwell", "imv", "multimedia-photo-viewer"]),
    "image-editor": ("pink", "brush", ["gimp", "org.gimp.GIMP", "krita", "org.kde.krita", "inkscape", "org.inkscape.Inkscape",
                                        "pinta", "drawing", "applications-graphics", "kolourpaint"]),
    "multimedia-video-player": ("red", "play", ["vlc", "org.videolan.VLC", "totem", "org.gnome.Totem", "celluloid",
                                                 "io.github.celluloid_player.Celluloid", "mpv", "parole", "org.xfce.Parole",
                                                 "xplayer", "smplayer", "haruna", "org.kde.haruna", "dragonplayer",
                                                 "org.kde.dragonplayer", "showtime", "org.gnome.Showtime",
                                                 "applications-multimedia", "video-player"]),
    "multimedia-audio-player": ("violet", "music", ["rhythmbox", "org.gnome.Rhythmbox3", "elisa", "org.kde.elisa",
                                                     "audacious", "lollypop", "spotify", "com.spotify.Client", "strawberry",
                                                     "clementine", "org.gnome.Music", "gnome-music", "hypnotix",
                                                     "music-player"]),
    "accessories-screenshot": ("slate", "screenshot", ["org.gnome.Screenshot", "gnome-screenshot", "xfce4-screenshooter",
                                                        "org.xfce.screenshooter", "spectacle", "org.kde.spectacle",
                                                        "mate-screenshot", "flameshot", "screengrab", "applets-screenshooter"]),
    "camera-app": ("dark", "camera", ["cheese", "org.gnome.Cheese", "org.gnome.Snapshot", "kamoso", "camera-photo-app",
                                       "guvcview"]),
    "document-viewer": ("red", "doc", ["evince", "org.gnome.Evince", "org.gnome.Papers", "okular", "org.kde.okular",
                                        "atril", "xreader", "qpdfview", "zathura", "acroread", "application-pdf-viewer"]),
    "office-calendar": ("orange", "calendar", ["org.gnome.Calendar", "gnome-calendar", "korganizer", "org.kde.korganizer",
                                                "calendar"]),
    "preferences-system-time": ("slate", "clock", ["org.gnome.clocks", "gnome-clocks", "time-admin", "clock"]),
    "weather-app": ("cyan", "weather", ["org.gnome.Weather", "gnome-weather", "weather"]),
    "maps-app": ("green", "pin", ["org.gnome.Maps", "gnome-maps", "marble", "org.kde.marble"]),
    "contacts-app": ("blue", "person", ["org.gnome.Contacts", "gnome-contacts", "kaddressbook", "x-office-address-book"]),
    "accessories-notes": ("sand", "notes", ["gnote", "org.gnome.Gnote", "tomboy", "xpad", "notes", "sticky",
                                             "org.x.Sticky", "knotes"]),
    "help-browser": ("blue", "help", ["yelp", "org.gnome.Yelp", "help-contents", "khelpcenter", "org.kde.khelpcenter",
                                       "mintwelcome", "help-about"]),
    "tunudan": ("orange", "crane", ["tunudan-welcome", "start-here", "distributor-logo", "distributor-logo-tunudan",
                                     "start-here-symbolic-tunudan", "linuxmint-logo", "debian-logo", "archlinux-logo",
                                     "cinnamon-menu", "mate-menu", "xfce4-whiskermenu", "kickoff", "lxqt-main-menu"]),
    "tunudan-help": ("orange", "phone", ["preferences-desktop-remote-desktop", "krdc", "remmina",
                                          "org.remmina.Remmina", "rustdesk", "anydesk", "teamviewer"]),
    "preferences-system-bluetooth": ("blue", "bluetooth", ["blueman", "blueman-manager", "bluetooth", "bluedevil",
                                                            "org.kde.bluedevil", "blueberry", "bluetooth-active"]),
    "preferences-system-network": ("teal", "network", ["nm-connection-editor", "network-manager", "preferences-network",
                                                        "network-workgroup", "applications-network"]),
    "printer-app": ("slate", "printer", ["system-config-printer", "printer", "printer-network", "preferences-devices-printer",
                                          "simple-scan", "org.gnome.SimpleScan", "skanlite", "scanner"]),
    "system-users": ("slate", "people", ["users", "user-info", "preferences-system-users", "users-admin", "mate-about-me",
                                          "about-me", "user_icon"]),
    "security-high": ("green", "shield", ["gufw", "firewall-config", "preferences-system-privacy", "org.gnome.Settings-privacy",
                                           "security-medium", "clamtk", "privacy"]),
    "backup-app": ("teal", "backup", ["deja-dup", "org.gnome.DejaDup", "timeshift", "mintbackup", "kbackup", "backintime",
                                       "pika-backup", "org.gnome.World.PikaBackup"]),
    "preferences-system-drivers": ("slate", "box", ["mintdrivers", "jockey", "software-properties-drivers", "nvidia-settings"]),
    "software-properties": ("slate", "sliders", ["mintsources", "software-sources", "synaptic", "org.gnome.Tweaks",
                                                 "gnome-tweaks", "dconf-editor", "ca.desrt.dconf-editor", "preferences-other"]),
    "preferences-desktop-theme": ("pink", "palette", ["preferences-desktop-color", "preferences-desktop-wallpaper",
                                                       "cinnamon-themes", "xfce4-appearance-settings", "org.xfce.settings.appearance",
                                                       "mate-appearance-properties", "lxqt-appearance", "preferences-desktop-appearance",
                                                       "kvantummanager", "qt5ct", "qt6ct", "nwg-look", "lxappearance"]),
    "preferences-desktop-display": ("blue", "monitor", ["xfce4-display-settings", "org.xfce.settings.display",
                                                         "display", "arandr", "wdisplays", "nwg-displays", "video-display"]),
    "preferences-desktop-keyboard": ("slate", "keyboard", ["input-keyboard", "keyboard", "xfce4-keyboard-settings",
                                                            "org.xfce.settings.keyboard"]),
    "preferences-desktop-peripherals": ("slate", "mouse", ["input-mouse", "xfce4-mouse-settings", "org.xfce.settings.mouse",
                                                            "preferences-desktop-mouse", "input-touchpad"]),
    "preferences-desktop-sound": ("violet", "speaker", ["pavucontrol", "org.pulseaudio.pavucontrol", "multimedia-volume-control",
                                                         "audio-card", "pwvucontrol", "helvum", "sound"]),
    "preferences-system-power": ("green", "battery", ["xfce4-power-manager-settings", "org.xfce.PowerManager",
                                                       "power-statistics", "org.gnome.PowerStats", "mate-power-preferences",
                                                       "battery", "powerdevil"]),
    "preferences-desktop-locale": ("cyan", "language", ["preferences-desktop-language", "mintlocale", "language-selector",
                                                         "system-config-language", "input-method", "fcitx", "ibus"]),
    "preferences-desktop-accessibility": ("blue", "accessibility", ["accessibility", "orca", "preferences-desktop-a11y"]),
    "preferences-desktop-notification": ("sand", "bell", ["notification-settings", "xfce4-notifyd-config",
                                                           "org.xfce.xfce4-notifyd-config", "preferences-system-notifications"]),
    "preferences-desktop-font": ("slate", "font", ["org.gnome.font-viewer", "gnome-font-viewer", "font-manager",
                                                    "fonts", "gucharmap", "org.gnome.Characters", "kcharselect"]),
    "online-accounts": ("cyan", "cloud", ["goa-panel", "preferences-desktop-online-accounts", "nextcloud", "com.nextcloud.desktopclient.nextcloud",
                                           "onedrive", "dropbox", "megasync"]),
    "password-manager": ("dark", "key", ["keepassxc", "org.keepassxc.KeePassXC", "bitwarden", "com.bitwarden.desktop",
                                          "seahorse", "org.gnome.seahorse.Application", "kwalletmanager", "kleopatra",
                                          "dialog-password", "gnome-keyring"]),
    "chat-app": ("violet", "chat", ["discord", "com.discordapp.Discord", "telegram", "telegram-desktop",
                                     "org.telegram.desktop", "signal-desktop", "org.signal.Signal", "element-desktop",
                                     "im.riot.Riot", "hexchat", "pidgin", "polari", "konversation", "internet-chat",
                                     "slack", "com.slack.Slack", "zoom", "us.zoom.Zoom", "teams"]),
    "steam-app": ("dark", "gamepad", ["steam", "com.valvesoftware.Steam", "lutris", "net.lutris.Lutris", "heroic",
                                       "applications-games", "gnome-mines", "aisleriot", "supertuxkart", "minecraft-launcher",
                                       "org.prismlauncher.PrismLauncher", "retroarch"]),
    "virtual-machine": ("slate", "vm", ["virt-manager", "gnome-boxes", "org.gnome.Boxes", "virtualbox", "VirtualBox",
                                         "qemu", "vmware-workstation", "distrobox", "boxbuddy"]),
    "torrent-app": ("green", "torrent", ["transmission", "transmission-gtk", "transmission-qt", "com.transmissionbt.Transmission",
                                          "qbittorrent", "org.qbittorrent.qBittorrent", "deluge", "ktorrent", "fragments",
                                          "de.haeckerfelix.Fragments"]),
    "video-editor": ("red", "film", ["kdenlive", "org.kde.kdenlive", "shotcut", "org.shotcut.Shotcut", "openshot",
                                      "org.openshot.OpenShot", "pitivi", "flowblade", "handbrake", "fr.handbrake.ghb"]),
    "audio-editor": ("violet", "wave", ["audacity", "org.audacityteam.Audacity", "ardour", "lmms", "tenacity",
                                         "easyeffects", "com.github.wwmm.easyeffects", "audio-recorder"]),
    "recorder-app": ("red", "record", ["obs", "com.obsproject.Studio", "simplescreenrecorder", "kooha",
                                        "io.github.seadve.Kooha", "vokoscreen", "gnome-sound-recorder", "org.gnome.SoundRecorder"]),
    "modeling-app": ("sand", "cube", ["blender", "org.blender.Blender", "freecad", "org.freecadweb.FreeCAD", "openscad",
                                       "prusa-slicer", "cura", "applications-engineering"]),
    "debug-app": ("dark", "bug", ["ghidra", "wireshark", "org.wireshark.Wireshark", "gdb", "radare2", "cutter",
                                   "burpsuite", "zaproxy", "nmap", "zenmap", "applications-security", "kali-menu"]),
    "database-app": ("violet", "database", ["sqlitebrowser", "dbeaver", "io.dbeaver.DBeaverCommunity", "pgadmin4",
                                             "mysql-workbench", "beekeeper-studio"]),
    "system-search": ("slate", "search", ["catfish", "org.xfce.catfish", "searchmonkey", "kfind", "albert", "ulauncher",
                                           "rofi", "fuzzel", "wofi", "krunner", "system-run", "gnome-search-tool"]),
    "system-lock-screen": ("dark", "lock", ["xscreensaver", "light-locker-settings", "lock", "swaylock", "hyprlock"]),
    "system-shutdown": ("red", "power", ["system-log-out", "system-reboot", "system-restart", "gnome-logout",
                                          "xfce4-session-logout", "wlogout", "nwg-bar", "application-exit"]),
    "accessories-dictionary": ("blue", "language", ["org.gnome.Dictionary", "goldendict", "dialect", "translator",
                                                    "app.drey.Dialect", "crow-translate"]),
    "applications-science": ("teal", "eye", ["kstars", "stellarium", "org.stellarium.Stellarium", "celestia",
                                              "applications-education", "geogebra", "octave", "org.octave.Octave", "rstudio"]),
    "downloader-app": ("blue", "download", ["uget", "motrix", "persepolis", "kget", "org.kde.kget", "yt-dlg",
                                             "com.github.unrud.VideoDownloader", "parabolic", "filezilla"]),
    "container-app": ("cyan", "box", ["docker-desktop", "podman-desktop", "io.podman_desktop.PodmanDesktop",
                                       "flatseal", "com.github.tchx84.Flatseal", "warehouse", "gnome-software-flatpak"]),
    "about-system": ("slate", "info", ["help-about", "gnome-info", "hardinfo", "hardinfo2", "kinfocenter",
                                        "org.kde.kinfocenter", "neofetch", "fastfetch", "mintreport", "system-info"]),
    "upload-app": ("cyan", "upload", ["syncthing", "syncthing-gtk", "megasync-upload", "warpinator", "org.x.Warpinator",
                                       "localsend", "org.localsend.localsend_app", "kdeconnect", "org.kde.kdeconnect.app",
                                       "gsconnect", "file-transfer"]),
    "favorites-app": ("sand", "star", ["bookmarks", "user-bookmarks", "starred", "emblem-favorite"]),
    "window-manager": ("slate", "windows", ["preferences-system-windows", "xfwm4-settings", "org.xfce.xfwm4",
                                             "xfce4-workspaces", "workspace-switcher", "preferences-desktop-workspaces",
                                             "kwin", "compiz"]),
}

# Catégories du menu
CATEGORIES = {
    "applications-accessories": ("sand", "pen"), "applications-development": ("dark", "code"),
    "applications-education": ("teal", "eye"), "applications-games": ("dark", "gamepad"),
    "applications-graphics": ("pink", "brush"), "applications-internet": ("blue", "globe"),
    "applications-multimedia": ("violet", "music"), "applications-office": ("blue", "doc"),
    "applications-other": ("slate", "box"), "applications-science": ("teal", "eye"),
    "applications-system": ("slate", "gear"), "applications-utilities": ("sand", "sliders"),
    "preferences-desktop": ("slate", "sliders"), "preferences-system": ("slate", "gear"),
    "preferences-desktop-personal": ("pink", "person"), "preferences-system-administration": ("dark", "shield"),
    "applications-engineering": ("sand", "cube"), "applications-security": ("dark", "shield"),
    "applications-video": ("red", "film"), "applications-audio": ("violet", "wave"),
}

# Dossiers : nom -> pictogramme (None = dossier simple), alias
PLACES = {
    "folder": (None, ["inode-directory", "folder-open", "folder-visiting", "folder-drag-accept", "folder-new"]),
    "user-home": ("home", ["folder-home", "user-home-open"]),
    "user-desktop": ("monitor", ["folder-desktop"]),
    "folder-documents": ("doc", ["folder-documents-open", "folder-text"]),
    "folder-download": ("download", ["folder-downloads", "folder-download-open"]),
    "folder-music": ("music", ["folder-sound", "folder-audio"]),
    "folder-pictures": ("image", ["folder-images", "folder-photos", "folder-image"]),
    "folder-videos": ("play", ["folder-video", "folder-movies"]),
    "folder-templates": ("notes", ["folder-templates-open"]),
    "folder-publicshare": ("people", ["folder-public", "folder-share", "folder-shared"]),
    "folder-remote": ("globe", ["folder-network", "network-workgroup-folder", "folder-remote-open"]),
    "folder-development": ("code", ["folder-code", "folder-projects", "folder-git", "folder-github", "folder-gitlab"]),
    "folder-games": ("gamepad", ["folder-steam"]),
    "folder-cloud": ("cloud", ["folder-dropbox", "folder-nextcloud", "folder-sync", "folder-onedrive"]),
    "folder-recent": ("clock", ["document-open-recent", "folder-history"]),
    "folder-favorites": ("star", ["folder-bookmark", "folder-important", "user-bookmarks-folder"]),
    "folder-locked": ("lock", ["folder-root", "folder-private", "folder-encrypted"]),
    "folder-books": ("doc", ["folder-book", "folder-library"]),
    "folder-backup": ("backup", ["folder-timeshift"]),
    "folder-tunudan": ("crane", ["folder-tunudan-cours"]),
}

TRASH = ("user-trash", ["trash-empty", "user-trash-empty"]), ("user-trash-full", ["trash-full"])

DEVICES = {
    "drive-harddisk": ("slate", "disk", ["drive-harddisk-system", "drive-harddisk-root", "drive-harddisk-solidstate",
                                          "drive-harddisk-ieee1394", "harddrive", "computer-harddisk"]),
    "drive-removable-media": ("orange", "disk", ["drive-removable-media-usb", "media-removable", "drive-removable-media-usb-pendrive",
                                                  "media-flash", "media-flash-sd-mmc", "drive-harddisk-usb"]),
    "drive-optical": ("slate", "record", ["media-optical", "media-optical-cd", "media-optical-dvd", "media-optical-bd"]),
    "computer": ("blue", "monitor", ["computer-laptop", "user-desktop-computer", "system", "video-display"]),
    "computer-laptop-alt": ("blue", "laptop", ["laptop"]),
    "input-keyboard-dev": ("slate", "keyboard", []),
    "input-mouse-dev": ("slate", "mouse", []),
    "input-gaming": ("dark", "gamepad", ["joystick", "input-gamepad"]),
    "audio-headphones": ("violet", "music", ["audio-headset", "headphones"]),
    "audio-speakers": ("violet", "speaker", ["audio-speaker", "multimedia-player"]),
    "audio-input-microphone": ("violet", "record", ["microphone"]),
    "camera-web": ("dark", "camera", ["camera-photo", "camera-video", "webcam"]),
    "phone": ("teal", "phone", ["smartphone", "phone-android", "phone-apple-iphone", "pda"]),
    "printer-dev": ("slate", "printer", []),
    "network-wired": ("teal", "network", ["network-wired-activated", "network-card"]),
    "network-wireless": ("teal", "wifi", ["network-wireless-connected", "wifi", "network-wireless-signal-excellent"]),
    "bluetooth-dev": ("blue", "bluetooth", []),
    "battery-dev": ("green", "battery", ["ac-adapter"]),
}

# Types de fichiers : nom -> (couleur de bande, étiquette ou None, pictogramme ou None, alias)
MIMES = {
    "text-x-generic": ("slate", "TXT", None, ["text-plain", "text-x-readme", "text-x-log", "unknown", "application-x-zerosize"]),
    "application-pdf": ("red", "PDF", None, ["application-x-pdf", "x-office-document-pdf"]),
    "x-office-document": ("blue", "DOC", None, ["application-msword", "application-vnd.oasis.opendocument.text",
                                                 "application-vnd.openxmlformats-officedocument.wordprocessingml.document",
                                                 "application-rtf", "text-rtf"]),
    "x-office-spreadsheet": ("green", "XLS", None, ["application-vnd.ms-excel", "application-vnd.oasis.opendocument.spreadsheet",
                                                     "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                                     "text-csv"]),
    "x-office-presentation": ("orange", "PPT", None, ["application-vnd.ms-powerpoint",
                                                       "application-vnd.oasis.opendocument.presentation",
                                                       "application-vnd.openxmlformats-officedocument.presentationml.presentation"]),
    "image-x-generic": ("teal", None, "image", ["image-png", "image-jpeg", "image-gif", "image-webp", "image-bmp",
                                                 "image-tiff", "image-x-xcf", "image-heic", "image-avif"]),
    "image-svg+xml": ("pink", "SVG", None, ["image-svg", "image-x-svg"]),
    "audio-x-generic": ("violet", None, "music", ["audio-mpeg", "audio-x-mp3", "audio-flac", "audio-ogg", "audio-x-wav",
                                                   "audio-x-vorbis+ogg", "audio-aac", "audio-mp4", "audio-x-flac"]),
    "video-x-generic": ("red", None, "play", ["video-mp4", "video-x-matroska", "video-webm", "video-x-msvideo",
                                               "video-quicktime", "video-mpeg", "video-x-ogm+ogg"]),
    "package-x-generic": ("sand", "ZIP", None, ["application-zip", "application-x-tar", "application-x-compressed-tar",
                                                 "application-x-7z-compressed", "application-x-rar", "application-gzip",
                                                 "application-x-xz", "application-x-bzip", "application-zstd",
                                                 "application-x-zstd-compressed-tar", "application-x-archive"]),
    "application-x-deb": ("ember", "DEB", None, ["application-vnd.debian.binary-package", "application-x-debian-package"]),
    "application-x-rpm": ("red", "RPM", None, ["application-x-redhat-package-manager"]),
    "application-x-iso9660-image": ("slate", "ISO", None, ["application-x-cd-image", "application-x-raw-disk-image",
                                                            "application-x-ms-dos-executable-iso"]),
    "application-x-executable": ("dark", None, "gear", ["application-x-sharedlib", "application-x-object",
                                                         "application-x-elf", "application-x-appimage", "exec"]),
    "application-x-shellscript": ("dark", "SH", None, ["text-x-script", "application-x-sh", "text-x-sh"]),
    "text-x-python": ("blue", "PY", None, ["text-x-python3", "application-x-python-bytecode"]),
    "text-html": ("orange", "HTML", None, ["application-xhtml+xml", "text-x-html"]),
    "text-css": ("blue", "CSS", None, ["text-x-css"]),
    "application-javascript": ("sand", "JS", None, ["text-javascript", "application-x-javascript", "text-x-javascript"]),
    "application-json": ("sand", "JSON", None, ["text-x-json", "application-x-yaml", "text-x-yaml", "application-toml"]),
    "text-x-csrc": ("blue", "C", None, ["text-x-c", "text-x-chdr", "text-x-c++src", "text-x-c++hdr", "text-x-cpp"]),
    "text-x-rust": ("ember", "RS", None, []),
    "text-x-go": ("cyan", "GO", None, []),
    "text-x-java": ("red", "JAVA", None, ["application-x-java", "application-x-java-archive"]),
    "text-x-markdown": ("slate", "MD", None, ["text-markdown"]),
    "text-x-script": ("dark", None, "code", ["text-x-makefile", "text-x-cmake", "text-x-sql", "application-sql"]),
    "font-x-generic": ("slate", None, "font", ["font-ttf", "font-otf", "application-x-font-ttf", "application-x-font-otf",
                                                "font-woff", "font-woff2"]),
    "application-x-bittorrent": ("green", None, "torrent", []),
    "application-x-desktop": ("orange", None, "crane", ["application-x-tunudan"]),
    "application-epub+zip": ("violet", "EPUB", None, ["application-x-mobipocket-ebook", "application-vnd.amazon.ebook"]),
    "text-calendar": ("orange", None, "calendar", ["text-x-vcalendar"]),
    "text-x-vcard": ("blue", None, "person", ["text-directory"]),
    "application-x-virtualbox-vdi": ("slate", None, "vm", ["application-x-qemu-disk", "application-x-vmdk"]),
    "application-x-sqlite3": ("violet", None, "database", ["application-vnd.sqlite3", "application-x-sqlite2"]),
    "application-pgp-encrypted": ("dark", None, "key", ["application-pgp-keys", "application-pgp-signature",
                                                       "application-x-x509-ca-cert", "application-pkcs12"]),
}


# Formats précis (une feuille étiquetée chacun)
LABELS = {
    "image-png": ("teal", "PNG"), "image-jpeg": ("teal", "JPG"), "image-gif": ("teal", "GIF"),
    "image-webp": ("teal", "WEBP"), "image-tiff": ("teal", "TIFF"), "image-bmp": ("teal", "BMP"),
    "image-heic": ("teal", "HEIC"), "image-x-xcf": ("pink", "XCF"), "image-vnd.adobe.photoshop": ("pink", "PSD"),
    "application-x-krita": ("pink", "KRA"), "image-x-icon": ("teal", "ICO"),
    "audio-mpeg": ("violet", "MP3"), "audio-flac": ("violet", "FLAC"), "audio-ogg": ("violet", "OGG"),
    "audio-x-wav": ("violet", "WAV"), "audio-aac": ("violet", "AAC"), "audio-x-opus+ogg": ("violet", "OPUS"),
    "audio-midi": ("violet", "MIDI"),
    "video-mp4": ("red", "MP4"), "video-x-matroska": ("red", "MKV"), "video-webm": ("red", "WEBM"),
    "video-x-msvideo": ("red", "AVI"), "video-quicktime": ("red", "MOV"), "video-mpeg": ("red", "MPG"),
    "application-x-tar": ("sand", "TAR"), "application-gzip": ("sand", "GZ"), "application-x-7z-compressed": ("sand", "7Z"),
    "application-vnd.rar": ("sand", "RAR"), "application-x-xz": ("sand", "XZ"), "application-zstd": ("sand", "ZST"),
    "application-x-bzip": ("sand", "BZ2"), "application-x-compressed-tar": ("sand", "TGZ"),
    "application-vnd.oasis.opendocument.text": ("blue", "ODT"),
    "application-vnd.openxmlformats-officedocument.wordprocessingml.document": ("blue", "DOCX"),
    "application-vnd.oasis.opendocument.spreadsheet": ("green", "ODS"),
    "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet": ("green", "XLSX"),
    "text-csv": ("green", "CSV"),
    "application-vnd.oasis.opendocument.presentation": ("orange", "ODP"),
    "application-vnd.openxmlformats-officedocument.presentationml.presentation": ("orange", "PPTX"),
    "application-rtf": ("blue", "RTF"), "text-x-tex": ("teal", "TEX"),
    "application-xml": ("orange", "XML"), "application-x-yaml": ("sand", "YAML"), "application-toml": ("sand", "TOML"),
    "application-sql": ("violet", "SQL"), "text-x-log": ("slate", "LOG"), "text-x-ini": ("slate", "INI"),
    "text-x-php": ("violet", "PHP"), "application-x-ruby": ("red", "RB"), "application-typescript": ("blue", "TS"),
    "text-x-kotlin": ("violet", "KT"), "text-x-swift": ("ember", "SWIFT"), "text-x-lua": ("blue", "LUA"),
    "application-x-perl": ("blue", "PL"), "text-x-haskell": ("violet", "HS"), "text-x-dart": ("cyan", "DART"),
    "text-x-csharp": ("violet", "CS"), "text-x-asm": ("dark", "ASM"), "text-x-patch": ("slate", "DIFF"),
    "text-x-dockerfile": ("cyan", "DOCK"), "text-x-nix": ("cyan", "NIX"), "application-wasm": ("violet", "WASM"),
    "application-vnd.android.package-archive": ("green", "APK"), "application-x-ms-dos-executable": ("slate", "EXE"),
    "application-x-msi": ("slate", "MSI"), "application-x-apple-diskimage": ("slate", "DMG"),
    "application-vnd.appimage": ("dark", "APP"), "application-vnd.flatpak": ("cyan", "FLAT"),
    "application-vnd.snap": ("ember", "SNAP"), "application-x-raw-disk-image": ("slate", "IMG"),
    "application-x-qemu-disk": ("slate", "QCOW"), "font-ttf": ("slate", "TTF"), "font-otf": ("slate", "OTF"),
    "font-woff2": ("slate", "WOFF"), "application-x-mobipocket-ebook": ("violet", "MOBI"),
    "model-stl": ("sand", "STL"), "model-obj": ("sand", "OBJ"), "model-gltf+json": ("sand", "GLTF"),
    "application-x-blender": ("sand", "BLEND"), "application-x-pem-file": ("dark", "PEM"),
    "application-pgp-keys": ("dark", "GPG"), "text-x-ssh-key": ("dark", "KEY"), "application-x-ipynb+json": ("orange", "IPYNB"),
    "text-x-cmake": ("dark", "CMAKE"), "text-x-makefile": ("dark", "MAKE"), "application-x-subrip": ("slate", "SRT"),
    "application-x-ovpn": ("teal", "VPN"), "application-x-wireshark-capture": ("teal", "PCAP"),
}

MORE_DEVICES = {
    "tablet": ("teal", "laptop"), "multimedia-player-ebook": ("violet", "doc"), "media-flash-sd": ("orange", "box"),
    "network-router": ("teal", "wifi"), "network-nas": ("slate", "database"), "video-television": ("blue", "display"),
    "video-projector": ("slate", "film"), "scanner-dev": ("slate", "image"), "uninterruptible-power-supply": ("green", "power"),
    "smartwatch": ("teal", "clock"), "input-tablet": ("pink", "pen"), "security-key": ("dark", "key"),
}

EMBLEMS = {
    "emblem-favorite": ("sand", "star"), "emblem-important": ("red", "info"), "emblem-readonly": ("dark", "lock"),
    "emblem-shared": ("teal", "people"), "emblem-synchronizing": ("blue", "refresh"), "emblem-downloads": ("blue", "download"),
    "emblem-photos": ("teal", "image"), "emblem-documents": ("blue", "doc"), "emblem-music": ("violet", "music"),
    "emblem-videos": ("red", "play"), "emblem-system": ("slate", "gear"), "emblem-web": ("blue", "globe"),
    "emblem-mail": ("cyan", "mail"), "emblem-new": ("orange", "star"), "emblem-default": ("green", "shield"),
    "emblem-unreadable": ("red", "lock"), "emblem-encrypted": ("dark", "key"), "emblem-cloud": ("cyan", "cloud"),
    "emblem-tunudan": ("orange", "crane"),
}


def emblem(color, glyph_fn):
    c = COL.get(color, color)
    return (f'<circle cx="32" cy="33" r="26" fill="#000" fill-opacity=".2"/>'
            f'<circle cx="32" cy="31" r="26" fill="{c}"/>'
            f'<path d="M32 5a26 26 0 0 1 0 52z" fill="{darker(c, .12)}"/>'
            f'<g transform="translate(16 15) scale(.5)">{glyph_fn("#FFFFFF")}</g>')


# ----------------------------------------------------------------- écriture
def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    kinds = ("apps", "places", "devices", "mimetypes", "categories", "emblems")
    dirs = {k: os.path.join(OUT, "scalable", k) for k in kinds}
    for d in dirs.values():
        os.makedirs(d)
    drawings, aliases = {}, []

    def put(kind, name, body, alias_list=()):
        drawings[(kind, name)] = body
        aliases.extend((kind, a, name) for a in alias_list)

    for name, (col, g, al) in APPS.items():
        put("apps", name, app(col, G[g]), al)
    for name, (col, g) in CATEGORIES.items():
        if ("apps", name) not in drawings:
            put("categories", name, app(col, G[g]))
    for name, (g, al) in PLACES.items():
        put("places", name, folder(G[g] if g else None), al)
    empty = ('<path d="M12 18h40l-4 40H16z" fill="#3A3A3E"/><path d="M32 18h20l-4 40H32z" fill="#2A2A2C"/>'
             f'<path d="M8 12h48v7H8z" fill="{ORANGE}"/><path d="M32 12h24v7H32z" fill="{ORANGE_D}"/>'
             '<path d="M24 26v24M32 26v24M40 26v24" stroke="#F5F1EA" stroke-opacity=".5" stroke-width="3" stroke-linecap="round"/>')
    full = empty + (f'<path d="M14 12l10-8 8 6 8-6 10 8z" fill="{CREME}"/>'
                    f'<path d="M24 4l8 6 8-6 6 5-14 3z" fill="{ORANGE_L}"/>')
    put("places", TRASH[0][0], empty, TRASH[0][1])
    put("places", TRASH[1][0], full, TRASH[1][1])
    put("places", "network-server", app("teal", G["database"]), ["network-server-database"])
    put("places", "network-workgroup", folder(G["network"]))
    for name, (col, g, al) in DEVICES.items():
        put("devices", name, app(col, G[g]), al)
    for name, (col, g) in MORE_DEVICES.items():
        put("devices", name, app(col, G[g]))
    for name, (band, label, g, al) in MIMES.items():
        put("mimetypes", name, sheet(band, label, G[g] if g else None), al)
    for name, (band, label) in LABELS.items():
        put("mimetypes", name, sheet(band, label))
    for name, (col, g) in EMBLEMS.items():
        put("emblems", name, emblem(col, G[g]))

    for (kind, name), body in drawings.items():
        with open(os.path.join(dirs[kind], name + ".svg"), "w", encoding="utf-8") as f:
            f.write(svg(body))
    n_alias = 0
    for kind, a, target in aliases:
        link = os.path.join(dirs[kind], a + ".svg")
        if not os.path.lexists(link):
            os.symlink(target + ".svg", link)
            n_alias += 1

    sections = "".join(f"""
[scalable/{k}]
Context={ctx}
Size=64
MinSize=16
MaxSize=512
Type=Scalable
""" for k, ctx in (("apps", "Applications"), ("places", "Places"), ("devices", "Devices"),
                    ("mimetypes", "MimeTypes"), ("categories", "Categories"), ("emblems", "Emblems")))
    with open(os.path.join(OUT, "index.theme"), "w", encoding="utf-8") as f:
        f.write("[Icon Theme]\nName=Tunudan\n"
                "Comment=Icônes origami Tunudan ; Papirus-Dark pour les icônes symboliques et le reste\n"
                "Inherits=Papirus-Dark,Papirus,breeze-dark,Adwaita,hicolor\nExample=folder\n"
                "Directories=" + ",".join(f"scalable/{k}" for k in kinds) + "\n" + sections)
    print(f"Icônes Tunudan : {len(drawings)} dessins, {n_alias} alias "
          f"({len(drawings) + n_alias} noms d'icônes)")
    if "--preview" in sys.argv:
        preview()


def preview():
    import cairosvg
    from PIL import Image
    names = []
    for kind in ("places", "apps", "devices", "mimetypes", "categories", "emblems"):
        d = os.path.join(OUT, "scalable", kind)
        for n in sorted(os.listdir(d)):
            if not os.path.islink(os.path.join(d, n)):
                names.append(os.path.join(d, n))
    cell, cols = 72, 16
    rows = (len(names) + cols - 1) // cols
    for bg, suffix in (((24, 24, 26), "sombre"), ((243, 237, 228), "clair")):
        sheet_img = Image.new("RGB", (cols * cell + 16, rows * cell + 16), bg)
        for i, p in enumerate(names):
            png = cairosvg.svg2png(url=p, output_width=64, output_height=64)
            import io
            im = Image.open(io.BytesIO(png)).convert("RGBA")
            sheet_img.paste(im, (8 + (i % cols) * cell + 4, 8 + (i // cols) * cell + 4), im)
        out = f"/tmp/icones-{suffix}.png"
        sheet_img.save(out)
        print("Aperçu :", out)


if __name__ == "__main__":
    main()

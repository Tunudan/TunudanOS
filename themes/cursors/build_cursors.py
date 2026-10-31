#!/usr/bin/env python3
"""Curseurs Tunudan (Xcursor) : flèche en papier plié orange, contour blanc.

    python3 themes/cursors/build_cursors.py [--preview]

Dépendances : cairosvg (pip) et xcursorgen (paquet x11-apps).
Écrit themes/shared/cursors/Tunudan/ (index.theme + cursors/).
"""
import math
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "shared", "cursors", "Tunudan-cursors")
SIZES = (24, 32, 48, 64, 96)
OR, OR_D, OR_L, DARK, DARK2, WHITE = "#FF6B1A", "#C2410C", "#FF9A5C", "#1C1C1E", "#0D0D0D", "#FFFFFF"
SHADOW = '<g transform="translate(.8 1.2)" opacity=".35">{}</g>'


def svg(body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">{body}</svg>'


def outlined(path, fill_a, fill_b=None, split=None):
    """Forme avec contour blanc, ombre, et pli (deux tons) si split est un chemin de la moitié droite."""
    shadow = SHADOW.format(f'<path d="{path}" fill="#000" stroke="#000" stroke-width="2.4" stroke-linejoin="round"/>')
    body = f'<path d="{path}" fill="{fill_a}" stroke="{WHITE}" stroke-width="1.6" stroke-linejoin="round"/>'
    if fill_b and split:
        body += f'<path d="{split}" fill="{fill_b}"/>'
        body += f'<path d="{path}" fill="none" stroke="{WHITE}" stroke-width="1.6" stroke-linejoin="round"/>'
    return shadow + body


ARROW = "M3 2 L3 24 L9 18.5 L13 27.5 L16.6 26 L12.8 17.2 L20.5 17.2 Z"
ARROW_RIGHT = "M3 2 L20.5 17.2 L12.8 17.2 L16.6 26 L13 27.5 L9 18.5 L8.2 19.2 Z"


def arrow(extra=""):
    return outlined(ARROW, OR, OR_D, ARROW_RIGHT) + extra


def badge(cx, cy, inner, color=DARK):
    return (f'<circle cx="{cx + .6}" cy="{cy + .9}" r="6" fill="#000" opacity=".35"/>'
            f'<circle cx="{cx}" cy="{cy}" r="6" fill="{color}" stroke="{WHITE}" stroke-width="1.4"/>' + inner)


def double_arrow(angle):
    p = "M16 3 L21 9 L18 9 L18 23 L21 23 L16 29 L11 23 L14 23 L14 9 L11 9 Z"
    right = "M16 3 L21 9 L18 9 L18 23 L21 23 L16 29 Z"
    return f'<g transform="rotate({angle} 16 16)">{outlined(p, DARK, DARK2, right)}' \
           f'<path d="M16 10.5V21.5" stroke="{OR}" stroke-width="2" stroke-linecap="round"/></g>'


def bar_arrow(angle):
    """Flèche double avec barre centrale (redimensionnement de colonne ou de ligne)."""
    p = "M3 16 L9 11 L9 14 L14.5 14 L14.5 6 L17.5 6 L17.5 14 L23 14 L23 11 L29 16 L23 21 L23 18 L17.5 18 L17.5 26 L14.5 26 L14.5 18 L9 18 L9 21 Z"
    return f'<g transform="rotate({angle} 16 16)">{outlined(p, DARK)}' \
           f'<path d="M16 7.5V24.5" stroke="{OR}" stroke-width="1.6"/></g>'


def pinwheel(cx, cy, r, rot):
    out = ""
    for k in range(4):
        a = math.radians(rot + k * 90)
        b = math.radians(rot + k * 90 + 90)
        p1 = (cx + r * math.cos(a), cy + r * math.sin(a))
        p2 = (cx + r * 0.95 * math.cos(b - 0.55), cy + r * 0.95 * math.sin(b - 0.55))
        col = OR if k % 2 == 0 else OR_D
        out += f'<path d="M{cx} {cy} L{p1[0]:.2f} {p1[1]:.2f} L{p2[0]:.2f} {p2[1]:.2f} Z" fill="{col}"/>'
    return (f'<circle cx="{cx + .6}" cy="{cy + .9}" r="{r + 1.2}" fill="#000" opacity=".35"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r + 1.2}" fill="{DARK}" stroke="{WHITE}" stroke-width="1.4"/>'
            + out + f'<circle cx="{cx}" cy="{cy}" r="1.6" fill="{WHITE}"/>')


HAND = ("M12 15 V5.5 a2 2 0 0 1 4 0 V13 a2 2 0 0 1 4 0 v1.5 a2 2 0 0 1 4 0 v2 a2 2 0 0 1 4 0 V22 "
        "c0 4.5-3 7.5-7.5 7.5 H17.5 c-2.6 0-4.3-1.2-5.7-3.4 L7.5 19.5 a2 2 0 0 1 3.2-2.4 Z")
OPEN_HAND = ("M10 17 V9 a2 2 0 0 1 4 0 V15 V6.5 a2 2 0 0 1 4 0 V15 V8 a2 2 0 0 1 4 0 V15.5 V11 a2 2 0 0 1 4 0 V21 "
             "c0 5-3 8.5-8 8.5 H17 c-2.6 0-4.3-1.2-5.7-3.4 L6.5 20 a2 2 0 0 1 3.5-2 Z")
FIST = "M9 14 a2.5 2.5 0 0 1 5 -1 a2.5 2.5 0 0 1 5 0 a2.5 2.5 0 0 1 5 .5 a2.5 2.5 0 0 1 4.5 1.5 V21 c0 5-3 8.5-8 8.5 H17 c-4.5 0-8-3.5-8-8 Z"


# name -> (svg, hotspot x, y)   (hotspots dans le repère 32)
def cursors():
    c = {}
    c["default"] = (svg(arrow()), 3, 2)
    c["context-menu"] = (svg(arrow(f'<rect x="19" y="18" width="11" height="12" rx="2" fill="{DARK}" stroke="{WHITE}" stroke-width="1.3"/>'
                                   f'<path d="M21.5 21.5h6M21.5 24h6M21.5 26.5h6" stroke="{OR}" stroke-width="1.3"/>')), 3, 2)
    c["help"] = (svg(arrow(badge(24, 23, f'<text x="24" y="26.3" font-family="DejaVu Sans, sans-serif" font-weight="bold" font-size="9" text-anchor="middle" fill="{WHITE}">?</text>'))), 3, 2)
    c["copy"] = (svg(arrow(badge(24, 23, f'<path d="M24 20v6M21 23h6" stroke="{WHITE}" stroke-width="1.8" stroke-linecap="round"/>', "#2E9E5B"))), 3, 2)
    c["alias"] = (svg(arrow(badge(24, 23, f'<path d="M21.5 25.5l5-5M23 20.5h3.5V24" stroke="{WHITE}" stroke-width="1.6" fill="none" stroke-linecap="round"/>', "#3A7BD5"))), 3, 2)
    c["not-allowed"] = (svg(f'<circle cx="16.6" cy="17" r="11" fill="#000" opacity=".35"/>'
                            f'<circle cx="16" cy="16" r="11" fill="none" stroke="{WHITE}" stroke-width="5.5"/>'
                            f'<circle cx="16" cy="16" r="11" fill="none" stroke="#E5484D" stroke-width="3"/>'
                            f'<path d="M8.5 23.5L23.5 8.5" stroke="{WHITE}" stroke-width="5.5"/><path d="M8.5 23.5L23.5 8.5" stroke="#E5484D" stroke-width="3"/>'), 16, 16)
    c["text"] = (svg(f'<path d="M11 4h3l2 2 2-2h3M16 6v20M11 28h3l2-2 2 2h3" fill="none" stroke="{WHITE}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<path d="M11 4h3l2 2 2-2h3M16 6v20M11 28h3l2-2 2 2h3" fill="none" stroke="{DARK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
                     f'<path d="M16 13v6" stroke="{OR}" stroke-width="2" stroke-linecap="round"/>'), 16, 16)
    c["vertical-text"] = (svg(f'<g transform="rotate(90 16 16)">{c["text"][0][c["text"][0].index(">") + 1:-6]}</g>'), 16, 16)
    c["crosshair"] = (svg(f'<path d="M16 3v10M16 19v10M3 16h10M19 16h10" stroke="{WHITE}" stroke-width="4" stroke-linecap="round"/>'
                          f'<path d="M16 3v10M16 19v10M3 16h10M19 16h10" stroke="{DARK}" stroke-width="2" stroke-linecap="round"/>'
                          f'<circle cx="16" cy="16" r="2" fill="{OR}" stroke="{WHITE}" stroke-width="1"/>'), 16, 16)
    c["cell"] = (svg(outlined("M13 4h6v9h9v6h-9v9h-6v-9H4v-6h9z", DARK, DARK2, "M16 4h3v9h9v6h-9v9h-3z")
                     + f'<path d="M16 9v14M9 16h14" stroke="{OR}" stroke-width="1.6"/>'), 16, 16)
    c["move"] = (svg(outlined("M16 2l5 5h-3.5v7h7V10.5l5 5.5-5 5.5V18h-7v7h3.5l-5 5-5-5h3.5v-7h-7v3.5L2 16l5-5.5V14h7V7H10.5z", DARK, DARK2,
                              "M16 2l5 5h-3.5v7h7V10.5l5 5.5-5 5.5V18h-7v7h3.5l-5 5z")
                     + f'<circle cx="16" cy="16" r="2" fill="{OR}"/>'), 16, 16)
    c["ns-resize"] = (svg(double_arrow(0)), 16, 16)
    c["ew-resize"] = (svg(double_arrow(90)), 16, 16)
    c["nesw-resize"] = (svg(double_arrow(45)), 16, 16)
    c["nwse-resize"] = (svg(double_arrow(-45)), 16, 16)
    c["col-resize"] = (svg(bar_arrow(0)), 16, 16)
    c["row-resize"] = (svg(bar_arrow(90)), 16, 16)
    c["pointer"] = (svg(outlined(HAND, OR, OR_D, "M20 14.5 a2 2 0 0 1 4 0 v2 a2 2 0 0 1 4 0 V22 c0 4.5-3 7.5-7.5 7.5 H20 Z")), 14, 3)
    c["grab"] = (svg(outlined(OPEN_HAND, OR, OR_D, "M18 15 V8 a2 2 0 0 1 4 0 V15.5 V11 a2 2 0 0 1 4 0 V21 c0 5-3 8.5-8 8.5 Z")), 16, 14)
    c["grabbing"] = (svg(outlined(FIST, OR, OR_D, "M19 12.5 a2.5 2.5 0 0 1 5 .5 a2.5 2.5 0 0 1 4.5 1.5 V21 c0 5-3 8.5-8 8.5 H19 Z")), 16, 16)
    c["zoom-in"] = (svg(f'<circle cx="13.6" cy="14" r="9" fill="#000" opacity=".35"/>'
                        f'<path d="M19 19l9 9" stroke="{WHITE}" stroke-width="6" stroke-linecap="round"/><path d="M19 19l9 9" stroke="{OR_D}" stroke-width="3.4" stroke-linecap="round"/>'
                        f'<circle cx="13" cy="13" r="9" fill="{DARK}" stroke="{WHITE}" stroke-width="1.6"/><circle cx="13" cy="13" r="6.5" fill="none" stroke="{OR}" stroke-width="1.6"/>'
                        f'<path d="M13 9.5v7M9.5 13h7" stroke="{WHITE}" stroke-width="2" stroke-linecap="round"/>'), 13, 13)
    c["zoom-out"] = (svg(c["zoom-in"][0].replace("M13 9.5v7M9.5 13h7", "M9.5 13h7")), 13, 13)
    c["pencil"] = (svg(outlined("M4 28l2-7L22 5l5 5L11 26z", OR, OR_D, "M24.5 7.5L27 10 11 26 4 28z")
                       + f'<path d="M4 28l2-7 5 5z" fill="{DARK}"/>'), 4, 28)
    c["color-picker"] = (svg(outlined("M5 27l1.5-4.5L17 12l3 3L9.5 25.5z M17.5 9.5l3-3a3 3 0 0 1 5 5l-3 3z", OR, OR_D)), 5, 27)
    c["all-scroll"] = c["move"]
    c["dnd-none"] = c["grabbing"]
    c["X_cursor"] = c["not-allowed"]
    return c


ANIMATED = {"wait": None, "progress": None}

ALIASES = {
    "default": ["left_ptr", "arrow", "top_left_arrow", "x-cursor", "default-arrow"],
    "pointer": ["hand2", "hand1", "hand", "pointing_hand", "openhand_link",
                "9d800788f1b08800ae810202380a0822", "e29285e634086352946a0e7090d73106"],
    "text": ["xterm", "ibeam"],
    "wait": ["watch", "busy"],
    "progress": ["left_ptr_watch", "half-busy", "3ecb610c1bf2410f44200f48c40d3599",
                 "00000000000000020006000e7e9ffc3f", "08e8e1c95fe2fc01f976f1e063a24ccd"],
    "crosshair": ["cross", "tcross", "cross_reverse", "diamond_cross", "target"],
    "move": ["fleur", "size_all", "dnd-move", "4498f0e0c1937ffe01fd06f973665830", "9081237383d90e509aa00f00170e968f"],
    "grab": ["openhand", "fcf21c00b30f7e3f83fe0dfd12e71cff"],
    "grabbing": ["closedhand", "dragging"],
    "not-allowed": ["crossed_circle", "no-drop", "forbidden", "circle", "dnd-no-drop", "pirate",
                    "03b6e0fcb3499374a867c041f52298f0"],
    "help": ["question_arrow", "whats_this", "left_ptr_help", "dnd-ask",
             "d9ce0ab605698f320427677b458ad60b", "5c6cd98b3f3ebcb1f9c7f1c204630408"],
    "copy": ["dnd-copy", "1081e37283d90000800003c07f3ef6bf", "6407b0e94181790501fd1e167b474872"],
    "alias": ["dnd-link", "link", "640fb0e74195791501fd1ed57b41487f", "3085a0e285430894940527032f8b26df"],
    "cell": ["plus"],
    "ns-resize": ["n-resize", "s-resize", "top_side", "bottom_side", "size_ver", "v_double_arrow", "sb_v_double_arrow",
                  "00008160000006810000408080010102"],
    "ew-resize": ["e-resize", "w-resize", "left_side", "right_side", "size_hor", "h_double_arrow", "sb_h_double_arrow",
                  "028006030e0e7ebffc7f7070c0600140"],
    "nesw-resize": ["ne-resize", "sw-resize", "top_right_corner", "bottom_left_corner", "size_bdiag",
                    "fd_double_arrow", "fcf1c3c7cd4491d801f1e1c78f100000"],
    "nwse-resize": ["nw-resize", "se-resize", "top_left_corner", "bottom_right_corner", "size_fdiag",
                    "bd_double_arrow", "c7088f0f3e6c8088236ef8e1e3e70000"],
    "col-resize": ["split_h", "14fef782d02440884392942c11205230"],
    "row-resize": ["split_v", "2870a09082c103050810ffdffffe0204"],
    "pencil": ["draft"],
    "color-picker": ["dropper"],
    "zoom-in": ["zoom_in"],
    "zoom-out": ["zoom_out"],
}


def build():
    import cairosvg
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    curdir = os.path.join(OUT, "cursors")
    os.makedirs(curdir)
    tmp = tempfile.mkdtemp()
    statics = cursors()
    frames = {}
    for k in range(12):
        rot = k * 30
        frames.setdefault("wait", []).append((svg(pinwheel(16, 16, 11, rot)), 16, 16))
        frames.setdefault("progress", []).append((svg(arrow(pinwheel(23, 23, 6.5, rot))), 3, 2))
    jobs = {name: [v] for name, v in statics.items()}
    jobs.update(frames)
    previews = {}
    for name, items in jobs.items():
        lines = []
        for fi, (s, hx, hy) in enumerate(items):
            for size in SIZES:
                png = os.path.join(tmp, f"{name}-{fi}-{size}.png")
                cairosvg.svg2png(bytestring=s.encode(), write_to=png, output_width=size, output_height=size)
                k = size / 32
                delay = " 60" if len(items) > 1 else ""
                lines.append(f"{size} {round(hx * k)} {round(hy * k)} {png}{delay}")
                if fi == 0 and size == 48:
                    previews[name] = png
        cfg = os.path.join(tmp, name + ".cfg")
        with open(cfg, "w") as f:
            f.write("\n".join(lines) + "\n")
        subprocess.run(["xcursorgen", cfg, os.path.join(curdir, name)], check=True)
    n = 0
    for target, al in ALIASES.items():
        for a in al:
            p = os.path.join(curdir, a)
            if not os.path.lexists(p):
                os.symlink(target, p)
                n += 1
    with open(os.path.join(OUT, "index.theme"), "w") as f:
        f.write("[Icon Theme]\nName=Tunudan-cursors\nComment=Curseurs origami Tunudan\nInherits=Adwaita\n")
    with open(os.path.join(OUT, "cursor.theme"), "w") as f:
        f.write("[Icon Theme]\nInherits=Tunudan-cursors\n")
    print(f"Curseurs Tunudan : {len(jobs)} curseurs, {n} alias, tailles {SIZES}")
    if "--preview" in sys.argv:
        from PIL import Image
        names = list(previews)
        cell, cols = 72, 10
        rows = (len(names) + cols - 1) // cols
        for bg, suf in (((24, 24, 26), "sombre"), ((243, 237, 228), "clair")):
            im = Image.new("RGB", (cols * cell, rows * cell), bg)
            for i, nm in enumerate(names):
                p = Image.open(previews[nm]).convert("RGBA")
                im.paste(p, ((i % cols) * cell + 12, (i // cols) * cell + 12), p)
            im.save(f"/tmp/curseurs-{suf}.png")
        print("Aperçu : /tmp/curseurs-sombre.png, /tmp/curseurs-clair.png")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    build()

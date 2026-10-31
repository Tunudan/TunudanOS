#!/usr/bin/env python3
"""Aperçus schématiques des bureaux (choix du bureau dans les installateurs).

    python3 themes/desktops/build_cards.py

Écrit themes/shared/desktops/<id>.png (800x500) et desktops.tsv (id, nom, description).
"""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "..", "shared", "desktops")
WALL = os.path.join(ROOT, "branding", "out", "wallpapers", "origami", "origami-envolee-sombre.png")
OR, OR_D, OR_L = "#FF6B1A", "#C2410C", "#FF9A5C"
BG0, BG1, BG2, BG3, FG = "#0D0D0D", "#141416", "#1C1C1E", "#2A2A2C", "#F5F1EA"

DESKTOPS = [
    ("cinnamon", "Cinnamon", "Le bureau de Linux Mint : menu en bas à gauche, très proche de Windows. Idéal pour débuter."),
    ("mate", "MATE", "Classique et économe : deux barres (menus en haut, fenêtres en bas). Parfait pour les ordinateurs anciens."),
    ("xfce", "Xfce", "Léger, rapide et simple. Une barre en bas, tout est à portée de main."),
    ("gnome", "GNOME", "Moderne et épuré : une barre en haut, les applications en plein écran avec la touche Super."),
    ("plasma", "KDE Plasma", "Complet et personnalisable à l'infini, avec de beaux effets. Barre en bas comme Windows."),
    ("lxqt", "LXQt", "Ultra-léger, basé sur Qt. Pour les petites configurations."),
    ("budgie", "Budgie", "Élégant et simple, avec un panneau latéral pour les notifications et réglages rapides."),
    ("cosmic", "COSMIC", "Le nouveau bureau de System76, rapide (écrit en Rust), avec un dock et la mosaïque intégrée."),
    ("hyprland", "Hyprland", "Gestionnaire en mosaïque très animé : flou, coins arrondis, tout au clavier. Pour experts."),
    ("sway", "Sway", "Mosaïque Wayland sobre et stable, compatible i3. Tout au clavier."),
    ("i3", "i3", "Le classique de la mosaïque sous X11 : minimaliste, rapide, entièrement au clavier."),
    ("niri", "niri", "Les fenêtres s'alignent sur une bande infinie qu'on fait défiler. Original et efficace."),
]


def win(x, y, w, h, title=True, r=8, active=False, border=None):
    s = f'<rect x="{x + 3}" y="{y + 5}" width="{w}" height="{h}" rx="{r}" fill="#000" fill-opacity=".35"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{BG2}"'
    if border:
        s += f' stroke="{border}" stroke-width="3"'
    s += "/>"
    if title:
        s += f'<path d="M{x} {y + r}a{r} {r} 0 0 1 {r}-{r}h{w - 2 * r}a{r} {r} 0 0 1 {r} {r}v14H{x}z" fill="{BG0}"/>'
        if active:
            s += f'<rect x="{x}" y="{y}" width="{w}" height="3" fill="{OR}"/>'
        s += "".join(f'<circle cx="{x + w - 14 - i * 14}" cy="{y + 11}" r="4" fill="{OR if i == 0 and active else "#5A5753"}"/>' for i in range(3))
    # lignes de contenu
    top = y + (30 if title else 14)
    for i in range(min(5, max(1, (h - 40) // 22))):
        lw = w * (0.75 - 0.1 * (i % 3))
        s += f'<rect x="{x + 14}" y="{top + i * 20}" width="{lw:.0f}" height="8" rx="4" fill="{BG3}"/>'
    if h > 120:
        s += f'<rect x="{x + 14}" y="{y + h - 46}" width="{w * .35:.0f}" height="30" rx="6" fill="{OR}" fill-opacity=".85"/>'
    return s


def icons(x, y, n, size=22, gap=10, vertical=False):
    cols = [OR, "#3A7BD5", "#2E9E5B", "#7B5EA7", "#D9A441", "#E5484D", "#23998E"]
    s = ""
    for i in range(n):
        xx, yy = (x, y + i * (size + gap)) if vertical else (x + i * (size + gap), y)
        s += f'<rect x="{xx}" y="{yy}" width="{size}" height="{size}" rx="{size * .25}" fill="{cols[i % len(cols)]}"/>'
    return s


def crane(x, y, s):
    pts = [((92, 150), (40, 118), (106, 169)), ((128, 108), (92, 150), (30, 56)), ((128, 108), (164, 150), (226, 56)),
           ((92, 150), (128, 204), (164, 150))]
    out = ""
    for i, tri in enumerate(pts):
        p = " ".join(f"{x + (px - 128) * s:.1f},{y + (py - 130) * s:.1f}" for px, py in tri)
        out += f'<polygon points="{p}" fill="{OR if i % 2 else OR_L}"/>'
    return out


def layout(dk):
    s = ""
    if dk in ("cinnamon", "xfce", "plasma", "lxqt"):
        h = {"cinnamon": 40, "xfce": 36, "plasma": 44, "lxqt": 32}[dk]
        s += win(70, 50, 420, 300, active=True) + win(330, 120, 380, 250, active=False)
        if dk == "xfce":
            s += icons(18, 30, 4, 26, 22, vertical=True)
        s += f'<rect x="0" y="{500 - h}" width="800" height="{h}" fill="{BG0}" fill-opacity=".95"/>'
        s += crane(26, 500 - h / 2, .13)
        s += icons(60, 500 - h + (h - 24) / 2, 5, 24, 10)
        s += f'<rect x="250" y="{500 - h + 6}" width="150" height="{h - 12}" rx="5" fill="{BG3}"/><rect x="250" y="{500 - 4}" width="150" height="3" fill="{OR}"/>'
        s += f'<rect x="690" y="{500 - h + (h - 12) / 2}" width="90" height="12" rx="6" fill="{BG3}"/>'
        if dk == "cinnamon":
            s += f'<rect x="10" y="190" width="230" height="260" rx="10" fill="{BG2}" stroke="{BG3}"/>' + \
                 "".join(f'<rect x="26" y="{210 + i * 32}" width="{150 - (i % 3) * 25}" height="14" rx="7" fill="{OR if i == 2 else BG3}"/>' for i in range(7))
    elif dk == "mate":
        s += f'<rect x="0" y="0" width="800" height="30" fill="{BG0}"/>' + crane(22, 15, .1)
        s += "".join(f'<rect x="{44 + i * 90}" y="10" width="70" height="10" rx="5" fill="{BG3}"/>' for i in range(3))
        s += f'<rect x="690" y="10" width="90" height="10" rx="5" fill="{BG3}"/>'
        s += win(80, 60, 400, 290, active=True) + win(360, 120, 360, 250)
        s += f'<rect x="0" y="468" width="800" height="32" fill="{BG0}"/>'
        s += "".join(f'<rect x="{12 + i * 160}" y="474" width="150" height="20" rx="4" fill="{BG3 if i else OR_D}"/>' for i in range(3))
    elif dk in ("gnome", "cosmic"):
        s += f'<rect x="0" y="0" width="800" height="28" fill="{BG0}"/><rect x="360" y="9" width="80" height="10" rx="5" fill="{FG}" fill-opacity=".8"/>'
        s += f'<rect x="12" y="7" width="60" height="14" rx="7" fill="{BG3}"/><rect x="700" y="9" width="86" height="10" rx="5" fill="{BG3}"/>'
        s += win(140, 70, 520, 330, active=True, r=12)
        dw = 330 if dk == "gnome" else 380
        s += f'<rect x="{400 - dw / 2}" y="420" width="{dw}" height="56" rx="18" fill="{BG1}" fill-opacity=".92" stroke="{BG3}"/>'
        s += icons(400 - dw / 2 + 18, 432, 8 if dk == "gnome" else 9, 32, 8)
    elif dk == "budgie":
        s += f'<rect x="0" y="0" width="800" height="30" fill="{BG0}"/>' + crane(22, 15, .1) + icons(50, 6, 5, 18, 8)
        s += win(40, 60, 430, 330, active=True) + f'<rect x="560" y="30" width="240" height="470" fill="{BG1}" fill-opacity=".96"/>'
        s += "".join(f'<rect x="578" y="{56 + i * 70}" width="204" height="54" rx="10" fill="{BG2}"/>' for i in range(5))
        s += f'<rect x="578" y="56" width="204" height="4" fill="{OR}"/>'
    elif dk in ("hyprland", "sway", "i3"):
        gap, r = (14, 12) if dk == "hyprland" else (6, 0)
        top = 34 if dk != "i3" else 8
        bot = 500 - (30 if dk == "i3" else 0)
        x0, x1, y0, y1 = gap, 800 - gap, top + gap, bot - gap
        mid = (x0 + x1) / 2
        rows = (y0 + y1) / 2
        bcol = OR if dk != "i3" else OR
        s += win(x0, y0, mid - x0 - gap / 2, y1 - y0, title=(dk == "i3"), r=r, active=True, border=bcol)
        s += win(mid + gap / 2, y0, x1 - mid - gap / 2, rows - y0 - gap / 2, title=(dk == "i3"), r=r, border=BG3)
        s += win(mid + gap / 2, rows + gap / 2, x1 - mid - gap / 2, y1 - rows - gap / 2, title=(dk == "i3"), r=r, border=BG3)
        if dk == "hyprland":
            s += f'<rect x="{gap}" y="6" width="{800 - 2 * gap}" height="24" rx="10" fill="{BG0}" fill-opacity=".9"/>' + icons(gap + 10, 10, 4, 16, 6)
            s += f'<rect x="360" y="12" width="80" height="12" rx="6" fill="{OR_L}"/>'
        elif dk == "sway":
            s += f'<rect x="0" y="0" width="800" height="26" fill="{BG0}"/>' + icons(6, 4, 4, 18, 4) + f'<rect x="690" y="8" width="100" height="10" rx="5" fill="{BG3}"/>'
        else:
            s += f'<rect x="0" y="470" width="800" height="30" fill="{BG0}"/>' + icons(6, 476, 3, 18, 4) + f'<rect x="640" y="480" width="150" height="10" rx="5" fill="{BG3}"/>'
    elif dk == "niri":
        s += f'<rect x="0" y="0" width="800" height="28" fill="{BG0}"/>' + icons(8, 5, 4, 18, 6)
        xs = [(-160, 260, False), (120, 300, True), (440, 260, False), (720, 260, False)]
        for x, w, act in xs:
            s += win(x, 50, w, 410, r=12, border=OR if act else None, active=act)
        s += f'<path d="M40 480l-20-12 20-12M760 480l20-12-20-12" fill="none" stroke="{OR_L}" stroke-width="4" stroke-linecap="round"/>'
    return s


def card(dk):
    with open(WALL, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="800" height="500" viewBox="0 0 800 500">'
            f'<image width="800" height="500" preserveAspectRatio="xMidYMid slice" xlink:href="data:image/png;base64,{b64}"/>'
            f'<rect width="800" height="500" fill="{BG0}" fill-opacity=".35"/>{layout(dk)}</svg>')


def main():
    global WALL
    import cairosvg
    from PIL import Image
    os.makedirs(OUT, exist_ok=True)
    # fond réduit une seule fois pour des cartes légères
    small = "/tmp/tunudan-card-bg.png"
    Image.open(WALL).resize((800, 450)).save(small)
    WALL = small
    with open(os.path.join(OUT, "desktops.tsv"), "w", encoding="utf-8") as f:
        for dk, name, desc in DESKTOPS:
            cairosvg.svg2png(bytestring=card(dk).encode(), write_to=os.path.join(OUT, dk + ".png"),
                             output_width=800, output_height=500)
            f.write(f"{dk}\t{name}\t{desc}\n")
    print("Aperçus des bureaux :", len(DESKTOPS))


if __name__ == "__main__":
    main()

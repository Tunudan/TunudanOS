"""Thèmes propres à certains bureaux : Cinnamon (SASS recompilé), LXQt (recoloré),
Plasma (copie des fichiers du paquet), visuels partagés. Appelé par build.py."""
import os
import re
import shutil


def copytree(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


# ----------------------------------------------------------------- Cinnamon
def cinnamon(P, HERE):
    try:
        import sass  # libsass
    except ImportError:
        print("  ! libsass absent (pip install libsass) : thème Cinnamon non régénéré")
        return
    src = os.path.join(HERE, "vendor", "cinnamon-theme")
    work = os.path.join(HERE, ".build-cinnamon")
    copytree(os.path.join(src, "cinnamon-sass"), work)
    colors = f"""// Palette Tunudan (remplace le _colors.scss de Cinnamon)
$bg_color: {P["bg2"]};
$base_color: {P["bg3"]};
$fg_color: {P["fg"]};
$panel_bg: {P["bg0"]};
$error_color: {P["red"]};
$error_bg_color: #c01c28;
$success_color: #8fe39a;
$success_bg_color: #2f8f3a;
$destructive_bg_color: #c01c28;
$destructive_color: {P["red"]};
$warning_color: {P["yellow"]};
$warning_bg_color: #cd9309;
$notification_badge_bg_color: {P["accent"]};
$accent_color: {P["accent_light"]};
$accent_bg_color: {P["accent"]};
$large_icon_color: transparentize($fg_color, 0.6);
$light_text_color: mix($fg_color, $bg_color, 65%);
$light_bg_color: #313134;
$light_base_color: #3c3c40;
$lighter_bg_color: #444448;
$lightest_bg_color: #5e5e62;
$link_color: {P["accent_light"]};
$borders_color: {P["bg3"]};
$shadow_color: rgba(0, 0, 0, 0.55);
$insensitive_fg_color: mix($fg_color, $bg_color, 40%);
"""
    with open(os.path.join(work, "_colors.scss"), "w", encoding="utf-8") as f:
        f.write(colors)
    css = sass.compile(filename=os.path.join(work, "cinnamon.scss"), output_style="expanded")
    dst = os.path.join(HERE, "cinnamon", "theme", "Tunudan", "cinnamon")
    os.makedirs(dst, exist_ok=True)
    with open(os.path.join(dst, "cinnamon.css"), "w", encoding="utf-8") as f:
        f.write("/* Thème Cinnamon par défaut (GPL-2.0-or-later) recompilé avec la palette "
                "Tunudan par themes/build.py */\n" + css)
    for name in os.listdir(src):
        if name.endswith((".svg", ".png")):
            shutil.copy(os.path.join(src, name), dst)
    toggle = os.path.join(dst, "toggle-on.svg")
    with open(toggle, encoding="utf-8") as f:
        svg = f.read().replace("#3584e4", P["accent"].lower())
    with open(toggle, "w", encoding="utf-8") as f:
        f.write(svg)
    shutil.copy(os.path.join(HERE, "shared", "logo", "tunudan-256.png"),
                os.path.join(dst, "thumbnail.png"))
    shutil.rmtree(work)
    print("  Cinnamon :", len(css.splitlines()), "lignes de CSS")


# ----------------------------------------------------------------- LXQt
LXQT_MAP = {
    "rgba(0, 0, 0, 50%)": "rgba(13, 13, 13, 92%)",
    "rgba(0, 0, 0, 80%)": "rgba(28, 28, 30, 96%)",
    "rgba(0, 0, 0, 40%)": "rgba(13, 13, 13, 70%)",
    "rgba(0, 0, 0, 35%)": "rgba(13, 13, 13, 60%)",
    "rgba(255, 255, 255, 20%)": "rgba(255, 107, 26, 30%)",
    "rgba(255, 255, 255, 25%)": "rgba(255, 107, 26, 38%)",
    "rgba(255, 255, 255, 30%)": "rgba(255, 107, 26, 45%)",
    "rgba(255, 255, 255, 40%)": "rgba(255, 107, 26, 60%)",
    "rgba(50, 50, 50, 80%)": "rgba(28, 28, 30, 92%)",
    "hsv(0, 0, 41)": "#2A2A2C",
    "hsv(0, 0, 20)": "#1C1C1E",
    "#640b0c": "#FF6B1A",
    "#500709": "#C2410C",
    "#880c10": "#FF9A5C",
    "#870e10": "#FF9A5C",
    "#d21518": "#FF6B1A",
    "#C94C21": "#FF6B1A",
    "#eb7140": "#FF9A5C",
    "#DEDEDE": "#F5F1EA",
    "#DDDDDD": "#F5F1EA",
    "#EEEEEE": "#F5F1EA",
    "#3c3c3c": "#2A2A2C",
    "#1e1e1e": "#141416",
}


def lxqt(P, HERE):
    src = os.path.join(HERE, "vendor", "lxqt-dark")
    dst = os.path.join(HERE, "lxqt", "theme", "Tunudan")
    copytree(src, dst)
    for name in os.listdir(dst):
        if not name.endswith(".qss"):
            continue
        path = os.path.join(dst, name)
        with open(path, encoding="utf-8") as f:
            qss = f.read()
        for old, new in LXQT_MAP.items():
            qss = re.sub(re.escape(old), new, qss, flags=re.IGNORECASE)
        with open(path, "w", encoding="utf-8") as f:
            f.write("/* Thème LXQt « dark » (LGPL-2.1-or-later) recoloré Tunudan */\n" + qss)
    with open(os.path.join(dst, "wallpaper.cfg"), "w", encoding="utf-8") as f:
        f.write("wallpapers/size=1\nwallpapers/1/file=wallpaper.png\n")
    shutil.copy(os.path.join(HERE, "shared", "wallpapers", "tunudan-sombre-1920x1080.png"),
                os.path.join(dst, "wallpaper.png"))
    shutil.copy(os.path.join(HERE, "shared", "logo", "tunudan-256.png"), os.path.join(dst, "preview.png"))
    shutil.copy(os.path.join(HERE, "shared", "logo", "tunudan-64.png"), os.path.join(dst, "mainmenu.png"))
    if os.path.exists(os.path.join(dst, "mainmenu.svg")):
        os.remove(os.path.join(dst, "mainmenu.svg"))
    for name in os.listdir(dst):
        if name.endswith(".qss"):
            p = os.path.join(dst, name)
            with open(p, encoding="utf-8") as f:
                t = f.read().replace("mainmenu.svg", "mainmenu.png")
            with open(p, "w", encoding="utf-8") as f:
                f.write(t)
    os.makedirs(os.path.join(HERE, "lxqt", "palettes"), exist_ok=True)
    with open(os.path.join(HERE, "lxqt", "palettes", "Tunudan"), "w", encoding="utf-8") as f:
        f.write(f"""[Palette]
base_color={P["bg1"]}
highlight_color={P["accent"]}
highlighted_text_color={P["bg0"]}
link_color={P["accent_light"]}
link_visited_color={P["accent_dark"]}
text_color={P["fg"]}
window_color={P["bg2"]}
window_text_color={P["fg"]}
tooltip_base_color={P["bg2"]}
tooltip_text_color={P["fg"]}
""")


# ----------------------------------------------------------------- visuels et Plasma
def shared_assets(HERE, ROOT):
    out = os.path.join(ROOT, "branding", "out")
    wall = os.path.join(HERE, "shared", "wallpapers")
    logo = os.path.join(HERE, "shared", "logo")
    os.makedirs(wall, exist_ok=True)
    os.makedirs(logo, exist_ok=True)
    for name in ("tunudan-sombre-1920x1080.png", "tunudan-sombre-3840x2160.png",
                 "tunudan-slogan-1920x1080.png", "tunudan-slogan-3840x2160.png",
                 "tunudan-clair-1920x1080.png"):
        shutil.copy(os.path.join(out, "wallpapers", name), wall)
    org_src = os.path.join(out, "wallpapers", "origami")
    if os.path.isdir(org_src):
        org = os.path.join(wall, "origami")
        os.makedirs(org, exist_ok=True)
        for name in sorted(os.listdir(org_src)):
            if name.endswith(".png") and "preview" not in name:
                shutil.copy(os.path.join(org_src, name), org)
    for size in (48, 64, 128, 256):
        shutil.copy(os.path.join(out, "logo", f"tunudan-{size}.png"), logo)
    shutil.copy(os.path.join(ROOT, "branding", "logo.svg"), os.path.join(logo, "tunudan.svg"))


def plasma(HERE, ROOT):
    """themes/plasma/files est la source (couleurs, Konsole, thème global) ;
    seul le fond « Tunudan » est rafraîchi depuis les visuels générés."""
    pk = os.path.join(ROOT, "packages")
    dst = os.path.join(HERE, "plasma", "files")
    wall = os.path.join(pk, "tunudan-theme", "files", "kde-wallpaper", "Tunudan")
    if os.path.isdir(os.path.join(wall, "contents", "images")):
        copytree(wall, os.path.join(dst, "wallpaper-Tunudan"))


# ----------------------------------------------------------------- GTK 3
def gtk3_theme(HERE):
    """Thème GTK 3 « Tunudan » autonome : adw-gtk3-dark compilé + couleurs Tunudan."""
    import subprocess
    sass_bin = shutil.which("sass")
    if not sass_bin:
        print("  ! Dart Sass absent (npm install -g sass) : thème GTK 3 non régénéré")
        return
    src = os.path.join(HERE, "vendor", "adw-gtk3")
    dst = os.path.join(HERE, "shared", "gtk", "Tunudan", "gtk-3.0")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    css = subprocess.run([sass_bin, "--no-source-map", "--style=expanded",
                          os.path.join(src, "sass", "gtk-dark.scss")],
                         check=True, capture_output=True, text=True).stdout
    with open(os.path.join(HERE, "shared", "gtk", "tunudan-overrides.css"), encoding="utf-8") as f:
        overrides = f.read()
    full = ("/* Thème GTK 3 Tunudan : adw-gtk3-dark (LGPL-2.1-or-later) + palette Tunudan.\n"
            "   Généré par themes/build.py. */\n" + css + "\n" + overrides)
    for name in ("gtk.css", "gtk-dark.css"):
        with open(os.path.join(dst, name), "w", encoding="utf-8") as f:
            f.write(full)
    shutil.copytree(os.path.join(src, "assets"), os.path.join(dst, "assets"))
    print("  GTK 3 :", len(full.splitlines()), "lignes de CSS")


def desktops(P, write, HEADER, HERE, ROOT):
    shared_assets(HERE, ROOT)
    gtk3_theme(HERE)
    plasma(HERE, ROOT)
    cinnamon(P, HERE)
    lxqt(P, HERE)

"""Décorations de fenêtres Tunudan : xfwm4 (Xfce), Openbox/labwc (LXQt, Budgie),
Metacity (MATE, Cinnamon). Appelé par build.py."""

H = 30          # hauteur de la barre de titre (xfwm4)
B = 4           # largeur des bordures (xfwm4)


# ----------------------------------------------------------------- XPM
class Canvas:
    def __init__(self, w, h, fill="."):
        self.w, self.h = w, h
        self.px = [[fill] * w for _ in range(h)]

    def set(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y][x] = ch

    def rect(self, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.set(x, y, ch)

    def disc(self, cx, cy, r, ch):
        for y in range(self.h):
            for x in range(self.w):
                if (x - cx + 0.5) ** 2 + (y - cy + 0.5) ** 2 <= r * r:
                    self.set(x, y, ch)

    def rows(self):
        return ["".join(r) for r in self.px]


def xpm_text(name, canvas, colors):
    ident = name.replace("-", "_")
    head = [f'"{canvas.w} {canvas.h} {len(colors)} 1"']
    head += [f'"{ch} c {col}"' for ch, col in colors.items()]
    body = [f'"{r}"' for r in canvas.rows()]
    return f"/* XPM */\nstatic char * {ident}_xpm[] = {{\n" + ",\n".join(head + body) + "};\n"


def glyph(c, kind, cx, cy, ch):
    """Dessine un pictogramme de 10 px centré sur (cx, cy)."""
    x0, y0 = cx - 5, cy - 5
    if kind == "close":
        for t in range(10):
            for d in (0, 1):
                c.set(x0 + t + d, y0 + t, ch)
                c.set(x0 + 9 - t + d, y0 + t, ch)
    elif kind == "hide":
        c.rect(x0, y0 + 7, x0 + 9, y0 + 8, ch)
    elif kind == "maximize":
        c.rect(x0, y0, x0 + 9, y0 + 1, ch)
        c.rect(x0, y0, x0, y0 + 9, ch)
        c.rect(x0 + 9, y0, x0 + 9, y0 + 9, ch)
        c.rect(x0, y0 + 9, x0 + 9, y0 + 9, ch)
    elif kind == "maximize-toggled":
        c.rect(x0 + 2, y0, x0 + 9, y0 + 1, ch)
        c.rect(x0 + 9, y0, x0 + 9, y0 + 7, ch)
        c.rect(x0, y0 + 2, x0 + 7, y0 + 3, ch)
        c.rect(x0, y0 + 2, x0, y0 + 9, ch)
        c.rect(x0 + 7, y0 + 2, x0 + 7, y0 + 9, ch)
        c.rect(x0, y0 + 9, x0 + 7, y0 + 9, ch)
    elif kind in ("shade", "shade-toggled"):
        up = kind == "shade"
        for t in range(5):
            y = (y0 + 7 - t) if up else (y0 + 3 + t)
            for d in (0, 1):
                c.set(x0 + t, y + d, ch)
                c.set(x0 + 9 - t, y + d, ch)
    elif kind == "stick":
        c.disc(cx, cy, 2.2, ch)
    elif kind == "stick-toggled":
        c.disc(cx, cy, 3.5, ch)
    elif kind == "menu":
        for y in range(-4, 5):
            for x in range(-4, 5):
                if abs(x) + abs(y) <= 4:
                    c.set(cx + x, cy + y, "d")


def xfwm4(P, write, HEADER):
    base = "xfce/xfwm4/Tunudan/xfwm4/"
    state_colors = {
        "active": {".": P["bg0"], "o": P["accent"], "b": P["bg3"], "g": P["fg"]},
        "inactive": {".": P["bg1"], "o": P["bg3"], "b": P["bg3"], "g": P["fg_muted"]},
    }

    def piece(name, w, h, state, draw=None, top=True):
        c = Canvas(w, h)
        if top:
            c.rect(0, 0, w - 1, 1, "o")
        if draw:
            draw(c)
        cols = dict(state_colors[state])
        write(base + name + ".xpm", xpm_text(name, c, cols))

    for st in ("active", "inactive"):
        for n in range(1, 6):
            piece(f"title-{n}-{st}", 2, H, st)
        piece(f"top-left-{st}", B, H, st, lambda c: c.rect(0, 0, 0, H - 1, "b") if False else None)
        piece(f"top-right-{st}", B, H, st)
        piece(f"left-{st}", B, 2, st, lambda c: c.rect(0, 0, 0, 1, "b"), top=False)
        piece(f"right-{st}", B, 2, st, lambda c: c.rect(B - 1, 0, B - 1, 1, "b"), top=False)
        piece(f"bottom-{st}", 2, B, st, lambda c: c.rect(0, B - 1, 1, B - 1, "b"), top=False)
        piece(f"bottom-left-{st}", B, B, st,
              lambda c: (c.rect(0, 0, 0, B - 1, "b"), c.rect(0, B - 1, B - 1, B - 1, "b")), top=False)
        piece(f"bottom-right-{st}", B, B, st,
              lambda c: (c.rect(B - 1, 0, B - 1, B - 1, "b"), c.rect(0, B - 1, B - 1, B - 1, "b")), top=False)

    buttons = ["close", "hide", "maximize", "maximize-toggled", "menu",
               "shade", "shade-toggled", "stick", "stick-toggled"]
    for btn in buttons:
        for st in ("active", "inactive", "prelight", "pressed"):
            c = Canvas(H, H)
            c.rect(0, 0, H - 1, 1, "o")
            cols = {".": P["bg0"] if st != "inactive" else P["bg1"],
                    "o": P["accent"] if st != "inactive" else P["bg3"],
                    "g": P["fg"] if st != "inactive" else P["fg_muted"],
                    "d": P["accent"] if st != "inactive" else P["fg_muted"]}
            if st in ("prelight", "pressed"):
                is_close = btn == "close"
                circle = (P["accent"] if st == "prelight" else P["accent_dark"]) if is_close else \
                         (P["bg3"] if st == "prelight" else P["bg4"])
                cols["c"] = circle
                c.disc(H / 2, H / 2 + 1, 11, "c")
                if is_close:
                    cols["g"] = P["bg0"]
            glyph(c, btn, H // 2, H // 2 + 1, "g")
            used = {ch for row in c.rows() for ch in row}
            cols = {k: v for k, v in cols.items() if k in used}
            write(base + f"{btn}-{st}.xpm", xpm_text(f"{btn}-{st}", c, cols))

    write(base + "themerc", f"""
# {HEADER}
button_offset=4
button_spacing=2
full_width_title=true
title_alignment=center
title_horizontal_offset=0
title_vertical_offset_active=1
title_vertical_offset_inactive=1
title_shadow_active=false
title_shadow_inactive=false
active_text_color={P["fg"]}
inactive_text_color={P["fg_muted"]}
show_frame_shadow=true
show_popup_shadow=true
shadow_delta_height=2
shadow_delta_width=0
shadow_delta_x=0
shadow_delta_y=-5
shadow_opacity=45
""")


# ----------------------------------------------------------------- Openbox / labwc
def xbm_text(name, rows):
    w, h = len(rows[0]), len(rows)
    data = []
    for r in rows:
        byte, val = 0, 0
        bits = []
        for x, ch in enumerate(r):
            if ch == "#":
                val |= 1 << (x % 8)
            if x % 8 == 7 or x == w - 1:
                bits.append(val)
                val = 0
        data += bits
    hexes = ", ".join(f"0x{b:02x}" for b in data)
    ident = name.replace("-", "_")
    return (f"#define {ident}_width {w}\n#define {ident}_height {h}\n"
            f"static unsigned char {ident}_bits[] = {{\n   {hexes} }};\n")


XBM = {
    "close": ["##....##", "###..###", ".######.", "..####..", "..####..", ".######.", "###..###", "##....##"],
    "max": ["########", "########", "#......#", "#......#", "#......#", "#......#", "#......#", "########"],
    "max_toggled": ["..######", "..######", "..#....#", "######.#", "######.#", "#....###", "#....#..", "######.."],
    "iconify": ["........", "........", "........", "........", "........", "........", "########", "########"],
    "desk": ["........", "........", "...##...", "..####..", "..####..", "...##...", "........", "........"],
    "desk_toggled": ["........", "..####..", ".######.", ".######.", ".######.", ".######.", "..####..", "........"],
    "shade": ["........", "........", "...##...", "..####..", ".##..##.", "##....##", "........", "........"],
    "shade_toggled": ["........", "........", "##....##", ".##..##.", "..####..", "...##...", "........", "........"],
    "menu": ["...##...", "..####..", ".######.", "########", "########", ".######.", "..####..", "...##..."],
}


def openbox(P, write, HEADER):
    base = "shared/openbox/Tunudan/openbox-3/"
    for name, rows in XBM.items():
        write(base + f"{name}.xbm", xbm_text(name, rows))
    def win(st, bg, title_fg, btn_fg, border):
        return f"""
window.{st}.border.color: {border}
window.{st}.title.bg: flat solid
window.{st}.title.bg.color: {bg}
window.{st}.label.bg: parentrelative
window.{st}.label.text.color: {title_fg}
window.{st}.handle.bg: flat solid
window.{st}.handle.bg.color: {bg}
window.{st}.grip.bg: flat solid
window.{st}.grip.bg.color: {bg}
window.{st}.client.color: {bg}
window.{st}.button.unpressed.bg: parentrelative
window.{st}.button.unpressed.image.color: {btn_fg}
window.{st}.button.hover.bg: flat solid
window.{st}.button.hover.bg.color: {P["bg3"]}
window.{st}.button.hover.image.color: {P["fg"]}
window.{st}.button.pressed.bg: flat solid
window.{st}.button.pressed.bg.color: {P["accent_dark"]}
window.{st}.button.pressed.image.color: {P["bg0"]}
window.{st}.button.disabled.bg: parentrelative
window.{st}.button.disabled.image.color: {P["bg4"]}
window.{st}.button.toggled.unpressed.bg: parentrelative
window.{st}.button.toggled.unpressed.image.color: {P["accent"]}
window.{st}.button.toggled.hover.bg: flat solid
window.{st}.button.toggled.hover.bg.color: {P["bg3"]}
window.{st}.button.toggled.hover.image.color: {P["accent_light"]}
window.{st}.button.toggled.pressed.bg: flat solid
window.{st}.button.toggled.pressed.bg.color: {P["accent_dark"]}
window.{st}.button.toggled.pressed.image.color: {P["bg0"]}"""
    write(base + "themerc", f"""
# {HEADER}
# Openbox 3 (LXQt, X11) et labwc (LXQt 2, Budgie 10.10 sous Wayland)
border.width: 1
padding.width: 8
padding.height: 6
window.handle.width: 0
window.client.padding.width: 0
window.client.padding.height: 0
window.label.text.justify: center
window.active.label.text.font: Inter:bold:size=10
window.inactive.label.text.font: Inter:bold:size=10
{win("active", P["bg0"], P["fg"], P["fg"], P["accent"])}
{win("inactive", P["bg1"], P["fg_muted"], P["fg_muted"], P["bg3"])}
window.active.button.close.hover.bg: flat solid
window.active.button.close.hover.bg.color: {P["accent"]}
window.active.button.close.hover.image.color: {P["bg0"]}

# labwc : coins arrondis et ombres
corner.radius: 10
window.active.shadow.size: 30
window.inactive.shadow.size: 18
window.active.shadow.color: #00000088
window.inactive.shadow.color: #00000055

menu.border.width: 1
menu.border.color: {P["bg3"]}
menu.overlap.x: 0
menu.items.bg: flat solid
menu.items.bg.color: {P["bg2"]}
menu.items.text.color: {P["fg"]}
menu.items.disabled.text.color: {P["fg_muted"]}
menu.items.active.bg: flat solid
menu.items.active.bg.color: {P["accent"]}
menu.items.active.text.color: {P["bg0"]}
menu.items.font: Inter:size=10
menu.title.bg: flat solid
menu.title.bg.color: {P["bg0"]}
menu.title.text.color: {P["accent"]}
menu.title.text.justify: center
menu.title.text.font: Inter:bold:size=10
menu.separator.color: {P["bg3"]}
menu.separator.width: 1
menu.separator.padding.width: 6
menu.separator.padding.height: 3

osd.border.width: 1
osd.border.color: {P["accent"]}
osd.bg: flat solid
osd.bg.color: {P["bg2"]}
osd.label.text.color: {P["fg"]}
osd.label.text.font: Inter:size=11
osd.hilight.bg: flat solid
osd.hilight.bg.color: {P["accent"]}
osd.unhilight.bg: flat solid
osd.unhilight.bg.color: {P["bg3"]}
osd.window-switcher.width: 600
""")


# ----------------------------------------------------------------- Metacity (MATE, Cinnamon)
def metacity(P, write, HEADER):
    def lines(color, pairs, width=2):
        return "\n".join(
            f'  <line color="{color}" width="{width}" x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>'
            for a, b, c, d in pairs)
    glyphs = {
        "close": [("width/2-4", "height/2-4", "width/2+4", "height/2+4"),
                  ("width/2+4", "height/2-4", "width/2-4", "height/2+4")],
        "minimize": [("width/2-5", "height/2+4", "width/2+5", "height/2+4")],
        "maximize": [("width/2-5", "height/2-4", "width/2+5", "height/2-4"),
                     ("width/2-5", "height/2-4", "width/2-5", "height/2+5"),
                     ("width/2+5", "height/2-4", "width/2+5", "height/2+5"),
                     ("width/2-5", "height/2+5", "width/2+5", "height/2+5")],
        "restore": [("width/2-2", "height/2-5", "width/2+5", "height/2-5"),
                    ("width/2+5", "height/2-5", "width/2+5", "height/2+2"),
                    ("width/2-5", "height/2-2", "width/2+2", "height/2-2"),
                    ("width/2-5", "height/2-2", "width/2-5", "height/2+5"),
                    ("width/2+2", "height/2-2", "width/2+2", "height/2+5"),
                    ("width/2-5", "height/2+5", "width/2+2", "height/2+5")],
        "menu": [("width/2", "height/2-4", "width/2+4", "height/2"),
                 ("width/2+4", "height/2", "width/2", "height/2+4"),
                 ("width/2", "height/2+4", "width/2-4", "height/2"),
                 ("width/2-4", "height/2", "width/2", "height/2-4")],
    }
    ops = []
    for g, pairs in glyphs.items():
        menu = g == "menu"
        for state, fg, circle in (
                ("normal", P["accent"] if menu else P["fg"], None),
                ("unfocused", P["fg_muted"], None),
                ("prelight", P["bg0"] if g == "close" else P["fg"], P["accent"] if g == "close" else P["bg3"]),
                ("pressed", P["bg0"] if g == "close" else P["fg"], P["accent_dark"] if g == "close" else P["bg4"])):
            arc = (f'  <arc color="{circle}" filled="true" x="width/2-11" y="height/2-11" '
                   f'width="22" height="22" start_angle="0" extent_angle="360"/>\n') if circle else ""
            ops.append(f'<draw_ops name="{g}_{state}">\n{arc}{lines(fg, pairs)}\n</draw_ops>')
    draw_ops = "\n\n".join(ops)

    def buttons(focused, maximized):
        out = []
        for fn, g in (("close", "close"), ("maximize", "restore" if maximized else "maximize"),
                      ("minimize", "minimize"), ("menu", "menu")):
            normal = f"{g}_normal" if focused else f"{g}_unfocused"
            out.append(f'  <button function="{fn}" state="normal" draw_ops="{normal}"/>')
            out.append(f'  <button function="{fn}" state="prelight" draw_ops="{g}_prelight"/>')
            out.append(f'  <button function="{fn}" state="pressed" draw_ops="{g}_pressed"/>')
        return "\n".join(out)

    write("shared/metacity/Tunudan/metacity-1/metacity-theme-1.xml", f"""
<?xml version="1.0"?>
<!-- {HEADER} -->
<!-- Décorations Metacity : utilisées par Marco (MATE) et Muffin (Cinnamon) -->
<metacity_theme>
<info>
  <name>Tunudan</name>
  <author>Tunudan &lt;contact@tunudan.fr&gt;</author>
  <copyright>2026 Tunudan, GPL-3.0-or-later</copyright>
  <date>2026</date>
  <description>Barre de titre noire, liseré orange, boutons ronds au survol</description>
</info>

<frame_geometry name="normal" rounded_top_left="false" rounded_top_right="false" rounded_bottom_left="false" rounded_bottom_right="false">
  <distance name="left_width" value="3"/>
  <distance name="right_width" value="3"/>
  <distance name="bottom_height" value="3"/>
  <distance name="left_titlebar_edge" value="6"/>
  <distance name="right_titlebar_edge" value="6"/>
  <aspect_ratio name="button" value="1.0"/>
  <distance name="title_vertical_pad" value="10"/>
  <border name="title_border" left="10" right="10" top="4" bottom="2"/>
  <border name="button_border" left="1" right="1" top="4" bottom="2"/>
</frame_geometry>

<frame_geometry name="maximized" parent="normal" rounded_top_left="false" rounded_top_right="false" rounded_bottom_left="false" rounded_bottom_right="false">
  <distance name="left_width" value="0"/>
  <distance name="right_width" value="0"/>
  <distance name="bottom_height" value="0"/>
  <distance name="left_titlebar_edge" value="4"/>
  <distance name="right_titlebar_edge" value="4"/>
</frame_geometry>

<frame_geometry name="border" has_title="false">
  <distance name="left_width" value="3"/>
  <distance name="right_width" value="3"/>
  <distance name="bottom_height" value="3"/>
  <distance name="left_titlebar_edge" value="0"/>
  <distance name="right_titlebar_edge" value="0"/>
  <distance name="button_width" value="0"/>
  <distance name="button_height" value="0"/>
  <distance name="title_vertical_pad" value="3"/>
  <border name="title_border" left="0" right="0" top="0" bottom="0"/>
  <border name="button_border" left="0" right="0" top="0" bottom="0"/>
</frame_geometry>

<draw_ops name="frame_focused">
  <rectangle color="{P["bg0"]}" filled="true" x="0" y="0" width="width" height="height"/>
  <rectangle color="{P["accent"]}" filled="true" x="0" y="0" width="width" height="2"/>
  <rectangle color="{P["bg3"]}" filled="false" x="0" y="0" width="width-1" height="height-1"/>
  <rectangle color="{P["accent"]}" filled="true" x="0" y="0" width="width" height="2"/>
</draw_ops>

<draw_ops name="frame_unfocused">
  <rectangle color="{P["bg1"]}" filled="true" x="0" y="0" width="width" height="height"/>
  <rectangle color="{P["bg3"]}" filled="false" x="0" y="0" width="width-1" height="height-1"/>
</draw_ops>

<draw_ops name="frame_focused_max">
  <rectangle color="{P["bg0"]}" filled="true" x="0" y="0" width="width" height="height"/>
  <rectangle color="{P["accent"]}" filled="true" x="0" y="0" width="width" height="2"/>
</draw_ops>

<draw_ops name="frame_unfocused_max">
  <rectangle color="{P["bg1"]}" filled="true" x="0" y="0" width="width" height="height"/>
</draw_ops>

<draw_ops name="title_focused">
  <title color="{P["fg"]}" x="(0 `max` ((width - title_width) / 2))" y="(0 `max` ((height - title_height) / 2))"/>
</draw_ops>

<draw_ops name="title_unfocused">
  <title color="{P["fg_muted"]}" x="(0 `max` ((width - title_width) / 2))" y="(0 `max` ((height - title_height) / 2))"/>
</draw_ops>

<draw_ops name="blank">
</draw_ops>

{draw_ops}

<frame_style name="normal" geometry="normal">
  <piece position="entire_background" draw_ops="frame_unfocused"/>
  <piece position="title" draw_ops="title_unfocused"/>
{buttons(False, False)}
</frame_style>

<frame_style name="focused" geometry="normal" parent="normal">
  <piece position="entire_background" draw_ops="frame_focused"/>
  <piece position="title" draw_ops="title_focused"/>
{buttons(True, False)}
</frame_style>

<frame_style name="normal_maximized" geometry="maximized">
  <piece position="entire_background" draw_ops="frame_unfocused_max"/>
  <piece position="title" draw_ops="title_unfocused"/>
{buttons(False, True)}
</frame_style>

<frame_style name="focused_maximized" geometry="maximized" parent="normal_maximized">
  <piece position="entire_background" draw_ops="frame_focused_max"/>
  <piece position="title" draw_ops="title_focused"/>
{buttons(True, True)}
</frame_style>

<frame_style name="border" geometry="border" parent="normal">
  <piece position="entire_background" draw_ops="frame_unfocused"/>
  <piece position="title" draw_ops="blank"/>
</frame_style>

<frame_style_set name="normal">
  <frame focus="yes" state="normal" resize="both" style="focused"/>
  <frame focus="no" state="normal" resize="both" style="normal"/>
  <frame focus="yes" state="maximized" style="focused_maximized"/>
  <frame focus="no" state="maximized" style="normal_maximized"/>
  <frame focus="yes" state="shaded" style="focused"/>
  <frame focus="no" state="shaded" style="normal"/>
  <frame focus="yes" state="maximized_and_shaded" style="focused_maximized"/>
  <frame focus="no" state="maximized_and_shaded" style="normal_maximized"/>
</frame_style_set>

<frame_style_set name="border">
  <frame focus="yes" state="normal" resize="both" style="border"/>
  <frame focus="no" state="normal" resize="both" style="border"/>
  <frame focus="yes" state="maximized" style="border"/>
  <frame focus="no" state="maximized" style="border"/>
  <frame focus="yes" state="shaded" style="border"/>
  <frame focus="no" state="shaded" style="border"/>
  <frame focus="yes" state="maximized_and_shaded" style="border"/>
  <frame focus="no" state="maximized_and_shaded" style="border"/>
</frame_style_set>

<window type="normal" style_set="normal"/>
<window type="dialog" style_set="normal"/>
<window type="modal_dialog" style_set="normal"/>
<window type="menu" style_set="normal"/>
<window type="utility" style_set="normal"/>
<window type="border" style_set="border"/>

<menu_icon function="close" state="normal" draw_ops="close_unfocused"/>
<menu_icon function="maximize" state="normal" draw_ops="maximize_unfocused"/>
<menu_icon function="unmaximize" state="normal" draw_ops="restore_unfocused"/>
<menu_icon function="minimize" state="normal" draw_ops="minimize_unfocused"/>

</metacity_theme>
""")


def window_managers(P, write, HEADER):
    xfwm4(P, write, HEADER)
    openbox(P, write, HEADER)
    metacity(P, write, HEADER)

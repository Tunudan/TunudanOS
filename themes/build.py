#!/usr/bin/env python3
"""Génère tous les fichiers de thème Tunudan à partir d'une seule palette.

    python3 themes/build.py

Écrit dans themes/shared/ et dans le dossier de chaque interface.
Dépendances (développement seulement) : cairosvg, libsass (pip).
Les fichiers générés sont versionnés : l'installateur n'a pas besoin de Python.
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ----------------------------------------------------------------- palette
P = {
    "bg0": "#0D0D0D",       # noir Tunudan (fond)
    "bg1": "#141416",       # vues, champs
    "bg2": "#1C1C1E",       # fenêtres, panneaux (anthracite)
    "bg3": "#2A2A2C",       # bordures, survol
    "bg4": "#3A3A3E",       # éléments actifs neutres
    "fg": "#F5F1EA",        # texte (blanc cassé)
    "fg_dim": "#BDB7AE",
    "fg_muted": "#8A857E",
    "accent": "#FF6B1A",    # orange Tunudan
    "accent_light": "#FF9A5C",
    "accent_dark": "#C2410C",
    "red": "#ED553B",
    "green": "#5CB85C",
    "yellow": "#F6B43C",
    "blue": "#4A90D9",
    "cyan": "#3FB8AF",
}
# Couleurs ANSI des terminaux (0-15)
ANSI = ["#1C1C1E", "#ED553B", "#5CB85C", "#F6B43C", "#4A90D9", "#C2410C", "#3FB8AF", "#BDB7AE",
        "#4A4A4E", "#FF7A5C", "#7ED37E", "#FFD166", "#7FB3FF", "#FF6B1A", "#6FE0D8", "#F5F1EA"]


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def hexa(h, a="ff"):
    return h.lstrip("#").lower() + a


def write(rel, text, mode=0o644):
    path = os.path.join(HERE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.lstrip("\n"))
    os.chmod(path, mode)
    return path


HEADER = "Thème Tunudan — généré par themes/build.py, ne pas modifier à la main"


# ----------------------------------------------------------------- GTK
def gtk():
    named = {
        "accent_bg_color": P["accent"], "accent_fg_color": P["bg0"], "accent_color": P["accent_light"],
        "destructive_bg_color": P["red"], "destructive_fg_color": P["bg0"], "destructive_color": P["red"],
        "success_bg_color": P["green"], "success_color": P["green"],
        "warning_bg_color": P["yellow"], "warning_color": P["yellow"],
        "error_bg_color": P["red"], "error_color": P["red"],
        "window_bg_color": P["bg2"], "window_fg_color": P["fg"],
        "view_bg_color": P["bg1"], "view_fg_color": P["fg"],
        "headerbar_bg_color": P["bg0"], "headerbar_fg_color": P["fg"],
        "headerbar_backdrop_color": P["bg1"], "headerbar_border_color": P["bg3"],
        "sidebar_bg_color": P["bg1"], "sidebar_fg_color": P["fg"], "sidebar_backdrop_color": P["bg1"],
        "secondary_sidebar_bg_color": P["bg1"], "secondary_sidebar_fg_color": P["fg"],
        "card_bg_color": "rgba(255, 255, 255, 0.04)", "card_fg_color": P["fg"],
        "dialog_bg_color": P["bg2"], "dialog_fg_color": P["fg"],
        "popover_bg_color": P["bg2"], "popover_fg_color": P["fg"],
        "thumbnail_bg_color": P["bg2"], "thumbnail_fg_color": P["fg"],
    }
    gtk3_extra = {
        "theme_selected_bg_color": P["accent"], "theme_selected_fg_color": P["bg0"],
        "theme_bg_color": P["bg2"], "theme_fg_color": P["fg"],
        "theme_base_color": P["bg1"], "theme_text_color": P["fg"],
        "borders": P["bg3"],
    }
    defines = "\n".join(f"@define-color {k} {v};" for k, v in {**named, **gtk3_extra}.items())
    panels = f"""
/* Panneaux des bureaux GTK (Xfce, MATE, Budgie) */
.xfce4-panel.background, .mate-panel-menu-bar, PanelToplevel, PanelWidget,
.budgie-panel, .budgie-panel .budgie-menubar {{
    background-color: alpha({P["bg0"]}, 0.94);
    color: {P["fg"]};
}}
.xfce4-panel button:checked, .budgie-panel button:checked,
.budgie-panel .launcher.running.focused, .budgie-panel #tasklist-button:checked {{
    background-color: alpha({P["accent"]}, 0.25);
    box-shadow: inset 0 -2px {P["accent"]};
}}
.budgie-panel .running {{ box-shadow: inset 0 -2px alpha({P["accent"]}, 0.6); }}
.raven, .budgie-popover, .budgie-menu, .budgie-notification-window {{
    background-color: {P["bg2"]};
    color: {P["fg"]};
}}
.budgie-menu button:hover, .budgie-menu row:selected {{
    background-color: {P["accent"]};
    color: {P["bg0"]};
}}
"""
    write("shared/gtk/tunudan-overrides.css", f"""
/* {HEADER} */
/* Couleurs Tunudan ajoutées après adw-gtk3-dark (style libadwaita pour GTK 3) */
{defines}
{panels}""")
    variables = "\n".join(f"  --{k.replace('_', '-')}: {v};" for k, v in named.items())
    write("shared/gtk/gtk-4.0.css", f"""
/* {HEADER} */
/* Applications GTK 4 / libadwaita : couleurs Tunudan.
   Variables CSS (libadwaita ≥ 1.6) + couleurs nommées (versions plus anciennes). */
:root {{
{variables}
}}

{defines}
""")


# ----------------------------------------------------------------- Qt
def qt():
    # Ordre qt5ct/qt6ct : WindowText, Button, Light, Midlight, Dark, Mid, Text, BrightText,
    # ButtonText, Base, Window, Shadow, Highlight, HighlightedText, Link, LinkVisited,
    # AlternateBase, NoRole, ToolTipBase, ToolTipText, PlaceholderText
    def row(fg, txt, hl_bg, hl_fg):
        cols = [fg, P["bg3"], P["bg4"], P["bg3"], P["bg0"], P["bg3"], txt, "#FFFFFF",
                fg, P["bg1"], P["bg2"], "#000000", hl_bg, hl_fg, P["accent_light"],
                P["accent_dark"], P["bg2"], P["bg0"], P["bg2"], P["fg"], P["fg_muted"]]
        return ", ".join("#ff" + c.lstrip("#").lower() for c in cols)
    write("shared/qt/Tunudan.conf", f"""
# {HEADER}
# Palette pour qt5ct / qt6ct (Hyprland, Sway, i3, niri…)
[ColorScheme]
active_colors={row(P["fg"], P["fg"], P["accent"], P["bg0"])}
disabled_colors={row(P["fg_muted"], P["fg_muted"], P["bg3"], P["fg_muted"])}
inactive_colors={row(P["fg"], P["fg"], P["accent_dark"], P["fg"])}
""")


# ----------------------------------------------------------------- terminaux
def terminals():
    k = "\n".join(f"color{i:<2} {c}" for i, c in enumerate(ANSI))
    write("shared/terminals/kitty.conf", f"""
# {HEADER}
foreground {P["fg"]}
background {P["bg0"]}
selection_foreground {P["bg0"]}
selection_background {P["accent"]}
cursor {P["accent"]}
url_color {P["accent_light"]}
active_border_color {P["accent"]}
inactive_border_color {P["bg3"]}
active_tab_background {P["accent"]}
active_tab_foreground {P["bg0"]}
inactive_tab_background {P["bg2"]}
inactive_tab_foreground {P["fg_dim"]}
{k}
""")
    names = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    normal = "\n".join(f'{n} = "{ANSI[i]}"' for i, n in enumerate(names))
    bright = "\n".join(f'{n} = "{ANSI[i + 8]}"' for i, n in enumerate(names))
    write("shared/terminals/alacritty.toml", f"""
# {HEADER}
[colors.primary]
foreground = "{P["fg"]}"
background = "{P["bg0"]}"

[colors.cursor]
text = "{P["bg0"]}"
cursor = "{P["accent"]}"

[colors.selection]
text = "{P["bg0"]}"
background = "{P["accent"]}"

[colors.normal]
{normal}

[colors.bright]
{bright}
""")
    regular = "\n".join(f"regular{i}={ANSI[i].lstrip('#')}" for i in range(8))
    brights = "\n".join(f"bright{i}={ANSI[i + 8].lstrip('#')}" for i in range(8))
    write("shared/terminals/foot.ini", f"""
# {HEADER}
[colors]
foreground={P["fg"].lstrip('#')}
background={P["bg0"].lstrip('#')}
selection-foreground={P["bg0"].lstrip('#')}
selection-background={P["accent"].lstrip('#')}
urls={P["accent_light"].lstrip('#')}
{regular}
{brights}
""")
    write("shared/terminals/tunudan.theme", f"""
[Scheme]
Name=Tunudan
ColorForeground={P["fg"]}
ColorBackground={P["bg0"]}
ColorCursor={P["accent"]}
ColorBold={P["accent_light"]}
ColorBoldUseDefault=FALSE
ColorSelection={P["accent"]}
ColorSelectionBackground={P["accent"]}
ColorPalette={";".join(ANSI)}
""")
    colors = "\n".join(f"Color{i}={c}" for i, c in enumerate(ANSI))
    section = f"""Foreground={P["fg"]}
Background={P["bg0"]}
Cursor={P["accent"]}
{colors}"""
    write("shared/terminals/tunudan.palette", f"""
[Palette]
Name=Tunudan

[Dark]
{section}

[Light]
{section}
""")
    # Chaîne de palette pour gnome-terminal / mate-terminal (dconf)
    write("shared/terminals/vte-palette.txt", ":".join(ANSI) + "\n")


# ----------------------------------------------------------------- lanceurs, barres, notifications
def launchers_bars_notifications():
    write("shared/rofi/tunudan.rasi", f"""
/* {HEADER} — rofi (i3, Sway, Hyprland) */
* {{
    bg: {P["bg0"]}F2;
    bg-alt: {P["bg2"]};
    fg: {P["fg"]};
    fg-dim: {P["fg_muted"]};
    accent: {P["accent"]};
    background-color: transparent;
    text-color: @fg;
    font: "Inter 12";
}}
window {{
    width: 640px;
    background-color: @bg;
    border: 2px;
    border-color: @accent;
    border-radius: 14px;
    padding: 16px;
}}
mainbox {{ spacing: 12px; children: [ inputbar, listview ]; }}
inputbar {{
    background-color: @bg-alt;
    border-radius: 10px;
    padding: 10px 14px;
    spacing: 10px;
    children: [ prompt, entry ];
}}
prompt {{ text-color: @accent; }}
entry {{ placeholder: "Rechercher…"; placeholder-color: @fg-dim; }}
listview {{ lines: 8; columns: 1; spacing: 4px; scrollbar: false; }}
element {{ padding: 8px 12px; border-radius: 8px; spacing: 10px; }}
element-icon {{ size: 24px; }}
element normal.normal, element alternate.normal {{ background-color: transparent; }}
element selected.normal {{ background-color: @accent; text-color: {P["bg0"]}; }}
element-text, element-icon {{ background-color: transparent; text-color: inherit; vertical-align: 0.5; }}
""")
    r, g, b = rgb(P["bg0"])
    write("shared/waybar/style.css", f"""
/* {HEADER} — Waybar (Sway, Hyprland, niri) */
* {{
    font-family: "Inter", "JetBrainsMono Nerd Font", sans-serif;
    font-size: 13px;
    border: none;
    border-radius: 0;
    min-height: 0;
}}
window#waybar {{
    background: rgba({r}, {g}, {b}, 0.88);
    color: {P["fg"]};
}}
#custom-tunudan {{
    color: {P["accent"]};
    font-size: 17px;
    padding: 0 14px;
}}
#workspaces button {{
    padding: 0 10px;
    margin: 4px 2px;
    color: {P["fg_muted"]};
    background: transparent;
    border-radius: 8px;
}}
#workspaces button:hover {{ background: {P["bg3"]}; color: {P["fg"]}; }}
#workspaces button.active, #workspaces button.focused {{
    color: {P["bg0"]};
    background: {P["accent"]};
}}
#workspaces button.urgent {{ color: {P["bg0"]}; background: {P["red"]}; }}
#window {{ color: {P["fg_dim"]}; padding: 0 10px; }}
#clock, #battery, #network, #pulseaudio, #wireplumber, #cpu, #memory, #tray, #backlight {{
    padding: 0 12px;
    margin: 4px 3px;
    background: {P["bg2"]};
    border-radius: 8px;
}}
#clock {{ color: {P["accent_light"]}; font-weight: bold; }}
#battery.warning {{ color: {P["yellow"]}; }}
#battery.critical {{ color: {P["red"]}; }}
#network.disconnected, #pulseaudio.muted {{ color: {P["fg_muted"]}; }}
tooltip {{
    background: {P["bg2"]};
    border: 1px solid {P["accent"]};
    border-radius: 8px;
}}
tooltip label {{ color: {P["fg"]}; }}
""")
    for wm in ("sway", "hyprland", "niri"):
        write(f"shared/waybar/config-{wm}.jsonc", f"""
// {HEADER} — Waybar pour {wm}
{{
    "layer": "top",
    "position": "top",
    "height": 38,
    "spacing": 2,
    "modules-left": ["custom/tunudan", "{wm}/workspaces", "{wm}/window"],
    "modules-center": ["clock"],
    "modules-right": ["pulseaudio", "network", "battery", "tray"],
    "custom/tunudan": {{
        "format": "◆",
        "tooltip-format": "Tunudan — Apprendre. Coder. Avancer.\\nClic : aide à distance",
        "on-click": "tunudan-help"
    }},
    "clock": {{
        "format": "{{:%H:%M}}",
        "format-alt": "{{:%A %d %B %Y}}",
        "tooltip-format": "<tt>{{calendar}}</tt>"
    }},
    "pulseaudio": {{
        "format": "♪ {{volume}} %",
        "format-muted": "♪ muet",
        "on-click": "pavucontrol"
    }},
    "network": {{
        "format-wifi": "wifi {{essid}}",
        "format-ethernet": "filaire",
        "format-disconnected": "hors ligne",
        "tooltip-format": "{{ifname}} {{ipaddr}}"
    }},
    "battery": {{
        "states": {{ "warning": 25, "critical": 10 }},
        "format": "⚡ {{capacity}} %"
    }},
    "tray": {{ "spacing": 8 }}
}}
""")
    write("shared/notifications/dunstrc", f"""
# {HEADER} — dunst (i3)
[global]
font = Inter 11
width = 360
offset = 16x16
origin = top-right
padding = 12
horizontal_padding = 14
frame_width = 2
frame_color = "{P["accent"]}"
separator_color = frame
corner_radius = 12
icon_corner_radius = 6
background = "{P["bg2"]}"
foreground = "{P["fg"]}"
highlight = "{P["accent"]}"

[urgency_low]
background = "{P["bg1"]}"
foreground = "{P["fg_dim"]}"
frame_color = "{P["bg3"]}"
timeout = 5

[urgency_normal]
background = "{P["bg2"]}"
foreground = "{P["fg"]}"
frame_color = "{P["accent"]}"
timeout = 8

[urgency_critical]
background = "{P["bg2"]}"
foreground = "{P["fg"]}"
frame_color = "{P["red"]}"
timeout = 0
""")
    write("shared/notifications/mako", f"""
# {HEADER} — mako (Sway, Hyprland)
font=Inter 11
background-color={P["bg2"]}F2
text-color={P["fg"]}
border-color={P["accent"]}
progress-color=over {P["accent_dark"]}
border-size=2
border-radius=12
padding=12
margin=16
width=360
default-timeout=7000

[urgency=low]
border-color={P["bg3"]}
text-color={P["fg_dim"]}

[urgency=critical]
border-color={P["red"]}
default-timeout=0
""")


# ----------------------------------------------------------------- i3 / Sway
def i3_sway():
    clients = f"""# class                 bordure  fond     texte    indicateur bordure_enfant
client.focused          {P["accent"]} {P["accent"]} {P["bg0"]} {P["accent_light"]}    {P["accent"]}
client.focused_inactive {P["bg3"]} {P["bg2"]} {P["fg"]} {P["bg3"]}    {P["bg3"]}
client.unfocused        {P["bg1"]} {P["bg1"]} {P["fg_muted"]} {P["bg1"]}    {P["bg1"]}
client.urgent           {P["red"]} {P["red"]} {P["bg0"]} {P["red"]}    {P["red"]}
client.placeholder      {P["bg0"]} {P["bg0"]} {P["fg"]} {P["bg0"]}    {P["bg0"]}
client.background       {P["bg0"]}"""
    barcolors = f"""    colors {{
        background {P["bg0"]}
        statusline {P["fg"]}
        separator  {P["bg3"]}
        #                  bordure  fond     texte
        focused_workspace  {P["accent"]} {P["accent"]} {P["bg0"]}
        active_workspace   {P["bg3"]} {P["bg3"]} {P["fg"]}
        inactive_workspace {P["bg0"]} {P["bg0"]} {P["fg_muted"]}
        urgent_workspace   {P["red"]} {P["red"]} {P["bg0"]}
        binding_mode       {P["accent_light"]} {P["accent_light"]} {P["bg0"]}
    }}"""
    write("i3-sway/i3/tunudan.conf", f"""
# {HEADER} — i3 (≥ 4.22)
# Inclus depuis ~/.config/i3/config par : include ~/.config/i3/tunudan.conf

font pango:Inter Bold 10
default_border pixel 2
default_floating_border pixel 2
gaps inner 8
gaps outer 4
smart_gaps on

{clients}

# Fond d'écran et notifications
exec_always --no-startup-id feh --no-fehbg --bg-fill "$HOME/.local/share/backgrounds/tunudan/origami/origami-grue-sombre.png"
exec --no-startup-id dunst

# Lanceur aux couleurs Tunudan : rofi -show drun -theme ~/.config/rofi/tunudan.rasi
""")
    write("i3-sway/i3/bar.conf", f"""
# {HEADER} — barre i3 aux couleurs Tunudan
# Remplace votre bloc « bar {{ … }} » par celui-ci (l'installateur le propose).
bar {{
    status_command i3status -c ~/.config/i3status/tunudan.conf
    position top
    font pango:Inter, JetBrains Mono 10
    tray_padding 4
{barcolors}
}}
""")
    write("i3-sway/i3/i3status.conf", f"""
# {HEADER} — i3status
general {{
    colors = true
    color_good = "{P["green"]}"
    color_degraded = "{P["yellow"]}"
    color_bad = "{P["red"]}"
    interval = 5
    separator = " · "
}}
order += "wireless _first_"
order += "ethernet _first_"
order += "battery all"
order += "volume master"
order += "tztime local"

wireless _first_ {{ format_up = "wifi %essid" format_down = "" }}
ethernet _first_ {{ format_up = "filaire" format_down = "" }}
battery all {{ format = "%status %percentage" format_down = "" }}
volume master {{ format = "son %volume" format_muted = "muet" }}
tztime local {{ format = "%a %d %b  %H:%M" }}
""")
    write("i3-sway/sway/tunudan.conf", f"""
# {HEADER} — Sway
# Inclus depuis ~/.config/sway/config par : include ~/.config/sway/tunudan.conf

font pango:Inter Bold 10
default_border pixel 2
default_floating_border pixel 2
gaps inner 8
gaps outer 4
smart_gaps on

{clients}

output * bg "$HOME/.local/share/backgrounds/tunudan/origami/origami-envolee-sombre.png" fill

# Thème GTK, icônes et curseur (Sway ne lit pas xsettings)
exec_always gsettings set org.gnome.desktop.interface gtk-theme Tunudan
exec_always gsettings set org.gnome.desktop.interface icon-theme Tunudan
exec_always gsettings set org.gnome.desktop.interface color-scheme prefer-dark
exec_always gsettings set org.gnome.desktop.interface font-name "Inter 11"

exec mako --config ~/.config/mako/tunudan
seat * xcursor_theme Tunudan-cursors 24
exec_always gsettings set org.gnome.desktop.interface cursor-theme Tunudan-cursors
""")
    write("i3-sway/sway/bar.conf", f"""
# {HEADER} — barre Sway (swaybar). Pour Waybar : voir README.
bar {{
    position top
    status_command while date +'%a %d %b  %H:%M'; do sleep 30; done
    font pango:Inter, JetBrains Mono 10
{barcolors}
}}
""")


# ----------------------------------------------------------------- Hyprland
def hyprland():
    a, al, i = hexa(P["accent"]), hexa(P["accent_light"]), hexa(P["bg3"])
    write("hyprland/tunudan.lua", f"""
-- {HEADER}
-- Hyprland 0.55 et plus (configuration Lua).
-- Chargé depuis ~/.config/hypr/hyprland.lua par : require("tunudan")

hl.config({{
  general = {{
    gaps_in = 6,
    gaps_out = 14,
    border_size = 2,
    col = {{
      active_border = {{ colors = {{ "rgba({a})", "rgba({al})" }}, angle = 45 }},
      inactive_border = "rgba({i})",
    }},
  }},
  decoration = {{
    rounding = 12,
    active_opacity = 1.0,
    inactive_opacity = 0.96,
    blur = {{ enabled = true, size = 6, passes = 2 }},
    shadow = {{ enabled = true, range = 20, render_power = 3, color = "rgba(00000099)" }},
  }},
  misc = {{
    disable_hyprland_logo = true,
    force_default_wallpaper = 0,
    background_color = "rgba({hexa(P["bg0"])})",
  }},
}})

hl.env("XCURSOR_SIZE", "24")
hl.env("XCURSOR_THEME", "Tunudan-cursors")
hl.env("QT_QPA_PLATFORMTHEME", "qt6ct")

hl.on("hyprland.start", function()
  hl.exec_cmd("hyprpaper")
  hl.exec_cmd("waybar -c ~/.config/waybar/tunudan-hyprland.jsonc -s ~/.config/waybar/tunudan.css")
  hl.exec_cmd("mako --config ~/.config/mako/tunudan")
end)
""")
    write("hyprland/tunudan.conf", f"""
# {HEADER}
# Hyprland 0.54 et avant (hyprlang).
# Chargé depuis ~/.config/hypr/hyprland.conf par : source = ~/.config/hypr/tunudan.conf

general {{
    gaps_in = 6
    gaps_out = 14
    border_size = 2
    col.active_border = rgba({a}) rgba({al}) 45deg
    col.inactive_border = rgba({i})
}}

decoration {{
    rounding = 12
    active_opacity = 1.0
    inactive_opacity = 0.96
    blur {{
        enabled = true
        size = 6
        passes = 2
    }}
    shadow {{
        enabled = true
        range = 20
        render_power = 3
        color = rgba(00000099)
    }}
}}

misc {{
    disable_hyprland_logo = true
    force_default_wallpaper = 0
    background_color = rgba({hexa(P["bg0"])})
}}

env = XCURSOR_SIZE,24
env = XCURSOR_THEME,Tunudan-cursors
env = QT_QPA_PLATFORMTHEME,qt6ct

exec-once = hyprpaper
exec-once = waybar -c ~/.config/waybar/tunudan-hyprland.jsonc -s ~/.config/waybar/tunudan.css
exec-once = mako --config ~/.config/mako/tunudan
""")
    write("hyprland/hyprpaper.conf", """
# Fond Tunudan — hyprpaper 0.8 et plus
wallpaper {
    monitor =
    path = ~/.local/share/backgrounds/tunudan/origami/origami-sommets-sombre.png
    fit_mode = cover
}
splash = false
""")
    write("hyprland/hyprpaper-legacy.conf", """
# Fond Tunudan — hyprpaper 0.7 et avant
preload = ~/.local/share/backgrounds/tunudan/origami/origami-sommets-sombre.png
wallpaper = ,~/.local/share/backgrounds/tunudan/origami/origami-sommets-sombre.png
splash = false
""")


# ----------------------------------------------------------------- COSMIC
def cosmic():
    def c(h, a="FF"):
        return f'"{h.upper()}{a}"'
    write("cosmic/tunudan-dark.ron", f"""
(
    palette: Dark((
        name: "tunudan-dark",
        bright_red: "#FFA09AFF",
        bright_green: "#5EDB8CFF",
        bright_orange: "#FF9A5CFF",
        gray_1: {c(P["bg1"])},
        gray_2: {c(P["bg2"])},
        neutral_0: "#000000FF",
        neutral_1: {c(P["bg0"])},
        neutral_2: {c(P["bg1"])},
        neutral_3: {c(P["bg2"])},
        neutral_4: {c(P["bg3"])},
        neutral_5: {c(P["bg4"])},
        neutral_6: "#5A5753FF",
        neutral_7: {c(P["fg_muted"])},
        neutral_8: {c(P["fg_dim"])},
        neutral_9: "#DCD7CFFF",
        neutral_10: {c(P["fg"])},
        accent_blue: "#63D0DFFF",
        accent_indigo: "#A1C0EBFF",
        accent_purple: "#E79CFEFF",
        accent_pink: "#FF9CB1FF",
        accent_red: "#FDA1A0FF",
        accent_orange: {c(P["accent"])},
        accent_yellow: "#F7E062FF",
        accent_green: "#92CF9CFF",
        accent_warm_grey: "#CABAB4FF",
        ext_warm_grey: "#9B8E8AFF",
        ext_orange: {c(P["accent"])},
        ext_yellow: "#FEDB40FF",
        ext_blue: "#48B9C7FF",
        ext_purple: "#CF7DFFFF",
        ext_pink: "#F93A83FF",
        ext_indigo: "#3E88FFFF",
    )),
    spacing: (
        space_none: 0,
        space_xxxs: 4,
        space_xxs: 8,
        space_xs: 12,
        space_s: 16,
        space_m: 24,
        space_l: 32,
        space_xl: 48,
        space_xxl: 64,
        space_xxxl: 128,
    ),
    corner_radii: (
        radius_0: (0.0, 0.0, 0.0, 0.0),
        radius_xs: (4.0, 4.0, 4.0, 4.0),
        radius_s: (10.0, 10.0, 10.0, 10.0),
        radius_m: (14.0, 14.0, 14.0, 14.0),
        radius_l: (14.0, 14.0, 14.0, 14.0),
        radius_xl: (18.0, 18.0, 18.0, 18.0),
    ),
    neutral_tint: None,
    bg_color: Some({c(P["bg0"])}),
    primary_container_bg: Some({c(P["bg2"])}),
    secondary_container_bg: None,
    text_tint: None,
    accent: Some({c(P["accent"])}),
    success: Some({c(P["green"])}),
    warning: Some({c(P["yellow"])}),
    destructive: Some({c(P["red"])}),
    frosted: Medium,
    gaps: (0, 8),
    active_hint: 3,
    window_hint: Some({c(P["accent"])}),
    frosted_windows: false,
    frosted_system_interface: true,
    frosted_panel: true,
    frosted_applets: true,
    alpha_map: (
        extremely_low: 0.9,
        extremely_low_2: 0.87692,
        very_low: 0.85385,
        very_low_2: 0.83076,
        low: 0.80769,
        low_2: 0.78461,
        medium: 0.76154,
        medium_2: 0.73846,
        high: 0.71538,
        high_2: 0.69231,
        very_high: 0.66023,
        very_high_2: 0.64615,
        extremely_high: 0.62308,
        extremely_high_2: 0.6,
    ),
)
""")


if __name__ == "__main__":
    from build_wm import window_managers  # noqa: E402  (deuxième moitié du générateur)
    from build_desktops import desktops  # noqa: E402
    gtk()
    qt()
    terminals()
    launchers_bars_notifications()
    i3_sway()
    hyprland()
    cosmic()
    window_managers(P, write, HEADER)
    desktops(P, write, HEADER, HERE, ROOT)
    print("Thèmes générés dans", HERE)

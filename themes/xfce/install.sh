#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"

say "Thème Tunudan pour Xfce"
install_base
has xfconf-query || { warn "xfconf-query introuvable : lancez ce script dans une session Xfce"; exit 1; }
X() { xfconf-query -c "$1" -p "$2" -n -t "$3" -s "$4"; }

X xsettings /Net/ThemeName string Tunudan
X xsettings /Net/IconThemeName string Tunudan
X xsettings /Gtk/CursorThemeName string "$CURSOR"
X xsettings /Gtk/CursorThemeSize int 24
X xsettings /Gtk/FontName string "Inter 11"
X xsettings /Gtk/MonospaceFontName string "JetBrains Mono 11"
X xfwm4 /general/theme string Tunudan
X xfwm4 /general/title_font string "Inter Bold 10"
X xfwm4 /general/button_layout string "O|HMC"
X xfce4-panel /panels/dark-mode bool true 2>/dev/null || true
ok "Thème GTK, icônes, polices et décorations xfwm4"

# Fond d'écran sur tous les écrans et espaces de travail
# Xfce 4.20 lit /backdrop/screen0/monitor<sortie>/workspace<n>/last-image ; les anciennes
# clés monitor0/last-image (sans workspace, venues de desktop-base) sont ignorées.
props=$(xfconf-query -c xfce4-desktop -l 2>/dev/null | grep -E '/workspace[0-9]+/last-image$' || true)
for m in $(xrandr --listmonitors 2>/dev/null | awk 'NR>1 {print $NF}'); do
    for w in 0 1 2 3; do
        props="$props /backdrop/screen0/monitor$m/workspace$w/last-image"
    done
done
props=$(printf '%s\n' $props | sort -u)
for p in $props; do
    X xfce4-desktop "$p" string "$WALLPAPER"
    X xfce4-desktop "$(dirname "$p")/image-style" int 5
done
ok "Fond d'écran"

# Terminal Xfce (version 1.1 et plus : réglages dans xfconf)
if has xfce4-terminal; then
    X xfce4-terminal /color-foreground string "#F5F1EA"
    X xfce4-terminal /color-background string "#0D0D0D"
    X xfce4-terminal /color-cursor string "#FF6B1A"
    X xfce4-terminal /color-palette string "$(tr ':' ';' < "$SHARED/terminals/vte-palette.txt" | tr -d '\n')"
    X xfce4-terminal /font-name string "JetBrains Mono 11" 2>/dev/null || true
    ok "Terminal Xfce"
fi
say "Terminé."

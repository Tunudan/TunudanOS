#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"
# Usage : install.sh [i3|sway] [--bar]
#   --bar : remplace votre bloc « bar { … } » par la barre Tunudan

WM=""
for a in "$@"; do case "$a" in i3|sway) WM=$a ;; esac; done
if [ -z "$WM" ]; then
    if [ -n "${SWAYSOCK:-}" ]; then WM=sway; elif [ -n "${I3SOCK:-}" ] || pgrep -x i3 >/dev/null 2>&1; then WM=i3
    elif has sway; then WM=sway; else WM=i3; fi
fi
say "Thème Tunudan pour $WM"
install_base
install_qt
gtk_settings_ini
S="$THEMES_DIR/i3-sway/$WM"
cfg="$CONF/$WM/config"
[ -f "$cfg" ] || { [ "$WM" = i3 ] && [ -f "$HOME/.i3/config" ] && cfg="$HOME/.i3/config"; }
mkdir -p "$CONF/$WM" "$CONF/rofi"
# Pas encore de configuration personnelle : on part de celle du système
if [ ! -f "$cfg" ] && [ -f "/etc/$WM/config" ]; then
    cp "/etc/$WM/config" "$CONF/$WM/config"
    cfg="$CONF/$WM/config"
    ok "Configuration de départ copiée depuis /etc/$WM/config"
fi
cp "$S/tunudan.conf" "$CONF/$WM/tunudan.conf"
cp "$S/bar.conf" "$CONF/$WM/tunudan-bar.conf"
sed -i "s#\$HOME/.local/share/backgrounds/tunudan#$WALL_DIR#g" "$CONF/$WM/tunudan.conf"
cp "$SHARED/rofi/tunudan.rasi" "$CONF/rofi/tunudan.rasi"
if [ "$WM" = i3 ]; then
    mkdir -p "$CONF/i3status" "$CONF/dunst"
    cp "$S/i3status.conf" "$CONF/i3status/tunudan.conf"
    backup "$CONF/dunst/dunstrc"
    cp "$SHARED/notifications/dunstrc" "$CONF/dunst/dunstrc"
    has feh || pkg_install feh || warn "feh absent : le fond d'écran ne s'affichera pas (paquet feh)"
else
    mkdir -p "$CONF/mako" "$CONF/waybar"
    cp "$SHARED/notifications/mako" "$CONF/mako/tunudan"
    cp "$SHARED/waybar/style.css" "$CONF/waybar/tunudan.css"
    cp "$SHARED/waybar/config-sway.jsonc" "$CONF/waybar/tunudan-sway.jsonc"
fi

if [ ! -f "$cfg" ]; then
    warn "Pas de configuration $WM trouvée : ajoutez « include $CONF/$WM/tunudan.conf » à la vôtre."
else
    grep -q 'tunudan.conf' "$cfg" || add_line "$cfg" "include $CONF/$WM/tunudan.conf"
    ok "Couleurs, bordures et espacements inclus dans $cfg"
    if grep -qE '^[[:space:]]*bar[[:space:]]*\{' "$cfg"; then
        case " $* " in
            *" --bar "*)
                backup "$cfg"
                awk 'BEGIN{d=0} /^[[:space:]]*bar[[:space:]]*\{/ {d=1} { if (d) print "#tunudan# " $0; else print } d && /^[[:space:]]*\}/ {d=0}' "$cfg" > "$cfg.tmp" && mv "$cfg.tmp" "$cfg"
                grep -q 'tunudan-bar.conf' "$cfg" || add_line "$cfg" "include $CONF/$WM/tunudan-bar.conf"
                ok "Barre Tunudan (votre ancienne barre est commentée)" ;;
            *) warn "Votre barre actuelle est conservée. Relancez avec --bar pour la barre Tunudan." ;;
        esac
    else
        grep -q 'tunudan-bar.conf' "$cfg" || add_line "$cfg" "include $CONF/$WM/tunudan-bar.conf"
        ok "Barre Tunudan"
    fi
fi
if [ "$WM" = sway ]; then swaymsg reload >/dev/null 2>&1 || true; else i3-msg reload >/dev/null 2>&1 || true; fi
say "Terminé. Lanceur : \$mod+d (rofi). Pour Waybar sous Sway : voir README."

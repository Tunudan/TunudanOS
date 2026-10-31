#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"

say "Thème Tunudan pour Hyprland"
install_base
install_qt
gtk_settings_ini
H="$THEMES_DIR/hyprland"
mkdir -p "$CONF/hypr" "$CONF/waybar" "$CONF/mako" "$CONF/rofi"

# Configuration Lua (Hyprland 0.55+) ou hyprlang (0.54 et avant)
if [ -f "$CONF/hypr/hyprland.lua" ]; then
    cp "$H/tunudan.lua" "$CONF/hypr/tunudan.lua"
    grep -q 'require("tunudan")' "$CONF/hypr/hyprland.lua" || add_line "$CONF/hypr/hyprland.lua" 'require("tunudan")'
    ok "hyprland.lua : require(\"tunudan\")"
elif [ -f "$CONF/hypr/hyprland.conf" ]; then
    cp "$H/tunudan.conf" "$CONF/hypr/tunudan.conf"
    grep -q 'tunudan.conf' "$CONF/hypr/hyprland.conf" || add_line "$CONF/hypr/hyprland.conf" "source = $CONF/hypr/tunudan.conf"
    ok "hyprland.conf : source = tunudan.conf"
else
    cp "$H/tunudan.lua" "$H/tunudan.conf" "$CONF/hypr/"
    warn "Aucune configuration Hyprland trouvée. Ajoutez require(\"tunudan\") à hyprland.lua (0.55+)"
    warn "ou « source = $CONF/hypr/tunudan.conf » à hyprland.conf (0.54 et avant)."
fi

# Fond d'écran : syntaxe hyprpaper 0.8+ ou ancienne
v=$(hyprpaper --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+' | head -n1 || true)
major=${v%%.*}; minor=${v#*.}
f="$CONF/hypr/hyprpaper.conf"
backup "$f"
if [ -n "$v" ] && [ "$major" = 0 ] && [ "$minor" -lt 8 ]; then
    cp "$H/hyprpaper-legacy.conf" "$f"
else
    cp "$H/hyprpaper.conf" "$f"
fi
sed -i "s#~/.local/share/backgrounds/tunudan#$WALL_DIR#g" "$f"
ok "hyprpaper (${v:-version inconnue})"

cp "$SHARED/waybar/style.css" "$CONF/waybar/tunudan.css"
cp "$SHARED/waybar/config-hyprland.jsonc" "$CONF/waybar/tunudan-hyprland.jsonc"
cp "$SHARED/notifications/mako" "$CONF/mako/tunudan"
cp "$SHARED/rofi/tunudan.rasi" "$CONF/rofi/tunudan.rasi"
ok "Waybar, mako, rofi (rofi -show drun -theme ~/.config/rofi/tunudan.rasi)"

if has hyprctl && [ -n "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]; then
    hyprctl reload >/dev/null && ok "Hyprland rechargé"
    hyprctl setcursor "$CURSOR" 24 >/dev/null 2>&1 || true
    pgrep -x waybar >/dev/null || (waybar -c "$CONF/waybar/tunudan-hyprland.jsonc" -s "$CONF/waybar/tunudan.css" >/dev/null 2>&1 &)
    pgrep -x hyprpaper >/dev/null || (hyprpaper >/dev/null 2>&1 &)
fi
say "Terminé."

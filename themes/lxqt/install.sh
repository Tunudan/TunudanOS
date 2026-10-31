#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"

say "Thème Tunudan pour LXQt"
install_base
install_qt

if [ "$TUNUDAN_SYSTEM" != 1 ]; then
    mkdir -p "$DATA/lxqt/themes" "$DATA/lxqt/palettes"
    rm -rf "$DATA/lxqt/themes/Tunudan"
    cp -r "$THEMES_DIR/lxqt/theme/Tunudan" "$DATA/lxqt/themes/"
    cp "$THEMES_DIR/lxqt/palettes/Tunudan" "$DATA/lxqt/palettes/"
fi
ok "Thème du panneau, du lanceur et des notifications"

L="$CONF/lxqt/lxqt.conf"
ini_set "$L" General theme Tunudan
ini_set "$L" General icon_theme Tunudan
ini_set "$L" Qt style Fusion
ini_set "$L" Qt font "\"Inter,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1\""
while IFS='=' read -r k v; do
    case "$k" in ''|\[*) continue ;; esac
    ini_set "$L" Palette "$k" "$v"
done < "$THEMES_DIR/lxqt/palettes/Tunudan"
ini_set "$CONF/lxqt/session.conf" Mouse cursor_theme "$CURSOR"
ok "Palette Qt, police et curseur"

# Décorations : Openbox (X11) ou labwc (LXQt 2 sous Wayland)
[ -f "$CONF/openbox/lxqt-rc.xml" ] && set_ob_theme "$CONF/openbox/lxqt-rc.xml" && ok "Openbox"
if has labwc || [ -f "$CONF/labwc/rc.xml" ]; then set_ob_theme "$CONF/labwc/rc.xml"; ok "labwc"; fi
has openbox && openbox --reconfigure 2>/dev/null || true
has labwc && labwc --reconfigure 2>/dev/null || true

gtk_settings_ini
if has pcmanfm-qt; then
    pcmanfm-qt --set-wallpaper "$WALLPAPER" --wallpaper-mode=zoom >/dev/null 2>&1 || true
    ok "Fond d'écran"
fi
say "Terminé. Déconnectez-vous puis reconnectez-vous pour recharger le panneau."

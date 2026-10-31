#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"

say "Thème Tunudan pour Budgie"
install_base

I=org.gnome.desktop.interface
gset $I color-scheme prefer-dark || true
gset $I gtk-theme Tunudan || true
gset $I icon-theme Tunudan || true
gset $I font-name "Inter 11" || true
gset $I monospace-font-name "JetBrains Mono 11" || true
gset org.gnome.desktop.wm.preferences titlebar-font "Inter Bold 10" || true
gset org.gnome.desktop.background picture-uri "file://$WALLPAPER_LIGHT" || true
gset org.gnome.desktop.background picture-uri-dark "file://$WALLPAPER" || true
gset com.solus-project.budgie-panel dark-theme true || true
gset com.solus-project.budgie-panel builtin-theme false || true
ok "Panneau Budgie : couleurs portées par le thème GTK Tunudan"

# Budgie 10.10 et plus (Wayland) : le compositeur labwc lit le thème Openbox
if [ -d "$CONF/budgie-desktop/labwc" ]; then RC="$CONF/budgie-desktop/labwc/rc.xml"; else RC="$CONF/labwc/rc.xml"; fi
if has labwc || [ -f "$RC" ]; then
    set_ob_theme "$RC"
    ok "Décorations labwc (Wayland) : $RC"
fi
has labwc && labwc --reconfigure 2>/dev/null || true
say "Terminé. Déconnectez-vous puis reconnectez-vous pour tout appliquer."

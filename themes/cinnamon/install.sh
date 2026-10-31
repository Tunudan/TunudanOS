#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"

say "Thème Tunudan pour Cinnamon"
install_base

D=org.cinnamon.desktop.interface
gset $D gtk-theme Tunudan || true
gset $D icon-theme Tunudan || true
gset $D font-name "Inter 10" || true
gset $D cursor-theme "$CURSOR" || true
gset org.cinnamon.desktop.wm.preferences theme Tunudan || true
gset org.cinnamon.desktop.wm.preferences titlebar-font "Inter Bold 10" || true
gset org.cinnamon.theme name Tunudan || true
gset org.cinnamon.desktop.background picture-uri "file://$WALLPAPER" || true
gset org.cinnamon.desktop.background picture-options zoom || true
gset org.x.apps.portal color-scheme prefer-dark || true
gset org.gnome.desktop.interface color-scheme prefer-dark || true
gset org.gnome.desktop.interface gtk-theme Tunudan || true
gset org.gnome.desktop.interface monospace-font-name "JetBrains Mono 11" || true
ok "Bureau (panneau, menu, notifications), fenêtres, applications et fond"
say "Terminé. Si le panneau ne change pas tout de suite : Alt+F2, tapez r, Entrée."

#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"

say "Thème Tunudan pour GNOME"
install_base

I=org.gnome.desktop.interface
gset $I color-scheme prefer-dark || true
# GNOME 47 et plus : couleur d'accent système (shell, réglages, applications libadwaita)
if gset $I accent-color orange; then ok "Couleur d'accent orange"; else warn "Couleur d'accent : GNOME 47 ou plus requis"; fi
gset $I gtk-theme Tunudan || true
gset $I icon-theme Tunudan || true
gset $I font-name "Inter 11" || true
gset $I document-font-name "Inter 11" || true
gset $I monospace-font-name "JetBrains Mono 11" || true
gset org.gnome.desktop.wm.preferences titlebar-font "Inter Bold 11" || true
gset org.gnome.desktop.background picture-uri "file://$WALLPAPER_LIGHT" || true
gset org.gnome.desktop.background picture-uri-dark "file://$WALLPAPER" || true
gset org.gnome.desktop.background primary-color "#0D0D0D" || true
gset org.gnome.desktop.screensaver picture-uri "file://$WALLPAPER" || true
ok "Réglages GNOME appliqués"
say "Terminé. Les applications déjà ouvertes prendront le thème à leur prochain lancement."

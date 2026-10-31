#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"

say "Thème Tunudan pour MATE"
install_base

M=org.mate.interface
gset $M gtk-theme Tunudan || true
gset $M icon-theme Tunudan || true
gset $M font-name "Inter 10" || true
gset $M document-font-name "Inter 10" || true
gset $M monospace-font-name "JetBrains Mono 11" || true
gset org.mate.Marco.general theme Tunudan || true
gset org.mate.Marco.general titlebar-font "Inter Bold 10" || true
gset org.mate.background picture-filename "$WALLPAPER" || true
gset org.mate.background picture-options zoom || true
gset org.mate.peripherals-mouse cursor-theme "$CURSOR" || true
gset org.gnome.desktop.interface color-scheme prefer-dark || true
ok "Thème GTK, icônes, polices, décorations Marco et fond"
say "Terminé."

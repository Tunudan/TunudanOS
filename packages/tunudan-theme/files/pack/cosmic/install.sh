#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"

say "Thème Tunudan pour COSMIC"
install_wallpapers
install_fonts
install_icons
install_cursors
install_terminals

mkdir -p "$DATA/tunudan/cosmic"
cp "$THEMES_DIR/cosmic/tunudan-dark.ron" "$DATA/tunudan/cosmic/"
# Mode sombre et icônes Tunudan
C="$CONF/cosmic"
mkdir -p "$C/com.system76.CosmicTheme.Mode/v1" "$C/com.system76.CosmicTk/v1"
echo "true" > "$C/com.system76.CosmicTheme.Mode/v1/is_dark"
echo '"Tunudan"' > "$C/com.system76.CosmicTk/v1/icon_theme"
ok "Mode sombre et icônes"
install_qt

say "Dernière étape, à faire une fois dans COSMIC :"
echo "   Paramètres > Bureau > Apparence > Importer"
echo "   puis choisir $DATA/tunudan/cosmic/tunudan-dark.ron"
echo "   Fond d'écran : Paramètres > Bureau > Fond d'écran > $WALLPAPER"
has cosmic-settings && (cosmic-settings appearance >/dev/null 2>&1 &) || true

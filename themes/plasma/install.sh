#!/bin/sh
set -eu
THEMES_DIR=$(cd "$(dirname "$0")/.." && pwd)
# shellcheck source=../lib/common.sh
. "$THEMES_DIR/lib/common.sh"
# Option : --lnf applique aussi le thème global (réorganise le panneau en bas)

say "Thème Tunudan pour KDE Plasma"
install_wallpapers
install_fonts
install_theme_dir
install_gtk4
install_icons
install_cursors
install_terminals

F="$THEMES_DIR/plasma/files"
if [ "$TUNUDAN_SYSTEM" = 1 ]; then
    KWALL=/usr/share/wallpapers/Tunudan-Grue
else
    mkdir -p "$DATA/color-schemes" "$DATA/konsole" "$DATA/plasma/look-and-feel" "$DATA/wallpapers"
    cp "$F/TunudanDark.colors" "$DATA/color-schemes/"
    cp "$F/Tunudan.profile" "$F/Tunudan.colorscheme" "$DATA/konsole/"
    rm -rf "$DATA/plasma/look-and-feel/fr.tunudan.desktop" "$DATA/wallpapers/Tunudan"
    cp -r "$F/fr.tunudan.desktop" "$DATA/plasma/look-and-feel/"
    cp -r "$F/wallpaper-Tunudan" "$DATA/wallpapers/Tunudan"
    KWALL="$DATA/wallpapers/Tunudan-Grue"
fi
ok "Schéma de couleurs, profil Konsole, thème global et fond installés"

KW=kwriteconfig6; has $KW || KW=kwriteconfig5
if has plasma-apply-colorscheme; then
    plasma-apply-colorscheme TunudanDark >/dev/null && ok "Couleurs TunudanDark appliquées"
fi
if has $KW; then
    $KW --file kdeglobals --group General --key AccentColor "255,107,26"
    $KW --file kdeglobals --group Icons --key Theme Tunudan
    $KW --file kdeglobals --group General --key font "Inter,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    $KW --file kdeglobals --group General --key fixed "JetBrains Mono,10,-1,5,400,0,0,0,0,0,0,0,0,0,0,1"
    $KW --file konsolerc --group "Desktop Entry" --key DefaultProfile Tunudan.profile
    $KW --file kcminputrc --group Mouse --key cursorTheme "$CURSOR"
    $KW --file kcminputrc --group Mouse --key cursorSize 24
    $KW --file kwinrc --group Plugins --key blurEnabled true
    ok "Accent orange, icônes, polices, Konsole"
fi
if has plasma-apply-wallpaperimage; then
    plasma-apply-wallpaperimage "$KWALL" >/dev/null 2>&1 \
        || plasma-apply-wallpaperimage "$WALLPAPER" >/dev/null 2>&1 || true
    ok "Fond d'écran"
fi
# Applications GTK dans Plasma
ini_set "$CONF/gtk-3.0/settings.ini" Settings gtk-theme-name Tunudan
ini_set "$CONF/gtk-3.0/settings.ini" Settings gtk-icon-theme-name Tunudan
ini_set "$CONF/gtk-3.0/settings.ini" Settings gtk-cursor-theme-name "$CURSOR"
has plasma-apply-cursortheme && plasma-apply-cursortheme "$CURSOR" >/dev/null 2>&1 || true
gset org.gnome.desktop.interface gtk-theme Tunudan || true
gset org.gnome.desktop.interface color-scheme prefer-dark || true

case " $* " in
    *" --lnf "*)
        if has plasma-apply-lookandfeel; then
            plasma-apply-lookandfeel -a fr.tunudan.desktop --resetLayout && ok "Thème global Tunudan (panneau réorganisé)"
        fi ;;
    *) say "Astuce : « ./install.sh plasma --lnf » applique aussi la disposition Tunudan (panneau en bas)." ;;
esac
has qdbus6 && qdbus6 org.kde.KWin /KWin reconfigure >/dev/null 2>&1 || true
say "Terminé."

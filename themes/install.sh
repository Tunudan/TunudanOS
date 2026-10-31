#!/bin/sh
# Thèmes Tunudan (orange, noir, origami) pour 10 interfaces Linux.
#
#   ./install.sh                 détecte votre bureau et installe le thème
#   ./install.sh xfce            installe pour une interface précise
#   ./install.sh --list          liste les interfaces prises en charge
#   ./install.sh --deps xfce     installe aussi les paquets manquants (icônes, polices)
#   ./install.sh --uninstall     retire les fichiers Tunudan de votre dossier personnel
#
# Interfaces : gnome plasma xfce cinnamon mate lxqt budgie cosmic hyprland i3 sway
set -eu
THEMES_DIR=$(cd "$(dirname "$0")" && pwd)
export THEMES_DIR
# shellcheck source=lib/common.sh
. "$THEMES_DIR/lib/common.sh"

LIST="gnome plasma xfce cinnamon mate lxqt budgie cosmic hyprland i3 sway"

detect() {
    d=$(printf '%s:%s' "${XDG_CURRENT_DESKTOP:-}" "${DESKTOP_SESSION:-}" | tr '[:upper:]' '[:lower:]')
    case "$d" in
        *budgie*) echo budgie ;;
        *cosmic*) echo cosmic ;;
        *cinnamon*) echo cinnamon ;;
        *kde*|*plasma*) echo plasma ;;
        *xfce*) echo xfce ;;
        *mate*) echo mate ;;
        *lxqt*) echo lxqt ;;
        *hyprland*) echo hyprland ;;
        *sway*) echo sway ;;
        *i3*) echo i3 ;;
        *gnome*|*ubuntu*|*pop*) echo gnome ;;
        *)
            if [ -n "${HYPRLAND_INSTANCE_SIGNATURE:-}" ]; then echo hyprland
            elif [ -n "${SWAYSOCK:-}" ]; then echo sway
            elif [ -n "${I3SOCK:-}" ]; then echo i3
            fi ;;
    esac
}

uninstall() {
    say "Retrait des thèmes Tunudan de votre dossier personnel"
    if [ "$TUNUDAN_SYSTEM" = 1 ]; then
        warn "Thème installé dans le système (Tunudan OS) : seuls vos réglages GTK 4 sont retirés."
        sed -i '/tunudan.css/d' "$CONF/gtk-4.0/gtk.css" 2>/dev/null || true
        ok "Choisissez un autre thème dans les réglages de votre bureau."
        return 0
    fi
    rm -rf "$THEME_DIR" "$ICON_DIR" "$CURSOR_DIR" "$WALL_DIR" "$DATA/lxqt/themes/Tunudan" \
           "$DATA/plasma/look-and-feel/fr.tunudan.desktop" "$DATA/wallpapers/Tunudan" \
           "$DATA"/wallpapers/Tunudan-* "$DATA/gnome-background-properties/tunudan-origami.xml"
    [ -L "$HOME/.themes/Tunudan" ] && rm -f "$HOME/.themes/Tunudan"
    [ -L "$HOME/.icons/Tunudan-cursors" ] && rm -f "$HOME/.icons/Tunudan-cursors"
    grep -qs Tunudan "$HOME/.icons/default/index.theme" && rm -f "$HOME/.icons/default/index.theme"
    f="$CONF/gtk-4.0/gtk.css"
    [ -f "$f" ] && sed -i '/tunudan.css/d' "$f"
    rm -f "$CONF/gtk-4.0/tunudan.css"
    ok "Fichiers retirés. Choisissez un autre thème dans les réglages de votre bureau."
    say "Les copies de sécurité de vos fichiers portent l'extension .tunudan-AAAAMMJJ-HHMMSS"
}

WHICH=""
EXTRA=""
for a in "$@"; do
    case "$a" in
        --list)
            echo "Interfaces prises en charge : $LIST"
            exit 0 ;;
        --deps) TUNUDAN_DEPS=1; export TUNUDAN_DEPS ;;
        --uninstall) uninstall; exit 0 ;;
        -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
        --*) EXTRA="$EXTRA $a" ;;
        *) WHICH=$(echo "$a" | tr '[:upper:]' '[:lower:]') ;;
    esac
done

[ -n "$WHICH" ] || WHICH=$(detect)
if [ -z "$WHICH" ]; then
    warn "Bureau non détecté. Précisez-le : ./install.sh <interface>"
    echo "Interfaces : $LIST"
    exit 2
fi
case " $LIST " in *" $WHICH "*) ;; *) warn "Interface inconnue : $WHICH"; echo "Interfaces : $LIST"; exit 2 ;; esac

printf '%s\n' "$O
   Tunudan — Apprendre. Coder. Avancer.$R
"
case "$WHICH" in
    i3|sway) # shellcheck disable=SC2086
             exec sh "$THEMES_DIR/i3-sway/install.sh" "$WHICH" $EXTRA ;;
    *)       # shellcheck disable=SC2086
             exec sh "$THEMES_DIR/$WHICH/install.sh" $EXTRA ;;
esac

#!/bin/sh
# Installation SYSTÈME du thème Tunudan complet (Mint, Debian, Arch).
#
#   sudo ./install-system.sh                      tout installer et activer
#   ./install-system.sh --files-only --destdir D  copier les fichiers dans D (paquets)
#   sudo ./install-system.sh --activate-only      activer (schémas, curseur, écrans de connexion)
#   options : --distro debian|mint|arch (détection automatique sinon)
#
# Contenu : thème GTK 3 + décorations (xfwm4, Metacity, Openbox/labwc, Cinnamon), couleurs
# libadwaita, ~290 icônes, curseurs, fonds origami, écrans de connexion (SDDM, LightDM,
# slick-greeter, GDM), réglages par défaut de GNOME/Cinnamon/MATE/Budgie/Xfce/Plasma/LXQt,
# configurations complètes i3/Sway/Hyprland pour les nouveaux comptes, et application
# automatique au premier login de chaque utilisateur (tunudan-theme apply).
set -eu
SRC=$(cd "$(dirname "$0")" && pwd)
D=""
DISTRO=""
DO_FILES=1
DO_ACTIVATE=1
while [ $# -gt 0 ]; do
    case "$1" in
        --destdir) D=$2; shift ;;
        --distro) DISTRO=$2; shift ;;
        --files-only) DO_ACTIVATE=0 ;;
        --activate-only) DO_FILES=0 ;;
        -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
        *) echo "Option inconnue : $1" >&2; exit 2 ;;
    esac
    shift
done
if [ -z "$DISTRO" ]; then
    if [ -f "$D/etc/linuxmint/info" ] || [ -f /etc/linuxmint/info ]; then DISTRO=mint
    elif [ -f /etc/arch-release ]; then DISTRO=arch
    else DISTRO=debian; fi
fi
SH="$SRC/shared"
U="$D/usr/share"
BG=/usr/share/backgrounds/tunudan
say() { printf '\033[1;38;5;208m◆\033[0m %s\n' "$*"; }

cp_dir() { rm -rf "$2"; mkdir -p "$(dirname "$2")"; cp -r "$1" "$2"; }

files() {
    say "Fichiers du thème Tunudan ($DISTRO) → ${D:-/}"
    # Thème GTK 3 et décorations de fenêtres
    T="$U/themes/Tunudan"
    rm -rf "$T"; mkdir -p "$T"
    cp -r "$SH/gtk/Tunudan/gtk-3.0" "$SRC/xfce/xfwm4/Tunudan/xfwm4" "$SH/metacity/Tunudan/metacity-1" \
          "$SH/openbox/Tunudan/openbox-3" "$SRC/cinnamon/theme/Tunudan/cinnamon" "$T/"
    cat > "$T/index.theme" <<'EOF'
[Desktop Entry]
Type=X-GNOME-Metatheme
Name=Tunudan
Comment=Thème Tunudan : orange, noir, origami
Encoding=UTF-8

[X-GNOME-Metatheme]
GtkTheme=Tunudan
MetacityTheme=Tunudan
IconTheme=Tunudan
CursorTheme=Tunudan-cursors
ButtonLayout=menu:minimize,maximize,close
EOF
    # Icônes et curseurs
    cp_dir "$SH/icons/Tunudan" "$U/icons/Tunudan"
    cp_dir "$SH/cursors/Tunudan-cursors" "$U/icons/Tunudan-cursors"
    mkdir -p "$U/icons/hicolor/256x256/apps" "$U/pixmaps/tunudan"
    cp "$SH/logo/tunudan-256.png" "$U/icons/hicolor/256x256/apps/tunudan.png"
    cp "$SH"/logo/*.png "$U/pixmaps/tunudan/"
    # Fonds d'écran (+ paires jour/nuit GNOME et Plasma)
    mkdir -p "$U/backgrounds/tunudan/origami" "$U/gnome-background-properties" "$U/wallpapers"
    cp "$SH"/wallpapers/*.png "$U/backgrounds/tunudan/"
    cp "$SH"/wallpapers/origami/*.png "$U/backgrounds/tunudan/origami/"
    ln -sfn origami/origami-grue-sombre.png "$U/backgrounds/tunudan/default.png"
    {
        echo '<?xml version="1.0" encoding="UTF-8"?>'
        echo '<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">'
        echo '<wallpapers>'
        for m in grue:Grue envolee:Envolée sommets:Sommets miura:Miura-ori eventail:Éventail; do
            s=${m%%:*}; n=${m#*:}
            printf '  <wallpaper deleted="false">\n    <name>Tunudan — %s</name>\n' "$n"
            printf '    <filename>%s/origami/origami-%s-clair.png</filename>\n' "$BG" "$s"
            printf '    <filename-dark>%s/origami/origami-%s-sombre.png</filename-dark>\n' "$BG" "$s"
            printf '    <options>zoom</options>\n    <shade_type>solid</shade_type>\n'
            printf '    <pcolor>#F5F1EA</pcolor>\n    <scolor>#0D0D0D</scolor>\n  </wallpaper>\n'
        done
        echo '</wallpapers>'
    } > "$U/gnome-background-properties/tunudan-origami.xml"
    for m in grue:Grue envolee:Envolée sommets:Sommets miura:Miura-ori eventail:Éventail; do
        s=${m%%:*}; n=${m#*:}
        cap=$(printf '%s' "$s" | awk '{print toupper(substr($0,1,1)) substr($0,2)}')
        k="$U/wallpapers/Tunudan-$cap"
        mkdir -p "$k/contents/images" "$k/contents/images_dark"
        ln -sfn "$BG/origami/origami-$s-clair.png" "$k/contents/images/3840x2160.png"
        ln -sfn "$BG/origami/origami-$s-sombre.png" "$k/contents/images_dark/3840x2160.png"
        printf '{\n    "KPlugin": {\n        "Id": "Tunudan-%s",\n        "License": "CC-BY-SA-4.0",\n        "Name": "Tunudan — %s"\n    }\n}\n' "$cap" "$n" > "$k/metadata.json"
    done
    cp_dir "$SRC/plasma/files/wallpaper-Tunudan" "$U/wallpapers/Tunudan"
    # Données partagées : couleurs GTK 4, Qt, terminaux, COSMIC, aperçus des bureaux
    TD="$U/tunudan"
    mkdir -p "$TD/gtk-4.0" "$TD/qt" "$TD/cosmic" "$TD/login"
    cp "$SH/gtk/gtk-4.0.css" "$TD/gtk-4.0/tunudan.css"
    cp "$SH/qt/Tunudan.conf" "$TD/qt/"
    cp "$SRC/cosmic/tunudan-dark.ron" "$TD/cosmic/"
    cp_dir "$SH/terminals" "$TD/terminals"
    cp_dir "$SH/desktops" "$TD/desktops"
    cp "$SRC/login/tunudan-wordmark.png" "$SRC/login/tunudan-wordmark.svg" "$TD/login/"
    mkdir -p "$U/xfce4/terminal/colorschemes" "$U/org.gnome.Ptyxis/palettes" "$U/konsole" "$U/color-schemes"
    cp "$SH/terminals/tunudan.theme" "$U/xfce4/terminal/colorschemes/"
    cp "$SH/terminals/tunudan.palette" "$U/org.gnome.Ptyxis/palettes/"
    # KDE Plasma : couleurs, thème global, Konsole
    cp "$SRC/plasma/files/TunudanDark.colors" "$U/color-schemes/"
    cp "$SRC/plasma/files/Tunudan.profile" "$SRC/plasma/files/Tunudan.colorscheme" "$U/konsole/"
    cp_dir "$SRC/plasma/files/fr.tunudan.desktop" "$U/plasma/look-and-feel/fr.tunudan.desktop"
    # LXQt
    cp_dir "$SRC/lxqt/theme/Tunudan" "$U/lxqt/themes/Tunudan"
    mkdir -p "$U/lxqt/palettes"
    cp "$SRC/lxqt/palettes/Tunudan" "$U/lxqt/palettes/"
    # Écrans de connexion
    cp_dir "$SRC/sddm/tunudan" "$U/sddm/themes/tunudan"
    mkdir -p "$D/etc/sddm.conf.d" "$D/etc/lightdm/lightdm-gtk-greeter.conf.d" "$D/etc/dconf/db/gdm.d"
    cp "$SRC/login/sddm-tunudan.conf" "$D/etc/sddm.conf.d/10-tunudan.conf"
    cp "$SRC/login/lightdm-gtk-greeter.conf" "$D/etc/lightdm/lightdm-gtk-greeter.conf.d/50-tunudan.conf"
    cp "$SRC/login/gdm-tunudan.dconf" "$D/etc/dconf/db/gdm.d/01-tunudan"
    cp "$SRC/login/slick-greeter.conf" "$TD/login/slick-greeter.conf"
    cp "$SRC/login/gdm.profile" "$TD/login/gdm.profile"
    # Réglages par défaut : GNOME, Cinnamon, MATE, Budgie (gsettings)
    mkdir -p "$U/glib-2.0/schemas"
    cp "$SRC/system/zz-tunudan.gschema.override" "$U/glib-2.0/schemas/"
    # KDE, Xfce, LXQt : valeurs par défaut dans /etc/xdg/tunudan, placé en tête de
    # XDG_CONFIG_DIRS (sessions X : Xsession.d ; shells de connexion : profile.d ;
    # sessions lancées par systemd : environment.d). Rien n'écrase les fichiers des paquets.
    rm -rf "$D/etc/xdg/tunudan"
    mkdir -p "$D/etc/xdg/tunudan" "$D/etc/profile.d" "$D/etc/environment.d"
    cp -r "$SRC/system/xdg/." "$D/etc/xdg/tunudan/"
    cp "$SRC/system/tunudan-xdg.sh" "$D/etc/profile.d/tunudan-xdg.sh"
    cp "$SRC/system/50-tunudan.conf" "$D/etc/environment.d/50-tunudan.conf"
    if [ "$DISTRO" != arch ]; then
        mkdir -p "$D/etc/X11/Xsession.d"
        cp "$SRC/system/55tunudan-xdg" "$D/etc/X11/Xsession.d/"
    fi
    mkdir -p "$D/etc/X11/Xresources"
    printf 'Xcursor.theme: Tunudan-cursors\nXcursor.size: 24\n' > "$D/etc/X11/Xresources/tunudan-cursor"
    # Configurations complètes des gestionnaires en mosaïque, pour les nouveaux comptes
    skel
    # Application par utilisateur (premier login) : scripts du pack de thèmes
    P="$TD/themes"
    rm -rf "$P"; mkdir -p "$P/shared"
    cp -r "$SRC/lib" "$SRC/install.sh" "$P/"
    for de in gnome plasma xfce cinnamon mate lxqt budgie cosmic hyprland i3-sway; do
        mkdir -p "$P/$de"; cp "$SRC/$de/install.sh" "$P/$de/"
    done
    cp -r "$SRC/hyprland" "$SRC/i3-sway" "$P/"
    for d in gtk terminals qt rofi waybar notifications; do
        mkdir -p "$P/shared/$d"
        find "$SH/$d" -maxdepth 1 -type f -exec cp {} "$P/shared/$d/" \;
    done
    mkdir -p "$P/cosmic" "$P/lxqt/palettes" && cp "$SRC/cosmic/tunudan-dark.ron" "$P/cosmic/" && cp "$SRC/lxqt/palettes/Tunudan" "$P/lxqt/palettes/"
    mkdir -p "$D/usr/bin" "$D/etc/xdg/autostart"
    cp "$SRC/system/tunudan-theme" "$D/usr/bin/tunudan-theme"
    chmod 755 "$D/usr/bin/tunudan-theme" "$P/install.sh"
    cp "$SRC/system/tunudan-theme-apply.desktop" "$D/etc/xdg/autostart/"
    cp "$SRC/install-system.sh" "$P/install-system.sh"
    chmod 755 "$P/install-system.sh"
}

# Fichiers ~/.config des nouveaux comptes (i3, Sway, Hyprland, Waybar, terminaux…)
skel() {
    K="$D/etc/skel/.config"
    mkdir -p "$K/i3" "$K/i3status" "$K/sway" "$K/hypr" "$K/waybar" "$K/mako" "$K/dunst" "$K/rofi" \
             "$K/fuzzel" "$K/kitty" "$K/foot" "$K/gtk-4.0" "$K/gtk-3.0" "$K/qt6ct/colors" "$K/qt5ct/colors"
    cp "$SRC/wm/i3/config" "$K/i3/config"
    cp "$SRC/i3-sway/i3/tunudan.conf" "$K/i3/tunudan.conf"
    cp "$SRC/i3-sway/i3/bar.conf" "$K/i3/tunudan-bar.conf"
    cp "$SRC/i3-sway/i3/i3status.conf" "$K/i3status/tunudan.conf"
    cp "$SRC/wm/sway/config" "$K/sway/config"
    cp "$SRC/i3-sway/sway/tunudan.conf" "$K/sway/tunudan.conf"
    cp "$SRC/i3-sway/sway/bar.conf" "$K/sway/tunudan-bar.conf"
    if [ "$DISTRO" = arch ]; then
        cp "$SRC/wm/hypr/hyprland.lua" "$K/hypr/hyprland.lua"
        cp "$SRC/hyprland/tunudan.lua" "$K/hypr/tunudan.lua"
        cp "$SRC/hyprland/hyprpaper.conf" "$K/hypr/hyprpaper.conf"
    else
        cp "$SRC/wm/hypr/hyprland.conf" "$K/hypr/hyprland.conf"
        cp "$SRC/hyprland/tunudan.conf" "$K/hypr/tunudan.conf"
        cp "$SRC/hyprland/hyprpaper.conf" "$K/hypr/hyprpaper.conf"
    fi
    cp "$SH/waybar/style.css" "$K/waybar/tunudan.css"
    for wm in sway hyprland niri; do cp "$SH/waybar/config-$wm.jsonc" "$K/waybar/tunudan-$wm.jsonc"; done
    cp "$SH/notifications/mako" "$K/mako/tunudan"
    cp "$SH/notifications/dunstrc" "$K/dunst/dunstrc"
    cp "$SH/rofi/tunudan.rasi" "$K/rofi/tunudan.rasi"
    cp "$SRC/system/fuzzel.ini" "$K/fuzzel/fuzzel.ini"
    cp "$SH/terminals/kitty.conf" "$K/kitty/tunudan.conf"
    printf 'include tunudan.conf\nfont_family JetBrains Mono\nfont_size 11.5\nwindow_padding_width 10\n' > "$K/kitty/kitty.conf"
    { echo "include=/usr/share/tunudan/terminals/foot.ini"; echo; echo "[main]"; echo "font=JetBrains Mono:size=11"; } > "$K/foot/foot.ini"
    echo '@import url("file:///usr/share/tunudan/gtk-4.0/tunudan.css");' > "$K/gtk-4.0/gtk.css"
    printf '[Settings]\ngtk-theme-name=Tunudan\ngtk-icon-theme-name=Tunudan\ngtk-cursor-theme-name=Tunudan-cursors\ngtk-font-name=Inter 11\ngtk-application-prefer-dark-theme=1\n' > "$K/gtk-3.0/settings.ini"
    printf '[Settings]\ngtk-icon-theme-name=Tunudan\ngtk-cursor-theme-name=Tunudan-cursors\ngtk-font-name=Inter 11\ngtk-application-prefer-dark-theme=1\n' > "$K/gtk-4.0/settings.ini"
    for v in qt5ct qt6ct; do
        cp "$SH/qt/Tunudan.conf" "$K/$v/colors/Tunudan.conf"
        printf '[Appearance]\ncolor_scheme_path=/usr/share/tunudan/qt/Tunudan.conf\ncustom_palette=true\nicon_theme=Tunudan\nstyle=Fusion\n' > "$K/$v/$v.conf"
    done
    # Chemins des fonds : version système
    for f in "$K/i3/tunudan.conf" "$K/sway/tunudan.conf" "$K/hypr/hyprpaper.conf"; do
        sed -i "s#\$HOME/.local/share/backgrounds/tunudan#$BG#g; s#~/.local/share/backgrounds/tunudan#$BG#g" "$f"
    done
}

activate() {
    say "Activation (schémas, curseur, écrans de connexion)"
    if command -v glib-compile-schemas >/dev/null 2>&1; then
        glib-compile-schemas /usr/share/glib-2.0/schemas 2>/dev/null || true
    fi
    for t in Tunudan Tunudan-cursors hicolor; do
        command -v gtk-update-icon-cache >/dev/null 2>&1 && gtk-update-icon-cache -qf "/usr/share/icons/$t" 2>/dev/null || true
    done
    # Curseur par défaut du système
    if command -v update-alternatives >/dev/null 2>&1 && [ "$DISTRO" != arch ]; then
        update-alternatives --install /usr/share/icons/default/index.theme x-cursor-theme \
            /usr/share/icons/Tunudan-cursors/cursor.theme 95 >/dev/null 2>&1 || true
    else
        mkdir -p /usr/share/icons/default
        printf '[Icon Theme]\nInherits=Tunudan-cursors\n' > /usr/share/icons/default/index.theme
    fi
    # GDM : profil dconf de l'écran de connexion
    if [ -d /etc/dconf ] && command -v dconf >/dev/null 2>&1; then
        mkdir -p /etc/dconf/profile
        [ -f /etc/dconf/profile/gdm ] || cp /usr/share/tunudan/login/gdm.profile /etc/dconf/profile/gdm
        dconf update 2>/dev/null || true
    fi
    # Linux Mint : écran de connexion slick-greeter
    if [ "$DISTRO" = mint ] || [ -x /usr/sbin/slick-greeter ]; then
        if [ -f /etc/lightdm/slick-greeter.conf ] && ! grep -q Tunudan /etc/lightdm/slick-greeter.conf; then
            cp /etc/lightdm/slick-greeter.conf /etc/lightdm/slick-greeter.conf.avant-tunudan
        fi
        cp /usr/share/tunudan/login/slick-greeter.conf /etc/lightdm/slick-greeter.conf
    fi
}

[ "$DO_FILES" = 1 ] && files
[ "$DO_ACTIVATE" = 1 ] && [ -z "$D" ] && activate
say "Thème Tunudan installé."

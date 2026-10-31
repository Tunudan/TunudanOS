# shellcheck shell=sh
# Fonctions communes des installateurs de thèmes Tunudan.
# Sourcé par themes/install.sh et themes/<interface>/install.sh. Tout est installé
# dans le dossier personnel : aucun droit administrateur n'est nécessaire,
# sauf pour --deps (installation des paquets manquants).
#
# Mode système (TUNUDAN_SYSTEM=1, ou automatique si le thème est déjà dans /usr/share,
# cas de Tunudan OS) : les fichiers du thème ne sont pas recopiés dans le dossier
# personnel, seuls les réglages du compte sont faits.

THEMES_DIR=${THEMES_DIR:-$(cd "$(dirname "$0")/.." && pwd)}
SHARED="$THEMES_DIR/shared"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}"
if [ -z "${TUNUDAN_SYSTEM:-}" ]; then
    if [ -f /usr/share/icons/Tunudan/index.theme ] && [ -d /usr/share/themes/Tunudan/gtk-3.0 ] \
       && [ -d /usr/share/backgrounds/tunudan/origami ]; then TUNUDAN_SYSTEM=1; else TUNUDAN_SYSTEM=0; fi
fi
if [ "$TUNUDAN_SYSTEM" = 1 ]; then
    WALL_DIR=/usr/share/backgrounds/tunudan
    THEME_DIR=/usr/share/themes/Tunudan
    ICON_DIR=/usr/share/icons/Tunudan
    CURSOR_DIR=/usr/share/icons/Tunudan-cursors
else
    WALL_DIR="$DATA/backgrounds/tunudan"
    THEME_DIR="$DATA/themes/Tunudan"
    ICON_DIR="$DATA/icons/Tunudan"
    CURSOR_DIR="$DATA/icons/Tunudan-cursors"
fi
# shellcheck disable=SC2034 # utilisés par les scripts de chaque interface
WALLPAPER="$WALL_DIR/origami/origami-grue-sombre.png"
# shellcheck disable=SC2034
WALLPAPER_LIGHT="$WALL_DIR/origami/origami-grue-clair.png"
CURSOR=Tunudan-cursors
STAMP=$(date +%Y%m%d-%H%M%S)
TUNUDAN_DEPS=${TUNUDAN_DEPS:-0}

O=$(printf '\033[1;38;5;208m'); G=$(printf '\033[32m'); Y=$(printf '\033[33m'); R=$(printf '\033[0m')
say()  { printf '%s◆%s %s\n' "$O" "$R" "$*"; }
ok()   { printf '  %s✓%s %s\n' "$G" "$R" "$*"; }
warn() { printf '  %s!%s %s\n' "$Y" "$R" "$*"; }
has()  { command -v "$1" >/dev/null 2>&1; }

# Copie de sécurité d'un fichier de l'utilisateur avant de le modifier (une fois par exécution)
backup() {
    [ -f "$1" ] || return 0
    [ -f "$1.tunudan-$STAMP" ] || cp -p "$1" "$1.tunudan-$STAMP"
}

# Ajoute une ligne à un fichier si elle n'y est pas déjà
add_line() {
    file=$1; line=$2
    mkdir -p "$(dirname "$file")"
    touch "$file"
    if ! grep -qxF "$line" "$file"; then
        backup "$file"
        printf '\n%s\n' "$line" >> "$file"
    fi
}

# Écrit clé=valeur dans une section d'un fichier .ini (créé si besoin)
ini_set() {
    file=$1; section=$2; key=$3; value=$4
    mkdir -p "$(dirname "$file")"
    touch "$file"
    backup "$file"
    tmp=$(mktemp)
    awk -v s="[$section]" -v k="$key" -v v="$value" '
        BEGIN { insec = 0; done = 0; found = 0 }
        $0 == s { print; insec = 1; found = 1; next }
        /^\[/ { if (insec && !done) { print k "=" v; done = 1 } insec = 0 }
        insec && index($0, k "=") == 1 { if (!done) { print k "=" v; done = 1 } next }
        { print }
        END {
            if (!found) { print ""; print s; print k "=" v }
            else if (insec && !done) print k "=" v
        }' "$file" > "$tmp"
    cat "$tmp" > "$file"
    rm -f "$tmp"
}

# gsettings sans erreur si le schéma ou la clé n'existe pas sur ce système
gset() {
    has gsettings || return 0
    if gsettings writable "$1" "$2" >/dev/null 2>&1; then
        gsettings set "$1" "$2" "$3" 2>/dev/null && return 0
    fi
    return 1
}

# ----------------------------------------------------------------- paquets
pkg_manager() {
    for m in apt-get pacman dnf zypper xbps-install; do
        if has "$m"; then echo "$m"; return; fi
    done
}

# Nom du paquet selon la distribution (nom générique → nom réel)
pkg_name() {
    case "$(pkg_manager):$1" in
        apt-get:papirus) echo papirus-icon-theme ;;
        apt-get:inter) echo fonts-inter ;;
        apt-get:jetbrains) echo fonts-jetbrains-mono ;;
        pacman:papirus) echo papirus-icon-theme ;;
        pacman:inter) echo inter-font ;;
        pacman:jetbrains) echo ttf-jetbrains-mono ;;
        dnf:papirus) echo papirus-icon-theme ;;
        dnf:inter) echo rsms-inter-fonts ;;
        dnf:jetbrains) echo jetbrains-mono-fonts ;;
        zypper:papirus) echo papirus-icon-theme ;;
        zypper:inter) echo google-inter-fonts ;;
        zypper:jetbrains) echo jetbrains-mono-fonts ;;
        *:*) echo "${1#*:}" ;;
    esac
}

pkg_install() {
    [ "$TUNUDAN_DEPS" = 1 ] || return 1
    m=$(pkg_manager)
    [ -n "$m" ] || return 1
    sudo=""
    [ "$(id -u)" = 0 ] || sudo=sudo
    for p in "$@"; do
        name=$(pkg_name "$p")
        say "Installation du paquet $name (mot de passe administrateur demandé)"
        case "$m" in
            apt-get) $sudo apt-get install -y "$name" ;;
            pacman) $sudo pacman -S --needed --noconfirm "$name" ;;
            dnf) $sudo dnf install -y "$name" ;;
            zypper) $sudo zypper --non-interactive install "$name" ;;
            xbps-install) $sudo xbps-install -y "$name" ;;
        esac || warn "Paquet $name non installé"
    done
}

# ----------------------------------------------------------------- briques communes
ORIGAMI="grue:Grue envolee:Envolée sommets:Sommets miura:Miura-ori eventail:Éventail"

install_wallpapers() {
    if [ "$TUNUDAN_SYSTEM" = 1 ]; then ok "Fonds d'écran : déjà installés dans $WALL_DIR"; return 0; fi
    mkdir -p "$WALL_DIR/origami"
    cp "$SHARED"/wallpapers/*.png "$WALL_DIR/"
    cp "$SHARED"/wallpapers/origami/*.png "$WALL_DIR/origami/" 2>/dev/null || true
    # Paires jour/nuit : GNOME (filename-dark) …
    x="$DATA/gnome-background-properties/tunudan-origami.xml"
    mkdir -p "$(dirname "$x")"
    {
        echo '<?xml version="1.0" encoding="UTF-8"?>'
        echo '<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">'
        echo '<wallpapers>'
        for m in $ORIGAMI; do
            slug=${m%%:*}; name=${m#*:}
            printf '  <wallpaper deleted="false">\n    <name>Tunudan — %s</name>\n' "$name"
            printf '    <filename>%s/origami/origami-%s-clair.png</filename>\n' "$WALL_DIR" "$slug"
            printf '    <filename-dark>%s/origami/origami-%s-sombre.png</filename-dark>\n' "$WALL_DIR" "$slug"
            printf '    <options>zoom</options>\n    <shade_type>solid</shade_type>\n'
            printf '    <pcolor>#F5F1EA</pcolor>\n    <scolor>#0D0D0D</scolor>\n  </wallpaper>\n'
        done
        echo '</wallpapers>'
    } > "$x"
    # … et KDE Plasma (images / images_dark)
    for m in $ORIGAMI; do
        slug=${m%%:*}; name=${m#*:}
        cap=$(printf '%s' "$slug" | awk '{print toupper(substr($0,1,1)) substr($0,2)}')
        k="$DATA/wallpapers/Tunudan-$cap"
        mkdir -p "$k/contents/images" "$k/contents/images_dark"
        ln -sfn "$WALL_DIR/origami/origami-$slug-clair.png" "$k/contents/images/3840x2160.png"
        ln -sfn "$WALL_DIR/origami/origami-$slug-sombre.png" "$k/contents/images_dark/3840x2160.png"
        printf '{\n    "KPlugin": {\n        "Id": "Tunudan-%s",\n        "License": "CC-BY-SA-4.0",\n        "Name": "Tunudan — %s"\n    }\n}\n' "$cap" "$name" > "$k/metadata.json"
    done
    ok "Fonds d'écran (dont 10 origami, clairs et sombres) dans $WALL_DIR"
}

install_fonts() {
    has fc-list || return 0
    missing=""
    fc-list | grep -qi "Inter" || missing="$missing inter"
    fc-list | grep -qi "JetBrains" || missing="$missing jetbrains"
    [ -z "$missing" ] && { ok "Polices Inter et JetBrains Mono présentes"; return 0; }
    # shellcheck disable=SC2086
    if pkg_install $missing; then
        ok "Polices installées"
    else
        warn "Polices manquantes :$missing (relancer avec --deps, sinon une police de repli est utilisée)"
    fi
}

# Thème « Tunudan » regroupant GTK 3 et les décorations de fenêtres
install_theme_dir() {
    if [ "$TUNUDAN_SYSTEM" = 1 ]; then ok "Thème GTK et décorations : déjà installés dans $THEME_DIR"; return 0; fi
    rm -rf "$THEME_DIR"
    mkdir -p "$THEME_DIR"
    cp -r "$SHARED/gtk/Tunudan/gtk-3.0" "$THEME_DIR/"
    cp -r "$THEMES_DIR/xfce/xfwm4/Tunudan/xfwm4" "$THEME_DIR/"
    cp -r "$SHARED/metacity/Tunudan/metacity-1" "$THEME_DIR/"
    cp -r "$SHARED/openbox/Tunudan/openbox-3" "$THEME_DIR/"
    cp -r "$THEMES_DIR/cinnamon/theme/Tunudan/cinnamon" "$THEME_DIR/"
    cat > "$THEME_DIR/index.theme" <<EOF
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
    # Certains bureaux (anciens Cinnamon, MATE, Openbox) cherchent encore dans ~/.themes
    mkdir -p "$HOME/.themes"
    [ -e "$HOME/.themes/Tunudan" ] || ln -s "$THEME_DIR" "$HOME/.themes/Tunudan"
    ok "Thème GTK 3 et décorations de fenêtres dans $THEME_DIR"
}

# Applications GTK 4 / libadwaita (elles ignorent les thèmes : on passe par gtk.css)
install_gtk4() {
    mkdir -p "$CONF/gtk-4.0"
    f="$CONF/gtk-4.0/gtk.css"
    touch "$f"
    if [ "$TUNUDAN_SYSTEM" = 1 ] && [ -f /usr/share/tunudan/gtk-4.0/tunudan.css ]; then
        imp='@import url("file:///usr/share/tunudan/gtk-4.0/tunudan.css");'
    else
        cp "$SHARED/gtk/gtk-4.0.css" "$CONF/gtk-4.0/tunudan.css"
        imp='@import url("tunudan.css");'
    fi
    if ! grep -q 'tunudan.css' "$f"; then
        backup "$f"
        { echo "$imp"; cat "$f"; } > "$f.tmp" && mv "$f.tmp" "$f"
    fi
    ok "Couleurs Tunudan pour les applications GTK 4 (libadwaita)"
}

# Réglages GTK lus quand aucun démon de réglages ne tourne (i3, Sway, Hyprland, LXQt)
gtk_settings_ini() {
    for v in 3.0 4.0; do
        f="$CONF/gtk-$v/settings.ini"
        [ "$v" = 3.0 ] && ini_set "$f" Settings gtk-theme-name Tunudan
        ini_set "$f" Settings gtk-icon-theme-name Tunudan
        ini_set "$f" Settings gtk-cursor-theme-name "$CURSOR"
        ini_set "$f" Settings gtk-cursor-theme-size 24
        ini_set "$f" Settings gtk-font-name "Inter 11"
        ini_set "$f" Settings gtk-application-prefer-dark-theme 1
    done
    gset org.gnome.desktop.interface gtk-theme Tunudan || true
    gset org.gnome.desktop.interface icon-theme Tunudan || true
    gset org.gnome.desktop.interface cursor-theme "$CURSOR" || true
    gset org.gnome.desktop.interface color-scheme prefer-dark || true
    ok "Réglages GTK (settings.ini et gsettings)"
}

# Icônes : ~290 icônes dessinées Tunudan (dossiers, applications, fichiers, appareils…),
# Papirus-Dark pour toutes les autres (héritage déclaré dans index.theme)
has_papirus() {
    for d in "$DATA/icons/Papirus-Dark" /usr/share/icons/Papirus-Dark /usr/local/share/icons/Papirus-Dark; do
        [ -d "$d" ] && return 0
    done
    return 1
}

install_icons() {
    if ! has_papirus; then
        pkg_install papirus || true
    fi
    if ! has_papirus && has wget && [ "${TUNUDAN_NO_DOWNLOAD:-0}" != 1 ] && [ "$TUNUDAN_SYSTEM" != 1 ]; then
        say "Téléchargement des icônes Papirus (complément) dans votre dossier personnel"
        wget -qO- https://raw.githubusercontent.com/PapirusDevelopmentTeam/papirus-icon-theme/master/install.sh \
            | DESTDIR="$DATA/icons" sh >/dev/null 2>&1 || true
    fi
    has_papirus || warn "Papirus absent : les icônes non dessinées par Tunudan viendront d'Adwaita"
    if [ "$TUNUDAN_SYSTEM" = 1 ]; then
        ok "Icônes Tunudan : déjà installées dans $ICON_DIR"
        return 0
    fi
    rm -rf "$ICON_DIR"
    mkdir -p "$(dirname "$ICON_DIR")"
    cp -r "$SHARED/icons/Tunudan" "$ICON_DIR"
    mkdir -p "$DATA/icons/hicolor/256x256/apps"
    cp "$SHARED/logo/tunudan-256.png" "$DATA/icons/hicolor/256x256/apps/tunudan.png"
    has gtk-update-icon-cache && gtk-update-icon-cache -qf "$ICON_DIR" 2>/dev/null || true
    ok "Icônes Tunudan ($(find "$ICON_DIR" -name '*.svg' | wc -l | tr -d ' ') noms d'icônes, complétées par Papirus)"
}

# Curseurs : flèche orange Tunudan (fichiers, puis curseur par défaut du compte)
install_cursors() {
    if [ "$TUNUDAN_SYSTEM" != 1 ]; then
        rm -rf "$CURSOR_DIR"
        mkdir -p "$(dirname "$CURSOR_DIR")"
        cp -r "$SHARED/cursors/Tunudan-cursors" "$CURSOR_DIR"
        # Curseur par défaut des applications X11 qui ne lisent aucun réglage
        d="$HOME/.icons/default/index.theme"
        if [ ! -f "$d" ] || grep -q Tunudan "$d"; then
            mkdir -p "$(dirname "$d")"
            printf '[Icon Theme]\nInherits=%s\n' "$CURSOR" > "$d"
            ln -sfn "$CURSOR_DIR" "$HOME/.icons/$CURSOR"
        else
            warn "$HOME/.icons/default/index.theme existe déjà : curseur par défaut inchangé"
        fi
    fi
    add_line "$HOME/.Xresources" "Xcursor.theme: $CURSOR"
    gset org.gnome.desktop.interface cursor-theme "$CURSOR" || true
    gset org.gnome.desktop.interface cursor-size 24 || true
    ok "Curseurs Tunudan"
}

# Palette Qt pour qt5ct / qt6ct (environnements sans réglages Qt intégrés)
install_qt() {
    for v in qt5ct qt6ct; do
        mkdir -p "$CONF/$v/colors"
        cp "$SHARED/qt/Tunudan.conf" "$CONF/$v/colors/Tunudan.conf"
        ini_set "$CONF/$v/$v.conf" Appearance color_scheme_path "$CONF/$v/colors/Tunudan.conf"
        ini_set "$CONF/$v/$v.conf" Appearance custom_palette true
        ini_set "$CONF/$v/$v.conf" Appearance icon_theme Tunudan
        ini_set "$CONF/$v/$v.conf" Appearance style Fusion
    done
    ok "Palette Qt (qt5ct/qt6ct). Pensez à QT_QPA_PLATFORMTHEME=qt6ct"
}

# Couleurs des terminaux installés
install_terminals() {
    T="$SHARED/terminals"
    if has kitty || [ -d "$CONF/kitty" ]; then
        mkdir -p "$CONF/kitty"
        cp "$T/kitty.conf" "$CONF/kitty/tunudan.conf"
        add_line "$CONF/kitty/kitty.conf" "include tunudan.conf"
        ok "kitty"
    fi
    if has foot || [ -d "$CONF/foot" ]; then
        mkdir -p "$CONF/foot"
        cp "$T/foot.ini" "$CONF/foot/tunudan.ini"
        f="$CONF/foot/foot.ini"
        if [ ! -f "$f" ] || ! grep -q 'tunudan.ini' "$f"; then
            backup "$f"
            { echo "include=$CONF/foot/tunudan.ini"; [ -f "$f" ] && cat "$f"; } > "$f.tmp" && mv "$f.tmp" "$f"
        fi
        ok "foot"
    fi
    if has alacritty || [ -d "$CONF/alacritty" ]; then
        mkdir -p "$CONF/alacritty"
        cp "$T/alacritty.toml" "$CONF/alacritty/tunudan.toml"
        f="$CONF/alacritty/alacritty.toml"
        if [ ! -f "$f" ]; then
            printf '[general]\nimport = ["%s"]\n' "$CONF/alacritty/tunudan.toml" > "$f"
            ok "alacritty"
        elif ! grep -q 'tunudan.toml' "$f"; then
            warn "alacritty : ajoutez \"$CONF/alacritty/tunudan.toml\" à la liste import de [general]"
        fi
    fi
    if has xfce4-terminal; then
        mkdir -p "$DATA/xfce4/terminal/colorschemes"
        cp "$T/tunudan.theme" "$DATA/xfce4/terminal/colorschemes/tunudan.theme"
        ok "xfce4-terminal (schéma « Tunudan » dans les préférences)"
    fi
    if has ptyxis; then
        mkdir -p "$DATA/org.gnome.Ptyxis/palettes"
        cp "$T/tunudan.palette" "$DATA/org.gnome.Ptyxis/palettes/tunudan.palette"
        uuid=$(gsettings get org.gnome.Ptyxis default-profile-uuid 2>/dev/null | tr -d "'")
        if [ -n "$uuid" ]; then
            gset "org.gnome.Ptyxis.Profile:/org/gnome/Ptyxis/Profiles/$uuid/" palette-id tunudan || true
        fi
        ok "Ptyxis (palette « Tunudan »)"
    fi
    palette="['$(sed 's/:/'"'"', '"'"'/g' "$T/vte-palette.txt" | tr -d '\n')']"
    if has gnome-terminal; then
        p=$(gsettings get org.gnome.Terminal.ProfilesList default 2>/dev/null | tr -d "'")
        if [ -n "$p" ]; then
            s="org.gnome.Terminal.Legacy.Profile:/org/gnome/terminal/legacy/profiles:/:$p/"
            gset "$s" use-theme-colors false || true
            gset "$s" foreground-color '#F5F1EA' || true
            gset "$s" background-color '#0D0D0D' || true
            gset "$s" palette "$palette" || true
            ok "GNOME Terminal"
        fi
    fi
    if has mate-terminal; then
        s="org.mate.terminal.profile:/org/mate/terminal/profiles/default/"
        gset "$s" use-theme-colors false || true
        gset "$s" foreground-color '#F5F1EA' || true
        gset "$s" background-color '#0D0D0D' || true
        gset "$s" palette "$(tr -d '\n' < "$T/vte-palette.txt")" || true
        ok "MATE Terminal"
    fi
}

# Mise en place commune à toutes les interfaces
install_base() {
    install_wallpapers
    install_fonts
    install_theme_dir
    install_gtk4
    install_icons
    install_cursors
    install_terminals
}

# Règle le thème Openbox/labwc dans un rc.xml (bloc <theme><name>…</name>)
set_ob_theme() {
    rc=$1
    if [ ! -f "$rc" ]; then
        mkdir -p "$(dirname "$rc")"
        cat > "$rc" <<XML
<?xml version="1.0"?>
<labwc_config>
  <theme>
    <name>Tunudan</name>
    <cornerRadius>10</cornerRadius>
    <font place="ActiveWindow"><name>Inter</name><size>10</size><weight>bold</weight></font>
    <font place="InactiveWindow"><name>Inter</name><size>10</size><weight>bold</weight></font>
  </theme>
</labwc_config>
XML
        return 0
    fi
    backup "$rc"
    tmp=$(mktemp)
    awk '
        /<theme>/ { intheme = 1 }
        intheme && !done && /<name>[^<]*<\/name>/ { sub(/<name>[^<]*<\/name>/, "<name>Tunudan</name>"); done = 1 }
        /<\/theme>/ { intheme = 0 }
        { print }
        END { if (!done) exit 3 }' "$rc" > "$tmp" && cat "$tmp" > "$rc" && rm -f "$tmp" && return 0
    rm -f "$tmp"
    # Pas de bloc <theme> : on l'ajoute avant la balise de fermeture
    sed -i 's#</\(labwc_config\|openbox_config\)>#  <theme><name>Tunudan</name></theme>\n</\1>#' "$rc"
}

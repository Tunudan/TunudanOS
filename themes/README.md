# Thème Tunudan complet pour 12 interfaces Linux

Orange `#FF6B1A`, noir `#0D0D0D`, origami. Pas seulement un fond et des couleurs :
icônes, curseurs, fenêtres, écrans de connexion, terminaux, barres et lanceurs.
Un seul installateur, pour n'importe quelle distribution (Debian, Ubuntu, Mint,
Fedora, Arch, openSUSE…). Tout s'installe dans votre dossier personnel, sans
droits administrateur.

```sh
./install.sh            # détecte votre bureau
./install.sh xfce       # ou précisez-le
./install.sh --deps     # installe aussi Papirus et les polices si besoin (sudo)
./install.sh --list
./install.sh --uninstall
```

| Interface | Ce qui change | Comment |
| --- | --- | --- |
| GNOME | accent orange (GNOME 47+), mode sombre, applis GTK 3 et 4, icônes, polices, fond | gsettings |
| KDE Plasma | schéma TunudanDark, accent, Konsole, icônes, fond, thème global (`--lnf`) | plasma-apply-*, kwriteconfig6 |
| Xfce | thème GTK, fenêtres xfwm4, panneau sombre, terminal, fond | xfconf |
| Cinnamon | panneau, menu et notifications (thème Cinnamon), fenêtres Metacity, fond | gsettings |
| MATE | thème GTK, fenêtres Marco, terminal, fond | gsettings |
| LXQt | panneau, lanceur, notifications, palette Qt, Openbox/labwc, fond | lxqt.conf |
| Budgie | panneau et Raven via le thème GTK, labwc (10.10+), fond | gsettings, rc.xml |
| COSMIC | thème `tunudan-dark.ron` à importer, mode sombre, icônes | Paramètres > Apparence |
| Hyprland | bordures dégradées, flou, ombres, Waybar, hyprpaper, mako, rofi | Lua (0.55+) ou hyprlang |
| i3 / Sway | couleurs, barre, i3status, rofi, dunst/mako, fond | `include` dans votre config |

Partout : thème GTK 3 « Tunudan » (basé sur adw-gtk3), couleurs libadwaita pour
GTK 4, palette Qt (qt5ct/qt6ct), couleurs des terminaux (kitty, foot, alacritty,
Ptyxis, GNOME Terminal, MATE Terminal, Xfce), et :

- **Icônes** (`icons/build_icons.py`) : 291 icônes dessinées dans le style Tunudan
  (tuile pliée en origami, deux tons d'orange) : dossiers et emplacements,
  77 applications courantes, catégories du menu, appareils, ~120 types de fichiers,
  emblèmes. 1 082 noms d'icônes au total ; Papirus-Dark complète le reste.
- **Curseurs** (`cursors/build_cursors.py`) : flèche orange bicolore, 24 formes
  (main, texte, redimensionnements, zoom, pipette…) et l'attente animée, en
  24 à 96 px, compatibles X11, Wayland, GTK et Qt.
- **Écrans de connexion** : thème SDDM (Plasma, LXQt, Sway, i3, Hyprland),
  LightDM GTK et slick-greeter (Linux Mint), GDM (logo et accent).
- **Gestionnaires en mosaïque** (`wm/`) : configurations complètes i3, Sway et
  Hyprland (0.54 et 0.55+), en AZERTY, prêtes à l'emploi.

Fonds d'écran : 10 fonds origami (Grue, Envolée, Sommets, Miura-ori, Éventail),
chacun en version claire et sombre. Sous GNOME et Plasma, chaque paire bascule
automatiquement en clair ou en sombre avec le mode du système.

Vos fichiers modifiés sont sauvegardés avec l'extension `.tunudan-AAAAMMJJ-HHMMSS`.

## Installation pour tout le système (Tunudan OS)

```sh
sudo ./install-system.sh                         # copie et active (Debian, Mint, Arch)
./install-system.sh --files-only --destdir DIR   # pour un paquet ou une image
```

Le thème va dans `/usr/share`, et devient le réglage **par défaut** de chaque bureau :
schémas GSettings (`zz-tunudan.gschema.override` : GNOME, Cinnamon, MATE, Budgie,
slick-greeter), `/etc/xdg/tunudan` placé en tête de `XDG_CONFIG_DIRS` (KDE, Xfce,
LXQt), curseur par défaut du système, `/etc/skel` pour i3/Sway/Hyprland. Rien
n'écrase les fichiers des autres paquets et chaque utilisateur garde la main.
À la première ouverture de session sur un bureau, `tunudan-theme apply` termine
le travail pour ce compte (terminaux, fonds sur tous les écrans…).

## Waybar sous Sway

La barre Sway par défaut reçoit les couleurs Tunudan. Pour Waybar à la place,
remplacez la ligne `include …/tunudan-bar.conf` de votre config Sway par :

```
bar { swaybar_command waybar -c ~/.config/waybar/tunudan-sway.jsonc -s ~/.config/waybar/tunudan.css }
```

## Aperçus

`previews/` contient des captures réelles prises sous X11/Wayland : applications
GTK 3, xfwm4, Marco (MATE/Cinnamon), Openbox (LXQt/Budgie), i3 et Sway avec Waybar,
icônes, curseurs, écran de connexion SDDM, et les écrans de choix du bureau
(Calamares pour Avancé, écran Tunudan pour Débutant).
GNOME, Plasma, Cinnamon (panneau), COSMIC et Hyprland n'ont pas pu être lancés
dans l'environnement de test : à vérifier sur une vraie machine.

## Modifier les couleurs

Toutes les couleurs viennent de la palette en tête de `build.py`. Pour régénérer :

```sh
pip install cairosvg libsass && npm install -g sass
python3 themes/build.py
python3 themes/icons/build_icons.py --preview
python3 themes/cursors/build_cursors.py --preview
python3 themes/desktops/build_cards.py
```

## Licences

Code et visuels Tunudan : GPL-3.0-or-later et CC BY-SA 4.0. Le thème GTK 3 dérive
d'adw-gtk3 (LGPL-2.1), le thème Cinnamon du thème par défaut de Cinnamon (GPL-2.0),
le thème LXQt du thème « dark » de LXQt (LGPL-2.1). Voir `vendor/README.md`.

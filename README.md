# Tunudan OS

**Apprendre. Coder. Avancer.** La distribution Linux de [Tunudan](https://tunudan.fr) :
orange, noir, origami.

| Édition | Base | Bureau (choisi à l'installation) | Pour qui | Installateur |
| --- | --- | --- | --- | --- |
| **Minimal** | Debian 13 | Console | Vieux PC, serveur maison, ceux qui veulent tout choisir | Debian (texte) |
| **Débutant** | Linux Mint 22.3 | Cinnamon, MATE ou Xfce | Seniors, premiers pas sous Linux | écran Tunudan + installateur de Mint |
| **Avancé** | Debian 13 | 10 au choix : GNOME, KDE Plasma, Xfce, Cinnamon, MATE, LXQt, Budgie, Sway, i3, Hyprland | Élèves dev et IA (pack cyber en option) | Calamares + page « Bureau » |
| **Expert** | Arch Linux | 12 au choix : les 10 + COSMIC et niri (par défaut) | Passionnés, cours cyber et reverse | menu Tunudan + archinstall |

Toutes les éditions portent le **thème Tunudan complet**, quel que soit le bureau :
thème GTK et couleurs libadwaita, décorations de fenêtres, ~290 icônes dessinées
(Papirus pour le reste), curseurs, 10 fonds origami clairs et sombres, écrans de
connexion (SDDM, LightDM, slick-greeter, GDM), réglages par défaut de chaque bureau,
configurations complètes i3/Sway/Hyprland, Plymouth, GRUB et installateur.

Le bureau se choisit pendant l'installation ; seuls les bureaux autres que celui de
la clé (Xfce pour Avancé, Cinnamon pour Débutant) demandent Internet. Il se change
ensuite avec `sudo tunudan-desktop <bureau>` (Debian et Mint).

## Construire une ISO

Il faut Docker (ou Podman avec `DOCKER=podman`), environ 15 Go libres par
édition et une connexion Internet. Ça marche depuis n'importe quelle distribution,
Arch compris.

```sh
make iso EDITION=debutant          # minimal | debutant | avance | expert
make iso EDITION=avance CYBER=1    # Avancé + outils de cybersécurité
make all                           # les quatre éditions
make test EDITION=debutant         # démarre l'ISO dans QEMU
make lint                          # vérifications rapides (shellcheck, Python, KDL…)
```

Les ISO arrivent dans `out/iso/` avec leur somme SHA-256. Le premier build est
long (téléchargement des paquets). Les suivants réutilisent le cache Docker
`tunudan-cache`. L'édition Débutant télécharge l'ISO officielle de Linux Mint
(vérifiée par SHA-256) dans `out/cache/` puis la « remasterise ».

Sans Docker : `sudo debian-live/build-edition.sh avance` sur une Debian 13,
`sudo mint/build-debutant.sh` sur une Ubuntu 24.04 ou une Mint 22 (après
`scripts/build-debs.sh`), `sudo arch/build-expert.sh` sur une Arch (paquet `archiso`).

## Organisation du dépôt

```text
branding/            logo SVG, generate.py (splash, logos), wallpapers.py (10 fonds origami)
packages/            paquets Debian maison (aussi utilisés par l'édition Mint)
  tunudan-theme        thème complet (via themes/install-system.sh), Plymouth, GRUB, Calamares
  tunudan-settings     os-release, mises à jour auto, pare-feu, français
  tunudan-tools        tunudan-welcome, -help, -update, -desktop, install-desktop
  tunudan-desktops     un métapaquet par bureau : tunudan-desktop-gnome, -plasma, -xfce…
  tunudan-meta         tunudan-edition-minimal/-avance/-mint et tunudan-pack-cyber
debian-live/         live-build : Minimal et Avancé (page « Bureau » de Calamares)
mint/                remaster de Linux Mint (Débutant) + écran de choix du bureau
arch/                archiso : Expert (session live niri), listes de paquets par bureau
docker/              images de build Debian, Ubuntu (Mint) et Arch
themes/              thème complet pour 12 interfaces, installateurs utilisateur et système
tests/               lint.sh, boot-qemu.sh
.github/workflows/   construction automatique des 4 ISO, publication sur tag v*
```

## Thème complet pour 12 interfaces

`themes/` contient le thème Tunudan pour GNOME, KDE Plasma, Xfce, Cinnamon, MATE,
LXQt, Budgie, COSMIC, Hyprland, Sway, i3 (et niri dans l'édition Expert) :

- `themes/install.sh` : dans votre dossier personnel, sur n'importe quelle distribution ;
- `themes/install-system.sh` : pour tout le système (c'est ce qu'utilisent les ISO) ;
- `tunudan-theme apply` : applique le thème à votre compte (automatique à la
  première ouverture de session sur chaque bureau).

Archive autonome : `make themes-archive`. Détails dans `themes/README.md`.

## Les outils maison

- **tunudan-welcome** : assistant du premier démarrage (taille du texte, cours suivi, liens).
- **tunudan-help** : bouton « Appeler Tunudan ». Interface graphique : lance RustDesk et
  affiche le numéro à dicter. Console : partage du terminal avec tmate.
- **tunudan-update** : « Votre ordinateur est à jour », mise à jour en un clic,
  rappel quotidien si un redémarrage est nécessaire.
- **tunudan-desktop** : liste les bureaux et en installe un autre
  (`sudo tunudan-desktop plasma`).
- **tunudan-theme** : réapplique le thème Tunudan à votre compte.

Le numéro de téléphone et le serveur RustDesk se règlent dans
`packages/tunudan-settings/files/tunudan.conf` (à remplir avant de diffuser).

## Avant de diffuser publiquement

Voir `docs/a-faire.md` : marque INPI, numéro d'assistance, clé GPG du dépôt
apt, tests sur du vrai matériel.

Licences : code sous GPL-3.0 ou ultérieure, visuels sous CC BY-SA 4.0.
Tunudan OS n'est pas un produit officiel de Debian, de Linux Mint ni d'Arch Linux.

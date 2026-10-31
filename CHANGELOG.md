# Journal des modifications

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
numérotation [SemVer](https://semver.org/lang/fr/).

## [Non publié]

## [0.4.1] - 2026-10-31

Première version dont les 4 ISO se construisent (localement et sur GitHub Actions)
et démarrent dans QEMU.

### Corrigé
- Construction des 4 ISO : arrêt silencieux de live-build (grep sans résultat avec
  `set -e`/`pipefail`), scripts non exécutables, conflit `.zshrc` avec archiso.
- Chaque ISO Debian installait les paquets de tous les bureaux et le pack cyber.
- Noms de paquets : `kde-spectacle` (Debian), `openbsd-netcat` et `otf-font-awesome`
  (Arch) ; `radare2` (absent de Debian 13) passe en Recommends ; `budgie-screensaver` retiré.
- Expert : Waybar Tunudan sous niri (DankMaterialShell n'est que dans l'AUR).
- Menu de démarrage : « Tunudan OS <édition> » et démarrage automatique après 10 s.
- `/etc/os-release` : le système s'annonce comme Tunudan OS (fastfetch affichait Debian).
- Avancé : fond d'écran Tunudan sous Xfce 4.20, lanceur « Installer Tunudan OS ».
- `tests/boot-qemu.sh` : `--headless` ignoré, repli sur `-vga std`, `QEMU_MEM`.

## [0.4.0] - 2026-10-31

### Ajouté
- Choix du bureau pendant l'installation : 10 bureaux pour Avancé (page « Bureau »
  de Calamares), Cinnamon, MATE ou Xfce pour Débutant, 12 pour Expert.
- `tunudan-desktop` : changer de bureau après l'installation.
- Thème Tunudan complet pour 12 interfaces (`themes/`).
- Construction automatique des ISO et publication des releases avec GitHub Actions.
- Licences, guide de contribution, modèles d'issues et de pull requests.

### Corrigé
- Image de build Debian : ajout de `build-essential`, sans quoi `dpkg-buildpackage`
  refusait de construire les paquets `tunudan-*`.

### Modifié
- `make iso` ne construit que l'image Docker utile à l'édition demandée.

[Non publié]: https://github.com/Tunudan/TunudanOS/compare/v0.4.1...HEAD
[0.4.1]: https://github.com/Tunudan/TunudanOS/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/Tunudan/TunudanOS/releases/tag/v0.4.0

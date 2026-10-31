# Journal des modifications

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
numérotation [SemVer](https://semver.org/lang/fr/).

## [Non publié]

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

[Non publié]: https://github.com/Tunudan/TunudanOS/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/Tunudan/TunudanOS/releases/tag/v0.4.0

# À faire avant la v1.0

## Premier build (à faire en premier)

1. `make lint` puis `make iso EDITION=minimal` : c'est l'édition la plus rapide à
   construire, elle valide toute la chaîne live-build.
2. `make test EDITION=minimal`, puis Débutant, Avancé et Expert.
3. Noter les erreurs dans `out/…/build.log` (Debian) ou dans la sortie de mkarchiso.

## Choix du bureau à l'installation (v0.4)

Testé ici : page « Bureau » de Calamares (affichage réel avec la config Tunudan),
écran de choix de l'édition Débutant, installation du paquet tunudan-theme sur une
base Ubuntu 24.04 (celle de Mint 22), installateur de bureau en simulation.
À tester en vrai, dans une machine virtuelle avec Internet :

- [ ] **Avancé** : installer chacun des 10 bureaux ; vérifier que Xfce disparaît
      bien quand on en choisit un autre et que l'écran de connexion est le bon
      (journal : `/var/log/tunudan-install-desktop.log` sur le système installé).
- [ ] **Avancé sans Internet** : choisir GNOME doit garder Xfce et proposer
      `sudo tunudan-desktop gnome` ensuite.
- [ ] **Hyprland sous Debian** : vient de trixie-backports ; vérifier les versions
      (hyprpaper, hypridle, hyprlock sont en Recommends).
- [ ] **Débutant (Mint)** : vérifier qu'Ubiquity lance bien
      `ubiquity/success_command` (MATE et Xfce installés à la fin), et le
      menu de démarrage renommé (BIOS et UEFI).
- [ ] **Prochaine Mint** (base Ubuntu 26.04) : `MINT_VERSION=… make iso EDITION=debutant` ;
      si Mint change d'installateur, adapter `mint/live/tunudan-installer`.
- [ ] **Expert** : menu des 12 bureaux, puis archinstall ; vérifier GDM, SDDM,
      LightDM, cosmic-greeter et greetd selon le choix.

Points non testés ici, faute d'accès aux miroirs Debian et Arch :

- **Noms de paquets** : la plupart sont dans `Depends`. Ceux dont la présence dans
  Debian 13 est incertaine (codium, jupyter-notebook, ghidra, nikto…) sont dans
  `Recommends` : leur absence ne bloque pas le build.
- **niri** : vérifier la configuration avec `niri validate -c arch/expert/airootfs/etc/skel/.config/niri/config.kdl`.
- **DankMaterialShell** : la commande `dms ipc call wallpaper set` du premier
  lancement est à confirmer. Si elle change, il suffit d'adapter
  `arch/expert/airootfs/usr/local/bin/tunudan-niri-session`.
- **archiso** : le build part du profil `releng` installé avec archiso et y ajoute
  la couche Tunudan. Si archiso renomme un fichier, voir `arch/build-expert.sh`.
- **Panneau Xfce** : le fichier `default.xml` ne s'applique qu'aux nouveaux comptes.
- **Noms des paquets par bureau** : `packages/tunudan-desktops/debian/control`
  (Debian) et `arch/expert/desktops/*.txt` (Arch) ; un nom absent bloque
  l'installation de ce bureau seulement (le bureau de la clé est gardé).

## Thèmes (themes/)

Testés ici avec captures : applications GTK 3, xfwm4, Marco, Openbox, i3, Sway + Waybar,
icônes, curseurs, écran de connexion SDDM (Qt 5 et Qt 6), slick-greeter, réglages
par défaut Xfce lus depuis `/etc/xdg/tunudan`, schémas GSettings.
À tester sur une vraie machine :
- [ ] GNOME 47+ (accent orange) et Plasma 6 (schéma, thème global `--lnf`)
- [ ] Panneau Cinnamon (thème recompilé) et panneau LXQt (thème recoloré)
- [ ] COSMIC : import de `tunudan-dark.ron`
- [ ] Hyprland 0.55+ (`tunudan.lua`) et 0.54 (`tunudan.conf`), hyprpaper 0.8
- [ ] Budgie 10.10 sous Wayland (emplacement du rc.xml de labwc)
- [ ] GDM : logo et accent sur l'écran de connexion (dconf `gdm.d`)
- [ ] Curseurs sous Wayland (GNOME, Plasma, Hyprland) et dans les applis Flatpak

## Identité et légal

- [ ] Remplir le numéro d'assistance dans `packages/tunudan-settings/files/tunudan.conf`
- [ ] Logo définitif (`branding/logo.svg`), puis `make branding`
- [ ] Déposer la marque Tunudan (INPI)
- [ ] Ne jamais utiliser les logos Debian ou Arch, garder la mention « basé sur »

## Dépôt apt Tunudan (phase 3)

1. Générer une clé GPG dédiée : `gpg --quick-gen-key "Tunudan OS <repo@tunudan.fr>"`
2. Publier `out/debs/*.deb` avec `reprepro` sur `repo.tunudan.fr`
3. Créer un paquet `tunudan-keyring` (clé dans `/usr/share/keyrings/tunudan-archive-keyring.gpg`)
4. Renommer `/etc/apt/sources.list.d/tunudan.sources.disabled` en `tunudan.sources`
   dans `tunudan-settings`.
   Les mises à jour du thème et des outils arriveront alors par apt.

## Aide à distance

- Héberger un relais RustDesk (`hbbs`/`hbbr`) sur un petit VPS
- Renseigner `serveur` et `cle` dans `tunudan.conf` (champs prévus ; tunudan-help ne les
  applique pas encore à RustDesk : à brancher une fois le relais en place)

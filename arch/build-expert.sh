#!/bin/bash
# Construit l'ISO Tunudan OS Expert (Arch Linux, session live niri, 12 bureaux au choix
# à l'installation) avec archiso.
# À lancer en root sur Arch (ou via « make iso EDITION=expert », qui utilise Docker).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/arch/expert"
WORK="${WORK:-/tmp/tunudan-expert}"
OUTDIR="${OUTDIR:-$ROOT/out/iso}"
VERSION="$(cat "$ROOT/VERSION")"
RELENG=/usr/share/archiso/configs/releng

[ "$(id -u)" = 0 ] || { echo "mkarchiso doit être lancé en root." >&2; exit 1; }
[ -d "$RELENG" ] || { echo "archiso n'est pas installé (pacman -S archiso)." >&2; exit 1; }

echo "==> Tunudan OS $VERSION — édition Expert (Arch, bureau au choix)"
"$ROOT/scripts/prepare-branding.sh"

rm -rf "$WORK" && mkdir -p "$WORK"
P="$WORK/profile"
cp -a "$RELENG" "$P"

# 1. Le live démarre en graphique : on retire l'auto-connexion root sur tty1
#    et systemd-networkd/iwd (remplacés par NetworkManager).
rm -f "$P/airootfs/etc/systemd/system/getty@tty1.service.d/autologin.conf"
find "$P/airootfs/etc/systemd/system" -depth -name 'systemd-networkd*' -exec rm -rf {} +
find "$P/airootfs/etc/systemd/system" -name 'iwd.service' -delete
rm -rf "$P/airootfs/etc/systemd/network"

# 2. Thème Tunudan complet dans le système live (icônes, curseurs, fonds, GTK, Qt,
#    écrans de connexion, réglages par défaut de tous les bureaux)…
sh "$ROOT/themes/install-system.sh" --files-only --distro arch --destdir "$P/airootfs"
#    … et le pack source complet, pour l'installer sur le disque (tunudan-install)
TS="$P/airootfs/usr/share/tunudan/themes-src"
mkdir -p "$TS"
tar -C "$ROOT/themes" --exclude=vendor --exclude=previews --exclude='build*.py' \
    --exclude=__pycache__ --exclude='.build-*' -cf - . | tar -C "$TS" -xf -
#    Fichiers propres à l'édition Expert (niri, zsh, kitty…), prioritaires
cp -a "$SRC/airootfs/." "$P/airootfs/"
T="$ROOT/packages/tunudan-tools"
install -Dm755 "$T/src/tunudan-help"    "$P/airootfs/usr/local/bin/tunudan-help"
install -Dm755 "$T/src/tunudan-welcome" "$P/airootfs/usr/local/bin/tunudan-welcome"
install -Dm755 "$T/src/tunudan-update"  "$P/airootfs/usr/local/bin/tunudan-update"
install -Dm644 "$T/src/tunudan_common.py" "$P/airootfs/usr/lib/tunudan/tunudan_common.py"
install -Dm755 "$T/src/tunudan-update-root" "$P/airootfs/usr/lib/tunudan/tunudan-update-root"
install -Dm644 "$T/polkit/fr.tunudan.update.policy" "$P/airootfs/usr/share/polkit-1/actions/fr.tunudan.update.policy"
install -Dm644 "$T/systemd/tunudan-update-notify.service" "$P/airootfs/usr/lib/systemd/user/tunudan-update-notify.service"
install -Dm644 "$T/systemd/tunudan-update-notify.timer" "$P/airootfs/usr/lib/systemd/user/tunudan-update-notify.timer"
install -Dm644 "$T/autostart/tunudan-welcome.desktop" "$P/airootfs/etc/xdg/autostart/tunudan-welcome.desktop"
for d in "$T"/applications/*.desktop; do
    install -Dm644 "$d" "$P/airootfs/usr/share/applications/$(basename "$d")"
done
install -Dm644 "$ROOT/packages/tunudan-settings/files/tunudan.conf" "$P/airootfs/etc/tunudan/tunudan.conf"
sed -i 's/^nom = .*/nom = expert/' "$P/airootfs/etc/tunudan/tunudan.conf"
TH="$ROOT/packages/tunudan-theme/files"
mkdir -p "$P/airootfs/usr/share/tunudan/fastfetch" "$P/airootfs/usr/share/icons/hicolor/256x256/apps"
cp "$TH"/fastfetch/* "$P/airootfs/usr/share/tunudan/fastfetch/"
cp "$ROOT/branding/out/logo/tunudan-256.png" "$P/airootfs/usr/share/icons/hicolor/256x256/apps/tunudan.png"
mkdir -p "$P/airootfs/usr/share/pixmaps/tunudan"
cp "$ROOT"/branding/out/logo/*.png "$P/airootfs/usr/share/pixmaps/tunudan/"

# 3. Paquets : releng + Tunudan (session live niri). tunudan-install installe ensuite
#    les paquets communs + ceux du bureau choisi.
grep -v '^\s*#' "$SRC/packages.extra" | grep -v '^\s*$' >> "$P/packages.x86_64"
sort -u -o "$P/packages.x86_64" "$P/packages.x86_64"
cp "$SRC/packages.base" "$P/airootfs/usr/share/tunudan/packages-base.txt"
mkdir -p "$P/airootfs/usr/share/tunudan/desktops-arch"
cp "$SRC"/desktops/*.txt "$P/airootfs/usr/share/tunudan/desktops-arch/"

# 4. Identité de l'ISO et droits des fichiers
# shellcheck disable=SC2016 # $(date …) doit être évalué par mkarchiso, pas ici
sed -i \
    -e 's/^iso_name=.*/iso_name="tunudan-os-expert"/' \
    -e 's/^iso_label=.*/iso_label="TUNUDAN_EXPERT_$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y%m)"/' \
    -e 's#^iso_publisher=.*#iso_publisher="Tunudan <https://tunudan.fr>"#' \
    -e 's/^iso_application=.*/iso_application="Tunudan OS Expert"/' \
    -e "s/^iso_version=.*/iso_version=\"$VERSION\"/" \
    "$P/profiledef.sh"
sed -i '/^file_permissions=(/a\  ["/etc/sudoers.d/10-tunudan-live"]="0:0:440"\n  ["/usr/local/bin/tunudan-install"]="0:0:755"\n  ["/usr/local/bin/tunudan-niri-session"]="0:0:755"\n  ["/usr/local/bin/tunudan-help"]="0:0:755"\n  ["/usr/local/bin/tunudan-update"]="0:0:755"\n  ["/usr/local/bin/tunudan-welcome"]="0:0:755"\n  ["/usr/lib/tunudan/tunudan-update-root"]="0:0:755"\n  ["/usr/bin/tunudan-theme"]="0:0:755"\n  ["/usr/share/tunudan/themes/install-system.sh"]="0:0:755"\n  ["/usr/share/tunudan/themes-src/install-system.sh"]="0:0:755"' "$P/profiledef.sh"

# 5. Menu de démarrage aux couleurs Tunudan
{ grep -rl "Arch Linux install medium" "$P" --include='*.cfg' --include='*.conf' || true; } \
    | xargs -r sed -i 's/Arch Linux install medium/Tunudan OS Expert/g'
[ -f "$P/syslinux/splash.png" ] && cp "$ROOT/branding/out/boot/splash-640x480.png" "$P/syslinux/splash.png"

# 6. Construction
mkdir -p "$OUTDIR"
mkarchiso -v -w "$WORK/work" -o "$WORK/out" "$P"
ISO=$(find "$WORK/out" -maxdepth 1 -name '*.iso' | head -n1)
cp "$ISO" "$OUTDIR/tunudan-os-expert-$VERSION-x86_64.iso"
(cd "$OUTDIR" && sha256sum "tunudan-os-expert-$VERSION-x86_64.iso" > "tunudan-os-expert-$VERSION-x86_64.iso.sha256")
echo "==> ISO prête : $OUTDIR/tunudan-os-expert-$VERSION-x86_64.iso"

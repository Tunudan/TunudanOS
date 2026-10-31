#!/bin/bash
# Construit l'ISO d'une édition Debian de Tunudan OS avec live-build.
# À lancer en root dans Debian 13 (ou via « make iso EDITION=… », qui utilise Docker).
#
#   debian-live/build-edition.sh minimal|avance [--cyber]
#
# (L'édition Débutant est basée sur Linux Mint : voir mint/build-debutant.sh.)
set -euo pipefail

EDITION="${1:-}"
CYBER=0
[ "${2:-}" = "--cyber" ] && CYBER=1
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ED_DIR="$ROOT/debian-live/editions/$EDITION"
if [ -z "$EDITION" ] || [ ! -f "$ED_DIR/edition.conf" ]; then
    echo "Usage : $0 minimal|avance [--cyber]" >&2; exit 2
fi
[ "$(id -u)" = 0 ] || { echo "live-build doit être lancé en root." >&2; exit 1; }

# shellcheck disable=SC1091
. "$ED_DIR/edition.conf"
NAME="tunudan-os-$EDITION"
[ "$CYBER" = 1 ] && NAME="$NAME-cyber"
WORK="${WORK:-/tmp/tunudan-build/$NAME}"
OUTDIR="${OUTDIR:-$ROOT/out/iso}"
MIRROR="${MIRROR:-http://deb.debian.org/debian/}"
VERSION="$(cat "$ROOT/VERSION")"

echo "==> Tunudan OS $VERSION — édition $EDITION (installateur : $INSTALLER)"

# 1. Paquets tunudan-*
if ! ls "$ROOT"/out/debs/tunudan-theme_*.deb >/dev/null 2>&1; then
    "$ROOT/scripts/build-debs.sh"
fi

# 2. Configuration live-build
CACHE_KEEP="$WORK.cache"
[ -d "$WORK/cache" ] && rm -rf "$CACHE_KEEP" && mv "$WORK/cache" "$CACHE_KEEP"
rm -rf "$WORK" && mkdir -p "$WORK" && cd "$WORK"
[ -d "$CACHE_KEEP" ] && mv "$CACHE_KEEP" "$WORK/cache"   # garde les paquets déjà téléchargés
DI_OPTS=(--debian-installer none)
if [ "$INSTALLER" = "debian-installer" ]; then
    DI_OPTS=(--debian-installer live --debian-installer-gui false)
fi

lb config \
    --mode debian \
    --distribution trixie \
    --architectures amd64 \
    --linux-flavours amd64 \
    --archive-areas "main contrib non-free-firmware" \
    --mirror-bootstrap "$MIRROR" \
    --mirror-chroot "$MIRROR" \
    --mirror-binary "$MIRROR" \
    --security true \
    --updates true \
    --firmware-chroot true \
    --firmware-binary true \
    --binary-images iso-hybrid \
    --memtest none \
    --checksums sha256 \
    --cache true \
    --apt-recommends true \
    "${DI_OPTS[@]}" \
    --iso-application "Tunudan OS $VERSION" \
    --iso-publisher "Tunudan; https://tunudan.fr" \
    --iso-volume "TUNUDAN_${EDITION^^}" \
    --image-name "$NAME" \
    --bootappend-live "boot=live components $BOOT_EXTRA locales=fr_FR.UTF-8 keyboard-layouts=fr timezone=Europe/Paris username=tunudan user-fullname=Tunudan hostname=tunudan"

# Liste des paquets
{
    echo "# Généré par build-edition.sh"
    cat "$ED_DIR/packages.list"
    [ "$CYBER" = 1 ] && echo "tunudan-pack-cyber"
} > config/package-lists/tunudan.list.chroot

# Paquets maison : live-build en fait un dépôt local
mkdir -p config/packages.chroot
cp "$ROOT"/out/debs/*.deb config/packages.chroot/

# Fichiers et hooks : communs puis spécifiques à l'édition
mkdir -p config/includes.chroot_after_packages config/hooks/live
for src in "$ROOT/debian-live/common" "$ED_DIR"; do
    [ -d "$src/includes" ] && cp -a "$src/includes/." config/includes.chroot_after_packages/
    [ -d "$src/hooks" ] && cp -a "$src/hooks/." config/hooks/live/
done
# Bureau au choix (Calamares) : les métapaquets tunudan-desktop-* restent dans un petit
# dépôt local de l'ISO (/opt/tunudan/repo), copié sur le disque avec le système.
if [ "$INSTALLER" = "calamares" ]; then
    REPO=config/includes.chroot_after_packages/opt/tunudan/repo
    mkdir -p "$REPO"
    cp "$ROOT"/out/debs/tunudan-desktop-*.deb "$REPO/"
    (cd "$REPO" && dpkg-scanpackages --multiversion . /dev/null > Packages 2>/dev/null && gzip -9kf Packages)
fi
# Scripts exécutés au démarrage de la session live uniquement
mkdir -p config/includes.chroot_after_packages/usr/lib/live/config
cp -a "$ROOT/debian-live/common/live-config/." config/includes.chroot_after_packages/usr/lib/live/config/
# Valeurs propres à l'édition dans les hooks
sed -i "s/@EDITION@/$EDITION/g; s/@VERSION@/$VERSION/g; s/@RUSTDESK@/${RUSTDESK:-no}/g" config/hooks/live/*
chmod +x config/hooks/live/* config/includes.chroot_after_packages/usr/lib/live/config/*

# 3. Menu de démarrage aux couleurs Tunudan
if [ -d /usr/share/live/build/bootloaders ]; then
    cp -a /usr/share/live/build/bootloaders config/
    SPLASH="$ROOT/branding/out/boot/splash-640x480.png"
    find config/bootloaders -name 'splash.svg*' -delete
    while IFS= read -r f; do cp "$SPLASH" "$f"; done < <(find config/bootloaders -name 'splash.png')
    for d in config/bootloaders/*/; do
        [ -f "$d/splash.png" ] || cp "$SPLASH" "$d/splash.png"
    done
    { grep -rl "Live system" config/bootloaders || true; } | xargs -r sed -i "s/Live system/Tunudan OS $EDITION_LABEL/g"
    { grep -rl "Debian GNU/Linux" config/bootloaders || true; } | xargs -r sed -i "s#Debian GNU/Linux#Tunudan OS#g"
fi

# 4. Construction
lb build 2>&1 | tee "$WORK/build.log"

mkdir -p "$OUTDIR"
ISO=$(find "$WORK" -maxdepth 1 -name "*.iso" | head -n1)
cp "$ISO" "$OUTDIR/$NAME-$VERSION-amd64.iso"
(cd "$OUTDIR" && sha256sum "$NAME-$VERSION-amd64.iso" > "$NAME-$VERSION-amd64.iso.sha256")
echo "==> ISO prête : $OUTDIR/$NAME-$VERSION-amd64.iso"

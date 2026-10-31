#!/bin/bash
# Construit l'ISO de l'édition Débutant de Tunudan OS : Linux Mint + thème et outils Tunudan,
# bureau au choix (Cinnamon, MATE, Xfce) pendant l'installation.
#
# Principe (« remaster ») : on part de l'ISO officielle de Linux Mint Cinnamon, on ouvre son
# système live (casper/filesystem.squashfs), on y ajoute les paquets tunudan-* et l'écran de
# choix du bureau, puis on referme l'ISO en gardant le démarrage d'origine (BIOS + UEFI,
# Secure Boot compris).
#
# À lancer en root sur Ubuntu 24.04 / Linux Mint 22 (ou via « make iso EDITION=debutant »).
#   MINT_VERSION=22.3              version de Mint (22.x, base Ubuntu 24.04)
#   MINT_MIRROR=https://…/stable   miroir (défaut : mirrors.kernel.org)
#   MINT_ISO=/chemin/mint.iso      ISO déjà téléchargée (sinon téléchargée dans out/cache)
#   MINT_ISO_SHA256=…              empreinte attendue (défaut : celle de Mint 22.3 Cinnamon,
#                                  sinon lue dans sha256sum.txt du miroir)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(cat "$ROOT/VERSION")"
MINT_VERSION="${MINT_VERSION:-22.3}"
MINT_MIRROR="${MINT_MIRROR:-https://mirrors.kernel.org/linuxmint/stable}"
ISO_NAME="linuxmint-$MINT_VERSION-cinnamon-64bit.iso"
CACHE="$ROOT/out/cache"
WORK="${WORK:-/tmp/tunudan-build/mint-debutant}"
OUTDIR="${OUTDIR:-$ROOT/out/iso}"
OUT_ISO="$OUTDIR/tunudan-os-debutant-$VERSION-amd64.iso"
KNOWN_SHA_22_3="a081ab202cfda17f6924128dbd2de8b63518ac0531bcfe3f1a1b88097c459bd4"
LABEL="Tunudan OS Debutant"

[ "$(id -u)" = 0 ] || { echo "À lancer en root (chroot, montages)." >&2; exit 1; }
for t in xorriso unsquashfs mksquashfs curl sha256sum; do
    command -v "$t" >/dev/null || { echo "Outil manquant : $t (apt install xorriso squashfs-tools curl)" >&2; exit 1; }
done
echo "==> Tunudan OS $VERSION — édition Débutant (Linux Mint $MINT_VERSION)"

# 1. ISO de Linux Mint ------------------------------------------------------------
mkdir -p "$CACHE" "$OUTDIR"
ISO="${MINT_ISO:-$CACHE/$ISO_NAME}"
if [ ! -f "$ISO" ]; then
    echo "==> Téléchargement de $ISO_NAME (2,9 Go)"
    curl -fL --retry 3 -o "$ISO.part" "$MINT_MIRROR/$MINT_VERSION/$ISO_NAME"
    mv "$ISO.part" "$ISO"
fi
SHA="${MINT_ISO_SHA256:-}"
if [ -z "$SHA" ] && [ "$MINT_VERSION" = 22.3 ]; then SHA=$KNOWN_SHA_22_3; fi
if [ -z "$SHA" ]; then
    SHA=$(curl -fsSL "$MINT_MIRROR/$MINT_VERSION/sha256sum.txt" | awk -v f="*$ISO_NAME" '$2 == f {print $1}')
fi
echo "==> Vérification de l'empreinte SHA-256"
echo "$SHA  $ISO" | sha256sum -c - || { echo "Empreinte incorrecte : ISO corrompue ou modifiée." >&2; exit 1; }

# 2. Paquets tunudan-* ---------------------------------------------------------------
if ! ls "$ROOT"/out/debs/tunudan-theme_*.deb >/dev/null 2>&1; then
    echo "Paquets absents : lancez d'abord « make debs » (ou scripts/build-debs.sh)." >&2
    exit 1
fi

# 3. Ouverture de l'ISO --------------------------------------------------------------
rm -rf "$WORK" && mkdir -p "$WORK" && cd "$WORK"
echo "==> Extraction de l'ISO"
xorriso -osirrox on -indev "$ISO" -extract / iso >/dev/null 2>&1
chmod -R u+w iso
echo "==> Extraction du système live"
unsquashfs -q -d rootfs iso/casper/filesystem.squashfs

# 4. Personnalisation dans le chroot -------------------------------------------------
MOUNTS=""
cleanup() {
    for m in $MOUNTS; do umount -l "$m" 2>/dev/null || true; done
}
trap cleanup EXIT
for d in dev dev/pts proc sys run; do
    mount --bind "/$d" "rootfs/$d"; MOUNTS="$WORK/rootfs/$d $MOUNTS"
done
mv rootfs/etc/resolv.conf rootfs/etc/resolv.conf.mint 2>/dev/null || true
cat /etc/resolv.conf > rootfs/etc/resolv.conf
printf '#!/bin/sh\nexit 101\n' > rootfs/usr/sbin/policy-rc.d; chmod 755 rootfs/usr/sbin/policy-rc.d

mkdir -p rootfs/tmp/tunudan-debs
for p in tunudan-theme tunudan-tools tunudan-settings tunudan-edition-mint; do
    cp "$ROOT"/out/debs/${p}_*.deb rootfs/tmp/tunudan-debs/
done
# Écran de choix du bureau (session live uniquement)
install -Dm755 "$ROOT/mint/live/tunudan-installer" rootfs/usr/lib/tunudan/live/tunudan-installer
echo cinnamon > rootfs/tmp/live-desktop

cat > rootfs/tmp/tunudan-chroot.sh <<'CHROOT'
#!/bin/sh
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends /tmp/tunudan-debs/*.deb
apt-get install -y papirus-icon-theme fonts-inter fonts-jetbrains-mono tmate || true
# RustDesk (aide à distance) : paquet officiel, facultatif
URL=$(curl -fsSL https://api.github.com/repos/rustdesk/rustdesk/releases/latest 2>/dev/null \
      | grep -o 'https://[^"]*x86_64\.deb' | head -n1 || true)
if [ -n "$URL" ] && curl -fsSL -o /tmp/rustdesk.deb "$URL"; then
    apt-get install -y /tmp/rustdesk.deb || echo "AVERTISSEMENT : RustDesk non installé"
fi
mkdir -p /etc/tunudan
mv /tmp/live-desktop /etc/tunudan/live-desktop
sed -i 's/^nom = .*/nom = debutant/' /etc/tunudan/tunudan.conf
echo debutant > /etc/tunudan/edition
# Lanceur de l'installateur : d'abord le choix du bureau, puis Ubiquity
U=/usr/share/applications/ubiquity.desktop
if [ -f "$U" ]; then
    grep -m1 '^Exec=' "$U" | cut -d= -f2- > /usr/lib/tunudan/live/ubiquity-exec
    sed -i -e 's#^Exec=.*#Exec=/usr/lib/tunudan/live/tunudan-installer#' \
           -e 's/^Name=.*/Name=Installer Tunudan OS/' -e '/^Name\[/d' \
           -e 's/^Icon=.*/Icon=tunudan/' "$U"
fi
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/tunudan-debs /tmp/rustdesk.deb
CHROOT
chmod +x rootfs/tmp/tunudan-chroot.sh
echo "==> Ajout de Tunudan dans le système live"
chroot rootfs /tmp/tunudan-chroot.sh
rm -f rootfs/tmp/tunudan-chroot.sh rootfs/usr/sbin/policy-rc.d rootfs/etc/resolv.conf
mv rootfs/etc/resolv.conf.mint rootfs/etc/resolv.conf 2>/dev/null || true
cleanup; MOUNTS=""

# 5. Fermeture du système live -------------------------------------------------------
echo "==> Compression du système live (plusieurs minutes)"
chroot rootfs dpkg-query -W --showformat='${Package} ${Version}\n' > iso/casper/filesystem.manifest
du -sx --block-size=1 rootfs | cut -f1 > iso/casper/filesystem.size
rm -f iso/casper/filesystem.squashfs
mksquashfs rootfs iso/casper/filesystem.squashfs -comp xz -b 1M -noappend -quiet

# 6. Menus de démarrage ---------------------------------------------------------------
for f in iso/boot/grub/grub.cfg iso/boot/grub/loopback.cfg iso/isolinux/isolinux.cfg; do
    [ -f "$f" ] || continue
    sed -i -E "s/Linux Mint $MINT_VERSION [A-Za-z]+ 64-bit/$LABEL/g; s/Start Linux Mint/Demarrer $LABEL/g" "$f"
done
printf 'Tunudan OS %s Debutant (Linux Mint %s) - %s\n' "$VERSION" "$MINT_VERSION" "$(date +%Y%m%d)" > iso/.disk/info
(cd iso && find . -type f ! -name md5sum.txt ! -path './isolinux/*' ! -path './boot/grub/i386-pc/*' \
    -print0 | sort -z | xargs -0 md5sum > md5sum.txt)

# 7. Nouvelle ISO, démarrage d'origine conservé ---------------------------------------
echo "==> Écriture de l'ISO"
rm -f "$OUT_ISO"
MAP=()
for f in casper/filesystem.squashfs casper/filesystem.manifest casper/filesystem.size \
         boot/grub/grub.cfg boot/grub/loopback.cfg isolinux/isolinux.cfg .disk/info md5sum.txt; do
    [ -f "iso/$f" ] && MAP+=(-map "iso/$f" "/$f")
done
# (le nom de volume d'origine est gardé : le chargeur UEFI de Mint peut le chercher)
xorriso -indev "$ISO" -outdev "$OUT_ISO" "${MAP[@]}" -boot_image any replay 2>&1 | tail -n 3
(cd "$OUTDIR" && sha256sum "$(basename "$OUT_ISO")" > "$(basename "$OUT_ISO").sha256")
echo "==> ISO prête : $OUT_ISO"

#!/bin/sh
# Génère les visuels et les copie dans les paquets qui en ont besoin.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT="$ROOT/branding/out"
T="$ROOT/packages/tunudan-theme/files"

if [ ! -f "$OUT/logo/tunudan-256.png" ] || [ "${FORCE:-0}" = 1 ]; then
    python3 "$ROOT/branding/generate.py" "$OUT"
fi

if [ ! -f "$OUT/wallpapers/origami/origami-grue-sombre.png" ] || [ "${FORCE:-0}" = 1 ]; then
    python3 "$ROOT/branding/wallpapers.py" "$OUT/wallpapers/origami"
fi

mkdir -p "$T/logo" "$T/kde-wallpaper/Tunudan/contents/images"
cp "$OUT"/logo/*.png "$T/logo/"
cp "$OUT/logo/tunudan-256.png" "$T/plymouth/tunudan/logo.png"
cp "$OUT/logo/tunudan-128.png" "$T/grub/tunudan/logo.png"
cp "$OUT/boot/grub-background.png" "$T/grub/tunudan/background.png"
cp "$OUT/logo/tunudan-128.png" "$T/calamares/tunudan/logo.png"
cp "$OUT/boot/splash-640x480.png" "$T/calamares/tunudan/welcome.png"
cp "$OUT/wallpapers/tunudan-sombre-1920x1080.png" "$T/kde-wallpaper/Tunudan/contents/images/1920x1080.png"
cp "$OUT/wallpapers/tunudan-sombre-3840x2160.png" "$T/kde-wallpaper/Tunudan/contents/images/3840x2160.png"
cp "$OUT/logo/tunudan-256.png" "$T/kde-wallpaper/Tunudan/contents/screenshot.png"

# Thème complet : le pack de thèmes (themes/) est embarqué dans le paquet tunudan-theme,
# dont debian/rules lance « install-system.sh --files-only ».
TH="$ROOT/themes"
rm -rf "$T/pack"
mkdir -p "$T/pack"
tar -C "$TH" --exclude=vendor --exclude=previews --exclude='build*.py' \
    --exclude=__pycache__ --exclude='.build-*' -cf - . | tar -C "$T/pack" -xf -
echo "Visuels prêts."

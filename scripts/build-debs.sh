#!/bin/sh
# Construit tous les paquets tunudan-* et les dépose dans out/debs/.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
DEST="$ROOT/out/debs"
"$ROOT/scripts/prepare-branding.sh"
mkdir -p "$DEST"
rm -f "$DEST"/*.deb
BUILD=$(mktemp -d)
trap 'rm -rf "$BUILD"' EXIT
for pkg in "$ROOT"/packages/*/; do
    name=$(basename "$pkg")
    echo "==> $name"
    cp -a "$pkg" "$BUILD/$name"
    (cd "$BUILD/$name" && dpkg-buildpackage -us -uc -b -tc >/dev/null)
done
mv "$BUILD"/*.deb "$DEST/"
ls -1 "$DEST"

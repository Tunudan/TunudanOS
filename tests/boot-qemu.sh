#!/bin/sh
# Démarre une ISO dans QEMU (UEFI si OVMF est présent) et prend une capture
# d'écran après 90 s pour vérifier que le bureau ou la console apparaît.
#   tests/boot-qemu.sh debutant [--headless]   (minimal | debutant | avance | expert)
#   QEMU_MEM=2048 tests/boot-qemu.sh …       (mémoire de la VM en Mo, 4096 par défaut)
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
EDITION="${1:-debutant}"
HEADLESS="${2:-}"   # lu avant « set -- », qui remplace les arguments
ISO=$(find "$ROOT/out/iso" -name "tunudan-os-$EDITION-*.iso" | sort | tail -n1)
[ -n "$ISO" ] || { echo "Aucune ISO pour $EDITION dans out/iso (make iso EDITION=$EDITION)"; exit 1; }
OVMF=""
for f in /usr/share/OVMF/OVMF_CODE.fd /usr/share/edk2/x64/OVMF_CODE.4m.fd /usr/share/ovmf/OVMF.fd; do
    [ -f "$f" ] && OVMF="$f" && break
done
ACCEL="-accel tcg"
[ -w /dev/kvm ] && ACCEL="-enable-kvm -cpu host"
VGA=std
qemu-system-x86_64 -device help 2>/dev/null | grep -q '"virtio-vga"' && VGA=virtio
# shellcheck disable=SC2086 # ACCEL contient plusieurs options
set -- -m "${QEMU_MEM:-4096}" -smp 2 $ACCEL -cdrom "$ISO" -boot d -vga $VGA -monitor unix:/tmp/tunudan-qemu.sock,server,nowait
[ -n "$OVMF" ] && set -- "$@" -drive if=pflash,format=raw,readonly=on,file="$OVMF"
if [ "$HEADLESS" = "--headless" ] || [ -z "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]; then
    qemu-system-x86_64 "$@" -display none &
    PID=$!
    sleep 90
    kill -0 "$PID" 2>/dev/null || { echo "QEMU s'est arrêté avant la capture" >&2; exit 1; }
    echo "screendump /tmp/tunudan-$EDITION.ppm" | socat - UNIX-CONNECT:/tmp/tunudan-qemu.sock || true
    kill "$PID" 2>/dev/null || true
    echo "Capture : /tmp/tunudan-$EDITION.ppm"
else
    exec qemu-system-x86_64 "$@"
fi

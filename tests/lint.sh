#!/bin/sh
# Vérifications rapides sans build complet : shell, Python, XML, JSON, KDL.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
fail=0
step() { printf '\n== %s\n' "$1"; }

step "shellcheck"
export LC_ALL=C.UTF-8
# (les hooks écrits en Python sont vérifiés plus bas)
find . -path ./out -prune -o -path ./packages/tunudan-theme/files/pack -prune -o -type f \
    \( -name '*.sh' -o -name '*.hook.chroot' \) -print \
    | while read -r f; do head -n1 "$f" | grep -q python || echo "$f"; done \
    | xargs shellcheck -S warning -x || fail=1
shellcheck -S warning -x packages/tunudan-tools/src/tunudan-update-root \
    packages/tunudan-tools/src/install-desktop packages/tunudan-tools/src/tunudan-desktop \
    themes/system/tunudan-theme themes/system/55tunudan-xdg themes/system/tunudan-xdg.sh \
    packages/*/debian/postinst packages/*/debian/prerm packages/*/debian/postrm packages/*/debian/preinst \
    debian-live/common/live-config/* \
    arch/expert/airootfs/usr/local/bin/tunudan-niri-session \
    arch/expert/airootfs/usr/local/bin/tunudan-install || fail=1

step "Python"
python3 -m py_compile packages/tunudan-tools/src/tunudan-help \
    packages/tunudan-tools/src/tunudan-welcome packages/tunudan-tools/src/tunudan-update \
    packages/tunudan-tools/src/tunudan_common.py branding/generate.py \
    mint/live/tunudan-installer debian-live/editions/avance/hooks/0250-calamares-desktop.hook.chroot \
    themes/icons/build_icons.py themes/cursors/build_cursors.py || fail=1

step "YAML (Calamares)"
if python3 -c "import yaml" 2>/dev/null; then
    find debian-live -name '*.conf' -path '*calamares*' -exec \
        python3 -c "import sys,yaml; [yaml.safe_load(open(f)) for f in sys.argv[1:]]" {} + || fail=1
else
    echo "(PyYAML absent)"
fi

step "Schémas GSettings"
if command -v glib-compile-schemas >/dev/null 2>&1; then
    t=$(mktemp -d)
    cp /usr/share/glib-2.0/schemas/*.xml "$t/" 2>/dev/null || true
    cp themes/system/zz-tunudan.gschema.override "$t/"
    glib-compile-schemas --dry-run "$t" || fail=1
    rm -rf "$t"
fi

step "XML (xfconf, polkit)"
find packages themes/system \( -name '*.xml' -o -name '*.policy' \) -exec \
    python3 -c "import sys,xml.dom.minidom as m; [m.parse(f) for f in sys.argv[1:]]" {} + || fail=1

step "JSON"
find packages arch themes/plasma -name '*.json' -exec \
    python3 -c "import sys,json; [json.load(open(f)) for f in sys.argv[1:]]" {} + || fail=1

step "KDL (niri)"
if python3 -c "import kdl" 2>/dev/null; then
    python3 -c "import kdl,sys; kdl.parse(open(sys.argv[1]).read())" \
        arch/expert/airootfs/etc/skel/.config/niri/config.kdl || fail=1
else
    echo "(kdl-py absent : pip install kdl-py ; sous Arch : niri validate)"
fi
if command -v niri >/dev/null 2>&1; then
    niri validate -c arch/expert/airootfs/etc/skel/.config/niri/config.kdl || fail=1
fi

if [ "$fail" = 0 ]; then
    printf '\nTout est bon.\n'
else
    printf '\nDes erreurs ont été trouvées.\n'
    exit 1
fi

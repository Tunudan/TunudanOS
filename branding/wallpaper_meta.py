#!/usr/bin/env python3
"""Métadonnées des fonds origami : paires jour/nuit pour GNOME et KDE Plasma.

    python3 branding/wallpaper_meta.py <dossier_files_du_paquet>      (paquet Debian)
    python3 branding/wallpaper_meta.py --user <dossier_fonds> <data>   (installation utilisateur)
"""
import json
import os
import sys

MOTIFS = [("grue", "Grue"), ("envolee", "Envolée"), ("sommets", "Sommets"),
          ("miura", "Miura-ori"), ("eventail", "Éventail")]


def gnome_xml(wall_dir):
    items = []
    for slug, name in MOTIFS:
        items.append(f"""  <wallpaper deleted="false">
    <name>Tunudan — {name}</name>
    <filename>{wall_dir}/origami-{slug}-clair.png</filename>
    <filename-dark>{wall_dir}/origami-{slug}-sombre.png</filename-dark>
    <options>zoom</options>
    <shade_type>solid</shade_type>
    <pcolor>#F5F1EA</pcolor>
    <scolor>#0D0D0D</scolor>
  </wallpaper>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">\n<wallpapers>\n'
            + "\n".join(items) + "\n</wallpapers>\n")


def kde_packages(dest, wall_dir, link=True):
    """Un paquet de fond Plasma par motif : images/ (clair) et images_dark/ (sombre)."""
    for slug, name in MOTIFS:
        root = os.path.join(dest, f"Tunudan-{slug.capitalize()}")
        for sub, variant in (("images", "clair"), ("images_dark", "sombre")):
            d = os.path.join(root, "contents", sub)
            os.makedirs(d, exist_ok=True)
            target = os.path.join(wall_dir, f"origami-{slug}-{variant}.png")
            f = os.path.join(d, "3840x2160.png")
            if os.path.lexists(f):
                os.remove(f)
            os.symlink(target, f)
        with open(os.path.join(root, "metadata.json"), "w", encoding="utf-8") as fh:
            json.dump({"KPlugin": {"Authors": [{"Name": "Tunudan", "Email": "contact@tunudan.fr"}],
                                   "Id": f"Tunudan-{slug.capitalize()}",
                                   "License": "CC-BY-SA-4.0",
                                   "Name": f"Tunudan — {name}"}}, fh, ensure_ascii=False, indent=4)


def main():
    if sys.argv[1] == "--user":
        wall_dir, data = sys.argv[2], sys.argv[3]
        os.makedirs(os.path.join(data, "gnome-background-properties"), exist_ok=True)
        with open(os.path.join(data, "gnome-background-properties", "tunudan-origami.xml"), "w",
                  encoding="utf-8") as f:
            f.write(gnome_xml(wall_dir))
        kde_packages(os.path.join(data, "wallpapers"), wall_dir)
        return
    files = sys.argv[1]
    sys_dir = "/usr/share/backgrounds/tunudan/origami"
    os.makedirs(os.path.join(files, "gnome-bg"), exist_ok=True)
    with open(os.path.join(files, "gnome-bg", "tunudan-origami.xml"), "w", encoding="utf-8") as f:
        f.write(gnome_xml(sys_dir))
    kde_packages(os.path.join(files, "kde-origami"), sys_dir)


if __name__ == "__main__":
    main()

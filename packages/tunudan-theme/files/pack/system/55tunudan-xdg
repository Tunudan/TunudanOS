# shellcheck shell=sh
# Tunudan : réglages par défaut (Xfce, KDE, LXQt) — surchargés par ceux de chaque utilisateur
case ":${XDG_CONFIG_DIRS:-/etc/xdg}:" in
    *:/etc/xdg/tunudan:*) ;;
    *) XDG_CONFIG_DIRS="/etc/xdg/tunudan:${XDG_CONFIG_DIRS:-/etc/xdg}"; export XDG_CONFIG_DIRS ;;
esac

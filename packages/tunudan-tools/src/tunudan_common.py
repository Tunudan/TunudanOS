"""Fonctions partagées par les outils Tunudan OS."""
import configparser
import os
import shutil
import subprocess

CONF_PATH = "/etc/tunudan/tunudan.conf"
STATE_DIR = os.path.join(os.environ.get("XDG_CONFIG_HOME",
                                        os.path.expanduser("~/.config")), "tunudan")
ORANGE = "#FF6B1A"


def conf() -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read(CONF_PATH, encoding="utf-8")
    return cfg


def get(section: str, key: str, default: str = "") -> str:
    return conf().get(section, key, fallback=default).strip() or default


def has_display() -> bool:
    return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def gtk_available() -> bool:
    if not has_display():
        return False
    try:
        import gi  # noqa: F401
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk  # noqa: F401
        return True
    except (ImportError, ValueError):
        return False


def desktop() -> str:
    d = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if "xfce" in d:
        return "xfce"
    if "kde" in d or "plasma" in d:
        return "kde"
    if "niri" in d:
        return "niri"
    return d or "console"


def run(cmd, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, capture_output=True, **kw)


def which(name: str) -> bool:
    return shutil.which(name) is not None


def state_file(name: str) -> str:
    os.makedirs(STATE_DIR, exist_ok=True)
    return os.path.join(STATE_DIR, name)


def apply_css(Gtk, Gdk) -> None:
    css = f"""
    window, assistant {{ background-color: #1C1C1E; color: #F5F1EA; }}
    .tunudan-title {{ font-size: 26px; font-weight: 800; color: {ORANGE}; }}
    .tunudan-big {{ font-size: 20px; }}
    .tunudan-id {{ font-size: 40px; font-weight: 800; letter-spacing: 4px; color: {ORANGE}; }}
    button.tunudan-cta {{ background-image: none; background-color: {ORANGE};
        color: #0D0D0D; font-size: 20px; font-weight: 700; padding: 18px 28px;
        border-radius: 12px; border: none; }}
    button.tunudan-cta:hover {{ background-color: #FF9A5C; }}
    """
    provider = Gtk.CssProvider()
    provider.load_from_data(css.encode())
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

-- Thème Tunudan — généré par themes/build.py, ne pas modifier à la main
-- Hyprland 0.55 et plus (configuration Lua).
-- Chargé depuis ~/.config/hypr/hyprland.lua par : require("tunudan")

hl.config({
  general = {
    gaps_in = 6,
    gaps_out = 14,
    border_size = 2,
    col = {
      active_border = { colors = { "rgba(ff6b1aff)", "rgba(ff9a5cff)" }, angle = 45 },
      inactive_border = "rgba(2a2a2cff)",
    },
  },
  decoration = {
    rounding = 12,
    active_opacity = 1.0,
    inactive_opacity = 0.96,
    blur = { enabled = true, size = 6, passes = 2 },
    shadow = { enabled = true, range = 20, render_power = 3, color = "rgba(00000099)" },
  },
  misc = {
    disable_hyprland_logo = true,
    force_default_wallpaper = 0,
    background_color = "rgba(0d0d0dff)",
  },
})

hl.env("XCURSOR_SIZE", "24")
hl.env("XCURSOR_THEME", "Tunudan-cursors")
hl.env("QT_QPA_PLATFORMTHEME", "qt6ct")

hl.on("hyprland.start", function()
  hl.exec_cmd("hyprpaper")
  hl.exec_cmd("waybar -c ~/.config/waybar/tunudan-hyprland.jsonc -s ~/.config/waybar/tunudan.css")
  hl.exec_cmd("mako --config ~/.config/mako/tunudan")
end)

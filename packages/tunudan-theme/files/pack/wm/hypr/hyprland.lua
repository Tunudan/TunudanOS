-- Tunudan OS — configuration Hyprland complète (0.55 et plus, Lua, clavier AZERTY)
-- Couleurs, fond et barre : ~/.config/hypr/tunudan.lua
local terminal = "kitty"
local menu = "fuzzel"
local mainMod = "SUPER"

hl.monitor({ output = "", mode = "preferred", position = "auto", scale = 1 })

hl.config({
  input = {
    kb_layout = "fr",
    numlock_by_default = true,
    follow_mouse = 1,
    touchpad = { natural_scroll = true },
  },
  dwindle = { preserve_split = true },
})

hl.curve("tunudan", { type = "bezier", points = { {0.23, 1}, {0.32, 1} } })
hl.animation({ leaf = "global", enabled = true, speed = 8, bezier = "tunudan" })
hl.animation({ leaf = "windowsIn", enabled = true, speed = 5, bezier = "tunudan", style = "popin 85%" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 5, bezier = "tunudan", style = "slide" })

hl.on("hyprland.start", function()
  hl.exec_cmd("nm-applet --indicator")
  hl.exec_cmd("hypridle")
end)

hl.bind(mainMod .. " + Return", hl.dsp.exec_cmd(terminal))
hl.bind(mainMod .. " + D", hl.dsp.exec_cmd(menu))
hl.bind(mainMod .. " + E", hl.dsp.exec_cmd("xdg-open " .. os.getenv("HOME")))
hl.bind(mainMod .. " + F1", hl.dsp.exec_cmd("tunudan-help"))
hl.bind(mainMod .. " + Q", hl.dsp.window.close())
hl.bind(mainMod .. " + V", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mainMod .. " + SHIFT + E", hl.dsp.exec_cmd("hyprctl dispatch 'hl.dsp.exit()'"))

for _, d in ipairs({ "left", "right", "up", "down" }) do
  hl.bind(mainMod .. " + " .. d, hl.dsp.focus({ direction = d }))
end

-- Espaces de travail : touches & é " ' ( - è _ ç à (codes clavier 10 à 19)
for i = 1, 10 do
  local key = "code:" .. (9 + i)
  hl.bind(mainMod .. " + " .. key, hl.dsp.focus({ workspace = i }))
  hl.bind(mainMod .. " + SHIFT + " .. key, hl.dsp.window.move({ workspace = i }))
end
hl.bind(mainMod .. " + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
hl.bind(mainMod .. " + mouse_up", hl.dsp.focus({ workspace = "e-1" }))
hl.bind(mainMod .. " + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind(mainMod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"), { locked = true, repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-"), { locked = true, repeating = true })
hl.bind("XF86AudioMute", hl.dsp.exec_cmd("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"), { locked = true })
hl.bind("XF86MonBrightnessUp", hl.dsp.exec_cmd("brightnessctl set 5%+"), { locked = true, repeating = true })
hl.bind("XF86MonBrightnessDown", hl.dsp.exec_cmd("brightnessctl set 5%-"), { locked = true, repeating = true })

require("tunudan")

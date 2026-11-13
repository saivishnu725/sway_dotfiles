# Desktop dotfiles

A gradual, reproducible Sway desktop using KDE applications, NetworkManager, and pavucontrol. Configuration changes and explanations are saved in Git.

## Current setup

- CachyOS with Plasma available as a fallback; Sway 1.12 is installed with a login-session entry.
- The Sway starter config is [sway/config](sway/config), linked at `~/.config/sway/config`. Its comments explain each setting and shortcut.
- COSMIC Terminal, Dolphin, Firefox, Wofi, NetworkManager, `nm-connection-editor`, and pavucontrol were found installed.
- The older [niri config](niri/config.kdl) remains in Git for reference. The user removed its link and uninstalled niri.
- The Sway session still needs an interactive test. NetworkManager service status could not be checked in the restricted environment; run `systemctl status NetworkManager` and `nmcli general status` locally.

## Sway basics

Touchpad tap-to-click is enabled via `input type:touchpad` and `tap enabled` in the config. Change `enabled` to `disabled` to turn it off.

Choose **Sway** at the login screen; choose **Plasma** to return. Save work before logging out. Super means the Windows/logo key. The configuration uses separate lines beginning with `#` for comments, `set` to define a variable, and `bindsym` to connect a key combination to a command. `exec` launches a program. Edit either the repository file or its symlink: they refer to the same file. Use Super+Shift+C to reload after editing.

- Super+T: COSMIC Terminal; Super+D: Wofi; Super+E: Dolphin; Super+B: Firefox.
- The keyboard calculator key opens KDE Kalk in a floating window. This assumes the key reports `XF86Calculator` and Kalk reports `org.kde.kalk` as its Wayland app ID; test both in the session.
- Super+N: connection editor; Super+A: pavucontrol. The editor manages saved connections; it is not a network tray applet.
- Super+arrows: focus a window; add Shift to move it. Super+Q closes it.
- Super+1–9 or 0: select workspace 1–10; add Shift to move the focused window there.
- Super+H or Super+V: split the focused container horizontally or vertically for subsequent windows. Super+W selects tabs, Super+S stacking, and Super+Shift+S returns to split layout.
- Super+F toggles fullscreen; Super+Shift+F or Super+Shift+Space toggles floating. Hold Super while dragging with the left mouse button to move, or the right button to resize.
- Super+Escape or Lock in the [Power] menu starts swaylock.
- The [Power] panel button opens a menu for lock, logout, reboot, and shutdown; logout, reboot, and shutdown ask for confirmation.
- Super+Shift+E asks before logging out. The top bar shows workspaces and the date/time; click the clock to open Calindori as a floating calendar window.
- The panel shows CPU usage, RAM usage, and download/upload rates to the left of Mute. CPU is sampled over the previous second; RAM uses total minus available memory. Network rates sum all non-loopback interfaces, including VPNs and virtual interfaces, so traffic can be counted more than once. Rates are bytes per second (KiB/s or MiB/s).
- Panel buttons **Mute**, **Prev**, **Play/Pause**, and **Next** control the default audio output and MPRIS-compatible media players. Prev and Next change tracks; they do not seek within a track.

The clock uses [sway/clock.py](sway/clock.py): it sends the time and buttons to swaybar and launches commands on a left click. The media buttons use `playerctl`; Mute uses the same audio helper as the keyboard key. If multiple players are open, playerctl chooses an available player. The `for_window` rule in the Sway config requests a 500 × 600 floating window; adjust those numbers to change its size. The rule depends on Calindori reporting `org.kde.calindori` as its Wayland app ID and should be checked in the session.

Swaylock is installed and manual locking has been tested. No idle or suspend locking is configured.

Notifications use Mako, configured in [mako/config](mako/config) and started by Sway at login. The user confirmed notifications work. On a new CachyOS installation, install it with `sudo pacman -S mako`, then test with `notify-send "Test notification" "Mako is working"`. The config controls position, timeout, margin, and width; each line is explained in the file.

Hardware volume-up, volume-down, speaker-mute, and microphone-mute keys use `wpctl` from WirePlumber. Volume changes in 5% steps and increases are capped at 100%. These bindings also work while locked. Each hardware-key action shows the resulting level or mute state through [sway/audio.py](sway/audio.py); Mako groups these notifications and dismisses them after 1.5 seconds. Changes made directly in other applications do not invoke this helper. Reload Sway with Super+Shift+C after editing them; use pavucontrol (Super+A) for detailed audio settings. Test the keys on your keyboard.

### Wallpaper rotation

[sway/wallpaper.py](sway/wallpaper.py) cycles through image files in `~/Pictures/Wallpaper` in filename order every 15 minutes (900 seconds), using Sway's `fill` mode. Change `DIRECTORY` or `INTERVAL_SECONDS` in the script to customize it. It rescans the folder on each change; if the folder is empty, it waits and checks again. The images themselves remain outside this repository.

Install the required background renderer on CachyOS with `sudo pacman -S swaybg`. The script starts once when Sway starts; after installing swaybg, log out and back into Sway to start it. For a single fixed wallpaper, leave just one image in the folder. Rotation needs an interactive test.

This starter does not configure idle handling or portal integration. Test the session and decide which features to add next.

## Reproduce

Install Sway, COSMIC Terminal, Dolphin, Firefox, Wofi, NetworkManager, the NetworkManager connection editor, Kalk, pavucontrol, Calindori, swaylock, Mako, libnotify, WirePlumber, playerctl, swaybg, and Python 3 using your distribution's packages. Ensure NetworkManager is running. Package names may differ. Clone the repository, then from its root:

```sh
sway --validate --config "$PWD/sway/config"
mkdir -p ~/.config/sway ~/.config/mako
ln -s "$PWD/sway/config" ~/.config/sway/config
ln -s "$PWD/sway/clock.py" ~/.config/sway/clock.py
ln -s "$PWD/sway/audio.py" ~/.config/sway/audio.py
ln -s "$PWD/sway/wallpaper.py" ~/.config/sway/wallpaper.py
ln -s "$PWD/mako/config" ~/.config/mako/config
```

Inspect and back up existing `~/.config/sway/config`, `~/.config/sway/clock.py`, `~/.config/sway/audio.py`, `~/.config/sway/wallpaper.py`, and `~/.config/mako/config` files before linking; do not overwrite it blindly. The link uses the clone's absolute path, so recreate it if the repository moves. Keep credentials and NetworkManager connection profiles out of Git.

A searchable shortcut overview is planned for later, once the main setup is mostly complete.

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
- Super+N: connection editor; Super+A: pavucontrol. The editor manages saved connections; it is not a network tray applet.
- Super+arrows: focus a window; add Shift to move it. Super+Q closes it.
- Super+1–9 or 0: select workspace 1–10; add Shift to move the focused window there.
- Super+H or Super+V: split the focused container horizontally or vertically for subsequent windows. Super+W selects tabs, Super+S stacking, and Super+Shift+S returns to split layout.
- Super+F toggles fullscreen; Super+Shift+F or Super+Shift+Space toggles floating. Hold Super while dragging with the left mouse button to move, or the right button to resize.
- Super+Shift+L or the [Lock] button in the top bar starts swaylock. Install `swaylock` first; see below.
- Super+Shift+E asks before logging out. The top bar shows workspaces and the date/time; click the clock to open Calindori as a floating calendar window.

The clock uses [sway/clock.py](sway/clock.py): it sends the time to swaybar and launches Calindori on a left click. The `for_window` rule in the Sway config requests a 500 × 600 floating window; adjust those numbers to change its size. The rule depends on Calindori reporting `org.kde.calindori` as its Wayland app ID and should be checked in the session.

Swaylock is installed and manual locking has been tested. No idle or suspend locking is configured.

Notifications use Mako, configured in [mako/config](mako/config) and started by Sway at login. Install it on CachyOS with `sudo pacman -S mako`; sudo required a password during setup, so installation is still needed. Log out and back in to start it, then test with `notify-send "Test notification" "Mako is working"`. Alternatively, start `mako` once from a terminal in the current Sway session. The config controls position, timeout, margin, and width; each line is explained in the file.

This starter does not configure idle handling, wallpaper, audio keys, or portal integration. Test the session and decide which features to add next.

## Reproduce

Install Sway, COSMIC Terminal, Dolphin, Firefox, Wofi, NetworkManager, the NetworkManager connection editor, pavucontrol, Calindori, swaylock, Mako, libnotify, and Python 3 using your distribution's packages. Ensure NetworkManager is running. Package names may differ. Clone the repository, then from its root:

```sh
sway --validate --config "$PWD/sway/config"
mkdir -p ~/.config/sway ~/.config/mako
ln -s "$PWD/sway/config" ~/.config/sway/config
ln -s "$PWD/sway/clock.py" ~/.config/sway/clock.py
ln -s "$PWD/mako/config" ~/.config/mako/config
```

Inspect and back up existing `~/.config/sway/config` `~/.config/sway/clock.py`, and `~/.config/mako/config` files before linking; do not overwrite it blindly. The link uses the clone's absolute path, so recreate it if the repository moves. Keep credentials and NetworkManager connection profiles out of Git.

A searchable shortcut overview is planned for later, once the main setup is mostly complete.

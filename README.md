# Desktop dotfiles

A gradual, reproducible Sway desktop using KDE applications, NetworkManager, and pavucontrol. Configuration changes and explanations are saved in Git.

## Current setup

- CachyOS with Plasma available as a fallback; Sway 1.12 is installed with a login-session entry.
- The Sway starter config is [sway/config](sway/config), linked at `~/.config/sway/config`. Its comments explain each setting and shortcut.
- Konsole, Dolphin, Firefox, Wofi, NetworkManager, `nm-connection-editor`, and pavucontrol were found installed.
- The older [niri config](niri/config.kdl) remains in Git for reference. The user removed its link and uninstalled niri.
- The Sway session still needs an interactive test. NetworkManager service status could not be checked in the restricted environment; run `systemctl status NetworkManager` and `nmcli general status` locally.

## Sway basics

Touchpad tap-to-click is enabled via `input type:touchpad` and `tap enabled` in the config. Change `enabled` to `disabled` to turn it off.

Choose **Sway** at the login screen; choose **Plasma** to return. Save work before logging out. Super means the Windows/logo key. The configuration uses `#` for comments, `set` to define a variable, and `bindsym` to connect a key combination to a command. `exec` launches a program. Edit either the repository file or its symlink: they refer to the same file. Use Super+Shift+C to reload after editing.

- Super+T: Konsole; Super+D: Wofi; Super+E: Dolphin; Super+B: Firefox.
- Super+N: connection editor; Super+A: pavucontrol. The editor manages saved connections; it is not a network tray applet.
- Super+arrows: focus a window; add Shift to move it. Super+Q closes it.
- Super+1–9 or 0: select workspace 1–10; add Shift to move the focused window there.
- Super+H or Super+V: split the focused container horizontally or vertically for subsequent windows. Super+W selects tabs, Super+S stacking, and Super+Shift+S returns to split layout.
- Super+F toggles fullscreen; Super+Shift+Space toggles floating. Hold Super while dragging with the left mouse button to move, or the right button to resize.
- Super+Shift+E asks before logging out. The top bar shows workspaces and the date/time.

This starter does not configure a screen locker, idle handling, notifications, wallpaper, audio keys, or portal integration. Test the session and decide which features to add next.

## Reproduce

Install Sway, Konsole, Dolphin, Firefox, Wofi, NetworkManager, the NetworkManager connection editor, and pavucontrol using your distribution's packages. Ensure NetworkManager is running. Package names may differ. Clone the repository, then from its root:

```sh
sway --validate --config "$PWD/sway/config"
mkdir -p ~/.config/sway
ln -s "$PWD/sway/config" ~/.config/sway/config
```

Inspect and back up an existing `~/.config/sway/config` before linking; do not overwrite it blindly. The link uses the clone's absolute path, so recreate it if the repository moves. Keep credentials and NetworkManager connection profiles out of Git.

# Desktop dotfiles

A gradual, reproducible Sway desktop using KDE applications, NetworkManager, and pavucontrol. Configuration changes and explanations are saved in Git.

## Current setup

- CachyOS with Plasma available as a fallback; Sway 1.12 is installed with a login-session entry.
- The Sway starter config is [sway/config](sway/config), linked at `~/.config/sway/config`. Its comments explain each setting and shortcut.
- COSMIC Terminal, Dolphin, Firefox, Wofi, NetworkManager, `nm-connection-editor`, and pavucontrol were found installed.
- The older [niri config](niri/config.kdl) remains in Git for reference. The user removed its link and uninstalled niri.
- The Sway session still needs an interactive test. NetworkManager service status could not be checked in the restricted environment; run `systemctl status NetworkManager` and `nmcli general status` locally.

## KDE app appearance

Dolphin, Kalk, and Calindori launched from the configured Sway shortcuts or clock button request the KDE Qt platform theme using `QT_QPA_PLATFORMTHEME=kde`. This is a limited experiment to see whether they pick up the existing Breeze Dark settings; applications launched elsewhere are unaffected. Reload Sway, close these apps fully, and reopen them to test. Remove `env QT_QPA_PLATFORMTHEME=kde` from the bindings (and the equivalent `env` arguments in `sway/clock.py`) to undo it.

## Sway appearance

The focused window and active workspace use the muted rose accent `#B76E79`. Edit the `client.focused` and `focused_workspace` colors in `sway/config` to change it; app-specific themes are separate.

Wofi searches are case-insensitive in the configured launcher and menus.

## Sway basics

Touchpad tap-to-click is enabled via `input type:touchpad` and `tap enabled` in the config. Change `enabled` to `disabled` to turn it off.

Choose **Sway** at the login screen; choose **Plasma** to return. Save work before logging out. Super means the Windows/logo key. The configuration uses separate lines beginning with `#` for comments, `set` to define a variable, and `bindsym` to connect a key combination to a command. `exec` launches a program. Edit either the repository file or its symlink: they refer to the same file. Use Super+Shift+C to reload after editing.

- Super+Shift+/ opens a searchable shortcut overview; it reads bindings from `sway/config` and shows the configured commands. Selecting an entry closes the menu without running it. Bindings added through other included files are not listed.
- Super+Shift+V opens searchable clipboard history; selecting an item copies it back to the clipboard for pasting. Install cliphist first as described below.
- Super+T: COSMIC Terminal; Super+D: Wofi; Super+E: Dolphin; Super+B: Firefox.
- The keyboard calculator key opens KDE Kalk in a floating window. This assumes the key reports `XF86Calculator` and Kalk reports `org.kde.kalk` as its Wayland app ID; test both in the session.
- Super+S selects a screen region with Slurp, captures it with Grim, saves the original to `~/Pictures/Screenshots`, and opens Swappy for annotation, copying, or saving an edited version. Install Swappy on CachyOS with `sudo pacman -S swappy`; Grim and Slurp are also required. Swappy saves annotated images to `~/Pictures/Screenshots`; Copy places the image on the clipboard, and either action closes the editor. Test Copy by pasting into an image-capable app. Escape cancels selection. The shortcut replaces the old stacking shortcut, now Super+Ctrl+S. OBS Studio is installed for optional recording.
- Super+N: connection editor; Super+A: pavucontrol. The editor manages saved connections; it is not a network tray applet.
- Super+arrows: focus a window; add Shift to move it. Super+Q closes it.
- Super+1–9 or 0: select workspace 1–10; add Shift to move the focused window there.
- Super+H or Super+V: split the focused container horizontally or vertically for subsequent windows. Super+W selects tabs, Super+Ctrl+S selects stacking, and Super+Shift+S returns to split layout.
- Super+F toggles fullscreen; Super+Shift+F or Super+Shift+Space toggles floating. Hold Super while dragging with the left mouse button to move, or the right button to resize.
- Super+Escape or Lock in the [⏻ Power] menu starts swaylock.
- Click the battery indicator at the far right for battery status, an estimated remaining or charging time when UPower provides one, and available power profiles. Select Battery saver, Balanced, or Performance to change it; unavailable profiles are omitted. Estimates vary with load and may be unavailable.
- The [⏻ Power] panel button opens a menu for lock, logout, reboot, and shutdown; logout, reboot, and shutdown ask for confirmation.
- Super+Shift+E asks before logging out. The top bar shows workspaces and the date/time; click the clock to open Calindori as a floating calendar window.
- The panel shows CPU usage, RAM usage, and download/upload rates to the left of Mute. The panel refreshes every two seconds, and CPU is sampled over that interval; RAM uses total minus available memory. Network rates sum all non-loopback interfaces, including VPNs and virtual interfaces, so traffic can be counted more than once. Rates are bytes per second (KiB/s or MiB/s).
- Click **DND Off/On** in the panel to toggle Mako’s Do Not Disturb mode. While on, notification popups are hidden. The indicator refreshes every two seconds.
- Panel buttons **Mute**, **Prev**, **Play/Pause**, and **Next** control the default audio output and MPRIS-compatible media players. Prev and Next change tracks; they do not seek within a track.

The clock uses [sway/clock.py](sway/clock.py): it sends the time and buttons to swaybar and launches commands on a left click. The media buttons use `playerctl`; Mute uses the same audio helper as the keyboard key. If multiple players are open, playerctl chooses an available player. The `for_window` rule in the Sway config requests a 500 × 600 floating window; adjust those numbers to change its size. The rule depends on Calindori reporting `org.kde.calindori` as its Wayland app ID and should be checked in the session.

Swaylock is installed and manual locking has been tested. No idle or suspend locking is configured.

Notifications use Mako, configured in [mako/config](mako/config) and started by Sway at login. The user confirmed notifications work. On a new CachyOS installation, install it with `sudo pacman -S mako`, then test with `notify-send "Test notification" "Mako is working"`. The config controls position, timeout, margin, and width; each line is explained in the file.

Hardware volume-up, volume-down, speaker-mute, and microphone-mute keys use `wpctl` from WirePlumber. Volume changes in 5% steps and increases are capped at 100%. These bindings also work while locked. Each hardware-key action shows the resulting level or mute state through [sway/audio.py](sway/audio.py); Mako groups these notifications and dismisses them after 1.5 seconds. Changes made directly in other applications do not invoke this helper. Reload Sway with Super+Shift+C after editing them; use pavucontrol (Super+A) for detailed audio settings. Test the keys on your keyboard.

### Wallpaper rotation

[sway/wallpaper.py](sway/wallpaper.py) cycles through image files in `~/Pictures/Wallpaper` in filename order every 15 minutes (900 seconds), using swaybg's `fill` mode. The background renderer stays running across Sway config reloads. Change `DIRECTORY` or `INTERVAL_SECONDS` in the script to customize it. It rescans the folder on each change; if the folder is empty, it waits and checks again. The images themselves remain outside this repository.

Install the required background renderer on CachyOS with `sudo pacman -S swaybg`. The script starts once when Sway starts; after installing swaybg, log out and back into Sway to start it. For a single fixed wallpaper, leave just one image in the folder. Rotation needs an interactive test.

Sway includes `/etc/sway/config.d/*` for distribution session integration. On this CachyOS installation, it exports the Sway display and desktop to user services so the installed GTK portal can provide file dialogs. Log out and back in after adding it, then test an upload or Save As dialog. For screen sharing, the distribution Sway portal configuration selects `xdg-desktop-portal-wlr` for ScreenCast and Screenshot, while keeping GTK for file dialogs. Install the missing backend and selection tool on CachyOS with `sudo pacman -S xdg-desktop-portal-wlr slurp`, then log out and back into Sway. Test by sharing a screen in a Wayland-capable browser or application. The installed portal supports screen and window selection. [xdg-desktop-portal-wlr/config](xdg-desktop-portal-wlr/config) uses Wofi to show available sources; the choices depend on what the requesting app supports. Restart the portal or log out and back in after changes. Screen and window selection were confirmed working in Firefox and the installed Discord app after restarting the portal with the Sway session environment. If the chooser stops appearing after switching desktop sessions, run the following from a Sway terminal, then retry:

```sh
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=sway SWAYSOCK
systemctl --user restart xdg-desktop-portal
```

This starter does not configure idle handling. Test the session and decide which features to add next.

## External displays

Install `wl-mirror` and `wdisplays` on CachyOS with `sudo pacman -S wl-mirror wdisplays`. Press Super+P for Extend, Mirror laptop, Laptop only, External only, or graphical display settings. The menu detects the laptop screen and lets you choose an external output if more than one is present. Extend places the chosen display to the right; the two "only" modes disable the other selected display. Mirror uses a fullscreen `wl-mirror` window, not native hardware mirroring; choosing another menu mode stops the mirror started by this menu. These settings are temporary and have not yet been tested with a connected monitor or projector. The graphical settings tool can adjust resolution, scale, and arrangement. To inspect outputs manually, run `swaymsg -t get_outputs`. If a display becomes unusable, reconnect it or use `swaymsg output <name> enable` from a terminal.

## Clipboard history

Install `cliphist` on CachyOS with `sudo pacman -S cliphist`, then log out and back into Sway to start the text and image watchers. Copy something and press Super+Shift+V to select it; paste normally afterward. Clipboard history is stored locally and can contain passwords or other sensitive copied data. Clear it with `cliphist wipe`; it does not clear your current clipboard. The watchers and shortcut are documented in `sway/config`.

## Reproduce

Install Sway, COSMIC Terminal, Dolphin, Firefox, Wofi, NetworkManager, the NetworkManager connection editor, Kalk, Grim, Slurp, Swappy, wl-clipboard, cliphist, pavucontrol, Calindori, swaylock, Mako, libnotify, WirePlumber, playerctl, swaybg, wl-mirror, wdisplays, upower, power-profiles-daemon, xdg-desktop-portal, xdg-desktop-portal-gtk, xdg-desktop-portal-wlr, slurp, and Python 3 using your distribution's packages. Ensure NetworkManager is running. Package names may differ. Clone the repository, then from its root:

```sh
sway --validate --config "$PWD/sway/config"
mkdir -p ~/.config/sway ~/.config/mako ~/.config/swappy ~/.config/xdg-desktop-portal-wlr
ln -s "$PWD/sway/config" ~/.config/sway/config
ln -s "$PWD/sway/clock.py" ~/.config/sway/clock.py
ln -s "$PWD/sway/audio.py" ~/.config/sway/audio.py
ln -s "$PWD/sway/displays.py" ~/.config/sway/displays.py
ln -s "$PWD/sway/shortcuts.py" ~/.config/sway/shortcuts.py
ln -s "$PWD/sway/screenshot.sh" ~/.config/sway/screenshot.sh
ln -s "$PWD/sway/battery.py" ~/.config/sway/battery.py
ln -s "$PWD/sway/wallpaper.py" ~/.config/sway/wallpaper.py
ln -s "$PWD/mako/config" ~/.config/mako/config
ln -s "$PWD/swappy/config" ~/.config/swappy/config
ln -s "$PWD/xdg-desktop-portal-wlr/config" ~/.config/xdg-desktop-portal-wlr/config
```

Inspect and back up existing `~/.config/sway/config`, `~/.config/sway/clock.py`, `~/.config/sway/audio.py`, `~/.config/sway/displays.py`, `~/.config/sway/shortcuts.py`, `~/.config/sway/screenshot.sh`, `~/.config/sway/battery.py`, `~/.config/sway/wallpaper.py`, `~/.config/mako/config`, `~/.config/swappy/config`, and `~/.config/xdg-desktop-portal-wlr/config` files before linking; do not overwrite it blindly. The link uses the clone's absolute path, so recreate it if the repository moves. Keep credentials and NetworkManager connection profiles out of Git.

## Zsh and Neovim

`~/.zshrc` links to [zsh/zshrc](zsh/zshrc). The original was backed up beside it with a `.backup-<timestamp>` suffix. The Tailscale exit-node aliases live in the private `~/local_aliases.sh`, which the tracked file sources if present; it is not in Git. Shell history and `.zshenv` are also not tracked. Review backups before deleting them.

Zsh uses Oh My Zsh with the `dst` theme, its archlinux, gh, git, rust, and sudo plugins, plus `zsh-autosuggestions` and `zsh-syntax-highlighting` in the Oh My Zsh custom plugins directory. It also uses Rust's `$HOME/.cargo/env`, optionally loads NVM, and sets Android SDK paths. Install or adjust those dependencies and paths on another machine; `.zshenv` separately sources Cargo on this machine. The configuration contains aliases and functions for Git, Cargo, editing and compiling C. The tracked file can be checked with `zsh -n zsh/zshrc`.

Neovim's `~/.config/nvim/init.lua` and `lazy-lock.json` link to [nvim](nvim/); timestamped backups are beside the originals. The config enables line numbers, four-space indentation, clipboard integration, `clangd` LSP, C/Lua Tree-sitter, and Git integration. It expects lazy.nvim at Neovim's data directory, the locked plugins, `clangd`, C/Lua parsers, and GCC for its C run mapping. The lockfile records plugin revisions but does not install lazy.nvim or the plugins by itself. The C run mapping expects an `output` directory next to the file. Plugin bootstrap and a clean-machine test are still needed for full reproduction.

To recreate these links after cloning, inspect and back up any existing files first. From the repository root:

```sh
mkdir -p ~/.config/nvim
ln -s "$PWD/zsh/zshrc" ~/.zshrc
ln -s "$PWD/nvim/init.lua" ~/.config/nvim/init.lua
ln -s "$PWD/nvim/lazy-lock.json" ~/.config/nvim/lazy-lock.json
```

Recreate `~/local_aliases.sh` separately for machine-specific aliases if needed. For example, use `alias tailexit="sudo tailscale set --exit-node=<your-node> --accept-routes"` and `alias tailexitno="sudo tailscale set --exit-node="`; replace `<your-node>` with your own node address. Never put shell history, credentials, or private local settings in Git.

## License

This project is licensed under the **GNU General Public License v2.0**.

See the `LICENSE` file for details.

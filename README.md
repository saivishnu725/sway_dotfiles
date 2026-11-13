# Desktop dotfiles

A gradual, reproducible niri desktop using existing KDE applications, NetworkManager, and pavucontrol. Keep changes small, explain them here, and save milestones in Git.

## Current setup

Observed on 2026-11-13 on CachyOS, with KDE running on Wayland:

- niri 26.04 is installed and has a Wayland login-session entry; KDE remains available.
- NetworkManager, pavucontrol, Plasma Network Management, Dolphin, Konsole, Wofi, and `nm-connection-editor` are installed.
- [niri/config.kdl](niri/config.kdl) is linked to `~/.config/niri/config.kdl`. It is a minimal starter, not a complete desktop shell.
- `~/.config/pavucontrol.ini` already exists and has not been copied or linked.
- NetworkManager's live service status could not be checked from the restricted environment. Run `systemctl status NetworkManager` locally; use `nmcli general status` for its connection state.

## Using and editing niri

Choose **niri** at the login screen to test it; choose **Plasma** there to return to KDE. Save your work before logging out. The configuration has been syntax-validated, but the session and applications still need an interactive test.

Edit `niri/config.kdl` in this repository (or the linked `~/.config/niri/config.kdl`); both paths refer to the same file. Comments next to the settings explain each line. Niri watches its config and normally reloads changes automatically. Check syntax with:

```sh
niri validate -c ~/Programs/dotfiles/niri/config.kdl
```

The config uses KDL: `//` starts a comment, `{ ... }` groups settings or an action, and quoted text is a string. `Mod` is the Super/Windows key in a normal session (Alt in a nested niri window). The `layout` block controls gaps and initial column width. The `binds` block maps each key combination to the action in braces; `spawn` starts the named program, with each argument quoted separately. `repeat=false` prevents repeated actions when holding the key. Settings not listed use niri's defaults.

Useful starter shortcuts (all use Super unless stated otherwise):

- `T`: Konsole; `D`: Wofi app launcher; `E`: Dolphin; `B`: Firefox.
- `N`: NetworkManager connection editor; `A`: pavucontrol.
- Arrow keys: focus windows or columns; Ctrl + left/right: move a column.
- Page Up/Down: switch workspaces; `O`: overview; `Q`: close window.
- `R`: change column width; `F`: maximize column; Shift + `F`: fullscreen; `V`: toggle floating.
- Shift + `/`: shortcut overlay; Print: screenshot; Shift + `E`: logout confirmation.

The connection editor manages saved connections; it is not a network tray applet. A bar, notifications, screen locking, wallpaper, audio keys, portals, and other session integration have not yet been configured or tested.

## Reproduce on another machine

Install niri, Konsole, Dolphin, Wofi, NetworkManager, `nm-connection-editor`, and pavucontrol using the target distribution's packages. Ensure NetworkManager is enabled and running according to that distribution's instructions. Package names may differ.

Clone this repository and inspect any existing config before linking. If `~/.config/niri/config.kdl` already exists, back it up first. From the repository root, create the link only when that destination is absent:

```sh
mkdir -p ~/.config/niri
ln -s "$PWD/niri/config.kdl" ~/.config/niri/config.kdl
niri validate -c ~/.config/niri/config.kdl
```

The link uses the clone's absolute path, so recreate it if the repository moves. Review the config and test the niri session before relying on it.

## Principles and next steps

- Preserve KDE as a fallback while testing niri.
- Track selected configuration deliberately, and back up existing files before replacing them with links.
- Keep credentials, NetworkManager connection profiles, and other secrets out of Git.
- Test the starter session and decide which desktop features to add next; document and commit each working milestone.

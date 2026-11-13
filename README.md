# Desktop dotfiles

A gradual, reproducible setup for a niri desktop using existing KDE applications, NetworkManager, and pavucontrol. Changes to the desktop and this documentation should be made in small, reviewable steps and saved in Git.

## Current baseline

Observed on 2026-11-13:

- CachyOS (Arch-based), currently running a KDE Wayland session.
- NetworkManager, pavucontrol, Plasma Network Management, Dolphin, Konsole, and the KDE desktop portal are installed.
- niri was not found in the installed packages or available Wayland sessions.
- `~/.config/pavucontrol.ini` exists. Its contents have not been copied or linked.
- NetworkManager service status could not be checked from the restricted environment; verify it on the machine with `systemctl status NetworkManager`.

No desktop configuration has been moved, linked, or changed yet.

## Approach

1. Keep the existing KDE session available while building and testing niri separately.
2. Install and configure niri in small steps; document package names, commands, and decisions here as they are verified.
3. Track only deliberately selected configuration files. Before replacing an existing file with a symlink, preserve a backup and check for private or machine-specific data.
4. Keep credentials, network connection profiles, and other secrets out of Git. NetworkManager connection profiles are system-managed and may contain secrets.
5. Commit working milestones so changes can be reviewed and reproduced.

## Reproducing this setup

This repository currently records the baseline only. Installation, configuration, and symlink instructions will be added as they are implemented and tested. Do not replace existing configuration files without first inspecting and backing them up.

## Next steps

- Verify NetworkManager is running and identify the KDE tools and desktop features needed in the niri session.
- Install niri and establish a minimal, testable configuration while retaining the KDE login option.
- Add selected configuration files and explicit, backup-aware linking instructions once their contents and intended ownership are understood.

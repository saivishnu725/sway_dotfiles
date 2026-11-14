#!/usr/bin/env bash
# Link the tracked desktop and shell configuration into the current home.
set -euo pipefail
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)

if [[ ${1:-} == --help ]]; then
    printf 'Usage: %s [--backup]\n\nWithout --backup, existing files are left untouched.\n' "$0"
    exit 0
fi
if [[ $# -gt 1 || ( $# -eq 1 && $1 != --backup ) ]]; then
    printf 'Usage: %s [--backup]\n' "$0" >&2
    exit 2
fi

missing=()
for command in sway cosmic-term dolphin firefox wofi nm-connection-editor kalk grim slurp swappy wl-copy cliphist pavucontrol calindori swaylock mako notify-send wpctl playerctl swaybg wl-mirror wdisplays upower python3 zsh nvim; do
    command -v "$command" >/dev/null 2>&1 || missing+=("$command")
done
if ((${#missing[@]})); then
    printf 'Commands not found (install the features you need): %s\n' "${missing[*]}"
fi
printf '%s\n' 'Also check the portal backends, NetworkManager, power-profiles-daemon, Oh My Zsh, and Neovim dependencies described in README.md.'

link() {
    local source=$1 destination=$2 backup index
    if [[ -L $destination && $(readlink -- "$destination") == "$source" ]]; then
        printf 'Already linked: %s\n' "$destination"
        return
    fi
    if [[ -e $destination || -L $destination ]]; then
        if [[ ${backup_existing:-} != yes ]]; then
            printf 'Skipped existing path: %s (use --backup to replace it)\n' "$destination"
            skipped=1
            return
        fi
        backup="${destination}.backup-$(date +%Y%m%d-%H%M%S)"
        index=0
        while [[ -e $backup || -L $backup ]]; do
            ((index+=1))
            backup="${destination}.backup-$(date +%Y%m%d-%H%M%S)-$index"
        done
        mv -- "$destination" "$backup"
        printf 'Backed up: %s -> %s\n' "$destination" "$backup"
    fi
    mkdir -p -- "$(dirname -- "$destination")"
    ln -s -- "$source" "$destination"
    printf 'Linked: %s -> %s\n' "$destination" "$source"
}

backup_existing=no
[[ ${1:-} == --backup ]] && backup_existing=yes
skipped=0
for file in config clock.py audio.py displays.py shortcuts.py screenshot.sh battery.py wallpaper.py; do
    link "$repo/sway/$file" "$HOME/.config/sway/$file"
done
for name in mako swappy xdg-desktop-portal-wlr; do
    link "$repo/$name/config" "$HOME/.config/$name/config"
done
link "$repo/zsh/zshrc" "$HOME/.zshrc"
for file in init.lua lazy-lock.json; do
    link "$repo/nvim/$file" "$HOME/.config/nvim/$file"
done
if ((skipped)); then
    printf '%s\n' 'Some paths were skipped. Review them and rerun with --backup if desired.'
    exit 1
fi

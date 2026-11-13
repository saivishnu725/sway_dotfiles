#!/bin/sh
# Save a selected region, then open a copy in Swappy for annotation.
set -eu
if ! command -v swappy >/dev/null 2>&1; then
    notify-send 'Screenshot' 'Install swappy to annotate screenshots.'
    exit 1
fi
region=$(slurp) || exit 0
[ -n "$region" ] || exit 0
# Create the folder if needed; mktemp prevents overwriting a prior capture.
directory="$HOME/Pictures/Screenshots"
mkdir -p "$directory"
image=$(mktemp "$directory/Screenshot-$(date +%Y-%m-%d_%H-%M-%S)-XXXXXX.png")
if ! grim -g "$region" "$image"; then
    rm -f "$image"
    notify-send 'Screenshot' 'Capture failed.'
    exit 1
fi
notify-send 'Screenshot saved' "$image"
# Swappy can save the edited result separately; the original remains on disk.
swappy -f "$image"

#!/bin/sh
# Select a region, capture it, and open it in Swappy for annotation and saving.
set -eu
if ! command -v swappy >/dev/null 2>&1; then
    notify-send 'Screenshot' 'Install swappy to annotate screenshots.'
    exit 1
fi
# A cancelled selection exits without creating a screenshot.
region=$(slurp) || exit 0
[ -n "$region" ] || exit 0
image=$(mktemp "${TMPDIR:-/tmp}/sway-screenshot-XXXXXX.png")
trap 'rm -f "$image"' EXIT HUP INT TERM
grim -g "$region" "$image"
swappy -f "$image"

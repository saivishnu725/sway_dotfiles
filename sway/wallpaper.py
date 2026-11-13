#!/usr/bin/env python3
"""Rotate wallpapers in a directory using Sway's output background command."""
import json
from pathlib import Path
import subprocess
import sys
import time

# Change this directory or interval (in seconds) to suit your preferences.
DIRECTORY = Path.home() / 'Pictures' / 'Wallpaper'
INTERVAL_SECONDS = 900
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

index = 0
while True:
    # Re-read the folder each time, so added and removed images are picked up.
    try:
        images = sorted((path for path in DIRECTORY.iterdir()
                         if path.is_file() and path.suffix.lower() in EXTENSIONS),
                        key=lambda path: path.name.lower())
    except OSError as error:
        print(f'Cannot read wallpaper directory: {error}', file=sys.stderr)
        images = []
    if images:
        image = images[index % len(images)]
        # Quote the path for Sway, including paths with spaces or quotes.
        command = f'output * bg {json.dumps(str(image), ensure_ascii=False)} fill'
        try:
            subprocess.run(['swaymsg', command], check=True, stdout=subprocess.DEVNULL)
        except (OSError, subprocess.CalledProcessError) as error:
            print(f'Could not set wallpaper: {error}', file=sys.stderr)
        index += 1
    time.sleep(INTERVAL_SECONDS)

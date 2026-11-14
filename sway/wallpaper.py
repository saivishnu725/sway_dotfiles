#!/usr/bin/env python3
"""Rotate wallpapers in a directory using a persistent swaybg process."""
from pathlib import Path
import subprocess
import signal
import threading
import sys
import time

# Change this directory or interval (in seconds) to suit your preferences.
DIRECTORY = Path.home() / 'Pictures' / 'Wallpaper'
INTERVAL_SECONDS = 900
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}

# SIGUSR1 wakes the loop and resets the interval after the next image.
advance = threading.Event()
signal.signal(signal.SIGUSR1, lambda _signum, _frame: advance.set())

index = 0
background = None
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
        # Start the new background before stopping the old one to avoid flicker.
        try:
            new_background = subprocess.Popen(['swaybg', '-i', str(image), '-m', 'fill'])
            time.sleep(1)
            if new_background.poll() is None:
                if background and background.poll() is None:
                    background.terminate()
                    background.wait()
                background = new_background
            else:
                print(f'Could not display wallpaper: {image}', file=sys.stderr)
        except OSError as error:
            print(f'Could not start swaybg: {error}', file=sys.stderr)
        index += 1
    advance.wait(INTERVAL_SECONDS)
    advance.clear()

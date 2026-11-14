#!/usr/bin/env python3
"""Rotate wallpapers; --next advances the running session's rotation."""
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time

# Change this directory or interval (in seconds) to suit your preferences.
DIRECTORY = Path.home() / 'Pictures' / 'Wallpaper'
INTERVAL_SECONDS = 900
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
PID_FILE = Path(os.environ.get('XDG_RUNTIME_DIR', '/tmp')) / 'sway-wallpaper-rotation.pid'

if sys.argv[1:] == ['--next']:
    try:
        pid = int(PID_FILE.read_text())
        args = Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
        if not any(Path(os.fsdecode(arg)).name == 'wallpaper.py' for arg in args):
            raise ValueError('Wallpaper process no longer matches')
        os.kill(pid, signal.SIGUSR1)
    except (OSError, ValueError) as error:
        subprocess.run(['notify-send', 'Wallpaper', 'Rotation is not running; log back into Sway.'], check=False)
        sys.exit(f'Could not advance wallpaper: {error}')
    sys.exit(0)

# A signal wakes the existing timer; the next wait starts a fresh 15 minutes.
advance = threading.Event()
signal.signal(signal.SIGUSR1, lambda _signum, _frame: advance.set())
PID_FILE.write_text(str(os.getpid()))
index = 0
background = None
while True:
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

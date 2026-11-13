#!/usr/bin/env python3
"""Search the key bindings declared in this repository's Sway config."""
from pathlib import Path
import shlex
import subprocess

config = Path.home() / '.config/sway/config'
entries = []
for line in config.read_text().splitlines():
    line = line.strip()
    if not line.startswith('bindsym '):
        continue
    try:
        parts = shlex.split(line)
    except ValueError:
        continue
    # Skip binding flags such as --locked before the key combination.
    index = 1
    while index < len(parts) and parts[index].startswith('--'):
        index += 1
    if index + 1 >= len(parts):
        continue
    keys = parts[index].replace('$mod', 'Super')
    action = ' '.join(parts[index + 1:])
    entries.append(f'{keys}  —  {action}')
# Selecting an entry simply closes the overview; it does not run the action.
subprocess.run(['wofi', '--dmenu', '--insensitive', '--prompt', 'Search shortcuts'],
               input='\n'.join(entries), text=True, stdout=subprocess.DEVNULL, check=False)

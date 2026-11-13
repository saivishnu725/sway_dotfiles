#!/usr/bin/env python3
"""Show clickable desktop controls and a clock using the i3bar status protocol."""
import datetime
import json
from pathlib import Path
import subprocess
import sys
import threading
import time


def handle_clicks():
    # swaybar sends click events as a stream of comma-separated JSON objects.
    for line in sys.stdin:
        line = line.strip().lstrip(',')
        if not line or line in ('[', ']'):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        # Button 1 is the left mouse button (or a normal touchpad tap).
        if event.get('button') != 1:
            continue
        # Each named panel block maps to a command and its arguments.
        commands = {
            'clock': ['calindori'],
            'power': ['sh', '-c', "choice=$(printf 'Lock\nLogout\nReboot\nShutdown\n' | wofi --dmenu --prompt Power); case \"$choice\" in Lock) swaylock ;; Logout) swaynag -t warning -m 'Log out of Sway?' -B 'Logout' 'swaymsg exit' ;; Reboot) swaynag -t warning -m 'Reboot this computer?' -B 'Reboot' 'systemctl reboot' ;; Shutdown) swaynag -t warning -m 'Shut down this computer?' -B 'Shutdown' 'systemctl poweroff' ;; esac"],
            'mute': [sys.executable, '-u', str(Path.home() / '.config/sway/audio.py'), 'mute'],
            'previous': ['playerctl', 'previous'],
            'play': ['playerctl', 'play-pause'],
            'next': ['playerctl', 'next'],
        }
        command = commands.get(event.get('name'))
        if command:
            try:
                subprocess.Popen(command, start_new_session=True)
            except OSError as error:
                print(f'Could not launch {command[0]}: {error}', file=sys.stderr)


# Announce the protocol and request click events, then start the status array.
print(json.dumps({'version': 1, 'click_events': True}), flush=True)
print('[', flush=True)
threading.Thread(target=handle_clicks, daemon=True).start()
while True:
    # A named block lets the click handler identify the clock.
    clock = {'name': 'clock', 'full_text': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    # Labels are kept as text so they work without a special icon font.
    controls = [
        {'name': 'mute', 'full_text': '[Mute]'},
        {'name': 'previous', 'full_text': '[Prev]'},
        {'name': 'play', 'full_text': '[Play/Pause]'},
        {'name': 'next', 'full_text': '[Next]'},
        {'name': 'power', 'full_text': '[Power]'},
    ]
    print(json.dumps([*controls, clock]) + ',', flush=True)
    time.sleep(1)

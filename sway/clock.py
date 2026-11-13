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
            'dnd': ['makoctl', 'mode', '-t', 'do-not-disturb'],
            'clock': ['env', 'QT_QPA_PLATFORMTHEME=kde', 'calindori'],
            'battery': [sys.executable, str(Path.home() / '.config/sway/battery.py')],
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


# Read Linux counters directly, avoiding extra polling processes.
def sample():
    fields = [int(value) for value in Path('/proc/stat').read_text().splitlines()[0].split()[1:]]
    cpu_total = sum(fields[:8])  # guest time is already included in user/nice.
    cpu_idle = fields[3] + fields[4]
    memory = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        parts = line.split()
        if len(parts) >= 2:
            memory[parts[0].rstrip(':')] = int(parts[1])
    used = 100 * (memory['MemTotal'] - memory['MemAvailable']) / memory['MemTotal']
    rx = tx = 0
    for line in Path('/proc/net/dev').read_text().splitlines()[2:]:
        name, values = line.split(':', 1)
        if name.strip() != 'lo':
            counters = values.split()
            rx += int(counters[0])
            tx += int(counters[8])
    return cpu_total, cpu_idle, used, rx, tx, time.monotonic()


def rate(value):
    # Display bytes per second in human-readable binary units.
    for unit in ('B/s', 'KiB/s', 'MiB/s', 'GiB/s'):
        if value < 1024 or unit == 'GiB/s':
            return f'{value:.1f} {unit}'
        value /= 1024


# Announce the protocol and request click events, then start the status array.
print(json.dumps({'version': 1, 'click_events': True}), flush=True)
print('[', flush=True)
threading.Thread(target=handle_clicks, daemon=True).start()
previous = None
while True:
    # Rates and CPU usage compare this sample with the previous one.
    try:
        current = sample()
        cpu = '--'
        down = up = '--'
        if previous:
            total = current[0] - previous[0]
            idle = current[1] - previous[1]
            cpu = f'{max(0, min(100, 100 * (total - idle) / total)):.0f}%' if total > 0 else '--'
            elapsed = max(current[5] - previous[5], 0.001)
            down = rate(max(0, current[3] - previous[3]) / elapsed)
            up = rate(max(0, current[4] - previous[4]) / elapsed)
        previous = current
        vitals = {'name': 'vitals', 'full_text': f'CPU {cpu}  RAM {current[2]:.0f}%  Down {down}  Up {up}'}
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(f'Could not read system vitals: {error}', file=sys.stderr)
        previous = None
        vitals = {'name': 'vitals', 'full_text': 'Vitals unavailable'}
    # A named block lets the click handler identify the clock.
    clock = {'name': 'clock', 'full_text': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    # Show whether Mako's do-not-disturb mode is active.
    try:
        modes = subprocess.check_output(['makoctl', 'mode'], text=True, stderr=subprocess.DEVNULL).splitlines()
        dnd_label = '[DND On]' if 'do-not-disturb' in modes else '[DND Off]'
    except (OSError, subprocess.CalledProcessError):
        dnd_label = '[DND ?]'
    # Labels are kept as text so they work without a special icon font.
    controls = [
        {'name': 'dnd', 'full_text': dnd_label},
        {'name': 'mute', 'full_text': '[Mute]'},
        {'name': 'previous', 'full_text': '[Prev]'},
        {'name': 'play', 'full_text': '[Play/Pause]'},
        {'name': 'next', 'full_text': '[Next]'},
        {'name': 'power', 'full_text': '[⏻ Power]'},
    ]
    # Read the first present battery's percentage and charging state from sysfs.
    battery_text = 'Battery --'
    for battery in sorted(Path('/sys/class/power_supply').glob('*')):
        try:
            if (battery / 'type').read_text().strip() != 'Battery':
                continue
            capacity = (battery / 'capacity').read_text().strip()
            state = (battery / 'status').read_text().strip()
            battery_text = f'Battery {capacity}% ({state})'
            break
        except OSError:
            continue
    battery_block = {'name': 'battery', 'full_text': battery_text}
    print(json.dumps([vitals, *controls, clock, battery_block]) + ',', flush=True)
    # Refresh the panel every two seconds.
    time.sleep(2)

#!/usr/bin/env python3
"""Adjust audio with wpctl and show its resulting level in a notification."""
import re
import subprocess
import sys

# The argument selected by a Sway binding chooses the action and audio device.
actions = {
    'up': ('@DEFAULT_AUDIO_SINK@', ['set-volume', '-l', '1.0', '@DEFAULT_AUDIO_SINK@', '5%+'], 'Volume'),
    'down': ('@DEFAULT_AUDIO_SINK@', ['set-volume', '@DEFAULT_AUDIO_SINK@', '5%-'], 'Volume'),
    'mute': ('@DEFAULT_AUDIO_SINK@', ['set-mute', '@DEFAULT_AUDIO_SINK@', 'toggle'], 'Volume'),
    'mic': ('@DEFAULT_AUDIO_SOURCE@', ['set-mute', '@DEFAULT_AUDIO_SOURCE@', 'toggle'], 'Microphone'),
}
if len(sys.argv) != 2 or sys.argv[1] not in actions:
    sys.exit('Usage: audio.py {up|down|mute|mic}')
device, command, label = actions[sys.argv[1]]
try:
    # Only report success after wpctl has changed the requested device.
    subprocess.run(['wpctl', *command], check=True)
    output = subprocess.check_output(['wpctl', 'get-volume', device], text=True)
    match = re.search(r'Volume:\s*([0-9.]+)', output)
    if not match:
        sys.exit('Could not read audio volume')
    percentage = round(float(match.group(1)) * 100)
    state = f'{percentage}% (muted)' if '[MUTED]' in output else f'{percentage}%'
    # Mako groups these notifications so rapid key presses do not fill the screen.
    subprocess.run(['notify-send', '-a', 'Sway audio', label, state], check=True)
except (OSError, subprocess.CalledProcessError) as error:
    sys.exit(f'Audio control failed: {error}')

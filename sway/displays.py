#!/usr/bin/env python3
"""Choose a temporary Sway display layout for a laptop and external monitor."""
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys


def choose(prompt, options):
    result = subprocess.run(['wofi', '--dmenu', '--insensitive', '--prompt', prompt],
                            input='\n'.join(options), text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else ''


def notify(message):
    subprocess.run(['notify-send', 'Displays', message], check=False)


def command(text):
    result = subprocess.run(['swaymsg', '-r', text], text=True, capture_output=True, check=True)
    for reply in json.loads(result.stdout):
        if not reply.get('success'):
            raise RuntimeError(reply.get('error', 'Sway rejected the command'))


def quoted(name):
    return json.dumps(name, ensure_ascii=False)


def stop_mirror():
    # Only stop a mirror started by this menu, after checking its process identity.
    path = Path(os.environ.get('XDG_RUNTIME_DIR', '/tmp')) / 'sway-display-mirror.pid'
    try:
        pid = int(path.read_text())
        args = Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')
        if args and Path(os.fsdecode(args[0])).name == 'wl-mirror' and b'sway-display-menu-mirror' in args:
            os.kill(pid, signal.SIGTERM)
    except (OSError, ValueError):
        pass
    path.unlink(missing_ok=True)


try:
    action = choose('Display mode', ['Extend', 'Mirror laptop', 'Laptop only', 'External only', 'Display settings'])
    if not action:
        sys.exit(0)
    if action == 'Display settings':
        if not shutil.which('wdisplays'):
            raise RuntimeError('Install wdisplays first')
        subprocess.Popen(['wdisplays'], start_new_session=True)
        sys.exit(0)
    outputs = json.loads(subprocess.check_output(['swaymsg', '-t', 'get_outputs', '-r'], text=True))
    internal = next((o for o in outputs if o['name'].startswith(('eDP-', 'LVDS-', 'DSI-'))), None)
    if not internal:
        raise RuntimeError('No laptop display detected')
    external = [o for o in outputs if o['name'] != internal['name'] and not o['name'].startswith('HEADLESS-')]
    if not external:
        raise RuntimeError('No external display detected')
    selected = external[0]['name'] if len(external) == 1 else choose('External display', [o['name'] for o in external])
    if not selected or selected not in [o['name'] for o in external]:
        sys.exit(0)
    laptop = internal['name']
    # Enable the destination first, so a failed operation never deliberately disables both.
    if action in ('Extend', 'Mirror laptop', 'Laptop only'):
        command(f'output {quoted(laptop)} enable')
    if action in ('Extend', 'Mirror laptop', 'External only'):
        command(f'output {quoted(selected)} enable')
    if action == 'Mirror laptop' and not shutil.which('wl-mirror'):
        raise RuntimeError('Install wl-mirror first')
    stop_mirror()
    if action in ('Extend', 'Mirror laptop'):
        outputs = json.loads(subprocess.check_output(['swaymsg', '-t', 'get_outputs', '-r'], text=True))
        rect = next(o['rect'] for o in outputs if o['name'] == laptop)
        command(f'output {quoted(selected)} position {rect["x"] + rect["width"]} {rect["y"]}')
        if action == 'Mirror laptop':
            process = subprocess.Popen(['wl-mirror', '--title', 'sway-display-menu-mirror',
                                        '--fullscreen-output', selected, laptop], start_new_session=True)
            (Path(os.environ.get('XDG_RUNTIME_DIR', '/tmp')) / 'sway-display-mirror.pid').write_text(str(process.pid))
    elif action == 'Laptop only':
        command(f'output {quoted(selected)} disable')
    elif action == 'External only':
        command(f'output {quoted(laptop)} disable')
except (OSError, RuntimeError, subprocess.CalledProcessError, ValueError, KeyError, StopIteration) as error:
    notify(str(error))
    sys.exit(1)

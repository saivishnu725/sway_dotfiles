#!/usr/bin/env python3
"""Show battery details and switch among available power profiles."""
import re
import subprocess
import sys


def run(*args):
    return subprocess.run(args, text=True, capture_output=True, check=True).stdout


try:
    # UPower supplies an estimate when the battery and daemon can calculate one.
    paths = run('upower', '-e').splitlines()
    battery = next((path for path in paths if '/battery_' in path), None)
    details = run('upower', '-i', battery) if battery else ''
    def field(name):
        match = re.search(r'^\s*' + re.escape(name) + r':\s*(.+)$', details, re.MULTILINE)
        return match.group(1).strip() if match else None
    status = field('state') or 'unknown'
    estimate = field('time to empty') or field('time to full') or 'unavailable'
    label = 'Time to full' if status == 'charging' else 'Time remaining'
    profiles = run('powerprofilesctl', 'list')
    available = re.findall(r'^\s*[* ]?\s*(power-saver|balanced|performance):', profiles, re.MULTILINE)
    active = run('powerprofilesctl', 'get').strip()
    names = {'power-saver': 'Battery saver', 'balanced': 'Balanced', 'performance': 'Performance'}
    lines = [f'Battery: {field("percentage") or "unavailable"} ({status})',
             f'{label}: {estimate}', f'Current: {names.get(active, active)}',
             *[names[profile] for profile in available]]
    choice = subprocess.run(['wofi', '--dmenu', '--prompt', 'Battery / power profile'],
                            input='\n'.join(lines), text=True, capture_output=True).stdout.strip()
    selected = next((profile for profile in available if names[profile] == choice), None)
    if selected:
        result = subprocess.run(['powerprofilesctl', 'set', selected], text=True, capture_output=True)
        message = f'Power profile: {names[selected]}' if result.returncode == 0 else f'Could not change profile: {result.stderr.strip()}'
        subprocess.run(['notify-send', 'Power profile', message], check=False)
except (OSError, subprocess.CalledProcessError) as error:
    print(f'Battery menu error: {error}', file=sys.stderr)
    subprocess.run(['notify-send', 'Battery menu', 'Could not read battery or power profiles.'], check=False)
    sys.exit(1)

#!/usr/bin/env python3
"""Change the laptop backlight and notify the resulting brightness."""
import subprocess
import sys

if len(sys.argv) != 2 or sys.argv[1] not in ('up', 'down'):
    sys.exit('Usage: brightness.py {up|down}')
step = '+5%' if sys.argv[1] == 'up' else '5%-'
base = ['brightnessctl', '--class=backlight']
try:
    # Keep at least one hardware brightness unit when dimming.
    subprocess.run([*base, '--min-value=1', 'set', step], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    value = int(subprocess.check_output([*base, 'get'], text=True).strip())
    maximum = int(subprocess.check_output([*base, 'max'], text=True).strip())
    percentage = round(100 * value / maximum)
    subprocess.run(['notify-send', '-a', 'Sway brightness', 'Brightness', f'{percentage}%'], check=True)
except (OSError, ValueError, ZeroDivisionError, subprocess.CalledProcessError) as error:
    detail = getattr(error, 'stderr', None) or str(error)
    print(f'Brightness control failed: {detail}', file=sys.stderr)
    subprocess.run(['notify-send', 'Brightness control failed', detail.strip()], check=False)
    sys.exit(1)

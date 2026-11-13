#!/usr/bin/env python3
"""Show a clickable clock in swaybar using its i3bar status protocol."""
import datetime
import json
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
        if event.get('name') == 'clock' and event.get('button') == 1:
            try:
                subprocess.Popen(['calindori'], start_new_session=True)
            except OSError as error:
                print(f'Could not open Calindori: {error}', file=sys.stderr)


# Announce the protocol and request click events, then start the status array.
print(json.dumps({'version': 1, 'click_events': True}), flush=True)
print('[', flush=True)
threading.Thread(target=handle_clicks, daemon=True).start()
while True:
    # A named block lets the click handler identify the clock.
    clock = {'name': 'clock', 'full_text': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    print(json.dumps([clock]) + ',', flush=True)
    time.sleep(1)

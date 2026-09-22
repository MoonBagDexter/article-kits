"""Shoots every art page in kits/<slug>/art/*.html to kits/<slug>/<name>.png at its exact size.

    python tools/render.py <slug>

The size is read from the page's first <svg width=".." height="..">. Headless Chrome
waits a few seconds so web fonts load before the shot.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

kit = ROOT / 'kits' / sys.argv[1]
for page in sorted((kit / 'art').glob('*.html')):
    m = re.search(r'<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"', page.read_text(encoding='utf-8'))
    if not m:
        print(f'skip {page.name}: no <svg width height>')
        continue
    w, h = m.groups()
    out = kit / f'{page.stem}.png'
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--virtual-time-budget=6000', f'--window-size={w},{h}', f'--screenshot={out}', page.as_uri()],
                   capture_output=True)
    print(f'{out.name} {w}x{h}')

"""Builds each article picture as an HTML page in NOKPAD's look: navy dot grid, pixel phone, LCD-green
panels, Jersey 15 for anything big, Tiny5 for anything small. render.py shoots them to PNG.

The phone-*.png files are real screenshots of the site's phone, taken by capture.py."""

PHONE_RATIO = 1194 / 2943  # width / height of the phone screenshots

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Jersey+15&family=Tiny5&display=block" rel="stylesheet">
<style>
html,body{margin:0;padding:0;background:#0b1430;overflow:hidden}
svg{display:block}
.disp{font-family:'Jersey 15';fill:#f4f7ff}
.y{fill:#ffd21f}
.ink{font-family:'Jersey 15';fill:#43523d}
.lcd{font-family:'Tiny5';fill:#43523d}
.dim{font-family:'Tiny5';fill:#8f9cc4}
.navy{font-family:'Jersey 15';fill:#0b1430}
.wire{fill:none;stroke:#ffd21f;stroke-width:6;stroke-dasharray:12 10}
</style></head><body>'''

DEFS = '''<defs>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="2" fill="#1b2a5e"/></pattern>
<filter id="hard" x="-10%" y="-10%" width="130%" height="130%"><feDropShadow dx="14" dy="14" stdDeviation="0" flood-color="#000" flood-opacity="0.45"/></filter>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#c4ff96" stop-opacity="0.35"/><stop offset="1" stop-color="#c4ff96" stop-opacity="0"/></radialGradient>
<radialGradient id="blue" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#2a4fc0" stop-opacity="0.45"/><stop offset="1" stop-color="#2a4fc0" stop-opacity="0"/></radialGradient>
</defs>'''


def page(name, w, h, body):
    html = HEAD + (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}'
                   f'<rect width="{w}" height="{h}" fill="#0b1430"/><rect width="{w}" height="{h}" fill="url(#dots)"/>'
                   f'{"".join(body)}</svg></body></html>')
    open(name, 'w', encoding='utf-8').write(html)


def phone(state, x, y, h):
    w = h * PHONE_RATIO
    return f'<image href="phone-{state}.png" x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#hard)"/>'


def panel(x, y, w, h):
    """The site's side panels: paper LCD inside a black then blue shell, hard shadow."""
    return (f'<rect x="{x - 12 + 14}" y="{y - 12 + 14}" width="{w + 24}" height="{h + 24}" fill="#000" fill-opacity="0.45"/>'
            f'<rect x="{x - 12}" y="{y - 12}" width="{w + 24}" height="{h + 24}" fill="#1d3a8a"/>'
            f'<rect x="{x - 6}" y="{y - 6}" width="{w + 12}" height="{h + 12}" fill="#060b1f"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#c7f0d8"/>')


def keycap(x, y, w, h, big, small='', lit=False):
    """A pixel key like the site's numbered steps: light face, navy outline, bevel."""
    face = '#ffd21f' if lit else '#d8deea'
    out = (f'<rect x="{x - 4}" y="{y - 4}" width="{w + 8}" height="{h + 8}" fill="#0b1430"/>'
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{face}"/>'
           f'<rect x="{x}" y="{y + h - 6}" width="{w}" height="6" fill="#8e98b3"/><rect x="{x + w - 6}" y="{y}" width="6" height="{h}" fill="#8e98b3"/>'
           f'<rect x="{x}" y="{y}" width="{w}" height="5" fill="#fff"/><rect x="{x}" y="{y}" width="5" height="{h}" fill="#fff"/>'
           f'<text class="navy" x="{x + 18}" y="{y + h * 0.72}" font-size="{h * 0.62}">{big}</text>')
    if small:
        out += f'<text class="lcd" x="{x + w - 14}" y="{y + h - 16}" font-size="{h * 0.22}" text-anchor="end" style="fill:#4a5578">{small}</text>'
    return out


def headline(text, w, y=112, size=86):
    return f'<text class="disp" x="{w / 2}" y="{y}" font-size="{size}" text-anchor="middle">{text}</text>'


def caption(text, w, y):
    return f'<text class="dim" x="{w / 2}" y="{y}" font-size="24" text-anchor="middle">{text}</text>'


# ---------------------------------------------------------------- 1 cover 2000x800
b = []
b.append('<ellipse cx="1480" cy="420" rx="420" ry="380" fill="url(#blue)"/>')
b.append('<text class="disp" x="140" y="420" font-size="270">NOKPAD</text>')
b.append('<text class="disp" x="148" y="540" font-size="92">Launch your $NOK pair</text>')
b.append('<text class="disp y" x="148" y="636" font-size="92">from a Nokia.</text>')
b.append(phone('menu', 1260, 60, 1500))
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 type it 1600x900
b = []
b.append(headline('Type your coin <tspan class="y">like a text.</tspan>', 1600))
b.append(phone('typing', 190, 165, 690))
px, py, pw, ph = 620, 190, 820, 590
b.append(panel(px, py, pw, ph))
b.append(f'<text class="ink" x="{px + 36}" y="{py + 64}" font-size="54">Three taps on 2 = C</text>')
b.append(f'<rect x="{px + 36}" y="{py + 84}" width="{pw - 72}" height="4" fill="#43523d"/>')
kx, ky = px + 40, py + 124
for i in range(3):
    b.append(keycap(kx + i * 150, ky, 118, 96, '2', 'abc', lit=(i == 2)))
    b.append(f'<text class="lcd" x="{kx + i * 150 + 59}" y="{ky + 138}" font-size="22" text-anchor="middle">{"abc"[i]}</text>')
b.append(f'<path d="M{kx + 450} {ky + 48}H{kx + 540}" stroke="#43523d" stroke-width="8"/><path d="M{kx + 536} {ky + 30}L{kx + 560} {ky + 48}L{kx + 536} {ky + 66}Z" fill="#43523d"/>')
b.append(f'<rect x="{kx + 590}" y="{ky - 4}" width="140" height="104" fill="#43523d"/>')
b.append(f'<text x="{kx + 660}" y="{ky + 82}" font-size="96" text-anchor="middle" style="font-family:\'Jersey 15\';fill:#c7f0d8">C</text>')
rows = [('1', 'Name', 'tap it out on the keys'), ('2', 'Ticker', 'the phone suggests one'), ('3', 'About it', 'a line, or skip'),
        ('4', 'Logo', 'your photo, or a pixel logo')]
for i, (n, a, c) in enumerate(rows):
    y = py + 330 + i * 64
    b.append(keycap(px + 40, y - 2, 46, 46, n))
    b.append(f'<text class="ink" x="{px + 112}" y="{y + 36}" font-size="42">{a}</text>')
    b.append(f'<text class="lcd" x="{px + 300}" y="{y + 32}" font-size="24">{c}</text>')
page('02-type.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 it rings 1600x900
b = []
b.append(headline('It rings when <tspan class="y">your coin moves.</tspan>', 1600))
b.append('<ellipse cx="335" cy="330" rx="260" ry="200" fill="url(#glow)"/>')
b.append(phone('call', 190, 165, 690))
b.append('<text class="dim" x="335" y="886" font-size="20" text-anchor="middle">demo call</text>')
alerts = [('New coin', 'the phone buzzes'), ('A trade', 'it blips'), ('Migrated', 'it rings')]
for i, (a, c) in enumerate(alerts):
    y = 200 + i * 190
    last = i == 2
    b.append(panel(660, y, 780, 140))
    if last:
        b.append(f'<rect x="660" y="{y}" width="780" height="140" fill="#e4ffd2"/>')
    b.append(f'<text class="ink" x="700" y="{y + 92}" font-size="68">{a}</text>')
    b.append(f'<text class="lcd" x="1400" y="{y + 86}" font-size="34" text-anchor="end">{c}</text>')
b.append('<text class="dim" x="1050" y="806" font-size="24" text-anchor="middle">Every coin launched here lives in Contacts, menu 2.</text>')
page('04-rings.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 closing 1600x900
b = []
b.append('<ellipse cx="420" cy="450" rx="330" ry="380" fill="url(#blue)"/>')
lh = 700
lw = lh * 457 / 1152
b.append(f'<image href="logo.png" x="{420 - lw / 2}" y="{450 - lh / 2}" width="{lw}" height="{lh}" filter="url(#hard)"/>')
b.append('<text class="disp" x="680" y="420" font-size="230">NOKPAD</text>')
b.append('<text class="disp y" x="688" y="530" font-size="96">nokpad.fun</text>')
b.append('<text class="dim" x="690" y="610" font-size="26">connecting people since 1865</text>')
page('05-close.html', 1600, 900, b)
print('built')

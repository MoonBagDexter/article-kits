"""Builds each article picture as an HTML page in the site's look. render.sh shoots them to PNG."""
import re

SHIP = "brand-marks.ts"  # copied from the loadout repo so this still rebuilds without it
src = open(SHIP, encoding='utf-8').read()
BR = {m[0]: (m[2], m[1]) for m in re.findall(r"(\w+): \{\s*label: '[^']+',\s*color: '([^']+)',\s*path: '([^']+)'", src)}

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Azeret+Mono:wght@400;500;700&family=Barlow+Semi+Condensed:wght@400;500;600;700&family=Unbounded:wght@500;600;700&display=block" rel="stylesheet">
<style>
html,body{margin:0;padding:0;background:#030303;overflow:hidden}
svg{display:block}
.disp{font-family:Unbounded;font-weight:700;fill:#f7f4ee}
.txt{font-family:'Barlow Semi Condensed';fill:#d3cdc3}
.dim{font-family:'Barlow Semi Condensed';fill:#9d978d}
.num{font-family:'Azeret Mono';font-weight:500;fill:#f7f4ee}
.gold{fill:#ffcc4d}
.cable{fill:none;stroke:#c8860d;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.cable-hi{fill:none;stroke:#f5b301;stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
.dash{fill:none;stroke:#f5b301;stroke-width:4;stroke-dasharray:3 14;stroke-linecap:round}
.ring{fill:#0f0f0f;stroke:#c8860d;stroke-width:3}
.line{fill:none;stroke:#ffcc4d;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
</style></head><body>'''

DEFS = '''<defs>
<linearGradient id="key" x1="0" y1="0" x2="0.7" y2="1"><stop offset="0" stop-color="#1c1c1c"/><stop offset="1" stop-color="#0a0a0a"/></linearGradient>
<linearGradient id="keylit" x1="0" y1="0" x2="0.7" y2="1"><stop offset="0" stop-color="#2a1f06"/><stop offset="1" stop-color="#0d0a03"/></linearGradient>
<linearGradient id="sol" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#9945ff"/><stop offset="1" stop-color="#14f195"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#f5b301" stop-opacity="0.28"/><stop offset="1" stop-color="#f5b301" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#0e0e0e" stroke-width="1"/></pattern>
<clipPath id="circ"><circle cx="0" cy="0" r="1"/></clipPath>
</defs>'''


def page(name, w, h, body, grid=True):
    bg = f'<rect width="{w}" height="{h}" fill="url(#grid)"/>' if grid else ''
    html = HEAD + f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns:xlink="http://www.w3.org/1999/xlink">{DEFS}{bg}{"".join(body)}</svg></body></html>'
    open(name, 'w', encoding='utf-8').write(html)


def logo(name, cx, cy, size):
    path, color = BR[name]
    fill = 'url(#sol)' if name == 'solana' else color
    s = size / 24
    return f'<g transform="translate({cx - size / 2} {cy - size / 2}) scale({s})"><path d="{path}" fill="{fill}"/></g>'


def key(x, y, w, h, r=14, lit=False):
    stroke = '#c8860d' if lit else '#2c2c2c'
    fill = 'url(#keylit)' if lit else 'url(#key)'
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{3 if lit else 2}"/>'
            f'<path d="M{x + r} {y + 1.5}H{x + w - r}" stroke="{"#ffd966" if lit else "#3a3a3a"}" stroke-opacity="{0.5 if lit else 0.8}" stroke-width="2"/>')


def mark(cx, cy, h, glow=True):
    w = h * 440 / 480
    g = f'<circle cx="{cx}" cy="{cy}" r="{h * 1.1}" fill="url(#glow)"/>' if glow else ''
    return g + f'<image href="logo-noglow.png" x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}"/>'


def avatar(img, cx, cy, r):
    return (f'<clipPath id="a{img}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
            f'<image href="{img}.jpg" x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" clip-path="url(#a{img})" preserveAspectRatio="xMidYMid slice"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#c8860d" stroke-width="3"/>')


# ---------------------------------------------------------------- 1 cover 2000x800
b = []
ks, gap = 108, 14
cols, rows = 16, 6
ox = (2000 - (cols * ks + (cols - 1) * gap)) / 2
oy = (800 - (rows * ks + (rows - 1) * gap)) / 2
lit = {(1, 0): 'youtube', (4, 0): 'reddit', (7, 0): 'tiktok', (10, 0): 'telegram', (13, 0): 'twitch', (15, 1): 'kick',
       (0, 2): 'tiktok', (1, 4): 'telegram', (0, 5): 'kick', (15, 3): 'solana', (14, 5): 'reddit', (15, 5): 'youtube',
       (3, 5): 'twitch', (6, 5): 'solana', (9, 5): 'tiktok', (12, 5): 'telegram', (0, 1): 'solana', (14, 2): 'tiktok'}
for c in range(cols):
    for r in range(rows):
        x, y = ox + c * (ks + gap), oy + r * (ks + gap)
        if 2 <= c <= 13 and 1 <= r <= 4:
            continue
        name = lit.get((c, r))
        b.append(key(x, y, ks, ks, 16))
        if name:
            b.append(logo(name, x + ks / 2, y + ks / 2, 44))
b.append('<ellipse cx="1000" cy="400" rx="640" ry="260" fill="url(#glow)"/>')
mh = 230
mw = mh * 440 / 480
wh = 230
ww = wh * 691 / 240
tot = mw + 30 + ww
x0 = 1000 - tot / 2
b.append(f'<image href="logo-noglow.png" x="{x0}" y="{400 - mh / 2}" width="{mw}" height="{mh}"/>')
b.append(f'<image href="wordmark-noglow.png" x="{x0 + mw + 30}" y="{400 - wh / 2 + 6}" width="{ww}" height="{wh}"/>')
page('01-cover.html', 2000, 800, b, grid=False)

# ---------------------------------------------------------------- 2 the split 1600x900
b = []
b.append('<text class="disp" x="800" y="118" font-size="54" text-anchor="middle">Set the split once. <tspan class="gold">Every fee follows it.</tspan></text>')
# coin fees in
b.append(key(90, 360, 340, 180, 18))
b.append('<text class="dim" x="120" y="410" font-size="28">Trading fees</text>')
b.append('<text class="num" x="120" y="478" font-size="46">$EXAMPLE</text>')
b.append('<text class="dim" x="120" y="518" font-size="24">every trade, forever</text>')
b.append('<path class="cable-hi" d="M430 450H640"/><path class="dash" d="M430 450H640"/>')
b.append(mark(740, 450, 190))
# branches
stops = [('tiktok', '@.tjr.him', 50, 'a TikTok gift', 'tjr', 250),
         ('twitch', 'xqc', 30, 'a tip on stream', 'xqc', 450),
         ('reddit', 'u/unipcs', 20, 'Reddit Gold', 'unipcs', 650)]
for name, handle, pct, gets, img, y in stops:
    wdt = {50: 9, 30: 7, 20: 5}[pct]
    b.append(f'<path d="M840 450 C930 450 930 {y} 1020 {y}" fill="none" stroke="#f5b301" stroke-width="{wdt}" stroke-linecap="round"/>')
    b.append(key(1020, y - 72, 480, 144, 16, lit=(pct == 50)))
    b.append(avatar(img, 1092, y, 44))
    b.append(f'<circle cx="1124" cy="{y + 32}" r="17" fill="#0f0f0f" stroke="#2c2c2c" stroke-width="2"/>' + logo(name, 1124, y + 32, 20))
    b.append(f'<text class="num" x="1160" y="{y - 8}" font-size="30">{handle}</text>')
    b.append(f'<text class="txt" x="1160" y="{y + 34}" font-size="27">gets {gets}</text>')
    b.append(f'<text class="num gold" x="1470" y="{y + 14}" font-size="46" font-weight="700" text-anchor="end">{pct}%</text>')
b.append('<text class="dim" x="800" y="830" font-size="26" text-anchor="middle">Locked at launch. Nobody can change it, us included.</text>')
page('02-split.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 where it can go 1600x900
b = []
b.append('<text class="disp" x="800" y="118" font-size="54" text-anchor="middle">Pay <tspan class="gold">anyone.</tspan> On the app they already use.</text>')
b.append(mark(330, 500, 230))
dests = [('tiktok', 'TikTok creators'), ('twitch', 'Streamers'), ('youtube', 'YouTubers'), ('kick', 'Kick streamers'),
         ('reddit', 'Reddit users'), ('telegram', 'Telegram Premium'), ('solana', 'Any wallet'), ('x', 'Your holders')]
icons = {'charity': '<path d="M0 8C-10 0 -14 -6 -14 -11C-14 -16 -10 -19 -6 -19C-3 -19 -1 -17 0 -15C1 -17 3 -19 6 -19C10 -19 14 -16 14 -11C14 -6 10 0 0 8Z"/>'}
col_x = [640, 1110]
spots = [(col_x[i // 4], 250 + (i % 4) * 160) for i in range(8)]
for cx, cy in spots[:4]:
    b.append(f'<path d="M445 500 C540 500 540 {cy} {cx} {cy}" class="cable" stroke-opacity="0.8"/>')
for (name, label), (cx, cy) in zip(dests, spots):
    b.append(key(cx - 10, cy - 60, 420, 120, 16))
    b.append(f'<circle cx="{cx + 60}" cy="{cy}" r="40" class="ring"/>')
    if name == 'x':
        b.append(f'<g transform="translate({cx + 60} {cy})" class="line"><circle cx="-9" cy="-6" r="7"/><circle cx="10" cy="-6" r="7"/><path d="M-22 16c1-8 6-12 13-12s12 4 13 12M-2 8c3-3 7-4 12-4 7 0 12 4 13 12"/></g>')
    else:
        b.append(logo(name, cx + 60, cy, 40))
    b.append(f'<text class="txt" x="{cx + 124}" y="{cy + 11}" font-size="34" font-weight="600" style="fill:#f7f4ee">{label}</text>')
b.append('<text class="dim" x="800" y="860" font-size="26" text-anchor="middle">Plus charity, gift cards, buybacks and more.</text>')
page('03-where.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 getting paid 1600x900
b = []
b.append('<text class="disp" x="800" y="118" font-size="54" text-anchor="middle">They sign up for <tspan class="gold">nothing.</tspan></text>')
y = 480
xs = [300, 800, 1300]
b.append(f'<path class="cable-hi" d="M{xs[0] + 95} {y}H{xs[1] - 95}"/><path class="dash" d="M{xs[0] + 95} {y}H{xs[1] - 95}"/>')
b.append(f'<path class="cable-hi" d="M{xs[1] + 95} {y}H{xs[2] - 95}"/><path class="dash" d="M{xs[1] + 95} {y}H{xs[2] - 95}"/>')
b.append(avatar('xqc', xs[0], y, 90))
b.append(f'<circle cx="{xs[0] + 64}" cy="{y + 64}" r="28" fill="#0f0f0f" stroke="#2c2c2c" stroke-width="2"/>' + logo('twitch', xs[0] + 64, y + 64, 30))
b.append(f'<circle cx="{xs[1]}" cy="{y}" r="90" class="ring"/>')
b.append(f'<g transform="translate({xs[1]} {y + 8})" class="line" style="stroke-width:5"><rect x="-30" y="-14" width="60" height="46" rx="6"/><path d="M-18 -14V-28A18 18 0 0 1 18 -28V-14"/><circle cx="0" cy="8" r="5"/></g>')
b.append(f'<circle cx="{xs[2]}" cy="{y}" r="90" fill="#231902" stroke="#f5b301" stroke-width="4"/><circle cx="{xs[2]}" cy="{y}" r="150" fill="url(#glow)"/>')
b.append(f'<path d="M{xs[2] - 32} {y + 2}L{xs[2] - 8} {y + 26}L{xs[2] + 36} {y - 22}" class="line" style="stroke-width:9"/>')
b.append(key(xs[2] - 95, y - 205, 190, 70, 12, lit=True))
b.append(f'<text class="num gold" x="{xs[2]}" y="{y - 158}" font-size="36" font-weight="700" text-anchor="middle">+$42.50</text>')
steps = [('Their share waits', 'in a vault tied to their handle'), ('They prove', 'the handle is theirs'), ('They get paid', 'as SOL, or the way that site pays')]
for x, (a, c) in zip(xs, steps):
    b.append(f'<text class="txt" x="{x}" y="{y + 160}" font-size="36" font-weight="700" text-anchor="middle" style="fill:#f7f4ee">{a}</text>')
    b.append(f'<text class="dim" x="{x}" y="{y + 205}" font-size="29" text-anchor="middle">{c}</text>')
page('04-paid.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 closing 1600x900
b = []
b.append('<ellipse cx="800" cy="400" rx="560" ry="260" fill="url(#glow)"/>')
mh = 240
mw = mh * 440 / 480
wh = 240
ww = wh * 691 / 240
x0 = 800 - (mw + 26 + ww) / 2
b.append(f'<image href="logo-noglow.png" x="{x0}" y="{400 - mh / 2}" width="{mw}" height="{mh}"/>')
b.append(f'<image href="wordmark-noglow.png" x="{x0 + mw + 26}" y="{400 - wh / 2 + 6}" width="{ww}" height="{wh}"/>')
b.append('<text class="num gold" x="800" y="660" font-size="46" font-weight="500" text-anchor="middle">maxpad.io</text>')
page('05-close.html', 1600, 900, b)
print('built')

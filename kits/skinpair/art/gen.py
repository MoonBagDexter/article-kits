"""Builds each article picture as an HTML page in SkinPair's look. tools/render.py shoots them to PNG.

Colours, fonts and logos come from the floatpad repo (globals.css @theme, layout.tsx, public/brand).
Skin art is from the CSGO-API dataset, copied here so this rebuilds without either source.
"""
import json

SK = json.load(open('skins.json', encoding='utf-8'))
GOLD = '#e4ae39'


def skin(name):
    s = SK[name]
    return s['file'], (GOLD if name.startswith('★') else s['color'])


HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@500;700&family=Pixelify+Sans:wght@500;600;700&display=block" rel="stylesheet">
<style>
@font-face{font-family:Figs;src:url(geist-figures-700.woff2) format('woff2');font-weight:700;unicode-range:U+24,U+30-39}
html,body{margin:0;padding:0;background:#f5e6c8;overflow:hidden}
svg{display:block}
.disp{font-family:Figs,'Pixelify Sans';font-weight:700;fill:#3b1f12}
.acc{fill:#e0741c}
.txt{font-family:Geist;fill:#6b4630}
.ink{font-family:Geist;font-weight:600;fill:#3b1f12}
.dim{font-family:Geist;fill:#85604a}
.px{font-family:Figs,'Pixelify Sans';font-weight:700}
.num{font-family:'Geist Mono';font-weight:700;fill:#3b1f12}
</style></head><body>'''

DEFS = '''<defs>
<pattern id="dots" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="9" cy="9" r="2.2" fill="#e0741c" fill-opacity="0.13"/></pattern>
<filter id="hard" x="-5%" y="-5%" width="115%" height="130%"><feDropShadow dx="3" dy="3" stdDeviation="0" flood-color="#3b1f12"/></filter>
</defs>'''

INK, WELL, LINE, SURF, BRAND, AMBER = '#3b1f12', '#2b160d', '#e0c79c', '#fbf2de', '#f7a531', '#e0741c'


def page(name, w, h, body):
    bg = f'<rect width="{w}" height="{h}" fill="#f5e6c8"/><rect width="{w}" height="{h}" fill="url(#dots)"/>'
    html = HEAD + f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{bg}{"".join(body)}</svg></body></html>'
    open(name, 'w', encoding='utf-8').write(html)


_gid = [0]


def tile(x, y, s, name, ticker=None, pct=None, label=None, shadow=True):
    """A skin in the dark well with its rarity glowing behind it, rarity bar on the bottom edge."""
    f, col = skin(name)
    _gid[0] += 1
    g = f'g{_gid[0]}'
    out = [f'<defs><radialGradient id="{g}" cx="0.5" cy="0.45" r="0.6"><stop offset="0" stop-color="{col}" stop-opacity="0.55"/>'
           f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>']
    if shadow:
        out.append(f'<rect x="{x + 6}" y="{y + 6}" width="{s}" height="{s}" rx="4" fill="{INK}"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="4" fill="{WELL}"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="4" fill="url(#{g})"/>')
    iw = s * 0.86
    out.append(f'<image href="{f}" x="{x + (s - iw) / 2}" y="{y + s * 0.06}" width="{iw}" height="{iw * 0.75}"/>')
    if ticker:
        fs = s * 0.085
        out.append(f'<text class="px" x="{x + s * 0.07}" y="{y + s * 0.84}" font-size="{fs}" fill="#fbf2de">${ticker}</text>')
        if pct is not None:
            out.append(f'<text class="px" x="{x + s * 0.93}" y="{y + s * 0.84}" font-size="{fs}" fill="{BRAND}" text-anchor="end">{pct}%</text>')
            bw = s * 0.86
            out.append(f'<rect x="{x + s * 0.07}" y="{y + s * 0.89}" width="{bw}" height="{s * 0.03}" fill="#5a3a26"/>')
            out.append(f'<rect x="{x + s * 0.07}" y="{y + s * 0.89}" width="{bw * pct / 100}" height="{s * 0.03}" fill="{BRAND}"/>')
    if label:
        lw = len(label) * s * 0.052 + s * 0.08
        out.append(f'<rect x="{x + s * 0.05}" y="{y + s * 0.05}" width="{lw}" height="{s * 0.11}" fill="{WELL}" stroke="#5a3a26" stroke-width="2"/>')
        out.append(f'<text class="px" x="{x + s * 0.09}" y="{y + s * 0.135}" font-size="{s * 0.075}" fill="#fbf2de">{label}</text>')
    out.append(f'<rect x="{x}" y="{y + s - s * 0.025}" width="{s}" height="{s * 0.025}" fill="{col}"/>')
    return ''.join(out)


def button(cx, cy, w, h, text, primary=True, fs=30):
    fill = BRAND if primary else SURF
    return (f'<rect x="{cx - w / 2 + 4}" y="{cy - h / 2 + 4}" width="{w}" height="{h}" fill="{INK}"/>'
            f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="3"/>'
            f'<text class="px" x="{cx}" y="{cy + fs * 0.34}" font-size="{fs}" fill="{INK}" text-anchor="middle">{text}</text>')


def panel(x, y, w, h):
    return (f'<rect x="{x + 6}" y="{y + 6}" width="{w}" height="{h}" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{SURF}" stroke="{INK}" stroke-width="3"/>')


def arrow(x1, x2, y):
    return (f'<path d="M{x1} {y}H{x2 - 26}" stroke="{AMBER}" stroke-width="8" stroke-dasharray="14 10"/>'
            f'<path d="M{x2 - 30} {y - 22}L{x2} {y}L{x2 - 30} {y + 22}Z" fill="{AMBER}"/>')


def headline(cx, y, plain, accent, fs=64):
    return f'<text class="disp" x="{cx}" y="{y}" font-size="{fs}" text-anchor="middle">{plain}<tspan class="acc">{accent}</tspan></text>'


WALL = [('★ Karambit | Doppler', 'DOPPLER', 53), ('AWP | Asiimov', 'ASIIMOV', 61), ('AK-47 | Redline', 'REDLINE', 88),
        ('Desert Eagle | Printstream', 'PRINT', 27), ('M4A4 | Howl', 'HOWL', 12), ('★ Butterfly Knife | Fade', 'FADE', 91),
        ('★ Sport Gloves | Vice', 'VICE', 48), ('AK-47 | Fire Serpent', 'SERPENT', 67), ('AWP | Dragon Lore', 'LORE', 9),
        ('USP-S | Kill Confirmed', 'CONFIRM', 73), ('★ M9 Bayonet | Crimson Web', 'CRIMSON', 35), ('M4A1-S | Printstream', 'PRINTM4', 84),
        ('Glock-18 | Fade', 'GLOCK', 96), ('AK-47 | Vulcan', 'VULCAN', 42), ('★ Specialist Gloves | Crimson Kimono', 'KIMONO', 19),
        ('AWP | Hyper Beast', 'BEAST', 62), ('★ Talon Knife | Marble Fade', 'MARBLE', 27), ('P90 | Asiimov', 'P90', 70)]

# ---------------------------------------------------------------- 1 cover 2000x800
b = []
s, gap = 230, 22
b.append(f'<rect width="2000" height="800" fill="{INK}"/>')
b.append('<g transform="rotate(-8 1000 400)">')
i = 0
for r in range(-2, 6):
    for c in range(-2, 11):
        name, tick, pct = WALL[i % len(WALL)]
        i += 5
        b.append(tile(-140 + c * (s + gap) + (r % 2) * 90, -260 + r * (s + gap), s, name, tick, pct, shadow=False))
b.append('</g>')
b.append(f'<rect width="2000" height="800" fill="{INK}" fill-opacity="0.25"/>')
b.append(panel(560, 175, 880, 450))
b.append(f'<image href="logo.png" x="610" y="215" width="{230 * 798 / 1023}" height="230"/>')
b.append('<image href="wordmark.png" x="805" y="225" width="600" height="150"/>')
b.append('<text class="disp" x="1000" y="518" font-size="56" text-anchor="middle">Every coin buys a real <tspan class="acc">skin</tspan></text>')
b.append('<text class="txt" x="1000" y="580" font-size="30" text-anchor="middle">A CSGO skin launchpad on Solana</text>')
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 pick a skin, launch its coin 1600x900
b = []
b.append(headline(800, 130, 'Pick a skin. ', 'Launch its coin.'))
# the picker: three tiles, one chosen
opts = ['AK-47 | Redline', 'AWP | Asiimov', '★ Karambit | Doppler']
for k, n in enumerate(opts):
    x, y = 110, 215 + k * 205
    b.append(tile(x, y, 180, n, shadow=(k == 1)))
    if k == 1:
        b.append(f'<rect x="{x - 10}" y="{y - 10}" width="200" height="200" fill="none" stroke="{BRAND}" stroke-width="6"/>')
    nm = n.replace('★ ', '')
    b.append(f'<text class="ink" x="{x + 210}" y="{y + 82}" font-size="{30 if k == 1 else 26}" style="{"" if k == 1 else "fill:#85604a"}">{nm}</text>')
    b.append(f'<text class="dim" x="{x + 210}" y="{y + 122}" font-size="24">{["Field-Tested", "Field-Tested", "Factory New"][k]}</text>')
b.append(arrow(640, 830, 522))
# the coin card
b.append(panel(860, 225, 640, 600))
f, col = skin('AWP | Asiimov')
b.append(f'<defs><clipPath id="coin"><circle cx="1010" cy="375" r="95"/></clipPath><radialGradient id="cg" cx="0.5" cy="0.5" r="0.6"><stop offset="0" stop-color="{col}" stop-opacity="0.6"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>')
b.append(f'<circle cx="1010" cy="375" r="95" fill="{WELL}"/><circle cx="1010" cy="375" r="95" fill="url(#cg)"/>')
b.append(f'<image href="{f}" x="905" y="300" width="210" height="157" clip-path="url(#coin)"/>')
b.append(f'<circle cx="1010" cy="375" r="95" fill="none" stroke="{BRAND}" stroke-width="7"/>')
b.append('<text class="disp" x="1135" y="365" font-size="56">$ASIIMOV</text>')
b.append('<text class="txt" x="1137" y="410" font-size="28">AWP Asiimov coin</text>')
rows = [('Name and ticker', 'filled in'), ('Coin image', 'drawn from the skin'), ('Creator fees', 'buy the skin')]
for k, (a, c) in enumerate(rows):
    y = 530 + k * 58
    b.append(f'<text class="txt" x="910" y="{y}" font-size="27">{a}</text>')
    b.append(f'<text class="ink" x="1450" y="{y}" font-size="27" text-anchor="end">{c}</text>')
    b.append(f'<path d="M910 {y + 20}H1450" stroke="{LINE}" stroke-width="2"/>')
b.append(button(1180, 752, 540, 76, 'Launch a coin', fs=34))
b.append('<text class="dim" x="800" y="872" font-size="25" text-anchor="middle">Knives, gloves, rifles. Dota 2 items work too.</text>')
page('02-launch.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 where the fees go 1600x900
b = []
b.append(headline(800, 130, '', '90%', fs=72))
b.append('<text class="disp" x="800" y="210" font-size="56" text-anchor="middle">of creator fees save toward the skin</text>')
b.append(tile(130, 330, 300, 'AWP | Asiimov', 'ASIIMOV', 64))
b.append(arrow(470, 620, 480))
bx, bw, by, bh = 650, 820, 395, 120
b.append(f'<rect x="{bx + 6}" y="{by + 6}" width="{bw}" height="{bh}" fill="{INK}"/>')
b.append(f'<rect x="{bx}" y="{by}" width="{bw * 0.9}" height="{bh}" fill="{BRAND}" stroke="{INK}" stroke-width="3"/>')
b.append(f'<rect x="{bx + bw * 0.9}" y="{by}" width="{bw * 0.1}" height="{bh}" fill="{WELL}" stroke="{INK}" stroke-width="3"/>')
b.append(f'<text class="disp" x="{bx + 36}" y="{by + 78}" font-size="56">90%</text>')
b.append(f'<text class="px" x="{bx + bw * 0.95}" y="{by + 72}" font-size="30" fill="#fbf2de" text-anchor="middle">10%</text>')
leg = [(BRAND, 'Saved toward that skin', '90%'), (WELL, 'Saved toward the next big skin', '10%'), (SURF, 'The coin creator', '0%')]
for k, (c, a, p) in enumerate(leg):
    y = 590 + k * 64
    b.append(f'<rect x="{bx}" y="{y - 26}" width="30" height="30" fill="{c}" stroke="{INK}" stroke-width="3"/>')
    b.append(f'<text class="ink" x="{bx + 52}" y="{y}" font-size="32">{a}</text>')
    b.append(f'<text class="num" x="{bx + bw}" y="{y}" font-size="34" text-anchor="end">{p}</text>')
b.append('<text class="dim" x="800" y="865" font-size="25" text-anchor="middle">Split on chain the moment the coin launches. Every coin on a skin saves for it together.</text>')
page('03-fees.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 then we buy it 1600x900
b = []
b.append(headline(800, 130, 'Saved hits 100%. ', 'We buy it.'))
xs = [290, 800, 1310]
ts = 330
for k, x in enumerate(xs):
    lbl = ['100% saved', 'Waxpeer', 'Bought'][k]
    b.append(tile(x - ts / 2, 230, ts, 'AK-47 | Redline', label=lbl))
    if k == 0:
        b.append(f'<rect x="{x - ts / 2 + 22}" y="{230 + ts * 0.86}" width="{ts - 44}" height="16" fill="{BRAND}"/>')
    if k == 1:
        b.append(f'<circle cx="{x + ts / 2 - 50}" cy="{230 + ts - 60}" r="34" fill="{BRAND}" stroke="{INK}" stroke-width="3"/>'
                 f'<text class="num" x="{x + ts / 2 - 50}" y="{230 + ts - 48}" font-size="34" text-anchor="middle">$</text>')
    if k == 2:
        b.append(f'<circle cx="{x + ts / 2 - 50}" cy="{230 + ts - 60}" r="34" fill="{BRAND}" stroke="{INK}" stroke-width="3"/>'
                 f'<path d="M{x + ts / 2 - 66} {230 + ts - 60}l12 12l22 -24" fill="none" stroke="{INK}" stroke-width="7"/>')
for x1, x2 in [(xs[0] + ts / 2 + 14, xs[1] - ts / 2 - 14), (xs[1] + ts / 2 + 14, xs[2] - ts / 2 - 14)]:
    b.append(arrow(x1, x2, 395))
steps = [('The savings cover it', "at the skin's live price"), ('Bought on Waxpeer', 'automatically, cheapest listing'),
         ('In our Steam account', 'public, checked every hour')]
for x, (a, c) in zip(xs, steps):
    b.append(f'<text class="disp" x="{x}" y="{650}" font-size="40" text-anchor="middle">{a}</text>')
    b.append(f'<text class="txt" x="{x}" y="{700}" font-size="28" text-anchor="middle">{c}</text>')
b.append('<text class="dim" x="800" y="840" font-size="25" text-anchor="middle">Then saving starts again toward the next copy.</text>')
page('04-bought.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 closing 1600x900
b = []
b.append(panel(300, 180, 1000, 540))
lh = 250
b.append(f'<image href="logo.png" x="360" y="235" width="{lh * 798 / 1023}" height="{lh}"/>')
b.append('<image href="wordmark.png" x="570" y="255" width="680" height="170"/>')
b.append('<text class="txt" x="800" y="545" font-size="34" text-anchor="middle">Every coin is paired with a CSGO skin.</text>')
b.append(button(800, 628, 460, 84, 'skinpair.fun', fs=44))
page('05-close.html', 1600, 900, b)
print('built')

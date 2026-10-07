"""Builds each article picture as an HTML page in Treepad's look. tools/render.py shoots them to PNG.

Assets are copied from the treepad repo (public/brand, public/art, src/lib/world-pixels.ts -> world.json)
so this rebuilds without it.
"""
import json

W = json.load(open('world.json', encoding='utf-8'))
PAD_X, PAD_Y = 6, 1
VIEW_W, VIEW_H = W['cols'] + PAD_X * 2, W['rows'] + PAD_Y * 2
LAND = ['#1a5c25', '#227a2d', '#2f9a39', '#1d6a29']

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet">
<style>
html,body{margin:0;padding:0;background:#07090a;overflow:hidden}
svg{display:block}
image{image-rendering:auto}  /* the art is drawn big and always shrunk here; 'pixelated' drops and doubles pixels when shrinking */
.disp{font-family:Outfit;font-weight:600;fill:#f3f6f2;letter-spacing:-0.02em}
.txt{font-family:Outfit;fill:rgb(243 246 242 / 0.62)}
.dim{font-family:'JetBrains Mono';fill:rgb(243 246 242 / 0.38)}
.mono{font-family:'JetBrains Mono';font-weight:500}
.neon{fill:#6dff4f}
.panel{fill:#0c110e;stroke:rgb(255 255 255 / 0.09);stroke-width:2}
.flow{fill:none;stroke:#6dff4f;stroke-width:4;stroke-dasharray:2 14;stroke-linecap:round}
</style></head><body>'''

DEFS = '''<defs>
<linearGradient id="sol" x1="8.5" y1="90" x2="89" y2="-3" gradientUnits="userSpaceOnUse">
<stop offset="0.08" stop-color="#9945FF"/><stop offset="0.3" stop-color="#8752F3"/><stop offset="0.5" stop-color="#5497D5"/>
<stop offset="0.6" stop-color="#43B4CA"/><stop offset="0.72" stop-color="#28E0B9"/><stop offset="0.97" stop-color="#19FB9B"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#6dff4f" stop-opacity="0.30"/><stop offset="1" stop-color="#6dff4f" stop-opacity="0"/></radialGradient>
<filter id="tree-glow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="0" stdDeviation="14" flood-color="#6eff5a" flood-opacity="0.35"/></filter>
<filter id="land-glow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.4"/></filter>
<pattern id="map-grid" width="1" height="1" patternUnits="userSpaceOnUse"><path d="M1 0H0V1" fill="none" stroke="#9fc4ff" stroke-opacity="0.1" stroke-width="0.08"/></pattern>
<linearGradient id="fade-l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#07090a" stop-opacity="1"/><stop offset="0.42" stop-color="#07090a" stop-opacity="0.92"/><stop offset="0.62" stop-color="#07090a" stop-opacity="0.15"/><stop offset="1" stop-color="#07090a" stop-opacity="0"/></linearGradient>
</defs>'''

SOLANA = ('M100.48 69.38L83.81 86.8a4 4 0 0 1-2.83 1.2H1.94a1.94 1.94 0 0 1-1.42-3.17L17.2 67.4a4 4 0 0 1 2.83-1.2h79.03a1.94 1.94 0 0 1 1.42 3.18Z'
          'M83.81 34.3a4 4 0 0 0-2.83-1.2H1.94A1.94 1.94 0 0 0 .52 36.28L17.2 53.7a4 4 0 0 0 2.83 1.2h79.03a1.94 1.94 0 0 0 1.42-3.17Z'
          'M1.94 21.79h79.04a4 4 0 0 0 2.83-1.2L100.48 3.17A1.94 1.94 0 0 0 99.06 0H20.03a4 4 0 0 0-2.82 1.2L.52 18.62a1.94 1.94 0 0 0 1.42 3.17Z')

STAGES = ['tree-0-seed', 'tree-1-sprout', 'tree-2-sapling', 'tree-3-tree', 'tree-4-giant']


def page(name, w, h, body):
    html = HEAD + f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}<rect width="{w}" height="{h}" fill="#07090a"/>{"".join(body)}</svg></body></html>'
    open(name, 'w', encoding='utf-8').write(html)


def ocean_dots():
    # Same seeded scatter as the site's map, so the islands sit in the same places.
    land = set()
    import re
    for d in W['paths']:
        for x, y, w in re.findall(r'M(\d+) (\d+)h(\d+)', d):
            for i in range(int(w)):
                land.add((int(x) + i, int(y)))

    def near(x, y):
        return any((x + dx, y + dy) in land for dy in range(-3, 4) for dx in range(-3, 4))

    out = []
    for y in range(-PAD_Y, W['rows'] + PAD_Y):
        for x in range(-PAD_X, W['cols'] + PAD_X):
            if (x, y) in land:
                continue
            a = (x * 374761393 + y * 668265263) & 0xffffffff
            roll = ((a * 1274126177) & 0xffffffff) / 2 ** 32
            if roll < (0.045 if near(x, y) else 0.008):
                out.append(f'M{x} {y}h1v1h-1z')
    return ''.join(out)


DOTS = ocean_dots()


def world(x, y, width, ocean=True):
    """The site's pixel world map, `width` px wide with its top-left at x, y. Returns (svg, scale)."""
    s = width / VIEW_W
    h = VIEW_H * s
    g = [f'<g transform="translate({x} {y}) scale({s}) translate({PAD_X} {PAD_Y})" shape-rendering="crispEdges">']
    if ocean:
        g.append(f'<rect x="{-PAD_X}" y="{-PAD_Y}" width="{VIEW_W}" height="{VIEW_H}" fill="#0a141d"/>')
    g.append(f'<rect x="{-PAD_X}" y="{-PAD_Y}" width="{VIEW_W}" height="{VIEW_H}" fill="url(#map-grid)"/>')
    g.append(f'<path d="{DOTS}" fill="#1d5634" fill-opacity="0.7"/>')
    g.append('<g filter="url(#land-glow)" opacity="0.22">' + ''.join(f'<path d="{d}" fill="#38c845"/>' for d in W['paths']) + '</g>')
    g += [f'<path d="{d}" fill="{LAND[i]}"/>' for i, d in enumerate(W['paths'])]
    g.append(f'<rect x="{-PAD_X}" y="{-PAD_Y}" width="{VIEW_W}" height="{VIEW_H}" fill="url(#map-grid)" opacity="0.5"/>')
    g.append('</g>')
    return ''.join(g), s, h


def map_point(x, y, s, lat, lng):
    return x + (PAD_X + (lng + 180) / 360 * W['cols']) * s, y + (PAD_Y + (W['top'] - lat) / W['step']) * s


def tree(stage, cx, base, size, glow=True):
    """A pixel tree sprite, bottom-centre at cx, base. The art sits on the bottom of its square frame."""
    f = ' filter="url(#tree-glow)"' if glow else ''
    return f'<image href="{STAGES[stage]}.png" x="{cx - size / 2}" y="{base - size}" width="{size}" height="{size}"{f}/>'


def brand(cx, cy, h):
    """Logo + wordmark lockup like the site header, centred on cx, cy, `h` tall."""
    lw = h * 985 / 964
    wh = h * 0.6
    ww = wh * 1804 / 433
    total = lw + h * 0.08 + ww
    x0 = cx - total / 2
    return (f'<image href="logo.png" x="{x0}" y="{cy - h / 2}" width="{lw}" height="{h}"/>'
            f'<image href="wordmark.png" x="{x0 + lw + h * 0.08}" y="{cy - wh / 2 + h * 0.04}" width="{ww}" height="{wh}"/>')


def solana(cx, cy, w):
    s = w / 101
    return f'<g transform="translate({cx - w / 2} {cy - 88 * s / 2}) scale({s})"><path d="{SOLANA}" fill="url(#sol)"/></g>'


def headline(x, y, plain, lit, size=78, anchor='start'):
    return (f'<text x="{x}" y="{y}" class="disp" font-size="{size}" text-anchor="{anchor}">{plain}'
            f'<tspan class="neon">{lit}</tspan></text>')


CAT = json.load(open('catalog.json', encoding='utf-8'))  # live /api/trees picks + all 43 project spots, saved 2026-10-08
KENYA = (-3.5, 39.6)

FLAME = ['...ab...', '..abba..', '..abbba.', '.abbcbba', '.abccbba', 'abbccbba', 'abcccbba', 'abccccba', '.abccba.', '..aaaa..']
FLAME_C = {'a': '#ff5c2a', 'b': '#ffa62b', 'c': '#ffe066'}


def flame(cx, base, px):
    out = []
    for r, row in enumerate(FLAME):
        for c, ch in enumerate(row):
            if ch in FLAME_C:
                out.append(f'<rect x="{cx - 4 * px + c * px}" y="{base - (len(FLAME) - r) * px}" width="{px}" height="{px}" fill="{FLAME_C[ch]}"/>')
    return '<g shape-rendering="crispEdges" filter="url(#fire-glow)">' + ''.join(out) + '</g>'


def pins(x, y, s, small, big):
    """Every Tree-Nation project as a small sapling, like the site's map, and Treepad's planted spot as a glowing giant."""
    out = []
    for lat, lng, name, place in CAT['projects']:
        if name == 'Kenya Mangroves Restoration':
            continue
        px, py = map_point(x, y, s, lat, lng)
        out.append(f'<ellipse cx="{px}" cy="{py}" rx="{small * 0.3}" ry="{small * 0.06}" fill="#000" opacity="0.6"/>')
        out.append(tree(2, px, py, small, glow=False).replace('/>', ' opacity="0.9" filter="url(#pin-glow)"/>'))
    px, py = map_point(x, y, s, *KENYA)
    out.append(f'<circle cx="{px}" cy="{py - big * 0.35}" r="{big * 0.85}" fill="url(#glow)"/>')
    out.append(tree(4, px, py + big * 0.06, big))
    return ''.join(out), px, py


EXTRA_DEFS = ('<defs><filter id="pin-glow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#6eff5a" flood-opacity="0.3"/></filter>'
              '<filter id="fire-glow" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#ff8a2a" flood-opacity="0.45"/></filter></defs>')

# ---------------------------------------------------------------- 1 cover 2000x800
# A row of pixel trees growing left to right along the ground, headline centred above.
b = []
b.append('<rect x="0" y="660" width="2000" height="140" fill="#0b120c"/>')
b.append('<path d="M0 660H2000" stroke="rgb(109 255 79 / 0.25)" stroke-width="2"/>')
b.append('<ellipse cx="1000" cy="660" rx="1100" ry="160" fill="url(#glow)" opacity="0.7"/>')
row = [(0, 70), (1, 95), (2, 130), (3, 170), (4, 230), (3, 160), (2, 120), (1, 90), (0, 64)]
xs = [140, 330, 520, 735, 1000, 1265, 1480, 1670, 1860]
for (st, sz), x in zip(row, xs):
    b.append(tree(st, x, 672, sz * 1.1))
b.append(brand(1000, 110, 80))
b.append('<text x="1000" y="275" class="disp" font-size="116" text-anchor="middle">Every trade <tspan class="neon">plants a tree.</tspan></text>')
b.append('<text x="1000" y="345" class="txt" font-size="38" text-anchor="middle">Launch a coin on pump.fun. Pick a real tree. Trades pay to plant it.</text>')
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 pick your tree 1600x900
b = [EXTRA_DEFS, headline(100, 160, 'Pick your tree. ', '580 to choose from.')]
order = ['Grey Mangrove', 'Ipê-Amarelo', 'Cork oak', 'Honduran Mahogany']
picks = {p['name']: p for p in CAT['picks']}
cw, gap = 320, 40
x0 = (1600 - (4 * cw + 3 * gap)) / 2
top, ph, ch = 240, 250, 470
for i, name in enumerate(order):
    sp = picks[name]
    x = x0 + i * (cw + gap)
    sel = i == 0
    b.append(f'<clipPath id="ph{i}"><rect x="{x}" y="{top}" width="{cw}" height="{ph + 20}" rx="22"/></clipPath>')
    b.append(f'<rect x="{x}" y="{top}" width="{cw}" height="{ch}" rx="22" fill="{"#0d1a0f" if sel else "#0c110e"}" stroke="{"#6dff4f" if sel else "rgb(255 255 255 / 0.09)"}" stroke-opacity="{0.7 if sel else 1}" stroke-width="{3 if sel else 2}"/>')
    b.append(f'<image href="{sp["file"]}" x="{x}" y="{top}" width="{cw}" height="{ph}" preserveAspectRatio="xMidYMid slice" clip-path="url(#ph{i})" style="image-rendering:auto"/>')
    b.append(f'<rect x="{x}" y="{top + ph - 1}" width="{cw}" height="2" fill="rgb(255 255 255 / 0.08)"/>')
    if sel:
        b.append(f'<rect x="{x + 18}" y="{top + 18}" width="112" height="40" rx="20" fill="#6dff4f"/>')
        b.append(f'<text x="{x + 74}" y="{top + 45}" font-family="Outfit" font-weight="600" font-size="21" fill="#07090a" text-anchor="middle">Picked</text>')
    tx = x + 26
    b.append(f'<text x="{tx}" y="{top + ph + 56}" class="disp" font-size="{30 if len(name) < 16 else 27}">{name}</text>')
    b.append(f'<text x="{tx}" y="{top + ph + 96}" class="txt" font-size="24">{sp["place"]}</text>')
    price = f'€{sp["priceEur"]:.2f}' if sp['priceEur'] < 1 else f'€{sp["priceEur"]:g}'
    b.append(f'<text x="{tx}" y="{top + ph + 150}" class="mono" font-size="25" font-weight="700" fill="{"#6dff4f" if sel else "rgb(243 246 242 / 0.85)"}">{price} a tree</text>')
    b.append(f'<text x="{tx}" y="{top + ph + 186}" class="dim" font-size="21">{sp["co2Kg"]} kg CO₂ each</text>')
b.append('<text x="800" y="800" class="dim" font-size="24" text-anchor="middle">580 trees in 22 countries, from €0.35. Every tree gets a public certificate.</text>')
page('02-pick.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 fee split 1600x900
b = [EXTRA_DEFS, headline(100, 160, 'Every trade ', 'pays for your tree.')]
b.append(f'<circle cx="138" cy="262" r="30" fill="#000" fill-opacity="0.5" stroke="rgb(255 255 255 / 0.08)" stroke-width="2"/>')
b.append(solana(138, 262, 30))
b.append('<text x="186" y="272" class="txt" font-size="30">The creator fee on every coin splits two ways</text>')
bx, by, bw, bh = 100, 330, 1400, 400
tw = bw * 0.8 - 12
b.append(f'<rect x="{bx}" y="{by}" width="{tw}" height="{bh}" rx="28" fill="#0d1a0f" stroke="#6dff4f" stroke-opacity="0.6" stroke-width="3"/>')
b.append(f'<circle cx="{bx + 300}" cy="{by + 200}" r="210" fill="url(#glow)"/>')
b.append(tree(4, bx + 300, by + 360, 320))
b.append(f'<text x="{bx + 590}" y="{by + 215}" class="disp neon" font-size="190">80%</text>')
b.append(f'<text x="{bx + 598}" y="{by + 300}" class="disp" font-size="50">plants your tree</text>')
fx = bx + tw + 24
fw = bw - tw - 24
b.append(f'<rect x="{fx}" y="{by}" width="{fw}" height="{bh}" rx="28" class="panel"/>')
b.append(flame(fx + fw / 2, by + 150, 9))
b.append(f'<text x="{fx + fw / 2}" y="{by + 255}" class="disp" font-size="84" text-anchor="middle">20%</text>')
b.append(f'<text x="{fx + fw / 2}" y="{by + 305}" class="txt" font-size="26" text-anchor="middle">buys back &amp; burns</text>')
b.append(f'<text x="{fx + fw / 2}" y="{by + 345}" font-family="Outfit" font-weight="600" font-size="27" fill="#f3f6f2" text-anchor="middle">the Treepad coin</text>')
b.append('<text x="800" y="820" class="dim" font-size="24" text-anchor="middle">Locked on chain at launch. Traders pay nothing extra.</text>')
page('03-split.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 tree grows 1600x900
b = [headline(100, 170, 'Your tree grows ', 'with your coin.')]
names = ['Seed', 'Sprout', 'Sapling', 'Tree', 'Giant']
caps = ['at launch', '$10k', '$50k', '$250k', '$1M']
sizes = [140, 180, 220, 260, 300]
base = 640
step = 1400 / 5
for i in range(5):
    cx = 100 + step * (i + 0.5)
    b.append(f'<circle cx="{cx}" cy="{base - sizes[i] * 0.35}" r="{sizes[i] * 0.55}" fill="url(#glow)" opacity="{0.4 + i * 0.15}"/>')
    b.append(tree(i, cx, base, sizes[i]))
    b.append(f'<text x="{cx}" y="{base + 70}" class="disp{" neon" if i == 4 else ""}" font-size="38" text-anchor="middle">{names[i]}</text>')
    b.append(f'<text x="{cx}" y="{base + 112}" class="mono" fill="rgb(243 246 242 / 0.55)" font-size="26" text-anchor="middle">{caps[i]}</text>')
b.append(f'<path d="M100 {base + 4}H1500" stroke="rgb(255 255 255 / 0.10)" stroke-width="2"/>')
b.append('<text x="800" y="850" class="dim" font-size="24" text-anchor="middle">Every coin on Treepad gets its own tree. Market cap sets its size.</text>')
page('04-grow.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 close 1600x900
b = []
b.append('<circle cx="800" cy="320" r="330" fill="url(#glow)"/>')
b.append(brand(800, 320, 230))
b.append('<text x="800" y="550" class="disp" font-size="76" text-anchor="middle">Every trade <tspan class="neon">plants a tree.</tspan></text>')
b.append('<rect x="610" y="620" width="380" height="96" rx="48" fill="#6dff4f"/>')
b.append('<text x="800" y="684" font-family="Outfit" font-weight="600" font-size="44" fill="#07090a" text-anchor="middle">treepad.fun</text>')
b.append('<text x="800" y="790" class="dim" font-size="28" text-anchor="middle">@treepadfun</text>')
page('05-close.html', 1600, 900, b)
print('ok')

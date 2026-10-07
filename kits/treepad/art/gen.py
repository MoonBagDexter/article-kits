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
image{image-rendering:pixelated}
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


# ---------------------------------------------------------------- 1 cover 2000x800
b = []
cover_w = 800 / VIEW_H * VIEW_W  # fill the full height, crop the sides
m, s, mh = world((2000 - cover_w) / 2, 0, cover_w)
b.append(m)
px, py = map_point((2000 - cover_w) / 2, 0, s, -3.5, 39.6)  # Kenya's coast, where the mangroves go
b.append(f'<circle cx="{px}" cy="{py}" r="90" fill="url(#glow)"/>')
b.append(tree(3, px, py + 18, 120))
b.append('<rect width="2000" height="800" fill="url(#fade-l)"/>')
b.append(brand(283, 150, 96))
b.append('<text x="110" y="400" class="disp" font-size="118">Every trade</text>')
b.append('<text x="110" y="530" class="disp neon" font-size="118">plants a tree.</text>')
b.append('<text x="114" y="620" class="txt" font-size="40">Launch a coin. 100% of its fees plant real trees.</text>')
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 launch flow 1600x900
b = [headline(100, 170, 'Launch a coin. ', 'Fees plant trees.')]
cards = [
    ('Your coin', 'goes live on pump.fun'),
    ('Every trade', 'pays the creator fee'),
    ('100% of it', 'buys real trees'),
]
cw, ch, gap = 380, 420, 130
x0 = (1600 - (3 * cw + 2 * gap)) / 2
cy = 270
for i, (t, sub) in enumerate(cards):
    x = x0 + i * (cw + gap)
    lit = i == 2
    stroke = ' stroke="#6dff4f" stroke-opacity="0.55"' if lit else ''
    b.append(f'<rect x="{x}" y="{cy}" width="{cw}" height="{ch}" rx="28" class="panel"{stroke}/>')
    mx = x + cw / 2
    b.append(f'<circle cx="{mx}" cy="{cy + 150}" r="110" fill="url(#glow)" opacity="{1 if lit else 0.55}"/>')
    if i == 0:
        b.append(tree(0, mx, cy + 262, 280))
    elif i == 1:
        b.append(f'<circle cx="{mx}" cy="{cy + 150}" r="78" fill="#000" fill-opacity="0.5" stroke="rgb(255 255 255 / 0.08)" stroke-width="2"/>')
        b.append(solana(mx, cy + 150, 72))
    else:
        b.append(tree(3, mx, cy + 262, 240))
    b.append(f'<text x="{mx}" y="{cy + 330}" class="disp{" neon" if lit else ""}" font-size="40" text-anchor="middle">{t}</text>')
    b.append(f'<text x="{mx}" y="{cy + 378}" class="txt" font-size="27" text-anchor="middle">{sub}</text>')
    if i < 2:
        ax = x + cw + 22
        b.append(f'<path d="M{ax} {cy + ch / 2}H{ax + gap - 44}" class="flow"/>')
        b.append(f'<path d="M{ax + gap - 56} {cy + ch / 2 - 13}l14 13l-14 13" fill="none" stroke="#6dff4f" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')
b.append('<text x="800" y="800" class="dim" font-size="24" text-anchor="middle">The tree split is locked on chain when the coin is created.</text>')
page('02-launch.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 tree grows 1600x900
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
page('03-grow.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 on the map 1600x900
b = [headline(100, 150, 'Every tree, ', 'on the map.')]
mw = 1400
mx0, my0 = 100, 210
m, s, mh = world(mx0, my0, mw)
b.append(f'<clipPath id="mapclip"><rect x="{mx0}" y="{my0}" width="{mw}" height="{mh}" rx="24"/></clipPath>')
b.append(f'<g clip-path="url(#mapclip)">{m}</g>')
b.append(f'<rect x="{mx0}" y="{my0}" width="{mw}" height="{mh}" rx="24" fill="none" stroke="rgb(255 255 255 / 0.08)" stroke-width="2"/>')
px, py = map_point(mx0, my0, s, -3.5, 39.6)
b.append(f'<circle cx="{px}" cy="{py}" r="70" fill="url(#glow)"/>')
b.append(tree(3, px, py + 14, 90))
# Pin card, like the site's hover card.
cwid, chei = 620, 190
cx, cyy = px - 70 - cwid, py - 120  # card sits left of the pin; the right side runs off the picture
b.append(f'<path d="M{cx + cwid} {py - 25}l14 14l-14 14z" fill="#10161c"/>')
b.append(f'<rect x="{cx}" y="{cyy}" width="{cwid}" height="{chei}" rx="20" fill="#10161c" stroke="rgb(255 255 255 / 0.14)" stroke-width="2"/>')
b.append(tree(3, cx + 70, cyy + 110, 84, glow=True))
b.append(f'<text x="{cx + 130}" y="{cyy + 62}" class="disp" font-size="31">Kenya Mangroves Restoration</text>')
b.append(f'<text x="{cx + 130}" y="{cyy + 106}" class="txt" font-size="27">Grey Mangroves, by Tree-Nation</text>')
b.append(f'<text x="{cx + 130}" y="{cyy + 150}" font-family="Outfit" font-size="27" class="neon">A public certificate for every tree</text>')
b.append('<text x="800" y="818" class="dim" font-size="24" text-anchor="middle">Every fee claim is a Solana transaction. Every tree has a certificate.</text>')
page('04-map.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 close 1600x900
b = []
b.append('<circle cx="800" cy="330" r="330" fill="url(#glow)"/>')
b.append(brand(800, 330, 230))
b.append('<text x="800" y="560" class="disp" font-size="76" text-anchor="middle">Every trade <tspan class="neon">plants a tree.</tspan></text>')
b.append('<rect x="610" y="640" width="380" height="96" rx="48" fill="#6dff4f"/>')
b.append('<text x="800" y="704" font-family="Outfit" font-weight="600" font-size="44" fill="#07090a" text-anchor="middle">treepad.fun</text>')
page('05-close.html', 1600, 900, b)
print('ok')

"""Builds each article picture as an HTML page in curv.fund's own look. tools/render.py shoots them to PNG.

The look is the site's: flat pixel tiles on a dark green ground, hard edges, no radius, shadow, gradient or glow.
Headlines in Pixelify Sans sit on solid ink strips, numbers are always JetBrains Mono, one phrase per headline
goes curv green. mark.png / wordmark.png are copied from fresh/public/brand and only ever drawn at whole
multiples of their 43x43 / 75x14 pixel grids.
"""
import random

GROUND, SURFACE, RAISED, EDGE = '#0d0f08', '#161a0f', '#1f2415', '#2c3320'
CURV, DEEP = '#b0fa37', '#327a0e'
TEXT, SOFT, MUTE = '#f4f0e8', '#a3ab8e', '#6c7458'
DANGER, CREAM, CREAM_EDGE, INK = '#f2553f', '#efeadb', '#d3ccb8', '#0d0f08'

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Pixelify+Sans:wght@700&family=Silkscreen&display=block" rel="stylesheet">
<style>
html,body{margin:0;padding:0;background:#0d0f08;overflow:hidden}
svg{display:block}
image{image-rendering:pixelated}
.hl{font-family:'Pixelify Sans';font-weight:700;fill:#f4f0e8;font-variant-ligatures:none;font-feature-settings:'liga' 0}
.tag{font-family:Silkscreen;text-transform:uppercase}
.txt{font-family:Inter;fill:#f4f0e8}
.soft{font-family:Inter;fill:#a3ab8e}
.num{font-family:'JetBrains Mono';font-weight:600;fill:#f4f0e8}
.c{fill:#b0fa37}
</style></head><body>'''

# Every text.strip gets a solid ink block behind it once the fonts are in, like the site's headline strips.
STRIPS = '''<script>
document.fonts.ready.then(() => {
  for (const t of document.querySelectorAll('text.strip')) {
    const b = t.getBBox(), p = +(t.dataset.pad || 14);
    const r = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    r.setAttribute('x', b.x - p); r.setAttribute('y', b.y - p / 2);
    r.setAttribute('width', b.width + 2 * p); r.setAttribute('height', b.height + p);
    r.setAttribute('fill', t.dataset.bg || '#0d0f08');
    t.parentNode.insertBefore(r, t);
  }
});
</script>'''


def page(name, w, h, body):
    svg = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges">{"".join(body)}</svg>'
    open(name, 'w', encoding='utf-8').write(HEAD + svg + STRIPS + '</body></html>')


def tiles(w, h, seed, lit=True, keep=None):
    """The site's tile field: 16x8 tiles on a 20x14 pitch. keep(x, y) -> False leaves that spot bare ground."""
    rnd = random.Random(seed)
    out = []
    for y in range(0, h, 14):
        for x in range(0, w, 20):
            if keep and not keep(x, y):
                continue
            r = rnd.random()
            if lit and r < 0.012:
                fill = CURV
            elif lit and r < 0.05:
                fill = DEEP
            elif r < 0.25:
                fill = '#1d2a12'
            elif r < 0.85:
                fill = '#141a0d'
            else:
                continue
            out.append(f'<rect x="{x}" y="{y}" width="16" height="8" fill="{fill}"/>')
    return out


def mark(x, y, k):
    """The chameleon, k screen px per grid square (43 squares across)."""
    return f'<image href="mark.png" x="{x}" y="{y}" width="{43 * k}" height="{43 * k}"/>'


def wordmark(x, y, k):
    """The wordmark, k screen px per grid square (75x14 squares)."""
    return f'<image href="wordmark.png" x="{x}" y="{y}" width="{75 * k}" height="{14 * k}"/>'


def headline(cx, y, plain, green, size=68):
    return (f'<text class="hl strip" x="{cx}" y="{y}" font-size="{size}" text-anchor="middle">'
            f'{plain}<tspan class="c">{green}</tspan></text>')


def caption(cx, y, s, size=28):
    return f'<text class="soft strip" data-pad="10" x="{cx}" y="{y}" font-size="{size}" text-anchor="middle">{s}</text>'


def block(x, y, w, h, fill, edge, sw=2):
    """A flat block with a hard outline drawn inside its own box."""
    return f'<rect x="{x + sw / 2}" y="{y + sw / 2}" width="{w - sw}" height="{h - sw}" fill="{fill}" stroke="{edge}" stroke-width="{sw}"/>'


def window(x, y, w, h, title):
    """The site's pixel window: ink title bar with the name in Silkscreen, cream body, 2px ink edge."""
    bar = 52
    return ''.join([
        block(x, y, w, h, CREAM, INK, 4),
        f'<rect x="{x}" y="{y}" width="{w}" height="{bar}" fill="{INK}"/>',
        f'<text class="tag" x="{x + 20}" y="{y + 35}" font-size="22" fill="{CURV}">{title}</text>',
        f'<rect x="{x + w - 58}" y="{y + 18}" width="16" height="16" fill="none" stroke="{CURV}" stroke-width="2"/>',
        f'<rect x="{x + w - 34}" y="{y + 18}" width="16" height="16" fill="{CURV}"/>',
    ])


def arrow(x1, x2, y, color=CURV):
    """A flat pixel arrow pointing right (or left when x2 < x1)."""
    d = 1 if x2 > x1 else -1
    tip = x2 - d * 28
    lo, hi = sorted([x1, tip])
    return (f'<rect x="{lo}" y="{y - 6}" width="{hi - lo}" height="12" fill="{color}"/>'
            f'<polygon points="{tip},{y - 22} {x2},{y} {tip},{y + 22}" fill="{color}"/>')


# ---------------------------------------------------------------- 1 cover 2000x800
b = tiles(2000, 800, 1, keep=lambda x, y: not (420 <= x < 1580 and 180 <= y < 610))
b.append(f'<rect x="440" y="196" width="1120" height="400" fill="{GROUND}"/>')
k = 5
mw, ww = 43 * k, 75 * 11
x0 = 1000 - (mw + 40 + ww) / 2
b.append(mark(x0, 232, k))
b.append(wordmark(x0 + mw + 40, 232 + (43 * k - 14 * 11) / 2, 11))
b.append('<text class="hl" x="1000" y="540" font-size="62" text-anchor="middle">'
         f'Borrow against a coin that’s <tspan class="c">minutes old.</tspan></text>')
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 priced off the curve 1600x900
b = tiles(1600, 900, 2, lit=False)
b.append(headline(800, 120, 'Priced from its ', 'first block.'))
# HeroCurve's shape, scaled up: a slow start and a steep end.
COLS, ROWS, PX, PY, TW, TH = 20, 16, 44, 30, 36, 18
ox, oy = 800 - COLS * PX / 2 + (PX - TW) / 2, 220
at = 11
b.append(f'<rect x="{ox - 30}" y="{oy - 30}" width="{COLS * PX + 52}" height="{ROWS * PY + 50}" fill="{GROUND}"/>')
for i in range(COLS):
    hgt = max(2, round(2 + (ROWS - 3) * (i / (COLS - 1)) ** 1.6))
    for r in range(ROWS):
        up = ROWS - r
        fill = '#141a0d'
        if up <= hgt:
            if i == at:
                fill = CURV
            elif i < at:
                fill = CURV if up == hgt else DEEP
            else:
                fill = DEEP if up == hgt else EDGE
        b.append(f'<rect x="{ox + i * PX}" y="{oy + r * PY}" width="{TW}" height="{TH}" fill="{fill}"/>')
top = oy + (ROWS - max(2, round(2 + (ROWS - 3) * (at / (COLS - 1)) ** 1.6))) * PY
colx = ox + at * PX + TW / 2
tx, ty = colx - 440, top - 170
b.append(block(tx, ty, 290, 88, GROUND, CURV, 4))
b.append(f'<rect x="{tx + 18}" y="{ty + 26}" width="36" height="36" fill="none" stroke="{CURV}" stroke-width="4"/>')
b.append(f'<text class="txt" x="{tx + 72}" y="{ty + 56}" font-size="30" font-weight="700">muse</text>')
b.append(f'<text class="num" x="{tx + 270}" y="{ty + 56}" font-size="30" text-anchor="end">$5K</text>')
b.append(f'<rect x="{tx + 290}" y="{ty + 41}" width="{colx - tx - 287}" height="6" fill="{CURV}"/>')
b.append(f'<rect x="{colx - 3}" y="{ty + 41}" width="6" height="{top - ty - 51}" fill="{CURV}"/>')
b.append(f'<text class="tag" x="{ox + (COLS - 1) * PX + TW}" y="{oy + 4}" font-size="20" fill="{SOFT}" text-anchor="end">graduates ↑</text>')
b.append(f'<text class="tag" x="{ox}" y="{oy + ROWS * PY + 6}" font-size="20" fill="{SOFT}">mint</text>')
b.append(caption(800, 842, 'Market cap read straight off the bonding curve on chain. No price feed needed.'))
page('02-curve.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 score sets the loan 1600x900
b = tiles(1600, 900, 3, lit=False)
b.append(headline(800, 120, 'The safer it reads, ', 'the more you borrow.', 62))
bands = [('80+', 33), ('65–79', 25), ('50–64', 18), ('35–49', 10)]
x, w, rh, gap, y0 = 170, 1260, 118, 26, 208
b.append(f'<rect x="{x - 26}" y="{y0 - 26}" width="{w + 52}" height="{4 * rh + 3 * gap + 52}" fill="{GROUND}"/>')
for n, (score, pct) in enumerate(bands):
    y = y0 + n * (rh + gap)
    b.append(block(x, y, w, rh, SURFACE, EDGE, 2))
    b.append(f'<text class="soft" x="{x + 36}" y="{y + 72}" font-size="30">score</text>')
    b.append(f'<text class="num" x="{x + 134}" y="{y + 73}" font-size="38">{score}</text>')
    bx, bw = x + 380, 640
    b.append(f'<rect x="{bx}" y="{y + 40}" width="{bw}" height="38" fill="{RAISED}"/>')
    b.append(block(bx, y + 40, bw * pct / 33, 38, CURV, DEEP, 4))
    b.append(f'<text class="num" x="{x + w - 36}" y="{y + 80}" font-size="54" font-weight="700" text-anchor="end">{pct}%</text>')
b.append(caption(800, 842, 'Up to a third of the bag. You see the rate before you borrow.'))
page('03-score.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 keep the bag 1600x900
b = tiles(1600, 900, 4, lit=False)
b.append(headline(800, 120, 'Get SOL. ', 'Keep the bag.'))
W, H, Y = 380, 330, 280
xs = [110, 610, 1110]
b.append(f'<rect x="80" y="{Y - 30}" width="1440" height="{H + 200}" fill="{GROUND}"/>')
b.append(window(xs[0], Y, W, H, 'your bag'))
b.append(window(xs[1], Y, W, H, 'the program'))
b.append(window(xs[2], Y, W, H, 'your wallet'))
# your bag: a stack of coins, drawn as flat pixel slabs
cx = xs[0] + W / 2
for i in range(4):
    sy = Y + 250 - i * 34
    b.append(block(cx - 80, sy, 160, 30, CURV, DEEP, 4))
b.append(f'<text class="txt" x="{cx}" y="{Y + 310}" font-size="26" font-weight="600" text-anchor="middle" style="fill:{INK}">any pump.fun coin</text>')
# the program: a pixel padlock
cx = xs[1] + W / 2
b.append(f'<path d="M{cx - 44} {Y + 170}V{Y + 116}H{cx - 30}V{Y + 102}H{cx + 30}V{Y + 116}H{cx + 44}V{Y + 170}" fill="none" stroke="{INK}" stroke-width="14" stroke-linejoin="miter"/>')
b.append(block(cx - 76, Y + 166, 152, 110, CURV, DEEP, 4))
b.append(f'<rect x="{cx - 10}" y="{Y + 200}" width="20" height="40" fill="{INK}"/>')
b.append(f'<text class="txt" x="{cx}" y="{Y + 310}" font-size="26" font-weight="600" text-anchor="middle" style="fill:{INK}">no admin key</text>')
# your wallet: the SOL
cx = xs[2] + W / 2
b.append(f'<text class="num" x="{cx}" y="{Y + 210}" font-size="72" font-weight="700" text-anchor="middle" style="fill:{INK}">+SOL</text>')
b.append(f'<text class="txt" x="{cx}" y="{Y + 310}" font-size="26" font-weight="600" text-anchor="middle" style="fill:{INK}">yours to use</text>')
b.append(arrow(xs[0] + W + 14, xs[1] - 14, Y + H / 2))
b.append(arrow(xs[1] + W + 14, xs[2] - 14, Y + H / 2))
# the way back: repay and the coins come home
ry = Y + H + 60
b.append(f'<rect x="{xs[2] + W / 2 - 6}" y="{Y + H + 8}" width="12" height="{ry - Y - H - 2}" fill="{SOFT}"/>')
b.append(f'<rect x="{xs[0] + W / 2 + 22}" y="{ry - 6}" width="{xs[2] - xs[0]- 16}" height="12" fill="{SOFT}"/>')
b.append(f'<rect x="{xs[0] + W / 2 - 6}" y="{Y + H + 36}" width="12" height="{ry - Y - H - 30}" fill="{SOFT}"/>')
b.append(f'<polygon points="{xs[0] + W / 2 - 22},{Y + H + 36} {xs[0] + W / 2},{Y + H + 8} {xs[0] + W / 2 + 22},{Y + H + 36}" fill="{SOFT}"/>')
b.append(f'<text class="txt strip" data-pad="12" x="800" y="{ry + 11}" font-size="30" font-weight="600" text-anchor="middle">Pay it back. <tspan class="c">The coins come straight back to you.</tspan></text>')
b.append(caption(800, 842, 'Your coins sit in the on-chain program the whole time. Nothing is sold.'))
page('04-keep.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 closing 1600x900
b = tiles(1600, 900, 5, keep=lambda x, y: not (280 <= x < 1320 and 250 <= y < 660))
b.append(f'<rect x="300" y="264" width="1000" height="382" fill="{GROUND}"/>')
k = 4
mw, ww = 43 * k, 75 * 9
x0 = 800 - (mw + 36 + ww) / 2
b.append(mark(x0, 300, k))
b.append(wordmark(x0 + mw + 36, 300 + (43 * k - 14 * 9) / 2, 9))
b.append('<text class="num c" x="800" y="560" font-size="64" font-weight="700" text-anchor="middle">curv.fund</text>')
b.append(f'<text class="num" x="800" y="615" font-size="28" font-weight="500" text-anchor="middle" style="fill:{SOFT}">$CURV</text>')
page('05-close.html', 1600, 900, b)
print('built')

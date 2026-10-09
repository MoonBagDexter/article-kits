"""Builds each article picture as an HTML page in Fee2Play's look: cream arcade paper, ink stickers
with notched pixel corners and hard shadows, dark screens, pixel sprites. render.py shoots them to PNG.
sprites.json is the site's sprite library exported from the gamepad repo, so this rebuilds without it."""
import json

SP = json.load(open('sprites.json', encoding='utf-8'))

PAPER, PAPER2, PAPER3, CARD = '#f6f1e4', '#ece4d0', '#dcd2b8', '#fffcf4'
INK, INK2, INK3 = '#0b0b0b', '#4a4537', '#6e6753'
YEL, YELHI, YELSH = '#ffd60a', '#ffe873', '#c49e10'
LIME, LIMESH = '#7ef23a', '#4db521'
SCREEN, BEZEL, SINK, SMUTED = '#0e1012', '#2a2f32', '#e6f2df', '#8a9a85'

HEAD = f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Pixelify+Sans:wght@400;700&family=Space+Grotesk:wght@400;500;700&display=block" rel="stylesheet">
<style>
html,body{{margin:0;padding:0;background:{PAPER};overflow:hidden}}
svg{{display:block}}
.disp{{font-family:'Pixelify Sans';font-weight:700;fill:{INK}}}
.txt{{font-family:'Space Grotesk';fill:{INK2}}}
.dim{{font-family:'Space Grotesk';fill:{INK3}}}
.mono{{font-family:'JetBrains Mono';fill:{INK}}}
</style></head><body>'''

DEFS = f'''<defs>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="12" cy="12" r="1.3" fill="{INK}" fill-opacity="0.09"/></pattern>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" fill-opacity="0.18"/></pattern>
</defs>'''


def page(name, w, h, body):
    bg = f'<rect width="{w}" height="{h}" fill="{PAPER}"/><rect width="{w}" height="{h}" fill="url(#dots)"/>'
    html = HEAD + f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{bg}{"".join(body)}</svg></body></html>'
    open(name, 'w', encoding='utf-8').write(html)


def notched(x, y, w, h, n, fill):
    """A rectangle with its four corner pixels (n x n) cut out: the site's notched sticker corner."""
    return (f'<path d="M{x + n} {y}H{x + w - n}V{y + n}H{x + w}V{y + h - n}H{x + w - n}V{y + h}H{x + n}'
            f'V{y + h - n}H{x}V{y + n}H{x + n}Z" fill="{fill}"/>')


def sticker(x, y, w, h, fill=CARD, o=4, sh=8, flat=False):
    """Ink outline OUTSIDE the box, hard offset shadow with no blur, notched corners. Same as the `sticker` utility."""
    out = '' if flat else notched(x - o + sh, y - o + sh, w + 2 * o, h + 2 * o, o, INK)
    return out + notched(x - o, y - o, w + 2 * o, h + 2 * o, o, INK) + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>'


def screen(x, y, w, h, title=None, o=4, sh=8, scan=True):
    """A dark CRT screen sticker with a bezel and a lime mono title bar."""
    b = [sticker(x, y, w, h, BEZEL, o, sh)]
    bar = 0
    if title:
        bar = 46
        b.append(f'<text class="mono" x="{x + 20}" y="{y + 31}" font-size="20" font-weight="700" letter-spacing="2" style="fill:{LIME}">{title}</text>')
    b.append(f'<rect x="{x + 6}" y="{y + 6 + bar}" width="{w - 12}" height="{h - 12 - bar}" fill="{SCREEN}"/>')
    if scan:
        b.append(f'<rect x="{x + 6}" y="{y + 6 + bar}" width="{w - 12}" height="{h - 12 - bar}" fill="url(#scan)"/>')
    return ''.join(b), (x + 6, y + 6 + bar, w - 12, h - 12 - bar)


def sprite(name, x, y, px, rows=None):
    """Draw a site sprite from its pixel rows, one rect per horizontal run of a color."""
    s = SP[name]
    rows = rows or s['rows']
    out = []
    for ry, row in enumerate(rows):
        cx = 0
        while cx < len(row):
            c = row[cx]
            run = 1
            while cx + run < len(row) and row[cx + run] == c:
                run += 1
            if c not in '. ':
                out.append(f'<rect x="{x + cx * px}" y="{y + ry * px}" width="{run * px + 0.3}" height="{px + 0.3}" fill="{s["palette"][c]}"/>')
            cx += run
    return f'<g shape-rendering="crispEdges">{"".join(out)}</g>'


def sprite_size(name, px):
    return SP[name]['w'] * px, SP[name]['h'] * px


def headline(cx, y, plain, gold, size=64, gold_first=False):
    """Pixel-font headline with one phrase on a yellow sticker, like the hero's 'a game'."""
    cw = size * 0.56  # Pixelify Sans average advance, close enough to centre a line
    pw, gw = len(plain) * cw, len(gold) * cw
    gap = size * 0.3
    total = pw + gap + gw + 24
    x0 = cx - total / 2
    parts = []
    if gold_first:
        gx, px_ = x0, x0 + gw + 24 + gap
    else:
        px_, gx = x0, x0 + pw + gap
    parts.append(sticker(gx, y - size * 0.86, gw + 24, size * 1.12, YEL, 3, 5))
    parts.append(f'<text class="disp" x="{gx + 12}" y="{y}" font-size="{size}" textLength="{gw}" lengthAdjust="spacingAndGlyphs">{gold}</text>')
    parts.append(f'<text class="disp" x="{px_}" y="{y}" font-size="{size}" textLength="{pw}" lengthAdjust="spacingAndGlyphs">{plain}</text>')
    return ''.join(parts)


def caption(cx, y, text, size=27):
    return f'<text class="dim" x="{cx}" y="{y}" font-size="{size}" text-anchor="middle">{text}</text>'


# Logo and wordmark PNG sizes (public/brand)
LOGO_W, LOGO_H = 300, 512
WM_W, WM_H = 1200, 310

# ---------------------------------------------------------------- 1 cover 2000x800
b = []
lh = 560
lw = lh * LOGO_W / LOGO_H
wmw = 1060
wmh = wmw * WM_H / WM_W
gx = 1000 - (lw + 70 + wmw) / 2
b.append(f'<image href="logo-512.png" x="{gx}" y="{400 - lh / 2 - 10}" width="{lw}" height="{lh}"/>')
tx = gx + lw + 70
b.append(f'<image href="wordmark-1200.png" x="{tx}" y="150" width="{wmw}" height="{wmh}"/>')
# the hero line, centred under the wordmark
b.append(headline(tx + wmw / 2, 540, 'Every coin is', 'a game', 92))
# the five games, small, in a row
games = ['tplRunner', 'tplFlappy', 'tplSnake', 'tplShooter', 'tplStacker']
tile, gapx = 92, 34
row_w = len(games) * tile + (len(games) - 1) * gapx
sx = tx + wmw / 2 - row_w / 2
for i, g in enumerate(games):
    x = sx + i * (tile + gapx)
    b.append(sticker(x, 625, tile, tile, CARD, 3, 5))
    w, h = sprite_size(g, 5)
    b.append(sprite(g, x + (tile - w) / 2, 625 + (tile - h) / 2, 5))
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 pick a game 1600x900
b = []
b.append(headline(800, 150, 'or pitch your own.', 'Pick a game', 70, gold_first=True))
cards = [('tplRunner', 'Endless runner'), ('tplFlappy', 'Flappy'), ('tplSnake', 'Snake'),
         ('tplShooter', 'Space shooter'), ('tplStacker', 'Tower stacker')]
cw, ch, gap = 380, 230, 50
pos = [(800 - 1.5 * cw - gap + i * (cw + gap), 270) for i in range(3)] + \
      [(800 - 1.5 * cw - gap + i * (cw + gap), 270 + ch + 60) for i in range(3)]
for (g, title), (x, y) in zip(cards, pos):
    b.append(sticker(x, y, cw, ch))
    w, h = sprite_size(g, 9)
    b.append(sprite(g, x + (cw - w) / 2, y + 26 + (112 - h) / 2, 9))
    b.append(f'<text class="disp" x="{x + cw / 2}" y="{y + 190}" font-size="38" text-anchor="middle">{title}</text>')
# sixth tile: your own idea, as a little input
x, y = pos[5]
b.append(sticker(x, y, cw, ch, YEL))
b.append(f'<text class="disp" x="{x + cw / 2}" y="{y + 70}" font-size="38" text-anchor="middle">Your idea</text>')
b.append(sticker(x + 28, y + 108, cw - 56, 80, CARD, 3, 0, flat=True))
b.append(f'<text class="txt" x="{x + 46}" y="{y + 142}" font-size="22" style="fill:{INK}">A frog hops across a</text>')
b.append(f'<text class="txt" x="{x + 46}" y="{y + 172}" font-size="22" style="fill:{INK}">neon swamp at night.</text>')
b.append(f'<rect x="{x + 300}" y="{y + 154}" width="12" height="24" fill="{INK}"/>')
b.append(caption(800, 850, 'Name the coin, launch it with one signature.'))
page('02-pick.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 fees fund it 1600x900
b = []
b.append(headline(800, 150, 'Fees', 'fund the game.', 70))
b.append('<g transform="translate(0 30)">')
# left: a trade
b.append(sticker(110, 330, 300, 250))
b.append(f'<text class="mono" x="140" y="385" font-size="22" font-weight="600" letter-spacing="2" style="fill:{INK3}">EVERY TRADE</text>')
b.append(f'<text class="disp" x="140" y="460" font-size="56">Fees</text>')
b.append(f'<text class="txt" x="140" y="520" font-size="26">from buys and sells</text>')
b.append(f'<text class="txt" x="140" y="554" font-size="26">on pump.fun</text>')
# arrow
for i in range(4):
    b.append(f'<rect x="{445 + i * 26}" y="449" width="14" height="14" fill="{INK}"/>')
b.append(f'<path d="M555 434L585 456L555 478Z" fill="{INK}"/>')
# middle: the 80/20 bar, like the site's FeeSplit
bx, by, bw = 620, 400, 500
seg_gap = 8
seg_w = (bw - 9 * seg_gap) / 10
for i in range(10):
    x = bx + i * (seg_w + seg_gap)
    b.append(sticker(x, by, seg_w, 70, LIME if i < 8 else PAPER2, 3, 0, flat=True))
b.append(f'<text class="mono" x="{bx}" y="{by + 130}" font-size="30" style="fill:{INK2}"><tspan font-weight="700" style="fill:{INK}">80%</tspan> game fund</text>')
b.append(f'<text class="mono" x="{bx + bw}" y="{by + 130}" font-size="30" text-anchor="end" style="fill:{INK2}"><tspan font-weight="700" style="fill:{INK}">20%</tspan> Fee2Play</text>')
b.append(f'<text class="dim" x="{bx + bw / 2}" y="{by - 40}" font-size="26" text-anchor="middle">Split set on pump.fun. Nobody can change it.</text>')
# arrow
for i in range(3):
    b.append(f'<rect x="{1150 + i * 26}" y="429" width="14" height="14" fill="{INK}"/>')
b.append(f'<path d="M1234 414L1264 436L1234 458Z" fill="{INK}"/>')
# right: the $20 kickstart, cabinet waking up
b.append(sticker(1290, 300, 210, 300, YEL))
b.append(f'<text class="disp" x="1395" y="380" font-size="72" text-anchor="middle">$20</text>')
w, h = sprite_size('agent', 8)
b.append(sprite('agent', 1395 - w / 2, 410, 8))
b.append(f'<text class="mono" x="1395" y="578" font-size="20" font-weight="700" text-anchor="middle" letter-spacing="1">AI STARTS</text>')
b.append('</g>')
b.append(caption(800, 760, 'The fund hits $20, the AI starts building. Every fee after that keeps it improving.'))
page('03-fees.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 watch it get built 1600x900
b = []
b.append(headline(800, 150, 'Watch it get', 'built live.', 70))
# left: the agent terminal
s, (ix, iy, iw, ih) = screen(110, 250, 760, 520, 'AGENT')
b.append(s)
b.append(f'<rect x="{110 + 760 - 150}" y="{250 + 13}" width="14" height="14" fill="{LIME}"/>')
b.append(f'<text class="mono" x="{110 + 760 - 128}" y="{250 + 27}" font-size="18" font-weight="700" style="fill:{LIME}">WORKING</text>')
lines = [('agent&gt;', 'reading the brief', SINK), ('agent&gt;', 'drawing the hero', SINK), ('agent&gt;', 'tap to jump, hold to go higher', SINK),
         ('test&gt;', 'played 3 runs, no errors', LIME), ('agent&gt;', 'speed ramps up every 10s', SINK), ('agent&gt;', 'adding a double jump', SINK)]
for i, (p, t, col) in enumerate(lines):
    y = iy + 62 + i * 66
    b.append(f'<text class="mono" x="{ix + 28}" y="{y}" font-size="26"><tspan style="fill:{SMUTED}">{p}</tspan> <tspan style="fill:{col}">{t}</tspan></text>')
b.append(f'<rect x="{ix + 28 + 21 * 15.6 + 128}" y="{iy + 62 + 5 * 66 - 22}" width="14" height="26" fill="{LIME}"/>')
# right: the game screen
s, (gx0, gy0, gw, gh) = screen(940, 250, 550, 520, 'PLAY', scan=False)
b.append(s)
# a tiny runner level: ground, a gap, the runner mid-jump, score
ground_y = gy0 + gh - 90
b.append(f'<rect x="{gx0}" y="{ground_y}" width="{200}" height="90" fill="{BEZEL}"/>')
b.append(f'<rect x="{gx0 + 290}" y="{ground_y}" width="{gw - 290}" height="90" fill="{BEZEL}"/>')
for i in range(0, gw, 40):
    if not (200 <= i < 290):
        b.append(f'<rect x="{gx0 + i}" y="{ground_y}" width="20" height="8" fill="{LIMESH}"/>')
w, h = sprite_size('runner', 8)
b.append(sprite('runner', gx0 + 210, ground_y - h - 120, 8))
b.append(f'<text class="mono" x="{gx0 + gw - 24}" y="{gy0 + 48}" font-size="28" font-weight="700" text-anchor="end" style="fill:{YEL}">SCORE 0420</text>')
b.append(caption(800, 845, 'Every step shows up on the coin\'s page. Only the wallet that launched it can steer.'))
page('04-built.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 closing 1600x900
b = []
lh = 470
lw = lh * LOGO_W / LOGO_H
wmw = 820
wmh = wmw * WM_H / WM_W
x0 = 800 - (lw + 60 + wmw) / 2
b.append(f'<image href="logo-512.png" x="{x0}" y="{430 - lh / 2}" width="{lw}" height="{lh}"/>')
wx = x0 + lw + 60
b.append(f'<image href="wordmark-1200.png" x="{wx}" y="{250}" width="{wmw}" height="{wmh}"/>')
bw_, bh_ = 520, 100
bx_ = wx + wmw / 2 - bw_ / 2
b.append(sticker(bx_, 520, bw_, bh_, YEL, 4, 8))
pw, ph = sprite_size('playArrow', 5)
b.append(sprite('playArrow', bx_ + 46, 520 + (bh_ - ph) / 2, 5))
b.append(f'<text class="disp" x="{bx_ + bw_ / 2 + 26}" y="{520 + 67}" font-size="54" text-anchor="middle">fee2play.fun</text>')
page('05-close.html', 1600, 900, b)
print('built')

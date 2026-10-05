"""Builds each article picture as an HTML page in mintmark's look. tools/render.py shoots them to PNG.

Assets (characters, logo, wordmark, clouds, plane) are copied from mintmark-creator-studio/dist/assets
so this still rebuilds without that repo.
"""
import random

INK, FACE, PAPER, MUTE, LINE, LIME = '#000', '#0b0b0b', '#fff', '#8a8a8a', '#2a2a2a', '#C6F24E'

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Silkscreen:wght@400;700&display=block" rel="stylesheet">
<style>
html,body{margin:0;padding:0;background:#000;overflow:hidden}
svg{display:block}
image{image-rendering:pixelated}
.disp{font-family:Silkscreen;fill:#fff;letter-spacing:.04em}
.lbl{font-family:Silkscreen;fill:#8a8a8a;letter-spacing:.14em}
.txt{font-family:'IBM Plex Mono';fill:#d6d6d6}
.dim{font-family:'IBM Plex Mono';fill:#8a8a8a}
.lime{fill:#C6F24E}
.ink{fill:#000}
</style></head><body>'''


def page(name, w, h, body, stars=True):
    bg = star_field(w, h) if stars else ''
    html = HEAD + f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges"><rect width="{w}" height="{h}" fill="{INK}"/>{bg}{"".join(body)}</svg></body></html>'
    open(name, 'w', encoding='utf-8').write(html)


def star_field(w, h, n=None):
    """Sparse plus-sign stars and dots, like the site's .sky layer."""
    rnd = random.Random(w * 7 + h)
    out = []
    for _ in range(n or w * h // 26000):
        x, y = rnd.randrange(0, w, 2), rnd.randrange(0, h, 2)
        c = rnd.choice(['#444', '#5a5a5a', '#707070', '#909090'])
        if rnd.random() < 0.45:
            s = rnd.choice([3, 4])
            out.append(f'<path d="M{x} {y - s * 2}h{s}v{s * 5}h-{s}zM{x - s * 2} {y}h{s * 5}v{s}h-{s * 5}z" fill="{c}"/>')
        else:
            out.append(f'<rect x="{x}" y="{y}" width="4" height="4" fill="{c}"/>')
    return ''.join(out)


def stamp(x, y, w, h, face=FACE, rim=PAPER, edge=6, hole=6, perf=18, selected=False):
    """Perforated postage-stamp card: paper rim, square holes along the edge, optional lime pixel."""
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{rim}"/>',
           f'<rect x="{x + edge}" y="{y + edge}" width="{w - 2 * edge}" height="{h - 2 * edge}" fill="{face}"/>']
    nx, ny = max(2, round(w / perf)), max(2, round(h / perf))
    for i in range(nx + 1):
        px = x + i * w / nx - hole / 2
        out.append(f'<rect x="{px:.1f}" y="{y - hole / 2}" width="{hole}" height="{hole}" fill="{INK}"/>')
        out.append(f'<rect x="{px:.1f}" y="{y + h - hole / 2}" width="{hole}" height="{hole}" fill="{INK}"/>')
    for j in range(1, ny):
        py = y + j * h / ny - hole / 2
        out.append(f'<rect x="{x - hole / 2}" y="{py:.1f}" width="{hole}" height="{hole}" fill="{INK}"/>')
        out.append(f'<rect x="{x + w - hole / 2}" y="{py:.1f}" width="{hole}" height="{hole}" fill="{INK}"/>')
    if selected:
        out.append(f'<rect x="{x + w + 8}" y="{y - 26}" width="18" height="18" fill="{LIME}"/>')
    return ''.join(out)


def img(file, x, y, w, h):
    return f'<image href="{file}" x="{x}" y="{y}" width="{w}" height="{h}"/>'


def minted(cx, cy, size=1.0, day=''):
    """The lime 'minted' ink stamp, tilted."""
    w, h = 190 * size, 74 * size
    t = f'<text class="disp lime" x="0" y="{8 * size}" font-size="{30 * size}" text-anchor="middle">minted</text>'
    if day:
        t = (f'<text class="disp lime" x="0" y="{2 * size}" font-size="{28 * size}" text-anchor="middle">minted</text>'
             f'<text class="lbl" style="fill:{LIME}" x="0" y="{26 * size}" font-size="{14 * size}" text-anchor="middle">{day}</text>')
    return (f'<g transform="translate({cx} {cy}) rotate(-12)">'
            f'<rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" fill="none" stroke="{LIME}" stroke-width="{5 * size}"/>{t}</g>')


def dither_rule(x, y, w):
    """The site's 10px checker divider, fading to sparse dots."""
    out = []
    for i in range(0, int(w), 4):
        out.append(f'<rect x="{x + i}" y="{y + (i // 2) % 4}" width="2" height="2" fill="{PAPER}"/>')
        if i % 8 == 0:
            out.append(f'<rect x="{x + i + 2}" y="{y + 6}" width="2" height="2" fill="{PAPER}" opacity=".6"/>')
    return ''.join(out)


def headline(x, y, parts, size=62, anchor='middle'):
    spans = ''.join(f'<tspan class="lime">{t[1:]}</tspan>' if t.startswith('*') else t for t in parts)
    return f'<text class="disp" x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{spans}</text>'


def label(x, y, text, size=20, anchor='start', dot=True):
    d = f'<rect x="{x - 26}" y="{y - size * .72}" width="{size * .6}" height="{size * .6}" fill="{LIME}"/>' if dot and anchor == 'start' else ''
    return d + f'<text class="lbl" x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{text.upper()}</text>'


# ---------------------------------------------------------------- 1 cover 2000x800
b = []
b.append(img('clouds.png', 0, 590, 1000, 400))
b.append(img('clouds.png', 1000, 590, 1000, 400))
# logo + wordmark on the left
b.append(img('logo.png', 60, 60, 300, 301))
b.append(img('wordmark.png', 300, 32, 760, 357))
b.append(headline(140, 440, ['your coin has a chart.'], size=50, anchor='start'))
b.append(headline(140, 510, ['give it a ', '*voice.'], size=50, anchor='start'))
# three character stamps on the right, the fox selected
chars = [('char-frog.png', 1150, 200, False), ('char-bot.png', 1770, 200, False), ('char-fox.png', 1410, 140, True)]
for f, x, y, sel in chars:
    s = 300 if sel else 190
    b.append(stamp(x - 20, y - 20, s + 40, s + 40, selected=sel, edge=7, hole=7, perf=20))
    b.append(img(f, x, y, s, s))
b.append(minted(1640, 480, 1.2, 'mon'))
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 the cast 1600x900
b = []
b.append(headline(800, 130, ['pick ', "*who's posting."]))
cast = [('char-fox.png', 'fox', 'volt', 'the sharp-tongued', 'signal hunter.', True),
        ('char-frog.png', 'frog', 'ripple', 'the unbothered', 'community spark.', False),
        ('char-bot.png', 'bot', 'node', 'the analytic', 'chaos machine.', False)]
cw, gap = 420, 70
x0 = (1600 - 3 * cw - 2 * gap) / 2
for i, (f, name, default, t1, t2, sel) in enumerate(cast):
    x = x0 + i * (cw + gap)
    y = 210
    b.append(stamp(x, y, cw, 560, selected=sel))
    b.append(img(f, x + 50, y + 34, 320, 320))
    b.append(label(x + 56, y + 400, f'the {name} · "{default}"', size=17))
    b.append(f'<text class="disp" x="{x + 30}" y="{y + 452}" font-size="44">{name}</text>')
    b.append(f'<text class="txt" x="{x + 30}" y="{y + 494}" font-size="24">{t1}</text>')
    b.append(f'<text class="txt" x="{x + 30}" y="{y + 528}" font-size="24">{t2}</text>')
b.append('<text class="dim" x="800" y="852" font-size="26" text-anchor="middle">Rename it. Add your ticker. It\'s yours.</text>')
page('02-cast.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 the voice 1600x900
b = []
b.append(headline(800, 130, ['three dials. ', '*one voice.']))
# dial panel
px, py, pw, ph = 110, 210, 640, 580
b.append(stamp(px, py, pw, ph))
b.append(label(px + 70, py + 76, 'voice', size=20))
dials = [('humor', 70), ('edge', 45), ('signal', 75)]
for i, (k, v) in enumerate(dials):
    y = py + 160 + i * 100
    b.append(f'<text class="disp" x="{px + 44}" y="{y + 14}" font-size="28">{k}</text>')
    tx, tw = px + 220, 300
    b.append(f'<rect x="{tx}" y="{y - 6}" width="{tw}" height="22" fill="none" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<rect x="{tx + 6}" y="{y}" width="{(tw - 12) * v / 100:.0f}" height="10" fill="{LIME}"/>')
    b.append(f'<rect x="{tx + (tw - 12) * v / 100 - 4:.0f}" y="{y - 14}" width="16" height="38" fill="{PAPER}"/>')
    b.append(f'<text class="txt" x="{px + pw - 44}" y="{y + 14}" font-size="28" text-anchor="end" style="fill:#fff">{v}</text>')
b.append(dither_rule(px + 40, py + 450, pw - 80))
b.append(label(px + 70, py + 504, 'never says', size=17))
cx = px + 40
for word in ['moonshot', 'guaranteed gains', 'financial advice']:  # the studio's default banned words
    cw = len(word) * 10.8 + 24
    b.append(f'<rect x="{cx}" y="{py + 522}" width="{cw:.0f}" height="40" fill="none" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<text class="dim" x="{cx + cw / 2:.0f}" y="{py + 549}" font-size="18" text-anchor="middle" text-decoration="line-through">{word}</text>')
    cx += cw + 14
# arrow
b.append(f'<path d="M790 500h60" stroke="{LIME}" stroke-width="8"/><path d="M850 484l18 16-18 16z" fill="{LIME}"/>')
# sample post
sx, sy, sw, sh = 900, 260, 600, 480
b.append(stamp(sx, sy, sw, sh, selected=True))
b.append(stamp(sx + 34, sy + 34, 84, 84, edge=3, hole=3, perf=10))
b.append(img('char-fox.png', sx + 40, sy + 40, 72, 72))
b.append(f'<text class="txt" x="{sx + 140}" y="{sy + 70}" font-size="26" font-weight="600" style="fill:#fff">Volt</text>')
b.append(f'<text class="dim" x="{sx + 140}" y="{sy + 104}" font-size="22">$VOLT · mon 09:15</text>')
post = ['Volt checked the timeline.', 'Still early. Still loud.', 'Still building.', '', 'This week: less noise,', 'more signal. $VOLT']
for k, line in enumerate(post):
    b.append(f'<text class="txt" x="{sx + 40}" y="{sy + 180 + k * 40}" font-size="27">{line}</text>')
b.append(f'<text class="dim" x="{sx + 40}" y="{sy + sh - 36}" font-size="20">110 / 280</text>')
b.append(minted(sx + sw - 120, sy + sh - 66, 0.9, 'mon'))
b.append('<text class="dim" x="800" y="862" font-size="26" text-anchor="middle">Every post comes out in that one voice.</text>')
page('03-voice.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 the week 1600x900
b = []
b.append(headline(800, 130, ['7 posts. ', '*7 cards.']))
days = [('mon', 'the signal', 'is back', True, 'ink'), ('tue', 'pick a', 'side', False, 'paper'),
        ('wed', 'stay', 'curious', True, 'ink'), ('thu', 'show the', 'receipts', True, 'ink'),
        ('fri', 'log off?', 'never', False, 'paper'), ('sat', 'built', 'different', True, 'ink'),
        ('sun', 'next week', 'loading', False, 'ink')]
dw, dg = 190, 22
x0 = (1600 - 7 * dw - 6 * dg) / 2
for i, (d, h1, h2, done, tone) in enumerate(days):
    x, y = x0 + i * (dw + dg), 230 + (i % 2) * 40
    paper = tone == 'paper'
    b.append(stamp(x, y, dw, 440, face=PAPER if paper else FACE, edge=5, hole=5, perf=16))
    b.append(img('char-fox.png', x + 25, y + 24, 140, 140))
    fill = 'ink' if paper else ''
    b.append(f'<text class="disp {fill}" x="{x + dw / 2}" y="{y + 210}" font-size="20" text-anchor="middle">{h1}</text>')
    b.append(f'<text class="disp {fill}" x="{x + dw / 2}" y="{y + 238}" font-size="20" text-anchor="middle">{h2}</text>')
    chip_c = INK if paper else PAPER
    b.append(f'<rect x="{x + 45}" y="{y + 258}" width="100" height="32" fill="none" stroke="{chip_c}" stroke-width="2"/>')
    b.append(f'<text class="txt" x="{x + dw / 2}" y="{y + 281}" font-size="17" text-anchor="middle" style="fill:{chip_c}">$VOLT</text>')
    b.append(f'<text class="lbl" x="{x + dw / 2}" y="{y + 346}" font-size="22" text-anchor="middle" style="fill:{"#555" if paper else MUTE}">{d.upper()}</text>')
    if done:
        b.append(minted(x + dw / 2, y + 396, 0.62))
    else:
        b.append(f'<text class="dim" x="{x + dw / 2}" y="{y + 402}" font-size="18" text-anchor="middle" style="fill:{"#555" if paper else MUTE}">draft</text>')
b.append('<text class="dim" x="800" y="822" font-size="26" text-anchor="middle">Edit anything. Stamp the ones you ship.</text>')
page('04-week.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 closing 1600x900
b = []
b.append(img('clouds.png', 0, 560, 1600, 640))
b.append(img('plane.png', 1180, 150, 192, 118))
b.append(img('logo.png', 150, 180, 300, 301))
b.append(img('wordmark.png', 380, 150, 760, 357))
b.append(headline(800, 560, ['one coin. one voice. ', '*every day.'], size=48))
b.append(f'<rect x="530" y="616" width="540" height="84" fill="{LIME}"/>')
b.append('<text class="disp ink" x="800" y="672" font-size="38" text-anchor="middle">mintmark.world</text>')
page('05-close.html', 1600, 900, b)
print('built')

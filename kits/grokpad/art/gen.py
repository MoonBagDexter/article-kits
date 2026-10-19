"""Builds each article picture as an HTML page in Grokpad's look. tools/render.py shoots them to PNG.

Colours, fonts and logos come from the grok-launcher redesign (frontend worktree: globals.css, docs/BRAND.md,
public/brand): LED white on true black, Urbanist + Doto + JetBrains Mono (the Grokpad font kit), the logo's lime as the one accent.
"""

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700&family=Doto:ROND,wght@0..100,100..900&family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet">
<style>
html,body{margin:0;padding:0;background:#000000;overflow:hidden}
svg{display:block}
.disp{font-family:Urbanist;font-weight:700;fill:#f4f6ee;letter-spacing:-0.03em}
.txt{font-family:Urbanist;fill:#f4f6ee}
.muted{font-family:Urbanist;fill:rgb(244 246 238 / 0.6)}
.dim{font-family:Urbanist;fill:rgb(244 246 238 / 0.38)}
.mono{font-family:'JetBrains Mono';fill:#f4f6ee}
.lime{fill:#a6ec0d}
.led{fill:#f4f6ee;font-family:Doto;font-variation-settings:'ROND' 100;font-weight:900}
.led.lime{fill:#a6ec0d}
.pct{font-family:Urbanist;font-weight:700;font-variation-settings:normal}
.glow{filter:drop-shadow(0 0 10px #5aab04)}
.panel{fill:#0a0a0a;stroke:rgb(255 255 255 / 0.15);stroke-width:2}
.panel-lit{fill:#0d1306;stroke:#a6ec0d;stroke-width:3}
.wire{fill:none;stroke:#a6ec0d;stroke-width:5;stroke-linecap:round}
.wire-dim{fill:none;stroke:rgb(255 255 255 / 0.22);stroke-width:4;stroke-linecap:round}
.dash{fill:none;stroke:#a6ec0d;stroke-width:5;stroke-dasharray:2 16;stroke-linecap:round}
</style></head><body>'''

DEFS = '''<defs>
<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#5aab04" stop-opacity="0.22"/><stop offset="1" stop-color="#a6ec0d" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="14" cy="14" r="1.4" fill="#ffffff" fill-opacity="0.075"/></pattern>
</defs>'''

LIME = '#a6ec0d'
URL = 'grokpad.org'


def page(name, w, h, body):
    html = HEAD + f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}<rect width="{w}" height="{h}" fill="url(#dots)"/>{"".join(body)}</svg></body></html>'
    open(name, 'w', encoding='utf-8').write(html)


def mark(cx, cy, size, glow=True):
    g = f'<circle cx="{cx}" cy="{cy}" r="{size * 0.85}" fill="url(#glow)"/>' if glow else ''
    return g + f'<image href="logo.png" x="{cx - size / 2}" y="{cy - size / 2}" width="{size}" height="{size}"/>'


def panel(x, y, w, h, r=20, lit=False):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" class="{"panel-lit" if lit else "panel"}"/>'


def lockup(cx, cy, h, glow=True):
    """The real logo + LED wordmark (public/brand/lockup.png, 1511x406), centred."""
    w = h * 1511 / 406
    g = f'<ellipse cx="{cx}" cy="{cy}" rx="{w * 0.62}" ry="{h * 0.95}" fill="url(#glow)"/>' if glow else ''
    return g + f'<image href="lockup.png" x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}"/>'


# ---------------------------------------------------------------- 1 cover 2000x800
b = [lockup(1000, 245, 250)]
# the Grok prompt bar, mid-launch
bx, by, bw, bh = 520, 450, 960, 112
b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="20" fill="#0a0a0a" stroke="{LIME}" stroke-width="3"/>')
b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="20" fill="none" stroke="{LIME}" stroke-width="10" stroke-opacity="0.12"/>')
b.append(f'<text class="mono" x="{bx + 44}" y="{by + 70}" font-size="40">hey grok, launch my coin<tspan class="lime">▍</tspan></text>')
b.append(f'<circle cx="{bx + bw - 58}" cy="{by + bh / 2}" r="36" fill="{LIME}"/>')
b.append(f'<path d="M{bx + bw - 58} {by + bh / 2 + 16}V{by + bh / 2 - 16}M{bx + bw - 72} {by + bh / 2 - 2}L{bx + bw - 58} {by + bh / 2 - 16}L{bx + bw - 44} {by + bh / 2 - 2}" fill="none" stroke="#000" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
b.append('<text class="disp" x="1000" y="680" font-size="58" text-anchor="middle">Launch coins. <tspan class="lime">Just ask Grok.</tspan></text>')
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 plug in 1600x900
b = ['<text class="disp" x="800" y="132" font-size="62" text-anchor="middle">One tap. <tspan class="lime">You’re in.</tspan></text>']
xs = [300, 800, 1300]
cy = 450
for a, c in zip(xs, xs[1:]):
    b.append(f'<path class="dash" d="M{a + 175} {cy}H{c - 175}"/>')
# 1: the button
b.append(panel(xs[0] - 175, cy - 150, 350, 300))
b.append(f'<rect x="{xs[0] - 125}" y="{cy - 40}" width="250" height="80" rx="16" fill="#f4f6ee"/>')
b.append(f'<text class="txt" x="{xs[0]}" y="{cy + 12}" font-size="28" font-weight="600" text-anchor="middle" style="fill:#000000">Get my Grok link</text>')
# 2: grokpad plugged into grok
b.append(panel(xs[1] - 175, cy - 150, 350, 300))
b.append(mark(xs[1] - 80, cy - 10, 110, glow=False))
b.append(f'<path class="wire" d="M{xs[1] - 20} {cy - 10}H{xs[1] + 30}"/>')
b.append(f'<text class="disp" x="{xs[1] + 90}" y="{cy + 6}" font-size="46" text-anchor="middle">grok</text>')
b.append(f'<text class="mono lime" x="{xs[1]}" y="{cy + 98}" font-size="22" text-anchor="middle">● connected</text>')
# 3: free
b.append(panel(xs[2] - 175, cy - 150, 350, 300, lit=True))
b.append(f'<text class="led lime glow" x="{xs[2] + 4}" y="{cy + 30}" font-size="84" text-anchor="middle">FREE</text>')
steps = [('Grab your link', 'one tap, no sign-up'), ('Add it to Grok', 'done, that’s the setup'), ('Launch free', 'nothing to deposit')]
for x, (a, c) in zip(xs, steps):
    b.append(f'<text class="txt" x="{x}" y="{cy + 228}" font-size="36" font-weight="600" text-anchor="middle">{a}</text>')
    b.append(f'<text class="muted" x="{x}" y="{cy + 274}" font-size="27" text-anchor="middle">{c}</text>')
page('02-setup.html', 1600, 900, b)

# ---------------------------------------------------------------- 3 then ask 1600x900
b = ['<text class="disp" x="800" y="132" font-size="62" text-anchor="middle">Then just <tspan class="lime">ask.</tspan></text>']
px, py, pw, ph = 230, 210, 1140, 560
b.append(panel(px, py, pw, ph, 28))
lx = px + 60
b.append(f'<text class="mono" x="{lx}" y="{py + 80}" font-size="26" style="fill:rgb(244 246 238 / 0.38)">you</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 128}" font-size="34">launch Moon Cat, ticker MCAT</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 212}" font-size="26" style="fill:rgb(244 246 238 / 0.38)">grok</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 260}" font-size="31" style="fill:rgb(244 246 238 / 0.6)"><tspan style="fill:#f4f6ee">Moon Cat ($MCAT)</tspan> is live on pump.fun.</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 304}" font-size="31" style="fill:rgb(244 246 238 / 0.6)">Share it and let it run.</text>')
# coin card
cx0, cy0, cw0, ch0 = lx, py + 350, pw - 120, 160
b.append(panel(cx0, cy0, cw0, ch0, 20, lit=True))
ax, ay = cx0 + 90, cy0 + ch0 / 2
b.append(f'<circle cx="{ax}" cy="{ay}" r="52" fill="#000" stroke="{LIME}" stroke-width="3"/>')
b.append(f'<text class="led lime" x="{ax}" y="{ay + 14}" font-size="40" text-anchor="middle">MC</text>')
b.append(f'<text class="disp" x="{ax + 80}" y="{ay - 4}" font-size="48">Moon Cat</text>')
b.append(f'<text class="mono" x="{ax + 82}" y="{ay + 40}" font-size="26" style="fill:rgb(244 246 238 / 0.6)">$MCAT · on pump.fun</text>')
b.append(f'<text class="led lime glow" x="{cx0 + cw0 - 40}" y="{ay + 26}" font-size="72" text-anchor="end">LIVE</text>')
b.append('<text class="dim" x="800" y="850" font-size="27" text-anchor="middle">No forms. No wallet pop-ups.</text>')
page('03-ask.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 say it again 1600x900
b = ['<text class="disp" x="800" y="132" font-size="62" text-anchor="middle">Got another one? <tspan class="lime">Say it again.</tspan></text>']
coins = [('MC', 'Moon Cat', '$MCAT', 'launch Moon Cat, ticker MCAT'),
         ('GD', 'Grok Dog', '$GDOG', 'launch Grok Dog, ticker GDOG'),
         ('SF', 'Space Frog', '$FROG', 'launch Space Frog, ticker FROG')]
rx, rw, rh, gap = 230, 1140, 150, 28
ry = 215
for i, (ini, name, tick, ask) in enumerate(coins):
    y = ry + i * (rh + gap)
    lit = i == len(coins) - 1
    b.append(panel(rx, y, rw, rh, 20, lit=lit))
    ax, ay = rx + 85, y + rh / 2
    b.append(f'<circle cx="{ax}" cy="{ay}" r="48" fill="#000" stroke="{LIME}" stroke-width="3"/>')
    b.append(f'<text class="led lime" x="{ax + 2}" y="{ay + 13}" font-size="36" text-anchor="middle">{ini}</text>')
    b.append(f'<text class="disp" x="{ax + 76}" y="{ay - 2}" font-size="44">{name}</text>')
    b.append(f'<text class="mono" x="{ax + 78}" y="{ay + 38}" font-size="24" style="fill:rgb(244 246 238 / 0.5)">“{ask}”</text>')
    b.append(f'<text class="led lime glow" x="{rx + rw - 40}" y="{ay + 22}" font-size="64" text-anchor="end">LIVE</text>')
b.append('<text class="dim" x="800" y="805" font-size="30" text-anchor="middle">See a meme. Say the word. <tspan style="fill:#f4f6ee">It’s live in seconds.</tspan></text>')
page('04-again.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 close 1600x900
b = [lockup(800, 370, 300)]
b.append(f'<text class="mono lime" x="800" y="650" font-size="40" font-weight="500" text-anchor="middle">{URL}</text>')
b.append('<text class="muted" x="800" y="720" font-size="34" text-anchor="middle">Just ask <tspan class="lime">Grok.</tspan></text>')
page('05-close.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 close, with the CA (the article's "with CA" version)
CA = 'CvUfTWZG9cyFy2cQdK6TGypxAYu1LuEu2MgunrKzpump'
b = [lockup(800, 330, 280)]
b.append(f'<text class="mono lime" x="800" y="590" font-size="40" font-weight="500" text-anchor="middle">{URL}</text>')
b.append('<text class="muted" x="800" y="655" font-size="34" text-anchor="middle">Just ask <tspan class="lime">Grok.</tspan></text>')
b.append(panel(250, 720, 1100, 84, 14))
b.append(f'<text class="mono" x="800" y="773" font-size="30" text-anchor="middle"><tspan style="fill:rgb(244 246 238 / 0.38)">CA  </tspan>{CA}</text>')
page('05-close-ca.html', 1600, 900, b)
print('built')

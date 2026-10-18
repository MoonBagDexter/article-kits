"""Builds each article picture as an HTML page in Grokpad's look. tools/render.py shoots them to PNG.

Colours, fonts and logos come from the grok-launcher redesign (frontend worktree: globals.css, docs/BRAND.md,
public/brand): LED white on true black, Geist + JetBrains Mono, the logo's lime as the one accent.
"""

HEAD = '''<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=block" rel="stylesheet">
<style>
html,body{margin:0;padding:0;background:#000000;overflow:hidden}
svg{display:block}
.disp{font-family:Geist;font-weight:600;fill:#f4f6ee;letter-spacing:-0.04em}
.txt{font-family:Geist;fill:#f4f6ee}
.muted{font-family:Geist;fill:rgb(244 246 238 / 0.6)}
.dim{font-family:Geist;fill:rgb(244 246 238 / 0.38)}
.mono{font-family:'JetBrains Mono';fill:#f4f6ee}
.lime{fill:#a6ec0d}
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
b = [lockup(1000, 350, 340)]
b.append('<text class="muted" x="1000" y="640" font-size="52" text-anchor="middle" font-weight="500">Launch coins by <tspan class="lime">asking Grok.</tspan></text>')
page('01-cover.html', 2000, 800, b)

# ---------------------------------------------------------------- 2 set it up 1600x900
b = ['<text class="disp" x="800" y="132" font-size="62" text-anchor="middle">Set it up <tspan class="lime">once.</tspan></text>']
xs = [300, 800, 1300]
cy = 450
for a, c in zip(xs, xs[1:]):
    b.append(f'<path class="dash" d="M{a + 175} {cy}H{c - 175}"/>')
# 1: the link
b.append(panel(xs[0] - 175, cy - 150, 350, 300))
b.append(f'<rect x="{xs[0] - 125}" y="{cy - 40}" width="250" height="80" rx="16" fill="#f4f6ee"/>')
b.append(f'<text class="txt" x="{xs[0]}" y="{cy + 12}" font-size="28" font-weight="600" text-anchor="middle" style="fill:#000000">Get my Grok link</text>')
b.append(f'<text class="mono" x="{xs[0]}" y="{cy - 82}" font-size="22" text-anchor="middle" style="fill:rgb(244 246 238 / 0.38)">grokpad</text>')
b.append(f'<text class="mono lime" x="{xs[0]}" y="{cy + 100}" font-size="22" text-anchor="middle">/mcp/••••••••</text>')
# 2: Grok connectors
b.append(panel(xs[1] - 175, cy - 150, 350, 300))
b.append(f'<text class="mono" x="{xs[1] - 135}" y="{cy - 88}" font-size="22" style="fill:rgb(244 246 238 / 0.38)">Connectors</text>')
b.append(f'<rect x="{xs[1] - 135}" y="{cy - 56}" width="270" height="64" rx="12" fill="#121212" stroke="rgb(255 255 255 / 0.15)" stroke-width="2"/>')
b.append(f'<text class="mono lime" x="{xs[1] - 115}" y="{cy - 15}" font-size="21">https://…/mcp/•••</text>')
b.append(f'<rect x="{xs[1] - 135}" y="{cy + 30}" width="270" height="64" rx="12" fill="none" stroke="{LIME}" stroke-width="3"/>')
b.append(f'<text class="txt" x="{xs[1]}" y="{cy + 71}" font-size="26" font-weight="600" text-anchor="middle">+ Add Connector</text>')
# 3: fund
b.append(panel(xs[2] - 175, cy - 150, 350, 300, lit=True))
b.append(f'<text class="mono" x="{xs[2]}" y="{cy - 82}" font-size="22" text-anchor="middle" style="fill:rgb(244 246 238 / 0.38)">launch wallet</text>')
b.append(f'<text class="mono lime" x="{xs[2]}" y="{cy + 20}" font-size="60" font-weight="700" text-anchor="middle">+0.1 SOL</text>')
b.append(f'<text class="mono" x="{xs[2]}" y="{cy + 92}" font-size="22" text-anchor="middle" style="fill:rgb(244 246 238 / 0.6)">launch ≈ 0.02 SOL</text>')
steps = [('Get your link', 'one tap, no sign-up'), ('Add it to Grok', 'paste it in Connectors'), ('Fund your wallet', 'just what you’ll launch with')]
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
b.append(f'<text class="mono" x="{lx}" y="{py + 128}" font-size="31">launch a coin called Moon Cat, ticker MCAT,</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 172}" font-size="31">about a cat that lives on the moon</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 256}" font-size="26" style="fill:rgb(244 246 238 / 0.38)">grok</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 304}" font-size="31" style="fill:rgb(244 246 238 / 0.6)">Done. <tspan style="fill:#f4f6ee">Moon Cat ($MCAT)</tspan> is live on pump.fun:</text>')
b.append(f'<text class="mono lime" x="{lx}" y="{py + 348}" font-size="31">pump.fun/coin/7xKp…pump</text>')
b.append(f'<text class="mono" x="{lx}" y="{py + 392}" font-size="31" style="fill:rgb(244 246 238 / 0.6)">Creator fees are locked: 80% to you, 20% to Grokpad.</text>')
chips = ['“what’s my balance?”', '“sell my MCAT”', '“withdraw to my wallet”']
cw = [330, 270, 380]
gap = 24
x = px + (pw - (sum(cw) + gap * 2)) / 2
for c, w in zip(chips, cw):
    b.append(f'<rect x="{x}" y="{py + 450}" width="{w}" height="64" rx="32" fill="#121212" stroke="rgb(255 255 255 / 0.15)" stroke-width="2"/>')
    b.append(f'<text class="mono" x="{x + w / 2}" y="{py + 491}" font-size="23" text-anchor="middle" style="fill:rgb(244 246 238 / 0.6)">{c}</text>')
    x += w + gap
b.append('<text class="dim" x="800" y="850" font-size="27" text-anchor="middle">No wallet pop-ups. No forms.</text>')
page('03-ask.html', 1600, 900, b)

# ---------------------------------------------------------------- 4 the fees 1600x900
b = ['<text class="disp" x="800" y="132" font-size="62" text-anchor="middle"><tspan class="lime">80%</tspan> of the fees are yours.</text>']
cy = 480
b.append(panel(110, cy - 110, 360, 220))
b.append(f'<text class="muted" x="150" y="{cy - 40}" font-size="28">Creator fees</text>')
b.append(f'<text class="mono" x="150" y="{cy + 26}" font-size="50" font-weight="700">$MCAT</text>')
b.append(f'<text class="dim" x="150" y="{cy + 72}" font-size="25">every trade, forever</text>')
b.append(f'<path class="wire" d="M470 {cy}H640"/>')
b.append(mark(760, cy, 230))
# 80 branch
y1, y2 = 330, 650
b.append(f'<path d="M870 {cy} C960 {cy} 960 {y1} 1050 {y1}" fill="none" stroke="{LIME}" stroke-width="12" stroke-linecap="round"/>')
b.append(f'<path d="M870 {cy} C960 {cy} 960 {y2} 1050 {y2}" class="wire-dim"/>')
b.append(panel(1050, y1 - 95, 440, 190, lit=True))
b.append(f'<text class="mono lime" x="1090" y="{y1 + 34}" font-size="96" font-weight="700">80%</text>')
b.append(f'<text class="txt" x="1450" y="{y1 - 6}" font-size="32" font-weight="600" text-anchor="end">You</text>')
b.append(f'<text class="muted" x="1450" y="{y1 + 34}" font-size="25" text-anchor="end">your wallet</text>')
b.append(panel(1050, y2 - 80, 440, 160))
b.append(f'<text class="mono" x="1090" y="{y2 + 24}" font-size="70" font-weight="700" style="fill:rgb(244 246 238 / 0.6)">20%</text>')
b.append(f'<text class="txt" x="1450" y="{y2 + 10}" font-size="32" font-weight="600" text-anchor="end" style="fill:rgb(244 246 238 / 0.6)">Grokpad</text>')
b.append('<text class="dim" x="800" y="840" font-size="27" text-anchor="middle">Locked on pump.fun’s fee program at launch. Nobody can change it, us included.</text>')
page('04-fees.html', 1600, 900, b)

# ---------------------------------------------------------------- 5 close 1600x900
b = [lockup(800, 370, 300)]
b.append(f'<text class="mono lime" x="800" y="650" font-size="40" font-weight="500" text-anchor="middle">{URL}</text>')
b.append('<text class="muted" x="800" y="720" font-size="32" text-anchor="middle">Say it. It’s live.</text>')
page('05-close.html', 1600, 900, b)
print('built')
